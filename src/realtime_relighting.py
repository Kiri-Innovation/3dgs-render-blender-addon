"""Shared realtime relighting and shadow support for the Gaussian renderers."""

import math
import os
import shutil
import tempfile

import bpy
import gpu
import numpy as np
from gpu_extras.batch import batch_for_shader
from mathutils import Euler, Matrix, Quaternion, Vector


MAX_LIGHTS = 16
MAX_SHADOW_LIGHTS = 4
WORLD_SH_COEFFICIENTS = 9
SHADOW_ROWS_PER_MAP = 13
WORLD_DATA_START = MAX_LIGHTS
GLOBAL_DATA_START = WORLD_DATA_START + WORLD_SH_COEFFICIENTS
SHADOW_DATA_START = GLOBAL_DATA_START + 2
RELIGHT_DATA_ROWS = SHADOW_DATA_START + MAX_SHADOW_LIGHTS * SHADOW_ROWS_PER_MAP


def _area_light_radius(light, matrix_world=None):
    """Return an equal-area disk radius, including object scale when available."""
    if matrix_world is not None:
        try:
            area = max(float(light.area(matrix_world=matrix_world)), 0.0)
            if area > 0.0:
                return math.sqrt(area / math.pi)
        except (AttributeError, TypeError):
            pass
    size_x = max(float(light.size), 0.0)
    size_y = size_x
    if light.shape in {"RECTANGLE", "ELLIPSE"}:
        size_y = max(float(light.size_y), 0.0)
    if light.shape in {"DISK", "ELLIPSE"}:
        return 0.5 * math.sqrt(size_x * size_y)
    return math.sqrt(size_x * size_y / math.pi)


def add_relighting_shader_inputs(shader_info):
    """Add the fixed relighting ABI used by the packaged Gaussian vertex shader."""
    for index in range(MAX_SHADOW_LIGHTS):
        shader_info.sampler(4 + index, "FLOAT_2D", f"mesh_shadow_depth_{index}")
    for index in range(4):
        shader_info.sampler(8 + index, "FLOAT_2D", f"proxy_shadow_layer_{index}")
    shader_info.sampler(12, "FLOAT_2D", "relight_data")


def _effective_light_color_and_energy(light, light_obj):
    color = np.asarray(light.color, dtype=np.float32)
    if getattr(light, "use_temperature", False):
        color *= np.asarray(light.temperature_color, dtype=np.float32)
    energy = float(light.energy) * (2.0 ** float(getattr(light, "exposure", 0.0)))
    if light.type == "AREA" and not getattr(light, "normalize", True):
        try:
            energy *= max(float(light.area(matrix_world=light_obj.matrix_world)), 0.0)
        except (AttributeError, TypeError):
            energy *= math.pi * _area_light_radius(light, light_obj.matrix_world) ** 2
    energy *= float(getattr(light, "diffuse_factor", 1.0))
    return (*color, energy)


def get_relight_lights(scene, preferred_light=None):
    """Return the compact evaluated Blender light set consumed by the shader."""
    lights = []
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in scene.objects:
        if obj.type != "LIGHT" or obj.hide_render or not obj.visible_get():
            continue
        light_obj = obj.evaluated_get(depsgraph)
        light = light_obj.data
        if light.type not in {"SUN", "POINT", "SPOT", "AREA"} or light.energy <= 0.0:
            continue
        light_range = light.cutoff_distance if getattr(light, "use_custom_distance", False) else 0.0
        light_radius = max(float(getattr(light, "shadow_soft_size", 0.0)), 0.0)
        direction = light_obj.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
        extra = (0.0, 0.0, 0.0, 0.0)
        if light.type == "SUN":
            # Blender lights emit along their local -Z axis. The shader wants the
            # direction from the shaded point towards the light, hence the inverse.
            position = (*(-direction), 0.0)
            settings = (0.0, 0.0, 0.0, 0.0)
        elif light.type == "AREA":
            position = (*light_obj.matrix_world.translation, 2.0)
            light_radius = _area_light_radius(light, light_obj.matrix_world)
            settings = (*direction.normalized(), light_radius)
            spread = max(float(getattr(light, "spread", math.pi)), 0.0001)
            extra = (light_range, math.cos(spread * 0.5), 0.0, 0.0)
        elif light.type == "SPOT":
            position = (*light_obj.matrix_world.translation, 3.0)
            settings = (*direction.normalized(), light_radius)
            outer_angle = max(float(light.spot_size) * 0.5, 0.0001)
            inner_angle = outer_angle * (1.0 - float(light.spot_blend))
            extra = (light_range, math.cos(outer_angle), math.cos(inner_angle), 0.0)
        else:
            position = (*light_obj.matrix_world.translation, 1.0)
            settings = (light_range, light_radius, 0.0, 0.0)
        lights.append({
            "object": obj,
            "position": position,
            "color": _effective_light_color_and_energy(light, light_obj),
            "range": light_range,
            "radius": light_radius,
            "settings": settings,
            "extra": extra,
        })
    if preferred_light:
        lights.sort(key=lambda light: light["object"] != preferred_light)
    return lights[:MAX_LIGHTS]


def shadow_light_object(scene):
    selected = scene.sna_dgs_scene_properties.r2_shadow_light
    if selected and selected.type == "LIGHT":
        return selected
    return next((obj for obj in scene.objects if obj.type == "LIGHT" and not obj.hide_render and obj.visible_get()), None)


def _fallback_texture(name, format, values):
    if not hasattr(bpy, name):
        buffer = gpu.types.Buffer("FLOAT", len(values), values)
        setattr(bpy, name, gpu.types.GPUTexture((1, 1), format=format, data=buffer))
    return getattr(bpy, name)


def _linked_source_node(input_socket):
    if not input_socket or not input_socket.is_linked:
        return None
    node = input_socket.links[0].from_node
    while node and node.bl_idname == "NodeReroute":
        node = _linked_source_node(node.inputs[0])
    return node


def _mapping_state(environment):
    vector_input = environment.inputs.get("Vector") if environment else None
    mapping = _linked_source_node(vector_input)
    if not mapping or mapping.bl_idname != "ShaderNodeMapping":
        return None
    state = {
        "name": mapping.name,
        "vector_type": mapping.vector_type,
        "location": tuple(float(value) for value in mapping.inputs["Location"].default_value),
        "rotation": tuple(float(value) for value in mapping.inputs["Rotation"].default_value),
        "scale": tuple(float(value) for value in mapping.inputs["Scale"].default_value),
    }
    return state


