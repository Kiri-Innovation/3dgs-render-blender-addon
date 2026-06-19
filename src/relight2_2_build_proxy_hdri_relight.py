import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_relight2_2_build_proxy_hdri_relight_89C9C():
    relight_cache_root = bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory
    proxy_obj = bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh
    normal_smoothing = bpy.context.scene.sna_dgs_scene_properties.normal_smoothing
    pre_light_smoothing = bpy.context.scene.sna_dgs_scene_properties.pre_light_smoothing
    post_light_smoothing = bpy.context.scene.sna_dgs_scene_properties.post_light_smoothing
    transfer_style = bpy.context.scene.sna_dgs_scene_properties.transfer_style
    transfer_smoothness = bpy.context.scene.sna_dgs_scene_properties.transfer_smoothness
    include_world_environment = bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment
    include_scene_lights = bpy.context.scene.sna_dgs_scene_properties.relight_include_scene_lights
    irradiance_resolution = bpy.context.scene.sna_dgs_scene_properties.irradiance_resolution
    irradiance_blur_strength = bpy.context.scene.sna_dgs_scene_properties.irradiance_blur_strength
    irradiance_luminance_clamp = bpy.context.scene.sna_dgs_scene_properties.irradiance_luminance_clamp
    use_proxy_occlusion = bpy.context.scene.sna_dgs_scene_properties.use_proxy_occlusion
    occlusion_sample_count = bpy.context.scene.sna_dgs_scene_properties.occlusion_sample_count
    occlusion_bias = bpy.context.scene.sna_dgs_scene_properties.occlusion_bias
    occlusion_max_distance = bpy.context.scene.sna_dgs_scene_properties.occlusion_max_distance
    scene_light_gain = bpy.context.scene.sna_dgs_scene_properties.relight_scene_light_gain
    include_hidden_lights = bpy.context.scene.sna_dgs_scene_properties.include_hidden_lights
    use_light_shadows = bpy.context.scene.sna_dgs_scene_properties.relight_use_light_shadows
    light_shadow_bias = bpy.context.scene.sna_dgs_scene_properties.light_shadow_bias
    clamp_base_color = True
    numeric_quality = 'Standard'
    hdri_max_width = bpy.context.scene.sna_dgs_scene_properties.hdri_max_width
    proxy_surface_relight_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_deferred_layers_utils.py')
    proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
    # UI range note: "Soft" means the recommended Serpens slider range; "Hard" means the safe absolute clamp.
    #proxy_surface_relight_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/relighting/proxy_deferred_layers_v2_overlay_only/proxy_deferred_layers_utils.py"  # Input: full path to proxy_deferred_layers_utils.py. UI: path text, no numeric min/max.
    #proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py. UI: path text, no numeric min/max.
    #relight_cache_root = "D:/GithubRepos/3DGS Render_Render Updates/relighting"  # Input: folder that stores the saved original state and baked lighting cache. UI: folder path, no numeric min/max.
    # ---------------------------------------------------------------------------
    # Target 3DGS object
    # ---------------------------------------------------------------------------
    target_mode = "Active"  # Input: Active or Input Object. UI: enum, no numeric min/max.
    target_obj = None  # Input: object pointer or object name. UI: show only when target_mode is Input Object; no numeric min/max.
    # ---------------------------------------------------------------------------
    # Base color source
    # This is the color being lit. Saved Original is the recommended default.
    # ---------------------------------------------------------------------------
    base_color_source_mode = "Saved Original"  # Input: Saved Original or Current f_dc. UI: enum, no numeric min/max; Saved Original is recommended.
    clamp_base_color = True  # Input: True = clamp base RGB into 0-1 before caching it. UI: boolean, hard False/True.
    # ---------------------------------------------------------------------------
    # Proxy source
    # ---------------------------------------------------------------------------
    #proxy_obj = None  # Input: proxy mesh object pointer or object name; blank = use the bound proxy mesh automatically. UI: object picker/text, no numeric min/max.
    use_evaluated_proxy = True  # Input: True = use the evaluated proxy mesh (mods/armature/GN result), False = use the raw proxy mesh data. UI: boolean, hard False/True.
    #normal_smoothing = 0.0  # Input: 0 = use proxy normals as-is, 1 = heavily smooth proxy normals before lighting. UI: soft 0.0-0.5, hard 0.0-1.0.
    #pre_light_smoothing = 0.0  # Input: 0 = use raw proxy-vertex lighting, 1 = strongly smooth proxy lighting before transfer. UI: soft 0.0-0.5, hard 0.0-1.0.
    #post_light_smoothing = 0.0  # Input: 0 = keep transferred lighting detail, 1 = strongly smooth the transferred light cache. UI: soft 0.0-0.5, hard 0.0-1.0.
    #transfer_style = "Accurate"  # Input: Accurate, Balanced, or Smooth. UI: enum, no numeric min/max.
    #transfer_smoothness = 0.5  # Input: extra smoothing amount used by Balanced and Smooth transfer styles. UI: show only when transfer_style is Balanced or Smooth; soft 0.0-1.0, hard 0.0-1.0.
    # ---------------------------------------------------------------------------
    # Relight sources
    # ---------------------------------------------------------------------------
    #include_world_environment = True  # Input: True = include the active World / HDRI contribution. UI: boolean, hard False/True.
    #include_scene_lights = True  # Input: True = include Blender Sun / Point / Spot / Area lights. UI: boolean, hard False/True.
    # ---------------------------------------------------------------------------
    # World / HDRI source
    # Only matters when include_world_environment is True.
    # hdri_image_path blank = use the active World setup from the current scene.
    # ---------------------------------------------------------------------------
    hdri_image_path = ""  # Input: world HDRI image path or Blender image name; blank = use the active world setup. UI: show only when include_world_environment is True; path/text, no numeric min/max.
    environment_rotation_degrees = 0.0  # Input: extra manual rotation added on top of the active world mapping rotation. UI: show only when include_world_environment is True; soft -180 to 180, hard -1080 to 1080.
    #irradiance_resolution = 32  # Input: irradiance map height in pixels; width is doubled automatically. UI: show only when include_world_environment is True; soft 8-128, hard 4-512.
    #irradiance_blur_strength = 8  # Input: extra blur passes applied to the irradiance map. UI: show only when include_world_environment is True; soft 0-16, hard 0-64.
    #irradiance_luminance_clamp = 10.0  # Input: clamp hot HDRI pixels before building the irradiance map; 0 = off. UI: show only when include_world_environment is True; soft 0.0-20.0, hard 0.0-1000.0.
    # ---------------------------------------------------------------------------
    # World / HDRI occlusion
    # These affect the baked lighting cache itself, so changes here require a rebake.
    # ---------------------------------------------------------------------------
    #use_proxy_occlusion = True  # Input: True = approximate HDRI shadowing / AO by ray-casting the proxy mesh. UI: show only when include_world_environment is True; boolean, hard False/True.
    #occlusion_sample_count = 6  # Input: hemisphere rays per proxy sample when use_proxy_occlusion is enabled. UI: show only when use_proxy_occlusion is True; soft 1-16, hard 1-128.
    #occlusion_bias = 0.002  # Input: world-space offset for proxy-occlusion rays. UI: show only when use_proxy_occlusion is True; soft 0.0-0.02, hard 0.0-1.0.
    #occlusion_max_distance = 0.0  # Input: 0 = infinite AO/shadow ray distance; otherwise clamp to this world-space distance. UI: show only when use_proxy_occlusion is True; soft 0.0-2.0, hard 0.0-100.0.
    # ---------------------------------------------------------------------------
    # Scene lights
    # These affect the baked lighting cache itself, so changes here require a rebake.
    # ---------------------------------------------------------------------------
    #scene_light_gain = 1.0  # Input: overall multiplier applied while baking Blender light-object contribution. UI: show only when include_scene_lights is True; soft 0.0-4.0, hard 0.0-100.0.
    #include_hidden_lights = False  # Input: True = include hidden light objects as contributors. UI: show only when include_scene_lights is True; boolean, hard False/True.
    #use_light_shadows = True  # Input: True = ray-cast proxy self-shadowing for direct light objects. UI: show only when include_scene_lights is True; boolean, hard False/True.
    #light_shadow_bias = 0.002  # Input: world-space offset for direct-light shadow rays. UI: show only when use_light_shadows is True; soft 0.0-0.02, hard 0.0-1.0.
    # ---------------------------------------------------------------------------
    # Debug / error handling
    # ---------------------------------------------------------------------------
    show_progress_overlay = True  # Input: True = show bake progress in the viewport/status bar. UI: boolean, hard False/True.
    debug_verbose = True  # Input: True = print detailed numeric debug info to the console. UI: boolean, hard False/True.
    debug_sample_indices = "0,1,2,10,100,-1"  # Input: comma-separated logical splat indices to print as samples. UI: text, no numeric min/max.
    raise_on_error = False  # Input: True = raise actual exceptions, False = fail softly. UI: boolean, hard False/True.
    success = False
    status_message = ""
    target_object_name = ""
    proxy_object_name = ""
    logical_splat_count = 0
    environment_image_name = ""
    cache_package_dir = ""

    def load_utils():
        module_path = str(proxy_surface_relight_utils_path).strip()
        if not module_path:
            raise RuntimeError("proxy_surface_relight_utils_path is blank.")
        spec = importlib.util.spec_from_file_location(
            "proxy_deferred_layers_utils_runtime_build",
            module_path,
        )
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load proxy_deferred_layers_utils.py from '{module_path}'.")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def main():
        global success
        global status_message
        global target_object_name
        global proxy_object_name
        global logical_splat_count
        global environment_image_name
        global cache_package_dir
        print("Building proxy deferred relight bake cache...")
        utils = load_utils()
        mesh_obj = utils.resolve_target_mesh_object(
            target_mode=target_mode,
            target_obj=target_obj,
            proxy_binding_utils_path=proxy_binding_utils_path,
        )
        progress_started = False
        progress_end_message = ""
        try:
            if show_progress_overlay:
                utils.begin_proxy_deferred_progress_overlay(
                    total_steps=13,
                    object_name=mesh_obj.name,
                    title="Proxy Deferred Relight Bake",
                )
                progress_started = True
            result = utils.build_proxy_lighting_layers(
                mesh_obj,
                proxy_obj=proxy_obj,
                hdri_image_path=hdri_image_path,
                base_color_source_mode=base_color_source_mode,
                clamp_base_color=clamp_base_color,
                use_evaluated_proxy=use_evaluated_proxy,
                normal_smoothing=normal_smoothing,
                pre_light_smoothing=pre_light_smoothing,
                post_light_smoothing=post_light_smoothing,
                transfer_style=transfer_style,
                transfer_smoothness=transfer_smoothness,
                include_world_environment=include_world_environment,
                include_scene_lights=include_scene_lights,
                scene_light_gain=scene_light_gain,
                use_light_shadows=use_light_shadows,
                include_hidden_lights=include_hidden_lights,
                use_proxy_occlusion=use_proxy_occlusion,
                occlusion_sample_count=occlusion_sample_count,
                occlusion_bias=occlusion_bias,
                occlusion_max_distance=occlusion_max_distance,
                light_shadow_bias=light_shadow_bias,
                environment_rotation_degrees=environment_rotation_degrees,
                irradiance_resolution=irradiance_resolution,
                irradiance_blur_strength=irradiance_blur_strength,
                irradiance_luminance_clamp=irradiance_luminance_clamp,
                relight_cache_root=relight_cache_root,
                proxy_binding_utils_path=proxy_binding_utils_path,
                progress_callback=utils.update_proxy_deferred_progress_overlay if show_progress_overlay else None,
            )
            progress_end_message = f"Finished baking lighting cache for {mesh_obj.name}."
        except Exception:
            progress_end_message = f"Proxy deferred relight bake failed for {mesh_obj.name}."
            raise
        finally:
            if progress_started:
                utils.end_proxy_deferred_progress_overlay(progress_end_message)
        target_object_name = mesh_obj.name
        proxy_object_name = str(result["proxy_name"])
        logical_splat_count = int(result["logical_splat_count"])
        environment_image_name = str(result["image_name"])
        cache_package_dir = str(result["cache_package_dir"])
        success = True
        status_message = (
            f"Built proxy deferred relight bake cache for '{mesh_obj.name}' "
            f"({logical_splat_count:,} logical splats) from proxy '{proxy_object_name}'. "
            f"Cache package: {cache_package_dir}"
        )
        print(status_message)
        if debug_verbose:
            print(
                f"[PROXY DEFERRED DEBUG] image size={result['image_size'][0]}x{result['image_size'][1]} "
                f"strength={result['image_strength']:.6f} "
                f"tint=({result['image_tint'][0]:.6f}, {result['image_tint'][1]:.6f}, {result['image_tint'][2]:.6f}) "
                f"color_space={result['image_color_space']} "
                f"is_float={result['image_is_float']} "
                f"world='{result['world_name']}' "
                f"world_rotation_degrees={result['world_rotation_degrees']:.6f} "
                f"total_rotation_degrees={result['total_rotation_degrees']:.6f}"
            )
            print(
                f"[PROXY DEFERRED DEBUG] irradiance map size={result['irradiance_image_size'][0]}x{result['irradiance_image_size'][1]} "
                f"base_color_source_mode={result['base_color_source_mode']} "
                f"proxy_interpolation_mode={result['proxy_interpolation_mode']} "
                f"normal_smoothing={result['normal_smoothing']:.3f} "
                f"pre_light_smoothing={result['pre_light_smoothing']:.3f} "
                f"post_light_smoothing={result['post_light_smoothing']:.3f} "
                f"transfer_style={result['transfer_style']} "
                f"transfer_smoothness={result['transfer_smoothness']:.3f} "
                f"transfer_blend={result['transfer_smoothness_blend']:.3f}"
            )
            print(
                f"[PROXY DEFERRED DEBUG] world vector nodes={result['vector_node_types']} "
                f"unsupported_vector_nodes={result['unsupported_vector_nodes']}"
            )
            print(
                f"[PROXY DEFERRED DEBUG] world color nodes={result['color_node_types']} "
                f"unsupported_color_nodes={result['unsupported_color_nodes']}"
            )
            print(
                f"[PROXY DEFERRED DEBUG] cache files: state='{result['cache_state_path']}' "
                f"metadata='{result['cache_metadata_path']}'"
            )
            utils.debug_print_array_stats(
                "base_color_cache",
                result["base_color"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "proxy_vertex_normals_for_lighting",
                result["proxy_vertex_normals_for_lighting"],
                value_kind="generic",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "indirect_light_raw",
                result["indirect_color"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "direct_light_raw",
                result["direct_color"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "shadow_factor",
                result["shadow_factor"],
                value_kind="scalar",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "occlusion_factor",
                result["occlusion_factor"],
                value_kind="scalar",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "proxy_surface_distance",
                result["surface_distances"],
                value_kind="scalar",
                sample_indices=debug_sample_indices,
            )
    try:
        main()
    except Exception as exc:
        success = False
        status_message = f"Proxy deferred relight bake failed: {exc}"
        print(status_message)
        if raise_on_error:
            raise
