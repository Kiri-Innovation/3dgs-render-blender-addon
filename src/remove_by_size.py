import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_remove_by_size_E1DB7(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Remove_By Size_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_3DF8E = layout_function.box()
        split_52769 = box_3DF8E.split(factor=0.5, align=False)
        split_52769.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], 'show_viewport', text='Remove By Size', icon_value=0, emboss=True, toggle=True)
        row_44648 = split_52769.row(heading='', align=True)
        row_44648.alignment = 'Right'.upper()
        row_44648.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_44648.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Remove_By Size_GN'
        op = row_44648.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Remove_By Size_GN'
        col_51C8C = box_3DF8E.column(heading='', align=True)
        attr_8753D = '["' + str('Socket_18' + '"]') 
        col_51C8C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_8753D), text='Remove:', icon_value=0, emboss=True, toggle=True)
        attr_F212A = '["' + str('Socket_5' + '"]') 
        col_51C8C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_F212A), text='Threshold', icon_value=0, emboss=True, toggle=True)
        col_AA341 = box_3DF8E.column(heading='', align=False)
        attr_12417 = '["' + str('Socket_13' + '"]') 
        col_AA341.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_12417), text='Remove By Size Masking', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_13']:
            col_AF706 = col_AA341.column(heading='', align=False)
            attr_952BC = '["' + str('Socket_15' + '"]') 
            col_AF706.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_952BC), text='', icon_value=0, emboss=True, toggle=True)
            attr_12EC2 = '["' + str('Socket_14' + '"]') 
            col_AF706.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_12EC2), text='', icon_value=0, emboss=True, toggle=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_15'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_15'] == 3)):
                attr_7198E = '["' + str('Socket_16' + '"]') 
                col_AF706.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_7198E), text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_1F29A = layout_function.box()
        box_1F29A.enabled = 'OBJECT'==bpy.context.mode
        row_8BC2D = box_1F29A.row(heading='', align=False)
        row_8BC2D.label(text='Remove By Size', icon_value=0)
        op = row_8BC2D.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Remove_By Size_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Remove_By Size_GN'
