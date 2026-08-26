import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_wire_primitives import sna_append_wire_primitives_15D73

__package__ = __package__.rsplit('.', 1)[0]


def sna_animate_function_interface_57F9E(layout_function, ):
    layout_function = layout_function
    sna_append_wire_primitives_15D73(layout_function, )
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Animate_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_1DAB6 = layout_function.box()
        box_1DAB6.alert = False
        box_1DAB6.enabled = True
        box_1DAB6.active = True
        box_1DAB6.use_property_split = False
        box_1DAB6.use_property_decorate = False
        box_1DAB6.alignment = 'Expand'.upper()
        box_1DAB6.scale_x = 1.0
        box_1DAB6.scale_y = 1.0
        if not True: box_1DAB6.operator_context = "EXEC_DEFAULT"
        split_D18F1 = box_1DAB6.split(factor=0.5, align=False)
        split_D18F1.alert = False
        split_D18F1.enabled = True
        split_D18F1.active = True
        split_D18F1.use_property_split = False
        split_D18F1.use_property_decorate = False
        split_D18F1.scale_x = 1.0
        split_D18F1.scale_y = 1.0
        split_D18F1.alignment = 'Expand'.upper()
        if not True: split_D18F1.operator_context = "EXEC_DEFAULT"
        split_D18F1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], 'show_viewport', text='Animate', icon_value=0, emboss=True, toggle=True)
        row_058B1 = split_D18F1.row(heading='', align=True)
        row_058B1.alert = False
        row_058B1.enabled = True
        row_058B1.active = True
        row_058B1.use_property_split = False
        row_058B1.use_property_decorate = False
        row_058B1.scale_x = 1.0
        row_058B1.scale_y = 1.0
        row_058B1.alignment = 'Right'.upper()
        row_058B1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_058B1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_058B1.operator('sna.dgs_render_apply_animate_modifier_3938e', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_058B1.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Animate_GN'
        col_03A93 = box_1DAB6.column(heading='', align=False)
        col_03A93.alert = False
        col_03A93.enabled = True
        col_03A93.active = True
        col_03A93.use_property_split = False
        col_03A93.use_property_decorate = False
        col_03A93.scale_x = 1.0
        col_03A93.scale_y = 1.0
        col_03A93.alignment = 'Expand'.upper()
        col_03A93.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_797F1 = col_03A93.box()
        box_797F1.alert = False
        box_797F1.enabled = True
        box_797F1.active = True
        box_797F1.use_property_split = False
        box_797F1.use_property_decorate = False
        box_797F1.alignment = 'Expand'.upper()
        box_797F1.scale_x = 1.0
        box_797F1.scale_y = 1.0
        if not True: box_797F1.operator_context = "EXEC_DEFAULT"
        attr_C6924 = '["' + str('Socket_6' + '"]') 
        box_797F1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_C6924), text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 2):
            pass
        else:
            col_44B28 = box_797F1.column(heading='', align=False)
            col_44B28.alert = False
            col_44B28.enabled = True
            col_44B28.active = True
            col_44B28.use_property_split = False
            col_44B28.use_property_decorate = False
            col_44B28.scale_x = 1.0
            col_44B28.scale_y = 1.0
            col_44B28.alignment = 'Expand'.upper()
            col_44B28.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 0):
                attr_3F944 = '["' + str('Socket_2' + '"]') 
                col_44B28.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_3F944), text='', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 0):
                pass
            else:
                col_44B28.prop_search(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_5"]'), bpy.context.scene.collection, 'children', text='', icon='NONE', item_search_property="name")
            attr_D5EE1 = '["' + str('Socket_3' + '"]') 
            col_44B28.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D5EE1), text='Distance Threshold', icon_value=0, emboss=True)
        box_3AE7F = col_03A93.box()
        box_3AE7F.alert = False
        box_3AE7F.enabled = True
        box_3AE7F.active = True
        box_3AE7F.use_property_split = False
        box_3AE7F.use_property_decorate = False
        box_3AE7F.alignment = 'Expand'.upper()
        box_3AE7F.scale_x = 1.0
        box_3AE7F.scale_y = 1.0
        if not True: box_3AE7F.operator_context = "EXEC_DEFAULT"
        attr_A68D1 = '["' + str('Socket_37' + '"]') 
        box_3AE7F.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_A68D1), text='Decimate Animated', icon_value=0, emboss=True)
        box_F6C6C = col_03A93.box()
        box_F6C6C.alert = False
        box_F6C6C.enabled = True
        box_F6C6C.active = True
        box_F6C6C.use_property_split = False
        box_F6C6C.use_property_decorate = False
        box_F6C6C.alignment = 'Expand'.upper()
        box_F6C6C.scale_x = 1.0
        box_F6C6C.scale_y = 1.0
        if not True: box_F6C6C.operator_context = "EXEC_DEFAULT"
        attr_FEA5B = '["' + str('Socket_26' + '"]') 
        box_F6C6C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FEA5B), text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 1):
            box_6DFC4 = box_F6C6C.box()
            box_6DFC4.alert = False
            box_6DFC4.enabled = True
            box_6DFC4.active = True
            box_6DFC4.use_property_split = False
            box_6DFC4.use_property_decorate = False
            box_6DFC4.alignment = 'Expand'.upper()
            box_6DFC4.scale_x = 1.0
            box_6DFC4.scale_y = 1.0
            if not True: box_6DFC4.operator_context = "EXEC_DEFAULT"
            box_6DFC4.prop_search(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_44"]'), bpy.data, 'materials', text='Material', icon='NONE', item_search_property="name")
            attr_55AA7 = '["' + str('Socket_9' + '"]') 
            box_6DFC4.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_55AA7), text='Point Min Radius', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 2):
                pass
            else:
                attr_A5ADF = '["' + str('Socket_10' + '"]') 
                box_6DFC4.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_A5ADF), text='Point Max Radius', icon_value=0, emboss=True)
            attr_D7ABF = '["' + str('Socket_11' + '"]') 
            box_6DFC4.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D7ABF), text='Random Mix', icon_value=0, emboss=True)
            attr_9A7E1 = '["' + str('Socket_12' + '"]') 
            box_6DFC4.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_9A7E1), text='Random Multiplier', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 2):
            box_91071 = box_F6C6C.box()
            box_91071.alert = False
            box_91071.enabled = True
            box_91071.active = True
            box_91071.use_property_split = False
            box_91071.use_property_decorate = False
            box_91071.alignment = 'Expand'.upper()
            box_91071.scale_x = 1.0
            box_91071.scale_y = 1.0
            if not True: box_91071.operator_context = "EXEC_DEFAULT"
            box_91071.prop_search(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_44"]'), bpy.data, 'materials', text='Material', icon='NONE', item_search_property="name")
            attr_F4993 = '["' + str('Socket_38' + '"]') 
            box_91071.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_F4993), text='Curve Length', icon_value=0, emboss=True)
            attr_070CD = '["' + str('Socket_31' + '"]') 
            box_91071.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_070CD), text='Curve Min Radius', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 2):
                pass
            else:
                attr_BA37E = '["' + str('Socket_32' + '"]') 
                box_91071.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_BA37E), text='Curve Max Radius', icon_value=0, emboss=True)
            attr_0D707 = '["' + str('Socket_33' + '"]') 
            box_91071.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_0D707), text='Random Mix', icon_value=0, emboss=True)
            attr_53122 = '["' + str('Socket_34' + '"]') 
            box_91071.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_53122), text='Random Multiplier', icon_value=0, emboss=True)
        box_B4084 = col_03A93.box()
        box_B4084.alert = False
        box_B4084.enabled = True
        box_B4084.active = True
        box_B4084.use_property_split = False
        box_B4084.use_property_decorate = False
        box_B4084.alignment = 'Expand'.upper()
        box_B4084.scale_x = 1.0
        box_B4084.scale_y = 1.0
        if not True: box_B4084.operator_context = "EXEC_DEFAULT"
        box_7D470 = box_B4084.box()
        box_7D470.alert = False
        box_7D470.enabled = True
        box_7D470.active = True
        box_7D470.use_property_split = False
        box_7D470.use_property_decorate = False
        box_7D470.alignment = 'Expand'.upper()
        box_7D470.scale_x = 1.0
        box_7D470.scale_y = 1.0
        if not True: box_7D470.operator_context = "EXEC_DEFAULT"
        attr_52B76 = '["' + str('Socket_28' + '"]') 
        box_7D470.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_52B76), text='Enable Noise Displacement', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_28']:
            col_28235 = box_7D470.column(heading='', align=False)
            col_28235.alert = False
            col_28235.enabled = True
            col_28235.active = True
            col_28235.use_property_split = False
            col_28235.use_property_decorate = False
            col_28235.scale_x = 1.0
            col_28235.scale_y = 1.0
            col_28235.alignment = 'Expand'.upper()
            col_28235.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_D3C6D = '["' + str('Socket_7' + '"]') 
            col_28235.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D3C6D), text='Noise Strength', icon_value=0, emboss=True)
            attr_6D7D3 = '["' + str('Socket_8' + '"]') 
            col_28235.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_6D7D3), text='Noise Scale', icon_value=0, emboss=True)
            attr_18DA5 = '["' + str('Socket_4' + '"]') 
            col_28235.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_18DA5), text='Time Evolution Multiplier', icon_value=0, emboss=True)
        box_54317 = box_B4084.box()
        box_54317.alert = False
        box_54317.enabled = True
        box_54317.active = True
        box_54317.use_property_split = False
        box_54317.use_property_decorate = False
        box_54317.alignment = 'Expand'.upper()
        box_54317.scale_x = 1.0
        box_54317.scale_y = 1.0
        if not True: box_54317.operator_context = "EXEC_DEFAULT"
        attr_FB923 = '["' + str('Socket_29' + '"]') 
        box_54317.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FB923), text='Enable Voronoi Displacement', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_29']:
            col_E8E24 = box_54317.column(heading='', align=False)
            col_E8E24.alert = False
            col_E8E24.enabled = True
            col_E8E24.active = True
            col_E8E24.use_property_split = False
            col_E8E24.use_property_decorate = False
            col_E8E24.scale_x = 1.0
            col_E8E24.scale_y = 1.0
            col_E8E24.alignment = 'Expand'.upper()
            col_E8E24.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_AEBD9 = '["' + str('Socket_21' + '"]') 
            col_E8E24.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_AEBD9), text='Voronoi Strength', icon_value=0, emboss=True)
            attr_D761F = '["' + str('Socket_20' + '"]') 
            col_E8E24.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D761F), text='Voronoi Scale', icon_value=0, emboss=True)
            attr_6054A = '["' + str('Socket_22' + '"]') 
            col_E8E24.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_6054A), text='Time Evolution Multiplier', icon_value=0, emboss=True)
        box_554D7 = col_03A93.box()
        box_554D7.alert = False
        box_554D7.enabled = True
        box_554D7.active = True
        box_554D7.use_property_split = False
        box_554D7.use_property_decorate = False
        box_554D7.alignment = 'Expand'.upper()
        box_554D7.scale_x = 1.0
        box_554D7.scale_y = 1.0
        if not True: box_554D7.operator_context = "EXEC_DEFAULT"
        box_E2A8B = box_554D7.box()
        box_E2A8B.alert = False
        box_E2A8B.enabled = True
        box_E2A8B.active = True
        box_E2A8B.use_property_split = False
        box_E2A8B.use_property_decorate = False
        box_E2A8B.alignment = 'Expand'.upper()
        box_E2A8B.scale_x = 1.0
        box_E2A8B.scale_y = 1.0
        if not True: box_E2A8B.operator_context = "EXEC_DEFAULT"
        attr_FE6FE = '["' + str('Socket_41' + '"]') 
        box_E2A8B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FE6FE), text='Enable Pixelate', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_41']:
            col_5DE3D = box_E2A8B.column(heading='', align=False)
            col_5DE3D.alert = False
            col_5DE3D.enabled = True
            col_5DE3D.active = True
            col_5DE3D.use_property_split = False
            col_5DE3D.use_property_decorate = False
            col_5DE3D.scale_x = 1.0
            col_5DE3D.scale_y = 1.0
            col_5DE3D.alignment = 'Expand'.upper()
            col_5DE3D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_0E515 = '["' + str('Socket_40' + '"]') 
            col_5DE3D.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_0E515), text='Pixelate Mix', icon_value=0, emboss=True)
            attr_9C041 = '["' + str('Socket_39' + '"]') 
            col_5DE3D.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_9C041), text='Grid Scale', icon_value=0, emboss=True)
    else:
        box_F44AB = layout_function.box()
        box_F44AB.alert = False
        box_F44AB.enabled = 'OBJECT'==bpy.context.mode
        box_F44AB.active = True
        box_F44AB.use_property_split = False
        box_F44AB.use_property_decorate = False
        box_F44AB.alignment = 'Expand'.upper()
        box_F44AB.scale_x = 1.0
        box_F44AB.scale_y = 1.0
        if not True: box_F44AB.operator_context = "EXEC_DEFAULT"
        row_07DA9 = box_F44AB.row(heading='', align=False)
        row_07DA9.alert = False
        row_07DA9.enabled = True
        row_07DA9.active = True
        row_07DA9.use_property_split = False
        row_07DA9.use_property_decorate = False
        row_07DA9.scale_x = 1.0
        row_07DA9.scale_y = 1.0
        row_07DA9.alignment = 'Expand'.upper()
        row_07DA9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_07DA9.label(text='Animate', icon_value=0)
        op = row_07DA9.operator('sna.dgs_render_add_animate_modifier_39c55', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
