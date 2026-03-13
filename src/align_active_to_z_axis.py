import bpy

class SNA_OT_Dgs_Render_Align_Active_To_Z_Axis_1E184(bpy.types.Operator):
    bl_idname = "sna.dgs_render_align_active_to_z_axis_1e184"
    bl_label = "3DGS Render: Align Active To Z Axis"
    bl_description = "Updates the 3DGS_Render modifier once to the Z axis for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_align_active_values_to_z_7B9ED()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
