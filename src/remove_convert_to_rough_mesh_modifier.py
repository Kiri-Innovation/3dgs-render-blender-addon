import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper

class SNA_OT_Dgs_Render_Remove_Convert_To_Rough_Mesh_Modifier_A8C4C(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_convert_to_rough_mesh_modifier_a8c4c"
    bl_label = "3DGS Render: Remove Convert To Rough Mesh Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], )
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
