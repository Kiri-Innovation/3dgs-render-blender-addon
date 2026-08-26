import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_decimate_D742E(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Decimate_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_D6E89 = layout_function.box()
        box_D6E89.alert = False
        box_D6E89.enabled = True
        box_D6E89.active = True
        box_D6E89.use_property_split = False
        box_D6E89.use_property_decorate = False
        box_D6E89.alignment = 'Expand'.upper()
        box_D6E89.scale_x = 1.0
        box_D6E89.scale_y = 1.0
        if not True: box_D6E89.operator_context = "EXEC_DEFAULT"
        split_32B05 = box_D6E89.split(factor=0.5, align=False)
        split_32B05.alert = False
        split_32B05.enabled = True
        split_32B05.active = True
        split_32B05.use_property_split = False
        split_32B05.use_property_decorate = False
        split_32B05.scale_x = 1.0
        split_32B05.scale_y = 1.0
        split_32B05.alignment = 'Expand'.upper()
        if not True: split_32B05.operator_context = "EXEC_DEFAULT"
        split_32B05.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], 'show_viewport', text='Decimate', icon_value=0, emboss=True, toggle=True)
        row_3CA54 = split_32B05.row(heading='', align=True)
        row_3CA54.alert = False
        row_3CA54.enabled = True
        row_3CA54.active = True
        row_3CA54.use_property_split = False
        row_3CA54.use_property_decorate = False
        row_3CA54.scale_x = 1.0
        row_3CA54.scale_y = 1.0
        row_3CA54.alignment = 'Right'.upper()
        row_3CA54.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_3CA54.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_3CA54.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Decimate_GN'
        op = row_3CA54.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Decimate_GN'
        col_49D7B = box_D6E89.column(heading='', align=True)
        col_49D7B.alert = False
        col_49D7B.enabled = True
        col_49D7B.active = True
        col_49D7B.use_property_split = False
        col_49D7B.use_property_decorate = False
        col_49D7B.scale_x = 1.0
        col_49D7B.scale_y = 1.0
        col_49D7B.alignment = 'Expand'.upper()
        col_49D7B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_C43B9 = '["' + str('Socket_15' + '"]') 
        col_49D7B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_C43B9), text='Decimate Percentage', icon_value=0, emboss=True)
        attr_97660 = '["' + str('Socket_16' + '"]') 
        col_49D7B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_97660), text='Decimate Seed', icon_value=0, emboss=True)
        col_CB092 = box_D6E89.column(heading='', align=False)
        col_CB092.alert = False
        col_CB092.enabled = True
        col_CB092.active = True
        col_CB092.use_property_split = False
        col_CB092.use_property_decorate = False
        col_CB092.scale_x = 1.0
        col_CB092.scale_y = 1.0
        col_CB092.alignment = 'Expand'.upper()
        col_CB092.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_93B93 = '["' + str('Socket_18' + '"]') 
        col_CB092.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_93B93), text='Decimate Masking', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_18']:
            col_70B17 = col_CB092.column(heading='', align=False)
            col_70B17.alert = False
            col_70B17.enabled = True
            col_70B17.active = True
            col_70B17.use_property_split = False
            col_70B17.use_property_decorate = False
            col_70B17.scale_x = 1.0
            col_70B17.scale_y = 1.0
            col_70B17.alignment = 'Expand'.upper()
            col_70B17.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_B0634 = '["' + str('Socket_20' + '"]') 
            col_70B17.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_B0634), text='', icon_value=0, emboss=True, toggle=True)
            attr_BD569 = '["' + str('Socket_21' + '"]') 
            col_70B17.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_BD569), text='', icon_value=0, emboss=True, toggle=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_20'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_20'] == 3)):
                attr_2288A = '["' + str('Socket_22' + '"]') 
                col_70B17.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_2288A), text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_2EA63 = layout_function.box()
        box_2EA63.alert = False
        box_2EA63.enabled = 'OBJECT'==bpy.context.mode
        box_2EA63.active = True
        box_2EA63.use_property_split = False
        box_2EA63.use_property_decorate = False
        box_2EA63.alignment = 'Expand'.upper()
        box_2EA63.scale_x = 1.0
        box_2EA63.scale_y = 1.0
        if not True: box_2EA63.operator_context = "EXEC_DEFAULT"
        row_DE93F = box_2EA63.row(heading='', align=False)
        row_DE93F.alert = False
        row_DE93F.enabled = True
        row_DE93F.active = True
        row_DE93F.use_property_split = False
        row_DE93F.use_property_decorate = False
        row_DE93F.scale_x = 1.0
        row_DE93F.scale_y = 1.0
        row_DE93F.alignment = 'Expand'.upper()
        row_DE93F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_DE93F.label(text='Decimate', icon_value=0)
        op = row_DE93F.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Decimate_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Decimate_GN'
