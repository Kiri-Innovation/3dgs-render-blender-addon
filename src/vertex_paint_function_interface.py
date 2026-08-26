import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_wire_effectors import sna_append_wire_effectors_D3038

__package__ = __package__.rsplit('.', 1)[0]


def sna_vertex_paint_function_interface_BEA3E(layout_function, ):
    if (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'):
        box_2FB04 = layout_function.box()
        box_2FB04.alert = True
        box_2FB04.enabled = True
        box_2FB04.active = True
        box_2FB04.use_property_split = False
        box_2FB04.use_property_decorate = False
        box_2FB04.alignment = 'Expand'.upper()
        box_2FB04.scale_x = 1.0
        box_2FB04.scale_y = 1.0
        if not True: box_2FB04.operator_context = "EXEC_DEFAULT"
        box_2FB04.label(text='Painting is only available for Face based', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_2FB04.label(text='3DGS objects. You can convert this object', icon_value=0)
        box_2FB04.label(text='from the Ctrl+A menu', icon_value=0)
    col_453E1 = layout_function.column(heading='', align=False)
    col_453E1.alert = False
    col_453E1.enabled = (not (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'))
    col_453E1.active = True
    col_453E1.use_property_split = False
    col_453E1.use_property_decorate = False
    col_453E1.scale_x = 1.0
    col_453E1.scale_y = 1.0
    col_453E1.alignment = 'Expand'.upper()
    col_453E1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_453E1.label(text='Vertex Painting', icon_value=0)
    col_453E1.separator(factor=1.0)
    attr_C4F4C = '["' + str('Socket_55' + '"]') 
    col_453E1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C4F4C), text='Enable Vertex Painting', icon_value=0, emboss=True, toggle=True)
    col_453E1.separator(factor=1.0)
    col_86FB7 = col_453E1.column(heading='', align=False)
    col_86FB7.alert = False
    col_86FB7.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_55']
    col_86FB7.active = True
    col_86FB7.use_property_split = False
    col_86FB7.use_property_decorate = False
    col_86FB7.scale_x = 1.0
    col_86FB7.scale_y = 1.0
    col_86FB7.alignment = 'Expand'.upper()
    col_86FB7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_2E9CF = col_86FB7.box()
    box_2E9CF.alert = False
    box_2E9CF.enabled = True
    box_2E9CF.active = True
    box_2E9CF.use_property_split = False
    box_2E9CF.use_property_decorate = False
    box_2E9CF.alignment = 'Expand'.upper()
    box_2E9CF.scale_x = 1.0
    box_2E9CF.scale_y = 1.0
    if not True: box_2E9CF.operator_context = "EXEC_DEFAULT"
    box_2E9CF.label(text='Painting', icon_value=0)
    if (property_exists("bpy.context.view_layer.objects.active.data.color_attributes", globals(), locals()) and 'KIRI_3DGS_Paint' in bpy.context.view_layer.objects.active.data.color_attributes):
        op = box_2E9CF.operator('sna.dgs_render_start_vertex_painting_a36e0', text='Start Painting', icon_value=0, emboss=True, depress=False)
    else:
        box_ACBF2 = box_2E9CF.box()
        box_ACBF2.alert = False
        box_ACBF2.enabled = True
        box_ACBF2.active = True
        box_ACBF2.use_property_split = False
        box_ACBF2.use_property_decorate = False
        box_ACBF2.alignment = 'Expand'.upper()
        box_ACBF2.scale_x = 1.0
        box_ACBF2.scale_y = 1.0
        if not True: box_ACBF2.operator_context = "EXEC_DEFAULT"
        box_ACBF2.label(text='KIRI_3DGS_Paint attribute is missing', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    op = box_2E9CF.operator('sna.dgs_render_refresh__create_paint_attribute_84655', text='Reset Paint', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg')), emboss=True, depress=False)
    box_7E936 = col_86FB7.box()
    box_7E936.alert = False
    box_7E936.enabled = True
    box_7E936.active = True
    box_7E936.use_property_split = False
    box_7E936.use_property_decorate = False
    box_7E936.alignment = 'Expand'.upper()
    box_7E936.scale_x = 1.0
    box_7E936.scale_y = 1.0
    if not True: box_7E936.operator_context = "EXEC_DEFAULT"
    box_7E936.label(text='Blend Mode', icon_value=0)
    attr_97713 = '["' + str('Socket_62' + '"]') 
    box_7E936.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_97713), text='', icon_value=0, emboss=True)
    attr_2A320 = '["' + str('Socket_57' + '"]') 
    box_7E936.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_2A320), text='Mix Factor', icon_value=0, emboss=True)
    box_55BC3 = col_86FB7.box()
    box_55BC3.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_64']
    box_55BC3.enabled = True
    box_55BC3.active = True
    box_55BC3.use_property_split = False
    box_55BC3.use_property_decorate = False
    box_55BC3.alignment = 'Expand'.upper()
    box_55BC3.scale_x = 1.0
    box_55BC3.scale_y = 1.0
    if not True: box_55BC3.operator_context = "EXEC_DEFAULT"
    box_55BC3.label(text='Masking', icon_value=0)
    attr_03413 = '["' + str('Socket_64' + '"]') 
    box_55BC3.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_03413), text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_64']:
        col_DC970 = box_55BC3.column(heading='', align=False)
        col_DC970.alert = False
        col_DC970.enabled = True
        col_DC970.active = True
        col_DC970.use_property_split = False
        col_DC970.use_property_decorate = False
        col_DC970.scale_x = 1.0
        col_DC970.scale_y = 1.0
        col_DC970.alignment = 'Expand'.upper()
        col_DC970.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_7340F = '["' + str('Socket_65' + '"]') 
        col_DC970.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_7340F), text='', icon_value=0, emboss=True, toggle=True)
        attr_34BD5 = '["' + str('Socket_66' + '"]') 
        col_DC970.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_34BD5), text='', icon_value=0, emboss=True, toggle=True)
    layout_function = col_86FB7
    sna_append_wire_effectors_D3038(layout_function, )
