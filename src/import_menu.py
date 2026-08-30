import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_import_menu_94FB1(layout_function, ):
    col_E3544 = layout_function.column(heading='', align=False)
    box_910F6 = col_E3544.box()
    row_8F631 = box_910F6.row(heading='Import as: ', align=False)
    row_8F631.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_face_vert', text=bpy.context.scene.sna_dgs_scene_properties.import_face_vert, icon_value=0, emboss=True, expand=True, toggle=True)
    if (bpy.context.scene.sna_dgs_scene_properties.import_face_vert == 'Faces'):
        box_910F6.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_uv', text='UV Reset', icon_value=0, emboss=True, toggle=False)
    box_910F6.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_proxy', text='Create Proxy Object', icon_value=0, emboss=True, expand=True, toggle=False)
    box_5C3FC = col_E3544.box()
    box_5C3FC.scale_y = 2.0
    op = box_5C3FC.operator('sna.dgs_render_import_ply_e0a3a', text='Import PLY', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'import.svg')), emboss=True, depress=False)
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        box_0AF9B = col_E3544.box()
        op = box_0AF9B.operator('sna.dgs_render_rotate_for_blender_axes_423de', text='Rotate Active To Blender Axes', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'refresh.svg')), emboss=True, depress=False)
    if bpy.context.preferences.addons[__package__].preferences.sna_show_tips:
        col_9F76F = col_E3544.column(heading='', align=False)
        box_599AC = col_9F76F.box()
        box_599AC.label(text='Do not apply rotation or scale', icon_value=0)
        box_599AC.label(text="using Blender's native Apply Transforms", icon_value=0)
        box_599AC.label(text="Use the addon's Apply 3DGS Transforms", icon_value=0)
        box_37F67 = col_9F76F.box()
        box_37F67.label(text='Verts = performance, rigging and ', icon_value=0)
        box_37F67.label(text='visual parity with Render mode results', icon_value=0)
        box_37F67.label(text='Faces = Vertex Painting and fine edits', icon_value=0)
        if (bpy.context.scene.render.engine != 'BLENDER_EEVEE_NEXT'):
            box_3BEA2 = col_9F76F.box()
            box_3BEA2.label(text='Eevee is recommended', icon_value=0)
