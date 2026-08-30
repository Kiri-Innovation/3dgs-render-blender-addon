import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_wire_effectors import sna_append_wire_effectors_D3038

__package__ = __package__.rsplit('.', 1)[0]


def sna_selective_adjustment_3_function_interface_69C53(layout_function, ):
    col_CF5CE = layout_function.column(heading='', align=False)
    col_CF5CE.label(text='Selective Adjustment 3', icon_value=0)
    col_CF5CE.separator(factor=1.0)
    attr_2E4D3 = '["' + str('Socket_23' + '"]') 
    col_CF5CE.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_2E4D3), text='Enable Selective Colour 3', icon_value=0, emboss=True, toggle=True)
    col_CF5CE.separator(factor=1.0)
    col_E631B = col_CF5CE.column(heading='', align=False)
    col_E631B.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_23']
    box_2DDC1 = col_E631B.box()
    box_2DDC1.label(text='Selection Type', icon_value=0)
    attr_C53D8 = '["' + str('Socket_40' + '"]') 
    box_2DDC1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C53D8), text='', icon_value=0, emboss=True)
    attr_A4E8F = '["' + str('Socket_20' + '"]') 
    box_2DDC1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_A4E8F), text='Selection', icon_value=0, emboss=True)
    attr_AFCF0 = '["' + str('Socket_22' + '"]') 
    box_2DDC1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_AFCF0), text='Change To', icon_value=0, emboss=True)
    attr_4CA6F = '["' + str('Socket_21' + '"]') 
    box_2DDC1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_4CA6F), text='Colour Threshold', icon_value=0, emboss=True)
    attr_B934F = '["' + str('Socket_27' + '"]') 
    box_2DDC1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_B934F), text='Saturation Threshold', icon_value=0, emboss=True)
    attr_B4B30 = '["' + str('Socket_30' + '"]') 
    box_2DDC1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_B4B30), text='Value Threshold', icon_value=0, emboss=True)
    box_D5CAB = col_E631B.box()
    box_D5CAB.label(text='Blend Mode', icon_value=0)
    attr_7153A = '["' + str('Socket_47' + '"]') 
    box_D5CAB.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_7153A), text='', icon_value=0, emboss=True)
    attr_FFE12 = '["' + str('Socket_48' + '"]') 
    box_D5CAB.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_FFE12), text='Mix Factor', icon_value=0, emboss=True)
    attr_C7965 = '["' + str('Socket_52' + '"]') 
    box_D5CAB.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C7965), text='Randomise Mix', icon_value=0, emboss=True)
    box_E6B78 = col_E631B.box()
    box_E6B78.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_49']
    box_E6B78.label(text='Masking', icon_value=0)
    attr_24D06 = '["' + str('Socket_49' + '"]') 
    box_E6B78.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_24D06), text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_49']:
        col_E9291 = box_E6B78.column(heading='', align=False)
        attr_3DC41 = '["' + str('Socket_50' + '"]') 
        col_E9291.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_3DC41), text='', icon_value=0, emboss=True, toggle=True)
        attr_020BD = '["' + str('Socket_51' + '"]') 
        col_E9291.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_020BD), text='', icon_value=0, emboss=True, toggle=True)
    layout_function = col_E631B
    sna_append_wire_effectors_D3038(layout_function, )
