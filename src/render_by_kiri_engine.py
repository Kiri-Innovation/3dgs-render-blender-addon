import bpy
from .important import load_preview_icon 
from .sna_dgs_render_main_function_menu import *

class SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_A02CB(bpy.types.Panel):
    import os
    bl_label = '3DGS Render by KIRI Engine'
    bl_idname = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_A02CB'
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
        layout.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'kiriengine icon.svg')), scale=1.0)

    def draw(self, context):
        layout = self.layout
        layout_function = layout
        sna_dgs_render__main_function_menu_019C7(layout_function, )
        layout_function = layout
        sna_about_kiri_links_docs_3dgs_D02EC(layout_function, )


def sna_about_kiri_links_docs_3dgs_D02EC(layout_function, ):
    box_12166 = layout_function.box()
    box_12166.alert = False
    box_12166.enabled = True
    box_12166.active = True
    box_12166.use_property_split = False
    box_12166.use_property_decorate = False
    box_12166.alignment = 'Expand'.upper()
    box_12166.scale_x = 1.0
    box_12166.scale_y = 1.0
    if not True: box_12166.operator_context = "EXEC_DEFAULT"
    col_CB7BF = box_12166.column(heading='', align=True)
    col_CB7BF.alert = False
    col_CB7BF.enabled = True
    col_CB7BF.active = True
    col_CB7BF.use_property_split = False
    col_CB7BF.use_property_decorate = False
    col_CB7BF.scale_x = 1.0
    col_CB7BF.scale_y = 1.0
    col_CB7BF.alignment = 'Expand'.upper()
    col_CB7BF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_D36BE = col_CB7BF.box()
    box_D36BE.alert = False
    box_D36BE.enabled = True
    box_D36BE.active = True
    box_D36BE.use_property_split = False
    box_D36BE.use_property_decorate = False
    box_D36BE.alignment = 'Center'.upper()
    box_D36BE.scale_x = 1.0
    box_D36BE.scale_y = 1.0
    if not True: box_D36BE.operator_context = "EXEC_DEFAULT"
    box_D36BE.label(text='About KIRI Engine', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'pointer-right-fill.svg')))
    box_D36BE.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'Addon speel 2.png')), scale=10.0)
    op = box_D36BE.operator('sna.dgs_render_launch_kiri_site_bf973', text='Learn More', icon_value=0, emboss=True, depress=False)
    box_28D7F = col_CB7BF.box()
    box_28D7F.alert = False
    box_28D7F.enabled = True
    box_28D7F.active = True
    box_28D7F.use_property_split = False
    box_28D7F.use_property_decorate = True
    box_28D7F.alignment = 'Expand'.upper()
    box_28D7F.scale_x = 1.0
    box_28D7F.scale_y = 1.2000000476837158
    if not True: box_28D7F.operator_context = "EXEC_DEFAULT"
    split_F339F = box_28D7F.split(factor=0.30000001192092896, align=False)
    split_F339F.alert = False
    split_F339F.enabled = True
    split_F339F.active = True
    split_F339F.use_property_split = False
    split_F339F.use_property_decorate = False
    split_F339F.scale_x = 1.0
    split_F339F.scale_y = 1.0
    split_F339F.alignment = 'Expand'.upper()
    if not True: split_F339F.operator_context = "EXEC_DEFAULT"
    split_F339F.prop(bpy.context.scene.sna_dgs_scene_properties, 'show_tips', text='Tips', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'tips-one.svg')), emboss=True)
    row_273F5 = split_F339F.row(heading='', align=False)
    row_273F5.alert = False
    row_273F5.enabled = True
    row_273F5.active = True
    row_273F5.use_property_split = False
    row_273F5.use_property_decorate = False
    row_273F5.scale_x = 1.0
    row_273F5.scale_y = 1.0
    row_273F5.alignment = 'Right'.upper()
    row_273F5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = row_273F5.operator('sna.dgs_render_open_documentation_3a04f', text='Documentation', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'documentation.svg')), emboss=True, depress=False)
    op = row_273F5.operator('sna.dgs_render_open_tutorial_video_0684a', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'video.svg')), emboss=True, depress=False)
    box_DE3AB = col_CB7BF.box()
    box_DE3AB.alert = False
    box_DE3AB.enabled = True
    box_DE3AB.active = True
    box_DE3AB.use_property_split = False
    box_DE3AB.use_property_decorate = False
    box_DE3AB.alignment = 'Expand'.upper()
    box_DE3AB.scale_x = 1.0
    box_DE3AB.scale_y = 1.0
    if not True: box_DE3AB.operator_context = "EXEC_DEFAULT"
    row_7D004 = box_DE3AB.row(heading='', align=False)
    row_7D004.alert = False
    row_7D004.enabled = True
    row_7D004.active = True
    row_7D004.use_property_split = False
    row_7D004.use_property_decorate = False
    row_7D004.scale_x = 1.0
    row_7D004.scale_y = 1.2000000476837158
    row_7D004.alignment = 'Expand'.upper()
    row_7D004.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_7D004.label(text='Get More Addons', icon_value=0)
    split_649B4 = row_7D004.split(factor=0.5, align=False)
    split_649B4.alert = False
    split_649B4.enabled = True
    split_649B4.active = True
    split_649B4.use_property_split = False
    split_649B4.use_property_decorate = False
    split_649B4.scale_x = 1.0
    split_649B4.scale_y = 1.0
    split_649B4.alignment = 'Expand'.upper()
    if not True: split_649B4.operator_context = "EXEC_DEFAULT"
    op = split_649B4.operator('sna.dgs_render_launch_superhive_store_08f23', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'SuperHive Logo White.png')), emboss=True, depress=False)
    op = split_649B4.operator('sna.dgs_render_launch_kiri_blender_addons_page_9d58c', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'kiriengine blender addon icon color.svg')), emboss=True, depress=False)
