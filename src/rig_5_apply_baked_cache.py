import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_rig_5_apply_baked_cache_5656F(target_mode, target_obj):
    proxy_binding_cache_root = bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory
    target_mode = target_mode
    target_obj = target_obj
    proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
    success = None
    import inspect
    import sys
    #proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py, e.g. D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py
    #proxy_binding_cache_root = "D:/GithubRepos/3DGS Render_Render Updates/rigging"  # Input: optional folder for binding cache packages; blank = blend folder if saved, otherwise system temp
    #target_mode = "Active"  # Input: Active, Input Object, or All Bound
    #target_obj = None  # Input: mesh 3DGS object pointer or object name when target_mode is Input Object
    frame_to_apply = None  # Input: baked frame to apply; None = use current scene frame
    raise_on_error = False  # Input: when False, missing baked frames only print status instead of raising
    success = False
    status_message = ""
    sequence_available = False
    frame_exists = False
    applied_frame = None
    applied_splat_count = 0
    processed_count = 0
    failed_count = 0
    processed_names = []
    failed_names = []

    def load_proxy_binding_utils():
        module_name = "proxy_binding_utils"
        candidate_paths = []
        override_path = str(proxy_binding_utils_path).strip()
        if override_path:
            candidate_paths.append(os.path.abspath(bpy.path.abspath(override_path)))
        file_hint = globals().get("__file__") or inspect.getsourcefile(lambda: 0)
        if file_hint and os.path.exists(file_hint):
            script_dir = os.path.dirname(os.path.abspath(file_hint))
            candidate_paths.append(os.path.join(script_dir, "proxy_binding_utils.py"))
            candidate_paths.append(os.path.join(script_dir, "rigging", "proxy_binding_utils.py"))
        cwd = os.getcwd()
        candidate_paths.append(os.path.join(cwd, "proxy_binding_utils.py"))
        candidate_paths.append(os.path.join(cwd, "rigging", "proxy_binding_utils.py"))
        blend_dir = bpy.path.abspath("//")
        if blend_dir:
            candidate_paths.append(os.path.join(blend_dir, "proxy_binding_utils.py"))
            candidate_paths.append(os.path.join(blend_dir, "rigging", "proxy_binding_utils.py"))
        checked_paths = set()
        for module_path in candidate_paths:
            normalized = os.path.normpath(module_path)
            if normalized in checked_paths:
                continue
            checked_paths.add(normalized)
            if os.path.exists(normalized):
                spec = importlib.util.spec_from_file_location(module_name, normalized)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                sys.modules[module_name] = module
                return module
        text_name_candidates = (
            "proxy_binding_utils.py",
            "Rigging - proxy_binding_utils.py",
            "proxy_binding_utils",
            "Rigging - proxy_binding_utils",
        )
        for text_name in text_name_candidates:
            text_block = bpy.data.texts.get(text_name)
            if text_block:
                module = types.ModuleType(module_name)
                module.__file__ = text_name
                exec(compile(text_block.as_string(), text_name, "exec"), module.__dict__)
                sys.modules[module_name] = module
                return module
        for text_block in bpy.data.texts:
            if "proxy_binding_utils" in text_block.name.lower():
                module = types.ModuleType(module_name)
                module.__file__ = text_block.name
                exec(compile(text_block.as_string(), text_block.name, "exec"), module.__dict__)
                sys.modules[module_name] = module
                return module
        raise RuntimeError(
            "Could not find proxy_binding_utils.py. Set the top input variable "
            "'proxy_binding_utils_path' to the helper file on disk, or load "
            "proxy_binding_utils.py as a Blender text block too."
        )
    proxy_utils = load_proxy_binding_utils()
    proxy_utils.PROXY_BINDING_ROOT_OVERRIDE = str(proxy_binding_cache_root).strip()
    current_frame = int(bpy.context.scene.frame_current if frame_to_apply is None else frame_to_apply)
    applied_frame = current_frame
    print(f"Applying baked 3DGS attributes for frame {current_frame}...")
    try:
        mesh_objects = proxy_utils.resolve_target_mesh_objects(
            target_mode=target_mode,
            target_obj=target_obj,
            require_bound=True,
            allow_all=True,
            active_only=False,
        )
        single_target = len(mesh_objects) == 1
        first_error = None
        for mesh_obj in mesh_objects:
            try:
                paths, metadata, _, _ = proxy_utils.load_binding_package(mesh_obj)
                sequence_available = sequence_available or bool(mesh_obj.get(proxy_utils.PROXY_SEQUENCE_BINDING_PROP))
                current_frame_exists = os.path.exists(proxy_utils.bake_state_file_path(paths["bake_dir"], current_frame))
                frame_exists = frame_exists or current_frame_exists
                if not current_frame_exists:
                    message = (
                        f"No baked frame exists for frame {current_frame} on '{mesh_obj.name}'. "
                        f"Bake the sequence first, or bake a range that includes this frame."
                    )
                    print(message)
                    failed_count += 1
                    failed_names.append(mesh_obj.name)
                    if raise_on_error and first_error is None:
                        first_error = proxy_utils.ProxyBindingError(message)
                    continue
                state = proxy_utils.apply_baked_frame_to_mesh(mesh_obj, current_frame)
                applied_splat_count += len(state["logical_positions_local"])
                processed_count += 1
                processed_names.append(mesh_obj.name)
                sequence_available = sequence_available or bool(metadata.get("baked_frames"))
                print(f"Applied baked frame {current_frame} to '{mesh_obj.name}'.")
                print(f"Applied splats: {len(state['logical_positions_local']):,}")
            except Exception as exc:
                failed_count += 1
                failed_names.append(mesh_obj.name)
                print(f"Apply failed for '{mesh_obj.name}': {exc}")
                if first_error is None:
                    first_error = exc
        success = failed_count == 0 and processed_count > 0
        status_message = (
            f"Applied baked frame {current_frame} to {processed_count} 3DGS object(s); failed objects: {failed_count}."
        )
        print(status_message)
        if single_target and first_error is not None and raise_on_error:
            raise first_error
    except Exception as exc:
        status_message = f"Apply baked frame failed: {exc}"
        print(status_message)
        if raise_on_error:
            raise
    return success
