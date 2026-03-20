import bpy
import bpy.utils.previews
import webbrowser
import os
import math
from bpy_extras.io_utils import ImportHelper, ExportHelper
import subprocess
import sys
import tempfile
import shutil
import gpu.state
import numpy as np
import time
import gpu
from gpu_extras.batch import batch_for_shader
import uuid
from math import pi
from mathutils import Matrix
from typing import Optional
from .important import *

def sna_dgs_render__main_function_menu_019C7(layout_function, ):
    box_BDC6F = layout_function.box()
    box_BDC6F.alert = False
    box_BDC6F.enabled = True
    box_BDC6F.active = True
    box_BDC6F.use_property_split = False
    box_BDC6F.use_property_decorate = False
    box_BDC6F.alignment = 'Expand'.upper()
    box_BDC6F.scale_x = 1.0
    box_BDC6F.scale_y = 1.0
    if not True: box_BDC6F.operator_context = "EXEC_DEFAULT"
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        if ('update_rot_to_cam' in bpy.context.view_layer.objects.active and (bpy.context.scene.sna_dgs_scene_properties.active_mode == 'Edit')):
            layout_function = box_BDC6F
            sna_active_3dgs_mesh_object_menu_9588F(layout_function, )
    box_DCCA2 = box_BDC6F.box()
    box_DCCA2.alert = False
    box_DCCA2.enabled = ((not ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop))) and 'OBJECT'==bpy.context.mode)
    box_DCCA2.active = True
    box_DCCA2.use_property_split = False
    box_DCCA2.use_property_decorate = False
    box_DCCA2.alignment = 'Expand'.upper()
    box_DCCA2.scale_x = 1.0
    box_DCCA2.scale_y = 1.0
    if not True: box_DCCA2.operator_context = "EXEC_DEFAULT"
    box_DCCA2.label(text='Active Mode', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    row_A59C6 = box_DCCA2.row(heading='', align=False)
    row_A59C6.alert = False
    row_A59C6.enabled = True
    row_A59C6.active = True
    row_A59C6.use_property_split = False
    row_A59C6.use_property_decorate = False
    row_A59C6.scale_x = 1.0
    row_A59C6.scale_y = 1.0
    row_A59C6.alignment = 'Expand'.upper()
    row_A59C6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_A59C6.prop(bpy.context.scene.sna_dgs_scene_properties, 'active_mode', text=bpy.context.scene.sna_dgs_scene_properties.active_mode, icon_value=0, emboss=True, expand=True)
    if str(bpy.context.scene.sna_dgs_scene_properties.active_mode) == "Edit":
        layout_function = box_BDC6F
        sna_edit_menu_D3299(layout_function, )
    elif str(bpy.context.scene.sna_dgs_scene_properties.active_mode) == "Render":
        layout_function = box_BDC6F
        sna_render_new_menu_66133(layout_function, )
    elif str(bpy.context.scene.sna_dgs_scene_properties.active_mode) == "Mesh 2 3DGS":
        layout_function = box_BDC6F
        sna_mesh_to_3dgs_function_interface_8DDDC(layout_function, )
    else:
        pass



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
        box_29E44 = col_247F1.box()
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
        col_A4D20.separator(factor=1.0)
        col_F0A3B = col_A4D20.column(heading='', align=False)
        col_F0A3B.alert = (bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Disable Camera Updates')
        col_F0A3B.enabled = True
        col_F0A3B.active = True
        col_F0A3B.use_property_split = False
        col_F0A3B.use_property_decorate = False
        col_F0A3B.scale_x = 1.0
        col_F0A3B.scale_y = 1.0
        col_F0A3B.alignment = 'Expand'.upper()
        col_F0A3B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_F0A3B.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'update_mode', text='', icon_value=0, emboss=True, toggle=True)
        col_A4D20.separator(factor=1.0)
        if ((bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode == 'Enable Camera Updates') and (not bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update)):
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
                        row_A3F2D = box_96194.row(heading='', align=False)
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
                op = box_1444A.operator('sna.dgs_render_align_active_to_view_30b13', text='Update Active To View', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'eye.svg')), emboss=True, depress=False)
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
            box_DC5A2 = col_A4D20.box()
            box_DC5A2.alert = bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update
            box_DC5A2.enabled = True
            box_DC5A2.active = True
            box_DC5A2.use_property_split = False
            box_DC5A2.use_property_decorate = False
            box_DC5A2.alignment = 'Expand'.upper()
            box_DC5A2.scale_x = 1.0
            box_DC5A2.scale_y = 1.0
            if not True: box_DC5A2.operator_context = "EXEC_DEFAULT"
            if ((bpy.context.scene.camera == None) and bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update):
                box_A3A41 = box_DC5A2.box()
                box_A3A41.alert = False
                box_A3A41.enabled = True
                box_A3A41.active = True
                box_A3A41.use_property_split = False
                box_A3A41.use_property_decorate = False
                box_A3A41.alignment = 'Expand'.upper()
                box_A3A41.scale_x = 1.0
                box_A3A41.scale_y = 1.0
                if not True: box_A3A41.operator_context = "EXEC_DEFAULT"
                box_A3A41.label(text='No Active Camera Found', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_DC5A2.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'cam_update', text='Use Active Camera', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera.svg')), emboss=True, toggle=True)




def sna_mesh_to_3dgs_function_interface_8DDDC(layout_function, ):
    if bpy.context.scene.sna_dgs_scene_properties.show_tips:
        box_58AE4 = layout_function.box()
        box_58AE4.alert = False
        box_58AE4.enabled = True
        box_58AE4.active = True
        box_58AE4.use_property_split = False
        box_58AE4.use_property_decorate = False
        box_58AE4.alignment = 'Expand'.upper()
        box_58AE4.scale_x = 1.0
        box_58AE4.scale_y = 1.0
        if not True: box_58AE4.operator_context = "EXEC_DEFAULT"
        box_58AE4.label(text='Linux and Mac are not supported', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_58AE4.label(text='         The .OBJ mesh must be triangulated', icon_value=0)
        box_58AE4.label(text='         The colour image texture must be', icon_value=0)
        box_58AE4.label(text='         in the same folder as your .OBJ and .MTL', icon_value=0)
    box_9766A = layout_function.box()
    box_9766A.alert = False
    box_9766A.enabled = True
    box_9766A.active = True
    box_9766A.use_property_split = False
    box_9766A.use_property_decorate = False
    box_9766A.alignment = 'Expand'.upper()
    box_9766A.scale_x = 1.0
    box_9766A.scale_y = 1.0
    if not True: box_9766A.operator_context = "EXEC_DEFAULT"
    box_9766A.prop(bpy.context.scene.sna_dgs_scene_properties, 'mesh2gs_validate', text='Validate Mesh, Texture and .MTL', icon_value=0, emboss=True)
    box_8C171 = layout_function.box()
    box_8C171.alert = False
    box_8C171.enabled = True
    box_8C171.active = True
    box_8C171.use_property_split = False
    box_8C171.use_property_decorate = False
    box_8C171.alignment = 'Expand'.upper()
    box_8C171.scale_x = 1.0
    box_8C171.scale_y = 1.0
    if not True: box_8C171.operator_context = "EXEC_DEFAULT"
    op = box_8C171.operator('sna.dgs_render_mesh23dgs_3dfed', text='Select .OBJ', icon_value=0, emboss=True, depress=False)







def sna_render_new_menu_66133(layout_function, ):
    box_D20F4 = layout_function.box()
    box_D20F4.alert = False
    box_D20F4.enabled = (not ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)))
    box_D20F4.active = True
    box_D20F4.use_property_split = False
    box_D20F4.use_property_decorate = False
    box_D20F4.alignment = 'Expand'.upper()
    box_D20F4.scale_x = 1.0
    box_D20F4.scale_y = 1.0
    if not True: box_D20F4.operator_context = "EXEC_DEFAULT"
    grid_DDB98 = box_D20F4.grid_flow(columns=2, row_major=False, even_columns=False, even_rows=False, align=True)
    grid_DDB98.enabled = True
    grid_DDB98.active = True
    grid_DDB98.use_property_split = False
    grid_DDB98.use_property_decorate = False
    grid_DDB98.alignment = 'Expand'.upper()
    grid_DDB98.scale_x = 1.0
    grid_DDB98.scale_y = 1.0
    if not True: grid_DDB98.operator_context = "EXEC_DEFAULT"
    grid_DDB98.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_main_mode', text=bpy.context.scene.sna_dgs_scene_properties.r2_main_mode, icon_value=0, emboss=True, expand=True)
    if bpy.context.scene.sna_dgs_scene_properties.r2_main_mode == "Update":
        box_10F75 = layout_function.box()
        box_10F75.alert = False
        box_10F75.enabled = True
        box_10F75.active = True
        box_10F75.use_property_split = False
        box_10F75.use_property_decorate = False
        box_10F75.alignment = 'Expand'.upper()
        box_10F75.scale_x = 1.0
        box_10F75.scale_y = 1.0
        if not True: box_10F75.operator_context = "EXEC_DEFAULT"
        box_10F75.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_hide_on_change', text='Hide / Show Objects On Menu Change*', icon_value=0, emboss=True)
        box_10F75.label(text='*Vert Imported objects only', icon_value=0)
        box_10F75.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_transforms', text='Copy Source Transforms', icon_value=0, emboss=True)
        box_10F75.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_selected', text='Selected Empties Only', icon_value=0, emboss=True)
        col_1EFCE = box_10F75.column(heading='', align=False)
        col_1EFCE.alert = False
        col_1EFCE.enabled = (not ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)))
        col_1EFCE.active = True
        col_1EFCE.use_property_split = False
        col_1EFCE.use_property_decorate = False
        col_1EFCE.scale_x = 1.0
        col_1EFCE.scale_y = 1.0
        col_1EFCE.alignment = 'Expand'.upper()
        col_1EFCE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_F6BE9 = col_1EFCE.row(heading='', align=False)
        row_F6BE9.alert = False
        row_F6BE9.enabled = True
        row_F6BE9.active = True
        row_F6BE9.use_property_split = False
        row_F6BE9.use_property_decorate = False
        row_F6BE9.scale_x = 1.0
        row_F6BE9.scale_y = 1.0
        row_F6BE9.alignment = 'Expand'.upper()
        row_F6BE9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_F6BE9.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_update_type', text=bpy.context.scene.sna_dgs_scene_properties.r2_update_type, icon_value=0, emboss=True, expand=True)
        if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update'):
            col_1EFCE.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_interval', text='Interval Time (Seconds)', icon_value=0, emboss=True, expand=True)
        col_5B10D = col_1EFCE.column(heading='', align=False)
        col_5B10D.alert = False
        col_5B10D.enabled = True
        col_5B10D.active = True
        col_5B10D.use_property_split = False
        col_5B10D.use_property_decorate = False
        col_5B10D.scale_x = 1.0
        col_5B10D.scale_y = 2.0
        col_5B10D.alignment = 'Expand'.upper()
        col_5B10D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_5B10D.operator('sna.dgs_render_refresh_scene_c0b35', text='Update Scene', icon_value=(load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'play.svg')) if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update') else load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg'))), emboss=True, depress=False)
        if ((bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop)):
            col_79A7A = box_10F75.column(heading='', align=False)
            col_79A7A.alert = True
            col_79A7A.enabled = True
            col_79A7A.active = True
            col_79A7A.use_property_split = False
            col_79A7A.use_property_decorate = False
            col_79A7A.scale_x = 1.0
            col_79A7A.scale_y = 2.0
            col_79A7A.alignment = 'Expand'.upper()
            col_79A7A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_79A7A.operator('sna.dgs_render_stop_interval_updates_5ac80', text='Stop', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'stop.svg')), emboss=True, depress=False)
        if bpy.context.scene.sna_dgs_scene_properties.show_tips:
            col_16809 = box_10F75.column(heading='', align=False)
            col_16809.alert = False
            col_16809.enabled = True
            col_16809.active = True
            col_16809.use_property_split = False
            col_16809.use_property_decorate = False
            col_16809.scale_x = 1.0
            col_16809.scale_y = 1.0
            col_16809.alignment = 'Expand'.upper()
            col_16809.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Interval Update'):
                box_FC0BD = col_16809.box()
                box_FC0BD.alert = False
                box_FC0BD.enabled = True
                box_FC0BD.active = True
                box_FC0BD.use_property_split = False
                box_FC0BD.use_property_decorate = False
                box_FC0BD.alignment = 'Expand'.upper()
                box_FC0BD.scale_x = 1.0
                box_FC0BD.scale_y = 1.0
                if not True: box_FC0BD.operator_context = "EXEC_DEFAULT"
                box_FC0BD.label(text='Interval Updates are intensive and', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
                box_FC0BD.label(text='not recommended for most scans. Use it', icon_value=0)
                box_FC0BD.label(text='to preview single, small object animations.', icon_value=0)
                box_FC0BD.label(text='Use with caution', icon_value=0)
            box_AC001 = col_16809.box()
            box_AC001.alert = False
            box_AC001.enabled = True
            box_AC001.active = True
            box_AC001.use_property_split = False
            box_AC001.use_property_decorate = False
            box_AC001.alignment = 'Expand'.upper()
            box_AC001.scale_x = 1.0
            box_AC001.scale_y = 1.0
            if not True: box_AC001.operator_context = "EXEC_DEFAULT"
            box_AC001.label(text='If rendering multiple objects and some', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_AC001.label(text='disappear. Try switching between Edit and', icon_value=0)
            box_AC001.label(text='Render modes.', icon_value=0)
            box_6A92E = col_16809.box()
            box_6A92E.alert = False
            box_6A92E.enabled = True
            box_6A92E.active = True
            box_6A92E.use_property_split = False
            box_6A92E.use_property_decorate = False
            box_6A92E.alignment = 'Expand'.upper()
            box_6A92E.scale_x = 1.0
            box_6A92E.scale_y = 1.0
            if not True: box_6A92E.operator_context = "EXEC_DEFAULT"
            box_6A92E.label(text='If depth sorting fails (objects appear', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_6A92E.label(text='cloudy or background is in front) Move the', icon_value=0)
            box_6A92E.label(text='camera with Shit+Middle Mouse', icon_value=0)
    elif bpy.context.scene.sna_dgs_scene_properties.r2_main_mode == "Create":
        col_0F0D4 = layout_function.column(heading='', align=False)
        col_0F0D4.alert = False
        col_0F0D4.enabled = True
        col_0F0D4.active = True
        col_0F0D4.use_property_split = False
        col_0F0D4.use_property_decorate = False
        col_0F0D4.scale_x = 1.0
        col_0F0D4.scale_y = 1.0
        col_0F0D4.alignment = 'Expand'.upper()
        col_0F0D4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_66033 = col_0F0D4.box()
        box_66033.alert = False
        box_66033.enabled = (not (bpy.context.view_layer.objects.active == None))
        box_66033.active = True
        box_66033.use_property_split = False
        box_66033.use_property_decorate = False
        box_66033.alignment = 'Expand'.upper()
        box_66033.scale_x = 1.0
        box_66033.scale_y = 1.0
        if not True: box_66033.operator_context = "EXEC_DEFAULT"
        op = box_66033.operator('sna.dgs_render_create_proxy_from_mesh_d5b41', text='Create Proxy From Active', icon_value=0, emboss=True, depress=False)
        if (bpy.context.view_layer.objects.active == None):
            box_383DE = col_0F0D4.box()
            box_383DE.alert = False
            box_383DE.enabled = True
            box_383DE.active = True
            box_383DE.use_property_split = False
            box_383DE.use_property_decorate = False
            box_383DE.alignment = 'Expand'.upper()
            box_383DE.scale_x = 1.0
            box_383DE.scale_y = 1.0
            if not True: box_383DE.operator_context = "EXEC_DEFAULT"
            box_383DE.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
    elif bpy.context.scene.sna_dgs_scene_properties.r2_main_mode == "Render":
        box_AC05E = layout_function.box()
        box_AC05E.alert = False
        box_AC05E.enabled = True
        box_AC05E.active = True
        box_AC05E.use_property_split = False
        box_AC05E.use_property_decorate = False
        box_AC05E.alignment = 'Expand'.upper()
        box_AC05E.scale_x = 1.0
        box_AC05E.scale_y = 1.0
        if not True: box_AC05E.operator_context = "EXEC_DEFAULT"
        box_AC05E.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_animation', text='Render Animation', icon_value=0, emboss=True)
        box_AC05E.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_color', text='Color Pass', icon_value=0, emboss=True)
        box_AC05E.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_depth', text='Depth Pass', icon_value=0, emboss=True)
        box_AC05E.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_comp', text='Combine With Native Render', icon_value=0, emboss=True)
        box_AC05E.prop(bpy.context.scene.render, 'filepath', text='Output', icon_value=0, emboss=True)
        col_B2DE2 = box_AC05E.column(heading='', align=False)
        col_B2DE2.alert = False
        col_B2DE2.enabled = ((bpy.context.scene.camera != None) and (bpy.context.scene.render.filepath != ''))
        col_B2DE2.active = True
        col_B2DE2.use_property_split = False
        col_B2DE2.use_property_decorate = False
        col_B2DE2.scale_x = 1.0
        col_B2DE2.scale_y = 2.0
        col_B2DE2.alignment = 'Expand'.upper()
        col_B2DE2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_B2DE2.operator('sna.dgs_render_advanced_render_ba196', text='Render', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera.svg')), emboss=True, depress=False)
        if (bpy.context.scene.camera == None):
            box_6E0B8 = box_AC05E.box()
            box_6E0B8.alert = False
            box_6E0B8.enabled = True
            box_6E0B8.active = True
            box_6E0B8.use_property_split = False
            box_6E0B8.use_property_decorate = False
            box_6E0B8.alignment = 'Expand'.upper()
            box_6E0B8.scale_x = 1.0
            box_6E0B8.scale_y = 1.0
            if not True: box_6E0B8.operator_context = "EXEC_DEFAULT"
            box_6E0B8.label(text='No Active Camera Found In Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        if (bpy.context.scene.render.filepath == ''):
            box_FF283 = box_AC05E.box()
            box_FF283.alert = False
            box_FF283.enabled = True
            box_FF283.active = True
            box_FF283.use_property_split = False
            box_FF283.use_property_decorate = False
            box_FF283.alignment = 'Expand'.upper()
            box_FF283.scale_x = 1.0
            box_FF283.scale_y = 1.0
            if not True: box_FF283.operator_context = "EXEC_DEFAULT"
            box_FF283.label(text='Output is empty', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        if bpy.context.scene.sna_dgs_scene_properties.show_tips:
            box_BE1D0 = box_AC05E.box()
            box_BE1D0.alert = False
            box_BE1D0.enabled = True
            box_BE1D0.active = True
            box_BE1D0.use_property_split = False
            box_BE1D0.use_property_decorate = False
            box_BE1D0.alignment = 'Expand'.upper()
            box_BE1D0.scale_x = 1.0
            box_BE1D0.scale_y = 1.0
            if not True: box_BE1D0.operator_context = "EXEC_DEFAULT"
            box_BE1D0.label(text='For light reactive Splats, render', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_BE1D0.label(text="mesh 3DGS objects while in the addon's", icon_value=0)
            box_BE1D0.label(text='Edit mode', icon_value=0)
    elif bpy.context.scene.sna_dgs_scene_properties.r2_main_mode == "Clean Up":
        box_32F4A = layout_function.box()
        box_32F4A.alert = False
        box_32F4A.enabled = True
        box_32F4A.active = True
        box_32F4A.use_property_split = False
        box_32F4A.use_property_decorate = False
        box_32F4A.alignment = 'Expand'.upper()
        box_32F4A.scale_x = 1.0
        box_32F4A.scale_y = 1.0
        if not True: box_32F4A.operator_context = "EXEC_DEFAULT"
        box_32F4A.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_clear_empties', text='Delete All Proxy Empties', icon_value=0, emboss=True)
        op = box_32F4A.operator('sna.dgs_render_clean_up_advanced_render_scene_09450', text='Stop Viewport Rendering', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
    else:
        pass
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Attributes_GN' in bpy.context.view_layer.objects.active.modifiers):
        col_5A5DB = layout_function.column(heading='', align=False)
        col_5A5DB.alert = False
        col_5A5DB.enabled = True
        col_5A5DB.active = True
        col_5A5DB.use_property_split = False
        col_5A5DB.use_property_decorate = False
        col_5A5DB.scale_x = 1.0
        col_5A5DB.scale_y = 1.0
        col_5A5DB.alignment = 'Expand'.upper()
        col_5A5DB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_83499 = col_5A5DB.box()
        box_83499.alert = False
        box_83499.enabled = True
        box_83499.active = True
        box_83499.use_property_split = False
        box_83499.use_property_decorate = False
        box_83499.alignment = 'Expand'.upper()
        box_83499.scale_x = 1.0
        box_83499.scale_y = 1.0
        if not True: box_83499.operator_context = "EXEC_DEFAULT"
        box_83499.label(text='Active Object: ' + bpy.context.view_layer.objects.active.name, icon_value=0)
        layout_function = col_5A5DB
        sna_attribute_adjust_properties_2C323(layout_function, )


def sna_edit_menu_D3299(layout_function, ):
    if (bpy.context.scene.sna_dgs_scene_properties.active_mode == 'Edit'):
        box_09ED1 = layout_function.box()
        box_09ED1.alert = False
        box_09ED1.enabled = True
        box_09ED1.active = True
        box_09ED1.use_property_split = False
        box_09ED1.use_property_decorate = False
        box_09ED1.alignment = 'Expand'.upper()
        box_09ED1.scale_x = 1.0
        box_09ED1.scale_y = 1.0
        if not True: box_09ED1.operator_context = "EXEC_DEFAULT"
        grid_B53F5 = box_09ED1.grid_flow(columns=2, row_major=True, even_columns=False, even_rows=False, align=True)
        grid_B53F5.enabled = True
        grid_B53F5.active = True
        grid_B53F5.use_property_split = False
        grid_B53F5.use_property_decorate = False
        grid_B53F5.alignment = 'Expand'.upper()
        grid_B53F5.scale_x = 1.0
        grid_B53F5.scale_y = 1.0
        if not True: grid_B53F5.operator_context = "EXEC_DEFAULT"
        grid_B53F5.prop(bpy.context.scene.sna_dgs_scene_properties, 'edit_mode_menu', text=bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu, icon_value=0, emboss=True, expand=True)
    if bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Import":
        box_456A0 = layout_function.box()
        box_456A0.alert = False
        box_456A0.enabled = True
        box_456A0.active = True
        box_456A0.use_property_split = False
        box_456A0.use_property_decorate = False
        box_456A0.alignment = 'Expand'.upper()
        box_456A0.scale_x = 1.0
        box_456A0.scale_y = 1.0
        if not True: box_456A0.operator_context = "EXEC_DEFAULT"
        layout_function = box_456A0
        sna_import_menu_94FB1(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Modifiers":
        if (bpy.context.view_layer.objects.active == None):
            box_BCC27 = layout_function.box()
            box_BCC27.alert = False
            box_BCC27.enabled = True
            box_BCC27.active = True
            box_BCC27.use_property_split = False
            box_BCC27.use_property_decorate = False
            box_BCC27.alignment = 'Expand'.upper()
            box_BCC27.scale_x = 1.0
            box_BCC27.scale_y = 1.0
            if not True: box_BCC27.operator_context = "EXEC_DEFAULT"
            box_BCC27.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        else:
            box_15E02 = layout_function.box()
            box_15E02.alert = False
            box_15E02.enabled = True
            box_15E02.active = True
            box_15E02.use_property_split = False
            box_15E02.use_property_decorate = False
            box_15E02.alignment = 'Expand'.upper()
            box_15E02.scale_x = 1.0
            box_15E02.scale_y = 1.0
            if not True: box_15E02.operator_context = "EXEC_DEFAULT"
            layout_function = box_15E02
            sna_modify_menu_AEA26(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Colour":
        if (bpy.context.view_layer.objects.active == None):
            box_7DC02 = layout_function.box()
            box_7DC02.alert = False
            box_7DC02.enabled = True
            box_7DC02.active = True
            box_7DC02.use_property_split = False
            box_7DC02.use_property_decorate = False
            box_7DC02.alignment = 'Expand'.upper()
            box_7DC02.scale_x = 1.0
            box_7DC02.scale_y = 1.0
            if not True: box_7DC02.operator_context = "EXEC_DEFAULT"
            box_7DC02.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        else:
            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Colour_And_Material' in bpy.context.view_layer.objects.active.modifiers):
                box_FB8A4 = layout_function.box()
                box_FB8A4.alert = False
                box_FB8A4.enabled = True
                box_FB8A4.active = True
                box_FB8A4.use_property_split = False
                box_FB8A4.use_property_decorate = False
                box_FB8A4.alignment = 'Expand'.upper()
                box_FB8A4.scale_x = 1.0
                box_FB8A4.scale_y = 1.0
                if not True: box_FB8A4.operator_context = "EXEC_DEFAULT"
                layout_function = box_FB8A4
                sna_colour_function_interface_3A6A5(layout_function, )
            else:
                box_6F020 = layout_function.box()
                box_6F020.alert = False
                box_6F020.enabled = True
                box_6F020.active = True
                box_6F020.use_property_split = False
                box_6F020.use_property_decorate = False
                box_6F020.alignment = 'Expand'.upper()
                box_6F020.scale_x = 1.0
                box_6F020.scale_y = 1.0
                if not True: box_6F020.operator_context = "EXEC_DEFAULT"
                box_6F020.label(text='Active Object is missing the ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
                box_6F020.label(text='Adjust_Colour_And_Material modifier', icon_value=0)
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Animate":
        if (bpy.context.view_layer.objects.active == None):
            box_36685 = layout_function.box()
            box_36685.alert = False
            box_36685.enabled = True
            box_36685.active = True
            box_36685.use_property_split = False
            box_36685.use_property_decorate = False
            box_36685.alignment = 'Expand'.upper()
            box_36685.scale_x = 1.0
            box_36685.scale_y = 1.0
            if not True: box_36685.operator_context = "EXEC_DEFAULT"
            box_36685.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        else:
            box_2B760 = layout_function.box()
            box_2B760.alert = False
            box_2B760.enabled = True
            box_2B760.active = True
            box_2B760.use_property_split = False
            box_2B760.use_property_decorate = False
            box_2B760.alignment = 'Expand'.upper()
            box_2B760.scale_x = 1.0
            box_2B760.scale_y = 1.0
            if not True: box_2B760.operator_context = "EXEC_DEFAULT"
            layout_function = box_2B760
            sna_animate_function_interface_57F9E(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "HQ / LQ":
        box_50BC2 = layout_function.box()
        box_50BC2.alert = False
        box_50BC2.enabled = True
        box_50BC2.active = True
        box_50BC2.use_property_split = False
        box_50BC2.use_property_decorate = False
        box_50BC2.alignment = 'Expand'.upper()
        box_50BC2.scale_x = 1.0
        box_50BC2.scale_y = 1.0
        if not True: box_50BC2.operator_context = "EXEC_DEFAULT"
        layout_function = box_50BC2
        sna_hq_mode_function_interface_17C41(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_menu == "Export":
        if (bpy.context.view_layer.objects.active == None):
            box_A093C = layout_function.box()
            box_A093C.alert = False
            box_A093C.enabled = True
            box_A093C.active = True
            box_A093C.use_property_split = False
            box_A093C.use_property_decorate = False
            box_A093C.alignment = 'Expand'.upper()
            box_A093C.scale_x = 1.0
            box_A093C.scale_y = 1.0
            if not True: box_A093C.operator_context = "EXEC_DEFAULT"
            box_A093C.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        else:
            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.view_layer.objects.active.modifiers):
                if (len(bpy.context.view_layer.objects.selected) > 1):
                    box_7DD8C = layout_function.box()
                    box_7DD8C.alert = False
                    box_7DD8C.enabled = True
                    box_7DD8C.active = True
                    box_7DD8C.use_property_split = False
                    box_7DD8C.use_property_decorate = False
                    box_7DD8C.alignment = 'Expand'.upper()
                    box_7DD8C.scale_x = 1.0
                    box_7DD8C.scale_y = 1.0
                    if not True: box_7DD8C.operator_context = "EXEC_DEFAULT"
                    box_7DD8C.label(text='Only select 1 object for export', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
                else:
                    box_3E038 = layout_function.box()
                    box_3E038.alert = False
                    box_3E038.enabled = True
                    box_3E038.active = True
                    box_3E038.use_property_split = False
                    box_3E038.use_property_decorate = False
                    box_3E038.alignment = 'Expand'.upper()
                    box_3E038.scale_x = 1.0
                    box_3E038.scale_y = 1.0
                    if not True: box_3E038.operator_context = "EXEC_DEFAULT"
                    layout_function = box_3E038
                    sna_export_3dgs_function_interface_CDF59(layout_function, )
            else:
                box_DE950 = layout_function.box()
                box_DE950.alert = False
                box_DE950.enabled = True
                box_DE950.active = True
                box_DE950.use_property_split = False
                box_DE950.use_property_decorate = False
                box_DE950.alignment = 'Expand'.upper()
                box_DE950.scale_x = 1.0
                box_DE950.scale_y = 1.0
                if not True: box_DE950.operator_context = "EXEC_DEFAULT"
                box_DE950.label(text='The Active Object is missing the', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
                box_DE950.label(text='Write F_DC_And_Merge modifier', icon_value=0)
    else:
        pass


def sna_export_3dgs_function_interface_CDF59(layout_function, ):
    if bpy.context.scene.sna_dgs_scene_properties.show_tips:
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
        box_9553E.label(text='If you have applied scale or rotation', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_9553E.label(text="using Blender's native Apply Transform,", icon_value=0)
        box_9553E.label(text='3DGS attributes will be corrupted', icon_value=0)
        box_9553E.label(text='Higher SH attributes are not updated', icon_value=0)
    box_7E22C = layout_function.box()
    box_7E22C.alert = False
    box_7E22C.enabled = True
    box_7E22C.active = True
    box_7E22C.use_property_split = False
    box_7E22C.use_property_decorate = False
    box_7E22C.alignment = 'Expand'.upper()
    box_7E22C.scale_x = 1.0
    box_7E22C.scale_y = 1.0
    if not True: box_7E22C.operator_context = "EXEC_DEFAULT"
    op = box_7E22C.operator('sna.dgs_render_apply_3dgs_tranforms_5b665', text='Apply 3DGS Transforms and Colour', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine icon.svg')), emboss=True, depress=False)
    box_E30D3 = layout_function.box()
    box_E30D3.alert = False
    box_E30D3.enabled = 'OBJECT'==bpy.context.mode
    box_E30D3.active = True
    box_E30D3.use_property_split = False
    box_E30D3.use_property_decorate = False
    box_E30D3.alignment = 'Expand'.upper()
    box_E30D3.scale_x = 1.0
    box_E30D3.scale_y = 1.0
    if not True: box_E30D3.operator_context = "EXEC_DEFAULT"
    op = box_E30D3.operator('sna.dgs_render_export_mesh_object_as_3dgs_ply_ce2f7', text='Export 3DGS', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'export.svg')), emboss=True, depress=False)


def sna_animate_function_interface_57F9E(layout_function, ):
    box_DFEF6 = layout_function.box()
    box_DFEF6.alert = False
    box_DFEF6.enabled = True
    box_DFEF6.active = True
    box_DFEF6.use_property_split = False
    box_DFEF6.use_property_decorate = False
    box_DFEF6.alignment = 'Expand'.upper()
    box_DFEF6.scale_x = 1.0
    box_DFEF6.scale_y = 1.0
    if not True: box_DFEF6.operator_context = "EXEC_DEFAULT"
    op = box_DFEF6.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = box_DFEF6.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Animate_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_1DAB6 = layout_function.box()
        box_1DAB6.alert = False
        box_1DAB6.enabled = True
        box_1DAB6.active = True
        box_1DAB6.use_property_split = False
        box_1DAB6.use_property_decorate = False
        box_1DAB6.alignment = 'Expand'.upper()
        box_1DAB6.scale_x = 1.0
        box_1DAB6.scale_y = 1.0
        if not True: box_1DAB6.operator_context = "EXEC_DEFAULT"
        split_D18F1 = box_1DAB6.split(factor=0.5, align=False)
        split_D18F1.alert = False
        split_D18F1.enabled = True
        split_D18F1.active = True
        split_D18F1.use_property_split = False
        split_D18F1.use_property_decorate = False
        split_D18F1.scale_x = 1.0
        split_D18F1.scale_y = 1.0
        split_D18F1.alignment = 'Expand'.upper()
        if not True: split_D18F1.operator_context = "EXEC_DEFAULT"
        split_D18F1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], 'show_viewport', text='Animate', icon_value=0, emboss=True, toggle=True)
        row_058B1 = split_D18F1.row(heading='', align=True)
        row_058B1.alert = False
        row_058B1.enabled = True
        row_058B1.active = True
        row_058B1.use_property_split = False
        row_058B1.use_property_decorate = False
        row_058B1.scale_x = 1.0
        row_058B1.scale_y = 1.0
        row_058B1.alignment = 'Right'.upper()
        row_058B1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_058B1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_058B1.operator('sna.dgs_render_apply_animate_modifier_3938e', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_058B1.operator('sna.dgs_render_remove_animate_modifier_5b34d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        col_03A93 = box_1DAB6.column(heading='', align=False)
        col_03A93.alert = False
        col_03A93.enabled = True
        col_03A93.active = True
        col_03A93.use_property_split = False
        col_03A93.use_property_decorate = False
        col_03A93.scale_x = 1.0
        col_03A93.scale_y = 1.0
        col_03A93.alignment = 'Expand'.upper()
        col_03A93.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_797F1 = col_03A93.box()
        box_797F1.alert = False
        box_797F1.enabled = True
        box_797F1.active = True
        box_797F1.use_property_split = False
        box_797F1.use_property_decorate = False
        box_797F1.alignment = 'Expand'.upper()
        box_797F1.scale_x = 1.0
        box_797F1.scale_y = 1.0
        if not True: box_797F1.operator_context = "EXEC_DEFAULT"
        attr_C6924 = '["' + str('Socket_6' + '"]') 
        box_797F1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_C6924, text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 2):
            pass
        else:
            col_44B28 = box_797F1.column(heading='', align=False)
            col_44B28.alert = False
            col_44B28.enabled = True
            col_44B28.active = True
            col_44B28.use_property_split = False
            col_44B28.use_property_decorate = False
            col_44B28.scale_x = 1.0
            col_44B28.scale_y = 1.0
            col_44B28.alignment = 'Expand'.upper()
            col_44B28.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 0):
                attr_3F944 = '["' + str('Socket_2' + '"]') 
                col_44B28.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_3F944, text='', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 0):
                pass
            else:
                col_44B28.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_5"]', bpy.context.scene.collection, 'children', text='', icon='NONE', item_search_property="name")
            attr_D5EE1 = '["' + str('Socket_3' + '"]') 
            col_44B28.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D5EE1, text='Distance Threshold', icon_value=0, emboss=True)
        box_3AE7F = col_03A93.box()
        box_3AE7F.alert = False
        box_3AE7F.enabled = True
        box_3AE7F.active = True
        box_3AE7F.use_property_split = False
        box_3AE7F.use_property_decorate = False
        box_3AE7F.alignment = 'Expand'.upper()
        box_3AE7F.scale_x = 1.0
        box_3AE7F.scale_y = 1.0
        if not True: box_3AE7F.operator_context = "EXEC_DEFAULT"
        attr_A68D1 = '["' + str('Socket_37' + '"]') 
        box_3AE7F.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_A68D1, text='Decimate Animated', icon_value=0, emboss=True)
        box_F6C6C = col_03A93.box()
        box_F6C6C.alert = False
        box_F6C6C.enabled = True
        box_F6C6C.active = True
        box_F6C6C.use_property_split = False
        box_F6C6C.use_property_decorate = False
        box_F6C6C.alignment = 'Expand'.upper()
        box_F6C6C.scale_x = 1.0
        box_F6C6C.scale_y = 1.0
        if not True: box_F6C6C.operator_context = "EXEC_DEFAULT"
        attr_FEA5B = '["' + str('Socket_26' + '"]') 
        box_F6C6C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FEA5B, text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 1):
            box_6DFC4 = box_F6C6C.box()
            box_6DFC4.alert = False
            box_6DFC4.enabled = True
            box_6DFC4.active = True
            box_6DFC4.use_property_split = False
            box_6DFC4.use_property_decorate = False
            box_6DFC4.alignment = 'Expand'.upper()
            box_6DFC4.scale_x = 1.0
            box_6DFC4.scale_y = 1.0
            if not True: box_6DFC4.operator_context = "EXEC_DEFAULT"
            box_6DFC4.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_44"]', bpy.data, 'materials', text='Material', icon='NONE', item_search_property="name")
            attr_55AA7 = '["' + str('Socket_9' + '"]') 
            box_6DFC4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_55AA7, text='Point Min Radius', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 2):
                pass
            else:
                attr_A5ADF = '["' + str('Socket_10' + '"]') 
                box_6DFC4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_A5ADF, text='Point Max Radius', icon_value=0, emboss=True)
            attr_D7ABF = '["' + str('Socket_11' + '"]') 
            box_6DFC4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D7ABF, text='Random Mix', icon_value=0, emboss=True)
            attr_9A7E1 = '["' + str('Socket_12' + '"]') 
            box_6DFC4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_9A7E1, text='Random Multiplier', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 2):
            box_91071 = box_F6C6C.box()
            box_91071.alert = False
            box_91071.enabled = True
            box_91071.active = True
            box_91071.use_property_split = False
            box_91071.use_property_decorate = False
            box_91071.alignment = 'Expand'.upper()
            box_91071.scale_x = 1.0
            box_91071.scale_y = 1.0
            if not True: box_91071.operator_context = "EXEC_DEFAULT"
            box_91071.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_44"]', bpy.data, 'materials', text='Material', icon='NONE', item_search_property="name")
            attr_F4993 = '["' + str('Socket_38' + '"]') 
            box_91071.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_F4993, text='Curve Length', icon_value=0, emboss=True)
            attr_070CD = '["' + str('Socket_31' + '"]') 
            box_91071.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_070CD, text='Curve Min Radius', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_6'] == 2):
                pass
            else:
                attr_BA37E = '["' + str('Socket_32' + '"]') 
                box_91071.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_BA37E, text='Curve Max Radius', icon_value=0, emboss=True)
            attr_0D707 = '["' + str('Socket_33' + '"]') 
            box_91071.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_0D707, text='Random Mix', icon_value=0, emboss=True)
            attr_53122 = '["' + str('Socket_34' + '"]') 
            box_91071.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_53122, text='Random Multiplier', icon_value=0, emboss=True)
        box_B4084 = col_03A93.box()
        box_B4084.alert = False
        box_B4084.enabled = True
        box_B4084.active = True
        box_B4084.use_property_split = False
        box_B4084.use_property_decorate = False
        box_B4084.alignment = 'Expand'.upper()
        box_B4084.scale_x = 1.0
        box_B4084.scale_y = 1.0
        if not True: box_B4084.operator_context = "EXEC_DEFAULT"
        box_7D470 = box_B4084.box()
        box_7D470.alert = False
        box_7D470.enabled = True
        box_7D470.active = True
        box_7D470.use_property_split = False
        box_7D470.use_property_decorate = False
        box_7D470.alignment = 'Expand'.upper()
        box_7D470.scale_x = 1.0
        box_7D470.scale_y = 1.0
        if not True: box_7D470.operator_context = "EXEC_DEFAULT"
        attr_52B76 = '["' + str('Socket_28' + '"]') 
        box_7D470.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_52B76, text='Enable Noise Displacement', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_28']:
            col_28235 = box_7D470.column(heading='', align=False)
            col_28235.alert = False
            col_28235.enabled = True
            col_28235.active = True
            col_28235.use_property_split = False
            col_28235.use_property_decorate = False
            col_28235.scale_x = 1.0
            col_28235.scale_y = 1.0
            col_28235.alignment = 'Expand'.upper()
            col_28235.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_D3C6D = '["' + str('Socket_7' + '"]') 
            col_28235.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D3C6D, text='Noise Strength', icon_value=0, emboss=True)
            attr_6D7D3 = '["' + str('Socket_8' + '"]') 
            col_28235.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_6D7D3, text='Noise Scale', icon_value=0, emboss=True)
            attr_18DA5 = '["' + str('Socket_4' + '"]') 
            col_28235.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_18DA5, text='Time Evolution Multiplier', icon_value=0, emboss=True)
        box_54317 = box_B4084.box()
        box_54317.alert = False
        box_54317.enabled = True
        box_54317.active = True
        box_54317.use_property_split = False
        box_54317.use_property_decorate = False
        box_54317.alignment = 'Expand'.upper()
        box_54317.scale_x = 1.0
        box_54317.scale_y = 1.0
        if not True: box_54317.operator_context = "EXEC_DEFAULT"
        attr_FB923 = '["' + str('Socket_29' + '"]') 
        box_54317.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FB923, text='Enable Voronoi Displacement', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_29']:
            col_E8E24 = box_54317.column(heading='', align=False)
            col_E8E24.alert = False
            col_E8E24.enabled = True
            col_E8E24.active = True
            col_E8E24.use_property_split = False
            col_E8E24.use_property_decorate = False
            col_E8E24.scale_x = 1.0
            col_E8E24.scale_y = 1.0
            col_E8E24.alignment = 'Expand'.upper()
            col_E8E24.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_AEBD9 = '["' + str('Socket_21' + '"]') 
            col_E8E24.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_AEBD9, text='Voronoi Strength', icon_value=0, emboss=True)
            attr_D761F = '["' + str('Socket_20' + '"]') 
            col_E8E24.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_D761F, text='Voronoi Scale', icon_value=0, emboss=True)
            attr_6054A = '["' + str('Socket_22' + '"]') 
            col_E8E24.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_6054A, text='Time Evolution Multiplier', icon_value=0, emboss=True)
        box_554D7 = col_03A93.box()
        box_554D7.alert = False
        box_554D7.enabled = True
        box_554D7.active = True
        box_554D7.use_property_split = False
        box_554D7.use_property_decorate = False
        box_554D7.alignment = 'Expand'.upper()
        box_554D7.scale_x = 1.0
        box_554D7.scale_y = 1.0
        if not True: box_554D7.operator_context = "EXEC_DEFAULT"
        box_E2A8B = box_554D7.box()
        box_E2A8B.alert = False
        box_E2A8B.enabled = True
        box_E2A8B.active = True
        box_E2A8B.use_property_split = False
        box_E2A8B.use_property_decorate = False
        box_E2A8B.alignment = 'Expand'.upper()
        box_E2A8B.scale_x = 1.0
        box_E2A8B.scale_y = 1.0
        if not True: box_E2A8B.operator_context = "EXEC_DEFAULT"
        attr_FE6FE = '["' + str('Socket_41' + '"]') 
        box_E2A8B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_FE6FE, text='Enable Pixelate', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_41']:
            col_5DE3D = box_E2A8B.column(heading='', align=False)
            col_5DE3D.alert = False
            col_5DE3D.enabled = True
            col_5DE3D.active = True
            col_5DE3D.use_property_split = False
            col_5DE3D.use_property_decorate = False
            col_5DE3D.scale_x = 1.0
            col_5DE3D.scale_y = 1.0
            col_5DE3D.alignment = 'Expand'.upper()
            col_5DE3D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_0E515 = '["' + str('Socket_40' + '"]') 
            col_5DE3D.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_0E515, text='Pixelate Mix', icon_value=0, emboss=True)
            attr_9C041 = '["' + str('Socket_39' + '"]') 
            col_5DE3D.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], attr_9C041, text='Grid Scale', icon_value=0, emboss=True)
    else:
        box_F44AB = layout_function.box()
        box_F44AB.alert = False
        box_F44AB.enabled = 'OBJECT'==bpy.context.mode
        box_F44AB.active = True
        box_F44AB.use_property_split = False
        box_F44AB.use_property_decorate = False
        box_F44AB.alignment = 'Expand'.upper()
        box_F44AB.scale_x = 1.0
        box_F44AB.scale_y = 1.0
        if not True: box_F44AB.operator_context = "EXEC_DEFAULT"
        row_07DA9 = box_F44AB.row(heading='', align=False)
        row_07DA9.alert = False
        row_07DA9.enabled = True
        row_07DA9.active = True
        row_07DA9.use_property_split = False
        row_07DA9.use_property_decorate = False
        row_07DA9.scale_x = 1.0
        row_07DA9.scale_y = 1.0
        row_07DA9.alignment = 'Expand'.upper()
        row_07DA9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_07DA9.label(text='Animate Modifier Is Missing', icon_value=0)
        op = row_07DA9.operator('sna.dgs_render_add_animate_modifier_39c55', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)


