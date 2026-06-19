import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_relight2_4_restore_original_3dgs_color_08334():
    relight_cache_root = bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory
    proxy_surface_relight_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_deferred_layers_utils.py')
    proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
    # UI range note: "Soft" means the recommended Serpens slider range; "Hard" means the safe absolute clamp.
    #proxy_surface_relight_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/relighting/proxy_deferred_layers_v2_overlay_only/proxy_deferred_layers_utils.py"  # Input: full path to proxy_deferred_layers_utils.py. UI: path text, no numeric min/max.
    #proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py. UI: path text, no numeric min/max.
    #relight_cache_root = "D:/GithubRepos/3DGS Render_Render Updates/relighting"  # Input: optional folder for relight packages; blank = blend folder if saved, otherwise system temp. UI: folder path, no numeric min/max.
    target_mode = "Active"  # Input: Active or Input Object. UI: enum, no numeric min/max.
    target_obj = None  # Input: object pointer or object name. UI: show only when target_mode is Input Object; no numeric min/max.
    clear_temp_attributes = True  # Input: True = remove any leftover legacy temp relight attrs from older workflows. UI: boolean, hard False/True.
    clear_saved_state = False  # Input: True = remove the saved original color package after restore. UI: boolean, hard False/True.
    show_progress_overlay = True  # Input: True = show restore progress in the viewport/status bar. UI: boolean, hard False/True.
    raise_on_error = False  # Input: True = raise actual exceptions, False = fail softly. UI: boolean, hard False/True.
    success = False
    status_message = ""
    target_object_name = ""
    logical_splat_count = 0
    restored_sh_degree = 0
    removed_temp_attributes = []
    removed_saved_files = []

    def load_utils():
        module_path = str(proxy_surface_relight_utils_path).strip()
        if not module_path:
            raise RuntimeError("proxy_surface_relight_utils_path is blank.")
        spec = importlib.util.spec_from_file_location(
            "proxy_surface_relight_utils_runtime_restore",
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
        global logical_splat_count
        global restored_sh_degree
        global removed_temp_attributes
        global removed_saved_files
        print("Restoring the original saved 3DGS color state from proxy deferred relighting...")
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
                    total_steps=3,
                    object_name=mesh_obj.name,
                    title="Proxy Deferred Restore Original",
                )
                progress_started = True
                utils.update_proxy_deferred_progress_overlay(
                    1,
                    3,
                    status_message="Loading saved original color state...",
                )
            result = utils.restore_original_color_state(
                mesh_obj,
                relight_cache_root=relight_cache_root,
                clear_temp_attributes=clear_temp_attributes,
                clear_saved_state=clear_saved_state,
                proxy_binding_utils_path=proxy_binding_utils_path,
            )
            if progress_started:
                utils.update_proxy_deferred_progress_overlay(
                    3,
                    3,
                    status_message="Restored original color state.",
                )
            progress_end_message = f"Finished restoring original color for {mesh_obj.name}."
        except Exception:
            progress_end_message = f"Proxy deferred restore failed for {mesh_obj.name}."
            raise
        finally:
            if progress_started:
                utils.end_proxy_deferred_progress_overlay(progress_end_message)
        target_object_name = mesh_obj.name
        logical_splat_count = int(result["logical_splat_count"])
        restored_sh_degree = int(result["sh_degree"])
        removed_temp_attributes = list(result["removed_attributes"])
        removed_saved_files = list(result["removed_files"])
        success = True
        status_message = (
            f"Restored the original proxy deferred relight color for '{mesh_obj.name}' "
            f"({logical_splat_count:,} logical splats, SH degree {restored_sh_degree})."
        )
        print(status_message)
    try:
        main()
    except Exception as exc:
        success = False
        status_message = f"Proxy deferred relight restore failed: {exc}"
        print(status_message)
        if raise_on_error:
            raise
