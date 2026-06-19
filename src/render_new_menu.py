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
    box_D20F4.alert = False
    box_D20F4.enabled = (not ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)))
    box_D20F4.active = True
    box_D20F4.use_property_split = False
    box_D20F4.use_property_decorate = False
    box_D20F4.alignment = 'Expand'.upper()
    box_D20F4.scale_x = 1.0
    box_D20F4.scale_y = 1.0
    if not True: box_D20F4.operator_context = "EXEC_DEFAULT"
    grid_DDB98 = box_D20F4.grid_flow(columns=2, row_major=False, even_columns=False, even_rows=False, align=True)
    grid_DDB98.enabled = True
    grid_DDB98.active = True
    grid_DDB98.use_property_split = False
    grid_DDB98.use_property_decorate = False
    grid_DDB98.alignment = 'Expand'.upper()
    grid_DDB98.scale_x = 1.0
    grid_DDB98.scale_y = 1.0
    if not True: grid_DDB98.operator_context = "EXEC_DEFAULT"
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
        col_5A5DB.alert = False
        col_5A5DB.enabled = True
        col_5A5DB.active = True
        col_5A5DB.use_property_split = False
        col_5A5DB.use_property_decorate = False
        col_5A5DB.scale_x = 1.0
        col_5A5DB.scale_y = 1.0
        col_5A5DB.alignment = 'Expand'.upper()
        col_5A5DB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_83499 = col_5A5DB.box()
        box_83499.alert = False
        box_83499.enabled = True
        box_83499.active = True
        box_83499.use_property_split = False
        box_83499.use_property_decorate = False
        box_83499.alignment = 'Expand'.upper()
        box_83499.scale_x = 1.0
        box_83499.scale_y = 1.0
        if not True: box_83499.operator_context = "EXEC_DEFAULT"
        box_83499.label(text='Active Object: ' + bpy.context.view_layer.objects.active.name, icon_value=0)
        layout_function = col_5A5DB
        sna_attribute_adjust_properties_2C323(layout_function, )
