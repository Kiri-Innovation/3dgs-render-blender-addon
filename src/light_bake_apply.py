import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_light_bake_apply_A5653(layout_function, ):
    if 'proxy_deferred_relight_stage_baked' in bpy.context.view_layer.objects.active:
        if bpy.context.view_layer.objects.active['proxy_deferred_relight_stage_baked']:
            pass
        else:
            box_FAC0D = layout_function.box()
            box_FAC0D.label(text='Bake light data before applying', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    else:
        box_C3353 = layout_function.box()
        box_C3353.label(text='Bake light data before applying', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    box_FCA92 = layout_function.box()
    box_FCA92.label(text='Light Pass Mix', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    col_55C97 = box_FCA92.column(heading='', align=True)
    col_55C97.prop(bpy.context.scene.sna_dgs_scene_properties, 'indirect_strength', text='Indirect Strength', icon_value=0, emboss=True)
    col_55C97.prop(bpy.context.scene.sna_dgs_scene_properties, 'direct_strength', text='Direct Strength', icon_value=0, emboss=True)
    col_55C97.prop(bpy.context.scene.sna_dgs_scene_properties, 'occlusion_strength', text='Occlusion Strength', icon_value=0, emboss=True)
    col_55C97.prop(bpy.context.scene.sna_dgs_scene_properties, 'shadow_strength', text='Shadow Strength', icon_value=0, emboss=True)
    if (bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment or bpy.context.scene.sna_dgs_scene_properties.relight_include_scene_lights):
        col_2D53F = layout_function.column(heading='', align=True)
        box_C2FE8 = col_2D53F.box()
        col_A17CD = box_C2FE8.column(heading='', align=True)
        col_A17CD.label(text='Color Mix', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        split_C326C = col_A17CD.split(factor=0.5, align=False)
        split_C326C.label(text='Factor Curve', icon_value=0)
        split_C326C.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_factor_curve_mode', text='', icon_value=0, emboss=True)
        split_AB173 = col_A17CD.split(factor=0.5, align=False)
        split_AB173.label(text='Factor Mode', icon_value=0)
        split_AB173.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_lighting_factor_mode', text='', icon_value=0, emboss=True)
        if (bpy.context.scene.sna_dgs_scene_properties.relight_lighting_factor_mode == 'Luminance'):
            pass
        else:
            col_D67D0 = col_A17CD.column(heading='', align=True)
            col_D67D0.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_colorize_mix', text='Color Mix', icon_value=0, emboss=True)
            split_18C65 = col_D67D0.split(factor=0.4000000059604645, align=True)
            split_18C65.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_max_color_tint', text='Max Tint', icon_value=0, emboss=True)
            split_18C65.prop(bpy.context.scene.sna_dgs_scene_properties, 'max_color_tint_mode', text='', icon_value=0, emboss=True)
        box_85BFD = col_2D53F.box()
        box_85BFD.label(text='Global Strength', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        col_B19E2 = box_85BFD.column(heading='', align=True)
        col_B19E2.prop(bpy.context.scene.sna_dgs_scene_properties, 'ambient_floor', text='Ambient Base', icon_value=0, emboss=True)
        col_B19E2.prop(bpy.context.scene.sna_dgs_scene_properties, 'light_gain', text='Light Gain', icon_value=0, emboss=True)
        col_B19E2.prop(bpy.context.scene.sna_dgs_scene_properties, 'light_power', text='Light Contrast', icon_value=0, emboss=True)
        col_B19E2.prop(bpy.context.scene.sna_dgs_scene_properties, 'max_light_factor', text='Max Light Factor', icon_value=0, emboss=True)
        box_51F49 = col_2D53F.box()
        box_51F49.label(text='SH Updates', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        col_57EA1 = box_51F49.column(heading='', align=True)
        col_57EA1.prop(bpy.context.scene.sna_dgs_scene_properties, 'export_mode', text='', icon_value=0, emboss=True)
        if (bpy.context.scene.sna_dgs_scene_properties.export_mode == 'Dampen Original SH'):
            col_57EA1.prop(bpy.context.scene.sna_dgs_scene_properties, 'directionality_strength', text='SH Strength', icon_value=0, emboss=True)
        box_BBA23 = col_2D53F.box()
        box_BBA23.scale_y = 2.0
        op = box_BBA23.operator('sna.dgs_render_apply_light_data_6c5ad', text='Apply Lighting', icon_value=0, emboss=True, depress=False)
