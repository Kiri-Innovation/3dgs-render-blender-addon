import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_export_3dgs_function_interface_CDF59(layout_function, ):
    if bpy.context.preferences.addons[__package__].preferences.sna_show_tips:
        box_9553E = layout_function.box()
        box_9553E.alert = False
        box_9553E.enabled = True
        box_9553E.active = True
        box_9553E.use_property_split = False
        box_9553E.use_property_decorate = False
        box_9553E.alignment = 'Expand'.upper()
        box_9553E.scale_x = 1.0
        box_9553E.scale_y = 1.0
        if not True: box_9553E.operator_context = "EXEC_DEFAULT"
        box_9553E.label(text='If you have applied scale or rotation', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_9553E.label(text="using Blender's native Apply Transform,", icon_value=0)
        box_9553E.label(text='3DGS attributes will be corrupted', icon_value=0)
    row_0B94F = layout_function.row(heading='', align=False)
    row_0B94F.alert = False
    row_0B94F.enabled = True
    row_0B94F.active = True
    row_0B94F.use_property_split = False
    row_0B94F.use_property_decorate = False
    row_0B94F.scale_x = 1.0
    row_0B94F.scale_y = 1.0
    row_0B94F.alignment = 'Expand'.upper()
    row_0B94F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_0B94F.prop(bpy.context.scene.sna_dgs_scene_properties, 'export_single_or_sequence', text=bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence, icon_value=0, emboss=True, expand=True)
    col_11CDA = layout_function.column(heading='', align=False)
    col_11CDA.alert = False
    col_11CDA.enabled = True
    col_11CDA.active = True
    col_11CDA.use_property_split = False
    col_11CDA.use_property_decorate = False
    col_11CDA.scale_x = 1.0
    col_11CDA.scale_y = 1.0
    col_11CDA.alignment = 'Expand'.upper()
    col_11CDA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_11CDA.label(text='Output Directory', icon_value=0)
    col_11CDA.prop(bpy.context.scene.sna_dgs_scene_properties, 'export_output_path', text='', icon_value=0, emboss=True)
    if bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == "3DGS":
        layout_function.prop(bpy.context.scene.sna_dgs_scene_properties, 'export_suffix', text='suffix', icon_value=0, emboss=True)
    elif bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == "4DGS":
        row_1B925 = layout_function.row(heading='', align=False)
        row_1B925.alert = False
        row_1B925.enabled = True
        row_1B925.active = True
        row_1B925.use_property_split = False
        row_1B925.use_property_decorate = False
        row_1B925.scale_x = 1.0
        row_1B925.scale_y = 1.0
        row_1B925.alignment = 'Expand'.upper()
        row_1B925.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_1B925.label(text='Rig Behaviour', icon_value=0)
        row_1B925.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_render_rig_cache_mode', text='', icon_value=0, emboss=True)
    else:
        pass
    col_AA350 = layout_function.column(heading='', align=False)
    col_AA350.alert = False
    col_AA350.enabled = ('OBJECT'==bpy.context.mode and (bpy.context.scene.sna_dgs_scene_properties.export_output_path != ''))
    col_AA350.active = True
    col_AA350.use_property_split = False
    col_AA350.use_property_decorate = False
    col_AA350.scale_x = 1.0
    col_AA350.scale_y = 1.0
    col_AA350.alignment = 'Expand'.upper()
    col_AA350.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == "3DGS":
        col_41DA9 = col_AA350.column(heading='', align=False)
        col_41DA9.alert = False
        col_41DA9.enabled = True
        col_41DA9.active = True
        col_41DA9.use_property_split = False
        col_41DA9.use_property_decorate = False
        col_41DA9.scale_x = 1.0
        col_41DA9.scale_y = 2.0
        col_41DA9.alignment = 'Expand'.upper()
        col_41DA9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_41DA9.operator('sna.dgs_render_export_mesh_as_3dgs4dgs_ce2f7', text='Export 3DGS', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'export.svg')), emboss=True, depress=False)
        op.sna_send_to_world_centre = False
    elif bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == "4DGS":
        col_8AE14 = col_AA350.column(heading='', align=False)
        col_8AE14.alert = False
        col_8AE14.enabled = True
        col_8AE14.active = True
        col_8AE14.use_property_split = False
        col_8AE14.use_property_decorate = False
        col_8AE14.scale_x = 1.0
        col_8AE14.scale_y = 2.0
        col_8AE14.alignment = 'Expand'.upper()
        col_8AE14.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_8AE14.operator('sna.dgs_render_export_mesh_as_3dgs4dgs_ce2f7', text='Export PLY Sequence', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'export.svg')), emboss=True, depress=False)
        op.sna_send_to_world_centre = False
    else:
        pass
    op = col_AA350.operator('sna.dgs_render_open_output_folder_82000', text='Open Output Folder', icon_value=0, emboss=True, depress=False)
    op.sna_path = bpy.context.scene.sna_dgs_scene_properties.export_output_path