def sna_hq_mode_function_interface_17C41(layout_function, ):
    if (bpy.context.scene.render.engine == 'BLENDER_EEVEE_NEXT'):
        pass
    else:
        box_5B434 = layout_function.box()
        box_5B434.alert = False
        box_5B434.enabled = True
        box_5B434.active = True
        box_5B434.use_property_split = False
        box_5B434.use_property_decorate = False
        box_5B434.alignment = 'Expand'.upper()
        box_5B434.scale_x = 1.0
        box_5B434.scale_y = 1.0
        if not True: box_5B434.operator_context = "EXEC_DEFAULT"
        box_5B434.label(text='Eevee is not enabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
    if (bpy.context.scene.camera == None):
        box_9AC8C = layout_function.box()
        box_9AC8C.alert = False
        box_9AC8C.enabled = True
        box_9AC8C.active = True
        box_9AC8C.use_property_split = False
        box_9AC8C.use_property_decorate = False
        box_9AC8C.alignment = 'Expand'.upper()
        box_9AC8C.scale_x = 1.0
        box_9AC8C.scale_y = 1.0
        if not True: box_9AC8C.operator_context = "EXEC_DEFAULT"
        box_9AC8C.label(text='No Active Camera', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_9AC8C.label(text='         HQ Materials Require An Active Camera', icon_value=0)
    col_249D2 = layout_function.column(heading='', align=False)
    col_249D2.alert = False
    col_249D2.enabled = True
    col_249D2.active = True
    col_249D2.use_property_split = False
    col_249D2.use_property_decorate = False
    col_249D2.scale_x = 1.0
    col_249D2.scale_y = 1.0
    col_249D2.alignment = 'Expand'.upper()
    col_249D2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if bpy.context.scene.sna_dgs_scene_properties.show_tips:
        box_AEE3F = col_249D2.box()
        box_AEE3F.alert = False
        box_AEE3F.enabled = True
        box_AEE3F.active = True
        box_AEE3F.use_property_split = False
        box_AEE3F.use_property_decorate = False
        box_AEE3F.alignment = 'Expand'.upper()
        box_AEE3F.scale_x = 1.0
        box_AEE3F.scale_y = 1.0
        if not True: box_AEE3F.operator_context = "EXEC_DEFAULT"
        box_AEE3F.label(text='LQ Mode requires high samples (64+)', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_AEE3F.label(text='Samples can be set to 1 in HQ Mode', icon_value=0)
        box_AEE3F.label(text="if 'Shadeless' materials are used", icon_value=0)
    if bpy.context.scene.eevee.use_taa_reprojection:
        box_06ADA = col_249D2.box()
        box_06ADA.alert = False
        box_06ADA.enabled = True
        box_06ADA.active = True
        box_06ADA.use_property_split = False
        box_06ADA.use_property_decorate = False
        box_06ADA.alignment = 'Expand'.upper()
        box_06ADA.scale_x = 1.0
        box_06ADA.scale_y = 1.0
        if not True: box_06ADA.operator_context = "EXEC_DEFAULT"
        box_06ADA.label(text='Temporal Reprojection is a enabled ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_06ADA.label(text='         This can cause flickering', icon_value=0)
    box_0F8BF = col_249D2.box()
    box_0F8BF.alert = False
    box_0F8BF.enabled = True
    box_0F8BF.active = True
    box_0F8BF.use_property_split = False
    box_0F8BF.use_property_decorate = False
    box_0F8BF.alignment = 'Expand'.upper()
    box_0F8BF.scale_x = 1.0
    box_0F8BF.scale_y = 1.0
    if not True: box_0F8BF.operator_context = "EXEC_DEFAULT"
    col_E83D4 = box_0F8BF.column(heading='', align=False)
    col_E83D4.alert = False
    col_E83D4.enabled = True
    col_E83D4.active = True
    col_E83D4.use_property_split = False
    col_E83D4.use_property_decorate = False
    col_E83D4.scale_x = 1.0
    col_E83D4.scale_y = 1.0
    col_E83D4.alignment = 'Expand'.upper()
    col_E83D4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_E83D4.prop(bpy.context.scene.eevee, 'taa_samples', text='Eevee Viewport Samples', icon_value=0, emboss=True)
    col_E83D4.prop(bpy.context.scene.eevee, 'taa_render_samples', text='Eevee Render Samples', icon_value=0, emboss=True)
    if bpy.context.scene.eevee.use_taa_reprojection:
        box_6EA64 = col_249D2.box()
        box_6EA64.alert = False
        box_6EA64.enabled = True
        box_6EA64.active = True
        box_6EA64.use_property_split = False
        box_6EA64.use_property_decorate = False
        box_6EA64.alignment = 'Expand'.upper()
        box_6EA64.scale_x = 1.0
        box_6EA64.scale_y = 1.0
        if not True: box_6EA64.operator_context = "EXEC_DEFAULT"
        box_6EA64.prop(bpy.context.scene.eevee, 'use_taa_reprojection', text='Temporal Reprojection', icon_value=0, emboss=True)
    col_249D2.separator(factor=1.0)
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        for i_E3C27 in range(len(bpy.context.view_layer.objects.active.material_slots)):
            if (bpy.context.view_layer.objects.active.material_slots[i_E3C27].material == None):
                pass
            else:
                box_2E343 = col_249D2.box()
                box_2E343.alert = False
                box_2E343.enabled = True
                box_2E343.active = True
                box_2E343.use_property_split = False
                box_2E343.use_property_decorate = False
                box_2E343.alignment = 'Expand'.upper()
                box_2E343.scale_x = 1.0
                box_2E343.scale_y = 1.0
                if not True: box_2E343.operator_context = "EXEC_DEFAULT"
                row_19BC2 = box_2E343.row(heading='', align=False)
                row_19BC2.alert = False
                row_19BC2.enabled = True
                row_19BC2.active = True
                row_19BC2.use_property_split = False
                row_19BC2.use_property_decorate = False
                row_19BC2.scale_x = 1.0
                row_19BC2.scale_y = 1.0
                row_19BC2.alignment = 'Expand'.upper()
                row_19BC2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_19BC2.label(text=str(bpy.context.view_layer.objects.active.material_slots[i_E3C27].material.name), icon_value=0)
                box_2E343.prop(bpy.context.view_layer.objects.active.material_slots[i_E3C27].material.sna_dgs_material_properties, 'lq_hq', text='', icon_value=0, emboss=True)
    col_249D2.separator(factor=1.0)
    box_D2847 = col_249D2.box()
    box_D2847.alert = False
    box_D2847.enabled = True
    box_D2847.active = True
    box_D2847.use_property_split = False
    box_D2847.use_property_decorate = False
    box_D2847.alignment = 'Expand'.upper()
    box_D2847.scale_x = 1.0
    box_D2847.scale_y = 1.0
    if not True: box_D2847.operator_context = "EXEC_DEFAULT"
    box_D2847.prop(bpy.context.scene.sna_dgs_scene_properties, 'hq_overlap', text='HQ Objects Overlap', icon_value=0, emboss=True, toggle=False)
    if bpy.context.scene.sna_dgs_scene_properties.hq_overlap:
        box_0826A = col_249D2.box()
        box_0826A.alert = False
        box_0826A.enabled = True
        box_0826A.active = True
        box_0826A.use_property_split = False
        box_0826A.use_property_decorate = False
        box_0826A.alignment = 'Expand'.upper()
        box_0826A.scale_x = 1.0
        box_0826A.scale_y = 1.0
        if not True: box_0826A.operator_context = "EXEC_DEFAULT"
        if (property_exists("bpy.context.scene.objects", globals(), locals()) and 'KIRI_HQ_Merged_Object' in bpy.context.scene.objects):
            box_BEFDD = box_0826A.box()
            box_BEFDD.alert = False
            box_BEFDD.enabled = False
            box_BEFDD.active = True
            box_BEFDD.use_property_split = False
            box_BEFDD.use_property_decorate = False
            box_BEFDD.alignment = 'Expand'.upper()
            box_BEFDD.scale_x = 1.0
            box_BEFDD.scale_y = 1.0
            if not True: box_BEFDD.operator_context = "EXEC_DEFAULT"
            box_BEFDD.label(text='HQ Object Already Exists', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            op = box_BEFDD.operator('sna.dgs_render_generate_hq_object_55455', text='Generate HQ Object', icon_value=0, emboss=True, depress=False)
        else:
            op = box_0826A.operator('sna.dgs_render_generate_hq_object_55455', text='Generate HQ Object', icon_value=0, emboss=True, depress=False)





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
    if bpy.context.scene.sna_dgs_scene_properties.show_tips:
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
        box_599AC.label(text='Do not apply rotation or scale', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_599AC.label(text="using Blender's native Apply Transforms", icon_value=0)
        box_599AC.label(text="Use the addon's Apply 3DGS Transforms", icon_value=0)
        box_599AC.label(text='Higher SH bands will not be updated', icon_value=0)
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
        box_37F67.label(text='For performance and similarity to', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_37F67.label(text='Render mode results, import as Verts', icon_value=0)
        box_37F67.label(text='For Vertex Painting, and fine ', icon_value=0)
        box_37F67.label(text='manual editing, import as Faces.', icon_value=0)
        box_32768 = col_9F76F.box()
        box_32768.alert = False
        box_32768.enabled = True
        box_32768.active = True
        box_32768.use_property_split = False
        box_32768.use_property_decorate = False
        box_32768.alignment = 'Expand'.upper()
        box_32768.scale_x = 1.0
        box_32768.scale_y = 1.0
        if not True: box_32768.operator_context = "EXEC_DEFAULT"
        box_32768.label(text='Face imported objects will be', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_32768.label(text="'Disabled In Viewport' in Render mode", icon_value=0)
        box_32768.label(text='If your objects disappears. Check viewport', icon_value=0)
        box_32768.label(text='disable settings in the outliner', icon_value=0)
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
            box_3BEA2.label(text='For best results use Eevee', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_3BEA2.label(text='Cycles can be used with high', icon_value=0)
            box_3BEA2.label(text='transparent bounces', icon_value=0)




def sna_modify_menu_AEA26(layout_function, ):
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
    col_4F908 = box_0B550.column(heading='', align=True)
    col_4F908.alert = False
    col_4F908.enabled = True
    col_4F908.active = True
    col_4F908.use_property_split = False
    col_4F908.use_property_decorate = False
    col_4F908.scale_x = 1.0
    col_4F908.scale_y = 1.0
    col_4F908.alignment = 'Expand'.upper()
    col_4F908.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_4F908.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = col_4F908.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)
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


def sna_adjust_attributes_AB643(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Attributes_GN' in bpy.context.view_layer.objects.active.modifiers):
        col_15AC3 = layout_function.column(heading='', align=False)
        col_15AC3.alert = False
        col_15AC3.enabled = True
        col_15AC3.active = True
        col_15AC3.use_property_split = False
        col_15AC3.use_property_decorate = False
        col_15AC3.scale_x = 1.0
        col_15AC3.scale_y = 1.0
        col_15AC3.alignment = 'Expand'.upper()
        col_15AC3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        layout_function = col_15AC3
        sna_attribute_adjust_properties_2C323(layout_function, )
        box_6671A = col_15AC3.box()
        box_6671A.alert = False
        box_6671A.enabled = True
        box_6671A.active = True
        box_6671A.use_property_split = False
        box_6671A.use_property_decorate = False
        box_6671A.alignment = 'Expand'.upper()
        box_6671A.scale_x = 1.0
        box_6671A.scale_y = 1.0
        if not True: box_6671A.operator_context = "EXEC_DEFAULT"
        box_6671A.label(text='Accurate value changes may only ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_6671A.label(text='be visible in Render mode and external', icon_value=0)
        box_6671A.label(text='3DGS viewers. This modifier will show in', icon_value=0)
        box_6671A.label(text='Render mode for the active object.', icon_value=0)
    else:
        box_6555D = layout_function.box()
        box_6555D.alert = False
        box_6555D.enabled = 'OBJECT'==bpy.context.mode
        box_6555D.active = True
        box_6555D.use_property_split = False
        box_6555D.use_property_decorate = False
        box_6555D.alignment = 'Expand'.upper()
        box_6555D.scale_x = 1.0
        box_6555D.scale_y = 1.0
        if not True: box_6555D.operator_context = "EXEC_DEFAULT"
        row_220DB = box_6555D.row(heading='', align=False)
        row_220DB.alert = False
        row_220DB.enabled = True
        row_220DB.active = True
        row_220DB.use_property_split = False
        row_220DB.use_property_decorate = False
        row_220DB.scale_x = 1.0
        row_220DB.scale_y = 1.0
        row_220DB.alignment = 'Expand'.upper()
        row_220DB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_220DB.label(text='Adjust Attributes', icon_value=0)
        op = row_220DB.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Adjust_Attributes_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Adjust_Attributes_GN'


def sna_attribute_adjust_properties_2C323(layout_function, ):
    box_C40B6 = layout_function.box()
    box_C40B6.alert = False
    box_C40B6.enabled = True
    box_C40B6.active = True
    box_C40B6.use_property_split = False
    box_C40B6.use_property_decorate = False
    box_C40B6.alignment = 'Expand'.upper()
    box_C40B6.scale_x = 1.0
    box_C40B6.scale_y = 1.0
    if not True: box_C40B6.operator_context = "EXEC_DEFAULT"
    split_B43D4 = box_C40B6.split(factor=0.5, align=False)
    split_B43D4.alert = False
    split_B43D4.enabled = True
    split_B43D4.active = True
    split_B43D4.use_property_split = False
    split_B43D4.use_property_decorate = False
    split_B43D4.scale_x = 1.0
    split_B43D4.scale_y = 1.0
    split_B43D4.alignment = 'Expand'.upper()
    if not True: split_B43D4.operator_context = "EXEC_DEFAULT"
    split_B43D4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], 'show_viewport', text='Adjust Attributes', icon_value=0, emboss=True, toggle=True)
    row_3EABC = split_B43D4.row(heading='', align=True)
    row_3EABC.alert = False
    row_3EABC.enabled = True
    row_3EABC.active = True
    row_3EABC.use_property_split = False
    row_3EABC.use_property_decorate = False
    row_3EABC.scale_x = 1.0
    row_3EABC.scale_y = 1.0
    row_3EABC.alignment = 'Right'.upper()
    row_3EABC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_3EABC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
    op = row_3EABC.operator('sna.dgs_render_apply_adjust_attribute_modifier_b24a5', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
    op = row_3EABC.operator('sna.dgs_render_remove_adjust_attribute_modifier_c5491', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
    box_F28C4 = box_C40B6.box()
    box_F28C4.alert = False
    box_F28C4.enabled = True
    box_F28C4.active = True
    box_F28C4.use_property_split = False
    box_F28C4.use_property_decorate = False
    box_F28C4.alignment = 'Expand'.upper()
    box_F28C4.scale_x = 1.0
    box_F28C4.scale_y = 1.0
    if not True: box_F28C4.operator_context = "EXEC_DEFAULT"
    op = box_F28C4.operator('sna.dgs_render_remove_higher_sh_attributes_cb703', text='Remove Higher SH Attributes', icon_value=0, emboss=True, depress=False)
    col_4C14E = box_C40B6.column(heading='', align=True)
    col_4C14E.alert = False
    col_4C14E.enabled = True
    col_4C14E.active = True
    col_4C14E.use_property_split = False
    col_4C14E.use_property_decorate = False
    col_4C14E.scale_x = 1.0
    col_4C14E.scale_y = 1.0
    col_4C14E.alignment = 'Expand'.upper()
    col_4C14E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    attr_E874B = '["' + str('Socket_3' + '"]') 
    col_4C14E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_E874B, text='Scale Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_3']:
        col_31C13 = col_4C14E.column(heading='', align=True)
        col_31C13.alert = False
        col_31C13.enabled = True
        col_31C13.active = True
        col_31C13.use_property_split = False
        col_31C13.use_property_decorate = False
        col_31C13.scale_x = 1.0
        col_31C13.scale_y = 1.0
        col_31C13.alignment = 'Expand'.upper()
        col_31C13.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_2C986 = '["' + str('Socket_6' + '"]') 
        col_31C13.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_2C986, text='', icon_value=0, emboss=True, toggle=True)
        if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_6'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_6'] == 3)):
            box_EE993 = col_31C13.box()
            box_EE993.alert = False
            box_EE993.enabled = True
            box_EE993.active = True
            box_EE993.use_property_split = False
            box_EE993.use_property_decorate = False
            box_EE993.alignment = 'Expand'.upper()
            box_EE993.scale_x = 1.0
            box_EE993.scale_y = 1.0
            if not True: box_EE993.operator_context = "EXEC_DEFAULT"
            box_EE993.label(text='Change values slowly to avoid crashes', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        attr_120DC = '["' + str('Socket_8' + '"]') 
        col_31C13.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_120DC, text='', icon_value=0, emboss=True, toggle=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_8'] == 0):
            attr_B4207 = '["' + str('Socket_5' + '"]') 
            col_31C13.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_B4207, text='All Scales', icon_value=0, emboss=True, toggle=True)
        else:
            col_9E5AF = col_31C13.column(heading='', align=False)
            col_9E5AF.alert = False
            col_9E5AF.enabled = True
            col_9E5AF.active = True
            col_9E5AF.use_property_split = False
            col_9E5AF.use_property_decorate = False
            col_9E5AF.scale_x = 1.0
            col_9E5AF.scale_y = 1.0
            col_9E5AF.alignment = 'Expand'.upper()
            col_9E5AF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_734DA = '["' + str('Socket_10' + '"]') 
            col_9E5AF.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_734DA, text='Scale_0', icon_value=0, emboss=True, toggle=True)
            attr_EAC87 = '["' + str('Socket_9' + '"]') 
            col_9E5AF.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_EAC87, text='Scale_1', icon_value=0, emboss=True, toggle=True)
            attr_F45C1 = '["' + str('Socket_7' + '"]') 
            col_9E5AF.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_F45C1, text='Scale_2', icon_value=0, emboss=True, toggle=True)
    col_75DFB = box_C40B6.column(heading='', align=True)
    col_75DFB.alert = False
    col_75DFB.enabled = True
    col_75DFB.active = True
    col_75DFB.use_property_split = False
    col_75DFB.use_property_decorate = False
    col_75DFB.scale_x = 1.0
    col_75DFB.scale_y = 1.0
    col_75DFB.alignment = 'Expand'.upper()
    col_75DFB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    attr_670D5 = '["' + str('Socket_4' + '"]') 
    col_75DFB.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_670D5, text='Rotation Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_4']:
        col_B2D6A = col_75DFB.column(heading='', align=True)
        col_B2D6A.alert = False
        col_B2D6A.enabled = True
        col_B2D6A.active = True
        col_B2D6A.use_property_split = False
        col_B2D6A.use_property_decorate = False
        col_B2D6A.scale_x = 1.0
        col_B2D6A.scale_y = 1.0
        col_B2D6A.alignment = 'Expand'.upper()
        col_B2D6A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_85A74 = '["' + str('Socket_48' + '"]') 
        col_B2D6A.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_85A74, text='', icon_value=0, emboss=True, toggle=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_48'] == 0):
            col_125B4 = col_B2D6A.column(heading='', align=True)
            col_125B4.alert = False
            col_125B4.enabled = True
            col_125B4.active = True
            col_125B4.use_property_split = False
            col_125B4.use_property_decorate = False
            col_125B4.scale_x = 1.0
            col_125B4.scale_y = 1.0
            col_125B4.alignment = 'Expand'.upper()
            col_125B4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_389BC = '["' + str('Socket_21' + '"]') 
            col_125B4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_389BC, text='Rotation', icon_value=0, emboss=True, toggle=True)
        else:
            col_F40AA = col_B2D6A.column(heading='', align=True)
            col_F40AA.alert = False
            col_F40AA.enabled = True
            col_F40AA.active = True
            col_F40AA.use_property_split = False
            col_F40AA.use_property_decorate = False
            col_F40AA.scale_x = 1.0
            col_F40AA.scale_y = 1.0
            col_F40AA.alignment = 'Expand'.upper()
            col_F40AA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_6DFDA = '["' + str('Socket_51' + '"]') 
            col_F40AA.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_6DFDA, text='Axis', icon_value=0, emboss=True, toggle=True)
            attr_E15B5 = '["' + str('Socket_50' + '"]') 
            col_F40AA.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_E15B5, text='Target', icon_value=0, emboss=True, toggle=True)
    col_0C20D = box_C40B6.column(heading='', align=True)
    col_0C20D.alert = False
    col_0C20D.enabled = True
    col_0C20D.active = True
    col_0C20D.use_property_split = False
    col_0C20D.use_property_decorate = False
    col_0C20D.scale_x = 1.0
    col_0C20D.scale_y = 1.0
    col_0C20D.alignment = 'Expand'.upper()
    col_0C20D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    attr_D2232 = '["' + str('Socket_54' + '"]') 
    col_0C20D.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_D2232, text='Opacity Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_54']:
        col_F6DA7 = col_0C20D.column(heading='', align=True)
        col_F6DA7.alert = False
        col_F6DA7.enabled = True
        col_F6DA7.active = True
        col_F6DA7.use_property_split = False
        col_F6DA7.use_property_decorate = False
        col_F6DA7.scale_x = 1.0
        col_F6DA7.scale_y = 1.0
        col_F6DA7.alignment = 'Expand'.upper()
        col_F6DA7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_7BD79 = '["' + str('Socket_52' + '"]') 
        col_F6DA7.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_7BD79, text='', icon_value=0, emboss=True, toggle=True)
        if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_52'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_52'] == 3)):
            box_E8A8F = col_F6DA7.box()
            box_E8A8F.alert = False
            box_E8A8F.enabled = True
            box_E8A8F.active = True
            box_E8A8F.use_property_split = False
            box_E8A8F.use_property_decorate = False
            box_E8A8F.alignment = 'Expand'.upper()
            box_E8A8F.scale_x = 1.0
            box_E8A8F.scale_y = 1.0
            if not True: box_E8A8F.operator_context = "EXEC_DEFAULT"
            box_E8A8F.label(text='Change values slowly to avoid crashes', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        attr_20728 = '["' + str('Socket_55' + '"]') 
        col_F6DA7.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_20728, text='All Scales', icon_value=0, emboss=True, toggle=True)
    col_CADFD = box_C40B6.column(heading='', align=True)
    col_CADFD.alert = False
    col_CADFD.enabled = True
    col_CADFD.active = True
    col_CADFD.use_property_split = False
    col_CADFD.use_property_decorate = False
    col_CADFD.scale_x = 1.0
    col_CADFD.scale_y = 1.0
    col_CADFD.alignment = 'Expand'.upper()
    col_CADFD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    attr_9A41E = '["' + str('Socket_23' + '"]') 
    col_CADFD.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_9A41E, text='SH 1 Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_23']:
        col_83806 = col_CADFD.column(heading='', align=True)
        col_83806.alert = False
        col_83806.enabled = True
        col_83806.active = True
        col_83806.use_property_split = True
        col_83806.use_property_decorate = False
        col_83806.scale_x = 1.0
        col_83806.scale_y = 1.0
        col_83806.alignment = 'Expand'.upper()
        col_83806.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_31D21 = '["' + str('Socket_24' + '"]') 
        col_83806.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_31D21, text='Red Adjust Type', icon_value=0, emboss=True, expand=False, toggle=True)
        attr_0574B = '["' + str('Socket_25' + '"]') 
        col_83806.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_0574B, text='', icon_value=0, emboss=True, toggle=True)
        attr_1A2E2 = '["' + str('Socket_30' + '"]') 
        col_83806.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_1A2E2, text='Green Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_8AA4D = '["' + str('Socket_31' + '"]') 
        col_83806.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_8AA4D, text='', icon_value=0, emboss=True, toggle=True)
        attr_FA4D9 = '["' + str('Socket_32' + '"]') 
        col_83806.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_FA4D9, text='Blue Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_955F9 = '["' + str('Socket_33' + '"]') 
        col_83806.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_955F9, text='', icon_value=0, emboss=True, toggle=True)
    col_F20A7 = box_C40B6.column(heading='', align=True)
    col_F20A7.alert = False
    col_F20A7.enabled = True
    col_F20A7.active = True
    col_F20A7.use_property_split = False
    col_F20A7.use_property_decorate = False
    col_F20A7.scale_x = 1.0
    col_F20A7.scale_y = 1.0
    col_F20A7.alignment = 'Expand'.upper()
    col_F20A7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    attr_86E8C = '["' + str('Socket_34' + '"]') 
    col_F20A7.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_86E8C, text='SH 2 Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_34']:
        col_41831 = col_F20A7.column(heading='', align=True)
        col_41831.alert = False
        col_41831.enabled = True
        col_41831.active = True
        col_41831.use_property_split = True
        col_41831.use_property_decorate = False
        col_41831.scale_x = 1.0
        col_41831.scale_y = 1.0
        col_41831.alignment = 'Expand'.upper()
        col_41831.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_EE5FE = '["' + str('Socket_35' + '"]') 
        col_41831.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_EE5FE, text='Red Adjust Type', icon_value=0, emboss=True, expand=False, toggle=True)
        attr_380DC = '["' + str('Socket_36' + '"]') 
        col_41831.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_380DC, text='', icon_value=0, emboss=True, toggle=True)
        attr_B1895 = '["' + str('Socket_37' + '"]') 
        col_41831.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_B1895, text='Green Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_1937E = '["' + str('Socket_38' + '"]') 
        col_41831.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_1937E, text='', icon_value=0, emboss=True, toggle=True)
        attr_609BB = '["' + str('Socket_42' + '"]') 
        col_41831.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_609BB, text='Blue Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_75F7B = '["' + str('Socket_43' + '"]') 
        col_41831.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_75F7B, text='', icon_value=0, emboss=True, toggle=True)
    col_1D52E = box_C40B6.column(heading='', align=True)
    col_1D52E.alert = False
    col_1D52E.enabled = True
    col_1D52E.active = True
    col_1D52E.use_property_split = False
    col_1D52E.use_property_decorate = False
    col_1D52E.scale_x = 1.0
    col_1D52E.scale_y = 1.0
    col_1D52E.alignment = 'Expand'.upper()
    col_1D52E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    attr_73E08 = '["' + str('Socket_39' + '"]') 
    col_1D52E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_73E08, text='SH 3 Attributes', icon_value=0, emboss=True, toggle=False)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN']['Socket_39']:
        col_9E249 = col_1D52E.column(heading='', align=True)
        col_9E249.alert = False
        col_9E249.enabled = True
        col_9E249.active = True
        col_9E249.use_property_split = True
        col_9E249.use_property_decorate = False
        col_9E249.scale_x = 1.0
        col_9E249.scale_y = 1.0
        col_9E249.alignment = 'Expand'.upper()
        col_9E249.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_E35A2 = '["' + str('Socket_40' + '"]') 
        col_9E249.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_E35A2, text='Red Adjust Type', icon_value=0, emboss=True, expand=False, toggle=True)
        attr_4369F = '["' + str('Socket_41' + '"]') 
        col_9E249.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_4369F, text='', icon_value=0, emboss=True, toggle=True)
        attr_DAC40 = '["' + str('Socket_44' + '"]') 
        col_9E249.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_DAC40, text='Green Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_BE5C0 = '["' + str('Socket_45' + '"]') 
        col_9E249.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_BE5C0, text='', icon_value=0, emboss=True, toggle=True)
        attr_A4AC7 = '["' + str('Socket_46' + '"]') 
        col_9E249.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_A4AC7, text='Blue Adjust Type', icon_value=0, emboss=True, toggle=True)
        attr_33CFF = '["' + str('Socket_47' + '"]') 
        col_9E249.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], attr_33CFF, text='', icon_value=0, emboss=True, toggle=True)



