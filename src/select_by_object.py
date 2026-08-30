import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Select_By_Object_92F9C(bpy.types.Operator):
    bl_idname = "sna.dgs_render_select_by_object_92f9c"
    bl_label = "3DGS Render: Select by object"
    bl_description = "Select points based on a selection objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        SELECTION_OBJ = bpy.context.scene.sna_dgs_scene_properties.select_select_by_obj
        SELECT_MODE = bpy.context.scene.sna_dgs_scene_properties.select_obj_select_mode
        CLEAR_PREVIOUS = None
        import bmesh
        from mathutils.bvhtree import BVHTree
        # =========================================================================
        # 1. ROOT LEVEL DECLARATIONS (Module Level)
        # Serpens will inject your node socket values into these variables
        # =========================================================================
        TARGET_OBJ = bpy.context.active_object
        #SELECTION_OBJ = bpy.data.objects.get("Cube")
        #SELECT_MODE = "INSIDE"
        CLEAR_PREVIOUS = True
        # Declare global output variables at the module level [cite: 143]
        SCRIPT_SUCCESS = False
        SELECTED_COUNT = 0
        # =========================================================================
        # 2. MAIN FUNCTION (No global keyword used inside)
        # =========================================================================

        def execute_volumetric_selection():
            # We do NOT use 'global SCRIPT_SUCCESS' here[cite: 167].
            # Safety Checks: Return early instead of failing silently
            if not TARGET_OBJ or TARGET_OBJ.type != 'MESH':
                return False, 0
            if not SELECTION_OBJ or SELECTION_OBJ.type != 'MESH':
                return True, 0 # Passing safely so nodes don't freeze
            if SELECTION_OBJ.name not in bpy.context.view_layer.objects:
                return True, 0
            original_mode = 'OBJECT'
            if bpy.context.active_object:
                original_mode = bpy.context.active_object.mode
            if bpy.context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            try:
                # Build a BVH Tree for the Selection Volume
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm_sel = bmesh.new()
                bm_sel.from_object(SELECTION_OBJ, depsgraph)
                bm_sel.transform(SELECTION_OBJ.matrix_world) 
                bvh = BVHTree.FromBMesh(bm_sel)
                bm_sel.free()
                # Access the Target Mesh data
                bm_target = bmesh.new()
                bm_target.from_mesh(TARGET_OBJ.data)
                bm_target.transform(TARGET_OBJ.matrix_world) 
                bm_target.verts.ensure_lookup_table()
                if CLEAR_PREVIOUS:
                    for v in bm_target.verts:
                        v.select = False
                # Raycast Logic
                ray_dir = Vector((0.0, 0.0, 1.0)) 
                count = 0
                for v in bm_target.verts:
                    hits = 0
                    current_loc = v.co.copy()
                    while True:
                        location, normal, index, dist = bvh.ray_cast(current_loc, ray_dir)
                        if location is None:
                            break
                        hits += 1
                        current_loc = location + (ray_dir * 0.0001)
                    is_inside = (hits % 2 != 0)
                    if SELECT_MODE == "INSIDE" and is_inside:
                        v.select = True
                        count += 1
                    elif SELECT_MODE == "OUTSIDE" and not is_inside:
                        v.select = True
                        count += 1
                # Apply and Cleanup
                matrix_world_inv = TARGET_OBJ.matrix_world.inverted()
                bm_target.transform(matrix_world_inv)
                bm_target.to_mesh(TARGET_OBJ.data)
                bm_target.free()
                TARGET_OBJ.data.update() 
                if bpy.context.active_object and bpy.context.active_object.mode != original_mode:
                     bpy.ops.object.mode_set(mode=original_mode)
                # Return values from functions instead of setting globals inside 
                return True, count
            except Exception as e:
                print(f"Serpens Script Error: {e}")
                # Ensure we return to original mode even on failure
                if bpy.context.active_object and bpy.context.active_object.mode != original_mode:
                     bpy.ops.object.mode_set(mode=original_mode)
                return False, 0
        # =========================================================================
        # 3. EXECUTE AND CATCH
        # Execute main function [cite: 154]
        # =========================================================================
        result_success, result_count = execute_volumetric_selection()
        # =========================================================================
        # 4. MODULE LEVEL ASSIGNMENT
        # Set global variables at MODULE LEVEL for Serpens access [cite: 156]
        # =========================================================================
        SCRIPT_SUCCESS = result_success
        SELECTED_COUNT = result_count
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
