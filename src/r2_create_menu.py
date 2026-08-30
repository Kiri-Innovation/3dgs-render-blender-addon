import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_r2_create_menu_03F72(layout_function, ):
    col_1D306 = layout_function.column(heading='', align=False)
    box_B3EB2 = col_1D306.box()
    box_B3EB2.enabled = (not (bpy.context.view_layer.objects.active == None))
    op = box_B3EB2.operator('sna.dgs_render_create_proxy_from_mesh_eafbb', text='Create Proxy From Visible Active Object', icon_value=0, emboss=True, depress=False)
    if (bpy.context.view_layer.objects.active == None):
        box_8209B = col_1D306.box()
        box_8209B.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
