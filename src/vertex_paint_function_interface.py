import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_wire_effectors import sna_append_wire_effectors_D3038

__package__ = __package__.rsplit('.', 1)[0]


def sna_vertex_paint_function_interface_BEA3E(layout_function, ):
    if (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'):
        box_2FB04 = layout_function.box()
        box_2FB04.label(text='Painting is only available for Face based', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_2FB04.label(text='3DGS objects. You can convert this object', icon_value=0)
        box_2FB04.label(text='from the Ctrl+A menu', icon_value=0)
    col_453E1 = layout_function.column(heading='', align=False)
    col_453E1.enabled = (not (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'))
    col_453E1.label(text='Vertex Painting', icon_value=0)
    col_453E1.separator(factor=1.0)
    attr_C4F4C = '["' + str('Socket_55' + '"]') 
    col_453E1.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C4F4C), text='Enable Vertex Painting', icon_value=0, emboss=True, toggle=True)
    col_453E1.separator(factor=1.0)
    col_86FB7 = col_453E1.column(heading='', align=False)
    col_86FB7.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_55']
    box_2E9CF = col_86FB7.box()
    box_2E9CF.label(text='Painting', icon_value=0)
    if (property_exists("bpy.context.view_layer.objects.active.data.color_attributes", globals(), locals()) and 'KIRI_3DGS_Paint' in bpy.context.view_layer.objects.active.data.color_attributes):
        op = box_2E9CF.operator('sna.dgs_render_start_vertex_painting_a36e0', text='Start Painting', icon_value=0, emboss=True, depress=False)
    else:
        box_ACBF2 = box_2E9CF.box()
        box_ACBF2.label(text='KIRI_3DGS_Paint attribute is missing', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    op = box_2E9CF.operator('sna.dgs_render_refresh__create_paint_attribute_84655', text='Reset Paint', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg')), emboss=True, depress=False)
    box_7E936 = col_86FB7.box()
    box_7E936.label(text='Blend Mode', icon_value=0)
    attr_97713 = '["' + str('Socket_62' + '"]') 
    box_7E936.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_97713), text='', icon_value=0, emboss=True)
    attr_2A320 = '["' + str('Socket_57' + '"]') 
    box_7E936.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_2A320), text='Mix Factor', icon_value=0, emboss=True)
    box_55BC3 = col_86FB7.box()
    box_55BC3.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_64']
    box_55BC3.label(text='Masking', icon_value=0)
    attr_03413 = '["' + str('Socket_64' + '"]') 
    box_55BC3.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_03413), text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_64']:
        col_DC970 = box_55BC3.column(heading='', align=False)
        attr_7340F = '["' + str('Socket_65' + '"]') 
        col_DC970.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_7340F), text='', icon_value=0, emboss=True, toggle=True)
        attr_34BD5 = '["' + str('Socket_66' + '"]') 
        col_DC970.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_34BD5), text='', icon_value=0, emboss=True, toggle=True)
    layout_function = col_86FB7
    sna_append_wire_effectors_D3038(layout_function, )