def _image_signature(image):
    filepath = bpy.path.abspath(image.filepath) if image.filepath else ""
    modified = os.path.getmtime(filepath) if filepath and os.path.isfile(filepath) else 0.0
    color_space = getattr(getattr(image, "colorspace_settings", None), "name", "")
    return (
        image.name, tuple(image.size), filepath, modified, image.source,
        bool(image.is_dirty), color_space,
    )


def _world_background_source(scene):
    world = scene.world
    if world is None:
        return None, np.zeros(3, dtype=np.float32), 0.0, None, ()
    color = np.asarray(world.color, dtype=np.float32)
    strength = 1.0
    image = None
    mapping = None
    signature = [world.name, tuple(float(value) for value in color), bool(world.use_nodes)]
    if world.use_nodes and world.node_tree:
        outputs = [node for node in world.node_tree.nodes if node.bl_idname == "ShaderNodeOutputWorld"]
        output = next((node for node in outputs if getattr(node, "is_active_output", False)), outputs[0] if outputs else None)
        surface = output.inputs.get("Surface") if output else None
        background = _linked_source_node(surface)
        if background and background.bl_idname == "ShaderNodeBackground":
            color_input = background.inputs.get("Color")
            strength_input = background.inputs.get("Strength")
            strength = float(strength_input.default_value) if strength_input else 1.0
            if color_input:
                color = np.asarray(color_input.default_value[:3], dtype=np.float32)
                if color_input.is_linked:
                    source = _linked_source_node(color_input)
                    if source and source.bl_idname == "ShaderNodeTexEnvironment":
                        image = source.image
                        mapping = _mapping_state(source)
            signature.extend((background.name, tuple(float(value) for value in color), strength))
    if image:
        signature.extend(_image_signature(image))
    if mapping:
        signature.extend((
            mapping["name"], mapping["vector_type"], mapping["location"],
            mapping["rotation"], mapping["scale"],
        ))
    return image, color, strength, mapping, tuple(signature)


def _sh_basis(direction):
    x, y, z = direction
    return np.asarray((
        0.2820947918,
        -0.4886025119 * y,
        0.4886025119 * z,
        -0.4886025119 * x,
        1.0925484306 * x * y,
        -1.0925484306 * y * z,
        0.3153915653 * (3.0 * z * z - 1.0),
        -1.0925484306 * x * z,
        0.5462742153 * (x * x - y * y),
    ), dtype=np.float64)


def _sh_basis_batch(directions):
    directions = np.asarray(directions, dtype=np.float64)
    x, y, z = directions[:, 0], directions[:, 1], directions[:, 2]
    return np.column_stack((
        np.full(len(directions), 0.2820947918, dtype=np.float64),
        -0.4886025119 * y,
        0.4886025119 * z,
        -0.4886025119 * x,
        1.0925484306 * x * y,
        -1.0925484306 * y * z,
        0.3153915653 * (3.0 * z * z - 1.0),
        -1.0925484306 * x * z,
        0.5462742153 * (x * x - y * y),
    ))


def _world_projection_samples():
    cached = getattr(bpy, "dgs_world_projection_samples", None)
    if cached is not None:
        return cached
    count = 96
    indices = np.arange(count, dtype=np.float64) + 0.5
    z = 1.0 - 2.0 * indices / count
    radius = np.sqrt(np.maximum(1.0 - z * z, 0.0))
    phi = indices * (math.pi * (3.0 - math.sqrt(5.0)))
    directions = np.column_stack((radius * np.cos(phi), radius * np.sin(phi), z))
    basis = _sh_basis_batch(directions)
    cached = (directions, basis, np.linalg.pinv(basis))
    bpy.dgs_world_projection_samples = cached
    return cached


def _transform_world_coefficients(coefficients, mapping):
    """Apply a Mapping-node transform to band-2 SH without rereading the HDRI."""
    if not mapping:
        return coefficients
    location = np.asarray(mapping["location"], dtype=np.float64)
    rotation_values = np.asarray(mapping["rotation"], dtype=np.float64)
    scale = np.asarray(mapping["scale"], dtype=np.float64)
    if np.max(np.abs(location)) < 1.0e-12 and np.max(np.abs(rotation_values)) < 1.0e-12 and np.max(np.abs(scale - 1.0)) < 1.0e-12:
        return coefficients

    rotation = np.asarray(Euler(rotation_values, "XYZ").to_matrix(), dtype=np.float64)
    scaled = rotation @ np.diag(scale)
    vector_type = mapping["vector_type"]
    translation = np.zeros(3, dtype=np.float64)
    if vector_type == "TEXTURE":
        linear = np.linalg.pinv(scaled)
        translation = -linear @ location
    elif vector_type == "NORMAL":
        linear = np.linalg.pinv(scaled).T
    else:
        linear = scaled
        if vector_type == "POINT":
            translation = location

    directions, basis, basis_inverse = _world_projection_samples()
    mapped = directions @ linear.T + translation[None, :]
    lengths = np.linalg.norm(mapped, axis=1, keepdims=True)
    mapped = mapped / np.maximum(lengths, 1.0e-12)
    mapped_values = _sh_basis_batch(mapped) @ np.asarray(coefficients, dtype=np.float64)
    return basis_inverse @ mapped_values


