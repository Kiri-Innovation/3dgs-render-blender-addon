import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_r2_cleanup_menu_09B59(layout_function, ):
    box_64A1D = layout_function.box()
    box_64A1D.alert = False
    box_64A1D.enabled = True
    box_64A1D.active = True
    box_64A1D.use_property_split = False
    box_64A1D.use_property_decorate = False
    box_64A1D.alignment = 'Expand'.upper()
    box_64A1D.scale_x = 1.0
    box_64A1D.scale_y = 1.0
    if not True: box_64A1D.operator_context = "EXEC_DEFAULT"
    box_64A1D.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_clear_empties', text='Delete All Proxy Empties', icon_value=0, emboss=True)
    op = box_64A1D.operator('sna.dgs_render_clean_up_scene_80052', text='Clean Up Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