def sna_camera_cull_8069C(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Camera_Cull_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_7279D = layout_function.box()
        box_7279D.alert = False
        box_7279D.enabled = True
        box_7279D.active = True
        box_7279D.use_property_split = False
        box_7279D.use_property_decorate = False
        box_7279D.alignment = 'Expand'.upper()
        box_7279D.scale_x = 1.0
        box_7279D.scale_y = 1.0
        if not True: box_7279D.operator_context = "EXEC_DEFAULT"
        split_D5A9B = box_7279D.split(factor=0.5, align=False)
        split_D5A9B.alert = False
        split_D5A9B.enabled = True
        split_D5A9B.active = True
        split_D5A9B.use_property_split = False
        split_D5A9B.use_property_decorate = False
        split_D5A9B.scale_x = 1.0
        split_D5A9B.scale_y = 1.0
        split_D5A9B.alignment = 'Expand'.upper()
        if not True: split_D5A9B.operator_context = "EXEC_DEFAULT"
        split_D5A9B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], 'show_viewport', text='Camera Cull', icon_value=0, emboss=True, toggle=True)
        row_F9B38 = split_D5A9B.row(heading='', align=True)
        row_F9B38.alert = False
        row_F9B38.enabled = True
        row_F9B38.active = True
        row_F9B38.use_property_split = False
        row_F9B38.use_property_decorate = False
        row_F9B38.scale_x = 1.0
        row_F9B38.scale_y = 1.0
        row_F9B38.alignment = 'Right'.upper()
        row_F9B38.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_F9B38.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_F9B38.operator('sna.dgs_render_apply_camera_cull_modifier_7c6f7', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_F9B38.operator('sna.dgs_render_remove_camera_cull_modifier_f15ee', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        if (bpy.context.scene.camera == None):
            box_07B9F = box_7279D.box()
            box_07B9F.alert = False
            box_07B9F.enabled = True
            box_07B9F.active = True
            box_07B9F.use_property_split = False
            box_07B9F.use_property_decorate = False
            box_07B9F.alignment = 'Expand'.upper()
            box_07B9F.scale_x = 1.0
            box_07B9F.scale_y = 1.0
            if not True: box_07B9F.operator_context = "EXEC_DEFAULT"
            box_07B9F.label(text='No Active Camera In Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        else:
            col_A2A21 = box_7279D.column(heading='', align=True)
            col_A2A21.alert = False
            col_A2A21.enabled = True
            col_A2A21.active = True
            col_A2A21.use_property_split = False
            col_A2A21.use_property_decorate = False
            col_A2A21.scale_x = 1.0
            col_A2A21.scale_y = 1.0
            col_A2A21.alignment = 'Expand'.upper()
            col_A2A21.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_A2A21.operator('sna.dgs_render_auto_set_up_camera_cull_properties_aef48', text='Auto Set Up', icon_value=0, emboss=True, depress=False)
            attr_31E14 = '["' + str('Socket_2' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_31E14, text='X Resolution', icon_value=0, emboss=True)
            attr_626D2 = '["' + str('Socket_3' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_626D2, text='Y Resolution', icon_value=0, emboss=True)
            attr_A688C = '["' + str('Socket_4' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_A688C, text='Focal Length', icon_value=0, emboss=True)
            attr_CC516 = '["' + str('Socket_5' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_CC516, text='Sensor Width', icon_value=0, emboss=True)
            attr_7333B = '["' + str('Socket_6' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_7333B, text='Padding', icon_value=0, emboss=True)
            attr_34623 = '["' + str('Socket_13' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_34623, text='Closer Than', icon_value=0, emboss=True)
            attr_45049 = '["' + str('Socket_14' + '"]') 
            col_A2A21.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_45049, text='Further Than', icon_value=0, emboss=True)
    else:
        box_05674 = layout_function.box()
        box_05674.alert = False
        box_05674.enabled = 'OBJECT'==bpy.context.mode
        box_05674.active = True
        box_05674.use_property_split = False
        box_05674.use_property_decorate = False
        box_05674.alignment = 'Expand'.upper()
        box_05674.scale_x = 1.0
        box_05674.scale_y = 1.0
        if not True: box_05674.operator_context = "EXEC_DEFAULT"
        row_B29D4 = box_05674.row(heading='', align=False)
        row_B29D4.alert = False
        row_B29D4.enabled = True
        row_B29D4.active = True
        row_B29D4.use_property_split = False
        row_B29D4.use_property_decorate = False
        row_B29D4.scale_x = 1.0
        row_B29D4.scale_y = 1.0
        row_B29D4.alignment = 'Expand'.upper()
        row_B29D4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_B29D4.label(text='Camera Cull', icon_value=0)
        op = row_B29D4.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Camera_Cull_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Camera_Cull_GN'


def sna_colour_edit_37123(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Colour_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_1A729 = layout_function.box()
        box_1A729.alert = False
        box_1A729.enabled = True
        box_1A729.active = True
        box_1A729.use_property_split = False
        box_1A729.use_property_decorate = False
        box_1A729.alignment = 'Expand'.upper()
        box_1A729.scale_x = 1.0
        box_1A729.scale_y = 1.0
        if not True: box_1A729.operator_context = "EXEC_DEFAULT"
        split_A4B39 = box_1A729.split(factor=0.5, align=False)
        split_A4B39.alert = False
        split_A4B39.enabled = True
        split_A4B39.active = True
        split_A4B39.use_property_split = False
        split_A4B39.use_property_decorate = False
        split_A4B39.scale_x = 1.0
        split_A4B39.scale_y = 1.0
        split_A4B39.alignment = 'Expand'.upper()
        if not True: split_A4B39.operator_context = "EXEC_DEFAULT"
        split_A4B39.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], 'show_viewport', text='Colour Edit', icon_value=0, emboss=True, toggle=True)
        row_7335E = split_A4B39.row(heading='', align=True)
        row_7335E.alert = False
        row_7335E.enabled = True
        row_7335E.active = True
        row_7335E.use_property_split = False
        row_7335E.use_property_decorate = False
        row_7335E.scale_x = 1.0
        row_7335E.scale_y = 1.0
        row_7335E.alignment = 'Right'.upper()
        row_7335E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_7335E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_7335E.operator('sna.dgs_render_apply_colour_edit_modifier_c83c4', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_7335E.operator('sna.dgs_render_remove_colour_edit_modifier_6255f', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        col_836C0 = box_1A729.column(heading='', align=True)
        col_836C0.alert = False
        col_836C0.enabled = True
        col_836C0.active = True
        col_836C0.use_property_split = False
        col_836C0.use_property_decorate = False
        col_836C0.scale_x = 1.0
        col_836C0.scale_y = 1.0
        col_836C0.alignment = 'Expand'.upper()
        col_836C0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_64F25 = '["' + str('Socket_4' + '"]') 
        col_836C0.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_64F25, text='', icon_value=0, emboss=True)
        attr_F9B60 = '["' + str('Socket_2' + '"]') 
        col_836C0.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_F9B60, text='', icon_value=0, emboss=True)
        if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_4'] == 0) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_4'] == 1)):
            col_A8E1B = col_836C0.column(heading='', align=False)
            col_A8E1B.alert = False
            col_A8E1B.enabled = True
            col_A8E1B.active = True
            col_A8E1B.use_property_split = False
            col_A8E1B.use_property_decorate = False
            col_A8E1B.scale_x = 1.0
            col_A8E1B.scale_y = 1.0
            col_A8E1B.alignment = 'Expand'.upper()
            col_A8E1B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_10C7C = '["' + str('Socket_3' + '"]') 
            col_A8E1B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_10C7C, text='Hue Threshold', icon_value=0, emboss=True)
            attr_8DE4C = '["' + str('Socket_6' + '"]') 
            col_A8E1B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_8DE4C, text='Saturation Threshold', icon_value=0, emboss=True)
            attr_E480B = '["' + str('Socket_7' + '"]') 
            col_A8E1B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_E480B, text='Value Threshold', icon_value=0, emboss=True)
        col_85E9D = box_1A729.column(heading='', align=False)
        col_85E9D.alert = False
        col_85E9D.enabled = True
        col_85E9D.active = True
        col_85E9D.use_property_split = False
        col_85E9D.use_property_decorate = False
        col_85E9D.scale_x = 1.0
        col_85E9D.scale_y = 1.0
        col_85E9D.alignment = 'Expand'.upper()
        col_85E9D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_7F527 = '["' + str('Socket_11' + '"]') 
        col_85E9D.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_7F527, text='Colour Edit Masking', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_11']:
            col_758DD = col_85E9D.column(heading='', align=False)
            col_758DD.alert = False
            col_758DD.enabled = True
            col_758DD.active = True
            col_758DD.use_property_split = False
            col_758DD.use_property_decorate = False
            col_758DD.scale_x = 1.0
            col_758DD.scale_y = 1.0
            col_758DD.alignment = 'Expand'.upper()
            col_758DD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_C4FB4 = '["' + str('Socket_8' + '"]') 
            col_758DD.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_C4FB4, text='', icon_value=0, emboss=True, toggle=True)
            attr_0B7C4 = '["' + str('Socket_9' + '"]') 
            col_758DD.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_0B7C4, text='', icon_value=0, emboss=True, toggle=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_8'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_8'] == 3)):
                attr_4B792 = '["' + str('Socket_12' + '"]') 
                col_758DD.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_4B792, text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_2F40B = layout_function.box()
        box_2F40B.alert = False
        box_2F40B.enabled = 'OBJECT'==bpy.context.mode
        box_2F40B.active = True
        box_2F40B.use_property_split = False
        box_2F40B.use_property_decorate = False
        box_2F40B.alignment = 'Expand'.upper()
        box_2F40B.scale_x = 1.0
        box_2F40B.scale_y = 1.0
        if not True: box_2F40B.operator_context = "EXEC_DEFAULT"
        row_78C95 = box_2F40B.row(heading='', align=False)
        row_78C95.alert = False
        row_78C95.enabled = True
        row_78C95.active = True
        row_78C95.use_property_split = False
        row_78C95.use_property_decorate = False
        row_78C95.scale_x = 1.0
        row_78C95.scale_y = 1.0
        row_78C95.alignment = 'Expand'.upper()
        row_78C95.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_78C95.label(text='Color Edit', icon_value=0)
        op = row_78C95.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Colour_Edit_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Colour_Edit_GN'



