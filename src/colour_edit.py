import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_colour_edit_37123(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Colour_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_1A729 = layout_function.box()
        box_1A729.alert = False
        box_1A729.enabled = True
        box_1A729.active = True
        box_1A729.use_property_split = False
        box_1A729.use_property_decorate = False
        box_1A729.alignment = 'Expand'.upper()
        box_1A729.scale_x = 1.0
        box_1A729.scale_y = 1.0
        if not True: box_1A729.operator_context = "EXEC_DEFAULT"
        split_A4B39 = box_1A729.split(factor=0.5, align=False)
        split_A4B39.alert = False
        split_A4B39.enabled = True
        split_A4B39.active = True
        split_A4B39.use_property_split = False
        split_A4B39.use_property_decorate = False
        split_A4B39.scale_x = 1.0
        split_A4B39.scale_y = 1.0
        split_A4B39.alignment = 'Expand'.upper()
        if not True: split_A4B39.operator_context = "EXEC_DEFAULT"
        split_A4B39.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], 'show_viewport', text='Colour Edit', icon_value=0, emboss=True, toggle=True)
        row_7335E = split_A4B39.row(heading='', align=True)
        row_7335E.alert = False
        row_7335E.enabled = True
        row_7335E.active = True
        row_7335E.use_property_split = False
        row_7335E.use_property_decorate = False
        row_7335E.scale_x = 1.0
        row_7335E.scale_y = 1.0
        row_7335E.alignment = 'Right'.upper()
        row_7335E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_7335E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_7335E.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Colour_Edit_GN'
        op = row_7335E.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Colour_Edit_GN'
        col_836C0 = box_1A729.column(heading='', align=True)
        col_836C0.alert = False
        col_836C0.enabled = True
        col_836C0.active = True
        col_836C0.use_property_split = False
        col_836C0.use_property_decorate = False
        col_836C0.scale_x = 1.0
        col_836C0.scale_y = 1.0
        col_836C0.alignment = 'Expand'.upper()
        col_836C0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_64F25 = '["' + str('Socket_4' + '"]') 
        col_836C0.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_64F25), text='', icon_value=0, emboss=True)
        attr_F9B60 = '["' + str('Socket_2' + '"]') 
        col_836C0.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_F9B60), text='', icon_value=0, emboss=True)
        if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_4'] == 0) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_4'] == 1)):
            col_A8E1B = col_836C0.column(heading='', align=False)
            col_A8E1B.alert = False
            col_A8E1B.enabled = True
            col_A8E1B.active = True
            col_A8E1B.use_property_split = False
            col_A8E1B.use_property_decorate = False
            col_A8E1B.scale_x = 1.0
            col_A8E1B.scale_y = 1.0
            col_A8E1B.alignment = 'Expand'.upper()
            col_A8E1B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_10C7C = '["' + str('Socket_3' + '"]') 
            col_A8E1B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_10C7C), text='Hue Threshold', icon_value=0, emboss=True)
            attr_8DE4C = '["' + str('Socket_6' + '"]') 
            col_A8E1B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_8DE4C), text='Saturation Threshold', icon_value=0, emboss=True)
            attr_E480B = '["' + str('Socket_7' + '"]') 
            col_A8E1B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_E480B), text='Value Threshold', icon_value=0, emboss=True)
        col_85E9D = box_1A729.column(heading='', align=False)
        col_85E9D.alert = False
        col_85E9D.enabled = True
        col_85E9D.active = True
        col_85E9D.use_property_split = False
        col_85E9D.use_property_decorate = False
        col_85E9D.scale_x = 1.0
        col_85E9D.scale_y = 1.0
        col_85E9D.alignment = 'Expand'.upper()
        col_85E9D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_7F527 = '["' + str('Socket_11' + '"]') 
        col_85E9D.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_7F527), text='Colour Edit Masking', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_11']:
            col_758DD = col_85E9D.column(heading='', align=False)
            col_758DD.alert = False
            col_758DD.enabled = True
            col_758DD.active = True
            col_758DD.use_property_split = False
            col_758DD.use_property_decorate = False
            col_758DD.scale_x = 1.0
            col_758DD.scale_y = 1.0
            col_758DD.alignment = 'Expand'.upper()
            col_758DD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_C4FB4 = '["' + str('Socket_8' + '"]') 
            col_758DD.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_C4FB4), text='', icon_value=0, emboss=True, toggle=True)
            attr_0B7C4 = '["' + str('Socket_9' + '"]') 
            col_758DD.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_0B7C4), text='', icon_value=0, emboss=True, toggle=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_8'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_8'] == 3)):
                attr_4B792 = '["' + str('Socket_12' + '"]') 
                col_758DD.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_4B792), text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_2F40B = layout_function.box()
        box_2F40B.alert = False
        box_2F40B.enabled = 'OBJECT'==bpy.context.mode
        box_2F40B.active = True
        box_2F40B.use_property_split = False
        box_2F40B.use_property_decorate = False
        box_2F40B.alignment = 'Expand'.upper()
        box_2F40B.scale_x = 1.0
        box_2F40B.scale_y = 1.0
        if not True: box_2F40B.operator_context = "EXEC_DEFAULT"
        row_78C95 = box_2F40B.row(heading='', align=False)
        row_78C95.alert = False
        row_78C95.enabled = True
        row_78C95.active = True
        row_78C95.use_property_split = False
        row_78C95.use_property_decorate = False
        row_78C95.scale_x = 1.0
        row_78C95.scale_y = 1.0
        row_78C95.alignment = 'Expand'.upper()
        row_78C95.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_78C95.label(text='Color Edit', icon_value=0)
        op = row_78C95.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Colour_Edit_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Colour_Edit_GN'
