import bpy

class SNA_OT_Dgs_Render_Clean_Up_Advanced_Render_Scene_09450(bpy.types.Operator):
    bl_idname = "sna.dgs_render_clean_up_advanced_render_scene_09450"
    bl_label = "3DGS Render: Clean Up Advanced Render Scene"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_clean_up_scene_5F1F1(bpy.context.scene.sna_dgs_scene_properties.r2_clear_empties)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