def _image_world_coefficients(image):
    signature = _image_signature(image)
    cache = getattr(bpy, "dgs_world_image_sh_cache", {})
    key = int(image.as_pointer())
    cached = cache.get(key)
    if cached and cached["signature"] == signature:
        return cached["coefficients"]

    coefficients = np.zeros((WORLD_SH_COEFFICIENTS, 3), dtype=np.float64)
    width, height = int(image.size[0]), int(image.size[1])
    sample_width, sample_height = min(width, 64), min(height, 32)
    pixels = image.pixels
    dphi, dlatitude = 2.0 * math.pi / sample_width, math.pi / sample_height
    for row in range(sample_height):
        latitude = -0.5 * math.pi + (row + 0.5) * dlatitude
        cos_latitude = math.cos(latitude)
        source_y = min(height - 1, int((row + 0.5) * height / sample_height))
        for column in range(sample_width):
            longitude = -math.pi + (column + 0.5) * dphi
            source_x = min(width - 1, int((column + 0.5) * width / sample_width))
            pixel_index = (source_y * width + source_x) * 4
            sample = np.asarray(pixels[pixel_index:pixel_index + 3], dtype=np.float64)
            direction = (
                cos_latitude * math.cos(longitude),
                cos_latitude * math.sin(longitude),
                math.sin(latitude),
            )
            coefficients += _sh_basis(direction)[:, None] * sample[None, :] * (cos_latitude * dphi * dlatitude)

    # Lambertian irradiance divided by pi.
    coefficients[1:4] *= 2.0 / 3.0
    coefficients[4:9] *= 1.0 / 4.0
    result = coefficients.astype(np.float32)
    cache[key] = {"signature": signature, "coefficients": result}
    bpy.dgs_world_image_sh_cache = cache
    return result


def _world_sh_coefficients(scene, enabled):
    if not enabled:
        return np.zeros((WORLD_SH_COEFFICIENTS, 3), dtype=np.float32)
    image, color, strength, mapping, signature = _world_background_source(scene)
    cached = getattr(bpy, "dgs_world_sh_cache", None)
    if cached and cached.get("signature") == signature:
        return cached["coefficients"]

    if image and image.size[0] and image.size[1]:
        coefficients = _transform_world_coefficients(_image_world_coefficients(image), mapping)
    else:
        coefficients = np.zeros((WORLD_SH_COEFFICIENTS, 3), dtype=np.float64)
        coefficients[0] = np.asarray(color, dtype=np.float64) * (4.0 * math.pi * 0.2820947918)
    coefficients *= strength
    result = coefficients.astype(np.float32)
    bpy.dgs_world_sh_cache = {"signature": signature, "coefficients": result}
    return result


def _write_matrix_to_data(data, row, matrix):
    data[row, :, :] = np.asarray(matrix, dtype=np.float32).T


def _relight_data_texture(lights, world_coefficients, shadows, config=None):
    data = np.zeros((RELIGHT_DATA_ROWS, 4, 4), dtype=np.float32)
    for index, light in enumerate(lights[:MAX_LIGHTS]):
        data[index, 0] = light["position"]
        data[index, 1] = light["color"]
        data[index, 2] = light["settings"]
        data[index, 3] = light["extra"]
    for index, coefficient in enumerate(world_coefficients):
        data[WORLD_DATA_START + index, 0, :3] = coefficient
    config = config or {}
    data[GLOBAL_DATA_START, 0] = (
        float(config.get("mode", 0)),
        float(config.get("response", 0)),
        float(config.get("light_count", len(lights))),
        float(config.get("world_strength", 0.0)),
    )
    data[GLOBAL_DATA_START, 1] = config.get("ambient", (0.0, 0.0, 0.0, 0.0))
    data[GLOBAL_DATA_START, 2] = config.get("settings", (0.0, 0.0, 0.0, 0.0))
    data[GLOBAL_DATA_START, 3] = (
        float(config.get("shadow_enabled", False)),
        float(config.get("shadow_count", len(shadows))),
        float(config.get("shadow_filter_radius", 0.0)),
        float(config.get("proxy_layer_count", 0)),
    )
    proxy_depth_range = config.get("proxy_depth_range", (0.0, 1.0))
    data[GLOBAL_DATA_START + 1, 0, :2] = proxy_depth_range
    data[GLOBAL_DATA_START + 1, 0, 2] = float(config.get("world_response", 0))
    for index, shadow in enumerate(shadows[:MAX_SHADOW_LIGHTS]):
        base = SHADOW_DATA_START + index * SHADOW_ROWS_PER_MAP
        point_faces = shadow.get("point_faces", ())
        data[base, 0] = (1.0 if point_faces else 0.0, float(shadow.get("light_index", -1)), float(len(point_faces) or 1), 0.0)
        data[base, 1] = (*shadow.get("light_position", (0.0, 0.0, 0.0)), 0.0)
        matrices = point_faces or ((shadow["view_matrix"], shadow["projection_matrix"]),)
        for face, (view_matrix, projection_matrix) in enumerate(matrices[:6]):
            _write_matrix_to_data(data, base + 1 + face * 2, view_matrix)
            _write_matrix_to_data(data, base + 2 + face * 2, projection_matrix)
    packed = data.tobytes()
    if getattr(bpy, "dgs_relight_data_bytes", None) != packed:
        buffer = gpu.types.Buffer("FLOAT", data.size, data.reshape(-1).tolist())
        bpy.dgs_relight_data_texture = gpu.types.GPUTexture((4, RELIGHT_DATA_ROWS), format="RGBA32F", data=buffer)
        bpy.dgs_relight_data_bytes = packed
    return bpy.dgs_relight_data_texture


def _ensure_eevee_shadows(scene):
    """Enable Eevee's global shadow switch when GS-to-mesh shadows are active."""
    settings = getattr(scene, "eevee", None)
    if settings is not None and hasattr(settings, "use_shadows") and not settings.use_shadows:
        settings.use_shadows = True
        return True
    return False


