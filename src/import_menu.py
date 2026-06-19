import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_import_menu_94FB1(layout_function, ):
    col_E3544 = layout_function.column(heading='', align=False)
    col_E3544.alert = False
    col_E3544.enabled = True
    col_E3544.active = True
    col_E3544.use_property_split = False
    col_E3544.use_property_decorate = False
    col_E3544.scale_x = 1.0
    col_E3544.scale_y = 1.0
    col_E3544.alignment = 'Expand'.upper()
    col_E3544.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_910F6 = col_E3544.box()
    box_910F6.alert = False
    box_910F6.enabled = True
    box_910F6.active = True
    box_910F6.use_property_split = False
    box_910F6.use_property_decorate = False
    box_910F6.alignment = 'Expand'.upper()
    box_910F6.scale_x = 1.0
    box_910F6.scale_y = 1.0
    if not True: box_910F6.operator_context = "EXEC_DEFAULT"
    row_8F631 = box_910F6.row(heading='Import as: ', align=False)
    row_8F631.alert = False
    row_8F631.enabled = True
    row_8F631.active = True
    row_8F631.use_property_split = False
    row_8F631.use_property_decorate = False
    row_8F631.scale_x = 1.0
    row_8F631.scale_y = 1.0
    row_8F631.alignment = 'Expand'.upper()
    row_8F631.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_8F631.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_face_vert', text=bpy.context.scene.sna_dgs_scene_properties.import_face_vert, icon_value=0, emboss=True, expand=True, toggle=True)
    if (bpy.context.scene.sna_dgs_scene_properties.import_face_vert == 'Faces'):
        box_910F6.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_uv', text='UV Reset', icon_value=0, emboss=True, toggle=False)
    box_910F6.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_proxy', text='Create Proxy Object', icon_value=0, emboss=True, expand=True, toggle=False)
    box_5C3FC = col_E3544.box()
    box_5C3FC.alert = False
    box_5C3FC.enabled = True
    box_5C3FC.active = True
    box_5C3FC.use_property_split = False
    box_5C3FC.use_property_decorate = False
    box_5C3FC.alignment = 'Expand'.upper()
    box_5C3FC.scale_x = 1.0
    box_5C3FC.scale_y = 2.0
    if not True: box_5C3FC.operator_context = "EXEC_DEFAULT"
    op = box_5C3FC.operator('sna.dgs_render_import_ply_e0a3a', text='Import PLY', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'import.svg')), emboss=True, depress=False)
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        box_0AF9B = col_E3544.box()
        box_0AF9B.alert = False
        box_0AF9B.enabled = True
        box_0AF9B.active = True
        box_0AF9B.use_property_split = False
        box_0AF9B.use_property_decorate = False
        box_0AF9B.alignment = 'Expand'.upper()
        box_0AF9B.scale_x = 1.0
        box_0AF9B.scale_y = 1.0
        if not True: box_0AF9B.operator_context = "EXEC_DEFAULT"
        op = box_0AF9B.operator('sna.dgs_render_rotate_for_blender_axes_423de', text='Rotate Active To Blender Axes', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'refresh.svg')), emboss=True, depress=False)
    if bpy.context.preferences.addons[__package__].preferences.sna_show_tips:
        col_9F76F = col_E3544.column(heading='', align=False)
        col_9F76F.alert = False
        col_9F76F.enabled = True
        col_9F76F.active = True
        col_9F76F.use_property_split = False
        col_9F76F.use_property_decorate = False
        col_9F76F.scale_x = 1.0
        col_9F76F.scale_y = 1.0
        col_9F76F.alignment = 'Expand'.upper()
        col_9F76F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_599AC = col_9F76F.box()
        box_599AC.alert = False
        box_599AC.enabled = True
        box_599AC.active = True
        box_599AC.use_property_split = False
        box_599AC.use_property_decorate = False
        box_599AC.alignment = 'Expand'.upper()
        box_599AC.scale_x = 1.0
        box_599AC.scale_y = 1.0
        if not True: box_599AC.operator_context = "EXEC_DEFAULT"
        box_599AC.label(text='Do not apply rotation or scale', icon_value=0)
        box_599AC.label(text="using Blender's native Apply Transforms", icon_value=0)
        box_599AC.label(text="Use the addon's Apply 3DGS Transforms", icon_value=0)
        box_37F67 = col_9F76F.box()
        box_37F67.alert = False
        box_37F67.enabled = True
        box_37F67.active = True
        box_37F67.use_property_split = False
        box_37F67.use_property_decorate = False
        box_37F67.alignment = 'Expand'.upper()
        box_37F67.scale_x = 1.0
        box_37F67.scale_y = 1.0
        if not True: box_37F67.operator_context = "EXEC_DEFAULT"
        box_37F67.label(text='Verts = performance, rigging and ', icon_value=0)
        box_37F67.label(text='visual parity with Render mode results', icon_value=0)
        box_37F67.label(text='Faces = Vertex Painting and fine edits', icon_value=0)
        if (bpy.context.scene.render.engine != 'BLENDER_EEVEE_NEXT'):
            box_3BEA2 = col_9F76F.box()
            box_3BEA2.alert = False
            box_3BEA2.enabled = True
            box_3BEA2.active = True
            box_3BEA2.use_property_split = False
            box_3BEA2.use_property_decorate = False
            box_3BEA2.alignment = 'Expand'.upper()
            box_3BEA2.scale_x = 1.0
            box_3BEA2.scale_y = 1.0
            if not True: box_3BEA2.operator_context = "EXEC_DEFAULT"
            box_3BEA2.label(text='Eevee is recommended', icon_value=0)
