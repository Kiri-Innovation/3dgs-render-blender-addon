import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_wire_primitives import sna_append_wire_primitives_15D73

__package__ = __package__.rsplit('.', 1)[0]


def sna_edit_select_tools_D0175(layout_function, ):
    box_DC33F = layout_function.box()
    box_DC33F.label(text='Select Tools', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    box_243AA = box_DC33F.box()
    box_243AA.label(text='Select by Object', icon_value=0)
    layout_function = box_243AA
    sna_append_wire_primitives_15D73(layout_function, )
    box_243AA.prop(bpy.context.scene.sna_dgs_scene_properties, 'select_select_by_obj', text='', icon_value=0, emboss=True)
    row_187F8 = box_243AA.row(heading='', align=False)
    row_187F8.prop(bpy.context.scene.sna_dgs_scene_properties, 'select_obj_select_mode', text=bpy.context.scene.sna_dgs_scene_properties.select_obj_select_mode, icon_value=0, emboss=True, expand=True)
    op = box_243AA.operator('sna.dgs_render_select_by_object_92f9c', text='Select', icon_value=0, emboss=True, depress=False)
    box_2DF89 = box_DC33F.box()
    box_2DF89.label(text='Select by attribute', icon_value=0)
    box_2DF89.prop(bpy.context.scene.sna_dgs_scene_properties, 'select_attribute_type', text=bpy.context.scene.sna_dgs_scene_properties.select_attribute_type, icon_value=0, emboss=True, expand=True)
    op = box_2DF89.operator('sna.dgs_render_attribute_select_51c86', text='Select', icon_value=0, emboss=True, depress=False)
    op.sna_scale_target_attr = 'scale_combined'
    op.sna_scale_factor = 0.8999999761581421
    op.sna_scale_compare = 'GREATER'
    op.sna_rot_target_euler = (0.0, 0.0, 0.0)
    op.sna_rot_tolerance_deg = 5.0
    op.sna_rot_compare = 'EQUAL'
