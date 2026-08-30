import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_convert_to_rough_mesh_BF549(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Convert_To_Rough_Mesh_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_F10CF = layout_function.box()
        split_CD9F1 = box_F10CF.split(factor=0.5, align=False)
        split_CD9F1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], 'show_viewport', text='Convert To Rough Mesh', icon_value=0, emboss=True, toggle=True)
        row_9D884 = split_CD9F1.row(heading='', align=True)
        row_9D884.alignment = 'Right'.upper()
        row_9D884.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_9D884.operator('sna.dgs_render_apply_modifier_0f5f2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Convert_To_Rough_Mesh_GN'
        op = row_9D884.operator('sna.dgs_render_remove_modifier_9cf0d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        op.sna_target_object = bpy.context.view_layer.objects.active.name
        op.sna_target_modifier = 'KIRI_3DGS_Convert_To_Rough_Mesh_GN'
        col_D3A3B = box_F10CF.column(heading='', align=False)
        attr_8B7BC = '["' + str('Socket_3' + '"]') 
        col_D3A3B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_8B7BC), text='Voxel Amount', icon_value=0, emboss=True, toggle=True)
        attr_A4FBE = '["' + str('Socket_4' + '"]') 
        col_D3A3B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_A4FBE), text='Voxel Threshold', icon_value=0, emboss=True, toggle=True)
        attr_47308 = '["' + str('Socket_7' + '"]') 
        col_D3A3B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_47308), text='Simplify', icon_value=0, emboss=True, toggle=True)
        attr_F2260 = '["' + str('Socket_6' + '"]') 
        col_D3A3B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_F2260), text='Smoothing', icon_value=0, emboss=True, toggle=True)
        attr_C0C06 = '["' + str('Socket_9' + '"]') 
        col_D3A3B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_C0C06), text='Point Volume Radius', icon_value=0, emboss=True, toggle=True)
        attr_6E61B = '["' + str('Socket_11' + '"]') 
        col_D3A3B.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_6E61B), text='Filter Islands', icon_value=0, emboss=True, toggle=False)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN']['Socket_11']:
            col_B8A6E = col_D3A3B.column(heading='', align=False)
            attr_65366 = '["' + str('Socket_12' + '"]') 
            col_B8A6E.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_65366), text='', icon_value=0, emboss=True, toggle=False)
            attr_0DE62 = '["' + str('Socket_10' + '"]') 
            col_B8A6E.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_0DE62), text='Island Threshold', icon_value=0, emboss=True, toggle=False)
    else:
        box_8332A = layout_function.box()
        box_8332A.enabled = 'OBJECT'==bpy.context.mode
        row_A4E6D = box_8332A.row(heading='', align=False)
        row_A4E6D.label(text='Convert To Rough Mesh', icon_value=0)
        op = row_A4E6D.operator('sna.dgs_render_append_rough_mesh_modifier_65da3', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_create_duplicate = True