def sna_convert_to_rough_mesh_BF549(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Convert_To_Rough_Mesh_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_F10CF = layout_function.box()
        box_F10CF.alert = False
        box_F10CF.enabled = True
        box_F10CF.active = True
        box_F10CF.use_property_split = False
        box_F10CF.use_property_decorate = False
        box_F10CF.alignment = 'Expand'.upper()
        box_F10CF.scale_x = 1.0
        box_F10CF.scale_y = 1.0
        if not True: box_F10CF.operator_context = "EXEC_DEFAULT"
        split_CD9F1 = box_F10CF.split(factor=0.5, align=False)
        split_CD9F1.alert = False
        split_CD9F1.enabled = True
        split_CD9F1.active = True
        split_CD9F1.use_property_split = False
        split_CD9F1.use_property_decorate = False
        split_CD9F1.scale_x = 1.0
        split_CD9F1.scale_y = 1.0
        split_CD9F1.alignment = 'Expand'.upper()
        if not True: split_CD9F1.operator_context = "EXEC_DEFAULT"
        split_CD9F1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], 'show_viewport', text='Convert To Rough Mesh', icon_value=0, emboss=True, toggle=True)
        row_9D884 = split_CD9F1.row(heading='', align=True)
        row_9D884.alert = False
        row_9D884.enabled = True
        row_9D884.active = True
        row_9D884.use_property_split = False
        row_9D884.use_property_decorate = False
        row_9D884.scale_x = 1.0
        row_9D884.scale_y = 1.0
        row_9D884.alignment = 'Right'.upper()
        row_9D884.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_9D884.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_9D884.operator('sna.dgs_render_apply_convert_to_rough_mesh_modifier_9f4b2', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_9D884.operator('sna.dgs_render_remove_convert_to_rough_mesh_modifier_a8c4c', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        col_D3A3B = box_F10CF.column(heading='', align=False)
        col_D3A3B.alert = False
        col_D3A3B.enabled = True
        col_D3A3B.active = True
        col_D3A3B.use_property_split = False
        col_D3A3B.use_property_decorate = False
        col_D3A3B.scale_x = 1.0
        col_D3A3B.scale_y = 1.0
        col_D3A3B.alignment = 'Expand'.upper()
        col_D3A3B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_8B7BC = '["' + str('Socket_3' + '"]') 
        col_D3A3B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_8B7BC, text='Voxel Amount', icon_value=0, emboss=True, toggle=True)
        attr_A4FBE = '["' + str('Socket_4' + '"]') 
        col_D3A3B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_A4FBE, text='Voxel Threshold', icon_value=0, emboss=True, toggle=True)
        attr_47308 = '["' + str('Socket_7' + '"]') 
        col_D3A3B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_47308, text='Simplify', icon_value=0, emboss=True, toggle=True)
        attr_F2260 = '["' + str('Socket_6' + '"]') 
        col_D3A3B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_F2260, text='Smoothing', icon_value=0, emboss=True, toggle=True)
        if '3DGS_Mesh_Type' in bpy.context.view_layer.objects.active:
            if (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'):
                attr_C0C06 = '["' + str('Socket_9' + '"]') 
                col_D3A3B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_C0C06, text='Point Volume Radius', icon_value=0, emboss=True, toggle=True)
        attr_6E61B = '["' + str('Socket_11' + '"]') 
        col_D3A3B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_6E61B, text='Filter Islands', icon_value=0, emboss=True, toggle=False)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN']['Socket_11']:
            col_B8A6E = col_D3A3B.column(heading='', align=False)
            col_B8A6E.alert = False
            col_B8A6E.enabled = True
            col_B8A6E.active = True
            col_B8A6E.use_property_split = False
            col_B8A6E.use_property_decorate = False
            col_B8A6E.scale_x = 1.0
            col_B8A6E.scale_y = 1.0
            col_B8A6E.alignment = 'Expand'.upper()
            col_B8A6E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_65366 = '["' + str('Socket_12' + '"]') 
            col_B8A6E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_65366, text='', icon_value=0, emboss=True, toggle=False)
            attr_0DE62 = '["' + str('Socket_10' + '"]') 
            col_B8A6E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], attr_0DE62, text='Island Threshold', icon_value=0, emboss=True, toggle=False)
    else:
        box_8332A = layout_function.box()
        box_8332A.alert = False
        box_8332A.enabled = 'OBJECT'==bpy.context.mode
        box_8332A.active = True
        box_8332A.use_property_split = False
        box_8332A.use_property_decorate = False
        box_8332A.alignment = 'Expand'.upper()
        box_8332A.scale_x = 1.0
        box_8332A.scale_y = 1.0
        if not True: box_8332A.operator_context = "EXEC_DEFAULT"
        row_A4E6D = box_8332A.row(heading='', align=False)
        row_A4E6D.alert = False
        row_A4E6D.enabled = True
        row_A4E6D.active = True
        row_A4E6D.use_property_split = False
        row_A4E6D.use_property_decorate = False
        row_A4E6D.scale_x = 1.0
        row_A4E6D.scale_y = 1.0
        row_A4E6D.alignment = 'Expand'.upper()
        row_A4E6D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A4E6D.label(text='Convert To Rough Mesh', icon_value=0)
        op = row_A4E6D.operator('sna.dgs_render_append_rough_mesh_modifier_65da3', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_create_duplicate_and_remove_other_modifiers = False



def sna_crop_box_F2C60(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Crop_Box_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_F47C3 = layout_function.box()
        box_F47C3.alert = False
        box_F47C3.enabled = True
        box_F47C3.active = True
        box_F47C3.use_property_split = False
        box_F47C3.use_property_decorate = False
        box_F47C3.alignment = 'Expand'.upper()
        box_F47C3.scale_x = 1.0
        box_F47C3.scale_y = 1.0
        if not True: box_F47C3.operator_context = "EXEC_DEFAULT"
        split_35FA4 = box_F47C3.split(factor=0.5, align=False)
        split_35FA4.alert = False
        split_35FA4.enabled = True
        split_35FA4.active = True
        split_35FA4.use_property_split = False
        split_35FA4.use_property_decorate = False
        split_35FA4.scale_x = 1.0
        split_35FA4.scale_y = 1.0
        split_35FA4.alignment = 'Expand'.upper()
        if not True: split_35FA4.operator_context = "EXEC_DEFAULT"
        split_35FA4.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], 'show_viewport', text='Crop Box', icon_value=0, emboss=True, toggle=True)
        row_D8B0A = split_35FA4.row(heading='', align=True)
        row_D8B0A.alert = False
        row_D8B0A.enabled = True
        row_D8B0A.active = True
        row_D8B0A.use_property_split = False
        row_D8B0A.use_property_decorate = False
        row_D8B0A.scale_x = 1.0
        row_D8B0A.scale_y = 1.0
        row_D8B0A.alignment = 'Right'.upper()
        row_D8B0A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_D8B0A.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_D8B0A.operator('sna.dgs_render_apply_crop_box_modifier_bfdca', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_D8B0A.operator('sna.dgs_render_remove_crop_box_modifier_64ea6', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        box_D7E3D = box_F47C3.box()
        box_D7E3D.alert = False
        box_D7E3D.enabled = True
        box_D7E3D.active = True
        box_D7E3D.use_property_split = False
        box_D7E3D.use_property_decorate = False
        box_D7E3D.alignment = 'Expand'.upper()
        box_D7E3D.scale_x = 1.0
        box_D7E3D.scale_y = 1.0
        if not True: box_D7E3D.operator_context = "EXEC_DEFAULT"
        op = box_D7E3D.operator('sna.dgs_render_auto_generate_crop_object_f20d5', text='Auto generate crop object', icon_value=0, emboss=True, depress=False)
        op.sna_filter_mode = 'quick'
        op.sna_filter_epsilon = 0.029999999329447746
        op.sna_filter_min_points = 10
        op.sna_fast_mode = False
        op.sna_create_convex_hull_object = False
        col_3D26B = box_F47C3.column(heading='', align=True)
        col_3D26B.alert = False
        col_3D26B.enabled = True
        col_3D26B.active = True
        col_3D26B.use_property_split = False
        col_3D26B.use_property_decorate = False
        col_3D26B.scale_x = 1.0
        col_3D26B.scale_y = 1.0
        col_3D26B.alignment = 'Expand'.upper()
        col_3D26B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_75E1E = '["' + str('Socket_19' + '"]') 
        col_3D26B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_75E1E, text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN']['Socket_19'] == 0):
            attr_4C8F9 = '["' + str('Socket_12' + '"]') 
            col_3D26B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_4C8F9, text='', icon_value=0, emboss=True)
        else:
            col_3D26B.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], '["Socket_18"]', bpy.data, 'collections', text='collection', icon='NONE', item_search_property="name")
        attr_5E746 = '["' + str('Socket_15' + '"]') 
        col_3D26B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_5E746, text='', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN']['Socket_15'] >= 2):
            attr_3021D = '["' + str('Socket_16' + '"]') 
            col_3D26B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_3021D, text='', icon_value=0, emboss=True)
    else:
        box_08D76 = layout_function.box()
        box_08D76.alert = False
        box_08D76.enabled = 'OBJECT'==bpy.context.mode
        box_08D76.active = True
        box_08D76.use_property_split = False
        box_08D76.use_property_decorate = False
        box_08D76.alignment = 'Expand'.upper()
        box_08D76.scale_x = 1.0
        box_08D76.scale_y = 1.0
        if not True: box_08D76.operator_context = "EXEC_DEFAULT"
        row_729E9 = box_08D76.row(heading='', align=False)
        row_729E9.alert = False
        row_729E9.enabled = True
        row_729E9.active = True
        row_729E9.use_property_split = False
        row_729E9.use_property_decorate = False
        row_729E9.scale_x = 1.0
        row_729E9.scale_y = 1.0
        row_729E9.alignment = 'Expand'.upper()
        row_729E9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_729E9.label(text='Crop Box', icon_value=0)
        op = row_729E9.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Crop_Box_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Crop_Box_GN'

