import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Apply_Armature_Pose_As_Rest_Pose_A8C68(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_armature_pose_as_rest_pose_a8c68"
    bl_label = "3DGS Render: Apply armature pose as Rest Pose"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        """Bake an armature's current pose into the rest pose without losing animation.
        This script avoids direct F-Curve access so it stays resilient across Blender's
        legacy action system and Blender 5.x slotted actions.
        """
        import bpy
        # ---------------------------------------------------------------------------
        # Inputs
        # ---------------------------------------------------------------------------
        # Armature object to process. Leave blank to use the active armature, or the
        # first armature in the file if no active armature is available.
        ARMATURE_NAME = ""
        # Frame whose current pose should become the new rest pose.
        # Use None to keep the current frame's live visible pose, including unkeyed edits.
        APPLY_FRAME = None
        # Bake range source:
        # "ACTIVE_ACTION" uses the currently assigned action on the armature.
        # "SCENE" uses the full scene timeline.
        # "CUSTOM" uses FRAME_START and FRAME_END below.
        FRAME_RANGE_MODE = "ACTIVE_ACTION"
        # Custom bake range. These are only used when FRAME_RANGE_MODE = "CUSTOM".
        FRAME_START = None
        FRAME_END = None
        # If True, only selected pose bones are applied as rest pose. The bake still
        # rekeys every pose bone so downstream children stay visually stable.
        USE_SELECTED_BONES_ONLY = False
        # If True, also rebake objects that visually depend on this armature, such as
        # children, bone-parented props, constraint-driven child objects, and meshes
        # deformed by this armature.
        BAKE_DEPENDENT_OBJECTS = True
        # Bake into a fresh action by default so the original action asset is preserved.
        CREATE_NEW_ACTION = True
        NEW_ACTION_NAME = ""
        NEW_ACTION_SUFFIX = "_rest_pose_baked"
        # Disable NLA evaluation after the bake so the result is driven only by the
        # baked action. Turn this off if you intentionally want to keep NLA mixing live.
        DISABLE_NLA_AFTER_BAKE = True
        # Re-applying cached matrices more than once can help some dependency chains
        # settle after the new rest pose is applied.
        MATRIX_APPLY_PASSES = 2
        # Re-applying dependent object world matrices can help parented object chains
        # settle after the armature pose has been restored for the current frame.
        OBJECT_MATRIX_APPLY_PASSES = 1
        # Enable verbose console logging.
        DEBUG_LOG = True
        # ---------------------------------------------------------------------------
        # Outputs
        # ---------------------------------------------------------------------------
        OUT_SUCCESS = False
        OUT_MESSAGE = ""
        OUT_ARMATURE_NAME = ""
        OUT_ACTION_NAME = ""
        OUT_FRAME_START = 0
        OUT_FRAME_END = 0
        OUT_BONE_COUNT = 0
        OUT_FRAME_COUNT = 0
        OUT_DEPENDENT_OBJECT_COUNT = 0
        OUT_DEFORMED_MESH_COUNT = 0
        OUT_FRAME_RANGE_SOURCE = ""

        def log(message):
            if DEBUG_LOG:
                print(f"[rest-pose-bake] {message}")

        def _resolve_armature(context, armature_name):
            if armature_name:
                armature_obj = bpy.data.objects.get(armature_name)
                if armature_obj is None:
                    raise ValueError(f'Armature "{armature_name}" was not found.')
                if armature_obj.type != "ARMATURE":
                    raise ValueError(f'Object "{armature_name}" is not an armature.')
                return armature_obj
            active_object = context.view_layer.objects.active
            if active_object and active_object.type == "ARMATURE":
                return active_object
            for obj in bpy.data.objects:
                if obj.type == "ARMATURE":
                    return obj
            raise ValueError("No armature object was found in the current file.")

        def _resolve_action_frame_range(armature_obj):
            anim_data = armature_obj.animation_data
            if anim_data is None or anim_data.action is None:
                return None
            action = anim_data.action
            for attr_name in ("curve_frame_range", "frame_range"):
                try:
                    action_range = getattr(action, attr_name)
                except Exception:
                    continue
                if action_range is None or len(action_range) < 2:
                    continue
                try:
                    frame_start = float(action_range[0])
                    frame_end = float(action_range[1])
                except Exception:
                    continue
                if not math.isfinite(frame_start) or not math.isfinite(frame_end):
                    continue
                frame_start = int(math.floor(frame_start))
                frame_end = int(math.ceil(frame_end))
                if frame_end < frame_start:
                    continue
                return frame_start, frame_end
            return None

        def _resolve_frame_range(scene, armature_obj):
            range_mode = str(FRAME_RANGE_MODE).strip().upper()
            if range_mode == "CUSTOM":
                if FRAME_START is None or FRAME_END is None:
                    raise ValueError(
                        'FRAME_RANGE_MODE is "CUSTOM", but FRAME_START/FRAME_END are not both set.'
                    )
                frame_start = int(FRAME_START)
                frame_end = int(FRAME_END)
                range_source = "CUSTOM"
            elif range_mode == "SCENE":
                frame_start = int(scene.frame_start)
                frame_end = int(scene.frame_end)
                range_source = "SCENE"
            elif range_mode == "ACTIVE_ACTION":
                action_range = _resolve_action_frame_range(armature_obj)
                if action_range is None:
                    frame_start = int(scene.frame_start)
                    frame_end = int(scene.frame_end)
                    range_source = "SCENE_FALLBACK"
                    log(
                        "No usable active action frame range was found; "
                        "falling back to the scene timeline."
                    )
                else:
                    frame_start, frame_end = action_range
                    range_source = "ACTIVE_ACTION"
            else:
                raise ValueError(
                    f'Unsupported FRAME_RANGE_MODE "{FRAME_RANGE_MODE}". '
                    'Use "ACTIVE_ACTION", "SCENE", or "CUSTOM".'
                )
            if frame_end < frame_start:
                raise ValueError(
                    f"Invalid frame range: start={frame_start}, end={frame_end}."
                )
            return frame_start, frame_end, range_source

        def _resolve_apply_frame(scene):
            return int(scene.frame_current if APPLY_FRAME is None else APPLY_FRAME)

        def _bone_depth(pose_bone):
            depth = 0
            current = pose_bone.parent
            while current is not None:
                depth += 1
                current = current.parent
            return depth

        def _ordered_pose_bones(armature_obj):
            return sorted(armature_obj.pose.bones, key=lambda bone: (_bone_depth(bone), bone.name))

        def _rotation_data_path(rotation_mode):
            if rotation_mode == "QUATERNION":
                return "rotation_quaternion"
            if rotation_mode == "AXIS_ANGLE":
                return "rotation_axis_angle"
            return "rotation_euler"

        def _set_active_armature(context, armature_obj):
            view_layer = context.view_layer
            try:
                for obj in view_layer.objects:
                    obj.select_set(False)
            except Exception:
                pass
            armature_obj.select_set(True)
            view_layer.objects.active = armature_obj

        def _enter_pose_mode(context, armature_obj):
            _set_active_armature(context, armature_obj)
            if armature_obj.mode != "POSE":
                bpy.ops.object.mode_set(mode="POSE")

        def _selected_pose_bone_names(context, armature_obj):
            _enter_pose_mode(context, armature_obj)
            selected_pose_bones = getattr(
                context, "selected_pose_bones_from_active_object", None
            )
            if selected_pose_bones is None:
                selected_pose_bones = getattr(context, "selected_pose_bones", None)
            if selected_pose_bones is not None:
                return [pose_bone.name for pose_bone in selected_pose_bones]
            selected_names = []
            for pose_bone in armature_obj.pose.bones:
                select_flag = getattr(pose_bone.bone, "select", None)
                if select_flag:
                    selected_names.append(pose_bone.name)
            return selected_names

        def _capture_visual_pose_matrices(context, armature_obj, ordered_bone_names):
            depsgraph = context.evaluated_depsgraph_get()
            context.view_layer.update()
            evaluated_obj = armature_obj.evaluated_get(depsgraph)
            return {
                bone_name: evaluated_obj.pose.bones[bone_name].matrix.copy()
                for bone_name in ordered_bone_names
            }

        def _cache_visual_matrices(
            context,
            armature_obj,
            ordered_bone_names,
            frame_start,
            frame_end,
            frame_overrides=None,
        ):
            scene = context.scene
            depsgraph = context.evaluated_depsgraph_get()
            cached_matrices = {}
            for frame in range(frame_start, frame_end + 1):
                if frame_overrides and frame in frame_overrides:
                    cached_matrices[frame] = {
                        bone_name: frame_overrides[frame][bone_name].copy()
                        for bone_name in ordered_bone_names
                    }
                    continue
                scene.frame_set(frame)
                context.view_layer.update()
                evaluated_obj = armature_obj.evaluated_get(depsgraph)
                cached_matrices[frame] = {
                    bone_name: evaluated_obj.pose.bones[bone_name].matrix.copy()
                    for bone_name in ordered_bone_names
                }
            return cached_matrices

        def _object_depth(obj):
            depth = 0
            current = obj.parent
            while current is not None:
                depth += 1
                current = current.parent
            return depth

        def _descends_from_object(obj, ancestor_obj):
            current = obj.parent
            while current is not None:
                if current == ancestor_obj:
                    return True
                current = current.parent
            return False

        def _uses_armature_constraints(obj, armature_obj):
            for constraint in obj.constraints:
                if getattr(constraint, "target", None) == armature_obj:
                    return True
            return False

        def _armature_modifiers_for_object(obj, armature_obj):
            matching_modifiers = []
            for modifier in obj.modifiers:
                if modifier.type != "ARMATURE":
                    continue
                if getattr(modifier, "object", None) == armature_obj:
                    matching_modifiers.append(modifier)
            return matching_modifiers

        def _collect_dependent_objects(armature_obj):
            transform_dependents = []

            deformed_meshes = []
            for obj in bpy.data.objects:
                if obj == armature_obj:
                    continue
                has_armature_modifier = bool(_armature_modifiers_for_object(obj, armature_obj))
                if has_armature_modifier:

                    deformed_meshes.append(obj)
                if _descends_from_object(obj, armature_obj) or _uses_armature_constraints(
                    obj, armature_obj
                ):
                    if not has_armature_modifier:
                        transform_dependents.append(obj)
            transform_dependents = sorted(
                transform_dependents,
                key=lambda obj: (_object_depth(obj), obj.name),
            )

            deformed_meshes = sorted(

                deformed_meshes,
                key=lambda obj: (_object_depth(obj), obj.name),
            )
            return transform_dependents, deformed_meshes

        def _capture_object_world_matrices(context, objects):
            depsgraph = context.evaluated_depsgraph_get()
            context.view_layer.update()
            cached_matrices = {}
            for obj in objects:
                evaluated_obj = obj.evaluated_get(depsgraph)
                cached_matrices[obj.name] = evaluated_obj.matrix_world.copy()
            return cached_matrices

        def _cache_object_world_matrices(
            context,
            objects,
            frame_start,
            frame_end,
            frame_overrides=None,
        ):
            if not objects:
                return {}
            scene = context.scene
            depsgraph = context.evaluated_depsgraph_get()
            cached_matrices = {}
            for frame in range(frame_start, frame_end + 1):
                if frame_overrides and frame in frame_overrides:
                    cached_matrices[frame] = {
                        obj_name: frame_overrides[frame][obj_name].copy()
                        for obj_name in frame_overrides[frame]
                    }
                    continue
                scene.frame_set(frame)
                context.view_layer.update()
                cached_matrices[frame] = {}
                for obj in objects:
                    evaluated_obj = obj.evaluated_get(depsgraph)
                    cached_matrices[frame][obj.name] = evaluated_obj.matrix_world.copy()
            return cached_matrices

        def _ensure_single_user_mesh_data(obj):
            if obj.type != "MESH":
                raise ValueError(f'Object "{obj.name}" is not a mesh.')
            if obj.data.users > 1:
                obj.data = obj.data.copy()

        def _capture_deformed_mesh_data(context, mesh_objects):
            depsgraph = context.evaluated_depsgraph_get()
            mesh_snapshots = {}
            for obj in mesh_objects:
                if obj.type != "MESH":
                    continue
                if obj.data.shape_keys and len(obj.data.shape_keys.key_blocks) > 1:
                    raise ValueError(
                        f'Mesh "{obj.name}" has shape keys; this script does not yet '
                        "support rewriting armature-driven mesh basis data with shape keys present."
                    )
                evaluated_obj = obj.evaluated_get(depsgraph)
                temp_mesh = evaluated_obj.to_mesh()
                try:
                    if len(temp_mesh.vertices) != len(obj.data.vertices):
                        raise ValueError(
                            f'Mesh "{obj.name}" changes topology during evaluation, so its '
                            "basis mesh cannot be rewritten safely."
                        )
                    mesh_snapshots[obj.name] = [vertex.co.copy() for vertex in temp_mesh.vertices]
                finally:
                    evaluated_obj.to_mesh_clear()
            return mesh_snapshots

        def _apply_deformed_mesh_data(mesh_objects, mesh_snapshots):
            for obj in mesh_objects:
                if obj.name not in mesh_snapshots:
                    continue
                _ensure_single_user_mesh_data(obj)
                vertex_positions = mesh_snapshots[obj.name]
                for index, vertex in enumerate(obj.data.vertices):
                    vertex.co = vertex_positions[index]
                obj.data.update()

        def _create_baked_action(anim_owner, custom_name=""):
            if anim_owner.animation_data is None:
                anim_owner.animation_data_create()
            original_action = anim_owner.animation_data.action
            if not CREATE_NEW_ACTION and original_action is not None:
                return original_action
            if custom_name:
                action_name = custom_name
            elif original_action is not None:
                action_name = f"{original_action.name}{NEW_ACTION_SUFFIX}"
            else:
                action_name = f"{anim_owner.name}{NEW_ACTION_SUFFIX}"
            baked_action = bpy.data.actions.new(action_name)
            anim_owner.animation_data.action = baked_action
            return baked_action

        def _keyframe_transform_owner(
            transform_owner,
            frame,
            group_name=None,
            use_visual_keying=True,
        ):
            key_kwargs = {
                "frame": frame,
            }
            if group_name is not None:
                key_kwargs["group"] = group_name
            if use_visual_keying:
                key_kwargs["options"] = {"INSERTKEY_VISUAL"}
            transform_owner.keyframe_insert(
                data_path="location",
                **key_kwargs,
            )
            transform_owner.keyframe_insert(
                data_path="scale",
                **key_kwargs,
            )
            transform_owner.keyframe_insert(
                data_path=_rotation_data_path(transform_owner.rotation_mode),
                **key_kwargs,
            )

        def _apply_cached_frame(context, armature_obj, ordered_bone_names, frame_cache):
            for _ in range(max(1, int(MATRIX_APPLY_PASSES))):
                for bone_name in ordered_bone_names:
                    pose_bone = armature_obj.pose.bones[bone_name]
                    target_pose_matrix = frame_cache[bone_name]
                    if pose_bone.parent is None:
                        local_pose_matrix = pose_bone.bone.convert_local_to_pose(
                            target_pose_matrix,
                            pose_bone.bone.matrix_local,
                            invert=True,
                        )
                    else:
                        local_pose_matrix = pose_bone.bone.convert_local_to_pose(
                            target_pose_matrix,
                            pose_bone.bone.matrix_local,
                            parent_matrix=frame_cache[pose_bone.parent.name],
                            parent_matrix_local=pose_bone.parent.bone.matrix_local,
                            invert=True,
                        )
                    pose_bone.matrix_basis = local_pose_matrix
                context.view_layer.update()

        def _apply_dependent_object_matrices(context, dependent_objects, frame_cache):
            for _ in range(max(1, int(OBJECT_MATRIX_APPLY_PASSES))):
                for obj in dependent_objects:
                    obj.matrix_world = frame_cache[obj.name]
                context.view_layer.update()
        # Serpens often executes script bodies through exec()-style contexts instead of
        # running them as __main__, so the primary execution path lives at top level.
        RESULT = {}
        try:
            context = bpy.context
            scene = context.scene
            original_frame = scene.frame_current
            armature_obj = _resolve_armature(context, ARMATURE_NAME)
            if armature_obj.library is not None:
                raise ValueError(
                    f'Armature "{armature_obj.name}" is linked from a library and is not editable.'
                )
            frame_start, frame_end, frame_range_source = _resolve_frame_range(
                scene,
                armature_obj,
            )
            apply_frame = _resolve_apply_frame(scene)
            ordered_bone_names = [
                pose_bone.name for pose_bone in _ordered_pose_bones(armature_obj)
            ]
            transform_dependent_objects = []

            deformed_mesh_objects = []
            if BAKE_DEPENDENT_OBJECTS:
                (
                    transform_dependent_objects,

                    deformed_mesh_objects,
                ) = _collect_dependent_objects(armature_obj)
            selected_bone_names = _selected_pose_bone_names(context, armature_obj)
            if USE_SELECTED_BONES_ONLY and not selected_bone_names:
                raise ValueError(
                    "USE_SELECTED_BONES_ONLY is enabled, but no pose bones are selected."
                )
            original_use_nla = False
            if armature_obj.animation_data is not None:
                original_use_nla = bool(getattr(armature_obj.animation_data, "use_nla", False))
            current_pose_override = None
            pose_frame_overrides = None
            current_object_override = None
            object_frame_overrides = None
            if APPLY_FRAME is None:
                current_pose_override = _capture_visual_pose_matrices(
                    context,
                    armature_obj,
                    ordered_bone_names,
                )
                if frame_start <= original_frame <= frame_end:
                    pose_frame_overrides = {original_frame: current_pose_override}
                if transform_dependent_objects:
                    current_object_override = _capture_object_world_matrices(
                        context,
                        transform_dependent_objects,
                    )
                    if frame_start <= original_frame <= frame_end:
                        object_frame_overrides = {original_frame: current_object_override}
            cached_matrices = _cache_visual_matrices(
                context,
                armature_obj,
                ordered_bone_names,
                frame_start,
                frame_end,
                frame_overrides=pose_frame_overrides,
            )
            cached_object_matrices = _cache_object_world_matrices(
                context,
                transform_dependent_objects,
                frame_start,
                frame_end,
                frame_overrides=object_frame_overrides,
            )
            log(
                f'Caching complete for "{armature_obj.name}" across '
                f"{frame_start}-{frame_end} ({len(ordered_bone_names)} bones)."
            )
            _enter_pose_mode(context, armature_obj)
            scene.frame_set(apply_frame)
            context.view_layer.update()
            if current_pose_override is not None:
                _apply_cached_frame(
                    context,
                    armature_obj,
                    ordered_bone_names,
                    current_pose_override,
                )
            if deformed_mesh_objects:

                deformed_mesh_snapshots = _capture_deformed_mesh_data(
                    context,

                    deformed_mesh_objects,
                )
                _apply_deformed_mesh_data(deformed_mesh_objects, deformed_mesh_snapshots)
                context.view_layer.update()
            log(f"Applying current pose as rest pose on frame {apply_frame}.")
            bpy.ops.pose.armature_apply(selected=USE_SELECTED_BONES_ONLY)
            baked_action = _create_baked_action(armature_obj, custom_name=NEW_ACTION_NAME)
            if DISABLE_NLA_AFTER_BAKE and armature_obj.animation_data is not None:
                try:
                    armature_obj.animation_data.use_nla = False
                except Exception:
                    pass
            for dependent_obj in transform_dependent_objects:
                _create_baked_action(dependent_obj)
                if DISABLE_NLA_AFTER_BAKE and dependent_obj.animation_data is not None:
                    try:
                        dependent_obj.animation_data.use_nla = False
                    except Exception:
                        pass
            for frame in range(frame_start, frame_end + 1):
                scene.frame_set(frame)
                context.view_layer.update()
                _apply_cached_frame(
                    context,
                    armature_obj,
                    ordered_bone_names,
                    cached_matrices[frame],
                )
                for bone_name in ordered_bone_names:
                    _keyframe_transform_owner(
                        armature_obj.pose.bones[bone_name],
                        frame,
                        group_name=bone_name,
                        use_visual_keying=True,
                    )
                if transform_dependent_objects:
                    _apply_dependent_object_matrices(
                        context,
                        transform_dependent_objects,
                        cached_object_matrices[frame],
                    )
                    for dependent_obj in transform_dependent_objects:
                        _keyframe_transform_owner(
                            dependent_obj,
                            frame,
                            use_visual_keying=False,
                        )
            scene.frame_set(original_frame)
            context.view_layer.update()
            _enter_pose_mode(context, armature_obj)
            RESULT = {
                "success": True,
                "message": (
                    f'Applied a new rest pose to "{armature_obj.name}" and baked '
                    f"{frame_end - frame_start + 1} frames into action "
                    f'"{baked_action.name}".'
                ),
                "armature_name": armature_obj.name,
                "action_name": baked_action.name,
                "frame_start": frame_start,
                "frame_end": frame_end,
                "bone_count": len(ordered_bone_names),
                "frame_count": frame_end - frame_start + 1,
                "dependent_object_count": len(transform_dependent_objects),
                "deformed_mesh_count": len(deformed_mesh_objects),
                "frame_range_source": frame_range_source,
                "selected_bones_were_used": USE_SELECTED_BONES_ONLY,
                "selected_bone_count": len(selected_bone_names),
                "original_use_nla": original_use_nla,
            }
            OUT_SUCCESS = bool(RESULT["success"])
            OUT_MESSAGE = RESULT["message"]
            OUT_ARMATURE_NAME = RESULT["armature_name"]
            OUT_ACTION_NAME = RESULT["action_name"]
            OUT_FRAME_START = int(RESULT["frame_start"])
            OUT_FRAME_END = int(RESULT["frame_end"])
            OUT_BONE_COUNT = int(RESULT["bone_count"])
            OUT_FRAME_COUNT = int(RESULT["frame_count"])
            OUT_DEPENDENT_OBJECT_COUNT = int(RESULT["dependent_object_count"])
            OUT_DEFORMED_MESH_COUNT = int(RESULT["deformed_mesh_count"])
            OUT_FRAME_RANGE_SOURCE = RESULT["frame_range_source"]
            log(RESULT["message"])
        except Exception as exc:
            OUT_SUCCESS = False
            OUT_MESSAGE = f"{type(exc).__name__}: {exc}"
            OUT_ARMATURE_NAME = ""
            OUT_ACTION_NAME = ""
            OUT_FRAME_START = 0
            OUT_FRAME_END = 0
            OUT_BONE_COUNT = 0
            OUT_FRAME_COUNT = 0
            OUT_DEPENDENT_OBJECT_COUNT = 0
            OUT_DEFORMED_MESH_COUNT = 0
            OUT_FRAME_RANGE_SOURCE = ""
            RESULT = {
                "success": False,
                "message": OUT_MESSAGE,
            }
            log(f"ERROR: {OUT_MESSAGE}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
