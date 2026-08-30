import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .relight2_4_restore_original_3dgs_color import sna_relight2_4_restore_original_3dgs_color_08334
from .relight_5_create_col_and_vertex_paint import sna_relight_5__create_col_and_vertex_paint_2AE5F

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Restore_Original_Light_9A7Fe(bpy.types.Operator):
    bl_idname = "sna.dgs_render_restore_original_light_9a7fe"
    bl_label = "3DGS Render: Restore Original Light"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        sna_relight2_4_restore_original_3dgs_color_08334()
        sna_relight_5__create_col_and_vertex_paint_2AE5F()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
