import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_relight2_1_build_base_color_from_f_dc_BAE18():
    relight_cache_root = bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory
    proxy_surface_relight_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_deferred_layers_utils.py')
    proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
    # UI range note: "Soft" means the recommended Serpens slider range; "Hard" means the safe absolute clamp.
    #proxy_surface_relight_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/relighting/proxy_deferred_layers_v2_overlay_only/proxy_deferred_layers_utils.py"  # Input: full path to proxy_deferred_layers_utils.py. UI: path text, no numeric min/max.
    #proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py. UI: path text, no numeric min/max.
    #relight_cache_root = "D:/GithubRepos/3DGS Render_Render Updates/relighting"  # Input: folder that stores the saved original proxy relight color packages. UI: folder path, no numeric min/max.
    target_mode = "Active"  # Input: Active or Input Object. UI: enum, no numeric min/max.
    target_obj = None  # Input: object pointer or object name. UI: show only when target_mode is Input Object; no numeric min/max.
    base_color_source_mode = "Saved Original"  # Input: Current f_dc or Saved Original. UI: enum, no numeric min/max; Saved Original is recommended.
    base_color_attr_name = "proxy_deferred_relight_base_color"  # Input: temp attribute name used for the base color layer. UI: text, no numeric min/max.
    clamp_base_color = True  # Input: True = clamp f_dc RGB into 0-1 before storing it. UI: boolean, hard False/True.
    show_progress_overlay = True  # Input: True = show base-color build progress in the viewport/status bar. UI: boolean, hard False/True.
    debug_verbose = True  # Input: True = print detailed numeric debug info to the console. UI: boolean, hard False/True.
    debug_sample_indices = "0,1,2,10,100,-1"  # Input: comma-separated logical splat indices to print as samples. UI: text, no numeric min/max.
    raise_on_error = False  # Input: True = raise actual exceptions, False = fail softly. UI: boolean, hard False/True.
    success = False
    status_message = ""
    target_object_name = ""
    logical_splat_count = 0
    mode_used = ""

    def load_utils():
        module_path = str(proxy_surface_relight_utils_path).strip()
        if not module_path:
            raise RuntimeError("proxy_surface_relight_utils_path is blank.")
        spec = importlib.util.spec_from_file_location(
            "proxy_surface_relight_utils_runtime_base",
            module_path,
        )
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load proxy_surface_relight_utils.py from '{module_path}'.")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def main():
        global success
        global status_message
        global target_object_name
        global logical_splat_count
        global mode_used
        print("Building proxy deferred relight base color layer from f_dc (legacy helper; not required for the Save -> Bake -> Write workflow)...")
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
                    total_steps=4,
                    object_name=mesh_obj.name,
                    title="Proxy Deferred Base Color",
                )
                progress_started = True
                utils.update_proxy_deferred_progress_overlay(
                    1,
                    4,
                    status_message="Reading f_dc color source...",
                )
            result = utils.build_base_color_from_f_dc(
                mesh_obj,
                base_color_attr_name=base_color_attr_name,
                clamp_base_color=clamp_base_color,
                source_mode=base_color_source_mode,
                relight_cache_root=relight_cache_root,
                proxy_binding_utils_path=proxy_binding_utils_path,
            )
            if progress_started:
                utils.update_proxy_deferred_progress_overlay(
                    4,
                    4,
                    status_message="Base color attribute written.",
                )
            progress_end_message = f"Finished base color build for {mesh_obj.name}."
        except Exception:
            progress_end_message = f"Proxy deferred base color build failed for {mesh_obj.name}."
            raise
        finally:
            if progress_started:
                utils.end_proxy_deferred_progress_overlay(progress_end_message)
        target_object_name = mesh_obj.name
        logical_splat_count = int(result["logical_splat_count"])
        mode_used = str(result["mode"])
        success = True
        status_message = (
            f"Built '{base_color_attr_name}' for '{mesh_obj.name}' "
            f"({logical_splat_count:,} logical splats) from {mode_used}."
        )
        print(status_message)
        if debug_verbose:
            utils.debug_print_array_stats(
                "f_dc_source_color",
                result["source_color"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                "f_dc_coeffs",
                result["f_dc_coeffs"],
                value_kind="generic",
                sample_indices=debug_sample_indices,
            )
            utils.debug_print_array_stats(
                base_color_attr_name,
                result["logical_color"],
                value_kind="color",
                sample_indices=debug_sample_indices,
            )
    try:
        main()
    except Exception as exc:
        success = False
        status_message = f"Proxy deferred relight base color build failed: {exc}"
        print(status_message)
        if raise_on_error:
            raise
