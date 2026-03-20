import bpy
from .important import *

class SNA_OT_Dgs_Render_Remove_Crop_Box_Modifier_64Ea6(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_crop_box_modifier_64ea6"
    bl_label = "3DGS Render: Remove Crop Box Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
