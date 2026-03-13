import bpy
from .important import *

class SNA_OT_Dgs_Render_Remove_Remove_By_Size_Modifier_3A0E5(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_remove_by_size_modifier_3a0e5"
    bl_label = "3DGS Render: Remove Remove By Size Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
