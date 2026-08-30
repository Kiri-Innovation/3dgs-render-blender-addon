import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .clean_up_scene_5f1f1 import sna_clean_up_scene_5F1F1

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Clean_Up_Scene_80052(bpy.types.Operator):
    bl_idname = "sna.dgs_render_clean_up_scene_80052"
    bl_label = "3DGS Render: Clean Up Scene"
    bl_description = "Stop advanced rendering and optionally delete all proxy empties."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        sna_clean_up_scene_5F1F1(bpy.context.scene.sna_dgs_scene_properties.r2_clear_empties)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
