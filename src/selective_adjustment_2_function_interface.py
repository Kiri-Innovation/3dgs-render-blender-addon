import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_wire_effectors import sna_append_wire_effectors_D3038

__package__ = __package__.rsplit('.', 1)[0]


def sna_selective_adjustment_2_function_interface_4A09B(layout_function, ):
    col_3234F = layout_function.column(heading='', align=False)
    col_3234F.alert = False
    col_3234F.enabled = True
    col_3234F.active = True
    col_3234F.use_property_split = False
    col_3234F.use_property_decorate = False
    col_3234F.scale_x = 1.0
    col_3234F.scale_y = 1.0
    col_3234F.alignment = 'Expand'.upper()
    col_3234F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_3234F.label(text='Selective Adjustment 2', icon_value=0)
    col_3234F.separator(factor=1.0)
    attr_8064D = '["' + str('Socket_16' + '"]') 
    col_3234F.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_8064D, text='Enable Selective Colour 2', icon_value=0, emboss=True, toggle=True)
    col_3234F.separator(factor=1.0)
    col_1ACBE = col_3234F.column(heading='', align=False)
    col_1ACBE.alert = False
    col_1ACBE.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_16']
    col_1ACBE.active = True
    col_1ACBE.use_property_split = False
    col_1ACBE.use_property_decorate = False
    col_1ACBE.scale_x = 1.0
    col_1ACBE.scale_y = 1.0
    col_1ACBE.alignment = 'Expand'.upper()
    col_1ACBE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_D327E = col_1ACBE.box()
    box_D327E.alert = False
    box_D327E.enabled = True
    box_D327E.active = True
    box_D327E.use_property_split = False
    box_D327E.use_property_decorate = False
    box_D327E.alignment = 'Expand'.upper()
    box_D327E.scale_x = 1.0
    box_D327E.scale_y = 1.0
    if not True: box_D327E.operator_context = "EXEC_DEFAULT"
    box_D327E.label(text='Selection Type', icon_value=0)
    attr_77E08 = '["' + str('Socket_39' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_77E08, text='', icon_value=0, emboss=True)
    attr_8B0ED = '["' + str('Socket_17' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_8B0ED, text='Selection', icon_value=0, emboss=True)
    attr_084CB = '["' + str('Socket_19' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_084CB, text='Change To', icon_value=0, emboss=True)
    attr_4E141 = '["' + str('Socket_18' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_4E141, text='Colour Threshold', icon_value=0, emboss=True)
    attr_281E6 = '["' + str('Socket_26' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_281E6, text='Saturation Threshold', icon_value=0, emboss=True)
    attr_90794 = '["' + str('Socket_29' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_90794, text='Value Threshold', icon_value=0, emboss=True)
    box_424BC = col_1ACBE.box()
    box_424BC.alert = False
    box_424BC.enabled = True
    box_424BC.active = True
    box_424BC.use_property_split = False
    box_424BC.use_property_decorate = False
    box_424BC.alignment = 'Expand'.upper()
    box_424BC.scale_x = 1.0
    box_424BC.scale_y = 1.0
    if not True: box_424BC.operator_context = "EXEC_DEFAULT"
    box_424BC.label(text='Blend Mode', icon_value=0)
    attr_D9EB5 = '["' + str('Socket_41' + '"]') 
    box_424BC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_D9EB5, text='', icon_value=0, emboss=True)
    attr_08AD5 = '["' + str('Socket_42' + '"]') 
    box_424BC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_08AD5, text='Mix Factor', icon_value=0, emboss=True)
    attr_4668B = '["' + str('Socket_46' + '"]') 
    box_424BC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_4668B, text='Randomise Mix', icon_value=0, emboss=True)
    box_E92EC = col_1ACBE.box()
    box_E92EC.alert = False
    box_E92EC.enabled = True
    box_E92EC.active = True
    box_E92EC.use_property_split = False
    box_E92EC.use_property_decorate = False
    box_E92EC.alignment = 'Expand'.upper()
    box_E92EC.scale_x = 1.0
    box_E92EC.scale_y = 1.0
    if not True: box_E92EC.operator_context = "EXEC_DEFAULT"
    box_E92EC.label(text='Masking', icon_value=0)
    attr_4D4AA = '["' + str('Socket_43' + '"]') 
    box_E92EC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_4D4AA, text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_43']:
        col_25741 = box_E92EC.column(heading='', align=False)
        col_25741.alert = False
        col_25741.enabled = True
        col_25741.active = True
        col_25741.use_property_split = False
        col_25741.use_property_decorate = False
        col_25741.scale_x = 1.0
        col_25741.scale_y = 1.0
        col_25741.alignment = 'Expand'.upper()
        col_25741.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_0F906 = '["' + str('Socket_44' + '"]') 
        col_25741.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_0F906, text='', icon_value=0, emboss=True, toggle=True)
        attr_9AC49 = '["' + str('Socket_45' + '"]') 
        col_25741.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9AC49, text='', icon_value=0, emboss=True, toggle=True)
    layout_function = col_1ACBE
    sna_append_wire_effectors_D3038(layout_function, )
