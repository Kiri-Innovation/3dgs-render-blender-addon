import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_wire_effectors import sna_append_wire_effectors_D3038

__package__ = __package__.rsplit('.', 1)[0]


def sna_image_overlay_function_interface_64796(layout_function, ):
    col_D492B = layout_function.column(heading='', align=False)
    col_D492B.label(text='Image Overlay', icon_value=0)
    col_D492B.separator(factor=1.0)
    attr_F9567 = '["' + str('Socket_56' + '"]') 
    col_D492B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_F9567), text='Enable Image Overlay', icon_value=0, emboss=True, toggle=True)
    col_D492B.separator(factor=1.0)
    col_FC5C4 = col_D492B.column(heading='', align=False)
    col_FC5C4.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_56']
    box_61F2D = col_FC5C4.box()
    row_4E69D = box_61F2D.row(heading='', align=False)
    row_4E69D.prop_search(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], '["Socket_60"]'), bpy.data, 'images', text='', icon='NONE', item_search_property="name")
    op = row_4E69D.operator('sna.dgs_render_import_image_overlay_4a457', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'folder.svg')), emboss=True, depress=False)
    box_EA447 = col_FC5C4.box()
    box_EA447.label(text='Blend Mode', icon_value=0)
    attr_9DFC4 = '["' + str('Socket_63' + '"]') 
    box_EA447.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9DFC4), text='', icon_value=0, emboss=True)
    attr_7BFD4 = '["' + str('Socket_61' + '"]') 
    box_EA447.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_7BFD4), text='Mix Factor', icon_value=0, emboss=True)
    box_CABC3 = col_FC5C4.box()
    box_CABC3.label(text='Image Mapping', icon_value=0)
    attr_1EE7F = '["' + str('Socket_76' + '"]') 
    box_CABC3.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_1EE7F), text='', icon_value=0, emboss=True)
    if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_76'] == 0) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_76'] == 2)):
        box_3B9C8 = col_FC5C4.box()
        attr_1C59C = '["' + str('Socket_82' + '"]') 
        box_3B9C8.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_1C59C), text='Location', icon_value=0, emboss=True)
        attr_18E1F = '["' + str('Socket_74' + '"]') 
        box_3B9C8.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_18E1F), text='Rotation', icon_value=0, emboss=True)
        attr_C764D = '["' + str('Socket_83' + '"]') 
        box_3B9C8.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C764D), text='Scale', icon_value=0, emboss=True)
    if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_76'] == 1):
        box_A6BCF = col_FC5C4.box()
        box_A6BCF.label(text='Mapping Object', icon_value=0)
        attr_47BD3 = '["' + str('Socket_77' + '"]') 
        box_A6BCF.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_47BD3), text='', icon_value=0, emboss=True)
    box_8D0CD = col_FC5C4.box()
    box_8D0CD.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_67']
    box_8D0CD.label(text='Masking', icon_value=0)
    attr_145C4 = '["' + str('Socket_67' + '"]') 
    box_8D0CD.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_145C4), text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_67']:
        col_D2C3C = box_8D0CD.column(heading='', align=False)
        attr_67BF4 = '["' + str('Socket_68' + '"]') 
        col_D2C3C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_67BF4), text='', icon_value=0, emboss=True, toggle=True)
        attr_9154D = '["' + str('Socket_69' + '"]') 
        col_D2C3C.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9154D), text='', icon_value=0, emboss=True, toggle=True)
    layout_function = col_FC5C4
    sna_append_wire_effectors_D3038(layout_function, )
