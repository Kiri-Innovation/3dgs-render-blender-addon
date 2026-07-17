import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .active_3dgs_mesh_object_menu import sna_active_3dgs_mesh_object_menu_9588F
from .edit_menu import sna_edit_menu_D3299
from .mesh_to_3dgs_function_interface import sna_mesh_to_3dgs_function_interface_8DDDC
from .render_new_menu import sna_render_new_menu_66133

__package__ = __package__.rsplit('.', 1)[0]


def sna_dgs_render__main_function_menu_019C7(layout_function, ):
    box_BDC6F = layout_function.box()
    box_BDC6F.alert = False
    box_BDC6F.enabled = True
    box_BDC6F.active = True
    box_BDC6F.use_property_split = False
    box_BDC6F.use_property_decorate = False
    box_BDC6F.alignment = 'Expand'.upper()
    box_BDC6F.scale_x = 1.0
    box_BDC6F.scale_y = 1.0
    if not True: box_BDC6F.operator_context = "EXEC_DEFAULT"
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        if (bpy.context.scene.sna_dgs_scene_properties.active_mode == 'Edit'):
            layout_function = box_BDC6F
            sna_active_3dgs_mesh_object_menu_9588F(layout_function, )
    box_DCCA2 = box_BDC6F.box()
    box_DCCA2.alert = False
    box_DCCA2.enabled = ((not ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop))) and 'OBJECT'==bpy.context.mode)
    box_DCCA2.active = True
    box_DCCA2.use_property_split = False
    box_DCCA2.use_property_decorate = False
    box_DCCA2.alignment = 'Expand'.upper()
    box_DCCA2.scale_x = 1.0
    box_DCCA2.scale_y = 1.0
    if not True: box_DCCA2.operator_context = "EXEC_DEFAULT"
    box_DCCA2.label(text='Active Mode', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    row_A59C6 = box_DCCA2.row(heading='', align=False)
    row_A59C6.alert = False
    row_A59C6.enabled = True
    row_A59C6.active = True
    row_A59C6.use_property_split = False
    row_A59C6.use_property_decorate = False
    row_A59C6.scale_x = 1.0
    row_A59C6.scale_y = 1.0
    row_A59C6.alignment = 'Expand'.upper()
    row_A59C6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_A59C6.prop(bpy.context.scene.sna_dgs_scene_properties, 'active_mode', text=bpy.context.scene.sna_dgs_scene_properties.active_mode, icon_value=0, emboss=True, expand=True)
    if str(bpy.context.scene.sna_dgs_scene_properties.active_mode) == "Edit":
        layout_function = box_BDC6F
        sna_edit_menu_D3299(layout_function, )
    elif str(bpy.context.scene.sna_dgs_scene_properties.active_mode) == "Render":
        layout_function = box_BDC6F
        sna_render_new_menu_66133(layout_function, )
    elif str(bpy.context.scene.sna_dgs_scene_properties.active_mode) == "Mesh 2 3DGS":
        layout_function = box_BDC6F
        sna_mesh_to_3dgs_function_interface_8DDDC(layout_function, )
    else:
        pass
