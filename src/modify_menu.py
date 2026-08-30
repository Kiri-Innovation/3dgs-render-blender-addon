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
    op = box_A4C5D.operator('sna.dgs_render_remove_higher_sh_attributes_cb703', text='Remove SH Attributes', icon_value=0, emboss=True, depress=False)
    box_0B550 = layout_function.box()
    layout_function = box_0B550
    sna_append_wire_primitives_15D73(layout_function, )
    col_5374E = layout_function.column(heading='', align=False)
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