def sna_decimate_D742E(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Decimate_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_D6E89 = layout_function.box()
        box_D6E89.alert = False
        box_D6E89.enabled = True
        box_D6E89.active = True
        box_D6E89.use_property_split = False
        box_D6E89.use_property_decorate = False
        box_D6E89.alignment = 'Expand'.upper()
        box_D6E89.scale_x = 1.0
        box_D6E89.scale_y = 1.0
        if not True: box_D6E89.operator_context = "EXEC_DEFAULT"
        split_32B05 = box_D6E89.split(factor=0.5, align=False)
        split_32B05.alert = False
        split_32B05.enabled = True
        split_32B05.active = True
        split_32B05.use_property_split = False
        split_32B05.use_property_decorate = False
        split_32B05.scale_x = 1.0
        split_32B05.scale_y = 1.0
        split_32B05.alignment = 'Expand'.upper()
        if not True: split_32B05.operator_context = "EXEC_DEFAULT"
        split_32B05.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], 'show_viewport', text='Decimate', icon_value=0, emboss=True, toggle=True)
        row_3CA54 = split_32B05.row(heading='', align=True)
        row_3CA54.alert = False
        row_3CA54.enabled = True
        row_3CA54.active = True
        row_3CA54.use_property_split = False
        row_3CA54.use_property_decorate = False
        row_3CA54.scale_x = 1.0
        row_3CA54.scale_y = 1.0
        row_3CA54.alignment = 'Right'.upper()
        row_3CA54.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_3CA54.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_3CA54.operator('sna.dgs_render_apply_decimate_modifier_7a32c', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_3CA54.operator('sna.dgs_render_remove_decimate_modifier_fff1b', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        col_49D7B = box_D6E89.column(heading='', align=True)
        col_49D7B.alert = False
        col_49D7B.enabled = True
        col_49D7B.active = True
        col_49D7B.use_property_split = False
        col_49D7B.use_property_decorate = False
        col_49D7B.scale_x = 1.0
        col_49D7B.scale_y = 1.0
        col_49D7B.alignment = 'Expand'.upper()
        col_49D7B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_C43B9 = '["' + str('Socket_15' + '"]') 
        col_49D7B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_C43B9, text='Decimate Percentage', icon_value=0, emboss=True)
        attr_97660 = '["' + str('Socket_16' + '"]') 
        col_49D7B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_97660, text='Decimate Seed', icon_value=0, emboss=True)
        col_CB092 = box_D6E89.column(heading='', align=False)
        col_CB092.alert = False
        col_CB092.enabled = True
        col_CB092.active = True
        col_CB092.use_property_split = False
        col_CB092.use_property_decorate = False
        col_CB092.scale_x = 1.0
        col_CB092.scale_y = 1.0
        col_CB092.alignment = 'Expand'.upper()
        col_CB092.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_93B93 = '["' + str('Socket_18' + '"]') 
        col_CB092.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_93B93, text='Decimate Masking', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_18']:
            col_70B17 = col_CB092.column(heading='', align=False)
            col_70B17.alert = False
            col_70B17.enabled = True
            col_70B17.active = True
            col_70B17.use_property_split = False
            col_70B17.use_property_decorate = False
            col_70B17.scale_x = 1.0
            col_70B17.scale_y = 1.0
            col_70B17.alignment = 'Expand'.upper()
            col_70B17.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_B0634 = '["' + str('Socket_20' + '"]') 
            col_70B17.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_B0634, text='', icon_value=0, emboss=True, toggle=True)
            attr_BD569 = '["' + str('Socket_21' + '"]') 
            col_70B17.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_BD569, text='', icon_value=0, emboss=True, toggle=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_20'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_20'] == 3)):
                attr_2288A = '["' + str('Socket_22' + '"]') 
                col_70B17.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_2288A, text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_2EA63 = layout_function.box()
        box_2EA63.alert = False
        box_2EA63.enabled = 'OBJECT'==bpy.context.mode
        box_2EA63.active = True
        box_2EA63.use_property_split = False
        box_2EA63.use_property_decorate = False
        box_2EA63.alignment = 'Expand'.upper()
        box_2EA63.scale_x = 1.0
        box_2EA63.scale_y = 1.0
        if not True: box_2EA63.operator_context = "EXEC_DEFAULT"
        row_DE93F = box_2EA63.row(heading='', align=False)
        row_DE93F.alert = False
        row_DE93F.enabled = True
        row_DE93F.active = True
        row_DE93F.use_property_split = False
        row_DE93F.use_property_decorate = False
        row_DE93F.scale_x = 1.0
        row_DE93F.scale_y = 1.0
        row_DE93F.alignment = 'Expand'.upper()
        row_DE93F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_DE93F.label(text='Decimate', icon_value=0)
        op = row_DE93F.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Decimate_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Decimate_GN'

