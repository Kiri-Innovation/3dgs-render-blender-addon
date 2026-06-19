import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_rig_update_settings_88DF0(layout_function, alert, enabled):
    if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
        if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
            box_3ABA6 = layout_function.box()
            box_3ABA6.alert = True
            box_3ABA6.enabled = True
            box_3ABA6.active = True
            box_3ABA6.use_property_split = False
            box_3ABA6.use_property_decorate = False
            box_3ABA6.alignment = 'Expand'.upper()
            box_3ABA6.scale_x = 1.0
            box_3ABA6.scale_y = 1.0
            if not True: box_3ABA6.operator_context = "EXEC_DEFAULT"
            box_3ABA6.label(text='Active Object has baked data', icon_value=load_preview_icon(''))
            op = box_3ABA6.operator('sna.dgs_render_clear_rig_cache_f38be', text='Clear Cache', icon_value=0, emboss=True, depress=False)
    col_8A21A = layout_function.column(heading='', align=True)
    col_8A21A.alert = alert
    col_8A21A.enabled = enabled
    col_8A21A.active = True
    col_8A21A.use_property_split = False
    col_8A21A.use_property_decorate = False
    col_8A21A.scale_x = 1.0
    col_8A21A.scale_y = 1.0
    col_8A21A.alignment = 'Expand'.upper()
    col_8A21A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_8A21A.label(text='Deform Mode', icon_value=0)
    col_8A21A.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_deform_mode', text='', icon_value=0, emboss=True)
    col_384C8 = layout_function.column(heading='', align=True)
    col_384C8.alert = alert
    col_384C8.enabled = enabled
    col_384C8.active = True
    col_384C8.use_property_split = False
    col_384C8.use_property_decorate = False
    col_384C8.scale_x = 1.0
    col_384C8.scale_y = 1.0
    col_384C8.alignment = 'Expand'.upper()
    col_384C8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_384C8.label(text='Scale Adjust Mode', icon_value=0)
    col_384C8.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_scale_safety_mode', text='', icon_value=0, emboss=True)
    col_96F9F = layout_function.column(heading='', align=True)
    col_96F9F.alert = alert
    col_96F9F.enabled = enabled
    col_96F9F.active = True
    col_96F9F.use_property_split = False
    col_96F9F.use_property_decorate = False
    col_96F9F.scale_x = 1.0
    col_96F9F.scale_y = 1.0
    col_96F9F.alignment = 'Expand'.upper()
    col_96F9F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_96F9F.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_update_sh_attributes', text='Update Spherical Harmonics', icon_value=0, emboss=True)
    if bpy.context.scene.sna_dgs_scene_properties.rig_update_sh_attributes:
        col_FEC76 = col_96F9F.column(heading='', align=True)
        col_FEC76.alert = alert
        col_FEC76.enabled = enabled
        col_FEC76.active = True
        col_FEC76.use_property_split = False
        col_FEC76.use_property_decorate = False
        col_FEC76.scale_x = 1.0
        col_FEC76.scale_y = 1.0
        col_FEC76.alignment = 'Expand'.upper()
        col_FEC76.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_FEC76.label(text='SH Quality', icon_value=0)
        row_83260 = col_FEC76.row(heading='', align=False)
        row_83260.alert = False
        row_83260.enabled = True
        row_83260.active = True
        row_83260.use_property_split = False
        row_83260.use_property_decorate = False
        row_83260.scale_x = 1.0
        row_83260.scale_y = 1.0
        row_83260.alignment = 'Expand'.upper()
        row_83260.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_83260.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_sh_quality_mode', text=bpy.context.scene.sna_dgs_scene_properties.rig_sh_quality_mode, icon_value=0, emboss=True, expand=True)
