import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_r2_create_menu_03F72(layout_function, ):
    col_1D306 = layout_function.column(heading='', align=False)
    col_1D306.alert = False
    col_1D306.enabled = True
    col_1D306.active = True
    col_1D306.use_property_split = False
    col_1D306.use_property_decorate = False
    col_1D306.scale_x = 1.0
    col_1D306.scale_y = 1.0
    col_1D306.alignment = 'Expand'.upper()
    col_1D306.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_B3EB2 = col_1D306.box()
    box_B3EB2.alert = False
    box_B3EB2.enabled = (not (bpy.context.view_layer.objects.active == None))
    box_B3EB2.active = True
    box_B3EB2.use_property_split = False
    box_B3EB2.use_property_decorate = False
    box_B3EB2.alignment = 'Expand'.upper()
    box_B3EB2.scale_x = 1.0
    box_B3EB2.scale_y = 1.0
    if not True: box_B3EB2.operator_context = "EXEC_DEFAULT"
    op = box_B3EB2.operator('sna.dgs_render_create_proxy_from_mesh_eafbb', text='Create Proxy From Visible Active Object', icon_value=0, emboss=True, depress=False)
    if (bpy.context.view_layer.objects.active == None):
        box_8209B = col_1D306.box()
        box_8209B.alert = False
        box_8209B.enabled = True
        box_8209B.active = True
        box_8209B.use_property_split = False
        box_8209B.use_property_decorate = False
        box_8209B.alignment = 'Expand'.upper()
        box_8209B.scale_x = 1.0
        box_8209B.scale_y = 1.0
        if not True: box_8209B.operator_context = "EXEC_DEFAULT"
        box_8209B.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
