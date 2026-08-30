import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_wire_effectors import sna_append_wire_effectors_D3038

__package__ = __package__.rsplit('.', 1)[0]


def sna_selective_adjustment_1_function_interface_AD57C(layout_function, ):
    col_8C182 = layout_function.column(heading='', align=False)
    col_8C182.label(text='Selective Adjustment 1', icon_value=0)
    col_8C182.separator(factor=1.0)
    attr_8071F = '["' + str('Socket_10' + '"]') 
    col_8C182.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_8071F), text='Enable Selective Colour 1', icon_value=0, emboss=True, toggle=True)
    col_8C182.separator(factor=1.0)
    col_B3736 = col_8C182.column(heading='', align=False)
    col_B3736.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_10']
    box_98D42 = col_B3736.box()
    box_98D42.label(text='Selection Type', icon_value=0)
    attr_8D909 = '["' + str('Socket_24' + '"]') 
    box_98D42.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_8D909), text='', icon_value=0, emboss=True)
    attr_34C57 = '["' + str('Socket_7' + '"]') 
    box_98D42.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_34C57), text='Selection', icon_value=0, emboss=True)
    attr_AA353 = '["' + str('Socket_9' + '"]') 
    box_98D42.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_AA353), text='Change To', icon_value=0, emboss=True)
    attr_A5076 = '["' + str('Socket_8' + '"]') 
    box_98D42.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_A5076), text='Colour Threshold', icon_value=0, emboss=True)
    attr_82487 = '["' + str('Socket_25' + '"]') 
    box_98D42.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_82487), text='Saturation Threshold', icon_value=0, emboss=True)
    attr_0164F = '["' + str('Socket_28' + '"]') 
    box_98D42.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_0164F), text='Value Threshold', icon_value=0, emboss=True)
    box_067A3 = col_B3736.box()
    box_067A3.label(text='Blend Mode', icon_value=0)
    attr_F9F7E = '["' + str('Socket_31' + '"]') 
    box_067A3.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_F9F7E), text='', icon_value=0, emboss=True)
    attr_D1562 = '["' + str('Socket_32' + '"]') 
    box_067A3.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_D1562), text='Mix Factor', icon_value=0, emboss=True)
    attr_BFCE5 = '["' + str('Socket_36' + '"]') 
    box_067A3.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_BFCE5), text='Randomise Mix', icon_value=0, emboss=True)
    box_3ED76 = col_B3736.box()
    box_3ED76.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_33']
    box_3ED76.label(text='Masking', icon_value=0)
    attr_74E93 = '["' + str('Socket_33' + '"]') 
    box_3ED76.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_74E93), text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_33']:
        col_29C70 = box_3ED76.column(heading='', align=False)
        attr_6C86C = '["' + str('Socket_35' + '"]') 
        col_29C70.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_6C86C), text='', icon_value=0, emboss=True, toggle=True)
        attr_1D6B4 = '["' + str('Socket_34' + '"]') 
        col_29C70.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_1D6B4), text='', icon_value=0, emboss=True, toggle=True)
    layout_function = col_B3736
    sna_append_wire_effectors_D3038(layout_function, )
