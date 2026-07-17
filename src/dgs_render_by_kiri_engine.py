import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .about_kiri_links_docs_3dgs import sna_about_kiri_links_docs_3dgs_D02EC
from .dgs_render_main_function_menu import sna_dgs_render__main_function_menu_019C7

__package__ = __package__.rsplit('.', 1)[0]


class SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_E1A83(bpy.types.Panel):
    bl_label = '3DGS Render by KIRI Engine'
    bl_idname = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_E1A83'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = '3DGS Render'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine icon.svg')), scale=1.0)

    def draw(self, context):
        layout = self.layout
        layout_function = layout
        sna_dgs_render__main_function_menu_019C7(layout_function, )
        layout_function = layout
        sna_about_kiri_links_docs_3dgs_D02EC(layout_function, )