def bind_relighting_uniforms(shader, scene):
    """Bind lights and cached shadow textures for either renderer path."""
    props = scene.sna_dgs_scene_properties
    if props.r2_shadow_proxy:
        _ensure_eevee_shadows(scene)
    proxy_material = None
    for obj in scene.objects:
        if obj.get("kiri_3dgs_shadow_proxy", False):
            if proxy_material is None:
                proxy_material = _shadow_proxy_material()
            if obj.type == "MESH" and (not obj.data.materials or obj.data.materials[0] != proxy_material):
                if obj.data.materials:
                    obj.data.materials[0] = proxy_material
                else:
                    obj.data.materials.append(proxy_material)
            if not obj.visible_camera:
                obj.visible_camera = True
            visible_shadow = bool(props.r2_shadow_proxy)
            if obj.visible_shadow != visible_shadow:
                obj.visible_shadow = visible_shadow
    enabled = bool(props.r2_relight)
    lights = get_relight_lights(scene, shadow_light_object(scene)) if enabled else []
    shadows = getattr(bpy, "dgs_mesh_shadow_maps", [])
    shadow_enabled = bool(enabled and props.r2_shadows and shadows)
    world_enabled = bool(enabled and getattr(props, "r2_world_lighting", False))
    world_coefficients = _world_sh_coefficients(scene, world_enabled)
    layers = getattr(bpy, "dgs_proxy_shadow_layers", []) if shadow_enabled else []
    proxy_depth_range = getattr(bpy, "dgs_proxy_shadow_depth_range", (0.0, 1.0))
    config = {
        "mode": int(props.r2_relight_mode) if enabled else 0,
        "response": int(props.r2_relight_response) if enabled else 0,
        "light_count": len(lights),
        "world_strength": float(getattr(props, "r2_world_strength", 1.0)) if world_enabled else 0.0,
        "world_response": int(getattr(props, "r2_world_response", "0")),
        "ambient": (*props.r2_relight_ambient, props.r2_relight_ambient_strength),
        "settings": (props.r2_relight_strength, props.r2_shadow_bias, props.r2_shadow_density, props.r2_shadow_normal_bias),
        "shadow_enabled": shadow_enabled,
        "shadow_count": min(len(shadows), MAX_SHADOW_LIGHTS) if shadow_enabled else 0,
        "shadow_filter_radius": props.r2_shadow_filter_radius,
        "proxy_layer_count": min(len(layers), 4),
        "proxy_depth_range": proxy_depth_range,
    }
    shader.uniform_sampler("relight_data", _relight_data_texture(lights, world_coefficients, shadows if shadow_enabled else [], config))
    fallback_depth = _fallback_texture("dgs_shadow_fallback_texture", "R32F", [1.0e10])
    for index in range(MAX_SHADOW_LIGHTS):
        shadow = shadows[index] if index < len(shadows) else None
        shader.uniform_sampler(f"mesh_shadow_depth_{index}", shadow["texture"] if shadow else fallback_depth)
    fallback_proxy = _fallback_texture("dgs_proxy_shadow_fallback", "RGBA16F", [0.0, 0.0, 0.0, 0.0])
    for index in range(4):
        shader.uniform_sampler(f"proxy_shadow_layer_{index}", layers[index] if index < len(layers) else fallback_proxy)


def _validated_gaussian_data(value, expected_count=0):
    """Return complete 59-float Gaussian records, rejecting truncated ID properties."""
    if value is None:
        return None
    try:
        if isinstance(value, (bytes, bytearray, memoryview)):
            data = np.frombuffer(value, dtype=np.float32)
        else:
            data = np.asarray(value, dtype=np.float32)
        if data.size == 0 or data.size % 59:
            return None
        data = data.reshape(-1, 59)
        if expected_count and len(data) != expected_count:
            return None
        if not np.all(np.isfinite(data[:, :11])):
            return None
        return data
    except (TypeError, ValueError):
        return None


def _gaussian_data(obj):
    expected_count = int(obj.get("gaussian_count", 0) or 0)
    cached = getattr(bpy, "gaussian_object_cache", {}).get(obj.name, {}).get("gaussian_data")
    data = _validated_gaussian_data(cached, expected_count)
    if data is not None:
        return data
    data = _validated_gaussian_data(obj.get("gaussian_data"), expected_count)
    if data is not None:
        return data

    # Blender ID byte properties can be truncated at an embedded null byte when
    # a .blend is reopened. Reuse the add-on's established source-mesh/PLY
    # recovery path, which reconstructs all 59-float records into the runtime
    # cache before the shadow cards are sampled.
    try:
        from .texture_creation import sna_texture_creation_FD1B2
        bpy.gaussian_object_cache = {}
        sna_texture_creation_FD1B2()
        recovered = getattr(bpy, "gaussian_object_cache", {}).get(obj.name, {}).get("gaussian_data")
        data = _validated_gaussian_data(recovered, expected_count)
        if data is not None:
            return data
    except Exception as error:
        print(f"Gaussian source recovery failed for '{obj.name}': {error}")

    raise RuntimeError(
        f"Gaussian data for '{obj.name}' is incomplete and could not be restored from its source. "
        "Refresh the Render scene, or re-import the original mesh/PLY, then rebuild the shadow proxies."
    )


def remove_shadow_proxies():
    for obj in list(bpy.data.objects):
        if obj.get("kiri_3dgs_shadow_proxy", False):
            mesh = obj.data if obj.type == "MESH" else None
            bpy.data.objects.remove(obj, do_unlink=True)
            if mesh and mesh.users == 0:
                bpy.data.meshes.remove(mesh)
    bpy.dgs_shadow_proxy_signature = None
    bpy.dgs_shadow_proxy_build_status = None


def _gaussian_proxy_signature(scene):
    props = scene.sna_dgs_scene_properties
    signature = [
        "per_source_v1",
        int(props.r2_shadow_proxy_limit), round(float(props.r2_shadow_proxy_cutoff), 5),
        bool(props.r2_shadow_proxy), bool(props.r2_gaussian_self_shadows),
    ]
    for obj in scene.objects:
        if not obj.get("is_gaussian_splat", False):
            continue
        data = _gaussian_data(obj)
        signature.extend((
            obj.name, len(data),
            _sample_points(data[:, :11]),
        ))
    return tuple(signature)


def _build_shadow_proxy_material(name, shadow_only):
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    version = 2 if shadow_only else 1
    if material.get("kiri_shadow_material_version") == version:
        return material
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    opacity_mix = nodes.new("ShaderNodeMixShader")
    opacity_mix.name = "Gaussian Opacity"
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    attribute = nodes.new("ShaderNodeAttribute")
    attribute.attribute_name = "kiri_shadow_alpha"
    principled.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
    principled.inputs["Roughness"].default_value = 1.0
    links.new(attribute.outputs["Fac"], opacity_mix.inputs[0])
    links.new(transparent.outputs[0], opacity_mix.inputs[1])
    links.new(principled.outputs[0], opacity_mix.inputs[2])
    if shadow_only:
        light_path = nodes.new("ShaderNodeLightPath")
        shadow_mix = nodes.new("ShaderNodeMixShader")
        shadow_mix.name = "Shadow Rays Only"
        links.new(light_path.outputs["Is Shadow Ray"], shadow_mix.inputs[0])
        links.new(transparent.outputs[0], shadow_mix.inputs[1])
        links.new(opacity_mix.outputs[0], shadow_mix.inputs[2])
        links.new(shadow_mix.outputs[0], output.inputs[0])
    else:
        links.new(opacity_mix.outputs[0], output.inputs[0])
    material.surface_render_method = "DITHERED"
    if hasattr(material, "use_transparent_shadow"):
        material.use_transparent_shadow = True
    material["kiri_shadow_material_version"] = version
    return material


