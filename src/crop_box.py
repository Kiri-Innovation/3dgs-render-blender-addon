import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_crop_box_F2C60(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Crop_Box_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_F47C3 = layout_function.box()
        box_F47C3.alert = False
        box_F47C3.enabled = True
        box_F47C3.active = True
        box_F47C3.use_property_split = False
        box_F47C3.use_property_decorate = False
        box_F47C3.alignment = 'Expand'.upper()
        box_F47C3.scale_x = 1.0
        box_F47C3.scale_y = 1.0
        if not True: box_F47C3.operator_context = "EXEC_DEFAULT"
        split_35FA4 = box_F47C3.split(factor=0.5, align=False)
        split_35FA4.alert = False
        split_35FA4.enabled = True
        split_35FA4.active = True
        split_35FA4.use_property_split = False
        split_35FA4.use_property_decorate = False
        split_35FA4.scale_x = 1.0
        split_35FA4.scale_y = 1.0
        split_35FA4.alignment = 'Expand'.upper()
        if not True: split_35FA4.operator_context = "EXEC_DEFAULT"
        split_35FA4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], 'show_viewport', text='Crop Box', icon_value=0, emboss=True, toggle=True)
        row_D8B0A = split_35FA4.row(heading='', align=True)
        row_D8B0A.alert = False
        row_D8B0A.enabled = True
        row_D8B0A.active = True
        row_D8B0A.use_property_split = False
        row_D8B0A.use_property_decorate = False
        row_D8B0A.scale_x = 1.0
        row_D8B0A.scale_y = 1.0
        row_D8B0A.alignment = 'Right'.upper()
        row_D8B0A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_D8B0A.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_D8B0A.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Crop_Box_GN'
        op = row_D8B0A.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Crop_Box_GN'
        box_D7E3D = box_F47C3.box()
        box_D7E3D.alert = False
        box_D7E3D.enabled = True
        box_D7E3D.active = True
        box_D7E3D.use_property_split = False
        box_D7E3D.use_property_decorate = False
        box_D7E3D.alignment = 'Expand'.upper()
        box_D7E3D.scale_x = 1.0
        box_D7E3D.scale_y = 1.0
        if not True: box_D7E3D.operator_context = "EXEC_DEFAULT"
        op = box_D7E3D.operator('sna.dgs_render_auto_generate_crop_object_f20d5', text='Auto generate crop object', icon_value=0, emboss=True, depress=False)
        op.sna_filter_mode = 'quick'
        op.sna_filter_epsilon = 0.029999999329447746
        op.sna_filter_min_points = 10
        op.sna_fast_mode = False
        op.sna_create_convex_hull_object = False
        col_3D26B = box_F47C3.column(heading='', align=True)
        col_3D26B.alert = False
        col_3D26B.enabled = True
        col_3D26B.active = True
        col_3D26B.use_property_split = False
        col_3D26B.use_property_decorate = False
        col_3D26B.scale_x = 1.0
        col_3D26B.scale_y = 1.0
        col_3D26B.alignment = 'Expand'.upper()
        col_3D26B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_75E1E = '["' + str('Socket_19' + '"]') 
        col_3D26B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_75E1E), text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN']['Socket_19'] == 0):
            attr_4C8F9 = '["' + str('Socket_12' + '"]') 
            col_3D26B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_4C8F9), text='', icon_value=0, emboss=True)
        else:
            col_3D26B.prop_search(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], '["Socket_18"]'), bpy.data, 'collections', text='collection', icon='NONE', item_search_property="name")
        attr_5E746 = '["' + str('Socket_15' + '"]') 
        col_3D26B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_5E746), text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN']['Socket_15'] >= 2):
            attr_3021D = '["' + str('Socket_16' + '"]') 
            col_3D26B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_3021D), text='', icon_value=0, emboss=True)
    else:
        box_08D76 = layout_function.box()
        box_08D76.alert = False
        box_08D76.enabled = 'OBJECT'==bpy.context.mode
        box_08D76.active = True
        box_08D76.use_property_split = False
        box_08D76.use_property_decorate = False
        box_08D76.alignment = 'Expand'.upper()
        box_08D76.scale_x = 1.0
        box_08D76.scale_y = 1.0
        if not True: box_08D76.operator_context = "EXEC_DEFAULT"
        row_729E9 = box_08D76.row(heading='', align=False)
        row_729E9.alert = False
        row_729E9.enabled = True
        row_729E9.active = True
        row_729E9.use_property_split = False
        row_729E9.use_property_decorate = False
        row_729E9.scale_x = 1.0
        row_729E9.scale_y = 1.0
        row_729E9.alignment = 'Expand'.upper()
        row_729E9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_729E9.label(text='Crop Box', icon_value=0)
        op = row_729E9.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Crop_Box_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Crop_Box_GN'
