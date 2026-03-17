import bpy
from .important import *

class SNA_OT_Dgs_Render_Remove_Decimate_Modifier_Fff1B(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_decimate_modifier_fff1b"
    bl_label = "3DGS Render: Remove Decimate Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
