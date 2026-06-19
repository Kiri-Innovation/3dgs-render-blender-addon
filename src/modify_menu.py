import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .adjust_attributes import sna_adjust_attributes_AB643
from .append_wire_primitives import sna_append_wire_primitives_15D73
from .camera_cull import sna_camera_cull_8069C
from .colour_edit import sna_colour_edit_37123
from .convert_to_rough_mesh import sna_convert_to_rough_mesh_BF549
from .crop_box import sna_crop_box_F2C60
from .decimate import sna_decimate_D742E
from .dgs_mods_uv_edit import sna_dgs_mods_uv_edit_7D8A8
from .remove_by_size import sna_remove_by_size_E1DB7

__package__ = __package__.rsplit('.', 1)[0]


def sna_modify_menu_AEA26(layout_function, ):
    box_A4C5D = layout_function.box()
    box_A4C5D.alert = False
    box_A4C5D.enabled = True
    box_A4C5D.active = True
    box_A4C5D.use_property_split = False
    box_A4C5D.use_property_decorate = False
    box_A4C5D.alignment = 'Expand'.upper()
    box_A4C5D.scale_x = 1.0
    box_A4C5D.scale_y = 1.0
    if not True: box_A4C5D.operator_context = "EXEC_DEFAULT"
    op = box_A4C5D.operator('sna.dgs_render_remove_higher_sh_attributes_cb703', text='Remove SH Attributes', icon_value=0, emboss=True, depress=False)
    box_0B550 = layout_function.box()
    box_0B550.alert = False
    box_0B550.enabled = True
    box_0B550.active = True
    box_0B550.use_property_split = False
    box_0B550.use_property_decorate = False
    box_0B550.alignment = 'Expand'.upper()
    box_0B550.scale_x = 1.0
    box_0B550.scale_y = 1.0
    if not True: box_0B550.operator_context = "EXEC_DEFAULT"
    layout_function = box_0B550
    sna_append_wire_primitives_15D73(layout_function, )
    col_5374E = layout_function.column(heading='', align=False)
    col_5374E.alert = False
    col_5374E.enabled = True
    col_5374E.active = True
    col_5374E.use_property_split = False
    col_5374E.use_property_decorate = False
    col_5374E.scale_x = 1.0
    col_5374E.scale_y = 1.0
    col_5374E.alignment = 'Expand'.upper()
    col_5374E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = col_5374E
    sna_camera_cull_8069C(layout_function, )
    layout_function = col_5374E
    sna_decimate_D742E(layout_function, )
    layout_function = col_5374E
    sna_crop_box_F2C60(layout_function, )
    layout_function = col_5374E
    sna_colour_edit_37123(layout_function, )
    layout_function = col_5374E
    sna_remove_by_size_E1DB7(layout_function, )
    layout_function = col_5374E
    sna_convert_to_rough_mesh_BF549(layout_function, )
    layout_function = col_5374E
    sna_adjust_attributes_AB643(layout_function, )
    layout_function = col_5374E
    sna_dgs_mods_uv_edit_7D8A8(layout_function, )