def _shadow_proxy_material():
    return _build_shadow_proxy_material("KIRI_3DGS_Eevee_Shadow_Proxy", True)


def _shadow_proxy_depth_material():
    return _build_shadow_proxy_material("KIRI_3DGS_Cached_Shadow_Depth_Proxy", False)


def _shadow_proxy_allocations(sources, limit, cutoff):
    """Distribute one scene-wide card budget proportionally across sources."""
    eligible = []
    for obj, data in sources:
        indices = np.flatnonzero(data[:, 10] >= cutoff)
        if len(indices):
            eligible.append((obj, data, indices))
    if not eligible:
        return []

    counts = np.asarray([len(indices) for _, _, indices in eligible], dtype=np.int64)
    total = int(counts.sum())
    effective_limit = max(int(limit), len(eligible))
    if total <= effective_limit:
        budgets = counts.copy()
    else:
        # Give every non-empty splat at least one representative card, then
        # distribute the remaining scene-wide budget by available card count.
        budgets = np.ones(len(eligible), dtype=np.int64)
        remaining = effective_limit - len(eligible)
        capacity = counts - 1
        capacity_total = int(capacity.sum())
        if remaining > 0 and capacity_total > 0:
            ideal = capacity.astype(np.float64) * (remaining / capacity_total)
            additions = np.minimum(np.floor(ideal).astype(np.int64), capacity)
            budgets += additions
            remaining -= int(additions.sum())
            fractions = ideal - additions
            order = sorted(range(len(eligible)), key=lambda index: (-fractions[index], -capacity[index], index))
            while remaining > 0:
                assigned = False
                for index in order:
                    if budgets[index] < counts[index]:
                        budgets[index] += 1
                        remaining -= 1
                        assigned = True
                        if remaining == 0:
                            break
                if not assigned:
                    break

    allocations = []
    for (obj, data, indices), budget in zip(eligible, budgets):
        budget = int(budget)
        if budget < len(indices):
            sample_positions = (np.arange(budget, dtype=np.int64) * len(indices)) // budget
            indices = indices[sample_positions]
        allocations.append((obj, data, indices))
    return allocations


def _shadow_proxy_geometry(data, indices):
    """Build local-space Gaussian cards for one source object."""
    vertices, faces, alpha = [], [], []
    for index in indices:
        row = data[index]
        opacity = float(row[10])
        rotation = Quaternion(row[3:7])
        if sum(value * value for value in rotation) == 0.0:
            rotation = Quaternion()
        else:
            rotation.normalize()
        scale = row[7:10]
        axes = sorted(range(3), key=lambda axis: scale[axis], reverse=True)
        unit = lambda axis: Vector((axis == 0, axis == 1, axis == 2))
        axis_u, axis_v = rotation @ unit(axes[0]), rotation @ unit(axes[1])
        center, base = Vector(row[:3]), len(vertices)
        for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            vertices.append(tuple(center + axis_u * scale[axes[0]] * 3.0 * u + axis_v * scale[axes[1]] * 3.0 * v))
            alpha.append(opacity)
        faces.append((base, base + 1, base + 2, base + 3))
    return vertices, faces, alpha


def build_shadow_proxies(context, signature=None):
    """Build one parented, camera-transparent Eevee shadow proxy per splat."""
    remove_shadow_proxies()
    props = context.scene.sna_dgs_scene_properties
    if props.r2_shadow_proxy:
        _ensure_eevee_shadows(context.scene)
    sources = [(obj, _gaussian_data(obj)) for obj in context.scene.objects if obj.get("is_gaussian_splat", False)]
    if not sources:
        raise RuntimeError("No Gaussian proxy data found. Update the Render scene first.")
    allocations = _shadow_proxy_allocations(sources, props.r2_shadow_proxy_limit, props.r2_shadow_proxy_cutoff)
    if not allocations:
        raise RuntimeError("No splats passed the shadow proxy opacity cutoff.")
    collection = bpy.data.collections.get("KIRI_3DGS_Shadow_Proxies") or bpy.data.collections.new("KIRI_3DGS_Shadow_Proxies")
    if collection not in context.scene.collection.children[:]:
        context.scene.collection.children.link(collection)
    material = _shadow_proxy_material()
    total_faces = 0
    for source, data, indices in allocations:
        vertices, faces, alpha = _shadow_proxy_geometry(data, indices)
        mesh = bpy.data.meshes.new(f"KIRI_3DGS_Shadow_Proxy_Mesh_{source.name}")
        mesh.from_pydata(vertices, [], faces)
        alpha_attribute = mesh.attributes.new("kiri_shadow_alpha", "FLOAT", "POINT")
        alpha_attribute.data.foreach_set("value", alpha)
        mesh.materials.append(material)
        proxy = bpy.data.objects.new(f"KIRI_3DGS_Shadow_Proxy_{source.name}", mesh)
        proxy["kiri_3dgs_shadow_proxy"] = True
        proxy["kiri_3dgs_shadow_source_name"] = source.name
        proxy["kiri_3dgs_shadow_card_count"] = len(faces)
        source_uuid = source.get("source_mesh_uuid") or source.get("gaussian_source_uuid")
        if source_uuid:
            proxy["kiri_3dgs_shadow_source_uuid"] = str(source_uuid)
        proxy.parent = source
        proxy.matrix_parent_inverse = Matrix.Identity(4)
        proxy.matrix_basis = Matrix.Identity(4)
        proxy.hide_select = True
        # Eevee needs the object to remain camera-visible to include it in its
        # raster shadow pass. The material itself is transparent to camera rays.
        proxy.visible_camera = True
        proxy.visible_shadow = bool(props.r2_shadow_proxy)
        collection.objects.link(proxy)
        total_faces += len(faces)
    context.view_layer.update()
    bpy.dgs_shadow_proxy_build_status = {"cards": total_faces, "objects": len(allocations)}
    bpy.dgs_shadow_proxy_signature = signature or _gaussian_proxy_signature(context.scene)
    return total_faces


