import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Bake_Frames_To_Cache_90885(bpy.types.Operator):
    bl_idname = "sna.dgs_render_bake_frames_to_cache_90885"
    bl_label = "3DGS Render: Bake Frames to Cache"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        proxy_binding_cache_root = bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory

        deform_mode = bpy.context.scene.sna_dgs_scene_properties.rig_deform_mode
        scale_safety_mode = bpy.context.scene.sna_dgs_scene_properties.rig_scale_safety_mode
        bake_frame_step = bpy.context.scene.sna_dgs_scene_properties.rig_bake_frame_step
        bake_frame_start = bpy.context.scene.sna_dgs_scene_properties.rig_bake_start_frame
        bake_frame_end = bpy.context.scene.sna_dgs_scene_properties.rig_bake_end_frame
        update_sh_attributes = bpy.context.scene.sna_dgs_scene_properties.rig_update_sh_attributes
        sh_quality_mode = bpy.context.scene.sna_dgs_scene_properties.rig_sh_quality_mode
        proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
        import inspect
        import sys
        #proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py, e.g. D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py
        #proxy_binding_cache_root = "D:/GithubRepos/3DGS Render_Render Updates/rigging"  # Input: optional folder for binding cache packages; blank = blend folder if saved, otherwise system temp
        target_mode = "Active"  # Input: Active, Input Object, or All Bound
        target_obj = None  # Input: mesh 3DGS object pointer or object name when target_mode is Input Object
        #deform_mode = "Elastic"  # Input: Stable, Adaptive, or Elastic
        #scale_safety_mode = "Local Clamp"  # Input: Off, Global Clamp, or Local Clamp
        #sh_quality_mode = "Final"  # Input: Fast (24 samples), Balanced (32 samples), or Final (48 samples)
        #update_sh_attributes = True  # Input: True = rotate/update SH during bake; False = keep rest SH for faster preview-style bakes
        #bake_frame_start = None  # Input: first frame to bake; None = use scene.frame_start
        #bake_frame_end = None  # Input: last frame to bake; None = use scene.frame_end
        #bake_frame_step = 1  # Input: bake every Nth frame; 1 = every frame
        success = False
        status_message = ""
        baked_frame_count = 0
        bake_output_dir = ""
        sequence_available = False
        resolved_frame_start = None
        resolved_frame_end = None
        resolved_frame_step = None
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
        scene = bpy.context.scene
        try:
            resolved_frame_start, resolved_frame_end, resolved_frame_step = proxy_utils.resolve_bake_frame_range(
                scene,
                frame_start=bake_frame_start,
                frame_end=bake_frame_end,
                frame_step=bake_frame_step,
            )
            print(
                f"Baking proxy-driven 3DGS deformation for frames "
                f"{resolved_frame_start} to {resolved_frame_end}"
                f" (step {resolved_frame_step})..."
            )
            mesh_objects = proxy_utils.resolve_target_mesh_objects(
                target_mode=target_mode,
                target_obj=target_obj,
                require_bound=True,
                allow_all=True,
                active_only=True,
            )
            for mesh_obj in mesh_objects:
                try:
                    proxy_obj, baked_frames, removed_files = proxy_utils.bake_bound_animation_with_options(
                        mesh_obj,

                        deform_mode=deform_mode,
                        scale_safety_mode=scale_safety_mode,
                        sh_quality_mode=sh_quality_mode,
                        update_sh_attributes=update_sh_attributes,
                        frame_start=resolved_frame_start,
                        frame_end=resolved_frame_end,
                        frame_step=resolved_frame_step,
                    )
                    processed_count += 1
                    processed_names.append(mesh_obj.name)
                    baked_frame_count += len(baked_frames)
                    sequence_available = sequence_available or bool(mesh_obj.get(proxy_utils.PROXY_SEQUENCE_BINDING_PROP))
                    if single_target:
                        bake_output_dir = os.path.join(mesh_obj[proxy_utils.PROXY_BINDING_PATH_PROP], "baked_frames")
                    print(f"Baked '{mesh_obj.name}' from proxy '{proxy_obj.name}'.")
                    print(f"Frames baked: {len(baked_frames):,}")
                    print(f"Old baked frames removed first: {removed_files}")
                    if single_target:
                        print(f"Bake folder: {bake_output_dir}")
                    print(f"Binding method: {mesh_obj.get(proxy_utils.PROXY_BINDING_METHOD_PROP, 'Volumetric')}")
                except Exception as exc:
                    failed_count += 1
                    failed_names.append(mesh_obj.name)
                    print(f"Bake failed for '{mesh_obj.name}': {exc}")
            success = failed_count == 0 and processed_count > 0
            status_message = (
                f"Baked {baked_frame_count:,} frame state(s) across {processed_count} bound 3DGS object(s); "
                f"failed objects: {failed_count}."
            )
            print(status_message)
            print(f"Binding root: {proxy_utils.get_binding_root_dir()}")
            print(
                f"Bake mode: {deform_mode} | Scale safety: {scale_safety_mode} | "
                f"SH quality: {sh_quality_mode} | Update SH: {bool(proxy_utils.normalize_update_sh_attributes(update_sh_attributes))}"
            )
        except Exception as exc:
            status_message = f"Proxy bake failed: {exc}"
            print(status_message)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