def sna_remove_by_size_E1DB7(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Remove_By Size_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_3DF8E = layout_function.box()
        box_3DF8E.alert = False
        box_3DF8E.enabled = True
        box_3DF8E.active = True
        box_3DF8E.use_property_split = False
        box_3DF8E.use_property_decorate = False
        box_3DF8E.alignment = 'Expand'.upper()
        box_3DF8E.scale_x = 1.0
        box_3DF8E.scale_y = 1.0
        if not True: box_3DF8E.operator_context = "EXEC_DEFAULT"
        split_52769 = box_3DF8E.split(factor=0.5, align=False)
        split_52769.alert = False
        split_52769.enabled = True
        split_52769.active = True
        split_52769.use_property_split = False
        split_52769.use_property_decorate = False
        split_52769.scale_x = 1.0
        split_52769.scale_y = 1.0
        split_52769.alignment = 'Expand'.upper()
        if not True: split_52769.operator_context = "EXEC_DEFAULT"
        split_52769.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], 'show_viewport', text='Remove By Size', icon_value=0, emboss=True, toggle=True)
        row_44648 = split_52769.row(heading='', align=True)
        row_44648.alert = False
        row_44648.enabled = True
        row_44648.active = True
        row_44648.use_property_split = False
        row_44648.use_property_decorate = False
        row_44648.scale_x = 1.0
        row_44648.scale_y = 1.0
        row_44648.alignment = 'Right'.upper()
        row_44648.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_44648.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], 'show_render', text='', icon_value=0, emboss=True, toggle=True)
        op = row_44648.operator('sna.dgs_render_apply_remove_by_size_modifier_6dbab', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        op = row_44648.operator('sna.dgs_render_remove_remove_by_size_modifier_3a0e5', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
        col_51C8C = box_3DF8E.column(heading='', align=True)
        col_51C8C.alert = False
        col_51C8C.enabled = True
        col_51C8C.active = True
        col_51C8C.use_property_split = False
        col_51C8C.use_property_decorate = False
        col_51C8C.scale_x = 1.0
        col_51C8C.scale_y = 1.0
        col_51C8C.alignment = 'Expand'.upper()
        col_51C8C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_8753D = '["' + str('Socket_18' + '"]') 
        col_51C8C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_8753D, text='Remove:', icon_value=0, emboss=True, toggle=True)
        attr_F212A = '["' + str('Socket_5' + '"]') 
        col_51C8C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_F212A, text='Threshold', icon_value=0, emboss=True, toggle=True)
        col_AA341 = box_3DF8E.column(heading='', align=False)
        col_AA341.alert = False
        col_AA341.enabled = True
        col_AA341.active = True
        col_AA341.use_property_split = False
        col_AA341.use_property_decorate = False
        col_AA341.scale_x = 1.0
        col_AA341.scale_y = 1.0
        col_AA341.alignment = 'Expand'.upper()
        col_AA341.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_12417 = '["' + str('Socket_13' + '"]') 
        col_AA341.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_12417, text='Remove By Size Masking', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_13']:
            col_AF706 = col_AA341.column(heading='', align=False)
            col_AF706.alert = False
            col_AF706.enabled = True
            col_AF706.active = True
            col_AF706.use_property_split = False
            col_AF706.use_property_decorate = False
            col_AF706.scale_x = 1.0
            col_AF706.scale_y = 1.0
            col_AF706.alignment = 'Expand'.upper()
            col_AF706.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_952BC = '["' + str('Socket_15' + '"]') 
            col_AF706.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_952BC, text='', icon_value=0, emboss=True, toggle=True)
            attr_12EC2 = '["' + str('Socket_14' + '"]') 
            col_AF706.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_12EC2, text='', icon_value=0, emboss=True, toggle=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_15'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_15'] == 3)):
                attr_7198E = '["' + str('Socket_16' + '"]') 
                col_AF706.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_7198E, text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_1F29A = layout_function.box()
        box_1F29A.alert = False
        box_1F29A.enabled = 'OBJECT'==bpy.context.mode
        box_1F29A.active = True
        box_1F29A.use_property_split = False
        box_1F29A.use_property_decorate = False
        box_1F29A.alignment = 'Expand'.upper()
        box_1F29A.scale_x = 1.0
        box_1F29A.scale_y = 1.0
        if not True: box_1F29A.operator_context = "EXEC_DEFAULT"
        row_8BC2D = box_1F29A.row(heading='', align=False)
        row_8BC2D.alert = False
        row_8BC2D.enabled = True
        row_8BC2D.active = True
        row_8BC2D.use_property_split = False
        row_8BC2D.use_property_decorate = False
        row_8BC2D.scale_x = 1.0
        row_8BC2D.scale_y = 1.0
        row_8BC2D.alignment = 'Expand'.upper()
        row_8BC2D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_8BC2D.label(text='Remove By Size', icon_value=0)
        op = row_8BC2D.operator('sna.dgs_render_append_geometry_node_modifier_c2492', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Remove_By Size_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Remove_By Size_GN'




def sna_colour_function_interface_3A6A5(layout_function, ):
    col_EB8EB = layout_function.column(heading='', align=False)
    col_EB8EB.alert = False
    col_EB8EB.enabled = True
    col_EB8EB.active = True
    col_EB8EB.use_property_split = False
    col_EB8EB.use_property_decorate = False
    col_EB8EB.scale_x = 1.0
    col_EB8EB.scale_y = 1.0
    col_EB8EB.alignment = 'Expand'.upper()
    col_EB8EB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_E0430 = col_EB8EB.box()
    box_E0430.alert = False
    box_E0430.enabled = True
    box_E0430.active = True
    box_E0430.use_property_split = False
    box_E0430.use_property_decorate = False
    box_E0430.alignment = 'Expand'.upper()
    box_E0430.scale_x = 1.0
    box_E0430.scale_y = 1.0
    if not True: box_E0430.operator_context = "EXEC_DEFAULT"
    attr_17916 = '["' + str('Socket_54' + '"]') 
    box_E0430.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_17916, text='Shadeless', icon_value=0, emboss=True, toggle=False)
    attr_787E3 = '["' + str('Socket_71' + '"]') 
    box_E0430.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_787E3, text='Create Extra Attributes', icon_value=0, emboss=True, toggle=False)
    col_EB8EB.separator(factor=1.0)
    box_47A8F = col_EB8EB.box()
    box_47A8F.alert = False
    box_47A8F.enabled = True
    box_47A8F.active = True
    box_47A8F.use_property_split = False
    box_47A8F.use_property_decorate = False
    box_47A8F.alignment = 'Expand'.upper()
    box_47A8F.scale_x = 1.0
    box_47A8F.scale_y = 1.0
    if not True: box_47A8F.operator_context = "EXEC_DEFAULT"
    col_89B6E = box_47A8F.column(heading='', align=True)
    col_89B6E.alert = False
    col_89B6E.enabled = True
    col_89B6E.active = True
    col_89B6E.use_property_split = False
    col_89B6E.use_property_decorate = False
    col_89B6E.scale_x = 1.0
    col_89B6E.scale_y = 1.0
    col_89B6E.alignment = 'Expand'.upper()
    col_89B6E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    attr_032D8 = '["' + str('Socket_6' + '"]') 
    col_89B6E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_032D8, text='Brightness', icon_value=0, emboss=True)
    attr_18662 = '["' + str('Socket_2' + '"]') 
    col_89B6E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_18662, text='Contrast', icon_value=0, emboss=True)
    attr_000D9 = '["' + str('Socket_4' + '"]') 
    col_89B6E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_000D9, text='Hue', icon_value=0, emboss=True)
    attr_9DF33 = '["' + str('Socket_3' + '"]') 
    col_89B6E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9DF33, text='Saturation', icon_value=0, emboss=True)
    col_EB8EB.separator(factor=1.0)
    box_A85FA = col_EB8EB.box()
    box_A85FA.alert = False
    box_A85FA.enabled = True
    box_A85FA.active = True
    box_A85FA.use_property_split = False
    box_A85FA.use_property_decorate = False
    box_A85FA.alignment = 'Expand'.upper()
    box_A85FA.scale_x = 1.0
    box_A85FA.scale_y = 1.0
    if not True: box_A85FA.operator_context = "EXEC_DEFAULT"
    box_A85FA.label(text='Active Colour Menu', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    box_A85FA.prop(bpy.context.scene.sna_dgs_scene_properties, 'shading_menu', text=bpy.context.scene.sna_dgs_scene_properties.shading_menu, icon_value=0, emboss=True, expand=True)
    col_EB8EB.separator(factor=1.0)
    if bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Selective 1":
        layout_function = col_EB8EB
        sna_selective_adjustment_1_function_interface_AD57C(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Selective 2":
        layout_function = col_EB8EB
        sna_selective_adjustment_2_function_interface_4A09B(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Selective 3":
        layout_function = col_EB8EB
        sna_selective_adjustment_3_function_interface_69C53(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Vertex Paint":
        layout_function = col_EB8EB
        sna_vertex_paint_function_interface_BEA3E(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.shading_menu == "Image Overlay":
        layout_function = col_EB8EB
        sna_image_overlay_function_interface_64796(layout_function, )
    else:
        pass


def sna_selective_adjustment_1_function_interface_AD57C(layout_function, ):
    col_8C182 = layout_function.column(heading='', align=False)
    col_8C182.alert = False
    col_8C182.enabled = True
    col_8C182.active = True
    col_8C182.use_property_split = False
    col_8C182.use_property_decorate = False
    col_8C182.scale_x = 1.0
    col_8C182.scale_y = 1.0
    col_8C182.alignment = 'Expand'.upper()
    col_8C182.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_8C182.label(text='Selective Adjustment 1', icon_value=0)
    col_8C182.separator(factor=1.0)
    attr_8071F = '["' + str('Socket_10' + '"]') 
    col_8C182.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_8071F, text='Enable Selective Colour 1', icon_value=0, emboss=True, toggle=True)
    col_8C182.separator(factor=1.0)
    col_B3736 = col_8C182.column(heading='', align=False)
    col_B3736.alert = False
    col_B3736.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_10']
    col_B3736.active = True
    col_B3736.use_property_split = False
    col_B3736.use_property_decorate = False
    col_B3736.scale_x = 1.0
    col_B3736.scale_y = 1.0
    col_B3736.alignment = 'Expand'.upper()
    col_B3736.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_98D42 = col_B3736.box()
    box_98D42.alert = False
    box_98D42.enabled = True
    box_98D42.active = True
    box_98D42.use_property_split = False
    box_98D42.use_property_decorate = False
    box_98D42.alignment = 'Expand'.upper()
    box_98D42.scale_x = 1.0
    box_98D42.scale_y = 1.0
    if not True: box_98D42.operator_context = "EXEC_DEFAULT"
    box_98D42.label(text='Selection Type', icon_value=0)
    attr_8D909 = '["' + str('Socket_24' + '"]') 
    box_98D42.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_8D909, text='', icon_value=0, emboss=True)
    attr_34C57 = '["' + str('Socket_7' + '"]') 
    box_98D42.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_34C57, text='Selection', icon_value=0, emboss=True)
    attr_AA353 = '["' + str('Socket_9' + '"]') 
    box_98D42.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_AA353, text='Change To', icon_value=0, emboss=True)
    attr_A5076 = '["' + str('Socket_8' + '"]') 
    box_98D42.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_A5076, text='Colour Threshold', icon_value=0, emboss=True)
    attr_82487 = '["' + str('Socket_25' + '"]') 
    box_98D42.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_82487, text='Saturation Threshold', icon_value=0, emboss=True)
    attr_0164F = '["' + str('Socket_28' + '"]') 
    box_98D42.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_0164F, text='Value Threshold', icon_value=0, emboss=True)
    box_067A3 = col_B3736.box()
    box_067A3.alert = False
    box_067A3.enabled = True
    box_067A3.active = True
    box_067A3.use_property_split = False
    box_067A3.use_property_decorate = False
    box_067A3.alignment = 'Expand'.upper()
    box_067A3.scale_x = 1.0
    box_067A3.scale_y = 1.0
    if not True: box_067A3.operator_context = "EXEC_DEFAULT"
    box_067A3.label(text='Blend Mode', icon_value=0)
    attr_F9F7E = '["' + str('Socket_31' + '"]') 
    box_067A3.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_F9F7E, text='', icon_value=0, emboss=True)
    attr_D1562 = '["' + str('Socket_32' + '"]') 
    box_067A3.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_D1562, text='Mix Factor', icon_value=0, emboss=True)
    attr_BFCE5 = '["' + str('Socket_36' + '"]') 
    box_067A3.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_BFCE5, text='Randomise Mix', icon_value=0, emboss=True)
    box_3ED76 = col_B3736.box()
    box_3ED76.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_33']
    box_3ED76.enabled = True
    box_3ED76.active = True
    box_3ED76.use_property_split = False
    box_3ED76.use_property_decorate = False
    box_3ED76.alignment = 'Expand'.upper()
    box_3ED76.scale_x = 1.0
    box_3ED76.scale_y = 1.0
    if not True: box_3ED76.operator_context = "EXEC_DEFAULT"
    box_3ED76.label(text='Masking', icon_value=0)
    attr_74E93 = '["' + str('Socket_33' + '"]') 
    box_3ED76.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_74E93, text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_33']:
        col_29C70 = box_3ED76.column(heading='', align=False)
        col_29C70.alert = False
        col_29C70.enabled = True
        col_29C70.active = True
        col_29C70.use_property_split = False
        col_29C70.use_property_decorate = False
        col_29C70.scale_x = 1.0
        col_29C70.scale_y = 1.0
        col_29C70.alignment = 'Expand'.upper()
        col_29C70.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_6C86C = '["' + str('Socket_35' + '"]') 
        col_29C70.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_6C86C, text='', icon_value=0, emboss=True, toggle=True)
        attr_1D6B4 = '["' + str('Socket_34' + '"]') 
        col_29C70.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_1D6B4, text='', icon_value=0, emboss=True, toggle=True)
    box_C9715 = col_B3736.box()
    box_C9715.alert = False
    box_C9715.enabled = True
    box_C9715.active = True
    box_C9715.use_property_split = False
    box_C9715.use_property_decorate = False
    box_C9715.alignment = 'Expand'.upper()
    box_C9715.scale_x = 1.0
    box_C9715.scale_y = 1.0
    if not True: box_C9715.operator_context = "EXEC_DEFAULT"
    op = box_C9715.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = box_C9715.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)