def _shadow_bounds(scene):
    points = []
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in scene.objects:
        if obj.hide_render:
            continue
        if obj.type == "MESH" and not obj.get("kiri_3dgs_shadow_proxy", False):
            evaluated = obj.evaluated_get(depsgraph)
            points.extend(evaluated.matrix_world @ Vector(corner) for corner in evaluated.bound_box)
        elif obj.get("is_gaussian_splat", False):
            data = _gaussian_data(obj)
            points.extend(obj.matrix_world @ Vector(point) for point in data[::max(1, len(data) // 2048), :3])
    if not points:
        raise RuntimeError("No native mesh or Gaussian bounds are available for the shadow map.")
    low = Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points)))
    high = Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points)))
    return points, (low + high) * 0.5, max((high - low).length, 1.0)


def _configure_shadow_camera(camera, light, center, extent, bounds):
    data = camera.data
    if light.data.type == "SUN":
        direction = light.matrix_world.to_quaternion() @ Vector((0.0, 0.0, 1.0))
        data.type, data.ortho_scale = "ORTHO", extent * 1.5
        data.clip_start, data.clip_end = 0.01, extent * 4.0
        camera.location = center + direction * extent * 2.0
        camera.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()
    elif light.data.type == "SPOT":
        data.type, data.angle = "PERSP", light.data.spot_size
        data.clip_start = max(light.data.shadow_soft_size * 0.1, 0.01)
        location = light.matrix_world.translation
        maximum_distance = max((point - location).length for point in bounds)
        data.clip_end = light.data.cutoff_distance if light.data.use_custom_distance else maximum_distance * 1.1
        data.clip_end = max(data.clip_end, data.clip_start + 0.01)
        camera.location = light.matrix_world.translation
        camera.rotation_euler = light.matrix_world.to_quaternion().to_euler()
        camera.scale = (1.0, 1.0, 1.0)
    elif light.data.type == "AREA":
        location = light.matrix_world.translation
        direction = light.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
        angles = [direction.angle((point - location).normalized()) for point in bounds if (point - location).length > 0.0001]
        distance = max((point - location).length for point in bounds)
        data.type = "PERSP"
        data.angle = min(max((max(angles) if angles else 0.0) * 2.1, math.radians(10.0)), math.radians(170.0))
        data.clip_start = 0.01
        data.clip_end = light.data.cutoff_distance if light.data.use_custom_distance else distance * 1.1
        camera.location = light.matrix_world.translation
        camera.rotation_euler = light.matrix_world.to_quaternion().to_euler()
        camera.scale = (1.0, 1.0, 1.0)
    else:
        location = light.matrix_world.translation
        direction = center - location
        direction = direction.normalized() if direction.length else Vector((0.0, 0.0, -1.0))
        angles = [direction.angle((point - location).normalized()) for point in bounds if (point - location).length > 0.0001]
        distance = max((point - location).length for point in bounds)
        data.type = "PERSP"
        data.angle = min(max((max(angles) if angles else 0.0) * 2.1, math.radians(10.0)), math.radians(170.0))
        data.clip_start = 0.01
        data.clip_end = light.data.cutoff_distance if light.data.use_custom_distance else distance * 1.1
        camera.location, camera.rotation_euler = location, direction.to_track_quat("-Z", "Y").to_euler()


def _point_shadow_directions():
    return (
        (Vector((1.0, 0.0, 0.0)), Vector((0.0, 0.0, 1.0))),
        (Vector((-1.0, 0.0, 0.0)), Vector((0.0, 0.0, 1.0))),
        (Vector((0.0, 1.0, 0.0)), Vector((0.0, 0.0, 1.0))),
        (Vector((0.0, -1.0, 0.0)), Vector((0.0, 0.0, 1.0))),
        (Vector((0.0, 0.0, 1.0)), Vector((0.0, -1.0, 0.0))),
        (Vector((0.0, 0.0, -1.0)), Vector((0.0, 1.0, 0.0))),
    )


def _configure_point_shadow_face(camera, light, direction, up, bounds):
    location = light.matrix_world.translation
    right = direction.cross(up).normalized()
    corrected_up = right.cross(direction).normalized()
    rotation = Matrix((right, corrected_up, -direction)).transposed().to_4x4()
    rotation.translation = location
    camera.matrix_world = rotation
    camera.data.type = "PERSP"
    camera.data.angle = math.radians(90.0)
    camera.data.clip_start = max(float(light.data.shadow_soft_size) * 0.01, 0.01)
    maximum_distance = max((point - location).length for point in bounds)
    camera.data.clip_end = light.data.cutoff_distance if light.data.use_custom_distance else maximum_distance * 1.1


def _read_exr_depth(exr_path):
    """Read one metric depth channel with Blender's bundled OpenImageIO module."""
    try:
        import OpenImageIO as oiio
    except ImportError as error:
        raise RuntimeError(
            "This Blender build does not expose its OpenImageIO Python module, "
            "so the native mesh-shadow depth map could not be read."
        ) from error

    image_input = oiio.ImageInput.open(exr_path)
    if image_input is None:
        details = oiio.geterror() if hasattr(oiio, "geterror") else ""
        raise RuntimeError(f"OpenImageIO could not open the native depth map. {details}".strip())

    try:
        for subimage in range(64):
            if subimage and not image_input.seek_subimage(subimage, 0):
                break
            spec = image_input.spec()
            channel_names = list(spec.channelnames)
            channel_index = next(
                (channel_names.index(name) for name in ("Depth.V", "Depth.Z", "Depth", "Z") if name in channel_names),
                None,
            )
            if channel_index is None:
                channel_index = next(
                    (
                        index for index, name in enumerate(channel_names)
                        if "depth" in name.lower() and name.lower().endswith((".v", ".z"))
                    ),
                    None,
                )
            if channel_index is None:
                continue

            pixels = image_input.read_image(subimage, 0, channel_index, channel_index + 1, oiio.FLOAT)
            if pixels is None:
                details = image_input.geterror()
                raise RuntimeError(f"OpenImageIO could not read the EXR depth channel. {details}".strip())
            depth = np.asarray(pixels, dtype=np.float32).reshape(spec.height, spec.width)
            # OIIO returns top-to-bottom scanlines. GPUTexture data follows Blender's
            # image-pixel convention, whose first row is the bottom of the image.
            return np.ascontiguousarray(np.flipud(depth)), spec.width, spec.height
    finally:
        image_input.close()

    raise RuntimeError("The rendered EXR did not contain a recognizable depth channel.")


