import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_decimate_D742E(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Decimate_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_D6E89 = layout_function.box()
        split_32B05 = box_D6E89.split(factor=0.5, align=False)
        split_32B05.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], 'show_viewport', text='Decimate', icon_value=0, emboss=True, toggle=True)
        row_3CA54 = split_32B05.row(heading='', align=True)
        row_3CA54.alignment = 'Right'.upper()
        row_3CA54.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_3CA54.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Decimate_GN'
        op = row_3CA54.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Decimate_GN'
        col_49D7B = box_D6E89.column(heading='', align=True)
        attr_C43B9 = '["' + str('Socket_15' + '"]') 
        col_49D7B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_C43B9), text='Decimate Percentage', icon_value=0, emboss=True)
        attr_97660 = '["' + str('Socket_16' + '"]') 
        col_49D7B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_97660), text='Decimate Seed', icon_value=0, emboss=True)
        col_CB092 = box_D6E89.column(heading='', align=False)
        attr_93B93 = '["' + str('Socket_18' + '"]') 
        col_CB092.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_93B93), text='Decimate Masking', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_18']:
            col_70B17 = col_CB092.column(heading='', align=False)
            attr_B0634 = '["' + str('Socket_20' + '"]') 
            col_70B17.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_B0634), text='', icon_value=0, emboss=True, toggle=True)
            attr_BD569 = '["' + str('Socket_21' + '"]') 
            col_70B17.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_BD569), text='', icon_value=0, emboss=True, toggle=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_20'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_20'] == 3)):
                attr_2288A = '["' + str('Socket_22' + '"]') 
                col_70B17.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_2288A), text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_2EA63 = layout_function.box()
        box_2EA63.enabled = 'OBJECT'==bpy.context.mode
        row_DE93F = box_2EA63.row(heading='', align=False)
        row_DE93F.label(text='Decimate', icon_value=0)
        op = row_DE93F.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Decimate_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Decimate_GN'
