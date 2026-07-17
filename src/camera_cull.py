import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_camera_cull_8069C(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Camera_Cull_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_7279D = layout_function.box()
        box_7279D.alert = False
        box_7279D.enabled = True
        box_7279D.active = True
        box_7279D.use_property_split = False
        box_7279D.use_property_decorate = False
        box_7279D.alignment = 'Expand'.upper()
        box_7279D.scale_x = 1.0
        box_7279D.scale_y = 1.0
        if not True: box_7279D.operator_context = "EXEC_DEFAULT"
        split_D5A9B = box_7279D.split(factor=0.5, align=False)
        split_D5A9B.alert = False
        split_D5A9B.enabled = True
        split_D5A9B.active = True
        split_D5A9B.use_property_split = False
        split_D5A9B.use_property_decorate = False
        split_D5A9B.scale_x = 1.0
        split_D5A9B.scale_y = 1.0
        split_D5A9B.alignment = 'Expand'.upper()
        if not True: split_D5A9B.operator_context = "EXEC_DEFAULT"
        split_D5A9B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], 'show_viewport', text='Camera Cull', icon_value=0, emboss=True, toggle=True)
        row_F9B38 = split_D5A9B.row(heading='', align=True)
        row_F9B38.alert = False
        row_F9B38.enabled = True
        row_F9B38.active = True
        row_F9B38.use_property_split = False
        row_F9B38.use_property_decorate = False
        row_F9B38.scale_x = 1.0
        row_F9B38.scale_y = 1.0
        row_F9B38.alignment = 'Right'.upper()
        row_F9B38.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_F9B38.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_F9B38.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Camera_Cull_GN'
        op = row_F9B38.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Camera_Cull_GN'
        if (bpy.context.scene.camera == None):
            box_07B9F = box_7279D.box()
            box_07B9F.alert = False
            box_07B9F.enabled = True
            box_07B9F.active = True
            box_07B9F.use_property_split = False
            box_07B9F.use_property_decorate = False
            box_07B9F.alignment = 'Expand'.upper()
            box_07B9F.scale_x = 1.0
            box_07B9F.scale_y = 1.0
            if not True: box_07B9F.operator_context = "EXEC_DEFAULT"
            box_07B9F.label(text='No Active Camera In Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        else:
            col_A2A21 = box_7279D.column(heading='', align=True)
            col_A2A21.alert = False
            col_A2A21.enabled = True
            col_A2A21.active = True
            col_A2A21.use_property_split = False
            col_A2A21.use_property_decorate = False
            col_A2A21.scale_x = 1.0
            col_A2A21.scale_y = 1.0
            col_A2A21.alignment = 'Expand'.upper()
            col_A2A21.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_A2A21.operator('sna.dgs_render_auto_set_up_camera_cull_properties_aef48', text='Auto Set Up', icon_value=0, emboss=True, depress=False)
            attr_31E14 = '["' + str('Socket_2' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_31E14, text='X Resolution', icon_value=0, emboss=True)
            attr_626D2 = '["' + str('Socket_3' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_626D2, text='Y Resolution', icon_value=0, emboss=True)
            attr_A688C = '["' + str('Socket_4' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_A688C, text='Focal Length', icon_value=0, emboss=True)
            attr_CC516 = '["' + str('Socket_5' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_CC516, text='Sensor Width', icon_value=0, emboss=True)
            attr_7333B = '["' + str('Socket_6' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_7333B, text='Padding', icon_value=0, emboss=True)
            attr_34623 = '["' + str('Socket_13' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_34623, text='Closer Than', icon_value=0, emboss=True)
            attr_45049 = '["' + str('Socket_14' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_45049, text='Further Than', icon_value=0, emboss=True)
    else:
        box_05674 = layout_function.box()
        box_05674.alert = False
        box_05674.enabled = 'OBJECT'==bpy.context.mode
        box_05674.active = True
        box_05674.use_property_split = False
        box_05674.use_property_decorate = False
        box_05674.alignment = 'Expand'.upper()
        box_05674.scale_x = 1.0
        box_05674.scale_y = 1.0
        if not True: box_05674.operator_context = "EXEC_DEFAULT"
        row_B29D4 = box_05674.row(heading='', align=False)
        row_B29D4.alert = False
        row_B29D4.enabled = True
        row_B29D4.active = True
        row_B29D4.use_property_split = False
        row_B29D4.use_property_decorate = False
        row_B29D4.scale_x = 1.0
        row_B29D4.scale_y = 1.0
        row_B29D4.alignment = 'Expand'.upper()
        row_B29D4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_B29D4.label(text='Camera Cull', icon_value=0)
        op = row_B29D4.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Camera_Cull_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Camera_Cull_GN'
