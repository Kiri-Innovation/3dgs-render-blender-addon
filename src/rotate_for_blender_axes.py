import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De(bpy.types.Operator):
    bl_idname = "sna.dgs_render_rotate_for_blender_axes_423de"
    bl_label = "3DGS Render: Rotate for Blender Axes"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        bpy.context.view_layer.objects.active.rotation_euler = (math.radians(-90.0), math.radians(0.0), math.radians(-90.0))
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
