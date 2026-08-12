"""Shared realtime relighting and shadow support for the Gaussian renderers."""

import math
import os
import shutil
import subprocess
import tempfile

import bpy
import gpu
import numpy as np
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix, Quaternion, Vector


MAX_LIGHTS = 4


def add_relighting_shader_inputs(shader_info):
    """Add the fixed relighting ABI used by the packaged Gaussian vertex shader."""
    shader_info.push_constant("INT", "relight_mode")
    shader_info.push_constant("INT", "relight_response")
    shader_info.push_constant("INT", "relight_light_count")
    shader_info.push_constant("VEC4", "relight_ambient")
    shader_info.push_constant("VEC4", "relight_settings")
    # Keep every direct-light value in the initial push-constant range supported by Metal.
    for index in range(MAX_LIGHTS):
        shader_info.push_constant("VEC4", f"relight_light_position_{index}")
        shader_info.push_constant("VEC4", f"relight_light_color_{index}")
        shader_info.push_constant("VEC4", f"relight_light_settings_{index}")
    shader_info.push_constant("INT", "shadow_enabled")
    shader_info.push_constant("INT", "shadow_light_count")
    shader_info.push_constant("FLOAT", "shadow_filter_radius")
    shader_info.push_constant("INT", "proxy_shadow_layer_count")
    shader_info.push_constant("VEC2", "proxy_shadow_depth_range")
    for index in range(MAX_LIGHTS):
        shader_info.push_constant("INT", f"shadow_light_index_{index}")
        shader_info.push_constant("MAT4", f"shadow_view_matrix_{index}")
        shader_info.push_constant("MAT4", f"shadow_projection_matrix_{index}")
        shader_info.sampler(4 + index, "FLOAT_2D", f"mesh_shadow_depth_{index}")
    for index in range(4):
        shader_info.sampler(8 + index, "FLOAT_2D", f"proxy_shadow_layer_{index}")


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
        if light.type == "SUN":
            direction = light_obj.matrix_world.to_quaternion() @ Vector((0.0, 0.0, 1.0))
            position, light_range = (*direction, 0.0), 0.0
        else:
            position = (*light_obj.matrix_world.translation, 1.0)
            light_range = light.cutoff_distance if light.use_custom_distance else 0.0
        lights.append({
            "object": obj,
            "position": position,
            "color": (*light.color, light.energy),
            "range": light_range,
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


def bind_relighting_uniforms(shader, scene):
    """Bind lights and cached shadow textures for either renderer path."""
    props = scene.sna_dgs_scene_properties
    enabled = props.r2_relight
    shader.uniform_int("relight_mode", int(props.r2_relight_mode) if enabled else 0)
    shader.uniform_int("relight_response", int(props.r2_relight_response) if enabled else 0)
    shader.uniform_float("relight_ambient", (*props.r2_relight_ambient, props.r2_relight_ambient_strength))
    shader.uniform_float("relight_settings", (props.r2_relight_strength, props.r2_shadow_bias, props.r2_shadow_density, props.r2_shadow_normal_bias))
    shader.uniform_float("shadow_filter_radius", props.r2_shadow_filter_radius)
    lights = get_relight_lights(scene, shadow_light_object(scene)) if enabled else []
    shader.uniform_int("relight_light_count", len(lights))
    for index in range(MAX_LIGHTS):
        light = lights[index] if index < len(lights) else None
        shader.uniform_float(f"relight_light_position_{index}", light["position"] if light else (0.0, 0.0, 0.0, 0.0))
        shader.uniform_float(f"relight_light_color_{index}", light["color"] if light else (0.0, 0.0, 0.0, 0.0))
        shader.uniform_float(f"relight_light_settings_{index}", (light["range"], 0.0, 0.0, 0.0) if light else (0.0, 0.0, 0.0, 0.0))
    shadows = getattr(bpy, "dgs_mesh_shadow_maps", [])
    shadow_enabled = bool(enabled and props.r2_shadows and shadows)
    shader.uniform_int("shadow_enabled", int(shadow_enabled))
    shader.uniform_int("shadow_light_count", min(len(shadows), MAX_LIGHTS))
    fallback_depth = _fallback_texture("dgs_shadow_fallback_texture", "R32F", [1.0e10])
    for index in range(MAX_LIGHTS):
        shadow = shadows[index] if index < len(shadows) else None
        shader.uniform_int(f"shadow_light_index_{index}", shadow["light_index"] if shadow else -1)
        shader.uniform_float(f"shadow_view_matrix_{index}", shadow["view_matrix"] if shadow else Matrix.Identity(4))
        shader.uniform_float(f"shadow_projection_matrix_{index}", shadow["projection_matrix"] if shadow else Matrix.Identity(4))
        shader.uniform_sampler(f"mesh_shadow_depth_{index}", shadow["texture"] if shadow else fallback_depth)
    layers = getattr(bpy, "dgs_proxy_shadow_layers", []) if shadow_enabled else []
    shader.uniform_int("proxy_shadow_layer_count", min(len(layers), 4))
    shader.uniform_float("proxy_shadow_depth_range", getattr(bpy, "dgs_proxy_shadow_depth_range", (0.0, 1.0)))
    fallback_proxy = _fallback_texture("dgs_proxy_shadow_fallback", "RGBA16F", [0.0, 0.0, 0.0, 0.0])
    for index in range(4):
        shader.uniform_sampler(f"proxy_shadow_layer_{index}", layers[index] if index < len(layers) else fallback_proxy)


def _gaussian_data(obj):
    cached = getattr(bpy, "gaussian_object_cache", {}).get(obj.name, {}).get("gaussian_data")
    if cached is not None:
        return np.asarray(cached, dtype=np.float32).reshape(-1, 59)
    packed = obj.get("gaussian_data")
    if packed:
        return np.frombuffer(packed, dtype=np.float32).reshape(-1, 59)
    raise RuntimeError(f"Gaussian data for '{obj.name}' is unavailable. Update the Render scene first.")


def remove_shadow_proxies():
    for obj in list(bpy.data.objects):
        if obj.get("kiri_3dgs_shadow_proxy", False):
            mesh = obj.data if obj.type == "MESH" else None
            bpy.data.objects.remove(obj, do_unlink=True)
            if mesh and mesh.users == 0:
                bpy.data.meshes.remove(mesh)


def _shadow_proxy_material():
    material = bpy.data.materials.get("KIRI_3DGS_Eevee_Shadow_Proxy")
    if material:
        return material
    material = bpy.data.materials.new("KIRI_3DGS_Eevee_Shadow_Proxy")
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    mix = nodes.new("ShaderNodeMixShader")
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    attribute = nodes.new("ShaderNodeAttribute")
    attribute.attribute_name = "kiri_shadow_alpha"
    principled.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
    principled.inputs["Roughness"].default_value = 1.0
    links.new(attribute.outputs["Fac"], mix.inputs[0])
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(principled.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])
    material.surface_render_method = "DITHERED"
    if hasattr(material, "use_transparent_shadow"):
        material.use_transparent_shadow = True
    return material


def build_shadow_proxies(context):
    """Build camera-invisible Gaussian cards that cast Eevee shadows on meshes."""
    remove_shadow_proxies()
    props, vertices, faces, alpha = context.scene.sna_dgs_scene_properties, [], [], []
    sources = [(obj, _gaussian_data(obj)) for obj in context.scene.objects if obj.get("is_gaussian_splat", False)]
    if not sources:
        raise RuntimeError("No Gaussian proxy data found. Update the Render scene first.")
    stride = max(1, math.ceil(sum(len(data) for _, data in sources) / props.r2_shadow_proxy_limit))
    for obj, data in sources:
        for row in data[::stride]:
            opacity = float(row[10])
            if opacity < props.r2_shadow_proxy_cutoff:
                continue
            rotation = Quaternion(row[3:7])
            if sum(value * value for value in rotation) == 0.0:
                rotation = Quaternion()
            else:
                rotation.normalize()
            scale, axes = row[7:10], sorted(range(3), key=lambda axis: scale[axis], reverse=True)
            unit = lambda axis: Vector((axis == 0, axis == 1, axis == 2))
            axis_u, axis_v = rotation @ unit(axes[0]), rotation @ unit(axes[1])
            center, base = Vector(row[:3]), len(vertices)
            for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                vertices.append(tuple(obj.matrix_world @ (center + axis_u * scale[axes[0]] * 3.0 * u + axis_v * scale[axes[1]] * 3.0 * v)))
                alpha.append(opacity)
            faces.append((base, base + 1, base + 2, base + 3))
    if not vertices:
        raise RuntimeError("No splats passed the shadow proxy opacity cutoff.")
    collection = bpy.data.collections.get("KIRI_3DGS_Shadow_Proxies") or bpy.data.collections.new("KIRI_3DGS_Shadow_Proxies")
    if collection not in context.scene.collection.children[:]:
        context.scene.collection.children.link(collection)
    mesh = bpy.data.meshes.new("KIRI_3DGS_Shadow_Proxy_Mesh")
    mesh.from_pydata(vertices, [], faces)
    alpha_attribute = mesh.attributes.new("kiri_shadow_alpha", "FLOAT", "POINT")
    alpha_attribute.data.foreach_set("value", alpha)
    mesh.materials.append(_shadow_proxy_material())
    proxy = bpy.data.objects.new("KIRI_3DGS_Shadow_Proxy", mesh)
    proxy["kiri_3dgs_shadow_proxy"] = True
    proxy.visible_camera, proxy.visible_shadow = False, True
    collection.objects.link(proxy)
    return len(faces)


def _shadow_bounds(scene):
    points = []
    for obj in scene.objects:
        if obj.type == "MESH" and not obj.get("kiri_3dgs_shadow_proxy", False):
            points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
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
        data.clip_end = light.data.cutoff_distance if light.data.use_custom_distance else extent * 4.0
        camera.matrix_world = light.matrix_world
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


def build_native_shadow_map(context, light):
    """Render native geometry from one light view and retain metric depth on the GPU."""
    oiiotool = shutil.which("oiiotool")
    if not oiiotool:
        raise RuntimeError("Native shadow maps require oiiotool. Install OpenImageIO with Homebrew.")
    scene, props = context.scene, context.scene.sna_dgs_scene_properties
    bounds, center, extent = _shadow_bounds(scene)
    camera_data = bpy.data.cameras.new("KIRI_3DGS_Shadow_Camera")
    camera = bpy.data.objects.new("KIRI_3DGS_Shadow_Camera", camera_data)
    scene.collection.objects.link(camera)
    _configure_shadow_camera(camera, light, center, extent, bounds)
    original = (scene.camera, scene.render.engine, scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage, scene.render.filepath, scene.compositing_node_group, scene.use_nodes)
    hidden, node_tree = [], None
    temp_dir = tempfile.mkdtemp(prefix="kiri_3dgs_shadow_", dir="/tmp")
    try:
        scene.camera, scene.render.engine = camera, "BLENDER_EEVEE"
        scene.render.resolution_x = scene.render.resolution_y = props.r2_shadow_resolution
        scene.render.resolution_percentage, scene.render.filepath = 100, "/tmp/"
        scene.view_layers[0].use_pass_z = True
        for obj in scene.objects:
            if obj.get("is_gaussian_splat", False) or obj.get("kiri_3dgs_shadow_proxy", False):
                hidden.append((obj, obj.hide_render))
                obj.hide_render = True
        node_tree = bpy.data.node_groups.new("KIRI_3DGS_Temporary_Shadow_Compositor", "CompositorNodeTree")
        scene.compositing_node_group, scene.use_nodes = node_tree, True
        layers = node_tree.nodes.new("CompositorNodeRLayers")
        output = node_tree.nodes.new("CompositorNodeOutputFile")
        output.file_name = os.path.join(os.path.basename(temp_dir), "depth.exr")
        output.file_output_items.new("FLOAT", "Depth")
        output.format.file_format = "OPEN_EXR_MULTILAYER"
        node_tree.links.new(layers.outputs["Depth"], output.inputs["Depth"])
        exr_path, hdr_path = os.path.join(temp_dir, "depth.exr"), os.path.join(temp_dir, "depth.hdr")
        bpy.ops.render.render(write_still=False)
        subprocess.run([oiiotool, exr_path, "--ch", "Depth.V,Depth.V,Depth.V", "-o", hdr_path], check=True, capture_output=True)
        image = bpy.data.images.load(hdr_path, check_existing=False)
        try:
            pixels = np.empty(len(image.pixels), dtype=np.float32)
            image.pixels.foreach_get(pixels)
            depth = pixels[0::4]
        finally:
            bpy.data.images.remove(image)
        resolution = props.r2_shadow_resolution
        if len(depth) != resolution ** 2:
            raise RuntimeError("The native depth map has an unexpected size.")
        buffer = gpu.types.Buffer("FLOAT", len(depth), depth.tolist())
        texture = gpu.types.GPUTexture((resolution, resolution), format="R32F", data=buffer)
        projection = camera.calc_matrix_camera(context.evaluated_depsgraph_get(), x=resolution, y=resolution)
        return {"texture": texture, "view_matrix": camera.matrix_world.inverted(), "projection_matrix": projection}
    finally:
        for obj, hidden_state in hidden:
            obj.hide_render = hidden_state
        scene.camera, scene.render.engine = original[0], original[1]
        scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = original[2], original[3], original[4]
        scene.render.filepath, scene.compositing_node_group, scene.use_nodes = original[5], original[6], original[7]
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
    signature = [
        light.name, light_data.type, _rounded_matrix(light.matrix_world),
        tuple(round(value, 5) for value in light_data.color), round(light_data.energy, 5),
        round(getattr(light_data, "cutoff_distance", 0.0), 5),
        round(getattr(light_data, "spot_size", 0.0), 5),
        round(getattr(light_data, "size", 0.0), 5),
    ]
    for obj in scene.objects:
        if obj.get("kiri_3dgs_shadow_proxy", False) or obj.type == "LIGHT":
            continue
        if obj.type == "MESH":
            evaluated = obj.evaluated_get(depsgraph)
            mesh = evaluated.data
            sample = _sample_points([obj.matrix_world @ vertex.co for vertex in mesh.vertices])
            signature.extend((obj.name, _rounded_matrix(obj.matrix_world), len(mesh.vertices), sample))
        elif obj.get("is_gaussian_splat", False):
            data = _gaussian_data(obj)
            sample = _sample_points(data[:, :3])
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
    lights = get_relight_lights(scene, preferred)[:props.r2_shadow_light_limit]
    if not lights:
        raise RuntimeError("Add an enabled Blender light before building shadow maps.")
    cache = getattr(bpy, "dgs_shadow_map_cache", {})
    maps, rebuilt = [], 0
    for index, light in enumerate(lights):
        signature = _shadow_scene_signature(scene, light["object"])
        cached = cache.get(light["object"].name)
        needs_rebuild = force or not cached or cached["signature"] != signature
        if needs_rebuild:
            shadow_map = build_native_shadow_map(context, light["object"])
            cache[light["object"].name] = {"signature": signature, "map": shadow_map}
            rebuilt += 1
        else:
            shadow_map = cached["map"]
        shadow_map["light_index"] = index
        maps.append(shadow_map)
    active_names = {light["object"].name for light in lights}
    bpy.dgs_shadow_map_cache = {name: entry for name, entry in cache.items() if name in active_names}
    if props.r2_shadow_proxy and (rebuilt or not any(obj.get("kiri_3dgs_shadow_proxy", False) for obj in scene.objects)):
        build_shadow_proxies(context)
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
            self.report({"INFO"}, f"Built {build_shadow_proxies(context):,} Eevee Gaussian shadow cards")
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
        except (RuntimeError, subprocess.CalledProcessError) as error:
            self.report({"ERROR"}, str(error))
            return {"CANCELLED"}
