import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper

class SNA_OT_Dgs_Render_Remove_Animate_Modifier_5B34D(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_animate_modifier_5b34d"
    bl_label = "3DGS Render: Remove Animate Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
