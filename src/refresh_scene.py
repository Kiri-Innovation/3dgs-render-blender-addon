import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .r2_viewport_update import sna_r2_viewport_update_BA246

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Refresh_Scene_A6719(bpy.types.Operator):
    bl_idname = "sna.dgs_render_refresh_scene_a6719"
    bl_label = "3DGS Render: Refresh Scene"
    bl_description = "Redraw any 3DGS proxy objects in the scene."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        exec('import os')
        if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Single'):
            pass
        else:
            bpy.context.scene.frame_current = bpy.context.scene.frame_start
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop = (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Single')

        def delayed_06D54():
            sna_r2_viewport_update_BA246()
            if bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop:
                return None
            return bpy.context.scene.sna_dgs_scene_properties.r2_interval
        bpy.app.timers.register(delayed_06D54, first_interval=0.0)
        sna_r2_viewport_update_BA246()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