def sna_selective_adjustment_2_function_interface_4A09B(layout_function, ):
    col_3234F = layout_function.column(heading='', align=False)
    col_3234F.alert = False
    col_3234F.enabled = True
    col_3234F.active = True
    col_3234F.use_property_split = False
    col_3234F.use_property_decorate = False
    col_3234F.scale_x = 1.0
    col_3234F.scale_y = 1.0
    col_3234F.alignment = 'Expand'.upper()
    col_3234F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_3234F.label(text='Selective Adjustment 2', icon_value=0)
    col_3234F.separator(factor=1.0)
    attr_8064D = '["' + str('Socket_16' + '"]') 
    col_3234F.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_8064D, text='Enable Selective Colour 2', icon_value=0, emboss=True, toggle=True)
    col_3234F.separator(factor=1.0)
    col_1ACBE = col_3234F.column(heading='', align=False)
    col_1ACBE.alert = False
    col_1ACBE.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_16']
    col_1ACBE.active = True
    col_1ACBE.use_property_split = False
    col_1ACBE.use_property_decorate = False
    col_1ACBE.scale_x = 1.0
    col_1ACBE.scale_y = 1.0
    col_1ACBE.alignment = 'Expand'.upper()
    col_1ACBE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_D327E = col_1ACBE.box()
    box_D327E.alert = False
    box_D327E.enabled = True
    box_D327E.active = True
    box_D327E.use_property_split = False
    box_D327E.use_property_decorate = False
    box_D327E.alignment = 'Expand'.upper()
    box_D327E.scale_x = 1.0
    box_D327E.scale_y = 1.0
    if not True: box_D327E.operator_context = "EXEC_DEFAULT"
    box_D327E.label(text='Selection Type', icon_value=0)
    attr_77E08 = '["' + str('Socket_39' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_77E08, text='', icon_value=0, emboss=True)
    attr_8B0ED = '["' + str('Socket_17' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_8B0ED, text='Selection', icon_value=0, emboss=True)
    attr_084CB = '["' + str('Socket_19' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_084CB, text='Change To', icon_value=0, emboss=True)
    attr_4E141 = '["' + str('Socket_18' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_4E141, text='Colour Threshold', icon_value=0, emboss=True)
    attr_281E6 = '["' + str('Socket_26' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_281E6, text='Saturation Threshold', icon_value=0, emboss=True)
    attr_90794 = '["' + str('Socket_29' + '"]') 
    box_D327E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_90794, text='Value Threshold', icon_value=0, emboss=True)
    box_424BC = col_1ACBE.box()
    box_424BC.alert = False
    box_424BC.enabled = True
    box_424BC.active = True
    box_424BC.use_property_split = False
    box_424BC.use_property_decorate = False
    box_424BC.alignment = 'Expand'.upper()
    box_424BC.scale_x = 1.0
    box_424BC.scale_y = 1.0
    if not True: box_424BC.operator_context = "EXEC_DEFAULT"
    box_424BC.label(text='Blend Mode', icon_value=0)
    attr_D9EB5 = '["' + str('Socket_41' + '"]') 
    box_424BC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_D9EB5, text='', icon_value=0, emboss=True)
    attr_08AD5 = '["' + str('Socket_42' + '"]') 
    box_424BC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_08AD5, text='Mix Factor', icon_value=0, emboss=True)
    attr_4668B = '["' + str('Socket_46' + '"]') 
    box_424BC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_4668B, text='Randomise Mix', icon_value=0, emboss=True)
    box_E92EC = col_1ACBE.box()
    box_E92EC.alert = False
    box_E92EC.enabled = True
    box_E92EC.active = True
    box_E92EC.use_property_split = False
    box_E92EC.use_property_decorate = False
    box_E92EC.alignment = 'Expand'.upper()
    box_E92EC.scale_x = 1.0
    box_E92EC.scale_y = 1.0
    if not True: box_E92EC.operator_context = "EXEC_DEFAULT"
    box_E92EC.label(text='Masking', icon_value=0)
    attr_4D4AA = '["' + str('Socket_43' + '"]') 
    box_E92EC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_4D4AA, text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_43']:
        col_25741 = box_E92EC.column(heading='', align=False)
        col_25741.alert = False
        col_25741.enabled = True
        col_25741.active = True
        col_25741.use_property_split = False
        col_25741.use_property_decorate = False
        col_25741.scale_x = 1.0
        col_25741.scale_y = 1.0
        col_25741.alignment = 'Expand'.upper()
        col_25741.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_0F906 = '["' + str('Socket_44' + '"]') 
        col_25741.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_0F906, text='', icon_value=0, emboss=True, toggle=True)
        attr_9AC49 = '["' + str('Socket_45' + '"]') 
        col_25741.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9AC49, text='', icon_value=0, emboss=True, toggle=True)
    box_D2552 = col_1ACBE.box()
    box_D2552.alert = False
    box_D2552.enabled = True
    box_D2552.active = True
    box_D2552.use_property_split = False
    box_D2552.use_property_decorate = False
    box_D2552.alignment = 'Expand'.upper()
    box_D2552.scale_x = 1.0
    box_D2552.scale_y = 1.0
    if not True: box_D2552.operator_context = "EXEC_DEFAULT"
    op = box_D2552.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = box_D2552.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)


