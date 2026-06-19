import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_light_bake_build_8B9DD(layout_function, ):
    box_90A4F = layout_function.box()
    box_90A4F.alert = False
    box_90A4F.enabled = True
    box_90A4F.active = True
    box_90A4F.use_property_split = False
    box_90A4F.use_property_decorate = False
    box_90A4F.alignment = 'Expand'.upper()
    box_90A4F.scale_x = 1.0
    box_90A4F.scale_y = 1.0
    if not True: box_90A4F.operator_context = "EXEC_DEFAULT"
    box_90A4F.label(text='Include', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    row_095CC = box_90A4F.row(heading='', align=False)
    row_095CC.alert = False
    row_095CC.enabled = True
    row_095CC.active = True
    row_095CC.use_property_split = False
    row_095CC.use_property_decorate = False
    row_095CC.scale_x = 1.0
    row_095CC.scale_y = 1.0
    row_095CC.alignment = 'Expand'.upper()
    row_095CC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_095CC.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_include_world_environment', text='World', icon_value=0, emboss=True)
    row_095CC.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_include_scene_lights', text='Light Objects', icon_value=0, emboss=True)
    if (bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment or bpy.context.scene.sna_dgs_scene_properties.relight_include_scene_lights):
        col_AD78B = layout_function.column(heading='', align=True)
        col_AD78B.alert = False
        col_AD78B.enabled = True
        col_AD78B.active = True
        col_AD78B.use_property_split = False
        col_AD78B.use_property_decorate = False
        col_AD78B.scale_x = 1.0
        col_AD78B.scale_y = 1.0
        col_AD78B.alignment = 'Expand'.upper()
        col_AD78B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_4882E = col_AD78B.box()
        box_4882E.alert = False
        box_4882E.enabled = True
        box_4882E.active = True
        box_4882E.use_property_split = False
        box_4882E.use_property_decorate = False
        box_4882E.alignment = 'Expand'.upper()
        box_4882E.scale_x = 1.0
        box_4882E.scale_y = 1.0
        if not True: box_4882E.operator_context = "EXEC_DEFAULT"
        col_3E710 = box_4882E.column(heading='', align=True)
        col_3E710.alert = False
        col_3E710.enabled = True
        col_3E710.active = True
        col_3E710.use_property_split = False
        col_3E710.use_property_decorate = False
        col_3E710.scale_x = 1.0
        col_3E710.scale_y = 1.0
        col_3E710.alignment = 'Expand'.upper()
        col_3E710.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
        col_3E710.label(text='Interpolation', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        col_3E710.prop(bpy.context.scene.sna_dgs_scene_properties, 'normal_smoothing', text='Proxy Normal Smoothing', icon_value=0, emboss=True)
        col_3E710.prop(bpy.context.scene.sna_dgs_scene_properties, 'pre_light_smoothing', text='Pre-Light Smoothing', icon_value=0, emboss=True)
        col_3E710.prop(bpy.context.scene.sna_dgs_scene_properties, 'post_light_smoothing', text='Post-Light Smoothing', icon_value=0, emboss=True)
        split_755B4 = col_3E710.split(factor=0.5, align=False)
        split_755B4.alert = False
        split_755B4.enabled = True
        split_755B4.active = True
        split_755B4.use_property_split = False
        split_755B4.use_property_decorate = False
        split_755B4.scale_x = 1.0
        split_755B4.scale_y = 1.0
        split_755B4.alignment = 'Expand'.upper()
        if not True: split_755B4.operator_context = "EXEC_DEFAULT"
        split_755B4.label(text='Transfer Style', icon_value=0)
        split_755B4.prop(bpy.context.scene.sna_dgs_scene_properties, 'transfer_style', text='', icon_value=0, emboss=True)
        if (bpy.context.scene.sna_dgs_scene_properties.transfer_style == 'Accurate'):
            pass
        else:
            col_3E710.prop(bpy.context.scene.sna_dgs_scene_properties, 'transfer_smoothness', text='Transfer Smoothness', icon_value=0, emboss=True)
        if bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment:
            box_018E2 = col_AD78B.box()
            box_018E2.alert = False
            box_018E2.enabled = True
            box_018E2.active = True
            box_018E2.use_property_split = False
            box_018E2.use_property_decorate = False
            box_018E2.alignment = 'Expand'.upper()
            box_018E2.scale_x = 1.0
            box_018E2.scale_y = 1.0
            if not True: box_018E2.operator_context = "EXEC_DEFAULT"
            col_12C25 = box_018E2.column(heading='', align=True)
            col_12C25.alert = False
            col_12C25.enabled = True
            col_12C25.active = True
            col_12C25.use_property_split = False
            col_12C25.use_property_decorate = False
            col_12C25.scale_x = 1.0
            col_12C25.scale_y = 1.0
            col_12C25.alignment = 'Expand'.upper()
            col_12C25.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
            col_12C25.label(text='World Light', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            col_12C25.prop(bpy.context.scene.sna_dgs_scene_properties, 'hdri_max_width', text='HDRI Max Width', icon_value=0, emboss=True)
            col_12C25.prop(bpy.context.scene.sna_dgs_scene_properties, 'irradiance_resolution', text='Irradiance Resolution', icon_value=0, emboss=True)
            col_12C25.prop(bpy.context.scene.sna_dgs_scene_properties, 'irradiance_blur_strength', text='Irradiance Blur', icon_value=0, emboss=True)
            col_12C25.prop(bpy.context.scene.sna_dgs_scene_properties, 'irradiance_luminance_clamp', text='Irradiance Clamp', icon_value=0, emboss=True)
        if bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment:
            box_10AE9 = col_AD78B.box()
            box_10AE9.alert = False
            box_10AE9.enabled = True
            box_10AE9.active = True
            box_10AE9.use_property_split = False
            box_10AE9.use_property_decorate = False
            box_10AE9.alignment = 'Expand'.upper()
            box_10AE9.scale_x = 1.0
            box_10AE9.scale_y = 1.0
            if not True: box_10AE9.operator_context = "EXEC_DEFAULT"
            box_10AE9.label(text='World Occlusion', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            box_10AE9.prop(bpy.context.scene.sna_dgs_scene_properties, 'use_proxy_occlusion', text='Enable Proxy Occlusion', icon_value=0, emboss=True)
            if bpy.context.scene.sna_dgs_scene_properties.use_proxy_occlusion:
                col_803AA = box_10AE9.column(heading='', align=True)
                col_803AA.alert = False
                col_803AA.enabled = True
                col_803AA.active = True
                col_803AA.use_property_split = False
                col_803AA.use_property_decorate = False
                col_803AA.scale_x = 1.0
                col_803AA.scale_y = 1.0
                col_803AA.alignment = 'Expand'.upper()
                col_803AA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_803AA.prop(bpy.context.scene.sna_dgs_scene_properties, 'occlusion_sample_count', text='Occlusion sample count', icon_value=0, emboss=True)
                col_803AA.prop(bpy.context.scene.sna_dgs_scene_properties, 'occlusion_bias', text='Occlusion bias', icon_value=0, emboss=True)
                col_803AA.prop(bpy.context.scene.sna_dgs_scene_properties, 'occlusion_max_distance', text='Occlusion Max Distance', icon_value=0, emboss=True)
        if bpy.context.scene.sna_dgs_scene_properties.relight_include_scene_lights:
            box_8F86C = col_AD78B.box()
            box_8F86C.alert = False
            box_8F86C.enabled = True
            box_8F86C.active = True
            box_8F86C.use_property_split = False
            box_8F86C.use_property_decorate = False
            box_8F86C.alignment = 'Expand'.upper()
            box_8F86C.scale_x = 1.0
            box_8F86C.scale_y = 1.0
            if not True: box_8F86C.operator_context = "EXEC_DEFAULT"
            col_548B3 = box_8F86C.column(heading='', align=True)
            col_548B3.alert = False
            col_548B3.enabled = True
            col_548B3.active = True
            col_548B3.use_property_split = False
            col_548B3.use_property_decorate = False
            col_548B3.scale_x = 1.0
            col_548B3.scale_y = 1.0
            col_548B3.alignment = 'Expand'.upper()
            col_548B3.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
            col_548B3.label(text='Light Objects', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            col_548B3.prop(bpy.context.scene.sna_dgs_scene_properties, 'include_hidden_lights', text='Include Hidden Lights', icon_value=0, emboss=True)
            col_548B3.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_scene_light_gain', text='Light Gain', icon_value=0, emboss=True)
            col_548B3.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_use_light_shadows', text='Light Object Shadows', icon_value=0, emboss=True)
            col_548B3.prop(bpy.context.scene.sna_dgs_scene_properties, 'light_shadow_bias', text='Light Object Shadow Bias', icon_value=0, emboss=True)
        box_A44FD = col_AD78B.box()
        box_A44FD.alert = False
        box_A44FD.enabled = True
        box_A44FD.active = True
        box_A44FD.use_property_split = False
        box_A44FD.use_property_decorate = False
        box_A44FD.alignment = 'Expand'.upper()
        box_A44FD.scale_x = 1.0
        box_A44FD.scale_y = 2.0
        if not True: box_A44FD.operator_context = "EXEC_DEFAULT"
        op = box_A44FD.operator('sna.dgs_render_build_light_data_ab375', text='Bake Light Data', icon_value=0, emboss=True, depress=False)
