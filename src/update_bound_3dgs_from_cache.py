import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .rig_5_apply_baked_cache import sna_rig_5_apply_baked_cache_5656F

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Update_Bound_3Dgs_From_Cache_385Ec(bpy.types.Operator):
    bl_idname = "sna.dgs_render_update_bound_3dgs_from_cache_385ec"
    bl_label = "3DGS Render: Update Bound 3DGS from cache"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.sna_dgs_scene_properties.rig_interval_stop = False

        def delayed_DBD03():
            sna_rig_5_apply_baked_cache_5656F('Active', None)
            if bpy.context.scene.sna_dgs_scene_properties.rig_interval_stop:
                return None
            return bpy.context.scene.sna_dgs_scene_properties.rig_update_interval
        bpy.app.timers.register(delayed_DBD03, first_interval=0.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
