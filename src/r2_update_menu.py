import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_r2_update_menu_6A492(layout_function, ):
    box_EB86E = layout_function.box()
    box_EB86E.alert = False
    box_EB86E.enabled = True
    box_EB86E.active = True
    box_EB86E.use_property_split = False
    box_EB86E.use_property_decorate = False
    box_EB86E.alignment = 'Expand'.upper()
    box_EB86E.scale_x = 1.0
    box_EB86E.scale_y = 1.0
    if not True: box_EB86E.operator_context = "EXEC_DEFAULT"
    box_B1484 = box_EB86E.box()
    box_B1484.alert = False
    box_B1484.enabled = True
    box_B1484.active = True
    box_B1484.use_property_split = False
    box_B1484.use_property_decorate = False
    box_B1484.alignment = 'Expand'.upper()
    box_B1484.scale_x = 1.0
    box_B1484.scale_y = 1.0
    if not True: box_B1484.operator_context = "EXEC_DEFAULT"
    box_B1484.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_hide_on_change', text='Toggle visibility on menu change', icon_value=0, emboss=True)
    box_B1484.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_transforms', text='Copy source transforms', icon_value=0, emboss=True)
    box_B1484.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_selected', text='Update selected Proxy Empties only', icon_value=0, emboss=True)
    row_7FB2A = box_B1484.row(heading='', align=False)
    row_7FB2A.alert = False
    row_7FB2A.enabled = True
    row_7FB2A.active = True
    row_7FB2A.use_property_split = False
    row_7FB2A.use_property_decorate = False
    row_7FB2A.scale_x = 1.0
    row_7FB2A.scale_y = 1.0
    row_7FB2A.alignment = 'Expand'.upper()
    row_7FB2A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_7FB2A.label(text='Rig Behaviour', icon_value=0)
    row_7FB2A.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_render_rig_cache_mode', text='', icon_value=0, emboss=True)
    box_2F177 = box_EB86E.box()
    box_2F177.alert = False
    box_2F177.enabled = True
    box_2F177.active = True
    box_2F177.use_property_split = False
    box_2F177.use_property_decorate = False
    box_2F177.alignment = 'Expand'.upper()
    box_2F177.scale_x = 1.0
    box_2F177.scale_y = 1.0
    if not True: box_2F177.operator_context = "EXEC_DEFAULT"
    col_9BE62 = box_2F177.column(heading='', align=True)
    col_9BE62.alert = False
    col_9BE62.enabled = True
    col_9BE62.active = True
    col_9BE62.use_property_split = False
    col_9BE62.use_property_decorate = False
    col_9BE62.scale_x = 1.0
    col_9BE62.scale_y = 1.0
    col_9BE62.alignment = 'Expand'.upper()
    col_9BE62.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_9BE62.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_sh_degree', text='SH Degrees', icon_value=0, emboss=True, expand=True)
    col_9BE62.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_sort_threshold', text='Camera Move Sort Threshold', icon_value=0, emboss=True, expand=True)
    box_4B521 = box_EB86E.box()
    box_4B521.alert = False
    box_4B521.enabled = (not ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)))
    box_4B521.active = True
    box_4B521.use_property_split = False
    box_4B521.use_property_decorate = False
    box_4B521.alignment = 'Expand'.upper()
    box_4B521.scale_x = 1.0
    box_4B521.scale_y = 1.0
    if not True: box_4B521.operator_context = "EXEC_DEFAULT"
    col_2B0AE = box_4B521.column(heading='', align=True)
    col_2B0AE.alert = False
    col_2B0AE.enabled = True
    col_2B0AE.active = True
    col_2B0AE.use_property_split = False
    col_2B0AE.use_property_decorate = False
    col_2B0AE.scale_x = 1.0
    col_2B0AE.scale_y = 1.0
    col_2B0AE.alignment = 'Expand'.upper()
    col_2B0AE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_09C1F = col_2B0AE.row(heading='', align=False)
    row_09C1F.alert = False
    row_09C1F.enabled = True
    row_09C1F.active = True
    row_09C1F.use_property_split = False
    row_09C1F.use_property_decorate = False
    row_09C1F.scale_x = 1.0
    row_09C1F.scale_y = 1.0
    row_09C1F.alignment = 'Expand'.upper()
    row_09C1F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_09C1F.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_update_type', text=bpy.context.scene.sna_dgs_scene_properties.r2_update_type, icon_value=0, emboss=True, expand=True)
    if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval'):
        col_2B0AE.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_interval', text='Interval Time (Seconds)', icon_value=0, emboss=True, expand=True)
    col_A95B5 = col_2B0AE.column(heading='', align=False)
    col_A95B5.alert = False
    col_A95B5.enabled = True
    col_A95B5.active = True
    col_A95B5.use_property_split = False
    col_A95B5.use_property_decorate = False
    col_A95B5.scale_x = 1.0
    col_A95B5.scale_y = 2.0
    col_A95B5.alignment = 'Expand'.upper()
    col_A95B5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_A95B5.operator('sna.dgs_render_refresh_scene_a6719', text='Update Scene', icon_value=(load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'play.svg')) if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval') else load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg'))), emboss=True, depress=False)
    if ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)):
        col_9AB35 = box_EB86E.column(heading='', align=False)
        col_9AB35.alert = True
        col_9AB35.enabled = True
        col_9AB35.active = True
        col_9AB35.use_property_split = False
        col_9AB35.use_property_decorate = False
        col_9AB35.scale_x = 1.0
        col_9AB35.scale_y = 2.0
        col_9AB35.alignment = 'Expand'.upper()
        col_9AB35.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_9AB35.operator('sna.dgs_render_stop_interval_updates_83370', text='Stop', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'stop.svg')), emboss=True, depress=False)
    if bpy.context.preferences.addons[__package__].preferences.sna_show_tips:
        col_BE44B = box_EB86E.column(heading='', align=False)
        col_BE44B.alert = False
        col_BE44B.enabled = True
        col_BE44B.active = True
        col_BE44B.use_property_split = False
        col_BE44B.use_property_decorate = False
        col_BE44B.scale_x = 1.0
        col_BE44B.scale_y = 1.0
        col_BE44B.alignment = 'Expand'.upper()
        col_BE44B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval'):
            box_CCFB1 = col_BE44B.box()
            box_CCFB1.alert = False
            box_CCFB1.enabled = True
            box_CCFB1.active = True
            box_CCFB1.use_property_split = False
            box_CCFB1.use_property_decorate = False
            box_CCFB1.alignment = 'Expand'.upper()
            box_CCFB1.scale_x = 1.0
            box_CCFB1.scale_y = 1.0
            if not True: box_CCFB1.operator_context = "EXEC_DEFAULT"
            box_CCFB1.label(text='Interval Updates are intensive', icon_value=0)
            box_CCFB1.label(text='Use it to preview single, small object animations', icon_value=0)
            box_CCFB1.label(text='Use with caution, expect lagging', icon_value=0)
        box_59076 = col_BE44B.box()
        box_59076.alert = False
        box_59076.enabled = True
        box_59076.active = True
        box_59076.use_property_split = False
        box_59076.use_property_decorate = False
        box_59076.alignment = 'Expand'.upper()
        box_59076.scale_x = 1.0
        box_59076.scale_y = 1.0
        if not True: box_59076.operator_context = "EXEC_DEFAULT"
        box_59076.label(text='If depth sorting fails', icon_value=0)
        box_59076.label(text='Move the camera with Shift+Middle Mouse', icon_value=0)
