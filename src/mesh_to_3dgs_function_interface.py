import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_mesh_to_3dgs_function_interface_8DDDC(layout_function, ):
    if bpy.context.preferences.addons[__package__].preferences.sna_show_tips:
        box_58AE4 = layout_function.box()
        box_58AE4.label(text='Linux and Mac are not supported', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_58AE4.label(text='         The .OBJ mesh must be triangulated', icon_value=0)
        box_58AE4.label(text='         The colour image texture must be', icon_value=0)
        box_58AE4.label(text='         in the same folder as your .OBJ and .MTL', icon_value=0)
    box_9766A = layout_function.box()
    box_9766A.prop(bpy.context.scene.sna_dgs_scene_properties, 'mesh2gs_validate', text='Validate Mesh, Texture and .MTL', icon_value=0, emboss=True)
    box_8C171 = layout_function.box()
    op = box_8C171.operator('sna.dgs_render_mesh23dgs_3dfed', text='Select .OBJ', icon_value=0, emboss=True, depress=False)
