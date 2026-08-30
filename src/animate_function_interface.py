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
        split_D18F1 = box_1DAB6.split(factor=0.5, align=False)
        split_D18F1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], 'show_viewport', text='Animate', icon_value=0, emboss=True, toggle=True)
        row_058B1 = split_D18F1.row(heading='', align=True)
        row_058B1.alignment = 'Right'.upper()
        row_058B1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_058B1.operator('sna.dgs_render_apply_animate_modifier_3938e', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_058B1.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Animate_GN'
        col_03A93 = box_1DAB6.column(heading='', align=False)
        box_797F1 = col_03A93.box()
        attr_C6924 = '["' + str('Socket_6' + '"]') 
        box_797F1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_C6924), text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 2):
            pass
        else:
            col_44B28 = box_797F1.column(heading='', align=False)
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
        attr_A68D1 = '["' + str('Socket_37' + '"]') 
        box_3AE7F.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_A68D1), text='Decimate Animated', icon_value=0, emboss=True)
        box_F6C6C = col_03A93.box()
        attr_FEA5B = '["' + str('Socket_26' + '"]') 
        box_F6C6C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FEA5B), text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 1):
            box_6DFC4 = box_F6C6C.box()
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
        box_7D470 = box_B4084.box()
        attr_52B76 = '["' + str('Socket_28' + '"]') 
        box_7D470.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_52B76), text='Enable Noise Displacement', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_28']:
            col_28235 = box_7D470.column(heading='', align=False)
            attr_D3C6D = '["' + str('Socket_7' + '"]') 
            col_28235.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D3C6D), text='Noise Strength', icon_value=0, emboss=True)
            attr_6D7D3 = '["' + str('Socket_8' + '"]') 
            col_28235.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_6D7D3), text='Noise Scale', icon_value=0, emboss=True)
            attr_18DA5 = '["' + str('Socket_4' + '"]') 
            col_28235.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_18DA5), text='Time Evolution Multiplier', icon_value=0, emboss=True)
        box_54317 = box_B4084.box()
        attr_FB923 = '["' + str('Socket_29' + '"]') 
        box_54317.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FB923), text='Enable Voronoi Displacement', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_29']:
            col_E8E24 = box_54317.column(heading='', align=False)
            attr_AEBD9 = '["' + str('Socket_21' + '"]') 
            col_E8E24.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_AEBD9), text='Voronoi Strength', icon_value=0, emboss=True)
            attr_D761F = '["' + str('Socket_20' + '"]') 
            col_E8E24.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D761F), text='Voronoi Scale', icon_value=0, emboss=True)
            attr_6054A = '["' + str('Socket_22' + '"]') 
            col_E8E24.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_6054A), text='Time Evolution Multiplier', icon_value=0, emboss=True)
        box_554D7 = col_03A93.box()
        box_E2A8B = box_554D7.box()
        attr_FE6FE = '["' + str('Socket_41' + '"]') 
        box_E2A8B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FE6FE), text='Enable Pixelate', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_41']:
            col_5DE3D = box_E2A8B.column(heading='', align=False)
            attr_0E515 = '["' + str('Socket_40' + '"]') 
            col_5DE3D.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_0E515), text='Pixelate Mix', icon_value=0, emboss=True)
            attr_9C041 = '["' + str('Socket_39' + '"]') 
            col_5DE3D.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_9C041), text='Grid Scale', icon_value=0, emboss=True)
    else:
        box_F44AB = layout_function.box()
        box_F44AB.enabled = 'OBJECT'==bpy.context.mode
        row_07DA9 = box_F44AB.row(heading='', align=False)
        row_07DA9.label(text='Animate', icon_value=0)
        op = row_07DA9.operator('sna.dgs_render_add_animate_modifier_39c55', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
