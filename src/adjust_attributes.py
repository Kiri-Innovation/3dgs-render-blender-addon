import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .attribute_adjust_properties import sna_attribute_adjust_properties_2C323

__package__ = __package__.rsplit('.', 1)[0]


def sna_adjust_attributes_AB643(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Attributes_GN' in bpy.context.view_layer.objects.active.modifiers):
        col_15AC3 = layout_function.column(heading='', align=False)
        col_15AC3.alert = False
        col_15AC3.enabled = True
        col_15AC3.active = True
        col_15AC3.use_property_split = False
        col_15AC3.use_property_decorate = False
        col_15AC3.scale_x = 1.0
        col_15AC3.scale_y = 1.0
        col_15AC3.alignment = 'Expand'.upper()
        col_15AC3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        layout_function = col_15AC3
        sna_attribute_adjust_properties_2C323(layout_function, )
        box_6671A = col_15AC3.box()
        box_6671A.alert = False
        box_6671A.enabled = True
        box_6671A.active = True
        box_6671A.use_property_split = False
        box_6671A.use_property_decorate = False
        box_6671A.alignment = 'Expand'.upper()
        box_6671A.scale_x = 1.0
        box_6671A.scale_y = 1.0
        if not True: box_6671A.operator_context = "EXEC_DEFAULT"
        box_6671A.label(text='Accurate value changes may only ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_6671A.label(text='be visible in Render mode and external', icon_value=0)
        box_6671A.label(text='3DGS viewers. This modifier will show in', icon_value=0)
        box_6671A.label(text='Render mode for the active object.', icon_value=0)
    else:
        box_6555D = layout_function.box()
        box_6555D.alert = False
        box_6555D.enabled = 'OBJECT'==bpy.context.mode
        box_6555D.active = True
        box_6555D.use_property_split = False
        box_6555D.use_property_decorate = False
        box_6555D.alignment = 'Expand'.upper()
        box_6555D.scale_x = 1.0
        box_6555D.scale_y = 1.0
        if not True: box_6555D.operator_context = "EXEC_DEFAULT"
        row_220DB = box_6555D.row(heading='', align=False)
        row_220DB.alert = False
        row_220DB.enabled = True
        row_220DB.active = True
        row_220DB.use_property_split = False
        row_220DB.use_property_decorate = False
        row_220DB.scale_x = 1.0
        row_220DB.scale_y = 1.0
        row_220DB.alignment = 'Expand'.upper()
        row_220DB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_220DB.label(text='Adjust Attributes', icon_value=0)
        op = row_220DB.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Adjust_Attributes_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Adjust_Attributes_GN'
