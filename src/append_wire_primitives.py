import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_append_wire_primitives_15D73(layout_function, ):
    col_4F908 = layout_function.column(heading='', align=True)
    col_4F908.alert = False
    col_4F908.enabled = True
    col_4F908.active = True
    col_4F908.use_property_split = False
    col_4F908.use_property_decorate = False
    col_4F908.scale_x = 1.0
    col_4F908.scale_y = 1.0
    col_4F908.alignment = 'Expand'.upper()
    col_4F908.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_4F908.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = col_4F908.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)