def build_native_shadow_map(context, light):
    """Render native geometry from one light view and retain metric depth on the GPU."""
    scene, props = context.scene, context.scene.sna_dgs_scene_properties
    bounds, center, extent = _shadow_bounds(scene)
    camera_data = bpy.data.cameras.new("KIRI_3DGS_Shadow_Camera")
    camera = bpy.data.objects.new("KIRI_3DGS_Shadow_Camera", camera_data)
    scene.collection.objects.link(camera)
    if light.data.type != "POINT":
        _configure_shadow_camera(camera, light, center, extent, bounds)
    original = (scene.camera, scene.render.engine, scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage, scene.render.filepath, scene.compositing_node_group, scene.use_nodes, scene.view_layers[0].use_pass_z)
    hidden, proxy_materials, node_tree = [], [], None
    include_gaussian_proxies = bool(getattr(props, "r2_gaussian_self_shadows", False))
    temp_dir = tempfile.mkdtemp(prefix="kiri_3dgs_shadow_")
    try:
        scene.camera, scene.render.engine = camera, "BLENDER_EEVEE"
        scene.render.resolution_x = scene.render.resolution_y = props.r2_shadow_resolution
        scene.render.resolution_percentage, scene.render.filepath = 100, temp_dir + os.sep
        scene.view_layers[0].use_pass_z = True
        for obj in scene.objects:
            is_gaussian = obj.get("is_gaussian_splat", False)
            is_proxy = obj.get("kiri_3dgs_shadow_proxy", False)
            if is_gaussian or is_proxy:
                hidden.append((obj, obj.hide_render, getattr(obj, "visible_camera", None)))
            if is_gaussian or (is_proxy and not include_gaussian_proxies):
                obj.hide_render = True
            elif is_proxy:
                obj.hide_render = False
                obj.visible_camera = True
                if obj.type == "MESH":
                    original_material = obj.data.materials[0] if obj.data.materials else None
                    proxy_materials.append((obj, original_material, bool(obj.data.materials)))
                    if obj.data.materials:
                        obj.data.materials[0] = _shadow_proxy_depth_material()
                    else:
                        obj.data.materials.append(_shadow_proxy_depth_material())
        node_tree = bpy.data.node_groups.new("KIRI_3DGS_Temporary_Shadow_Compositor", "CompositorNodeTree")
        scene.compositing_node_group, scene.use_nodes = node_tree, True
        layers = node_tree.nodes.new("CompositorNodeRLayers")
        output = node_tree.nodes.new("CompositorNodeOutputFile")
        output.directory = temp_dir
        output.file_output_items.new("FLOAT", "Depth")
        output.format.file_format = "OPEN_EXR_MULTILAYER"
        node_tree.links.new(layers.outputs["Depth"], output.inputs["Depth"])
        resolution = props.r2_shadow_resolution

        def render_depth(name):
            output.file_name = name
            exr_path = os.path.join(temp_dir, name)
            bpy.ops.render.render(write_still=False)
            depth, width, height = _read_exr_depth(exr_path)
            if (width, height) != (resolution, resolution):
                raise RuntimeError("The native depth map has an unexpected size.")
            return depth

        if light.data.type == "POINT":
            atlas = np.full((resolution * 2, resolution * 3), 1.0e10, dtype=np.float32)
            point_faces = []
            for face, (direction, up) in enumerate(_point_shadow_directions()):
                _configure_point_shadow_face(camera, light, direction, up, bounds)
                depth = render_depth(f"depth_{face}.exr")
                atlas_row, atlas_column = divmod(face, 3)
                atlas[
                    atlas_row * resolution:(atlas_row + 1) * resolution,
                    atlas_column * resolution:(atlas_column + 1) * resolution,
                ] = depth
                projection = camera.calc_matrix_camera(context.evaluated_depsgraph_get(), x=resolution, y=resolution)
                point_faces.append((camera.matrix_world.inverted().copy(), projection.copy()))
            packed_depth = atlas.reshape(-1)
            buffer = gpu.types.Buffer("FLOAT", len(packed_depth), packed_depth.tolist())
            texture = gpu.types.GPUTexture((resolution * 3, resolution * 2), format="R32F", data=buffer)
            return {
                "texture": texture,
                "view_matrix": point_faces[0][0],
                "projection_matrix": point_faces[0][1],
                "point_faces": tuple(point_faces),
                "light_position": tuple(light.matrix_world.translation),
            }

        depth = render_depth("depth.exr").reshape(-1)
        buffer = gpu.types.Buffer("FLOAT", len(depth), depth.tolist())
        texture = gpu.types.GPUTexture((resolution, resolution), format="R32F", data=buffer)
        projection = camera.calc_matrix_camera(context.evaluated_depsgraph_get(), x=resolution, y=resolution)
        return {
            "texture": texture,
            "view_matrix": camera.matrix_world.inverted(),
            "projection_matrix": projection,
            "light_position": tuple(light.matrix_world.translation),
        }
    finally:
        for obj, hidden_state, camera_state in hidden:
            obj.hide_render = hidden_state
            if camera_state is not None:
                obj.visible_camera = camera_state
        for obj, original_material, had_slot in proxy_materials:
            if had_slot:
                obj.data.materials[0] = original_material
            elif obj.data.materials:
                obj.data.materials.pop(index=0)
        scene.camera, scene.render.engine = original[0], original[1]
        scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = original[2], original[3], original[4]
        scene.render.filepath, scene.compositing_node_group, scene.use_nodes = original[5], original[6], original[7]
        scene.view_layers[0].use_pass_z = original[8]
        if node_tree and node_tree.users == 0:
            bpy.data.node_groups.remove(node_tree)
        bpy.data.objects.remove(camera, do_unlink=True)
        bpy.data.cameras.remove(camera_data)
        shutil.rmtree(temp_dir, ignore_errors=True)


