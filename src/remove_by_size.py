import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_remove_by_size_E1DB7(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Remove_By Size_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_3DF8E = layout_function.box()
        box_3DF8E.alert = False
        box_3DF8E.enabled = True
        box_3DF8E.active = True
        box_3DF8E.use_property_split = False
        box_3DF8E.use_property_decorate = False
        box_3DF8E.alignment = 'Expand'.upper()
        box_3DF8E.scale_x = 1.0
        box_3DF8E.scale_y = 1.0
        if not True: box_3DF8E.operator_context = "EXEC_DEFAULT"
        split_52769 = box_3DF8E.split(factor=0.5, align=False)
        split_52769.alert = False
        split_52769.enabled = True
        split_52769.active = True
        split_52769.use_property_split = False
        split_52769.use_property_decorate = False
        split_52769.scale_x = 1.0
        split_52769.scale_y = 1.0
        split_52769.alignment = 'Expand'.upper()
        if not True: split_52769.operator_context = "EXEC_DEFAULT"
        split_52769.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], 'show_viewport', text='Remove By Size', icon_value=0, emboss=True, toggle=True)
        row_44648 = split_52769.row(heading='', align=True)
        row_44648.alert = False
        row_44648.enabled = True
        row_44648.active = True
        row_44648.use_property_split = False
        row_44648.use_property_decorate = False
        row_44648.scale_x = 1.0
        row_44648.scale_y = 1.0
        row_44648.alignment = 'Right'.upper()
        row_44648.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_44648.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_44648.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Remove_By Size_GN'
        op = row_44648.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Remove_By Size_GN'
        col_51C8C = box_3DF8E.column(heading='', align=True)
        col_51C8C.alert = False
        col_51C8C.enabled = True
        col_51C8C.active = True
        col_51C8C.use_property_split = False
        col_51C8C.use_property_decorate = False
        col_51C8C.scale_x = 1.0
        col_51C8C.scale_y = 1.0
        col_51C8C.alignment = 'Expand'.upper()
        col_51C8C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_8753D = '["' + str('Socket_18' + '"]') 
        col_51C8C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_8753D, text='Remove:', icon_value=0, emboss=True, toggle=True)
        attr_F212A = '["' + str('Socket_5' + '"]') 
        col_51C8C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_F212A, text='Threshold', icon_value=0, emboss=True, toggle=True)
        col_AA341 = box_3DF8E.column(heading='', align=False)
        col_AA341.alert = False
        col_AA341.enabled = True
        col_AA341.active = True
        col_AA341.use_property_split = False
        col_AA341.use_property_decorate = False
        col_AA341.scale_x = 1.0
        col_AA341.scale_y = 1.0
        col_AA341.alignment = 'Expand'.upper()
        col_AA341.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_12417 = '["' + str('Socket_13' + '"]') 
        col_AA341.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_12417, text='Remove By Size Masking', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_13']:
            col_AF706 = col_AA341.column(heading='', align=False)
            col_AF706.alert = False
            col_AF706.enabled = True
            col_AF706.active = True
            col_AF706.use_property_split = False
            col_AF706.use_property_decorate = False
            col_AF706.scale_x = 1.0
            col_AF706.scale_y = 1.0
            col_AF706.alignment = 'Expand'.upper()
            col_AF706.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_952BC = '["' + str('Socket_15' + '"]') 
            col_AF706.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_952BC, text='', icon_value=0, emboss=True, toggle=True)
            attr_12EC2 = '["' + str('Socket_14' + '"]') 
            col_AF706.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_12EC2, text='', icon_value=0, emboss=True, toggle=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_15'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_15'] == 3)):
                attr_7198E = '["' + str('Socket_16' + '"]') 
                col_AF706.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_7198E, text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_1F29A = layout_function.box()
        box_1F29A.alert = False
        box_1F29A.enabled = 'OBJECT'==bpy.context.mode
        box_1F29A.active = True
        box_1F29A.use_property_split = False
        box_1F29A.use_property_decorate = False
        box_1F29A.alignment = 'Expand'.upper()
        box_1F29A.scale_x = 1.0
        box_1F29A.scale_y = 1.0
        if not True: box_1F29A.operator_context = "EXEC_DEFAULT"
        row_8BC2D = box_1F29A.row(heading='', align=False)
        row_8BC2D.alert = False
        row_8BC2D.enabled = True
        row_8BC2D.active = True
        row_8BC2D.use_property_split = False
        row_8BC2D.use_property_decorate = False
        row_8BC2D.scale_x = 1.0
        row_8BC2D.scale_y = 1.0
        row_8BC2D.alignment = 'Expand'.upper()
        row_8BC2D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_8BC2D.label(text='Remove By Size', icon_value=0)
        op = row_8BC2D.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Remove_By Size_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Remove_By Size_GN'
