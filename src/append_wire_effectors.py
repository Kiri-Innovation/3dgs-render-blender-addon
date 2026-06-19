import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_append_wire_effectors_D3038(layout_function, ):
    box_C9715 = layout_function.box()
    box_C9715.alert = False
    box_C9715.enabled = True
    box_C9715.active = True
    box_C9715.use_property_split = False
    box_C9715.use_property_decorate = False
    box_C9715.alignment = 'Expand'.upper()
    box_C9715.scale_x = 1.0
    box_C9715.scale_y = 1.0
    if not True: box_C9715.operator_context = "EXEC_DEFAULT"
    op = box_C9715.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = box_C9715.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)
