import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Unbind_From_Proxy_Mesh_7648D(bpy.types.Operator):
    bl_idname = "sna.dgs_render_unbind_from_proxy_mesh_7648d"
    bl_label = "3DGS Render: Unbind from Proxy Mesh"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        bpy.context.view_layer.objects.active.lock_location = (False, False, False)
        bpy.context.view_layer.objects.active.lock_rotation = (False, False, False)
        bpy.context.view_layer.objects.active.lock_scale = (False, False, False)
        bpy.context.view_layer.objects.active.parent = None
        object_name = bpy.context.view_layer.objects.active.name
        property_name = 'proxy_binding_active'
        # Replace these with your object and property names
        #object_name = "Cube"
        #property_name = "my_custom_prop"
        # Get the object
        obj = bpy.data.objects.get(object_name)
        if obj is None:
            print(f"Error: Object '{object_name}' not found in the scene")
        else:
            if property_name in obj:
                del obj[property_name]
                print(f"Removed property '{property_name}' from object '{object_name}'")
            else:
                print(f"Property '{property_name}' not found on object '{object_name}'")
        proxy_binding_cache_root = bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory
        proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
        import inspect
        import sys
        #proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py, e.g. D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py
        #proxy_binding_cache_root = "D:/GithubRepos/3DGS Render_Render Updates/rigging"  # Input: optional folder for binding cache packages; blank = blend folder if saved, otherwise system temp
        target_mode = "Active"  # Input: Active, Input Object, or All Bound
        target_obj = None  # Input: mesh 3DGS object pointer or object name when target_mode is Input Object
        success = False
        status_message = ""
        processed_count = 0
        failed_count = 0
        processed_names = []
        failed_names = []

        def load_proxy_binding_utils():
            import bpy
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
        print("Restoring the original saved 3DGS attributes...")
        try:
            mesh_objects = proxy_utils.resolve_target_mesh_objects(
                target_mode=target_mode,
                target_obj=target_obj,
                require_bound=True,
                allow_all=True,
                active_only=True,
            )
            for mesh_obj in mesh_objects:
                try:
                    rest_state = proxy_utils.restore_original_bound_state(mesh_obj)
                    processed_count += 1
                    processed_names.append(mesh_obj.name)
                    print(f"Restored '{mesh_obj.name}' to its original unbound state.")
                    print(f"Restored splats: {len(rest_state['logical_positions_local']):,}")
                    print("The binding cache stays on disk, but live proxy updating is now disabled for this object.")
                except Exception as exc:
                    failed_count += 1
                    failed_names.append(mesh_obj.name)
                    print(f"Unbind failed for '{mesh_obj.name}': {exc}")
            success = failed_count == 0 and processed_count > 0
            status_message = (
                f"Restored {processed_count} bound 3DGS object(s); failed: {failed_count}."
            )
            print(status_message)
        except Exception as exc:
            status_message = f"Proxy unbind failed: {exc}"
            print(status_message)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
