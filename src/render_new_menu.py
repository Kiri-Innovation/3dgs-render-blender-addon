import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .attribute_adjust_properties import sna_attribute_adjust_properties_2C323
from .r2_cleanup_menu import sna_r2_cleanup_menu_09B59
from .r2_create_menu import sna_r2_create_menu_03F72
from .r2_render_menu import sna_r2_render_menu_7AD0F
from .r2_update_menu import sna_r2_update_menu_6A492

__package__ = __package__.rsplit('.', 1)[0]


def sna_render_new_menu_66133(layout_function, ):
    box_D20F4 = layout_function.box()
    box_D20F4.enabled = (not ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)))
    grid_DDB98 = box_D20F4.grid_flow(columns=2, row_major=False, even_columns=False, even_rows=False, align=True)
    grid_DDB98.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_main_mode', text=bpy.context.scene.sna_dgs_scene_properties.r2_main_mode, icon_value=0, emboss=True, expand=True)
    if bpy.context.scene.sna_dgs_scene_properties.r2_main_mode == "Update":
        layout_function = layout_function
        sna_r2_update_menu_6A492(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.r2_main_mode == "Create":
        layout_function = layout_function
        sna_r2_create_menu_03F72(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.r2_main_mode == "Render":
        layout_function = layout_function
        sna_r2_render_menu_7AD0F(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.r2_main_mode == "Clean Up":
        layout_function = layout_function
        sna_r2_cleanup_menu_09B59(layout_function, )
    else:
        pass
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Attributes_GN' in bpy.context.view_layer.objects.active.modifiers):
        col_5A5DB = layout_function.column(heading='', align=False)
        box_83499 = col_5A5DB.box()
        box_83499.label(text='Active Object: ' + bpy.context.view_layer.objects.active.name, icon_value=0)
        layout_function = col_5A5DB
        sna_attribute_adjust_properties_2C323(layout_function, )
