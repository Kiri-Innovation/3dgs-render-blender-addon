import math
import bpy

class SNA_OT_Dgs_Render_Align_Active_To_View_30B13(bpy.types.Operator):
    bl_idname = "sna.dgs_render_align_active_to_view_30b13"
    bl_label = "3DGS Render: Align Active To View"
    bl_description = "Updates the 3DGS_Render modifier once to the current view for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        ObjectName = bpy.context.view_layer.objects.active.name
        from mathutils import Matrix
        # Define helper function for updating the geometry node sockets

        def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
            geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
            if not geometryNodes_modifier:
                print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                return False
            # Update view matrix
            geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
            geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
            geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
            geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
            geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
            geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
            geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
            geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
            geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
            geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
            geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
            geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
            geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
            geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
            geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
            geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
            # Update projection matrix
            geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
            geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
            geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
            geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
            geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
            geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
            geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
            geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
            geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
            geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
            geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
            geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
            geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
            geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
            geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
            geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
            # Update window dimensions
            geometryNodes_modifier['Socket_34'] = window_width
            geometryNodes_modifier['Socket_35'] = window_height
            return True
        # Main code for updating specific object
        updated_objects = []
        # Find view and projection matrices from the 3D view area
        found_3d_view = False
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                view_matrix = area.spaces.active.region_3d.view_matrix
                proj_matrix = area.spaces.active.region_3d.window_matrix
                window_width = area.width
                window_height = area.height
                found_3d_view = True
                break
        if not found_3d_view:
            print("Error: No 3D View found to update camera information.")
        else:
            # Update only specific object
            target_object_name = ObjectName  # Serpens Variable
            obj = bpy.data.objects.get(target_object_name)
            if obj and obj.visible_get():
                print(f"Attempting to update object: {obj.name}")  # Debugging print
                if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                    updated_objects.append(obj.name)  # Add to updated list
        # Print or output the list of updated objects
        print("Updated objects:", updated_objects)
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
