import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .image_overlay_function_interface import sna_image_overlay_function_interface_64796
from .selective_adjustment_1_function_interface import sna_selective_adjustment_1_function_interface_AD57C
from .selective_adjustment_2_function_interface import sna_selective_adjustment_2_function_interface_4A09B
from .selective_adjustment_3_function_interface import sna_selective_adjustment_3_function_interface_69C53
from .vertex_paint_function_interface import sna_vertex_paint_function_interface_BEA3E

__package__ = __package__.rsplit('.', 1)[0]


def sna_colour_function_interface_3A6A5(layout_function, ):
    col_EB8EB = layout_function.column(heading='', align=False)
    box_E0430 = col_EB8EB.box()
    attr_17916 = '["' + str('Socket_54' + '"]') 
    box_E0430.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_17916), text='Shadeless', icon_value=0, emboss=True, toggle=False)
    attr_787E3 = '["' + str('Socket_71' + '"]') 
    box_E0430.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_787E3), text='Create Extra Attributes', icon_value=0, emboss=True, toggle=False)
    col_EB8EB.separator(factor=1.0)
    box_47A8F = col_EB8EB.box()
    col_89B6E = box_47A8F.column(heading='', align=True)
    attr_032D8 = '["' + str('Socket_6' + '"]') 
    col_89B6E.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_032D8), text='Brightness', icon_value=0, emboss=True)
    attr_18662 = '["' + str('Socket_2' + '"]') 
    col_89B6E.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_18662), text='Contrast', icon_value=0, emboss=True)
    attr_000D9 = '["' + str('Socket_4' + '"]') 
    col_89B6E.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_000D9), text='Hue', icon_value=0, emboss=True)
    attr_9DF33 = '["' + str('Socket_3' + '"]') 
    col_89B6E.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9DF33), text='Saturation', icon_value=0, emboss=True)
    col_EB8EB.separator(factor=1.0)
    box_A85FA = col_EB8EB.box()
    box_A85FA.label(text='Active Colour Menu', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    box_A85FA.prop(bpy.context.scene.sna_dgs_scene_properties, 'shading_menu', text=bpy.context.scene.sna_dgs_scene_properties.shading_menu, icon_value=0, emboss=True, expand=True)
    col_EB8EB.separator(factor=1.0)
    if bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Selective 1":
        layout_function = col_EB8EB
        sna_selective_adjustment_1_function_interface_AD57C(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Selective 2":
        layout_function = col_EB8EB
        sna_selective_adjustment_2_function_interface_4A09B(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Selective 3":
        layout_function = col_EB8EB
        sna_selective_adjustment_3_function_interface_69C53(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Vertex Paint":
        layout_function = col_EB8EB
        sna_vertex_paint_function_interface_BEA3E(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Image Overlay":
        layout_function = col_EB8EB
        sna_image_overlay_function_interface_64796(layout_function, )
    else:
        pass
