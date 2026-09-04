import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_r2_update_menu_6A492(layout_function, ):
    box_EB86E = layout_function.box()
    box_B1484 = box_EB86E.box()
    box_B1484.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_hide_on_change', text='Toggle visibility on menu change', icon_value=0, emboss=True)
    box_B1484.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_transforms', text='Copy source transforms', icon_value=0, emboss=True)
    box_B1484.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_selected', text='Update selected Proxy Empties only', icon_value=0, emboss=True)
    row_7FB2A = box_B1484.row(heading='', align=False)
    row_7FB2A.label(text='Rig Behaviour', icon_value=0)
    row_7FB2A.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_render_rig_cache_mode', text='', icon_value=0, emboss=True)
    box_2F177 = box_EB86E.box()
    col_9BE62 = box_2F177.column(heading='', align=True)
    col_9BE62.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_sh_degree', text='SH Degrees', icon_value=0, emboss=True, expand=True)
    col_9BE62.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_sort_threshold', text='Camera Move Sort Threshold', icon_value=0, emboss=True, expand=True)
    col_9BE62.prop(bpy.context.scene.sna_dgs_scene_properties, 'rt_rotation_sort_threshold', text='Camera Turn Sort Threshold', icon_value=0, emboss=True, expand=True)
    box_4B521 = box_EB86E.box()
    box_4B521.enabled = (not ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)))
    col_2B0AE = box_4B521.column(heading='', align=True)
    row_09C1F = col_2B0AE.row(heading='', align=False)
    row_09C1F.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_update_type', text=bpy.context.scene.sna_dgs_scene_properties.r2_update_type, icon_value=0, emboss=True, expand=True)
    if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval'):
        col_2B0AE.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_interval', text='Interval Time (Seconds)', icon_value=0, emboss=True, expand=True)
    col_A95B5 = col_2B0AE.column(heading='', align=False)
    col_A95B5.scale_y = 2.0
    op = col_A95B5.operator('sna.dgs_render_refresh_scene_a6719', text='Update Scene', icon_value=(load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'play.svg')) if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval') else load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg'))), emboss=True, depress=False)
    if ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)):
        col_9AB35 = box_EB86E.column(heading='', align=False)
        col_9AB35.alert = True
        col_9AB35.scale_y = 2.0
        op = col_9AB35.operator('sna.dgs_render_stop_interval_updates_83370', text='Stop', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'stop.svg')), emboss=True, depress=False)
    if bpy.context.preferences.addons[__package__].preferences.sna_show_tips:
        col_BE44B = box_EB86E.column(heading='', align=False)
        if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval'):
            box_CCFB1 = col_BE44B.box()
            box_CCFB1.label(text='Interval Updates are intensive', icon_value=0)
            box_CCFB1.label(text='Use it to preview single, small object animations', icon_value=0)
            box_CCFB1.label(text='Use with caution, expect lagging', icon_value=0)
        box_59076 = col_BE44B.box()
        box_59076.label(text='If depth sorting fails', icon_value=0)
        box_59076.label(text='Move the camera with Shift+Middle Mouse', icon_value=0)