def _rounded_matrix(matrix):
    return tuple(round(value, 6) for row in matrix for value in row)


def _sample_points(points, limit=64):
    count = len(points)
    if count == 0:
        return ()
    step = max(1, count // limit)
    return tuple(round(component, 5) for index in range(0, count, step) for component in points[index][:])


def _shadow_scene_signature(scene, light):
    """Capture light/caster state without hashing every Gaussian every frame."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    light_data = light.data
    props = scene.sna_dgs_scene_properties
    signature = [
        bool(getattr(props, "r2_gaussian_self_shadows", False)),
        int(props.r2_shadow_proxy_limit), round(float(props.r2_shadow_proxy_cutoff), 5),
        light.name, light_data.type, _rounded_matrix(light.matrix_world),
        tuple(round(value, 5) for value in light_data.color), round(light_data.energy, 5),
        round(getattr(light_data, "exposure", 0.0), 5),
        bool(getattr(light_data, "use_temperature", False)), round(getattr(light_data, "temperature", 6500.0), 2),
        bool(getattr(light_data, "normalize", True)), bool(getattr(light_data, "use_shadow", True)),
        bool(getattr(light_data, "use_custom_distance", False)),
        round(getattr(light_data, "cutoff_distance", 0.0), 5),
        round(getattr(light_data, "spot_size", 0.0), 5),
        round(getattr(light_data, "spot_blend", 0.0), 5),
        round(getattr(light_data, "shadow_soft_size", 0.0), 5),
        round(getattr(light_data, "size", 0.0), 5),
        round(getattr(light_data, "size_y", 0.0), 5),
        getattr(light_data, "shape", ""), round(getattr(light_data, "spread", 0.0), 5),
    ]
    for obj in scene.objects:
        if obj.hide_render or obj.get("kiri_3dgs_shadow_proxy", False) or obj.type == "LIGHT":
            continue
        if obj.type == "MESH":
            evaluated = obj.evaluated_get(depsgraph)
            mesh = evaluated.data
            sample = _sample_points([evaluated.matrix_world @ vertex.co for vertex in mesh.vertices])
            signature.extend((obj.name, _rounded_matrix(evaluated.matrix_world), len(mesh.vertices), len(mesh.polygons), sample))
        elif obj.get("is_gaussian_splat", False):
            data = _gaussian_data(obj)
            sample = _sample_points(data[:, :11])
            signature.extend((obj.name, _rounded_matrix(obj.matrix_world), len(data), sample))
    return tuple(signature)


def _shadow_cache_status(rebuilt, total):
    bpy.dgs_shadow_cache_status = {
        "frame": bpy.context.scene.frame_current,
        "rebuilt": rebuilt,
        "total": total,
    }


def refresh_shadow_maps(context, force=True):
    scene, props = context.scene, context.scene.sna_dgs_scene_properties
    context.evaluated_depsgraph_get().update()
    preferred = shadow_light_object(scene)
    uses_gaussian_proxies = bool(props.r2_shadow_proxy or getattr(props, "r2_gaussian_self_shadows", False))
    if uses_gaussian_proxies:
        proxy_signature = _gaussian_proxy_signature(scene)
        if proxy_signature != getattr(bpy, "dgs_shadow_proxy_signature", None):
            build_shadow_proxies(context, proxy_signature)
    all_lights = get_relight_lights(scene, preferred)
    lights = [
        (index, light) for index, light in enumerate(all_lights)
        if getattr(light["object"].data, "use_shadow", True)
    ][:props.r2_shadow_light_limit]
    if not lights:
        raise RuntimeError("Add an enabled Blender light before building shadow maps.")
    cache = getattr(bpy, "dgs_shadow_map_cache", {})
    maps, rebuilt = [], 0
    for light_index, light in lights:
        signature = _shadow_scene_signature(scene, light["object"])
        cached = cache.get(light["object"].name)
        needs_rebuild = force or not cached or cached["signature"] != signature
        if needs_rebuild:
            shadow_map = build_native_shadow_map(context, light["object"])
            cache[light["object"].name] = {"signature": signature, "map": shadow_map}
            rebuilt += 1
        else:
            shadow_map = cached["map"]
        shadow_map["light_index"] = light_index
        maps.append(shadow_map)
    active_names = {light["object"].name for _, light in lights}
    bpy.dgs_shadow_map_cache = {name: entry for name, entry in cache.items() if name in active_names}
    bpy.dgs_mesh_shadow_maps = maps
    _shadow_cache_status(rebuilt, len(maps))
    return maps


def update_shadow_maps_for_frame(context, is_animation):
    """Apply the selected update policy after the animation frame is evaluated."""
    props = context.scene.sna_dgs_scene_properties
    if not (props.r2_relight and props.r2_shadows):
        return False
    mode = props.r2_shadow_update_mode
    if mode == "Manual":
        return False
    return bool(refresh_shadow_maps(context, force=mode == "Every Frame"))


class SNA_OT_Dgs_Render_Build_Shadow_Proxies_5B787(bpy.types.Operator):
    bl_idname = "sna.dgs_render_build_shadow_proxies_5b787"
    bl_label = "Build Eevee Shadow Proxies"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            cards = build_shadow_proxies(context)
            objects = getattr(bpy, "dgs_shadow_proxy_build_status", {}).get("objects", 0)
            self.report({"INFO"}, f"Built {cards:,} Eevee Gaussian shadow cards across {objects} splat prox{'y' if objects == 1 else 'ies'}")
            return {"FINISHED"}
        except RuntimeError as error:
            self.report({"ERROR"}, str(error))
            return {"CANCELLED"}


class SNA_OT_Dgs_Render_Refresh_Shadows_16F2B(bpy.types.Operator):
    bl_idname = "sna.dgs_render_refresh_shadows_16f2b"
    bl_label = "Refresh Gaussian Shadows"
    bl_options = {"REGISTER"}

    def execute(self, context):
        try:
            self.report({"INFO"}, f"Refreshed {len(refresh_shadow_maps(context, force=True))} shadow maps")
            return {"FINISHED"}
        except RuntimeError as error:
            self.report({"ERROR"}, str(error))
            return {"CANCELLED"}
