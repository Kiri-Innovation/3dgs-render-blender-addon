import bpy
from .important import *
import math

class SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De(bpy.types.Operator):
    bl_idname = "sna.dgs_render_rotate_for_blender_axes_423de"
    bl_label = "3DGS Render: Rotate for Blender Axes"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.rotation_euler = (math.radians(-90.0), math.radians(0.0), math.radians(-90.0))
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

