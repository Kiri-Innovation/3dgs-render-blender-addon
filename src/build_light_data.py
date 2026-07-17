import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .relight2_1_build_base_color_from_f_dc import sna_relight2_1_build_base_color_from_f_dc_BAE18
from .relight2_2_build_proxy_hdri_relight import sna_relight2_2_build_proxy_hdri_relight_89C9C

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Build_Light_Data_Ab375(bpy.types.Operator):
    bl_idname = "sna.dgs_render_build_light_data_ab375"
    bl_label = "3DGS Render: Build Light Data"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_relight2_1_build_base_color_from_f_dc_BAE18()
        sna_relight2_2_build_proxy_hdri_relight_89C9C()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
