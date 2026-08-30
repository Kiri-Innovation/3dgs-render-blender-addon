import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .align_active_values_to_y import sna_align_active_values_to_y_E5E9E

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Align_Active_To_Y_Axis_C305D(bpy.types.Operator):
    bl_idname = "sna.dgs_render_align_active_to_y_axis_c305d"
    bl_label = "3DGS Render: Align Active To Y Axis"
    bl_description = "Updates the 3DGS_Render modifier once to the Y axis for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        sna_align_active_values_to_y_E5E9E()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
