import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_active_3dgs_mesh_object_menu_9588F(layout_function, ):
    col_33976 = layout_function.column(heading='', align=False)
    col_33976.alert = False
    col_33976.enabled = True
    col_33976.active = True
    col_33976.use_property_split = False
    col_33976.use_property_decorate = False
    col_33976.scale_x = 1.0
    col_33976.scale_y = 1.0
    col_33976.alignment = 'Expand'.upper()
    col_33976.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_1AD2D = col_33976.box()
        box_1AD2D.alert = False
        box_1AD2D.enabled = True
        box_1AD2D.active = True
        box_1AD2D.use_property_split = False
        box_1AD2D.use_property_decorate = False
        box_1AD2D.alignment = 'Expand'.upper()
        box_1AD2D.scale_x = 1.0
        box_1AD2D.scale_y = 1.0
        if not True: box_1AD2D.operator_context = "EXEC_DEFAULT"
        col_A4D20 = box_1AD2D.column(heading='', align=False)
        col_A4D20.alert = False
        col_A4D20.enabled = True
        col_A4D20.active = True
        col_A4D20.use_property_split = False
        col_A4D20.use_property_decorate = False
        col_A4D20.scale_x = 1.0
        col_A4D20.scale_y = 1.0
        col_A4D20.alignment = 'Expand'.upper()
        col_A4D20.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_247F1 = col_A4D20.column(heading='', align=False)
        col_247F1.alert = False
        col_247F1.enabled = True
        col_247F1.active = True
        col_247F1.use_property_split = False
        col_247F1.use_property_decorate = False
        col_247F1.scale_x = 1.0
        col_247F1.scale_y = 1.0
        col_247F1.alignment = 'Expand'.upper()
        col_247F1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_247F1.label(text='Active 3DGS Mesh Object:', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
        row_0AD6D = col_A4D20.row(heading='', align=True)
        row_0AD6D.alert = False
        row_0AD6D.enabled = True
        row_0AD6D.active = True
        row_0AD6D.use_property_split = False
        row_0AD6D.use_property_decorate = False
        row_0AD6D.scale_x = 1.0
        row_0AD6D.scale_y = 1.0
        row_0AD6D.alignment = 'Expand'.upper()
        row_0AD6D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_29E44 = row_0AD6D.box()
        box_29E44.alert = False
        box_29E44.enabled = True
        box_29E44.active = True
        box_29E44.use_property_split = False
        box_29E44.use_property_decorate = False
        box_29E44.alignment = 'Expand'.upper()
        box_29E44.scale_x = 1.0
        box_29E44.scale_y = 1.0
        if not True: box_29E44.operator_context = "EXEC_DEFAULT"
        box_29E44.label(text=bpy.context.view_layer.objects.active.name, icon_value=0)
        col_F0A3B = row_0AD6D.column(heading='', align=False)
        col_F0A3B.alert = (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Disable Camera Updates')
        col_F0A3B.enabled = True
        col_F0A3B.active = True
        col_F0A3B.use_property_split = False
        col_F0A3B.use_property_decorate = False
        col_F0A3B.scale_x = 1.0
        col_F0A3B.scale_y = 1.5
        col_F0A3B.alignment = 'Expand'.upper()
        col_F0A3B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_F0A3B.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'update_mode', text='', icon_value=0, emboss=True, toggle=True)
        col_A4D20.separator(factor=1.0)
        if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Enable Camera Updates'):
            if 'EDIT_MESH'==bpy.context.mode:
                if '3DGS_Mesh_Type' in bpy.context.view_layer.objects.active:
                    if (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'):
                        pass
                    else:
                        box_96194 = col_A4D20.box()
                        box_96194.alert = False
                        box_96194.enabled = True
                        box_96194.active = True
                        box_96194.use_property_split = False
                        box_96194.use_property_decorate = False
                        box_96194.alignment = 'Expand'.upper()
                        box_96194.scale_x = 1.0
                        box_96194.scale_y = 1.0
                        if not True: box_96194.operator_context = "EXEC_DEFAULT"
                        row_A3F2D = box_96194.row(heading='', align=True)
                        row_A3F2D.alert = False
                        row_A3F2D.enabled = True
                        row_A3F2D.active = True
                        row_A3F2D.use_property_split = False
                        row_A3F2D.use_property_decorate = False
                        row_A3F2D.scale_x = 1.0
                        row_A3F2D.scale_y = 1.0
                        row_A3F2D.alignment = 'Expand'.upper()
                        row_A3F2D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                        op = row_A3F2D.operator('sna.dgs_render_align_active_to_x_axis_6ae0e', text='X', icon_value=0, emboss=True, depress=False)
                        op = row_A3F2D.operator('sna.dgs_render_align_active_to_y_axis_c305d', text='Y', icon_value=0, emboss=True, depress=False)
                        op = row_A3F2D.operator('sna.dgs_render_align_active_to_z_axis_1e184', text='Z', icon_value=0, emboss=True, depress=False)
            else:
                box_1444A = col_A4D20.box()
                box_1444A.alert = False
                box_1444A.enabled = True
                box_1444A.active = True
                box_1444A.use_property_split = False
                box_1444A.use_property_decorate = False
                box_1444A.alignment = 'Expand'.upper()
                box_1444A.scale_x = 1.0
                box_1444A.scale_y = 1.0
                if not True: box_1444A.operator_context = "EXEC_DEFAULT"
                op = box_1444A.operator('sna.dgs_render_align_active_to_view_30b13', text=('Refresh update to camera' if ((bpy.context.scene.camera != None) and bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update) else 'Update Active To View'), icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'eye.svg')), emboss=True, depress=False)
        if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Show As Point Cloud'):
            box_AA375 = col_A4D20.box()
            box_AA375.alert = False
            box_AA375.enabled = True
            box_AA375.active = True
            box_AA375.use_property_split = False
            box_AA375.use_property_decorate = False
            box_AA375.alignment = 'Expand'.upper()
            box_AA375.scale_x = 1.0
            box_AA375.scale_y = 1.0
            if not True: box_AA375.operator_context = "EXEC_DEFAULT"
            attr_C8F44 = '["' + str('Socket_51' + '"]') 
            box_AA375.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_C8F44, text='Point Radius', icon_value=0, emboss=True)
            box_AA375.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], '["Socket_61"]', bpy.data, 'materials', text='Material', icon='NONE', item_search_property="name")
        if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Enable Camera Updates'):
            col_75D68 = col_A4D20.column(heading='', align=False)
            col_75D68.alert = False
            col_75D68.enabled = True
            col_75D68.active = True
            col_75D68.use_property_split = False
            col_75D68.use_property_decorate = False
            col_75D68.scale_x = 1.0
            col_75D68.scale_y = 1.0
            col_75D68.alignment = 'Expand'.upper()
            col_75D68.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if ((bpy.context.scene.camera == None) and bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update):
                box_A3A41 = col_75D68.box()
                box_A3A41.alert = False
                box_A3A41.enabled = True
                box_A3A41.active = True
                box_A3A41.use_property_split = False
                box_A3A41.use_property_decorate = False
                box_A3A41.alignment = 'Expand'.upper()
                box_A3A41.scale_x = 1.0
                box_A3A41.scale_y = 1.0
                if not True: box_A3A41.operator_context = "EXEC_DEFAULT"
                box_A3A41.label(text='No Active Camera Found', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            box_21A87 = col_75D68.box()
            box_21A87.alert = bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update
            box_21A87.enabled = True
            box_21A87.active = True
            box_21A87.use_property_split = False
            box_21A87.use_property_decorate = False
            box_21A87.alignment = 'Expand'.upper()
            box_21A87.scale_x = 1.0
            box_21A87.scale_y = 1.5
            if not True: box_21A87.operator_context = "EXEC_DEFAULT"
            box_21A87.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'cam_update', text='Use Active Camera', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera.svg')), emboss=True, toggle=True)
            if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update and (bpy.context.scene.camera != None) and property_exists("bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_68']", globals(), locals()) and property_exists("None", globals(), locals())):
                col_C389F = col_75D68.column(heading='', align=True)
                col_C389F.alert = False
                col_C389F.enabled = True
                col_C389F.active = True
                col_C389F.use_property_split = False
                col_C389F.use_property_decorate = False
                col_C389F.scale_x = 1.0
                col_C389F.scale_y = 1.0
                col_C389F.alignment = 'Expand'.upper()
                col_C389F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                box_81D6E = col_C389F.box()
                box_81D6E.alert = False
                box_81D6E.enabled = True
                box_81D6E.active = True
                box_81D6E.use_property_split = False
                box_81D6E.use_property_decorate = False
                box_81D6E.alignment = 'Expand'.upper()
                box_81D6E.scale_x = 1.0
                box_81D6E.scale_y = 1.0
                if not True: box_81D6E.operator_context = "EXEC_DEFAULT"
                row_BAB68 = box_81D6E.row(heading='', align=False)
                row_BAB68.alert = False
                row_BAB68.enabled = True
                row_BAB68.active = True
                row_BAB68.use_property_split = False
                row_BAB68.use_property_decorate = False
                row_BAB68.scale_x = 1.0
                row_BAB68.scale_y = 1.0
                row_BAB68.alignment = 'Expand'.upper()
                row_BAB68.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                attr_47247 = '["' + str('Socket_68' + '"]') 
                row_BAB68.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_47247, text='Frustrum Cull (Edit Mode)', icon_value=0, emboss=True)
                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_68']:
                    split_06E70 = row_BAB68.split(factor=0.30000001192092896, align=False)
                    split_06E70.alert = False
                    split_06E70.enabled = True
                    split_06E70.active = True
                    split_06E70.use_property_split = False
                    split_06E70.use_property_decorate = False
                    split_06E70.scale_x = 1.0
                    split_06E70.scale_y = 1.0
                    split_06E70.alignment = 'Expand'.upper()
                    if not True: split_06E70.operator_context = "EXEC_DEFAULT"
                    attr_F00D7 = '["' + str('Socket_74' + '"]') 
                    split_06E70.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_F00D7, text='Invert', icon_value=0, emboss=True)
                    attr_D8000 = '["' + str('Socket_63' + '"]') 
                    split_06E70.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_D8000, text='Padding', icon_value=0, emboss=True)
                box_D224C = col_C389F.box()
                box_D224C.alert = False
                box_D224C.enabled = True
                box_D224C.active = True
                box_D224C.use_property_split = False
                box_D224C.use_property_decorate = False
                box_D224C.alignment = 'Expand'.upper()
                box_D224C.scale_x = 1.0
                box_D224C.scale_y = 1.0
                if not True: box_D224C.operator_context = "EXEC_DEFAULT"
                row_03A56 = box_D224C.row(heading='', align=False)
                row_03A56.alert = False
                row_03A56.enabled = True
                row_03A56.active = True
                row_03A56.use_property_split = False
                row_03A56.use_property_decorate = False
                row_03A56.scale_x = 1.0
                row_03A56.scale_y = 1.0
                row_03A56.alignment = 'Expand'.upper()
                row_03A56.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                attr_12DA6 = '["' + str('Socket_69' + '"]') 
                row_03A56.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_12DA6, text='Distance Cull (Edit Mode)', icon_value=0, emboss=True)
                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_69']:
                    attr_29452 = '["' + str('Socket_72' + '"]') 
                    row_03A56.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_29452, text='Use Camera Clip Range', icon_value=0, emboss=True)
                if ( not bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_72'] and bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_69']):
                    row_050CC = box_D224C.row(heading='', align=False)
                    row_050CC.alert = False
                    row_050CC.enabled = True
                    row_050CC.active = True
                    row_050CC.use_property_split = False
                    row_050CC.use_property_decorate = False
                    row_050CC.scale_x = 1.0
                    row_050CC.scale_y = 1.0
                    row_050CC.alignment = 'Expand'.upper()
                    row_050CC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    attr_47D5F = '["' + str('Socket_70' + '"]') 
                    row_050CC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_47D5F, text='Near Distance', icon_value=0, emboss=True)
                    attr_05FB6 = '["' + str('Socket_71' + '"]') 
                    row_050CC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_05FB6, text='Far Distance', icon_value=0, emboss=True)
