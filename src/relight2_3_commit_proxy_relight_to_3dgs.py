import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_relight2_3_commit_proxy_relight_to_3dgs_6E60F():
    relight_cache_root = bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory
    indirect_strength = bpy.context.scene.sna_dgs_scene_properties.indirect_strength
    direct_strength = bpy.context.scene.sna_dgs_scene_properties.direct_strength
    occlusion_strength = bpy.context.scene.sna_dgs_scene_properties.occlusion_strength
    shadow_strength = bpy.context.scene.sna_dgs_scene_properties.shadow_strength
    lighting_factor_mode = bpy.context.scene.sna_dgs_scene_properties.relight_lighting_factor_mode
    factor_curve_mode = bpy.context.scene.sna_dgs_scene_properties.relight_factor_curve_mode
    colorize_mix = bpy.context.scene.sna_dgs_scene_properties.relight_colorize_mix
    max_color_tint = bpy.context.scene.sna_dgs_scene_properties.relight_max_color_tint
    ambient_floor = bpy.context.scene.sna_dgs_scene_properties.ambient_floor
    light_gain = bpy.context.scene.sna_dgs_scene_properties.light_gain
    light_power = bpy.context.scene.sna_dgs_scene_properties.light_power
    max_light_factor = bpy.context.scene.sna_dgs_scene_properties.max_light_factor
    sh_mode = bpy.context.scene.sna_dgs_scene_properties.export_mode
    original_sh_strength = bpy.context.scene.sna_dgs_scene_properties.directionality_strength
    clamp_relight_color = True
    max_color_tint_mode = bpy.context.scene.sna_dgs_scene_properties.max_color_tint_mode
    proxy_surface_relight_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_deferred_layers_utils.py')
    proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
    # UI range note: "Soft" means the recommended Serpens slider range; "Hard" means the safe absolute clamp.
    #proxy_surface_relight_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/relighting/proxy_deferred_layers_v2_overlay_only/proxy_deferred_layers_utils.py"  # Input: full path to proxy_deferred_layers_utils.py. UI: path text, no numeric min/max.
    #proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py. UI: path text, no numeric min/max.
    #relight_cache_root = "D:/GithubRepos/3DGS Render_Render Updates/relighting"  # Input: folder that stores the saved original state and baked lighting cache. UI: folder path, no numeric min/max.
    target_mode = "Active"  # Input: Active or Input Object. UI: enum, no numeric min/max.
    target_obj = None  # Input: object pointer or object name. UI: show only when target_mode is Input Object; no numeric min/max.
    # ---------------------------------------------------------------------------
    # Cheap composition controls
    # These do not reread the world or proxy. They only remix the baked cache.
    # ---------------------------------------------------------------------------
    #indirect_strength = 1.0  # Input: overall strength of the baked indirect / HDRI fill. UI: soft 0.0-2.0, hard 0.0-20.0.
    #direct_strength = 1.0  # Input: overall strength of the baked direct light contribution. UI: soft 0.0-2.0, hard 0.0-20.0.
    #occlusion_strength = 0.7  # Input: 0 = ignore baked occlusion, 1 = use baked occlusion fully. UI: soft 0.0-1.0, hard 0.0-1.0.
    #shadow_strength = 1.0  # Input: 0 = ignore baked direct-light shadowing, 1 = use baked shadowing fully. UI: soft 0.0-1.0, hard 0.0-1.0.
    #lighting_factor_mode = "Tinted Luminance"  # Input: Luminance, Tinted Luminance, or RGB. UI: enum, no numeric min/max.
    #factor_curve_mode = "Reinhard"  # Input: Reinhard or Linear. UI: enum, no numeric min/max.
    #colorize_mix = 0.20  # Input: 0 = preserve original base hue, 1 = stronger light color tinting. UI: soft 0.0-0.5, hard 0.0-1.0.
    #max_color_tint = 2.0  # Input: clamp for per-channel light tint. UI: show only when lighting_factor_mode is Tinted Luminance; soft 1.0-3.0, hard 0.0-10.0.
    # Perceived Brightness = original method; limiting RGB tint can also change visible brightness.
    # Preserve Luminance = limits color cast while keeping the tint's numeric luminance at 1.0; values below 1.0 are treated as 1.0.
    #max_color_tint_mode = "Perceived Brightness"  # Input: Perceived Brightness or Preserve Luminance. UI: show only when lighting_factor_mode is Tinted Luminance; enum, no numeric min/max.
    #ambient_floor = 0.08  # Input: minimum ambient light factor before multiplying the base color. UI: soft 0.0-0.3, hard 0.0-2.0.
    #light_gain = 0.85  # Input: overall light factor multiplier. UI: soft 0.0-2.0, hard 0.0-20.0.
    #light_power = 0.75  # Input: contrast/power applied to the normalized light factor. UI: soft 0.25-2.0, hard 0.01-8.0.
    #max_light_factor = 1.75  # Input: clamp for the final light factor to avoid blow-outs. UI: soft 0.5-4.0, hard 0.0-100.0.
    # ---------------------------------------------------------------------------
    # 3DGS SH export / write mode
    # - "Flatten SH": writes the relit color into f_dc and sets f_rest / higher-order SH to 0.
    # - "Preserve Original SH": writes the relit color into f_dc and restores the saved original f_rest at full strength.
    # - "Dampen Original SH": writes the relit color into f_dc and restores the saved original f_rest multiplied by original_sh_strength.
    # ---------------------------------------------------------------------------
    #sh_mode = "Flatten SH"  # Input: Flatten SH, Preserve Original SH, or Dampen Original SH. UI: enum, no numeric min/max.
    #original_sh_strength = 0.25  # Input: only used by Dampen Original SH; 0 = flattened f_rest SH, 1 = full saved original f_rest SH. UI: show only for Dampen Original SH; soft 0.0-0.5, hard 0.0-1.0.
    #clamp_relight_color = True  # Input: True = clamp final RGB to 0-1 before writing f_dc. UI: boolean, hard False/True.
    # ---------------------------------------------------------------------------
    # Debug / error handling
    # ---------------------------------------------------------------------------
    show_progress_overlay = True  # Input: True = show write/commit progress in the viewport/status bar. UI: boolean, hard False/True.
    debug_verbose = True  # Input: True = print detailed numeric debug info to the console. UI: boolean, hard False/True.
    debug_sample_indices = "0,1,2,10,100,-1"  # Input: comma-separated logical splat indices to print as samples. UI: text, no numeric min/max.
    raise_on_error = False  # Input: True = raise actual exceptions, False = fail softly. UI: boolean, hard False/True.
    success = False
    status_message = ""
    target_object_name = ""
    logical_splat_count = 0
    resolved_export_mode = ""
    bake_package_dir = ""

    def load_utils():
        module_path = str(proxy_surface_relight_utils_path).strip()
        if not module_path:
            raise RuntimeError("proxy_surface_relight_utils_path is blank.")
        spec = importlib.util.spec_from_file_location(
            "proxy_deferred_layers_utils_runtime_commit",
            module_path,
        )
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load proxy_deferred_layers_utils.py from '{module_path}'.")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def resolve_utility_sh_settings(mode_name, strength):
        compact = "".join(
            ch for ch in str(mode_name).strip().lower().replace("_", " ") if ch.isalnum()
        )
        if compact in (
            "",
            "compatible",
            "flat",
            "flatten",
            "flattensh",
            "zerosh",
            "zerofrest",
            "zerofrestsh",
            "fdconly",
            "fdconlyzerofrest",
            "fdconlyzerofrestsh",
        ):
            return "Flatten SH", 0.0
        if compact in (
            "preserveoriginalsh",
            "restoreoriginalsh",
            "useoriginalsh",
            "originalsh",
            "preservesavedsh",
            "restoresavedsh",
        ):
            return "Preserve Original SH", 1.0
        if compact in (
            "dampensavedoriginaldirectionality",
            "savedoriginaldirectionality",
            "dampedoriginal",
            "enhanced",
            "dampenoriginalsh",
            "dampensavedsh",
            "dampensavedoriginalsh",
            "fdcsavedoriginalfrestdamped",
            "fdcsavedoriginalfrestshdamped",
        ):
            return "Dampen Original SH", strength
        return str(mode_name), strength

    def main():
        global success
        global status_message
        global target_object_name
        global logical_splat_count
        global resolved_export_mode
        global bake_package_dir
        print("Committing proxy deferred relight baked cache back into the real 3DGS attributes...")
        utils = load_utils()
        mesh_obj = utils.resolve_target_mesh_object(
            target_mode=target_mode,
            target_obj=target_obj,
            proxy_binding_utils_path=proxy_binding_utils_path,
        )
        resolved_sh_export_mode, resolved_sh_strength = resolve_utility_sh_settings(
            sh_mode,
            original_sh_strength,
        )
        progress_started = False
        progress_end_message = ""
        try:
            if show_progress_overlay:
                utils.begin_proxy_deferred_progress_overlay(
                    total_steps=6,
                    object_name=mesh_obj.name,
                    title="Proxy Deferred Relight Write",
                )
                progress_started = True
                utils.update_proxy_deferred_progress_overlay(
                    1,
                    6,
                    status_message="Loading baked lighting cache...",
                )
            result = utils.commit_composed_color_to_3dgs(
                mesh_obj,
                indirect_strength=indirect_strength,
                direct_strength=direct_strength,
                occlusion_strength=occlusion_strength,
                shadow_strength=shadow_strength,
                lighting_factor_mode=lighting_factor_mode,
                factor_curve_mode=factor_curve_mode,
                colorize_mix=colorize_mix,
                max_color_tint=max_color_tint,
                max_color_tint_mode=max_color_tint_mode,
                ambient_floor=ambient_floor,
                light_gain=light_gain,
                light_power=light_power,
                max_light_factor=max_light_factor,
                export_mode=resolved_sh_export_mode,
                directionality_strength=resolved_sh_strength,
                clamp_relight_color=clamp_relight_color,
                relight_cache_root=relight_cache_root,
                proxy_binding_utils_path=proxy_binding_utils_path,
            )
            if progress_started:
                utils.update_proxy_deferred_progress_overlay(
                    6,
                    6,
                    status_message="Composed color written to 3DGS attributes.",
                )
            progress_end_message = f"Finished writing relit color for {mesh_obj.name}."
        except Exception:
            progress_end_message = f"Proxy deferred relight write failed for {mesh_obj.name}."
            raise
        finally:
            if progress_started:
                utils.end_proxy_deferred_progress_overlay(progress_end_message)
        target_object_name = mesh_obj.name
        logical_splat_count = int(result["logical_splat_count"])
        resolved_export_mode = str(result["resolved_export_mode"])
        bake_package_dir = str(result["bake_package_dir"])
        success = True
        status_message = (
            f"Committed baked proxy deferred relight cache to '{mesh_obj.name}' "
            f"({logical_splat_count:,} logical splats) using export mode '{resolved_export_mode}'. "
            f"clamp_relight_color={bool(result['clamped'])}."
        )
        print(status_message)
        if debug_verbose:
            print(
                f"[PROXY DEFERRED DEBUG] clamp stats before commit: "
                f"below_zero={float(result['clipped_low_pct']):.3f}% "
                f"above_one={float(result['clipped_high_pct']):.3f}% "
                f"mean_luminance={float(result['mean_luminance']):.6f} "
                f"reference_mean_luminance={float(result['reference_mean_luminance']):.6f} "
                f"indirect_mean={float(result['indirect_base_mean_luminance']):.6f} "
                f"direct_mean={float(result['direct_base_mean_luminance']):.6f} "
                f"source_strength_sum={float(result['source_strength_sum']):.6f} "
                f"factor_mode={result['factor_mode']} "
                f"factor_curve_mode={result['factor_curve_mode']} "
                f"max_color_tint_mode={result['max_color_tint_mode']}"
            )
            print(
                f"[PROXY DEFERRED DEBUG] bake package='{bake_package_dir}' "
                f"baked_at='{result['bake_metadata'].get('baked_at_utc', '')}' "
                f"base_color_source='{result['bake_metadata'].get('base_color_source_mode', '')}'"
            )
            utils.debug_print_array_stats(
                "base_color_cache",
                result["base_color"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "indirect_light_raw",
                result["indirect_color_raw"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "direct_light_raw",
                result["direct_color_raw"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "occlusion_factor",
                result["occlusion_factor"],
                value_kind="scalar",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "shadow_factor",
                result["shadow_factor"],
                value_kind="scalar",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "shaded_indirect",
                result["shaded_indirect"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "shaded_direct",
                result["shaded_direct"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "light_tint_color",
                result["light_tint_color"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "light_factor_scalar",
                result["light_factor_scalar"],
                value_kind="scalar",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "light_factor_rgb",
                result["light_factor_rgb"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "final_color_before_clamp",
                result["relit_color_before_clamp"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "final_color_after_clamp",
                result["relit_color_after_clamp"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "committed_f_dc_coeffs",
                result["new_dc_coeffs"],
                value_kind="generic",
                sample_indices=debug_sample_indices,
            )
    try:
        main()
    except Exception as exc:
        success = False
        status_message = f"Proxy deferred relight commit failed: {exc}"
        print(status_message)
        if raise_on_error:
            raise
