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
            box_FAC0D.alert = False
            box_FAC0D.enabled = True
            box_FAC0D.active = True
            box_FAC0D.use_property_split = False
            box_FAC0D.use_property_decorate = False
            box_FAC0D.alignment = 'Expand'.upper()
            box_FAC0D.scale_x = 1.0
            box_FAC0D.scale_y = 1.0
            if not True: box_FAC0D.operator_context = "EXEC_DEFAULT"
            box_FAC0D.label(text='Bake light data before applying', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    else:
        box_C3353 = layout_function.box()
        box_C3353.alert = False
        box_C3353.enabled = True
        box_C3353.active = True
        box_C3353.use_property_split = False
        box_C3353.use_property_decorate = False
        box_C3353.alignment = 'Expand'.upper()
        box_C3353.scale_x = 1.0
        box_C3353.scale_y = 1.0
        if not True: box_C3353.operator_context = "EXEC_DEFAULT"
        box_C3353.label(text='Bake light data before applying', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    box_FCA92 = layout_function.box()
    box_FCA92.alert = False
    box_FCA92.enabled = True
    box_FCA92.active = True
    box_FCA92.use_property_split = False
    box_FCA92.use_property_decorate = False
    box_FCA92.alignment = 'Expand'.upper()
    box_FCA92.scale_x = 1.0
    box_FCA92.scale_y = 1.0
    if not True: box_FCA92.operator_context = "EXEC_DEFAULT"
    box_FCA92.label(text='Light Pass Mix', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    col_55C97 = box_FCA92.column(heading='', align=True)
    col_55C97.alert = False
    col_55C97.enabled = True
    col_55C97.active = True
    col_55C97.use_property_split = False
    col_55C97.use_property_decorate = False
    col_55C97.scale_x = 1.0
    col_55C97.scale_y = 1.0
    col_55C97.alignment = 'Expand'.upper()
    col_55C97.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
    col_55C97.prop(bpy.context.scene.sna_dgs_scene_properties, 'indirect_strength', text='Indirect Strength', icon_value=0, emboss=True)
    col_55C97.prop(bpy.context.scene.sna_dgs_scene_properties, 'direct_strength', text='Direct Strength', icon_value=0, emboss=True)
    col_55C97.prop(bpy.context.scene.sna_dgs_scene_properties, 'occlusion_strength', text='Occlusion Strength', icon_value=0, emboss=True)
    col_55C97.prop(bpy.context.scene.sna_dgs_scene_properties, 'shadow_strength', text='Shadow Strength', icon_value=0, emboss=True)
    if (bpy.context.scene.sna_dgs_scene_properties.relight_include_world_environment or bpy.context.scene.sna_dgs_scene_properties.relight_include_scene_lights):
        col_2D53F = layout_function.column(heading='', align=True)
        col_2D53F.alert = False
        col_2D53F.enabled = True
        col_2D53F.active = True
        col_2D53F.use_property_split = False
        col_2D53F.use_property_decorate = False
        col_2D53F.scale_x = 1.0
        col_2D53F.scale_y = 1.0
        col_2D53F.alignment = 'Expand'.upper()
        col_2D53F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_C2FE8 = col_2D53F.box()
        box_C2FE8.alert = False
        box_C2FE8.enabled = True
        box_C2FE8.active = True
        box_C2FE8.use_property_split = False
        box_C2FE8.use_property_decorate = False
        box_C2FE8.alignment = 'Expand'.upper()
        box_C2FE8.scale_x = 1.0
        box_C2FE8.scale_y = 1.0
        if not True: box_C2FE8.operator_context = "EXEC_DEFAULT"
        col_A17CD = box_C2FE8.column(heading='', align=True)
        col_A17CD.alert = False
        col_A17CD.enabled = True
        col_A17CD.active = True
        col_A17CD.use_property_split = False
        col_A17CD.use_property_decorate = False
        col_A17CD.scale_x = 1.0
        col_A17CD.scale_y = 1.0
        col_A17CD.alignment = 'Expand'.upper()
        col_A17CD.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
        col_A17CD.label(text='Color Mix', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        split_C326C = col_A17CD.split(factor=0.5, align=False)
        split_C326C.alert = False
        split_C326C.enabled = True
        split_C326C.active = True
        split_C326C.use_property_split = False
        split_C326C.use_property_decorate = False
        split_C326C.scale_x = 1.0
        split_C326C.scale_y = 1.0
        split_C326C.alignment = 'Expand'.upper()
        if not True: split_C326C.operator_context = "EXEC_DEFAULT"
        split_C326C.label(text='Factor Curve', icon_value=0)
        split_C326C.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_factor_curve_mode', text='', icon_value=0, emboss=True)
        split_AB173 = col_A17CD.split(factor=0.5, align=False)
        split_AB173.alert = False
        split_AB173.enabled = True
        split_AB173.active = True
        split_AB173.use_property_split = False
        split_AB173.use_property_decorate = False
        split_AB173.scale_x = 1.0
        split_AB173.scale_y = 1.0
        split_AB173.alignment = 'Expand'.upper()
        if not True: split_AB173.operator_context = "EXEC_DEFAULT"
        split_AB173.label(text='Factor Mode', icon_value=0)
        split_AB173.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_lighting_factor_mode', text='', icon_value=0, emboss=True)
        if (bpy.context.scene.sna_dgs_scene_properties.relight_lighting_factor_mode == 'Luminance'):
            pass
        else:
            col_D67D0 = col_A17CD.column(heading='', align=True)
            col_D67D0.alert = False
            col_D67D0.enabled = True
            col_D67D0.active = True
            col_D67D0.use_property_split = False
            col_D67D0.use_property_decorate = False
            col_D67D0.scale_x = 1.0
            col_D67D0.scale_y = 1.0
            col_D67D0.alignment = 'Expand'.upper()
            col_D67D0.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
            col_D67D0.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_colorize_mix', text='Color Mix', icon_value=0, emboss=True)
            split_18C65 = col_D67D0.split(factor=0.4000000059604645, align=True)
            split_18C65.alert = False
            split_18C65.enabled = True
            split_18C65.active = True
            split_18C65.use_property_split = False
            split_18C65.use_property_decorate = False
            split_18C65.scale_x = 1.0
            split_18C65.scale_y = 1.0
            split_18C65.alignment = 'Expand'.upper()
            if not True: split_18C65.operator_context = "EXEC_DEFAULT"
            split_18C65.prop(bpy.context.scene.sna_dgs_scene_properties, 'relight_max_color_tint', text='Max Tint', icon_value=0, emboss=True)
            split_18C65.prop(bpy.context.scene.sna_dgs_scene_properties, 'max_color_tint_mode', text='', icon_value=0, emboss=True)
        box_85BFD = col_2D53F.box()
        box_85BFD.alert = False
        box_85BFD.enabled = True
        box_85BFD.active = True
        box_85BFD.use_property_split = False
        box_85BFD.use_property_decorate = False
        box_85BFD.alignment = 'Expand'.upper()
        box_85BFD.scale_x = 1.0
        box_85BFD.scale_y = 1.0
        if not True: box_85BFD.operator_context = "EXEC_DEFAULT"
        box_85BFD.label(text='Global Strength', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        col_B19E2 = box_85BFD.column(heading='', align=True)
        col_B19E2.alert = False
        col_B19E2.enabled = True
        col_B19E2.active = True
        col_B19E2.use_property_split = False
        col_B19E2.use_property_decorate = False
        col_B19E2.scale_x = 1.0
        col_B19E2.scale_y = 1.0
        col_B19E2.alignment = 'Expand'.upper()
        col_B19E2.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
        col_B19E2.prop(bpy.context.scene.sna_dgs_scene_properties, 'ambient_floor', text='Ambient Base', icon_value=0, emboss=True)
        col_B19E2.prop(bpy.context.scene.sna_dgs_scene_properties, 'light_gain', text='Light Gain', icon_value=0, emboss=True)
        col_B19E2.prop(bpy.context.scene.sna_dgs_scene_properties, 'light_power', text='Light Contrast', icon_value=0, emboss=True)
        col_B19E2.prop(bpy.context.scene.sna_dgs_scene_properties, 'max_light_factor', text='Max Light Factor', icon_value=0, emboss=True)
        box_51F49 = col_2D53F.box()
        box_51F49.alert = False
        box_51F49.enabled = True
        box_51F49.active = True
        box_51F49.use_property_split = False
        box_51F49.use_property_decorate = False
        box_51F49.alignment = 'Expand'.upper()
        box_51F49.scale_x = 1.0
        box_51F49.scale_y = 1.0
        if not True: box_51F49.operator_context = "EXEC_DEFAULT"
        box_51F49.label(text='SH Updates', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        col_57EA1 = box_51F49.column(heading='', align=True)
        col_57EA1.alert = False
        col_57EA1.enabled = True
        col_57EA1.active = True
        col_57EA1.use_property_split = False
        col_57EA1.use_property_decorate = False
        col_57EA1.scale_x = 1.0
        col_57EA1.scale_y = 1.0
        col_57EA1.alignment = 'Expand'.upper()
        col_57EA1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_57EA1.prop(bpy.context.scene.sna_dgs_scene_properties, 'export_mode', text='', icon_value=0, emboss=True)
        if (bpy.context.scene.sna_dgs_scene_properties.export_mode == 'Dampen Original SH'):
            col_57EA1.prop(bpy.context.scene.sna_dgs_scene_properties, 'directionality_strength', text='SH Strength', icon_value=0, emboss=True)
        box_BBA23 = col_2D53F.box()
        box_BBA23.alert = False
        box_BBA23.enabled = True
        box_BBA23.active = True
        box_BBA23.use_property_split = False
        box_BBA23.use_property_decorate = False
        box_BBA23.alignment = 'Expand'.upper()
        box_BBA23.scale_x = 1.0
        box_BBA23.scale_y = 2.0
        if not True: box_BBA23.operator_context = "EXEC_DEFAULT"
        op = box_BBA23.operator('sna.dgs_render_apply_light_data_6c5ad', text='Apply Lighting', icon_value=0, emboss=True, depress=False)
