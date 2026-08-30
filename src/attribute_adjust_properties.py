import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_attribute_adjust_properties_2C323(layout_function, ):
    box_C40B6 = layout_function.box()
    split_B43D4 = box_C40B6.split(factor=0.5, align=False)
    split_B43D4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], 'show_viewport', text='Adjust Attributes', icon_value=0, emboss=True, toggle=True)
    row_3EABC = split_B43D4.row(heading='', align=True)
    row_3EABC.alignment = 'Right'.upper()
    row_3EABC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
    op = row_3EABC.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
    op.sna_target_object = bpy.context.view_layer.objects.active.name
    op.sna_target_modifier = 'KIRI_3DGS_Adjust_Attributes_GN'
    op = row_3EABC.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
    op.sna_target_object = bpy.context.view_layer.objects.active.name
    op.sna_target_modifier = 'KIRI_3DGS_Adjust_Attributes_GN'
    box_F28C4 = box_C40B6.box()
    op = box_F28C4.operator('sna.dgs_render_remove_higher_sh_attributes_cb703', text='Remove Higher SH Attributes', icon_value=0, emboss=True, depress=False)
    col_4C14E = box_C40B6.column(heading='', align=True)
    attr_E874B = '["' + str('Socket_3' + '"]') 
    col_4C14E.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_E874B), text='Scale Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_3']:
        col_31C13 = col_4C14E.column(heading='', align=True)
        attr_2C986 = '["' + str('Socket_6' + '"]') 
        col_31C13.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_2C986), text='', icon_value=0, emboss=True, toggle=True)
        if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_6'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_6'] == 3)):
            box_EE993 = col_31C13.box()
            box_EE993.label(text='Change values slowly to avoid crashes', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        attr_120DC = '["' + str('Socket_8' + '"]') 
        col_31C13.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_120DC), text='', icon_value=0, emboss=True, toggle=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_8'] == 0):
            attr_B4207 = '["' + str('Socket_5' + '"]') 
            col_31C13.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_B4207), text='All Scales', icon_value=0, emboss=True, toggle=True)
        else:
            col_9E5AF = col_31C13.column(heading='', align=False)
            attr_734DA = '["' + str('Socket_10' + '"]') 
            col_9E5AF.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_734DA), text='Scale_0', icon_value=0, emboss=True, toggle=True)
            attr_EAC87 = '["' + str('Socket_9' + '"]') 
            col_9E5AF.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_EAC87), text='Scale_1', icon_value=0, emboss=True, toggle=True)
            attr_F45C1 = '["' + str('Socket_7' + '"]') 
            col_9E5AF.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_F45C1), text='Scale_2', icon_value=0, emboss=True, toggle=True)
    col_75DFB = box_C40B6.column(heading='', align=True)
    attr_670D5 = '["' + str('Socket_4' + '"]') 
    col_75DFB.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_670D5), text='Rotation Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_4']:
        col_B2D6A = col_75DFB.column(heading='', align=True)
        attr_85A74 = '["' + str('Socket_48' + '"]') 
        col_B2D6A.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_85A74), text='', icon_value=0, emboss=True, toggle=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_48'] == 0):
            col_125B4 = col_B2D6A.column(heading='', align=True)
            attr_389BC = '["' + str('Socket_21' + '"]') 
            col_125B4.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_389BC), text='Rotation', icon_value=0, emboss=True, toggle=True)
        else:
            col_F40AA = col_B2D6A.column(heading='', align=True)
            attr_6DFDA = '["' + str('Socket_51' + '"]') 
            col_F40AA.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_6DFDA), text='Axis', icon_value=0, emboss=True, toggle=True)
            attr_E15B5 = '["' + str('Socket_50' + '"]') 
            col_F40AA.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_E15B5), text='Target', icon_value=0, emboss=True, toggle=True)
    col_0C20D = box_C40B6.column(heading='', align=True)
    attr_D2232 = '["' + str('Socket_54' + '"]') 
    col_0C20D.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_D2232), text='Opacity Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_54']:
        col_F6DA7 = col_0C20D.column(heading='', align=True)
        attr_7BD79 = '["' + str('Socket_52' + '"]') 
        col_F6DA7.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_7BD79), text='', icon_value=0, emboss=True, toggle=True)
        if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_52'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_52'] == 3)):
            box_E8A8F = col_F6DA7.box()
            box_E8A8F.label(text='Change values slowly to avoid crashes', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        attr_20728 = '["' + str('Socket_55' + '"]') 
        col_F6DA7.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_20728), text='All Scales', icon_value=0, emboss=True, toggle=True)
    col_CADFD = box_C40B6.column(heading='', align=True)
    attr_9A41E = '["' + str('Socket_23' + '"]') 
    col_CADFD.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_9A41E), text='SH 1 Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_23']:
        col_83806 = col_CADFD.column(heading='', align=True)
        attr_31D21 = '["' + str('Socket_24' + '"]') 
        col_83806.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_31D21), text='Red Adjust Type', icon_value=0, emboss=True, expand=False, toggle=True)
        attr_0574B = '["' + str('Socket_25' + '"]') 
        col_83806.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_0574B), text='', icon_value=0, emboss=True, toggle=True)
        attr_1A2E2 = '["' + str('Socket_30' + '"]') 
        col_83806.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_1A2E2), text='Green Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_8AA4D = '["' + str('Socket_31' + '"]') 
        col_83806.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_8AA4D), text='', icon_value=0, emboss=True, toggle=True)
        attr_FA4D9 = '["' + str('Socket_32' + '"]') 
        col_83806.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_FA4D9), text='Blue Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_955F9 = '["' + str('Socket_33' + '"]') 
        col_83806.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_955F9), text='', icon_value=0, emboss=True, toggle=True)
    col_F20A7 = box_C40B6.column(heading='', align=True)
    attr_86E8C = '["' + str('Socket_34' + '"]') 
    col_F20A7.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_86E8C), text='SH 2 Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_34']:
        col_41831 = col_F20A7.column(heading='', align=True)
        attr_EE5FE = '["' + str('Socket_35' + '"]') 
        col_41831.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_EE5FE), text='Red Adjust Type', icon_value=0, emboss=True, expand=False, toggle=True)
        attr_380DC = '["' + str('Socket_36' + '"]') 
        col_41831.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_380DC), text='', icon_value=0, emboss=True, toggle=True)
        attr_B1895 = '["' + str('Socket_37' + '"]') 
        col_41831.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_B1895), text='Green Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_1937E = '["' + str('Socket_38' + '"]') 
        col_41831.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_1937E), text='', icon_value=0, emboss=True, toggle=True)
        attr_609BB = '["' + str('Socket_42' + '"]') 
        col_41831.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_609BB), text='Blue Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_75F7B = '["' + str('Socket_43' + '"]') 
        col_41831.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_75F7B), text='', icon_value=0, emboss=True, toggle=True)
    col_1D52E = box_C40B6.column(heading='', align=True)
    attr_73E08 = '["' + str('Socket_39' + '"]') 
    col_1D52E.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_73E08), text='SH 3 Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_39']:
        col_9E249 = col_1D52E.column(heading='', align=True)
        attr_E35A2 = '["' + str('Socket_40' + '"]') 
        col_9E249.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_E35A2), text='Red Adjust Type', icon_value=0, emboss=True, expand=False, toggle=True)
        attr_4369F = '["' + str('Socket_41' + '"]') 
        col_9E249.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_4369F), text='', icon_value=0, emboss=True, toggle=True)
        attr_DAC40 = '["' + str('Socket_44' + '"]') 
        col_9E249.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_DAC40), text='Green Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_BE5C0 = '["' + str('Socket_45' + '"]') 
        col_9E249.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_BE5C0), text='', icon_value=0, emboss=True, toggle=True)
        attr_A4AC7 = '["' + str('Socket_46' + '"]') 
        col_9E249.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_A4AC7), text='Blue Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_33CFF = '["' + str('Socket_47' + '"]') 
        col_9E249.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_33CFF), text='', icon_value=0, emboss=True, toggle=True)
