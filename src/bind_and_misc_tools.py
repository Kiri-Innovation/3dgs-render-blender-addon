import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_bind_and_misc_tools_C36C1(layout_function, ):
    box_D0924 = layout_function.box()
    box_D0924.alert = False
    box_D0924.enabled = True
    box_D0924.active = True
    box_D0924.use_property_split = False
    box_D0924.use_property_decorate = False
    box_D0924.alignment = 'Expand'.upper()
    box_D0924.scale_x = 1.0
    box_D0924.scale_y = 1.0
    if not True: box_D0924.operator_context = "EXEC_DEFAULT"
    box_D0924.label(text='Bind', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    box_D0924.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_bind_method', text='', icon_value=0, emboss=True)
    if (bpy.context.scene.sna_dgs_scene_properties.rig_bind_method == 'Hybrid'):
        box_D0924.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_surface_dist_factor', text='Hybrid Distance Factor', icon_value=0, emboss=True)
    box_D0924.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_bind_samples', text='Bind Samples', icon_value=0, emboss=True)
    col_A97C8 = box_D0924.column(heading='', align=False)
    col_A97C8.alert = False
    col_A97C8.enabled = True
    col_A97C8.active = True
    col_A97C8.use_property_split = False
    col_A97C8.use_property_decorate = False
    col_A97C8.scale_x = 1.0
    col_A97C8.scale_y = 2.0
    col_A97C8.alignment = 'Expand'.upper()
    col_A97C8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_A97C8.operator('sna.dgs_render_bind_to_proxy_mesh_6c58f', text='Bind to Proxy Mesh', icon_value=0, emboss=True, depress=False)
