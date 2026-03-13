import bpy
from .important import *

class SNA_OT_Dgs_Render_Stop_Interval_Updates_5Ac80(bpy.types.Operator):
    bl_idname = "sna.dgs_render_stop_interval_updates_5ac80"
    bl_label = "3DGS Render: Stop Interval Updates"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