def sna_selective_adjustment_3_function_interface_69C53(layout_function, ):
    col_CF5CE = layout_function.column(heading='', align=False)
    col_CF5CE.alert = False
    col_CF5CE.enabled = True
    col_CF5CE.active = True
    col_CF5CE.use_property_split = False
    col_CF5CE.use_property_decorate = False
    col_CF5CE.scale_x = 1.0
    col_CF5CE.scale_y = 1.0
    col_CF5CE.alignment = 'Expand'.upper()
    col_CF5CE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_CF5CE.label(text='Selective Adjustment 3', icon_value=0)
    col_CF5CE.separator(factor=1.0)
    attr_2E4D3 = '["' + str('Socket_23' + '"]') 
    col_CF5CE.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_2E4D3, text='Enable Selective Colour 3', icon_value=0, emboss=True, toggle=True)
    col_CF5CE.separator(factor=1.0)
    col_E631B = col_CF5CE.column(heading='', align=False)
    col_E631B.alert = False
    col_E631B.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_23']
    col_E631B.active = True
    col_E631B.use_property_split = False
    col_E631B.use_property_decorate = False
    col_E631B.scale_x = 1.0
    col_E631B.scale_y = 1.0
    col_E631B.alignment = 'Expand'.upper()
    col_E631B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_2DDC1 = col_E631B.box()
    box_2DDC1.alert = False
    box_2DDC1.enabled = True
    box_2DDC1.active = True
    box_2DDC1.use_property_split = False
    box_2DDC1.use_property_decorate = False
    box_2DDC1.alignment = 'Expand'.upper()
    box_2DDC1.scale_x = 1.0
    box_2DDC1.scale_y = 1.0
    if not True: box_2DDC1.operator_context = "EXEC_DEFAULT"
    box_2DDC1.label(text='Selection Type', icon_value=0)
    attr_C53D8 = '["' + str('Socket_40' + '"]') 
    box_2DDC1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C53D8, text='', icon_value=0, emboss=True)
    attr_A4E8F = '["' + str('Socket_20' + '"]') 
    box_2DDC1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_A4E8F, text='Selection', icon_value=0, emboss=True)
    attr_AFCF0 = '["' + str('Socket_22' + '"]') 
    box_2DDC1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_AFCF0, text='Change To', icon_value=0, emboss=True)
    attr_4CA6F = '["' + str('Socket_21' + '"]') 
    box_2DDC1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_4CA6F, text='Colour Threshold', icon_value=0, emboss=True)
    attr_B934F = '["' + str('Socket_27' + '"]') 
    box_2DDC1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_B934F, text='Saturation Threshold', icon_value=0, emboss=True)
    attr_B4B30 = '["' + str('Socket_30' + '"]') 
    box_2DDC1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_B4B30, text='Value Threshold', icon_value=0, emboss=True)
    box_D5CAB = col_E631B.box()
    box_D5CAB.alert = False
    box_D5CAB.enabled = True
    box_D5CAB.active = True
    box_D5CAB.use_property_split = False
    box_D5CAB.use_property_decorate = False
    box_D5CAB.alignment = 'Expand'.upper()
    box_D5CAB.scale_x = 1.0
    box_D5CAB.scale_y = 1.0
    if not True: box_D5CAB.operator_context = "EXEC_DEFAULT"
    box_D5CAB.label(text='Blend Mode', icon_value=0)
    attr_7153A = '["' + str('Socket_47' + '"]') 
    box_D5CAB.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_7153A, text='', icon_value=0, emboss=True)
    attr_FFE12 = '["' + str('Socket_48' + '"]') 
    box_D5CAB.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_FFE12, text='Mix Factor', icon_value=0, emboss=True)
    attr_C7965 = '["' + str('Socket_52' + '"]') 
    box_D5CAB.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C7965, text='Randomise Mix', icon_value=0, emboss=True)
    box_E6B78 = col_E631B.box()
    box_E6B78.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_49']
    box_E6B78.enabled = True
    box_E6B78.active = True
    box_E6B78.use_property_split = False
    box_E6B78.use_property_decorate = False
    box_E6B78.alignment = 'Expand'.upper()
    box_E6B78.scale_x = 1.0
    box_E6B78.scale_y = 1.0
    if not True: box_E6B78.operator_context = "EXEC_DEFAULT"
    box_E6B78.label(text='Masking', icon_value=0)
    attr_24D06 = '["' + str('Socket_49' + '"]') 
    box_E6B78.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_24D06, text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_49']:
        col_E9291 = box_E6B78.column(heading='', align=False)
        col_E9291.alert = False
        col_E9291.enabled = True
        col_E9291.active = True
        col_E9291.use_property_split = False
        col_E9291.use_property_decorate = False
        col_E9291.scale_x = 1.0
        col_E9291.scale_y = 1.0
        col_E9291.alignment = 'Expand'.upper()
        col_E9291.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_3DC41 = '["' + str('Socket_50' + '"]') 
        col_E9291.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_3DC41, text='', icon_value=0, emboss=True, toggle=True)
        attr_020BD = '["' + str('Socket_51' + '"]') 
        col_E9291.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_020BD, text='', icon_value=0, emboss=True, toggle=True)
    box_008E7 = col_E631B.box()
    box_008E7.alert = False
    box_008E7.enabled = True
    box_008E7.active = True
    box_008E7.use_property_split = False
    box_008E7.use_property_decorate = False
    box_008E7.alignment = 'Expand'.upper()
    box_008E7.scale_x = 1.0
    box_008E7.scale_y = 1.0
    if not True: box_008E7.operator_context = "EXEC_DEFAULT"
    op = box_008E7.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = box_008E7.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)


def sna_image_overlay_function_interface_64796(layout_function, ):
    col_D492B = layout_function.column(heading='', align=False)
    col_D492B.alert = False
    col_D492B.enabled = True
    col_D492B.active = True
    col_D492B.use_property_split = False
    col_D492B.use_property_decorate = False
    col_D492B.scale_x = 1.0
    col_D492B.scale_y = 1.0
    col_D492B.alignment = 'Expand'.upper()
    col_D492B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_D492B.label(text='Image Overlay', icon_value=0)
    col_D492B.separator(factor=1.0)
    attr_F9567 = '["' + str('Socket_56' + '"]') 
    col_D492B.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_F9567, text='Enable Image Overlay', icon_value=0, emboss=True, toggle=True)
    col_D492B.separator(factor=1.0)
    col_FC5C4 = col_D492B.column(heading='', align=False)
    col_FC5C4.alert = False
    col_FC5C4.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_56']
    col_FC5C4.active = True
    col_FC5C4.use_property_split = False
    col_FC5C4.use_property_decorate = False
    col_FC5C4.scale_x = 1.0
    col_FC5C4.scale_y = 1.0
    col_FC5C4.alignment = 'Expand'.upper()
    col_FC5C4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_61F2D = col_FC5C4.box()
    box_61F2D.alert = False
    box_61F2D.enabled = True
    box_61F2D.active = True
    box_61F2D.use_property_split = False
    box_61F2D.use_property_decorate = False
    box_61F2D.alignment = 'Expand'.upper()
    box_61F2D.scale_x = 1.0
    box_61F2D.scale_y = 1.0
    if not True: box_61F2D.operator_context = "EXEC_DEFAULT"
    row_4E69D = box_61F2D.row(heading='', align=False)
    row_4E69D.alert = False
    row_4E69D.enabled = True
    row_4E69D.active = True
    row_4E69D.use_property_split = False
    row_4E69D.use_property_decorate = False
    row_4E69D.scale_x = 1.0
    row_4E69D.scale_y = 1.0
    row_4E69D.alignment = 'Expand'.upper()
    row_4E69D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_4E69D.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], '["Socket_60"]', bpy.data, 'images', text='', icon='NONE', item_search_property="name")
    op = row_4E69D.operator('sna.dgs_render_import_image_overlay_4a457', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'folder.svg')), emboss=True, depress=False)
    box_EA447 = col_FC5C4.box()
    box_EA447.alert = False
    box_EA447.enabled = True
    box_EA447.active = True
    box_EA447.use_property_split = False
    box_EA447.use_property_decorate = False
    box_EA447.alignment = 'Expand'.upper()
    box_EA447.scale_x = 1.0
    box_EA447.scale_y = 1.0
    if not True: box_EA447.operator_context = "EXEC_DEFAULT"
    box_EA447.label(text='Blend Mode', icon_value=0)
    attr_9DFC4 = '["' + str('Socket_63' + '"]') 
    box_EA447.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9DFC4, text='', icon_value=0, emboss=True)
    attr_7BFD4 = '["' + str('Socket_61' + '"]') 
    box_EA447.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_7BFD4, text='Mix Factor', icon_value=0, emboss=True)
    box_CABC3 = col_FC5C4.box()
    box_CABC3.alert = False
    box_CABC3.enabled = True
    box_CABC3.active = True
    box_CABC3.use_property_split = False
    box_CABC3.use_property_decorate = False
    box_CABC3.alignment = 'Expand'.upper()
    box_CABC3.scale_x = 1.0
    box_CABC3.scale_y = 1.0
    if not True: box_CABC3.operator_context = "EXEC_DEFAULT"
    box_CABC3.label(text='Image Mapping', icon_value=0)
    attr_1EE7F = '["' + str('Socket_76' + '"]') 
    box_CABC3.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_1EE7F, text='', icon_value=0, emboss=True)
    if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_76'] == 0) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_76'] == 2)):
        box_3B9C8 = col_FC5C4.box()
        box_3B9C8.alert = False
        box_3B9C8.enabled = True
        box_3B9C8.active = True
        box_3B9C8.use_property_split = False
        box_3B9C8.use_property_decorate = False
        box_3B9C8.alignment = 'Expand'.upper()
        box_3B9C8.scale_x = 1.0
        box_3B9C8.scale_y = 1.0
        if not True: box_3B9C8.operator_context = "EXEC_DEFAULT"
        attr_1C59C = '["' + str('Socket_82' + '"]') 
        box_3B9C8.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_1C59C, text='Location', icon_value=0, emboss=True)
        attr_18E1F = '["' + str('Socket_74' + '"]') 
        box_3B9C8.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_18E1F, text='Rotation', icon_value=0, emboss=True)
        attr_C764D = '["' + str('Socket_83' + '"]') 
        box_3B9C8.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C764D, text='Scale', icon_value=0, emboss=True)
    if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_76'] == 1):
        box_A6BCF = col_FC5C4.box()
        box_A6BCF.alert = False
        box_A6BCF.enabled = True
        box_A6BCF.active = True
        box_A6BCF.use_property_split = False
        box_A6BCF.use_property_decorate = False
        box_A6BCF.alignment = 'Expand'.upper()
        box_A6BCF.scale_x = 1.0
        box_A6BCF.scale_y = 1.0
        if not True: box_A6BCF.operator_context = "EXEC_DEFAULT"
        box_A6BCF.label(text='Mapping Object', icon_value=0)
        attr_47BD3 = '["' + str('Socket_77' + '"]') 
        box_A6BCF.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_47BD3, text='', icon_value=0, emboss=True)
    box_8D0CD = col_FC5C4.box()
    box_8D0CD.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_67']
    box_8D0CD.enabled = True
    box_8D0CD.active = True
    box_8D0CD.use_property_split = False
    box_8D0CD.use_property_decorate = False
    box_8D0CD.alignment = 'Expand'.upper()
    box_8D0CD.scale_x = 1.0
    box_8D0CD.scale_y = 1.0
    if not True: box_8D0CD.operator_context = "EXEC_DEFAULT"
    box_8D0CD.label(text='Masking', icon_value=0)
    attr_145C4 = '["' + str('Socket_67' + '"]') 
    box_8D0CD.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_145C4, text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_67']:
        col_D2C3C = box_8D0CD.column(heading='', align=False)
        col_D2C3C.alert = False
        col_D2C3C.enabled = True
        col_D2C3C.active = True
        col_D2C3C.use_property_split = False
        col_D2C3C.use_property_decorate = False
        col_D2C3C.scale_x = 1.0
        col_D2C3C.scale_y = 1.0
        col_D2C3C.alignment = 'Expand'.upper()
        col_D2C3C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_67BF4 = '["' + str('Socket_68' + '"]') 
        col_D2C3C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_67BF4, text='', icon_value=0, emboss=True, toggle=True)
        attr_9154D = '["' + str('Socket_69' + '"]') 
        col_D2C3C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9154D, text='', icon_value=0, emboss=True, toggle=True)
    box_A11BE = col_FC5C4.box()
    box_A11BE.alert = False
    box_A11BE.enabled = True
    box_A11BE.active = True
    box_A11BE.use_property_split = False
    box_A11BE.use_property_decorate = False
    box_A11BE.alignment = 'Expand'.upper()
    box_A11BE.scale_x = 1.0
    box_A11BE.scale_y = 1.0
    if not True: box_A11BE.operator_context = "EXEC_DEFAULT"
    op = box_A11BE.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = box_A11BE.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)


def sna_vertex_paint_function_interface_BEA3E(layout_function, ):
    if (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'):
        box_07727 = layout_function.box()
        box_07727.alert = False
        box_07727.enabled = True
        box_07727.active = True
        box_07727.use_property_split = False
        box_07727.use_property_decorate = False
        box_07727.alignment = 'Expand'.upper()
        box_07727.scale_x = 1.0
        box_07727.scale_y = 1.0
        if not True: box_07727.operator_context = "EXEC_DEFAULT"
        box_07727.label(text='Vertex Paint is not available to objects', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_07727.label(text="imported as 'Verts'", icon_value=0)
    col_453E1 = layout_function.column(heading='', align=False)
    col_453E1.alert = False
    col_453E1.enabled = (not (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'vert'))
    col_453E1.active = True
    col_453E1.use_property_split = False
    col_453E1.use_property_decorate = False
    col_453E1.scale_x = 1.0
    col_453E1.scale_y = 1.0
    col_453E1.alignment = 'Expand'.upper()
    col_453E1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_453E1.label(text='Vertex Painting', icon_value=0)
    col_453E1.separator(factor=1.0)
    attr_C4F4C = '["' + str('Socket_55' + '"]') 
    col_453E1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_C4F4C, text='Enable Vertex Painting', icon_value=0, emboss=True, toggle=True)
    col_453E1.separator(factor=1.0)
    col_86FB7 = col_453E1.column(heading='', align=False)
    col_86FB7.alert = False
    col_86FB7.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_55']
    col_86FB7.active = True
    col_86FB7.use_property_split = False
    col_86FB7.use_property_decorate = False
    col_86FB7.scale_x = 1.0
    col_86FB7.scale_y = 1.0
    col_86FB7.alignment = 'Expand'.upper()
    col_86FB7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_2E9CF = col_86FB7.box()
    box_2E9CF.alert = False
    box_2E9CF.enabled = True
    box_2E9CF.active = True
    box_2E9CF.use_property_split = False
    box_2E9CF.use_property_decorate = False
    box_2E9CF.alignment = 'Expand'.upper()
    box_2E9CF.scale_x = 1.0
    box_2E9CF.scale_y = 1.0
    if not True: box_2E9CF.operator_context = "EXEC_DEFAULT"
    box_2E9CF.label(text='Painting', icon_value=0)
    if (property_exists("bpy.context.view_layer.objects.active.data.color_attributes", globals(), locals()) and 'KIRI_3DGS_Paint' in bpy.context.view_layer.objects.active.data.color_attributes):
        op = box_2E9CF.operator('sna.dgs_render_start_vertex_painting_a36e0', text='Start Painting', icon_value=0, emboss=True, depress=False)
    else:
        box_ACBF2 = box_2E9CF.box()
        box_ACBF2.alert = False
        box_ACBF2.enabled = True
        box_ACBF2.active = True
        box_ACBF2.use_property_split = False
        box_ACBF2.use_property_decorate = False
        box_ACBF2.alignment = 'Expand'.upper()
        box_ACBF2.scale_x = 1.0
        box_ACBF2.scale_y = 1.0
        if not True: box_ACBF2.operator_context = "EXEC_DEFAULT"
        box_ACBF2.label(text='KIRI_3DGS_Paint attribute is missing', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
    op = box_2E9CF.operator('sna.dgs_render_refresh__create_paint_attribute_84655', text='Reset Paint', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg')), emboss=True, depress=False)
    box_7E936 = col_86FB7.box()
    box_7E936.alert = False
    box_7E936.enabled = True
    box_7E936.active = True
    box_7E936.use_property_split = False
    box_7E936.use_property_decorate = False
    box_7E936.alignment = 'Expand'.upper()
    box_7E936.scale_x = 1.0
    box_7E936.scale_y = 1.0
    if not True: box_7E936.operator_context = "EXEC_DEFAULT"
    box_7E936.label(text='Blend Mode', icon_value=0)
    attr_97713 = '["' + str('Socket_62' + '"]') 
    box_7E936.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_97713, text='', icon_value=0, emboss=True)
    attr_2A320 = '["' + str('Socket_57' + '"]') 
    box_7E936.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_2A320, text='Mix Factor', icon_value=0, emboss=True)
    box_55BC3 = col_86FB7.box()
    box_55BC3.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_64']
    box_55BC3.enabled = True
    box_55BC3.active = True
    box_55BC3.use_property_split = False
    box_55BC3.use_property_decorate = False
    box_55BC3.alignment = 'Expand'.upper()
    box_55BC3.scale_x = 1.0
    box_55BC3.scale_y = 1.0
    if not True: box_55BC3.operator_context = "EXEC_DEFAULT"
    box_55BC3.label(text='Masking', icon_value=0)
    attr_03413 = '["' + str('Socket_64' + '"]') 
    box_55BC3.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_03413, text='Mask By Object', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_64']:
        col_DC970 = box_55BC3.column(heading='', align=False)
        col_DC970.alert = False
        col_DC970.enabled = True
        col_DC970.active = True
        col_DC970.use_property_split = False
        col_DC970.use_property_decorate = False
        col_DC970.scale_x = 1.0
        col_DC970.scale_y = 1.0
        col_DC970.alignment = 'Expand'.upper()
        col_DC970.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_7340F = '["' + str('Socket_65' + '"]') 
        col_DC970.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_7340F, text='', icon_value=0, emboss=True, toggle=True)
        attr_34BD5 = '["' + str('Socket_66' + '"]') 
        col_DC970.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_34BD5, text='', icon_value=0, emboss=True, toggle=True)
    box_95EA8 = col_86FB7.box()
    box_95EA8.alert = False
    box_95EA8.enabled = True
    box_95EA8.active = True
    box_95EA8.use_property_split = False
    box_95EA8.use_property_decorate = False
    box_95EA8.alignment = 'Expand'.upper()
    box_95EA8.scale_x = 1.0
    box_95EA8.scale_y = 1.0
    if not True: box_95EA8.operator_context = "EXEC_DEFAULT"
    op = box_95EA8.operator('sna.dgs_render_append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-sphere-7915480-FFFFFF.svg')), emboss=True, depress=False)
    op = box_95EA8.operator('sna.dgs_render_append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)

