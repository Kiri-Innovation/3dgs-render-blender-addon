import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_light_bake_build_8B9DD(layout_function, ):
    box_90A4F = layout_function.box()
    box_90A4F.label(text='Include', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    row_095CC = box_90A4F.row(heading='', align=False)
    row_095CC.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_include_world_environment', text='World', icon_value=0, emboss=True)
    row_095CC.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_include_scene_lights', text='Light Objects', icon_value=0, emboss=True)
    if (bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment or bpy.context.scene.sna_dgs_scene_properties.relight_include_scene_lights):
        col_AD78B = layout_function.column(heading='', align=True)
        box_4882E = col_AD78B.box()
        col_3E710 = box_4882E.column(heading='', align=True)
        col_3E710.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
        col_3E710.label(text='Interpolation', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        col_3E710.prop(bpy.context.scene.sna_dgs_scene_properties, 'normal_smoothing', text='Proxy Normal Smoothing', icon_value=0, emboss=True)
        col_3E710.prop(bpy.context.scene.sna_dgs_scene_properties, 'pre_light_smoothing', text='Pre-Light Smoothing', icon_value=0, emboss=True)
        col_3E710.prop(bpy.context.scene.sna_dgs_scene_properties, 'post_light_smoothing', text='Post-Light Smoothing', icon_value=0, emboss=True)
        split_755B4 = col_3E710.split(factor=0.5, align=False)
        split_755B4.label(text='Transfer Style', icon_value=0)
        split_755B4.prop(bpy.context.scene.sna_dgs_scene_properties, 'transfer_style', text='', icon_value=0, emboss=True)
        if (bpy.context.scene.sna_dgs_scene_properties.transfer_style == 'Accurate'):
            pass
        else:
            col_3E710.prop(bpy.context.scene.sna_dgs_scene_properties, 'transfer_smoothness', text='Transfer Smoothness', icon_value=0, emboss=True)
        if bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment:
            box_018E2 = col_AD78B.box()
            col_12C25 = box_018E2.column(heading='', align=True)
            col_12C25.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
            col_12C25.label(text='World Light', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            col_12C25.prop(bpy.context.scene.sna_dgs_scene_properties, 'hdri_max_width', text='HDRI Max Width', icon_value=0, emboss=True)
            col_12C25.prop(bpy.context.scene.sna_dgs_scene_properties, 'irradiance_resolution', text='Irradiance Resolution', icon_value=0, emboss=True)
            col_12C25.prop(bpy.context.scene.sna_dgs_scene_properties, 'irradiance_blur_strength', text='Irradiance Blur', icon_value=0, emboss=True)
            col_12C25.prop(bpy.context.scene.sna_dgs_scene_properties, 'irradiance_luminance_clamp', text='Irradiance Clamp', icon_value=0, emboss=True)
        if bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment:
            box_10AE9 = col_AD78B.box()
            box_10AE9.label(text='World Occlusion', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            box_10AE9.prop(bpy.context.scene.sna_dgs_scene_properties, 'use_proxy_occlusion', text='Enable Proxy Occlusion', icon_value=0, emboss=True)
            if bpy.context.scene.sna_dgs_scene_properties.use_proxy_occlusion:
                col_803AA = box_10AE9.column(heading='', align=True)
                col_803AA.prop(bpy.context.scene.sna_dgs_scene_properties, 'occlusion_sample_count', text='Occlusion sample count', icon_value=0, emboss=True)
                col_803AA.prop(bpy.context.scene.sna_dgs_scene_properties, 'occlusion_bias', text='Occlusion bias', icon_value=0, emboss=True)
                col_803AA.prop(bpy.context.scene.sna_dgs_scene_properties, 'occlusion_max_distance', text='Occlusion Max Distance', icon_value=0, emboss=True)
        if bpy.context.scene.sna_dgs_scene_properties.relight_include_scene_lights:
            box_8F86C = col_AD78B.box()
            col_548B3 = box_8F86C.column(heading='', align=True)
            col_548B3.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
            col_548B3.label(text='Light Objects', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            col_548B3.prop(bpy.context.scene.sna_dgs_scene_properties, 'include_hidden_lights', text='Include Hidden Lights', icon_value=0, emboss=True)
            col_548B3.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_scene_light_gain', text='Light Gain', icon_value=0, emboss=True)
            col_548B3.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_use_light_shadows', text='Light Object Shadows', icon_value=0, emboss=True)
            col_548B3.prop(bpy.context.scene.sna_dgs_scene_properties, 'light_shadow_bias', text='Light Object Shadow Bias', icon_value=0, emboss=True)
        box_A44FD = col_AD78B.box()
        box_A44FD.scale_y = 2.0
        op = box_A44FD.operator('sna.dgs_render_build_light_data_ab375', text='Bake Light Data', icon_value=0, emboss=True, depress=False)
