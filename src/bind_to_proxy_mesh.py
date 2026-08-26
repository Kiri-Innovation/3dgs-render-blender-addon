import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Bind_To_Proxy_Mesh_6C58F(bpy.types.Operator):
    bl_idname = "sna.dgs_render_bind_to_proxy_mesh_6c58f"
    bl_label = "3DGS Render: Bind to Proxy Mesh"
    bl_description = "Binds the Active Object to the assigned Proxy Mesh."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is None:
            self.report({'WARNING'}, message='Binding cancelled: select a 3DGS mesh object first.')
            return {'CANCELLED'}
        proxy_mesh_object = active_obj.sna_dgs_object_properties.rig_proxy_mesh
        if proxy_mesh_object is None:
            self.report({'WARNING'}, message='Binding cancelled: assign a Proxy Mesh first.')
            return {'CANCELLED'}
        if proxy_mesh_object.type == 'MESH':
            if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh == bpy.context.view_layer.objects.active):
                self.report({'WARNING'}, message='Binding cancelled: the Proxy Mesh cannot be the active 3DGS object.')
                return {'CANCELLED'}
            else:
                CHILD_NAME = bpy.context.view_layer.objects.active.name
                PARENT_NAME = bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh.name
                # ==========================================
                # VARIABLES (Set these for your Serprens node)
                # ==========================================
                #CHILD_NAME = "Cube"      # Replace with the name of the object to be parented
                #PARENT_NAME = "Sphere"   # Replace with the name of the target parent object
                # ==========================================
                # SCRIPT LOGIC
                # ==========================================

                def parent_keep_transform(child_name, parent_name):
                    # 1. Fetch the objects securely from the Data API
                    child = bpy.data.objects.get(child_name)
                    parent = bpy.data.objects.get(parent_name)
                    # 2. Safety check: Ensure both objects actually exist in the file
                    if not child:
                        print(f"Error: Could not find child object '{child_name}'")
                        return
                    if not parent:
                        print(f"Error: Could not find parent object '{parent_name}'")
                        return
                    # 3. Safety check: Prevent an object from parenting to itself
                    if child == parent:
                        print("Error: Object cannot be a parent of itself.")
                        return
                    # 4. Perform the hierarchy change
                    child.parent = parent
                    # 5. Apply the inverse matrix math to freeze the visual transform
                    child.matrix_parent_inverse = parent.matrix_world.inverted()
                    # Optional: Force a scene update so the viewport refreshes instantly
                    bpy.context.view_layer.update()
                    print(f"Success: '{child_name}' parented to '{parent_name}' with transforms kept.")
                # Execute the function using the variables at the top
                proxy_binding_cache_root = bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory
                binding_method = bpy.context.scene.sna_dgs_scene_properties.rig_bind_method
                hybrid_surface_distance_factor = bpy.context.scene.sna_dgs_scene_properties.rig_surface_dist_factor
                proxy_neighbor_count = bpy.context.scene.sna_dgs_scene_properties.rig_bind_samples
                proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
                import inspect
                import sys
                #proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py, e.g. D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py
                #proxy_binding_cache_root = "D:/GithubRepos/3DGS Render_Render Updates/rigging"  # Input: optional folder for binding cache packages; blank = blend folder if saved, otherwise system temp
                target_mode = "Active"  # Input: Active or Input Object
                target_obj = None  # Input: mesh 3DGS object pointer or object name when target_mode is Input Object
                #proxy_mesh_object = None  # Input: proxy mesh object pointer or object name; if empty, fallback uses the selected proxy mesh
                #binding_method = "Volumetric"  # Input: Volumetric, Surface, or Hybrid
                #proxy_neighbor_count = 32  # Input: nearest proxy vertices per splat; higher counts are more stable for volumetric splats
                #hybrid_surface_distance_factor = 1.5  # Input: Hybrid only; lower = more volumetric, higher = more surface-following
                success = False
                status_message = ""
                binding_package_path = ""
                binding_root_path = ""
                binding_method_used = ""

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
                register_proxy_binding_gpu_module(proxy_utils)
                apply_gpu_sh_addon_pref()
                proxy_utils.PROXY_BINDING_ROOT_OVERRIDE = str(proxy_binding_cache_root).strip()
                print("Binding active mesh 3DGS object to proxy mesh...")
                try:
                    mesh_obj = proxy_utils.resolve_target_mesh_object(
                        target_mode=target_mode,
                        target_obj=target_obj,
                        require_bound=False,
                        allow_all=False,
                    )
                    mesh_obj, proxy_obj, metadata = proxy_utils.bind_3dgs_object_to_proxy(
                        mesh_obj,
                        proxy_input=proxy_mesh_object,
                        neighbor_count=proxy_neighbor_count,
                        binding_method=binding_method,
                        hybrid_surface_distance_factor=hybrid_surface_distance_factor,
                    )
                    success = True
                    binding_package_path = mesh_obj[proxy_utils.PROXY_BINDING_PATH_PROP]
                    binding_root_path = proxy_utils.get_binding_root_dir()
                    binding_method_used = metadata.get("binding_method", binding_method)
                    status_message = f"Bound '{mesh_obj.name}' to proxy '{proxy_obj.name}'."
                    mesh_obj.lock_location = (True, True, True)
                    mesh_obj.lock_rotation = (True, True, True)
                    mesh_obj.lock_scale = (True, True, True)
                    parent_keep_transform(mesh_obj.name, proxy_obj.name)
                    mesh_obj['rig_baked_render_enabled'] = True
                    print(
                        f"Bound '{mesh_obj.name}' to proxy '{proxy_obj.name}' using "
                        f"binding method '{binding_method_used}'."
                    )
                    if metadata["binding_method"] == "Volumetric":
                        print(f"Nearest proxy vertices per splat: {metadata['neighbors_per_splat']}")
                    elif metadata["binding_method"] == "Hybrid":
                        print(f"Nearest proxy vertices per splat: {metadata['neighbors_per_splat']}")
                        print(
                            f"Hybrid classification: surface={metadata.get('hybrid_surface_count', 0):,}, "
                            f"volumetric={metadata.get('hybrid_volumetric_count', 0):,}, "
                            f"surface distance factor={metadata.get('hybrid_surface_distance_factor', hybrid_surface_distance_factor)}"
                        )
                    print(f"Splats bound: {metadata['splat_count']:,}")
                    print(f"Binding package: {binding_package_path}")
                    print(f"Binding root: {binding_root_path}")
                    print("The 3DGS object now has a rest cache and can be updated, baked, or restored later.")
                except proxy_utils.ProxyBindingError as exc:
                    status_message = f"Proxy bind failed: {exc}"
                    print(status_message)
                    self.report({'WARNING'}, message=f"Binding cancelled: {exc}")
                    return {'CANCELLED'}
                except Exception as exc:
                    status_message = f"Proxy bind failed: {exc}"
                    print(status_message)
                    raise
        else:
            self.report({'WARNING'}, message='Binding cancelled: the assigned Proxy Mesh must be a mesh object.')
            return {'CANCELLED'}
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
