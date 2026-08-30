import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_active_3dgs_mesh_object_menu_9588F(layout_function, ):
    col_33976 = layout_function.column(heading='', align=False)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_1AD2D = col_33976.box()
        col_A4D20 = box_1AD2D.column(heading='', align=False)
        col_247F1 = col_A4D20.column(heading='', align=False)
        col_247F1.label(text='Active 3DGS Mesh Object:', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        row_0AD6D = col_A4D20.row(heading='', align=True)
        box_29E44 = row_0AD6D.box()
        box_29E44.label(text=bpy.context.view_layer.objects.active.name, icon_value=0)
        col_F0A3B = row_0AD6D.column(heading='', align=False)
        col_F0A3B.alert = (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Disable Camera Updates')
        col_F0A3B.scale_y = 1.5
        col_F0A3B.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'update_mode', text='', icon_value=0, emboss=True, toggle=True)
        col_A4D20.separator(factor=1.0)
        if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Enable Camera Updates'):
            if 'EDIT_MESH'==bpy.context.mode:
                if '3DGS_Mesh_Type' in bpy.context.view_layer.objects.active:
                    if (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'):
                        pass
                    else:
                        box_96194 = col_A4D20.box()
                        row_A3F2D = box_96194.row(heading='', align=True)
                        op = row_A3F2D.operator('sna.dgs_render_align_active_to_x_axis_6ae0e', text='X', icon_value=0, emboss=True, depress=False)
                        op = row_A3F2D.operator('sna.dgs_render_align_active_to_y_axis_c305d', text='Y', icon_value=0, emboss=True, depress=False)
                        op = row_A3F2D.operator('sna.dgs_render_align_active_to_z_axis_1e184', text='Z', icon_value=0, emboss=True, depress=False)
            else:
                box_1444A = col_A4D20.box()
                op = box_1444A.operator('sna.dgs_render_align_active_to_view_30b13', text=('Refresh update to camera' if ((bpy.context.scene.camera != None) and bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update) else 'Update Active To View'), icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'eye.svg')), emboss=True, depress=False)
        if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Show As Point Cloud'):
            box_AA375 = col_A4D20.box()
            attr_C8F44 = '["' + str('Socket_51' + '"]') 
            box_AA375.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_C8F44), text='Point Radius', icon_value=0, emboss=True)
            box_AA375.prop_search(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], '["Socket_61"]'), bpy.data, 'materials', text='Material', icon='NONE', item_search_property="name")
        if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Enable Camera Updates'):
            col_75D68 = col_A4D20.column(heading='', align=False)
            if ((bpy.context.scene.camera == None) and bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update):
                box_A3A41 = col_75D68.box()
                box_A3A41.label(text='No Active Camera Found', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            box_21A87 = col_75D68.box()
            box_21A87.alert = bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update
            box_21A87.scale_y = 1.5
            box_21A87.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'cam_update', text='Use Active Camera', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera.svg')), emboss=True, toggle=True)
            if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update and (bpy.context.scene.camera != None) and property_exists("bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_68']", globals(), locals()) and property_exists("None", globals(), locals())):
                col_C389F = col_75D68.column(heading='', align=True)
                box_81D6E = col_C389F.box()
                row_BAB68 = box_81D6E.row(heading='', align=False)
                attr_47247 = '["' + str('Socket_68' + '"]') 
                row_BAB68.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_47247), text='Frustrum Cull (Edit Mode)', icon_value=0, emboss=True)
                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_68']:
                    split_06E70 = row_BAB68.split(factor=0.30000001192092896, align=False)
                    attr_F00D7 = '["' + str('Socket_74' + '"]') 
                    split_06E70.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_F00D7), text='Invert', icon_value=0, emboss=True)
                    attr_D8000 = '["' + str('Socket_63' + '"]') 
                    split_06E70.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_D8000), text='Padding', icon_value=0, emboss=True)
                box_D224C = col_C389F.box()
                row_03A56 = box_D224C.row(heading='', align=False)
                attr_12DA6 = '["' + str('Socket_69' + '"]') 
                row_03A56.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_12DA6), text='Distance Cull (Edit Mode)', icon_value=0, emboss=True)
                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_69']:
                    attr_29452 = '["' + str('Socket_72' + '"]') 
                    row_03A56.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_29452), text='Use Camera Clip Range', icon_value=0, emboss=True)
                if ( not bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_72'] and bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_69']):
                    row_050CC = box_D224C.row(heading='', align=False)
                    attr_47D5F = '["' + str('Socket_70' + '"]') 
                    row_050CC.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_47D5F), text='Near Distance', icon_value=0, emboss=True)
                    attr_05FB6 = '["' + str('Socket_71' + '"]') 
                    row_050CC.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_05FB6), text='Far Distance', icon_value=0, emboss=True)
