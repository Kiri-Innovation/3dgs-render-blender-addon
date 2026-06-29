import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .apply_all_modifiers_for_export import sna_apply_all_modifiers_for_export_B90C0
from .duplicate_object import sna_duplicate_object_ED1F0
from .. import dgs_render__export

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Export_Mesh_As_3Dgs4Dgs_Ce2F7(bpy.types.Operator):
    bl_idname = "sna.dgs_render_export_mesh_as_3dgs4dgs_ce2f7"
    bl_label = "3DGS Render: Export Mesh As 3DGS/4DGS"
    bl_description = "Applies scale and rotation transforms, applies color modifiers and exports the active object as a 3DGS .ply"
    bl_options = {"REGISTER", "UNDO"}
    sna_send_to_world_centre: bpy.props.BoolProperty(name='Send to World Centre', description='', options={'HIDDEN'}, default=True)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if os.path.isdir(bpy.context.scene.sna_dgs_scene_properties.export_output_path):
            if (bpy.context.view_layer.objects.active == None):
                self.report({'ERROR'}, message='No Active Object')
            else:
                if (len(bpy.context.view_layer.objects.selected) > 1):
                    self.report({'ERROR'}, message='Only select 1 object please.')
                else:
                    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.view_layer.objects.active.modifiers):
                        dgs_render__export['sna_export_base_object'] = bpy.context.view_layer.objects.active
                        if self.sna_send_to_world_centre:
                            bpy.context.view_layer.objects.active.location = (0.0, 0.0, 0.0)
                        if bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == "3DGS":
                            new_object_name_0_52da7 = sna_duplicate_object_ED1F0(dgs_render__export['sna_export_base_object'].name)
                            dgs_render__export['sna_export_temp_object'] = bpy.data.objects[new_object_name_0_52da7]
                            dgs_render__export['sna_export_temp_object'].select_set(state=True, view_layer=bpy.context.view_layer, )
                            dgs_render__export['sna_export_temp_object'].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = True
                            dgs_render__export['sna_export_temp_object'].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = True

                            def delayed_C77D9():
                                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                                    dgs_render__export['sna_export_base_object'].sna_dgs_object_properties.update_mode = 'Disable Camera Updates'
                                sna_apply_all_modifiers_for_export_B90C0(dgs_render__export['sna_export_temp_object'].name)
                                target_obj_name = dgs_render__export['sna_export_temp_object'].name
                                load_export_transform_utils().apply_transforms_to_object(target_obj_name)

                                def delayed_5B08A():
                                    bpy.ops.wm.ply_export(filepath=os.path.join(bpy.context.scene.sna_dgs_scene_properties.export_output_path,dgs_render__export['sna_export_base_object'].name + bpy.context.scene.sna_dgs_scene_properties.export_suffix + '.ply'), export_selected_objects=True, export_attributes=True)
                                    bpy.data.objects.remove(object=dgs_render__export['sna_export_temp_object'], do_unlink=True, do_id_user=True, do_ui_user=True, )
                                bpy.app.timers.register(delayed_5B08A, first_interval=0.10000000149011612)
                            bpy.app.timers.register(delayed_C77D9, first_interval=0.10000000149011612)
                        elif bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == "4DGS":
                            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                                bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
                                bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode = 'Disable Camera Updates'
                            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Animate_GN' in bpy.context.view_layer.objects.active.modifiers):
                                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_viewport:
                                    if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 1) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 2)):
                                        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] = 0
                            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = True
                            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = True
                            bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
                            if bpy.context and bpy.context.screen:
                                for a in bpy.context.screen.areas:
                                    a.tag_redraw()
                            target_obj_name = bpy.context.view_layer.objects.active.name
                            load_export_transform_utils().apply_transforms_to_object(target_obj_name)
                            source_obj_name = bpy.context.view_layer.objects.active.name
                            start_frame = bpy.context.scene.frame_start
                            end_frame = bpy.context.scene.frame_end
                            RIG_BAKED_UPDATE_MODE = bpy.context.scene.sna_dgs_scene_properties.r2_render_rig_cache_mode
                            output_object_list = None
                            import inspect
                            import sys
                            #source_obj_name = ""  # Input: source mesh object name; blank = active object
                            #start_frame = None  # Input: first frame to duplicate; blank/None = scene frame_start
                            #end_frame = None  # Input: last frame to duplicate; blank/None = scene frame_end
                            frame_step = 1  # Input: duplicate every Nth frame
                            #RIG_BAKED_UPDATE_MODE = "None"  # Input: None, Enabled Baked, or All Baked
                            RIG_BAKED_ENABLED_PROP_NAME = "rig_baked_render_enabled"  # Input: source object custom property checked when mode is Enabled Baked
                            MISSING_BAKED_FRAME_MODE = "Keep Current"  # Input: Keep Current, Skip Frame, Restore Rest, or Error
                            proxy_binding_utils_path = os.path.join(os.path.dirname(__file__), 'assets', 'proxy_binding_utils.py')
                            raise_on_error = False  # Input: when False, missing/corrupt baked data reports softly instead of raising
                            output_object_list = []
                            success = False
                            status_message = ""
                            generated_count = 0
                            processed_frame_count = 0
                            skipped_frame_count = 0
                            failed_frame_count = 0
                            rig_applied_frame_count = 0
                            rig_missing_frame_count = 0
                            used_baked_rig_updates = False

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
                                    candidate_paths.append(os.path.join(script_dir, "..", "rigging", "proxy_binding_utils.py"))
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
                                raise RuntimeError(
                                    "Could not find proxy_binding_utils.py. Set 'proxy_binding_utils_path' to the helper file on disk "
                                    "or load proxy_binding_utils.py as a Blender text block."
                                )

                            def get_source_object():
                                obj_name = str(source_obj_name).strip()
                                if obj_name:
                                    obj = bpy.data.objects.get(obj_name)
                                    if obj is None:
                                        raise ValueError(f"Object '{obj_name}' not found.")
                                else:
                                    obj = bpy.context.view_layer.objects.active
                                    if obj is None:
                                        raise ValueError("No active object found and source_obj_name is blank.")
                                if obj.type != "MESH":
                                    raise ValueError(f"Object '{obj.name}' is not a mesh.")
                                return obj

                            def normalize_rig_baked_update_mode(value):
                                text = str(value).strip().lower()
                                if text in {"", "none"}:
                                    return "None"
                                if text in {"enabled baked", "enabled_baked", "enabled"}:
                                    return "Enabled Baked"
                                if text in {"all baked", "all_baked", "all"}:
                                    return "All Baked"
                                raise ValueError("RIG_BAKED_UPDATE_MODE must be None, Enabled Baked, or All Baked.")

                            def normalize_missing_baked_frame_mode(value):
                                text = str(value).strip().lower()
                                if text in {"", "keep current", "keep_current", "keep"}:
                                    return "Keep Current"
                                if text in {"skip frame", "skip_frame", "skip"}:
                                    return "Skip Frame"
                                if text in {"restore rest", "restore_rest", "rest"}:
                                    return "Restore Rest"
                                if text in {"error", "raise"}:
                                    return "Error"
                                raise ValueError(
                                    "MISSING_BAKED_FRAME_MODE must be Keep Current, Skip Frame, Restore Rest, or Error."
                                )

                            def resolve_frame_range(scene):
                                resolved_start = int(scene.frame_start if start_frame in (None, "") else start_frame)
                                resolved_end = int(scene.frame_end if end_frame in (None, "") else end_frame)
                                resolved_step = max(1, int(frame_step))
                                if resolved_end < resolved_start:
                                    raise ValueError("end_frame must be greater than or equal to start_frame.")
                                return resolved_start, resolved_end, resolved_step

                            def duplicate_evaluated_mesh(source_obj, collection, depsgraph, frame_number):
                                eval_obj = source_obj.evaluated_get(depsgraph)
                                new_mesh = bpy.data.meshes.new_from_object(eval_obj)
                                new_obj = bpy.data.objects.new(f"{source_obj.name}_baked_f{frame_number}", new_mesh)
                                new_obj.matrix_world = source_obj.matrix_world.copy()
                                collection.objects.link(new_obj)
                                return new_obj
                            scene = bpy.context.scene
                            collection = scene.collection
                            try:
                                source_obj = get_source_object()
                                rig_baked_update_mode = normalize_rig_baked_update_mode(RIG_BAKED_UPDATE_MODE)
                                missing_baked_frame_mode = normalize_missing_baked_frame_mode(MISSING_BAKED_FRAME_MODE)
                                resolved_start, resolved_end, resolved_step = resolve_frame_range(scene)
                                frame_numbers = list(range(resolved_start, resolved_end + 1, resolved_step))
                                print(f"Duplicating evaluated mesh '{source_obj.name}' for {len(frame_numbers)} frame(s)...")
                                print(
                                    f"Rig baked settings: Mode={rig_baked_update_mode}, "
                                    f"MissingFrame={missing_baked_frame_mode}, EnabledProp={RIG_BAKED_ENABLED_PROP_NAME}"
                                )
                                original_frame = int(scene.frame_current)
                                original_hide_viewport = bool(source_obj.hide_viewport)
                                depsgraph = bpy.context.evaluated_depsgraph_get()
                                proxy_utils = None
                                rig_should_apply = False
                                rig_paths = None
                                rig_metadata = None
                                rig_rest_state = None
                                original_3dgs_state = None
                                if rig_baked_update_mode != "None":
                                    proxy_utils = load_proxy_binding_utils()
                                    if rig_baked_update_mode == "Enabled Baked":
                                        rig_should_apply = bool(source_obj.get(RIG_BAKED_ENABLED_PROP_NAME, False))
                                    else:
                                        rig_should_apply = True
                                    if rig_should_apply:
                                        try:
                                            if not proxy_utils.check_mesh_has_gaussian_attributes(source_obj):
                                                raise proxy_utils.ProxyBindingError(
                                                    f"'{source_obj.name}' does not look like a valid mesh 3DGS object."
                                                )
                                            original_3dgs_state = proxy_utils.read_logical_gaussian_state(source_obj)
                                            rig_paths, rig_metadata, rig_rest_state, _ = proxy_utils.load_binding_package(source_obj)
                                            proxy_utils.validate_current_3dgs_object(source_obj, rig_metadata)
                                            used_baked_rig_updates = True
                                            print(f"Baked rig package found for '{source_obj.name}'.")
                                        except Exception as exc:
                                            used_baked_rig_updates = False
                                            rig_should_apply = False
                                            print(f"Rig baked updates disabled for '{source_obj.name}': {exc}")
                                            if raise_on_error:
                                                raise
                                    else:
                                        print(f"Rig baked updates not enabled for '{source_obj.name}'.")
                                try:
                                    if original_hide_viewport:
                                        source_obj.hide_viewport = False
                                    for frame_number in frame_numbers:
                                        scene.frame_set(frame_number)
                                        processed_frame_count += 1
                                        if rig_should_apply:
                                            bake_path = proxy_utils.bake_state_file_path(rig_paths["bake_dir"], frame_number)
                                            if os.path.exists(bake_path):
                                                state = proxy_utils.load_baked_state(rig_paths["bake_dir"], frame_number, rig_rest_state)
                                                proxy_utils.apply_bound_state(source_obj, state)
                                                rig_applied_frame_count += 1
                                            else:
                                                rig_missing_frame_count += 1
                                                if missing_baked_frame_mode == "Skip Frame":
                                                    skipped_frame_count += 1
                                                    print(
                                                        f"Skipping frame {frame_number}: no baked rig frame exists for '{source_obj.name}'."
                                                    )
                                                    continue
                                                if missing_baked_frame_mode == "Restore Rest":
                                                    proxy_utils.apply_bound_state(source_obj, rig_rest_state)
                                                    print(
                                                        f"Restored rest rig state for frame {frame_number} on '{source_obj.name}'."
                                                    )
                                                elif missing_baked_frame_mode == "Error":
                                                    raise proxy_utils.ProxyBindingError(
                                                        f"No baked rig frame exists for frame {frame_number} on '{source_obj.name}'."
                                                    )
                                                else:
                                                    print(
                                                        f"Keeping current rig state for frame {frame_number}: no baked rig frame exists "
                                                        f"for '{source_obj.name}'."
                                                    )
                                        bpy.context.view_layer.update()
                                        new_obj = duplicate_evaluated_mesh(source_obj, collection, depsgraph, frame_number)
                                        output_object_list.append(new_obj)
                                        generated_count += 1
                                    success = failed_frame_count == 0
                                    status_message = (
                                        f"Generated {generated_count} duplicate object(s) from '{source_obj.name}'. "
                                        f"Rig-applied frames: {rig_applied_frame_count}. "
                                        f"Skipped frames: {skipped_frame_count}. Missing baked frames: {rig_missing_frame_count}."
                                    )
                                    print(status_message)
                                finally:
                                    if original_3dgs_state is not None:
                                        try:
                                            proxy_utils.write_logical_gaussian_state(source_obj, original_3dgs_state)
                                        except Exception as restore_exc:
                                            print(f"Warning: failed to restore original 3DGS state on '{source_obj.name}': {restore_exc}")
                                    scene.frame_set(original_frame)
                                    source_obj.hide_viewport = original_hide_viewport
                                    bpy.context.view_layer.update()
                            except Exception as exc:
                                status_message = f"Export duplicate-per-frame failed: {exc}"
                                failed_frame_count = max(failed_frame_count, 1)
                                print(status_message)
                                if raise_on_error:
                                    raise
                            for i_4588B in range(len(output_object_list)):
                                input_object = output_object_list[i_4588B]
                                # --- Input Variables (For testing or Serpens integration) ---
                                #input_object = bpy.context.object  # The target object
                                deselect_all_first = True          # Clear selection before starting?
                                make_active = True                 # NEW: Toggle between just selecting or selecting + activating
                                # --- Output Variables ---
                                success = False
                                error_message = ""

                                def safe_deselect_all():
                                    try:
                                        view_layer = bpy.context.view_layer
                                        for obj in bpy.context.selected_objects[:]:
                                            if obj.name in view_layer.objects:
                                                obj.select_set(False)
                                        # Only clear active if we actually want to reset everything
                                        if view_layer.objects.active:
                                            view_layer.objects.active = None
                                        return True, ""
                                    except Exception as e:
                                        return False, f"Deselect error: {str(e)}"

                                def select_object_logic(obj, should_activate):
                                    if not obj:
                                        return False, "No object provided"
                                    try:
                                        view_layer = bpy.context.view_layer
                                        if obj.name not in view_layer.objects:
                                            return False, f"Object '{obj.name}' not in current view layer"
                                        # 1. Unhide Object
                                        if obj.hide_viewport:
                                            obj.hide_viewport = False
                                        view_layer_obj = view_layer.objects[obj.name]
                                        if view_layer_obj.hide_get():
                                            view_layer_obj.hide_set(False)
                                        # 2. Unhide Direct Parent Collections
                                        for col in obj.users_collection:
                                            if col.hide_viewport:
                                                col.hide_viewport = False
                                        # 3. Select 
                                        view_layer_obj.select_set(True)
                                        # 4. Conditionally Activate
                                        if should_activate:
                                            view_layer.objects.active = view_layer_obj
                                            msg = f"Selected and activated {obj.name}"
                                        else:
                                            msg = f"Selected {obj.name} (Active object remains {view_layer.objects.active})"
                                        return True, msg
                                    except Exception as e:
                                        return False, f"Selection error: {str(e)}"
                                # --- Execution Logic ---
                                # 1. Handle Deselection
                                if deselect_all_first:
                                    success, error_message = safe_deselect_all()
                                else:
                                    success = True # Skip deselect, proceed to selection
                                # 2. Handle Selection
                                if success:
                                    if input_object:
                                        success, error_message = select_object_logic(input_object, make_active)
                                    else:
                                        success = False
                                        error_message = "No input object provided"
                                print(f"Result -> Success: {success}, Message: {error_message}")
                                bpy.ops.wm.ply_export(filepath=os.path.join(bpy.context.scene.sna_dgs_scene_properties.export_output_path,dgs_render__export['sna_export_base_object'].name + '_frame_000' + str(int(bpy.context.scene.frame_start + i_4588B)) + '.ply'), export_selected_objects=True, export_attributes=True)
                            for i_C1E70 in range(len(output_object_list)):
                                bpy.data.objects.remove(object=output_object_list[i_C1E70], do_unlink=True, do_id_user=True, do_ui_user=True, )
                        else:
                            pass
                        bpy.context.view_layer.objects.active = dgs_render__export['sna_export_base_object']
                        dgs_render__export['sna_export_base_object'].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = False
                        dgs_render__export['sna_export_base_object'].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = False
                        if (property_exists("dgs_render__export['sna_export_base_object'].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in dgs_render__export['sna_export_base_object'].modifiers):
                            dgs_render__export['sna_export_base_object'].sna_dgs_object_properties.update_mode = 'Enable Camera Updates'
                    else:
                        self.report({'ERROR'}, message='Object is missing the KIRI_3DGS_Write F_DC_And_Merge Modifier')
        else:
            self.report({'ERROR'}, message='Output Directory is not valid')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        if (bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == '4DGS'):
            box_5A7F8 = layout.box()
            box_5A7F8.alert = False
            box_5A7F8.enabled = True
            box_5A7F8.active = True
            box_5A7F8.use_property_split = False
            box_5A7F8.use_property_decorate = False
            box_5A7F8.alignment = 'Expand'.upper()
            box_5A7F8.scale_x = 1.0
            box_5A7F8.scale_y = 1.0
            if not True: box_5A7F8.operator_context = "EXEC_DEFAULT"
            box_5A7F8.label(text='Exporting large scans as .PLY sequences is not recommended,', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            box_5A7F8.label(text='        it can be best to export a cropped subset of points', icon_value=0)
            box_5A7F8.label(text='        Exporting large numbers of frames can take a while', icon_value=0)
        box_44942 = layout.box()
        box_44942.alert = False
        box_44942.enabled = True
        box_44942.active = True
        box_44942.use_property_split = False
        box_44942.use_property_decorate = False
        box_44942.alignment = 'Expand'.upper()
        box_44942.scale_x = 1.0
        box_44942.scale_y = 1.0
        if not True: box_44942.operator_context = "EXEC_DEFAULT"
        box_44942.label(text='Camera updates will be set to Disabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_44942.label(text='        Any enabled Animate modifiers found will be set to Displace Only', icon_value=0)
        box_44942.label(text='        3DGS Transforms will be applied to the input object', icon_value=0)
        box_44942.label(text='        The World Centre will be the exported model origin', icon_value=0)
        box_2A27F = layout.box()
        box_2A27F.alert = False
        box_2A27F.enabled = True
        box_2A27F.active = True
        box_2A27F.use_property_split = False
        box_2A27F.use_property_decorate = False
        box_2A27F.alignment = 'Expand'.upper()
        box_2A27F.scale_x = 1.0
        box_2A27F.scale_y = 1.0
        if not True: box_2A27F.operator_context = "EXEC_DEFAULT"
        box_2A27F.prop(self, 'sna_send_to_world_centre', text='Reset Position (Rig locked objects ignore this)', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)
