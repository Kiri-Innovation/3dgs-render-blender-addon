import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .rig2_update_single import sna_rig2_update_single_DC225
from .rig_5_apply_baked_cache import sna_rig_5_apply_baked_cache_5656F

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Update_Bound_3Dgs_From_Proxy_Mesh_951A0(bpy.types.Operator):
    bl_idname = "sna.dgs_render_update_bound_3dgs_from_proxy_mesh_951a0"
    bl_label = "3DGS Render: Update Bound 3DGS from Proxy Mesh"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
            if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                success_0_47472 = sna_rig_5_apply_baked_cache_5656F('Active', None)
                if success_0_47472:
                    pass
                else:
                    sna_rig2_update_single_DC225()
            else:
                sna_rig2_update_single_DC225()
        else:
            sna_rig2_update_single_DC225()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
