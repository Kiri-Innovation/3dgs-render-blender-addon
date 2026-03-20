import bpy

class SNA_OT_Dgs_Render_Update_Enabled_3Dgs_Objects_6D7F4(bpy.types.Operator):
    bl_idname = "sna.dgs_render_update_enabled_3dgs_objects_6d7f4"
    bl_label = "3DGS Render: Update Enabled 3DGS Objects"
    bl_description = "Updates all enabled 3DGS objects faces to the current view."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_update_camera_single_time_9EF18()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
