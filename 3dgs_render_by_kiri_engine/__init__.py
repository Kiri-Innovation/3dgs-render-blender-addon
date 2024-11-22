# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "3DGS Render by KIRI Engine",
    "author" : "KIRI ENGINE TEAM", 
    "description" : "Import, edit and render and animate 3DGS scans",
    "blender" : (4, 2, 0),
    "version" : (2, 0, 0),
    "location" : "",
    "warning" : "Please restart Blender after install/uninstall",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
import webbrowser
import os
from bpy.app.handlers import persistent
import numpy as np
from multiprocessing import shared_memory
import time
from bpy_extras.io_utils import ImportHelper, ExportHelper
from mathutils import Matrix
import math
import sys
from mathutils import Vector, Matrix


addon_keymaps = {}
_icons = None
kiri_3dgs_render__active_object_update = {'sna_apply_modifier_list': [], 'sna_in_camera_view': False, }
kiri_3dgs_render__hq_render = {'sna_hq_render_base_object_list': [], 'sna_hq_render_origpos_duplicate_list': [], }


kiri_3dgs_render__import_ply = {'sna_dgs_lq_active': None, }
kiri_3dgs_render__omnisplat = {'sna_omniviewobjectsformerge': [], 'sna_omniviewbase': None, 'sna_omniviewmodifierlist': [], }


def sna_update_sna_kiri3dgs_active_object_update_mode_868D4(self, context):
    sna_updated_prop = self.sna_kiri3dgs_active_object_update_mode
    self['update_rot_to_cam'] = (sna_updated_prop == 'Enable Camera Updates')
    self.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = (2 if (sna_updated_prop == 'Show As Point Cloud') else (1 if (sna_updated_prop != 'Enable Camera Updates') else 0))
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport = (True if (sna_updated_prop != 'Disable Camera Updates') else False)
    bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


def sna_update_sna_kiri3dgs_active_object_enable_active_camera_DE26E(self, context):
    sna_updated_prop = self.sna_kiri3dgs_active_object_enable_active_camera
    if sna_updated_prop:
        bpy.context.area.spaces.active.region_3d.view_perspective = 'CAMERA'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop

        def delayed_214CF():
            sna_dgs__update_camera_single_time_function_execute_9C695()
        bpy.app.timers.register(delayed_214CF, first_interval=0.10000000149011612)
    else:
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop


def sna_add_geo_nodes__append_group_2D522_F22B7(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_BF551(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_91587(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_8E257(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_DDE79(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_EB4FD(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_592E9(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_B6203(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_5FBAE(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_add_geo_nodes__append_group_2D522_74B9D(Append_Path, Node_Group_Name, Objects, Modifier_Name):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=Append_Path + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_C35B3 = None if not new_data else new_data[0]
    modifier_D540A = Objects.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_D540A.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_D540A


def sna_update_sna_kiri3dgs_modifier_enable_animate_1F5D0(self, context):
    sna_updated_prop = self.sna_kiri3dgs_modifier_enable_animate
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_viewport = sna_updated_prop
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_render = sna_updated_prop


def sna_update_sna_kiri3dgs_modifier_enable_decimate_641A7(self, context):
    sna_updated_prop = self.sna_kiri3dgs_modifier_enable_decimate
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'].show_viewport = sna_updated_prop
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'].show_render = sna_updated_prop


def sna_update_sna_kiri3dgs_modifier_enable_camera_cull_A98D6(self, context):
    sna_updated_prop = self.sna_kiri3dgs_modifier_enable_camera_cull
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'].show_viewport = sna_updated_prop
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'].show_render = sna_updated_prop


def sna_update_sna_kiri3dgs_modifier_enable_crop_box_6FCA7(self, context):
    sna_updated_prop = self.sna_kiri3dgs_modifier_enable_crop_box
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'].show_viewport = sna_updated_prop
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'].show_render = sna_updated_prop


def sna_update_sna_kiri3dgs_modifier_enable_colour_edit_1D6A1(self, context):
    sna_updated_prop = self.sna_kiri3dgs_modifier_enable_colour_edit
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'].show_viewport = sna_updated_prop
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'].show_render = sna_updated_prop


def sna_update_sna_kiri3dgs_modifier_enable_remove_stray_488C9(self, context):
    sna_updated_prop = self.sna_kiri3dgs_modifier_enable_remove_stray
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'].show_viewport = sna_updated_prop
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'].show_render = sna_updated_prop


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


class SNA_OT_Launch_Kiri_Site_D26Bf(bpy.types.Operator):
    bl_idname = "sna.launch_kiri_site_d26bf"
    bl_label = "Launch Kiri Site"
    bl_description = "Launches a browser for the KIRI Engine main site"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.com/'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Launch_Blender_Market_77F72(bpy.types.Operator):
    bl_idname = "sna.launch_blender_market_77f72"
    bl_label = "Launch Blender Market"
    bl_description = "Launches a browser for the KIRI Engine Blender Market store"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://blendermarket.com/creators/blender-addon-from-kiri-engine'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_active_object_camera_update_interface_func_9588F(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
        col_A4D20 = layout_function.column(heading='', align=False)
        col_A4D20.alert = False
        col_A4D20.enabled = True
        col_A4D20.active = True
        col_A4D20.use_property_split = False
        col_A4D20.use_property_decorate = False
        col_A4D20.scale_x = 1.0
        col_A4D20.scale_y = 1.0
        col_A4D20.alignment = 'Expand'.upper()
        col_A4D20.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_A4D20.label(text='Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
        col_A4D20.separator(factor=1.0)
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Enable Camera Updates'):
            if bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera:
                pass
            else:
                if 'EDIT_MESH'==bpy.context.mode:
                    box_A6D9A = col_A4D20.box()
                    box_A6D9A.alert = False
                    box_A6D9A.enabled = True
                    box_A6D9A.active = True
                    box_A6D9A.use_property_split = False
                    box_A6D9A.use_property_decorate = False
                    box_A6D9A.alignment = 'Expand'.upper()
                    box_A6D9A.scale_x = 1.0
                    box_A6D9A.scale_y = 1.0
                    if not True: box_A6D9A.operator_context = "EXEC_DEFAULT"
                    row_6C7B3 = box_A6D9A.row(heading='', align=False)
                    row_6C7B3.alert = False
                    row_6C7B3.enabled = True
                    row_6C7B3.active = True
                    row_6C7B3.use_property_split = False
                    row_6C7B3.use_property_decorate = False
                    row_6C7B3.scale_x = 1.0
                    row_6C7B3.scale_y = 1.0
                    row_6C7B3.alignment = 'Expand'.upper()
                    row_6C7B3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = row_6C7B3.operator('sna.align_active_to_x_axis_9b12e', text='X', icon_value=0, emboss=True, depress=False)
                    op = row_6C7B3.operator('sna.align_active_to_y_axis_9bd1f', text='Y', icon_value=0, emboss=True, depress=False)
                    op = row_6C7B3.operator('sna.align_active_to_z_axis_720a9', text='Z', icon_value=0, emboss=True, depress=False)
                else:
                    box_D2CC1 = col_A4D20.box()
                    box_D2CC1.alert = False
                    box_D2CC1.enabled = True
                    box_D2CC1.active = True
                    box_D2CC1.use_property_split = False
                    box_D2CC1.use_property_decorate = False
                    box_D2CC1.alignment = 'Expand'.upper()
                    box_D2CC1.scale_x = 1.0
                    box_D2CC1.scale_y = 1.0
                    if not True: box_D2CC1.operator_context = "EXEC_DEFAULT"
                    op = box_D2CC1.operator('sna.align_active_to_view_88e3a', text='Update Active To View', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'eye-6926444-white.png')), emboss=True, depress=False)
        col_A4D20.separator(factor=1.0)
        col_F0A3B = col_A4D20.column(heading='', align=False)
        col_F0A3B.alert = False
        col_F0A3B.enabled = True
        col_F0A3B.active = True
        col_F0A3B.use_property_split = False
        col_F0A3B.use_property_decorate = False
        col_F0A3B.scale_x = 1.0
        col_F0A3B.scale_y = 1.0
        col_F0A3B.alignment = 'Expand'.upper()
        col_F0A3B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_F0A3B.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_active_object_update_mode', text='', icon_value=0, emboss=True, toggle=True)
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Show As Point Cloud'):
            attr_C8F44 = '["' + str('Socket_51' + '"]') 
            col_A4D20.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], attr_C8F44, text='Point Radius', icon_value=0, emboss=True)
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Enable Camera Updates'):
            box_85B7C = col_A4D20.box()
            box_85B7C.alert = bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera
            box_85B7C.enabled = (not (bpy.context.scene.camera == None))
            box_85B7C.active = True
            box_85B7C.use_property_split = False
            box_85B7C.use_property_decorate = False
            box_85B7C.alignment = 'Expand'.upper()
            box_85B7C.scale_x = 1.0
            box_85B7C.scale_y = 1.0
            if not True: box_85B7C.operator_context = "EXEC_DEFAULT"
            if (bpy.context.scene.camera == None):
                box_9DBDD = box_85B7C.box()
                box_9DBDD.alert = True
                box_9DBDD.enabled = True
                box_9DBDD.active = True
                box_9DBDD.use_property_split = False
                box_9DBDD.use_property_decorate = False
                box_9DBDD.alignment = 'Expand'.upper()
                box_9DBDD.scale_x = 1.0
                box_9DBDD.scale_y = 1.0
                if not True: box_9DBDD.operator_context = "EXEC_DEFAULT"
                box_9DBDD.label(text='No active camera in scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
            box_85B7C.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_active_object_enable_active_camera', text='Use Active Camera', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera-7391968-white.png')), emboss=True, toggle=True)
    col_58BF4 = layout_function.column(heading='', align=False)
    col_58BF4.alert = False
    col_58BF4.enabled = True
    col_58BF4.active = True
    col_58BF4.use_property_split = False
    col_58BF4.use_property_decorate = False
    col_58BF4.scale_x = 1.0
    col_58BF4.scale_y = 1.0
    col_58BF4.alignment = 'Expand'.upper()
    col_58BF4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_58BF4.operator('sna.apply_3dgs_modifiers_e67a2', text='Apply Modifiers', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
    op.sna_apply_3dgs_render_modifier = False
    op.sna_apply_decimate_modifier = False
    op.sna_apply_camera_cull_modifier = False
    op.sna_apply_crop_box_modifier = False
    op.sna_apply_colour_edit_modifier = False
    op.sna_apply_remove_stray_modifier = False
    op.sna_apply_animate_modifier = False


class SNA_OT_Apply_3Dgs_Modifiers_E67A2(bpy.types.Operator):
    bl_idname = "sna.apply_3dgs_modifiers_e67a2"
    bl_label = "Apply 3DGS Modifiers"
    bl_description = "Applies selected modifiers."
    bl_options = {"REGISTER", "UNDO"}
    sna_apply_3dgs_render_modifier: bpy.props.BoolProperty(name='Apply 3DGS Render Modifier', description='', default=True)
    sna_apply_decimate_modifier: bpy.props.BoolProperty(name='Apply Decimate Modifier', description='', default=False)
    sna_apply_camera_cull_modifier: bpy.props.BoolProperty(name='Apply Camera Cull Modifier', description='', default=False)
    sna_apply_crop_box_modifier: bpy.props.BoolProperty(name='Apply Crop Box Modifier', description='', default=False)
    sna_apply_colour_edit_modifier: bpy.props.BoolProperty(name='Apply Colour Edit Modifier', description='', default=False)
    sna_apply_remove_stray_modifier: bpy.props.BoolProperty(name='Apply Remove Stray Modifier', description='', default=False)
    sna_apply_animate_modifier: bpy.props.BoolProperty(name='Apply Animate Modifier', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        kiri_3dgs_render__active_object_update['sna_apply_modifier_list'] = []
        if self.sna_apply_3dgs_render_modifier:
            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_57'] = True
        if self.sna_apply_animate_modifier:
            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_35'] = True
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        if self.sna_apply_3dgs_render_modifier:
            kiri_3dgs_render__active_object_update['sna_apply_modifier_list'].append('KIRI_3DGS_Render_GN')
        if self.sna_apply_decimate_modifier:
            kiri_3dgs_render__active_object_update['sna_apply_modifier_list'].append('KIRI_3DGS_Decimate_GN')
        if self.sna_apply_camera_cull_modifier:
            kiri_3dgs_render__active_object_update['sna_apply_modifier_list'].append('KIRI_3DGS_Camera_Cull_GN')
        if self.sna_apply_crop_box_modifier:
            kiri_3dgs_render__active_object_update['sna_apply_modifier_list'].append('KIRI_3DGS_Crop_Box_GN')
        if self.sna_apply_colour_edit_modifier:
            kiri_3dgs_render__active_object_update['sna_apply_modifier_list'].append('KIRI_3DGS_Colour_Edit_GN')
        if self.sna_apply_remove_stray_modifier:
            kiri_3dgs_render__active_object_update['sna_apply_modifier_list'].append('KIRI_3DGS_Remove_Stray_GN')
        if self.sna_apply_animate_modifier:
            kiri_3dgs_render__active_object_update['sna_apply_modifier_list'].append('KIRI_3DGS_Animate_GN')
        for i_E1E08 in range(len(kiri_3dgs_render__active_object_update['sna_apply_modifier_list'])):
            object_name = bpy.context.view_layer.objects.active.name
            modifier_name = kiri_3dgs_render__active_object_update['sna_apply_modifier_list'][i_E1E08]
            obj = bpy.data.objects.get(object_name)
            if obj:
                modifier = obj.modifiers.get(modifier_name)
                if modifier:
                    if not modifier.show_viewport:
                        # Simply remove the modifier if it's hidden
                        obj.modifiers.remove(modifier)
                        print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                    else:
                        # Apply normally if visible
                        bpy.ops.object.modifier_apply(modifier=modifier_name)
                        print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
                else:
                    print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
            else:
                print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        col_DFD19 = layout.column(heading='', align=False)
        col_DFD19.alert = False
        col_DFD19.enabled = True
        col_DFD19.active = True
        col_DFD19.use_property_split = False
        col_DFD19.use_property_decorate = False
        col_DFD19.scale_x = 1.0
        col_DFD19.scale_y = 1.0
        col_DFD19.alignment = 'Expand'.upper()
        col_DFD19.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_34FDC = col_DFD19.box()
        box_34FDC.alert = True
        box_34FDC.enabled = True
        box_34FDC.active = True
        box_34FDC.use_property_split = False
        box_34FDC.use_property_decorate = False
        box_34FDC.alignment = 'Expand'.upper()
        box_34FDC.scale_x = 1.0
        box_34FDC.scale_y = 1.0
        if not True: box_34FDC.operator_context = "EXEC_DEFAULT"
        box_34FDC.label(text='This is a destructive act.', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
        box_34FDC.label(text='         If the 3DGS Render modifier is applied, faces will no longer be updated.', icon_value=0)
        col_DFD19.separator(factor=1.0)
        box_4F8F8 = col_DFD19.box()
        box_4F8F8.alert = False
        box_4F8F8.enabled = True
        box_4F8F8.active = True
        box_4F8F8.use_property_split = False
        box_4F8F8.use_property_decorate = False
        box_4F8F8.alignment = 'Expand'.upper()
        box_4F8F8.scale_x = 1.0
        box_4F8F8.scale_y = 1.0
        if not True: box_4F8F8.operator_context = "EXEC_DEFAULT"
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
            row_FB27E = box_4F8F8.row(heading='', align=False)
            row_FB27E.alert = False
            row_FB27E.enabled = True
            row_FB27E.active = True
            row_FB27E.use_property_split = False
            row_FB27E.use_property_decorate = False
            row_FB27E.scale_x = 1.0
            row_FB27E.scale_y = 1.0
            row_FB27E.alignment = 'Expand'.upper()
            row_FB27E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_FB27E.label(text='Apply 3DGS Render Modifier', icon_value=0)
            row_FB27E.prop(self, 'sna_apply_3dgs_render_modifier', text='', icon_value=0, emboss=True)
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Decimate_GN' in bpy.context.view_layer.objects.active.modifiers):
            row_274B0 = box_4F8F8.row(heading='', align=False)
            row_274B0.alert = False
            row_274B0.enabled = True
            row_274B0.active = True
            row_274B0.use_property_split = False
            row_274B0.use_property_decorate = False
            row_274B0.scale_x = 1.0
            row_274B0.scale_y = 1.0
            row_274B0.alignment = 'Expand'.upper()
            row_274B0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_274B0.label(text='Apply Decimate Modifier', icon_value=0)
            row_274B0.prop(self, 'sna_apply_decimate_modifier', text='', icon_value=0, emboss=True)
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Camera_Cull_GN' in bpy.context.view_layer.objects.active.modifiers):
            row_DCB98 = box_4F8F8.row(heading='', align=False)
            row_DCB98.alert = False
            row_DCB98.enabled = True
            row_DCB98.active = True
            row_DCB98.use_property_split = False
            row_DCB98.use_property_decorate = False
            row_DCB98.scale_x = 1.0
            row_DCB98.scale_y = 1.0
            row_DCB98.alignment = 'Expand'.upper()
            row_DCB98.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_DCB98.label(text='Apply Camera Cull Modifier', icon_value=0)
            row_DCB98.prop(self, 'sna_apply_camera_cull_modifier', text='', icon_value=0, emboss=True)
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Crop_Box_GN' in bpy.context.view_layer.objects.active.modifiers):
            row_D27A7 = box_4F8F8.row(heading='', align=False)
            row_D27A7.alert = False
            row_D27A7.enabled = True
            row_D27A7.active = True
            row_D27A7.use_property_split = False
            row_D27A7.use_property_decorate = False
            row_D27A7.scale_x = 1.0
            row_D27A7.scale_y = 1.0
            row_D27A7.alignment = 'Expand'.upper()
            row_D27A7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_D27A7.label(text='Apply Crop Box Modifier', icon_value=0)
            row_D27A7.prop(self, 'sna_apply_crop_box_modifier', text='', icon_value=0, emboss=True)
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Colour_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
            row_ECA62 = box_4F8F8.row(heading='', align=False)
            row_ECA62.alert = False
            row_ECA62.enabled = True
            row_ECA62.active = True
            row_ECA62.use_property_split = False
            row_ECA62.use_property_decorate = False
            row_ECA62.scale_x = 1.0
            row_ECA62.scale_y = 1.0
            row_ECA62.alignment = 'Expand'.upper()
            row_ECA62.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_ECA62.label(text='Apply Colour Edit Modifier', icon_value=0)
            row_ECA62.prop(self, 'sna_apply_colour_edit_modifier', text='', icon_value=0, emboss=True)
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Remove_Stray_GN' in bpy.context.view_layer.objects.active.modifiers):
            row_E5905 = box_4F8F8.row(heading='', align=False)
            row_E5905.alert = False
            row_E5905.enabled = True
            row_E5905.active = True
            row_E5905.use_property_split = False
            row_E5905.use_property_decorate = False
            row_E5905.scale_x = 1.0
            row_E5905.scale_y = 1.0
            row_E5905.alignment = 'Expand'.upper()
            row_E5905.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_E5905.label(text='Apply Remove Stray Modifier', icon_value=0)
            row_E5905.prop(self, 'sna_apply_remove_stray_modifier', text='', icon_value=0, emboss=True)
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Animate_GN' in bpy.context.view_layer.objects.active.modifiers):
            row_CAA60 = box_4F8F8.row(heading='', align=False)
            row_CAA60.alert = False
            row_CAA60.enabled = True
            row_CAA60.active = True
            row_CAA60.use_property_split = False
            row_CAA60.use_property_decorate = False
            row_CAA60.scale_x = 1.0
            row_CAA60.scale_y = 1.0
            row_CAA60.alignment = 'Expand'.upper()
            row_CAA60.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_CAA60.label(text='Apply Animate Modifier', icon_value=0)
            row_CAA60.prop(self, 'sna_apply_animate_modifier', text='', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_OT_Align_Active_To_X_Axis_9B12E(bpy.types.Operator):
    bl_idname = "sna.align_active_to_x_axis_9b12e"
    bl_label = "Align Active To X Axis"
    bl_description = "Updates the 3DGS_Render modifier once to the X axis for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_align_active_values_to_x_function_execute_03E8D()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Align_Active_To_Y_Axis_9Bd1F(bpy.types.Operator):
    bl_idname = "sna.align_active_to_y_axis_9bd1f"
    bl_label = "Align Active To Y Axis"
    bl_description = "Updates the 3DGS_Render modifier once to the Y axis for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_align_active_values_to_y_function_execute_89335()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Align_Active_To_Z_Axis_720A9(bpy.types.Operator):
    bl_idname = "sna.align_active_to_z_axis_720a9"
    bl_label = "Align Active To Z Axis"
    bl_description = "Updates the 3DGS_Render modifier once to the Z axis for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_align_active_values_to_z_function_execute_62C4D()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Align_Active_To_View_88E3A(bpy.types.Operator):
    bl_idname = "sna.align_active_to_view_88e3a"
    bl_label = "Align Active To View"
    bl_description = "Updates the 3DGS_Render modifier once to the current view for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        ObjectName = bpy.context.view_layer.objects.active.name
        from mathutils import Matrix
        # Define helper function for updating the geometry node sockets

        def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
            geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
            if not geometryNodes_modifier:
                print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                return False
            # Update view matrix
            geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
            geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
            geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
            geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
            geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
            geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
            geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
            geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
            geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
            geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
            geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
            geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
            geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
            geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
            geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
            geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
            # Update projection matrix
            geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
            geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
            geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
            geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
            geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
            geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
            geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
            geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
            geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
            geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
            geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
            geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
            geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
            geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
            geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
            geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
            # Update window dimensions
            geometryNodes_modifier['Socket_34'] = window_width
            geometryNodes_modifier['Socket_35'] = window_height
            return True
        # Main code for updating specific object
        updated_objects = []
        # Find view and projection matrices from the 3D view area
        found_3d_view = False
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                view_matrix = area.spaces.active.region_3d.view_matrix
                proj_matrix = area.spaces.active.region_3d.window_matrix
                window_width = area.width
                window_height = area.height
                found_3d_view = True
                break
        if not found_3d_view:
            print("Error: No 3D View found to update camera information.")
        else:
            # Update only specific object
            target_object_name = ObjectName  # Serpens Variable
            obj = bpy.data.objects.get(target_object_name)
            if obj and obj.visible_get():
                print(f"Attempting to update object: {obj.name}")  # Debugging print
                if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                    updated_objects.append(obj.name)  # Add to updated list
        # Print or output the list of updated objects
        print("Updated objects:", updated_objects)
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs__Start_Camera_Update_001Bd(bpy.types.Operator):
    bl_idname = "sna.dgs__start_camera_update_001bd"
    bl_label = "3DGS - Start Camera Update"
    bl_description = "Starts updating the 3DGS_Render modifier for all enabled objects in the scene."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        input_update_method = bpy.context.scene.sna_kiri3dgs_scene_camera_refresh_mode.replace('Frame Change', 'frame_change')
        from mathutils import Matrix

        def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
            geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
            if not geometryNodes_modifier:
                print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                return False
            # Update view matrix
            geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
            geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
            geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
            geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
            geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
            geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
            geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
            geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
            geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
            geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
            geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
            geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
            geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
            geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
            geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
            geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
            # Update projection matrix
            geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
            geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
            geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
            geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
            geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
            geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
            geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
            geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
            geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
            geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
            geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
            geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
            geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
            geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
            geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
            geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
            # Update window dimensions
            geometryNodes_modifier['Socket_34'] = window_width
            geometryNodes_modifier['Socket_35'] = window_height
            geometryNodes_modifier.show_on_cage = True
            geometryNodes_modifier.show_on_cage = False
            return True

        def update_all_gaussian_splats(scene, force_update=False):
            if not scene.get('gaussian_splat_updates_active', False):
                return
            current_frame = scene.frame_current
            last_updated_frame = scene.get('last_updated_frame', -1)
            # Update if forced or if the frame has changed
            if not force_update and current_frame == last_updated_frame:
                return
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    view_matrix = area.spaces.active.region_3d.view_matrix
                    proj_matrix = area.spaces.active.region_3d.window_matrix
                    window_width = area.width
                    window_height = area.height
                    break
            else:
                print("Error: No 3D View found to update camera information.")
                return
            updated_count = 0
            for obj in scene.objects:
                if obj.visible_get() and obj.get('update_rot_to_cam', False):
                    if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                        updated_count += 1
            print(f"Updated {updated_count} Gaussian Splat object(s) at frame {current_frame}")
            scene['last_updated_frame'] = current_frame

        def frame_change_update(scene):
            update_all_gaussian_splats(scene, force_update=False)

        def continuous_update():
            if bpy.context.scene.get('gaussian_splat_updates_active', False):
                update_all_gaussian_splats(bpy.context.scene, force_update=True)
                return 0  # Update as fast as possible
            return None  # Stop the timer if updates are not active

        def stop_all_updates():
            bpy.context.scene['gaussian_splat_updates_active'] = False
            # Remove frame change handler
            for handler in bpy.app.handlers.frame_change_post:
                if handler.__name__ == 'frame_change_update':
                    bpy.app.handlers.frame_change_post.remove(handler)
            # Stop continuous update timer
            if bpy.app.timers.is_registered(continuous_update):
                bpy.app.timers.unregister(continuous_update)
            if 'last_updated_frame' in bpy.context.scene:
                del bpy.context.scene['last_updated_frame']
            print("All Gaussian Splat update processes stopped.")

        def start_gaussian_splat_updates(update_method: str):
            if update_method not in ['frame_change', 'Continuous']:
                print("Error: Update method must be either 'frame_change' or 'Continuous'.")
                return False
            # Stop any existing update processes
            stop_all_updates()
            bpy.context.scene['gaussian_splat_updates_active'] = True
            bpy.context.scene['last_updated_frame'] = -1  # Initialize last updated frame
            if update_method == 'frame_change':
                bpy.app.handlers.frame_change_post.append(frame_change_update)
                print("Gaussian Splat update process started for all eligible objects on frame change")
            elif update_method == 'Continuous':
                bpy.app.timers.register(continuous_update, persistent=True)
                print("Gaussian Splat update process started for all eligible objects in continuous mode")
            return True
        # Serpens execution
        update_method = input_update_method  # This will be set by Serpens to either 'frame_change' or 'Continuous'
        if update_method not in ['frame_change', 'Continuous']:
            print("Error: Update method must be either 'frame_change' or 'Continuous'.")
        else:
            result = start_gaussian_splat_updates(update_method)
            if result:
                print(f"Update process started successfully using method: {update_method}")
            else:
                print("Failed to start update process.")
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs__Stop_Camera_Update_88568(bpy.types.Operator):
    bl_idname = "sna.dgs__stop_camera_update_88568"
    bl_label = "3DGS - Stop Camera Update"
    bl_description = "Stops updating the 3DGS_Render modifier for all objects."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        import os

        def stop_gaussian_splat_updates():
            # Remove specific frame change handlers
            handlers_to_remove = [handler for handler in bpy.app.handlers.frame_change_post 
                                  if handler.__name__ == 'frame_change_update']
            for handler in handlers_to_remove:
                bpy.app.handlers.frame_change_post.remove(handler)
            # Stop the timer
            if bpy.app.timers.is_registered(continuous_update):
                bpy.app.timers.unregister(continuous_update)
            # Set the flag to stop updates
            bpy.context.scene['gaussian_splat_updates_active'] = False
            if 'last_updated_frame' in bpy.context.scene:
                del bpy.context.scene['last_updated_frame']
            print("Gaussian Splat update process stopped.")
            return True

        def continuous_update():
            # This function needs to be defined here for unregistering
            if bpy.context.scene.get('gaussian_splat_updates_active', False):
                update_all_gaussian_splats(bpy.context.scene, force_update=True)
                return 0  # Update as fast as possible
            return None  # Stop the timer if updates are not active

        def update_all_gaussian_splats(scene, force_update=False):
            # This function needs to be defined here for completeness
            pass
        # Serpens execution
        result = stop_gaussian_splat_updates()
        if result:
            print("Update process stopped successfully.")
        else:
            print("Failed to stop update process.")
        for i_2F9A8 in range(len(bpy.data.objects)):
            if (property_exists("bpy.data.objects[i_2F9A8].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.data.objects[i_2F9A8].modifiers):
                bpy.data.objects[i_2F9A8].modifiers['KIRI_3DGS_Render_GN'].show_on_cage = True
                bpy.data.objects[i_2F9A8].modifiers['KIRI_3DGS_Render_GN'].show_in_editmode = True
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_camera_update_mode_function_interface_B961D(layout_function, ):
    col_1A281 = layout_function.column(heading='', align=True)
    col_1A281.alert = False
    col_1A281.enabled = True
    col_1A281.active = True
    col_1A281.use_property_split = False
    col_1A281.use_property_decorate = False
    col_1A281.scale_x = 1.0
    col_1A281.scale_y = 1.0
    col_1A281.alignment = 'Expand'.upper()
    col_1A281.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_3A687 = col_1A281.box()
    box_3A687.alert = False
    box_3A687.enabled = True
    box_3A687.active = True
    box_3A687.use_property_split = False
    box_3A687.use_property_decorate = False
    box_3A687.alignment = 'Expand'.upper()
    box_3A687.scale_x = 1.0
    box_3A687.scale_y = 1.0
    if not True: box_3A687.operator_context = "EXEC_DEFAULT"
    box_3A687.label(text='Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
    box_3A687.prop(bpy.context.scene, 'sna_kiri3dgs_scene_camera_refresh_mode', text='', icon_value=0, emboss=True)
    box_BB246 = col_1A281.box()
    box_BB246.alert = (bpy.context.scene['gaussian_splat_updates_active'] if 'gaussian_splat_updates_active' in bpy.context.scene else False)
    box_BB246.enabled = True
    box_BB246.active = True
    box_BB246.use_property_split = False
    box_BB246.use_property_decorate = False
    box_BB246.alignment = 'Expand'.upper()
    box_BB246.scale_x = 1.0
    box_BB246.scale_y = 1.0
    if not True: box_BB246.operator_context = "EXEC_DEFAULT"
    if (bpy.context.scene['gaussian_splat_updates_active'] if 'gaussian_splat_updates_active' in bpy.context.scene else False):
        op = box_BB246.operator('sna.dgs__stop_camera_update_88568', text='Stop Camera Update', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
    else:
        op = box_BB246.operator('sna.dgs__start_camera_update_001bd', text='Start Camera Update', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera-7391968-white.png')), emboss=True, depress=False)
    op = box_BB246.operator('sna.dgs__update_camera_single_time_03530', text='Update All To View', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'eye-6926444-white.png')), emboss=True, depress=False)


class SNA_OT_Dgs__Update_Camera_Single_Time_03530(bpy.types.Operator):
    bl_idname = "sna.dgs__update_camera_single_time_03530"
    bl_label = "3DGS - Update Camera (Single Time)"
    bl_description = "Updates the 3DGS_Render modifier once for all enabled objects in the scene."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_dgs__update_camera_single_time_function_execute_9C695()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_dgs__update_camera_single_time_function_execute_9C695():
    updated_objects = None
    from mathutils import Matrix
    # Define helper function for updating the geometry node sockets

    def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
        geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
        if not geometryNodes_modifier:
            print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
            return False
        # Update view matrix
        geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
        geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
        geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
        geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
        geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
        geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
        geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
        geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
        geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
        geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
        geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
        geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
        geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
        geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
        geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
        geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
        # Update projection matrix
        geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
        geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
        geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
        geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
        geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
        geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
        geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
        geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
        geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
        geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
        geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
        geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
        geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
        geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
        geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
        geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
        # Update window dimensions
        geometryNodes_modifier['Socket_34'] = window_width
        geometryNodes_modifier['Socket_35'] = window_height
        return True
    # Main code for updating all relevant objects
    updated_objects = []
    # Find view and projection matrices from the 3D view area
    found_3d_view = False
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            view_matrix = area.spaces.active.region_3d.view_matrix
            proj_matrix = area.spaces.active.region_3d.window_matrix
            window_width = area.width
            window_height = area.height
            found_3d_view = True
            break
    if not found_3d_view:
        print("Error: No 3D View found to update camera information.")
    else:
        # Loop through objects and update those marked for update
        for obj in bpy.context.scene.objects:
            if obj.visible_get() and obj.get('update_rot_to_cam', False):
                print(f"Attempting to update object: {obj.name}")  # Debugging print
                if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                    updated_objects.append(obj.name)  # Add to updated list
    # Print or output the list of updated objects
    print("Updated objects:", updated_objects)
    for i_13DD6 in range(len(updated_objects)):
        bpy.data.objects[updated_objects[i_13DD6]].update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()


@persistent
def load_pre_handler_F6F13(dummy):
    bpy.context.scene['gaussian_splat_updates_active'] = False
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


class SNA_OT_Open_Blender_Splat_Render_Documentation_1Eac5(bpy.types.Operator):
    bl_idname = "sna.open_blender_splat_render_documentation_1eac5"
    bl_label = "Open Blender Splat Render Documentation"
    bl_description = "Launches a browser with the addon documentation"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.app/blender-addon/3dgs-render'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Open_Blender_Splat_Render_Tutorial_Video_A4Fe6(bpy.types.Operator):
    bl_idname = "sna.open_blender_splat_render_tutorial_video_a4fe6"
    bl_label = "Open Blender Splat Render Tutorial Video"
    bl_description = "Launches a browser with the addon documentation video"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://youtu.be/vBU8b9vrKrk'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_edit_points_function_interface_906CF(layout_function, ):
    layout_function = layout_function
    sna_edit_points_import_function_interface_8E4CD(layout_function, )
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Point_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
        layout_function = layout_function
        sna_edit_points_modifier_properties_function_interface_1EEBD(layout_function, )
    layout_function = layout_function
    sna_edit_points_export_function_interface_0D64D(layout_function, )


def sna_edit_points_export_function_interface_0D64D(layout_function, ):
    box_1C944 = layout_function.box()
    box_1C944.alert = False
    box_1C944.enabled = True
    box_1C944.active = True
    box_1C944.use_property_split = False
    box_1C944.use_property_decorate = False
    box_1C944.alignment = 'Expand'.upper()
    box_1C944.scale_x = 1.0
    box_1C944.scale_y = 1.0
    if not True: box_1C944.operator_context = "EXEC_DEFAULT"
    op = box_1C944.operator('sna.export_points_for_3dgs_63cd8', text='Export Points For 3DGS', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'export-7322163-white.png')), emboss=True, depress=False)


class SNA_OT_Import_Ply_As_Points_E9E21(bpy.types.Operator):
    bl_idname = "sna.import_ply_as_points_e9e21"
    bl_label = "Import .PLY as points"
    bl_description = "Imports a .ply file as a point cloud."
    bl_options = {"REGISTER", "UNDO"}
    sna_auto_rotate_on_import: bpy.props.BoolProperty(name='Auto Rotate On Import', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.wm.ply_import('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_D45CB = layout.box()
        box_D45CB.alert = True
        box_D45CB.enabled = True
        box_D45CB.active = True
        box_D45CB.use_property_split = False
        box_D45CB.use_property_decorate = False
        box_D45CB.alignment = 'Expand'.upper()
        box_D45CB.scale_x = 1.0
        box_D45CB.scale_y = 1.0
        if not True: box_D45CB.operator_context = "EXEC_DEFAULT"
        box_D45CB.label(text='DO NOT APPLY TRANSFORMS', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
        box_D45CB.label(text='You are free to rotate / scale / move your object in object mode while editing', icon_value=17)
        box_D45CB.label(text="Do not apply transforms or rotate/scale in 'edit' mode.", icon_value=17)
        box_D45CB.label(text="Using the 'Export Points For 3DGS' button will revert scale and rotation transforms before exporting.", icon_value=17)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=700)


class SNA_OT_Remove_Point_Edit_Modifier_47851(bpy.types.Operator):
    bl_idname = "sna.remove_point_edit_modifier_47851"
    bl_label = "Remove Point Edit modifier"
    bl_description = "Removes the Point Edit modifier from the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Refresh_Point_Edit_Modifier_Ec829(bpy.types.Operator):
    bl_idname = "sna.refresh_point_edit_modifier_ec829"
    bl_label = "Refresh Point Edit Modifier"
    bl_description = "Updates geometry edits from the Point Edit modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'].show_viewport = True
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Append_Point_Edit_Modifier_A0188(bpy.types.Operator):
    bl_idname = "sna.append_point_edit_modifier_a0188"
    bl_label = "Append Point Edit Modifier"
    bl_description = "Appends a modifier to the selected point cloud for editing and colour visualising."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if property_exists("bpy.data.node_groups['KIRI_3DGS_Point_Edit_GN']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.node_groups)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\NodeTree', filename='KIRI_3DGS_Point_Edit_GN', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
            appended_B2734 = None if not new_data else new_data[0]
        if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.materials)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
            appended_459F4 = None if not new_data else new_data[0]
        geonodemodreturn_0_f22b7 = sna_add_geo_nodes__append_group_2D522_F22B7(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Point_Edit_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Point_Edit_GN')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_6'] = bpy.data.materials['KIRI_3DGS_Render_Material']
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_edit_points_import_function_interface_8E4CD(layout_function, ):
    box_70822 = layout_function.box()
    box_70822.alert = False
    box_70822.enabled = True
    box_70822.active = True
    box_70822.use_property_split = False
    box_70822.use_property_decorate = False
    box_70822.alignment = 'Expand'.upper()
    box_70822.scale_x = 1.0
    box_70822.scale_y = 1.0
    if not True: box_70822.operator_context = "EXEC_DEFAULT"
    op = box_70822.operator('sna.import_ply_as_points_e9e21', text='Import .PLY As Points', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'import-7102651-white.png')), emboss=True, depress=False)
    op.sna_auto_rotate_on_import = False
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Point_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
            pass
        else:
            if bpy.context.view_layer.objects.active.type == 'MESH':
                if (len(bpy.context.view_layer.objects.active.data.polygons) >= 1):
                    pass
                else:
                    if 'OBJECT'==bpy.context.mode:
                        op = box_70822.operator('sna.append_point_edit_modifier_a0188', text='Append Point Edit Modifier', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'wrench-1599876-white.png')), emboss=True, depress=False)


def sna_edit_points_modifier_properties_function_interface_1EEBD(layout_function, ):
    box_81CE8 = layout_function.box()
    box_81CE8.alert = False
    box_81CE8.enabled = True
    box_81CE8.active = True
    box_81CE8.use_property_split = False
    box_81CE8.use_property_decorate = False
    box_81CE8.alignment = 'Expand'.upper()
    box_81CE8.scale_x = 1.0
    box_81CE8.scale_y = 1.0
    if not True: box_81CE8.operator_context = "EXEC_DEFAULT"
    row_69E53 = box_81CE8.row(heading='', align=False)
    row_69E53.alert = False
    row_69E53.enabled = True
    row_69E53.active = True
    row_69E53.use_property_split = False
    row_69E53.use_property_decorate = False
    row_69E53.scale_x = 1.0
    row_69E53.scale_y = 1.0
    row_69E53.alignment = 'Expand'.upper()
    row_69E53.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_69E53.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], 'show_viewport', text='', icon_value=0, emboss=True)
    op = row_69E53.operator('sna.remove_point_edit_modifier_47851', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
    op = row_69E53.operator('sna.refresh_point_edit_modifier_ec829', text='Refresh', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'refresh-7390745 - white.png')), emboss=True, depress=False)
    op = row_69E53.operator('sna.apply_point_edit_modifier_d6b08', text='Apply', icon_value=36, emboss=True, depress=False)
    box_86931 = layout_function.box()
    box_86931.alert = False
    box_86931.enabled = True
    box_86931.active = True
    box_86931.use_property_split = False
    box_86931.use_property_decorate = False
    box_86931.alignment = 'Expand'.upper()
    box_86931.scale_x = 1.0
    box_86931.scale_y = 1.0
    if not True: box_86931.operator_context = "EXEC_DEFAULT"
    op = box_86931.operator('sna.append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'sphere-6796353-white.png')), emboss=True, depress=False)
    op = box_86931.operator('sna.append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cube-4212258-white.png')), emboss=True, depress=False)
    box_F8921 = layout_function.box()
    box_F8921.alert = False
    box_F8921.enabled = True
    box_F8921.active = True
    box_F8921.use_property_split = False
    box_F8921.use_property_decorate = False
    box_F8921.alignment = 'Expand'.upper()
    box_F8921.scale_x = 1.0
    box_F8921.scale_y = 1.0
    if not True: box_F8921.operator_context = "EXEC_DEFAULT"
    box_F8921.label(text='Point Scale', icon_value=0)
    attr_C7885 = '["' + str('Socket_19' + '"]') 
    box_F8921.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_C7885, text='', icon_value=0, emboss=True)
    box_3294E = layout_function.box()
    box_3294E.alert = False
    box_3294E.enabled = True
    box_3294E.active = True
    box_3294E.use_property_split = False
    box_3294E.use_property_decorate = False
    box_3294E.alignment = 'Expand'.upper()
    box_3294E.scale_x = 1.0
    box_3294E.scale_y = 1.0
    if not True: box_3294E.operator_context = "EXEC_DEFAULT"
    box_C2D6E = box_3294E.box()
    box_C2D6E.alert = False
    box_C2D6E.enabled = True
    box_C2D6E.active = True
    box_C2D6E.use_property_split = False
    box_C2D6E.use_property_decorate = False
    box_C2D6E.alignment = 'Expand'.upper()
    box_C2D6E.scale_x = 1.0
    box_C2D6E.scale_y = 1.0
    if not True: box_C2D6E.operator_context = "EXEC_DEFAULT"
    attr_F84FA = '["' + str('Socket_2' + '"]') 
    box_C2D6E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_F84FA, text='Enable Auto Crop BG Sphere', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_2']:
        col_B395E = box_C2D6E.column(heading='', align=False)
        col_B395E.alert = False
        col_B395E.enabled = True
        col_B395E.active = True
        col_B395E.use_property_split = False
        col_B395E.use_property_decorate = False
        col_B395E.scale_x = 1.0
        col_B395E.scale_y = 1.0
        col_B395E.alignment = 'Expand'.upper()
        col_B395E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_F3669 = '["' + str('Socket_7' + '"]') 
        col_B395E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_F3669, text='Sphere threshold', icon_value=0, emboss=True)
        attr_E7BC5 = '["' + str('Socket_21' + '"]') 
        col_B395E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_E7BC5, text='Invert', icon_value=0, emboss=True, toggle=True)
    box_BFED0 = box_3294E.box()
    box_BFED0.alert = False
    box_BFED0.enabled = True
    box_BFED0.active = True
    box_BFED0.use_property_split = False
    box_BFED0.use_property_decorate = False
    box_BFED0.alignment = 'Expand'.upper()
    box_BFED0.scale_x = 1.0
    box_BFED0.scale_y = 1.0
    if not True: box_BFED0.operator_context = "EXEC_DEFAULT"
    attr_D8FF2 = '["' + str('Socket_20' + '"]') 
    box_BFED0.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_D8FF2, text='Enable Crop Box', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_20']:
        col_725F8 = box_BFED0.column(heading='', align=False)
        col_725F8.alert = False
        col_725F8.enabled = True
        col_725F8.active = True
        col_725F8.use_property_split = False
        col_725F8.use_property_decorate = False
        col_725F8.scale_x = 1.0
        col_725F8.scale_y = 1.0
        col_725F8.alignment = 'Expand'.upper()
        col_725F8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_32DFD = '["' + str('Socket_3' + '"]') 
        col_725F8.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_32DFD, text='', icon_value=0, emboss=True)
        attr_B3084 = '["' + str('Socket_4' + '"]') 
        col_725F8.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_B3084, text='', icon_value=0, emboss=True, toggle=True)
    if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_4'] == 1) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_4'] == 2)):
        attr_215E7 = '["' + str('Socket_5' + '"]') 
        box_BFED0.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_215E7, text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    box_FEB97 = box_3294E.box()
    box_FEB97.alert = False
    box_FEB97.enabled = True
    box_FEB97.active = True
    box_FEB97.use_property_split = False
    box_FEB97.use_property_decorate = False
    box_FEB97.alignment = 'Expand'.upper()
    box_FEB97.scale_x = 1.0
    box_FEB97.scale_y = 1.0
    if not True: box_FEB97.operator_context = "EXEC_DEFAULT"
    attr_FB39D = '["' + str('Socket_9' + '"]') 
    box_FEB97.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_FB39D, text='Remove Isolated Points', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_9']:
        col_28580 = box_FEB97.column(heading='', align=False)
        col_28580.alert = False
        col_28580.enabled = True
        col_28580.active = True
        col_28580.use_property_split = False
        col_28580.use_property_decorate = False
        col_28580.scale_x = 1.0
        col_28580.scale_y = 1.0
        col_28580.alignment = 'Expand'.upper()
        col_28580.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_DB2DC = '["' + str('Socket_8' + '"]') 
        col_28580.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_DB2DC, text='Distance threshold', icon_value=0, emboss=True)
    box_713CF = box_3294E.box()
    box_713CF.alert = False
    box_713CF.enabled = True
    box_713CF.active = True
    box_713CF.use_property_split = False
    box_713CF.use_property_decorate = False
    box_713CF.alignment = 'Expand'.upper()
    box_713CF.scale_x = 1.0
    box_713CF.scale_y = 1.0
    if not True: box_713CF.operator_context = "EXEC_DEFAULT"
    attr_23921 = '["' + str('Socket_13' + '"]') 
    box_713CF.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_23921, text='Colour Edit', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_13']:
        col_DB052 = box_713CF.column(heading='', align=False)
        col_DB052.alert = False
        col_DB052.enabled = True
        col_DB052.active = True
        col_DB052.use_property_split = False
        col_DB052.use_property_decorate = False
        col_DB052.scale_x = 1.0
        col_DB052.scale_y = 1.0
        col_DB052.alignment = 'Expand'.upper()
        col_DB052.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_DCC91 = '["' + str('Socket_17' + '"]') 
        col_DB052.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_DCC91, text='', icon_value=0, emboss=True)
        attr_EC650 = '["' + str('Socket_15' + '"]') 
        col_DB052.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_EC650, text='', icon_value=0, emboss=True)
        attr_143D6 = '["' + str('Socket_28' + '"]') 
        col_DB052.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_143D6, text='Hue Threshold', icon_value=0, emboss=True)
        attr_2184D = '["' + str('Socket_29' + '"]') 
        col_DB052.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_2184D, text='Saturation Threshold', icon_value=0, emboss=True)
        attr_9FF85 = '["' + str('Socket_30' + '"]') 
        col_DB052.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_9FF85, text='Value Threshold', icon_value=0, emboss=True)
    box_9FF22 = box_3294E.box()
    box_9FF22.alert = False
    box_9FF22.enabled = True
    box_9FF22.active = True
    box_9FF22.use_property_split = False
    box_9FF22.use_property_decorate = False
    box_9FF22.alignment = 'Expand'.upper()
    box_9FF22.scale_x = 1.0
    box_9FF22.scale_y = 1.0
    if not True: box_9FF22.operator_context = "EXEC_DEFAULT"
    attr_CFACB = '["' + str('Socket_24' + '"]') 
    box_9FF22.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_CFACB, text='Enable Decimate', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_24']:
        col_DE786 = box_9FF22.column(heading='', align=False)
        col_DE786.alert = False
        col_DE786.enabled = True
        col_DE786.active = True
        col_DE786.use_property_split = False
        col_DE786.use_property_decorate = False
        col_DE786.scale_x = 1.0
        col_DE786.scale_y = 1.0
        col_DE786.alignment = 'Expand'.upper()
        col_DE786.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_65A8B = '["' + str('Socket_25' + '"]') 
        col_DE786.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_65A8B, text='Decimate Percentage', icon_value=0, emboss=True)
        attr_59851 = '["' + str('Socket_26' + '"]') 
        col_DE786.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_59851, text='Decimate Seed', icon_value=0, emboss=True)


class SNA_OT_Export_Points_For_3Dgs_63Cd8(bpy.types.Operator):
    bl_idname = "sna.export_points_for_3dgs_63cd8"
    bl_label = "Export Points For 3DGS"
    bl_description = "Resets scale and rotation transforms, applies the Point Edit modifier and exports the active object for 3DGS reimporting"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.view_layer.objects.active == None):
            self.report({'ERROR'}, message='No active object')
        else:
            if (len(bpy.context.view_layer.objects.selected) > 1):
                self.report({'ERROR'}, message='Only select 1 object please.')
            else:
                bpy.context.view_layer.objects.active.select_set(state=True, view_layer=bpy.context.view_layer, )
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Point_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
                    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_22'] = True
                    bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
                    bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Point_Edit_GN', report=False, merge_customdata=False, single_user=False, use_selected_objects=False)
                bpy.context.view_layer.objects.active.scale = (1.0, 1.0, 1.0)
                bpy.context.view_layer.objects.active.rotation_euler = (0.0, 0.0, 0.0)
                bpy.ops.wm.ply_export('INVOKE_DEFAULT', apply_modifiers=True, export_selected_objects=True, export_attributes=True)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Apply_Point_Edit_Modifier_D6B08(bpy.types.Operator):
    bl_idname = "sna.apply_point_edit_modifier_d6b08"
    bl_label = "Apply Point Edit Modifier"
    bl_description = "Applies the Point Edit modifier for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_22'] = True
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Point_Edit_GN'
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Hq_Render_B89Bf(bpy.types.Operator):
    bl_idname = "sna.hq_render_b89bf"
    bl_label = "HQ Render"
    bl_description = "Offline renders maximum quality (blended alpha) versions of all enabled 3DGS objects using current render settings."
    bl_options = {"REGISTER", "UNDO"}
    sna_render_animation: bpy.props.BoolProperty(name='Render Animation', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        import subprocess
        from mathutils import Matrix, Vector
        import os
        if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.materials)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
            appended_54167 = None if not new_data else new_data[0]
        if property_exists("bpy.data.node_groups['KIRI_3DGS_Restore_Origpos_GN']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.node_groups)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\NodeTree', filename='KIRI_3DGS_Restore_Origpos_GN', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
            appended_D2ADF = None if not new_data else new_data[0]
        bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method = 'BLENDED'
        kiri_3dgs_render__hq_render['sna_hq_render_base_object_list'] = []
        kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'] = []
        for i_534B6 in range(len(bpy.data.objects)):
            if ('GS_ID' in bpy.data.objects[i_534B6] and (not bpy.data.objects[i_534B6].hide_render)):
                kiri_3dgs_render__hq_render['sna_hq_render_base_object_list'].append(bpy.data.objects[i_534B6])
        for i_86401 in range(len(kiri_3dgs_render__hq_render['sna_hq_render_base_object_list'])):
            source_obj_name = kiri_3dgs_render__hq_render['sna_hq_render_base_object_list'][i_86401].name
            offset_x = 0.0
            new_object_name = None
            # Input variables
            #source_obj_name = "Cube"  # Change this to your object's name
            #offset_x = 0.0  # Input float variable for X offset
            # Get the source object
            source_obj = bpy.data.objects.get(source_obj_name)
            # Check if the object exists
            if source_obj:
                # Create a copy of the object
                new_obj = source_obj.copy()
                new_obj.data = source_obj.data.copy()
                # Link the new object to the scene
                bpy.context.scene.collection.objects.link(new_obj)
                # Apply the offset if any
                new_obj.location.x += offset_x
                # Store the new object's name in a variable
                new_object_name = new_obj.name
            else:
                new_object_name = "ERROR: Source object not found"
            # Output the new object's name (this will be captured by Serpens)
            print(new_object_name)
            kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'].append(new_object_name)
        for i_10AF9 in range(len(kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'])):
            object_name = kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'][i_10AF9]
            # Replace this with your object's name
            #object_name = "YourObjectName"
            # Get the object
            obj = bpy.data.objects.get(object_name)
            if obj:
                # Make sure the object is selected and active
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Apply all modifiers
                for modifier in obj.modifiers[:]:  # [:] creates a copy of the list to avoid modification issues
                    try:
                        bpy.ops.object.modifier_apply(modifier=modifier.name)
                        print(f"Applied modifier: {modifier.name}")
                    except Exception as e:
                        print(f"Failed to apply modifier {modifier.name}: {str(e)}")
            else:
                print(f"Object '{object_name}' not found")
            modifier_9CFE8 = bpy.data.objects[kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'][i_10AF9]].modifiers.new(name='KIRI_3DGS_Restore_Origpos_GN', type='NODES', )
            modifier_9CFE8.node_group = bpy.data.node_groups['KIRI_3DGS_Restore_Origpos_GN']
            object_name = kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'][i_10AF9]
            # Replace this with your object's name
            #object_name = "YourObjectName"
            # Get the object
            obj = bpy.data.objects.get(object_name)
            if obj:
                # Make sure the object is selected and active
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Apply all modifiers
                for modifier in obj.modifiers[:]:  # [:] creates a copy of the list to avoid modification issues
                    try:
                        bpy.ops.object.modifier_apply(modifier=modifier.name)
                        print(f"Applied modifier: {modifier.name}")
                    except Exception as e:
                        print(f"Failed to apply modifier {modifier.name}: {str(e)}")
            else:
                print(f"Object '{object_name}' not found")
            modifier_1E994 = bpy.data.objects[kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'][i_10AF9]].modifiers.new(name='KIRI_3DGS_Render_GN', type='NODES', )
            modifier_1E994.node_group = bpy.data.node_groups['KIRI_3DGS_Render_GN']
        for i_9B7EB in range(len(kiri_3dgs_render__hq_render['sna_hq_render_base_object_list'])):
            kiri_3dgs_render__hq_render['sna_hq_render_base_object_list'][i_9B7EB].hide_render = True
        render_animation = self.sna_render_animation
        sorter_path = bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences.sna_hq_sorter_directory

        def check_operating_system():
            from platform import system
            os_name = system()
            if os_name == "Windows":
                return True
            elif os_name == "Darwin":
                return False
            else:
                print("This addon doesn't support " + os_name)
                print("please try window or mac")
                exit(0)

        def create_render_object(obj : bpy.types.Object, splatID_array):
            orig_mesh : bpy.types.Mesh = obj.data
            new_mesh : bpy.types.Mesh = orig_mesh.copy()
            new_obj : bpy.types.Object = bpy.data.objects.new(f"{obj.name}_temp_render_object", new_mesh)
            # Copy transform exactly as original does
            new_obj.location = obj.location.copy()
            new_obj.rotation_euler = obj.rotation_euler.copy()
            new_obj.scale = obj.scale.copy()    
            splat_count = len(orig_mesh.polygons) // 2
            # Initialize arrays exactly as original does
            Vrk_1 = [0.0] * splat_count * 2 * 1 
            Vrk_2 = [0.0] * splat_count * 2 * 1
            Vrk_3 = [0.0] * splat_count * 2 * 1
            Vrk_4 = [0.0] * splat_count * 2 * 1
            Vrk_5 = [0.0] * splat_count * 2 * 1
            Vrk_6 = [0.0] * splat_count * 2 * 1
            center = [0.0] * splat_count * 2 * 3 
            color = [0.0] * splat_count * 2 * 4
            # Copy data using original exact indexing pattern
            for i in range(splat_count):
                splat_id = splatID_array[i] 
                # Vrk values - using exact 2 * splat_id + 0 indexing
                Vrk_1[2 * i + 0] = orig_mesh.attributes["Vrk_1"].data[2 * splat_id + 0].value
                Vrk_1[2 * i + 1] = orig_mesh.attributes["Vrk_1"].data[2 * splat_id + 0].value
                Vrk_2[2 * i + 0] = orig_mesh.attributes["Vrk_2"].data[2 * splat_id + 0].value
                Vrk_2[2 * i + 1] = orig_mesh.attributes["Vrk_2"].data[2 * splat_id + 0].value
                Vrk_3[2 * i + 0] = orig_mesh.attributes["Vrk_3"].data[2 * splat_id + 0].value
                Vrk_3[2 * i + 1] = orig_mesh.attributes["Vrk_3"].data[2 * splat_id + 0].value
                Vrk_4[2 * i + 0] = orig_mesh.attributes["Vrk_4"].data[2 * splat_id + 0].value
                Vrk_4[2 * i + 1] = orig_mesh.attributes["Vrk_4"].data[2 * splat_id + 0].value
                Vrk_5[2 * i + 0] = orig_mesh.attributes["Vrk_5"].data[2 * splat_id + 0].value
                Vrk_5[2 * i + 1] = orig_mesh.attributes["Vrk_5"].data[2 * splat_id + 0].value
                Vrk_6[2 * i + 0] = orig_mesh.attributes["Vrk_6"].data[2 * splat_id + 0].value
                Vrk_6[2 * i + 1] = orig_mesh.attributes["Vrk_6"].data[2 * splat_id + 0].value
                # Center values - maintaining original exact indexing
                orig_center = orig_mesh.attributes["center"].data[2 * splat_id].vector
                center[6 * i + 0] = orig_center[0]
                center[6 * i + 1] = orig_center[1]
                center[6 * i + 2] = orig_center[2]
                center[6 * i + 3] = orig_center[0]
                center[6 * i + 4] = orig_center[1]
                center[6 * i + 5] = orig_center[2]
                # Color values - maintaining original exact indexing
                orig_color = orig_mesh.attributes["color"].data[2 * splat_id].color
                color[8 * i + 0] = orig_color[0]
                color[8 * i + 1] = orig_color[1]
                color[8 * i + 2] = orig_color[2]
                color[8 * i + 3] = orig_color[3]
                color[8 * i + 4] = orig_color[0]
                color[8 * i + 5] = orig_color[1]
                color[8 * i + 6] = orig_color[2]
                color[8 * i + 7] = orig_color[3]
                #tex_coord[12 * i + 0] = -2.0
                #tex_coord[12 * i + 1] = -2.0
                #tex_coord[12 * i + 2] = float(i)
                #tex_coord[12 * i + 3] = 2.0
                #tex_coord[12 * i + 4] = -2.0
                #tex_coord[12 * i + 5] = float(i)
                #tex_coord[12 * i + 6] = 2.0
                #tex_coord[12 * i + 7] = 2.0
                #tex_coord[12 * i + 8] = float(i)
                #tex_coord[12 * i + 9] = -2.0
                #tex_coord[12 * i + 10] = 2.0
                #tex_coord[12 * i + 11] = float(i)
            # Create attributes exactly as original does
            # center_attr : bpy.types.FloatVectorAttribute = new_mesh.attributes.new(name="center", type='FLOAT_VECTOR', domain='FACE')
            center_attr : bpy.types.FloatVectorAttribute = new_mesh.attributes.get("center")
            center_attr.data.foreach_set("vector", center)
            #color_attr : bpy.types.ByteColorAttribute = new_mesh.attributes.new(name="color", type='FLOAT_COLOR', domain='FACE')
            color_attr : bpy.types.ByteColorAttribute = new_mesh.attributes.get("color")
            color_attr.data.foreach_set("color", color)
            # Create Vrk attributes with original exact pattern
            #Vrk_1_attr = new_mesh.attributes.new(name="Vrk_1", type='FLOAT', domain='FACE')
            Vrk_1_attr = new_mesh.attributes.get("Vrk_1")
            Vrk_1_attr.data.foreach_set("value", Vrk_1)
            #Vrk_2_attr = new_mesh.attributes.new(name="Vrk_2", type='FLOAT', domain='FACE')
            Vrk_2_attr = new_mesh.attributes.get("Vrk_2")
            Vrk_2_attr.data.foreach_set("value", Vrk_2)
            #Vrk_3_attr = new_mesh.attributes.new(name="Vrk_3", type='FLOAT', domain='FACE')
            Vrk_3_attr = new_mesh.attributes.get("Vrk_3")
            Vrk_3_attr.data.foreach_set("value", Vrk_3)
            #Vrk_4_attr = new_mesh.attributes.new(name="Vrk_4", type='FLOAT', domain='FACE')
            Vrk_4_attr = new_mesh.attributes.get("Vrk_4")
            Vrk_4_attr.data.foreach_set("value", Vrk_4)
            #Vrk_5_attr = new_mesh.attributes.new(name="Vrk_5", type='FLOAT', domain='FACE')
            Vrk_5_attr = new_mesh.attributes.get("Vrk_5")
            Vrk_5_attr.data.foreach_set("value", Vrk_5)
            #Vrk_6_attr = new_mesh.attributes.new(name="Vrk_6", type='FLOAT', domain='FACE')
            Vrk_6_attr = new_mesh.attributes.get("Vrk_6")
            Vrk_6_attr.data.foreach_set("value", Vrk_6)
            # Set up node group and material with high quality render material
            """
            node_group = bpy.data.node_groups['KIRI_3DGS_Render_GN']
            node_modifier : bpy.types.NodesModifier = new_obj.modifiers.new(name="KIRI_3DGS_Render_GN", type='NODES')
            node_modifier.node_group = node_group
            """
            for i in range(splat_count):
                new_mesh.polygons[2 * i   ].vertices = orig_mesh.polygons[2 * splatID_array[i]    ].vertices
                new_mesh.polygons[2 * i +1].vertices = orig_mesh.polygons[2 * splatID_array[i] + 1].vertices
            new_mesh.update()
            # Find and assign high quality render material
            material = None
            for mat in bpy.data.materials:
                if mat.name == "KIRI_3DGS_Render_Material":
                    material = mat
                    break
            if new_obj and new_obj.data:
                if len(new_obj.material_slots) < 1:
                    new_obj.data.materials.append(material)
                else:
                    new_obj.material_slots[0].material = material
            bpy.context.collection.objects.link(new_obj)
            return new_obj

        def update_camera_matrices(obj, camera):
            # Get matrices exactly as original does
            view_matrix = camera.matrix_world.inverted()
            depsgraph = bpy.context.evaluated_depsgraph_get()
            scene = bpy.context.scene
            resolution_x = scene.render.resolution_x
            resolution_y = scene.render.resolution_y
            proj_matrix = camera.calc_matrix_camera(depsgraph,
                                                  x=resolution_x,
                                                  y=resolution_y)
            # Get modifier using exact name
            geometryNodes_modifier = obj.modifiers['KIRI_3DGS_Render_GN']
            # View matrix assignments in exact same order as original
            geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
            geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
            geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
            geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
            geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
            geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
            geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
            geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
            geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
            geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
            geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
            geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
            geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
            geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
            geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
            geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
            # Projection matrix assignments with exact duplicate pattern from original
            geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
            geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
            geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
            geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
            geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
            geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
            geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
            geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
            geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]  # Intentional duplicate as in original code
            geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
            geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
            geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
            geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
            geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
            geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
            geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
            geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
            geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
            geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
            geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
            geometryNodes_modifier['Socket_34'] = resolution_x
            geometryNodes_modifier['Socket_35'] = resolution_y
            # Update trigger exactly as in original code
            geometryNodes_modifier.show_on_cage = True
            geometryNodes_modifier.show_on_cage = False

        def sort_splats(obj, sorter):
            splat_count = len(obj.data.polygons) // 2
            # Create shared memory exactly as original does
            splatID_shm = shared_memory.SharedMemory(create=True, size=splat_count * np.dtype('int32').itemsize)
            camera_shm = shared_memory.SharedMemory(create=True, size=6 * np.dtype('float32').itemsize)
            center_shm = shared_memory.SharedMemory(create=True, size=splat_count * 3 * np.dtype('float32').itemsize)
            # Create numpy arrays with exact same dtypes as original
            splatID_array = np.ndarray((splat_count,), dtype='int32', buffer=splatID_shm.buf)
            camera_array = np.ndarray((6,), dtype='float32', buffer=camera_shm.buf)
            center_array = np.ndarray((splat_count * 3,), dtype='float32', buffer=center_shm.buf)
            # Get camera info using original exact method in obj space
            camera : bpy.types.Camera = bpy.context.scene.camera
            # Camera position exactly as original does
            camera_array[0] =  camera.matrix_world[0][3]
            camera_array[1] =  camera.matrix_world[1][3]
            camera_array[2] =  camera.matrix_world[2][3]
            # Camera direction using original exact Vector.Fill method
            direction : Vector = Vector.Fill(3,0)
            direction.x = camera.matrix_world[0][2]
            direction.y = camera.matrix_world[1][2]
            direction.z = camera.matrix_world[2][2]
            direction.normalize()
            camera_array[3] = direction.x
            camera_array[4] = direction.y
            camera_array[5] = direction.z
            # Get center data using original indexing
            center_data = [0.0] * splat_count * 6
            position_attr = obj.data.attributes["position"]
            position_data = [0.0] * (len(position_attr.data) * 3)
            obj.data.attributes["position"].data.foreach_get("vector", position_data)
            obj.data.attributes["center"].data.foreach_get("vector", center_data)
            for i in range(splat_count):
                center_array[i * 3 + 0] = (position_data[i*12 + 0] + position_data[i*12 + 3] + position_data[i*12 + 6] +position_data[i*12 + 9])/4
                center_array[i * 3 + 1] = (position_data[i*12 + 1] + position_data[i*12 + 4] + position_data[i*12 + 7] +position_data[i*12 + 10])/4
                center_array[i * 3 + 2] = (position_data[i*12 + 2] + position_data[i*12 + 5] + position_data[i*12 + 8] +position_data[i*12 + 11])/4
                #center_array[i * 3 + 0] = center_data[6 * i+0]
                #center_array[i * 3 + 1] = center_data[6 * i+1]
                #center_array[i * 3 + 2] = center_data[6 * i+2]
            # Call sorter using original exact command format
            is_windows = check_operating_system()
            prefix = '' if is_windows else '/'
            print("begin sort")
            command = f"0 {splat_count} {prefix}{splatID_shm.name} {prefix}{camera_shm.name} {prefix}{center_shm.name}\n"
            sorter.stdin.write(command)
            sorter.stdin.flush()
            sorter.stdout.readline()
            print("end sort")
            print(splatID_array)
            print(command)
            # Create render object
            render_obj = create_render_object(joined_obj, splatID_array)
            render_obj.name = "render_object"
            # Cleanup shared memory in original order
            splatID_shm.close()
            camera_shm.close()
            center_shm.close()
            splatID_shm.unlink()
            camera_shm.unlink()
            center_shm.unlink()
            return render_obj
        # Serpens inputs
        #render_animation = False  # Will be set by Serpens
        #sorter_path = r"C:/Users/xiaoh/Desktop/project/3DGS/3DGS-Blender-Addon/3DGS_Sort/win/x64/Release/3DGS_Sort.exe"  # Will be set by Serpens
        # Main render process
        gs_objects = [obj for obj in bpy.context.scene.objects if "GS_ID" in obj and not obj.hide_render]
        print(gs_objects)
        if gs_objects:
            # Start sorter process
            sorter = subprocess.Popen([sorter_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            try:
                if render_animation:
                    scene = bpy.context.scene
                    orig_frame = scene.frame_current
                    # Check if output format is a movie format
                    is_movie_format = scene.render.image_settings.file_format in ['FFMPEG', 'AVI_JPEG', 'AVI_RAW']
                    # If it's a movie format, we don't modify the filepath for each frame
                    if not is_movie_format:
                        original_filepath = scene.render.filepath
                    for frame in range(scene.frame_start, scene.frame_end + 1):
                        scene.frame_set(frame)
                        copied_objects = []
                        # Apply modifiers to ALL objects
                        for obj in gs_objects:
                            bpy.ops.object.select_all(action='DESELECT')
                            obj.select_set(True)
                            bpy.ops.object.duplicate(linked=False)
                            copied_obj = bpy.context.selected_objects[0]
                            bpy.context.view_layer.objects.active = copied_obj
                            update_camera_matrices(copied_obj, bpy.context.scene.camera)
                            bpy.ops.object.modifier_apply(modifier="KIRI_3DGS_Render_GN")
                            bpy.ops.object.transform_apply(
                                location=True,  
                                rotation=True,  
                                scale=True      
                            )
                            obj.hide_render = True
                            copied_objects.append(copied_obj)
                        if copied_objects:
                            # join objects as one , and sort it
                            bpy.ops.object.select_all(action='DESELECT')
                            for obj in copied_objects:
                                obj.select_set(True)
                            bpy.context.view_layer.objects.active = copied_objects[0]
                            copied_objects[0].name = "joined_temp_render_object"
                            bpy.ops.object.join()
                            joined_obj = copied_objects[0]
                            render_obj = sort_splats(joined_obj, sorter)
                            joined_obj.hide_render = True
                            if is_movie_format:
                                # For movie formats, render without write_still
                                bpy.ops.render.render()
                            else:
                                # For image sequences, use write_still and numbered files
                                scene.render.filepath = f"{original_filepath}_{frame:04d}"
                                bpy.ops.render.render(write_still=True)
                            # Safe cleanup with name checking
                            bpy.data.objects.remove(render_obj, do_unlink=True)
                            bpy.data.objects.remove(joined_obj, do_unlink=True)
                    # Restore original filepath if we modified it
                    if not is_movie_format:
                        scene.render.filepath = original_filepath
                    scene.frame_set(orig_frame)
                else:
                    # Single frame render
                    copied_objects = []
                    # Apply modifiers to ALL objects
                    for obj in gs_objects:
                        bpy.ops.object.select_all(action='DESELECT')
                        obj.select_set(True)
                        bpy.ops.object.duplicate(linked=False)
                        copied_obj = bpy.context.selected_objects[0]
                        bpy.context.view_layer.objects.active = copied_obj
                        update_camera_matrices(copied_obj, bpy.context.scene.camera)
                        bpy.ops.object.modifier_apply(modifier="KIRI_3DGS_Render_GN")
                        bpy.ops.object.transform_apply(
                            location=True,  
                            rotation=True,  
                            scale=True      
                        )
                        obj.hide_render = True
                        copied_objects.append(copied_obj)
                    if copied_objects:
                         # join objects as one , and sort it
                        bpy.ops.object.select_all(action='DESELECT')
                        for obj in copied_objects:
                            obj.select_set(True)
                        bpy.context.view_layer.objects.active = copied_objects[0]
                        copied_objects[0].name = "joined_temp_render_object"
                        bpy.ops.object.join()
                        joined_obj = copied_objects[0]
                        render_obj = sort_splats(joined_obj, sorter)
                        joined_obj.hide_render = True
                        bpy.ops.render.render(write_still=True)
                        # Safe cleanup with name checking
                        bpy.data.objects.remove(render_obj, do_unlink=True)
                        bpy.data.objects.remove(joined_obj, do_unlink=True)
                # Restore visibility
                for obj in gs_objects:
                    obj.hide_render = False
            finally:
                # Always cleanup sorter
                if sorter:
                    sorter.terminate()
        for i_3A153 in range(len(kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'])):
            bpy.data.objects.remove(object=bpy.data.objects[kiri_3dgs_render__hq_render['sna_hq_render_origpos_duplicate_list'][i_3A153]], do_unlink=True, )
        for i_30800 in range(len(kiri_3dgs_render__hq_render['sna_hq_render_base_object_list'])):
            kiri_3dgs_render__hq_render['sna_hq_render_base_object_list'][i_30800].hide_render = False
            bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method = 'DITHERED'
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_2C0C3 = layout.box()
        box_2C0C3.alert = True
        box_2C0C3.enabled = True
        box_2C0C3.active = True
        box_2C0C3.use_property_split = False
        box_2C0C3.use_property_decorate = False
        box_2C0C3.alignment = 'Expand'.upper()
        box_2C0C3.scale_x = 1.0
        box_2C0C3.scale_y = 1.0
        if not True: box_2C0C3.operator_context = "EXEC_DEFAULT"
        box_2C0C3.label(text='This is a very performance intensive process - it may take some time', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'info-3016385-white.png')))
        box_2C0C3.label(text='         The rendered object will not respect edit/animate modifiers', icon_value=0)
        box_2C0C3.label(text='         To cancel rendering - force close Blender', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


def sna_hq_render_function_interface_17C41(layout_function, ):
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
    if ((bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences.sna_hq_sorter_directory == 'SELECT SORT FILE') or (bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences.sna_hq_sorter_directory == '')):
        box_30157 = col_249D2.box()
        box_30157.alert = True
        box_30157.enabled = True
        box_30157.active = True
        box_30157.use_property_split = False
        box_30157.use_property_decorate = False
        box_30157.alignment = 'Expand'.upper()
        box_30157.scale_x = 1.0
        box_30157.scale_y = 1.0
        if not True: box_30157.operator_context = "EXEC_DEFAULT"
        box_30157.label(text="Specify 'SORT' file in preferences", icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
    else:
        if (bpy.context.scene.camera == None):
            box_9AC8C = col_249D2.box()
            box_9AC8C.alert = True
            box_9AC8C.enabled = True
            box_9AC8C.active = True
            box_9AC8C.use_property_split = False
            box_9AC8C.use_property_decorate = False
            box_9AC8C.alignment = 'Expand'.upper()
            box_9AC8C.scale_x = 1.0
            box_9AC8C.scale_y = 1.0
            if not True: box_9AC8C.operator_context = "EXEC_DEFAULT"
            box_9AC8C.label(text='No active camera in scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
        else:
            if (bpy.context.scene.render.filepath == ''):
                box_EAECE = col_249D2.box()
                box_EAECE.alert = True
                box_EAECE.enabled = True
                box_EAECE.active = True
                box_EAECE.use_property_split = False
                box_EAECE.use_property_decorate = False
                box_EAECE.alignment = 'Expand'.upper()
                box_EAECE.scale_x = 1.0
                box_EAECE.scale_y = 1.0
                if not True: box_EAECE.operator_context = "EXEC_DEFAULT"
                box_EAECE.label(text='Output path is empty', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
            else:
                col_203A5 = col_249D2.column(heading='', align=False)
                col_203A5.alert = False
                col_203A5.enabled = True
                col_203A5.active = True
                col_203A5.use_property_split = False
                col_203A5.use_property_decorate = False
                col_203A5.scale_x = 1.0
                col_203A5.scale_y = 1.0
                col_203A5.alignment = 'Expand'.upper()
                col_203A5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                box_66291 = col_203A5.box()
                box_66291.alert = (bpy.context.scene.view_settings.view_transform != 'Standard')
                box_66291.enabled = True
                box_66291.active = True
                box_66291.use_property_split = False
                box_66291.use_property_decorate = False
                box_66291.alignment = 'Expand'.upper()
                box_66291.scale_x = 1.0
                box_66291.scale_y = 1.0
                if not True: box_66291.operator_context = "EXEC_DEFAULT"
                if (bpy.context.scene.view_settings.view_transform != 'Standard'):
                    box_66291.label(text='Standard gives most accurate colours', icon_value=0)
                split_B6534 = box_66291.split(factor=0.5111111402511597, align=False)
                split_B6534.alert = False
                split_B6534.enabled = True
                split_B6534.active = True
                split_B6534.use_property_split = False
                split_B6534.use_property_decorate = False
                split_B6534.scale_x = 1.0
                split_B6534.scale_y = 1.0
                split_B6534.alignment = 'Expand'.upper()
                if not True: split_B6534.operator_context = "EXEC_DEFAULT"
                split_B6534.label(text='View Transform', icon_value=0)
                split_B6534.prop(bpy.context.scene.view_settings, 'view_transform', text='', icon_value=0, emboss=True)
                split_C7F1C = box_66291.split(factor=0.5111111402511597, align=False)
                split_C7F1C.alert = False
                split_C7F1C.enabled = True
                split_C7F1C.active = True
                split_C7F1C.use_property_split = False
                split_C7F1C.use_property_decorate = False
                split_C7F1C.scale_x = 1.0
                split_C7F1C.scale_y = 1.0
                split_C7F1C.alignment = 'Expand'.upper()
                if not True: split_C7F1C.operator_context = "EXEC_DEFAULT"
                split_C7F1C.label(text='Look', icon_value=0)
                split_C7F1C.prop(bpy.context.scene.view_settings, 'look', text='', icon_value=0, emboss=True)
                col_203A5.prop(bpy.context.scene.eevee, 'taa_render_samples', text='Samples', icon_value=0, emboss=True)
                col_203A5.prop(bpy.context.scene.render.image_settings, 'file_format', text='', icon_value=0, emboss=True)
                if (bpy.context.scene.render.image_settings.file_format == 'FFMPEG'):
                    box_A372C = col_203A5.box()
                    box_A372C.alert = True
                    box_A372C.enabled = True
                    box_A372C.active = True
                    box_A372C.use_property_split = False
                    box_A372C.use_property_decorate = False
                    box_A372C.alignment = 'Expand'.upper()
                    box_A372C.scale_x = 1.0
                    box_A372C.scale_y = 1.0
                    if not True: box_A372C.operator_context = "EXEC_DEFAULT"
                    box_A372C.label(text='Use an image format', icon_value=0)
                else:
                    box_93DA8 = col_203A5.box()
                    box_93DA8.alert = False
                    box_93DA8.enabled = True
                    box_93DA8.active = True
                    box_93DA8.use_property_split = False
                    box_93DA8.use_property_decorate = False
                    box_93DA8.alignment = 'Expand'.upper()
                    box_93DA8.scale_x = 1.0
                    box_93DA8.scale_y = 1.0
                    if not True: box_93DA8.operator_context = "EXEC_DEFAULT"
                    op = box_93DA8.operator('sna.hq_render_b89bf', text='HQ Render Offline (Image)', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'images-7391277-white.png')), emboss=True, depress=False)
                    op.sna_render_animation = False
                    op = box_93DA8.operator('sna.hq_render_b89bf', text='HQ Render Offline (Animation)', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'movie-7390465-white.png')), emboss=True, depress=False)
                    op.sna_render_animation = True


class SNA_OT_Import_Ply_As_Splats_8458E(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.import_ply_as_splats_8458e"
    bl_label = "Import PLY As Splats"
    bl_description = "Imports a .ply file and adds a series of 3DGS modifiers"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.ply', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.view_settings.view_transform = 'Standard'
        import os

        def stop_gaussian_splat_updates():
            # Remove specific frame change handlers
            handlers_to_remove = [handler for handler in bpy.app.handlers.frame_change_post 
                                  if handler.__name__ == 'frame_change_update']
            for handler in handlers_to_remove:
                bpy.app.handlers.frame_change_post.remove(handler)
            # Stop the timer
            if bpy.app.timers.is_registered(continuous_update):
                bpy.app.timers.unregister(continuous_update)
            # Set the flag to stop updates
            bpy.context.scene['gaussian_splat_updates_active'] = False
            if 'last_updated_frame' in bpy.context.scene:
                del bpy.context.scene['last_updated_frame']
            print("Gaussian Splat update process stopped.")
            return True

        def continuous_update():
            # This function needs to be defined here for unregistering
            if bpy.context.scene.get('gaussian_splat_updates_active', False):
                update_all_gaussian_splats(bpy.context.scene, force_update=True)
                return 0  # Update as fast as possible
            return None  # Stop the timer if updates are not active

        def update_all_gaussian_splats(scene, force_update=False):
            # This function needs to be defined here for completeness
            pass
        # Serpens execution
        result = stop_gaussian_splat_updates()
        if result:
            print("Update process stopped successfully.")
        else:
            print("Failed to stop update process.")
        if property_exists("bpy.data.node_groups['KIRI_3DGS_Render_GN']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.node_groups)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\NodeTree', filename='KIRI_3DGS_Render_GN', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
            appended_CAEF1 = None if not new_data else new_data[0]
        if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.materials)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
            appended_6CC4A = None if not new_data else new_data[0]
        ply_import_path = self.filepath
        import numpy as np
        import os
        try:
            from plyfile import PlyData
        except ImportError:
            print("plyfile is not installed. Please install it to use this feature.")
            PlyData = None
        # Get next available GS_ID

        def get_next_available_gs_id():
            used_ids = set()
            for obj in bpy.data.objects:
                if "GS_ID" in obj:
                    used_ids.add(obj["GS_ID"])
            next_id = 0
            while next_id in used_ids:
                next_id += 1
            return next_id

        def RS_matrix(quat, scale):
            matrix = []
            length = 1/ math.sqrt(quat[0] *quat[0]  + quat[1] *quat[1]  + quat[2] *quat[2] + quat[3] *quat[3] )
            x = quat[0] * length 
            y = quat[1] * length 
            z = quat[2] * length 
            w = quat[3] * length 
            matrix.append(scale[0] * (1 - 2 * (z * z + w * w)))
            matrix.append(scale[0] * (2 * (y * z + x * w)))
            matrix.append(scale[0] * (2 * (y * w - x * z)))
            matrix.append(scale[1] * (2 * (y * z - x * w)))
            matrix.append(scale[1] * (1 - 2 * (y * y + w * w)))
            matrix.append(scale[1] * (2 * (z * w + x * y)))
            matrix.append(scale[2] * (2 * (y * w + x * z)))
            matrix.append(scale[2] * (2 * (z * w - x * y)))
            matrix.append(scale[2] * (1 - 2 * (y * y + z * z)))
            return matrix
        # Serpens will provide this
        #ply_import_path = "C:\\Users\\joe and pig\\Documents\\Flamingo.ply"  # Input from Serpens
        if not ply_import_path:
            print("Error: No file path provided.")
        else:
            if not os.path.exists(ply_import_path):
                print(f"Error: File not found at path {ply_import_path}")
            else:
                # Read PLY file
                plydata = PlyData.read(ply_import_path)
                # Get base filename for object name
                file_base_name = os.path.splitext(os.path.basename(ply_import_path))[0]
                object_name = f"{file_base_name}"
                # Extract data from PLY
                center = np.stack((np.asarray(plydata.elements[0]["x"]),
                                  np.asarray(plydata.elements[0]["y"]),
                                  np.asarray(plydata.elements[0]["z"])), axis=1)
                splat_count = int(len(center))
                N = splat_count
                # Handle opacity
                if 'opacity' in plydata.elements[0]:
                    log_opacities = np.asarray(plydata.elements[0]["opacity"])[..., np.newaxis]
                    opacities = 1 / (1 + np.exp(-log_opacities))
                else:
                    log_opacities = np.asarray(1)[..., np.newaxis]
                    opacities = 1 / (1 + np.exp(-log_opacities))
                opacities = opacities.flatten()
                # Extract features
                features_dc = np.zeros((N, 3, 1))
                features_dc[:, 0, 0] = np.asarray(plydata.elements[0]["f_dc_0"])
                features_dc[:, 1, 0] = np.asarray(plydata.elements[0]["f_dc_1"])
                features_dc[:, 2, 0] = np.asarray(plydata.elements[0]["f_dc_2"])
                # Extract scales and rotations
                log_scales = np.stack((np.asarray(plydata.elements[0]["scale_0"]),
                                     np.asarray(plydata.elements[0]["scale_1"]),
                                     np.asarray(plydata.elements[0]["scale_2"])), axis=1)
                scales = np.exp(log_scales)
                quats = np.stack((np.asarray(plydata.elements[0]["rot_0"]),
                                 np.asarray(plydata.elements[0]["rot_1"]),
                                 np.asarray(plydata.elements[0]["rot_2"]),
                                 np.asarray(plydata.elements[0]["rot_3"])), axis=1)
                # Create geometry
                vertices = []
                indices = []
                for i in range(splat_count):
                    vertices.append((-2.0, -2.0, float(i)))
                    vertices.append((2.0, -2.0, float(i)))
                    vertices.append((2.0, 2.0, float(i)))
                    vertices.append((-2.0, 2.0, float(i)))
                    b = i * 4
                    indices.append((b, b+1, b+2))
                    indices.append((b, b+2, b+3))
                # Create mesh and object
                mesh : bpy.types.Mesh = bpy.data.meshes.new(name=object_name)
                mesh.from_pydata(vertices, [], indices)
                obj : bpy.types.Object = bpy.data.objects.new(object_name, mesh)
                # Create attribute arrays
                Vrk_1 = [0.0] * splat_count * 2 * 1
                Vrk_2 = [0.0] * splat_count * 2 * 1
                Vrk_3 = [0.0] * splat_count * 2 * 1
                Vrk_4 = [0.0] * splat_count * 2 * 1
                Vrk_5 = [0.0] * splat_count * 2 * 1
                Vrk_6 = [0.0] * splat_count * 2 * 1
                center_data = [0.0] * splat_count * 2 * 3
                color = [0.0] * splat_count * 2 * 4
                # Process each splat
                SH_0 = 0.28209479177387814
                for i in range(splat_count):
                    RS = RS_matrix(quats[i], scales[i])
                    # Covariance Matrix
                    vrk_1 = RS[0] * RS[0] + RS[3] * RS[3] + RS[6] * RS[6]
                    vrk_2 = RS[0] * RS[1] + RS[3] * RS[4] + RS[6] * RS[7]
                    vrk_3 = RS[0] * RS[2] + RS[3] * RS[5] + RS[6] * RS[8]
                    vrk_4 = RS[1] * RS[1] + RS[4] * RS[4] + RS[7] * RS[7]
                    vrk_5 = RS[1] * RS[2] + RS[4] * RS[5] + RS[7] * RS[8]
                    vrk_6 = RS[2] * RS[2] + RS[5] * RS[5] + RS[8] * RS[8]
                    Vrk_1[2 * i + 0] = vrk_1
                    Vrk_1[2 * i + 1] = vrk_1
                    Vrk_2[2 * i + 0] = vrk_2
                    Vrk_2[2 * i + 1] = vrk_2
                    Vrk_3[2 * i + 0] = vrk_3
                    Vrk_3[2 * i + 1] = vrk_3
                    Vrk_4[2 * i + 0] = vrk_4
                    Vrk_4[2 * i + 1] = vrk_4
                    Vrk_5[2 * i + 0] = vrk_5
                    Vrk_5[2 * i + 1] = vrk_5
                    Vrk_6[2 * i + 0] = vrk_6
                    Vrk_6[2 * i + 1] = vrk_6
                    # To this:
                    center_data[6 * i + 0] = center[i][0]
                    center_data[6 * i + 1] = center[i][1] 
                    center_data[6 * i + 2] = center[i][2]
                    center_data[6 * i + 3] = center[i][0]
                    center_data[6 * i + 4] = center[i][1]
                    center_data[6 * i + 5] = center[i][2]
                    # Colors
                    R = (features_dc[i][0][0] * SH_0  + 0.5) 
                    G = (features_dc[i][1][0] * SH_0  + 0.5) 
                    B = (features_dc[i][2][0] * SH_0  + 0.5)
                    A = opacities[i]
                    color[8 * i + 0] = R
                    color[8 * i + 1] = G
                    color[8 * i + 2] = B
                    color[8 * i + 3] = A
                    color[8 * i + 4] = R
                    color[8 * i + 5] = G
                    color[8 * i + 6] = B
                    color[8 * i + 7] = A
                # Create mesh attributes
                center_attr : bpy.types.FloatVectorAttribute = mesh.attributes.new(name="center", type='FLOAT_VECTOR', domain='FACE')
                center_attr.data.foreach_set("vector", center_data)  # Using center_data array instead of center_attr
                color_attr : bpy.types.ByteColorAttribute = mesh.attributes.new(name="color", type='FLOAT_COLOR', domain='FACE')
                color_attr.data.foreach_set("color", color)
                # Create Vrk attributes
                for idx, data in enumerate([Vrk_1, Vrk_2, Vrk_3, Vrk_4, Vrk_5, Vrk_6]):
                    Vrk_attr = mesh.attributes.new(name=f"Vrk_{idx+1}", type='FLOAT', domain='FACE')
                    Vrk_attr.data.foreach_set("value", data)
                # Set up node group and material
                node_group = bpy.data.node_groups['KIRI_3DGS_Render_GN']
                node_modifier : bpy.types.NodesModifier = obj.modifiers.new(name="KIRI_3DGS_Render_GN", type='NODES')
                node_modifier.node_group = node_group
                # Find and assign material
                material = None
                for mat in bpy.data.materials:
                    if mat.name == "KIRI_3DGS_Render_Material":
                        material = mat
                        break
                if obj and obj.data:
                    if len(obj.material_slots) < 1:
                        obj.data.materials.append(material)
                    else:
                        obj.material_slots[0].material = material
                # Add object properties
                obj['update_rot_to_cam'] = True
                obj["GS_ID"] = get_next_available_gs_id()
                # Link object to scene
                bpy.context.collection.objects.link(obj)
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                print(f"Created Gaussian Splat object {obj.name}")
        if (bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences.sna_default_face_alignment_edit_mode == 'To X Axis'):
            sna_align_active_values_to_x_function_execute_03E8D()
        else:
            if bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences.sna_auto_rotate_for_blender_axes_z_up:
                if (bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences.sna_default_face_alignment_edit_mode == 'To Y Axis'):
                    sna_align_active_values_to_z_function_execute_62C4D()
                else:
                    sna_align_active_values_to_y_function_execute_89335()
            else:
                if (bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences.sna_default_face_alignment_edit_mode == 'To Y Axis'):
                    sna_align_active_values_to_y_function_execute_89335()
                else:
                    sna_align_active_values_to_z_function_execute_62C4D()
        geonodemodreturn_0_bf551 = sna_add_geo_nodes__append_group_2D522_BF551(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Store_Origpos_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Store_Origpos_GN')
        bpy.ops.object.modifier_move_to_index('INVOKE_DEFAULT', modifier='KIRI_3DGS_Store_Origpos_GN', index=0)
        bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Store_Origpos_GN')
        bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Render_GN')
        geonodemodreturn_0_91587 = sna_add_geo_nodes__append_group_2D522_91587(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Remove_Stray_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Remove_Stray_GN')
        geonodemodreturn_0_8e257 = sna_add_geo_nodes__append_group_2D522_8E257(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Camera_Cull_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Camera_Cull_GN')
        geonodemodreturn_0_dde79 = sna_add_geo_nodes__append_group_2D522_DDE79(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Crop_Box_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Crop_Box_GN')
        geonodemodreturn_0_eb4fd = sna_add_geo_nodes__append_group_2D522_EB4FD(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Colour_Edit_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Colour_Edit_GN')
        geonodemodreturn_0_592e9 = sna_add_geo_nodes__append_group_2D522_592E9(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Decimate_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Decimate_GN')
        geonodemodreturn_0_b6203 = sna_add_geo_nodes__append_group_2D522_B6203(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Render_GN')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_55'] = True
        geonodemodreturn_0_5fbae = sna_add_geo_nodes__append_group_2D522_5FBAE(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Animate_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Animate_GN')
        geonodemodreturn_0_74b9d = sna_add_geo_nodes__append_group_2D522_74B9D(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend'), 'KIRI_3DGS_Set_Material_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Set_Material_GN')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'].show_render = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'].show_render = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'].show_render = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'].show_render = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'].show_render = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_render = False
        bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode = 'Disable Camera Updates'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_on_cage = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_in_editmode = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Set_Material_GN']['Socket_2'] = bpy.data.materials['KIRI_3DGS_Render_Material']
        bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera = False
        bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode = 'Disable Camera Updates'
        bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_animate = False
        bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_camera_cull = False
        bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_colour_edit = False
        bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_crop_box = False
        bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_decimate = False
        bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_stray = False
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        if bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences.sna_auto_rotate_for_blender_axes_z_up:
            bpy.context.view_layer.objects.active.rotation_euler = (math.radians(-90.0), 0.0, math.radians(180.0))
        return {"FINISHED"}


def sna_align_active_values_to_x_function_execute_03E8D():
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_2'] = -4.3711398944878965e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_3'] = -4.3711398944878965e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_4'] = -1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_5'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_6'] = -1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_7'] = 1.910689912087678e-15
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_8'] = 4.3711398944878965e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_9'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_10'] = 2.117579969998599e-22
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_11'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_12'] = -4.3711398944878965e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_13'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_14'] = -3.553000027523012e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_15'] = -3.571039915084839
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_16'] = -8.938460350036621
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_17'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_34'] = 958.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_35'] = 962.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_18'] = 3.095370054244995
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_19'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_20'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_21'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_22'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_23'] = 3.0824999809265137
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_24'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_25'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_26'] = 0.19324299693107605
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_27'] = 0.21085800230503082
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_28'] = -1.0002000331878662
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_30'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_31'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_29'] = -1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_32'] = -0.20002000033855438
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_33'] = 0.0
    bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


def sna_import_ply_as_splats_function_interface_94FB1(layout_function, ):
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
    box_5C3FC = col_E3544.box()
    box_5C3FC.alert = False
    box_5C3FC.enabled = True
    box_5C3FC.active = True
    box_5C3FC.use_property_split = False
    box_5C3FC.use_property_decorate = False
    box_5C3FC.alignment = 'Expand'.upper()
    box_5C3FC.scale_x = 1.0
    box_5C3FC.scale_y = 1.0
    if not True: box_5C3FC.operator_context = "EXEC_DEFAULT"
    op = box_5C3FC.operator('sna.import_ply_as_splats_8458e', text='Import PLY As Splats', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'import-7102651-white.png')), emboss=True, depress=False)


def sna_align_active_values_to_y_function_execute_89335():
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_2'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_3'] = -7.642740166592926e-15
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_4'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_5'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_6'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_7'] = -4.3711398944878965e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_8'] = -1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_9'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_10'] = 8.470330482284962e-22
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_11'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_12'] = -4.3711398944878965e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_13'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_14'] = -0.2445569932460785
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_15'] = -3.571039915084839
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_16'] = -9.365139961242676
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_17'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_34'] = 411.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_35'] = 853.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_18'] = 1.4878499507904053
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_19'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_20'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_21'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_22'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_23'] = 0.7168909907341003
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_24'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_25'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_26'] = -0.050099000334739685
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_27'] = 0.01845400035381317
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_28'] = -1.0002000331878662
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_30'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_31'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_29'] = -1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_32'] = -0.20002000033855438
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_33'] = 0.0
    bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


def sna_align_active_values_to_z_function_execute_62C4D():
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_2'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_3'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_4'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_5'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_6'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_7'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_8'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_9'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_10'] = 8.470330482284962e-22
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_11'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_12'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_13'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_14'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_15'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_16'] = -15.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_17'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_34'] = 1920.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_35'] = 971.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_18'] = 1.0323200225830078
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_19'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_20'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_21'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_22'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_23'] = 2.041260004043579
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_24'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_25'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_26'] = 0.06471700221300125
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_27'] = 0.07061599940061569
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_28'] = -1.0002000331878662
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_30'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_31'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_29'] = -1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_32'] = -0.20002000033855438
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_33'] = 0.0
    bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


class SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_F216E(bpy.types.Panel):
    bl_label = '3DGS Render by KIRI Engine'
    bl_idname = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_F216E'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = '3DGS Render'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine icon.png')), scale=0.0)

    def draw(self, context):
        layout = self.layout


# Add plyfile to the path
addon_dir = os.path.dirname(__file__)
assets_dir = os.path.join(addon_dir, 'assets')  # Create path to assets directory
if assets_dir not in sys.path:
    sys.path.append(assets_dir)  # Add assets directory to path instead


try:
    import plyfile


except ImportError as e:
    print(f"Error importing plyfile: {e}")


class SNA_OT_Set_Render_Engine_To_Eevee_D73Ee(bpy.types.Operator):
    bl_idname = "sna.set_render_engine_to_eevee_d73ee"
    bl_label = "Set render engine to Eevee"
    bl_description = "Sets the render engine to Eevee for the current scene"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_enable_eevee_function_interface_891B1(layout_function, ):
    box_CF76C = layout_function.box()
    box_CF76C.alert = False
    box_CF76C.enabled = True
    box_CF76C.active = True
    box_CF76C.use_property_split = False
    box_CF76C.use_property_decorate = False
    box_CF76C.alignment = 'Expand'.upper()
    box_CF76C.scale_x = 1.0
    box_CF76C.scale_y = 1.0
    if not True: box_CF76C.operator_context = "EXEC_DEFAULT"
    col_DE06A = box_CF76C.column(heading='', align=False)
    col_DE06A.alert = False
    col_DE06A.enabled = True
    col_DE06A.active = True
    col_DE06A.use_property_split = False
    col_DE06A.use_property_decorate = False
    col_DE06A.scale_x = 1.0
    col_DE06A.scale_y = 1.0
    col_DE06A.alignment = 'Expand'.upper()
    col_DE06A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_DC146 = col_DE06A.box()
    box_DC146.alert = True
    box_DC146.enabled = True
    box_DC146.active = True
    box_DC146.use_property_split = False
    box_DC146.use_property_decorate = False
    box_DC146.alignment = 'Expand'.upper()
    box_DC146.scale_x = 1.0
    box_DC146.scale_y = 1.0
    if not True: box_DC146.operator_context = "EXEC_DEFAULT"
    box_DC146.label(text='Eevee render engine required', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
    op = col_DE06A.operator('sna.set_render_engine_to_eevee_d73ee', text='Enable Eevee', icon_value=0, emboss=True, depress=False)


def sna_modify_animate_function_interface_57F9E(layout_function, ):
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
    op = box_DFEF6.operator('sna.append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'sphere-6796353-white.png')), emboss=True, depress=False)
    op = box_DFEF6.operator('sna.append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cube-4212258-white.png')), emboss=True, depress=False)
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
        row_004B5 = box_1DAB6.row(heading='', align=False)
        row_004B5.alert = False
        row_004B5.enabled = True
        row_004B5.active = True
        row_004B5.use_property_split = False
        row_004B5.use_property_decorate = False
        row_004B5.scale_x = 1.0
        row_004B5.scale_y = 1.0
        row_004B5.alignment = 'Expand'.upper()
        row_004B5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_004B5.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_modifier_enable_animate', text=('Animate' if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_animate else 'Enable Animate'), icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_animate:
            op = row_004B5.operator('sna.apply_animate_modifier_3938e', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
            op = row_004B5.operator('sna.remove_animate_modifier_5b34d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_animate:
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
                    col_44B28.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_5"]', bpy.context.scene.collection, 'children', text='', icon='OUTLINER_COLLECTION')
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


class SNA_OT_Remove_Animate_Modifier_5B34D(bpy.types.Operator):
    bl_idname = "sna.remove_animate_modifier_5b34d"
    bl_label = "Remove Animate Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Apply_Animate_Modifier_3938E(bpy.types.Operator):
    bl_idname = "sna.apply_animate_modifier_3938e"
    bl_label = "Apply Animate Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_35'] = True
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Animate_GN'
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_modify_edit_function_interface_AEA26(layout_function, ):
    box_B07E1 = layout_function.box()
    box_B07E1.alert = False
    box_B07E1.enabled = True
    box_B07E1.active = True
    box_B07E1.use_property_split = False
    box_B07E1.use_property_decorate = False
    box_B07E1.alignment = 'Expand'.upper()
    box_B07E1.scale_x = 1.0
    box_B07E1.scale_y = 1.0
    if not True: box_B07E1.operator_context = "EXEC_DEFAULT"
    op = box_B07E1.operator('sna.append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'sphere-6796353-white.png')), emboss=True, depress=False)
    op = box_B07E1.operator('sna.append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cube-4212258-white.png')), emboss=True, depress=False)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Camera_Cull_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_3C6E7 = layout_function.box()
        box_3C6E7.alert = False
        box_3C6E7.enabled = True
        box_3C6E7.active = True
        box_3C6E7.use_property_split = False
        box_3C6E7.use_property_decorate = False
        box_3C6E7.alignment = 'Expand'.upper()
        box_3C6E7.scale_x = 1.0
        box_3C6E7.scale_y = 1.0
        if not True: box_3C6E7.operator_context = "EXEC_DEFAULT"
        row_4E799 = box_3C6E7.row(heading='', align=False)
        row_4E799.alert = False
        row_4E799.enabled = True
        row_4E799.active = True
        row_4E799.use_property_split = False
        row_4E799.use_property_decorate = False
        row_4E799.scale_x = 1.0
        row_4E799.scale_y = 1.0
        row_4E799.alignment = 'Expand'.upper()
        row_4E799.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_4E799.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_modifier_enable_camera_cull', text=('Camera Cull' if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_camera_cull else 'Enable Camera Cull'), icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_camera_cull:
            op = row_4E799.operator('sna.apply_camera_cull_modifier_d55d0', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
            op = row_4E799.operator('sna.remove_camera_cull_modifier_884cc', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_camera_cull:
            if (bpy.context.scene.camera == None):
                box_FCEF8 = box_3C6E7.box()
                box_FCEF8.alert = True
                box_FCEF8.enabled = True
                box_FCEF8.active = True
                box_FCEF8.use_property_split = False
                box_FCEF8.use_property_decorate = False
                box_FCEF8.alignment = 'Expand'.upper()
                box_FCEF8.scale_x = 1.0
                box_FCEF8.scale_y = 1.0
                if not True: box_FCEF8.operator_context = "EXEC_DEFAULT"
                box_FCEF8.label(text='No active camera in scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
            else:
                col_DCB98 = box_3C6E7.column(heading='', align=False)
                col_DCB98.alert = False
                col_DCB98.enabled = True
                col_DCB98.active = True
                col_DCB98.use_property_split = False
                col_DCB98.use_property_decorate = False
                col_DCB98.scale_x = 1.0
                col_DCB98.scale_y = 1.0
                col_DCB98.alignment = 'Expand'.upper()
                col_DCB98.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                box_E944F = col_DCB98.box()
                box_E944F.alert = False
                box_E944F.enabled = True
                box_E944F.active = True
                box_E944F.use_property_split = False
                box_E944F.use_property_decorate = False
                box_E944F.alignment = 'Expand'.upper()
                box_E944F.scale_x = 1.0
                box_E944F.scale_y = 1.0
                if not True: box_E944F.operator_context = "EXEC_DEFAULT"
                op = box_E944F.operator('sna.auto_set_up_camera_cull_properties_78ea9', text='Auto Set Up', icon_value=0, emboss=True, depress=False)
                attr_CC025 = '["' + str('Socket_2' + '"]') 
                col_DCB98.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_CC025, text='X Resolution', icon_value=0, emboss=True)
                attr_17ECD = '["' + str('Socket_3' + '"]') 
                col_DCB98.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_17ECD, text='Y Resolution', icon_value=0, emboss=True)
                attr_73B2F = '["' + str('Socket_4' + '"]') 
                col_DCB98.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_73B2F, text='Focal Length', icon_value=0, emboss=True)
                attr_15665 = '["' + str('Socket_5' + '"]') 
                col_DCB98.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_15665, text='Sensor Width', icon_value=0, emboss=True)
                attr_89F4F = '["' + str('Socket_6' + '"]') 
                col_DCB98.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_89F4F, text='Padding', icon_value=0, emboss=True)
                attr_55D17 = '["' + str('Socket_13' + '"]') 
                col_DCB98.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_55D17, text='Closer Than', icon_value=0, emboss=True)
                attr_FF78A = '["' + str('Socket_14' + '"]') 
                col_DCB98.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], attr_FF78A, text='Further Than', icon_value=0, emboss=True)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Decimate_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_A8194 = layout_function.box()
        box_A8194.alert = False
        box_A8194.enabled = True
        box_A8194.active = True
        box_A8194.use_property_split = False
        box_A8194.use_property_decorate = False
        box_A8194.alignment = 'Expand'.upper()
        box_A8194.scale_x = 1.0
        box_A8194.scale_y = 1.0
        if not True: box_A8194.operator_context = "EXEC_DEFAULT"
        row_16CFC = box_A8194.row(heading='', align=False)
        row_16CFC.alert = False
        row_16CFC.enabled = True
        row_16CFC.active = True
        row_16CFC.use_property_split = False
        row_16CFC.use_property_decorate = False
        row_16CFC.scale_x = 1.0
        row_16CFC.scale_y = 1.0
        row_16CFC.alignment = 'Expand'.upper()
        row_16CFC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_16CFC.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_modifier_enable_decimate', text=('Decimate' if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_decimate else 'Enable Decimate'), icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_decimate:
            op = row_16CFC.operator('sna.apply_decimate_modifier_8c14b', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
            op = row_16CFC.operator('sna.remove_decimate_modifier_63381', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_decimate:
            col_F472C = box_A8194.column(heading='', align=False)
            col_F472C.alert = False
            col_F472C.enabled = True
            col_F472C.active = True
            col_F472C.use_property_split = False
            col_F472C.use_property_decorate = False
            col_F472C.scale_x = 1.0
            col_F472C.scale_y = 1.0
            col_F472C.alignment = 'Expand'.upper()
            col_F472C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_0F7C7 = '["' + str('Socket_15' + '"]') 
            col_F472C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_0F7C7, text='Decimate Percentage', icon_value=0, emboss=True)
            attr_39B47 = '["' + str('Socket_16' + '"]') 
            col_F472C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_39B47, text='Decimate Seed', icon_value=0, emboss=True)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Crop_Box_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_C914B = layout_function.box()
        box_C914B.alert = False
        box_C914B.enabled = True
        box_C914B.active = True
        box_C914B.use_property_split = False
        box_C914B.use_property_decorate = False
        box_C914B.alignment = 'Expand'.upper()
        box_C914B.scale_x = 1.0
        box_C914B.scale_y = 1.0
        if not True: box_C914B.operator_context = "EXEC_DEFAULT"
        row_5B9C3 = box_C914B.row(heading='', align=False)
        row_5B9C3.alert = False
        row_5B9C3.enabled = True
        row_5B9C3.active = True
        row_5B9C3.use_property_split = False
        row_5B9C3.use_property_decorate = False
        row_5B9C3.scale_x = 1.0
        row_5B9C3.scale_y = 1.0
        row_5B9C3.alignment = 'Expand'.upper()
        row_5B9C3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_5B9C3.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_modifier_enable_crop_box', text=('Crop Box' if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_crop_box else 'Enable Crop Box'), icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_crop_box:
            op = row_5B9C3.operator('sna.apply_crop_box_modifier_36522', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
            op = row_5B9C3.operator('sna.remove_crop_box_modifier_90df7', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_crop_box:
            col_E8EFC = box_C914B.column(heading='', align=False)
            col_E8EFC.alert = False
            col_E8EFC.enabled = True
            col_E8EFC.active = True
            col_E8EFC.use_property_split = False
            col_E8EFC.use_property_decorate = False
            col_E8EFC.scale_x = 1.0
            col_E8EFC.scale_y = 1.0
            col_E8EFC.alignment = 'Expand'.upper()
            col_E8EFC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_E3439 = '["' + str('Socket_19' + '"]') 
            col_E8EFC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_E3439, text='', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN']['Socket_19'] == 0):
                attr_6FC7C = '["' + str('Socket_12' + '"]') 
                col_E8EFC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_6FC7C, text='', icon_value=0, emboss=True)
            else:
                col_E8EFC.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], '["Socket_18"]', bpy.data, 'collections', text='collection', icon='NONE')
            attr_83D09 = '["' + str('Socket_15' + '"]') 
            col_E8EFC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_83D09, text='', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN']['Socket_15'] >= 2):
                attr_AA28A = '["' + str('Socket_16' + '"]') 
                col_E8EFC.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], attr_AA28A, text='', icon_value=0, emboss=True)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Colour_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_1CE63 = layout_function.box()
        box_1CE63.alert = False
        box_1CE63.enabled = True
        box_1CE63.active = True
        box_1CE63.use_property_split = False
        box_1CE63.use_property_decorate = False
        box_1CE63.alignment = 'Expand'.upper()
        box_1CE63.scale_x = 1.0
        box_1CE63.scale_y = 1.0
        if not True: box_1CE63.operator_context = "EXEC_DEFAULT"
        row_C26BC = box_1CE63.row(heading='', align=False)
        row_C26BC.alert = False
        row_C26BC.enabled = True
        row_C26BC.active = True
        row_C26BC.use_property_split = False
        row_C26BC.use_property_decorate = False
        row_C26BC.scale_x = 1.0
        row_C26BC.scale_y = 1.0
        row_C26BC.alignment = 'Expand'.upper()
        row_C26BC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_C26BC.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_modifier_enable_colour_edit', text=('Colour Edit' if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_colour_edit else 'Enable Colour Edit'), icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_colour_edit:
            op = row_C26BC.operator('sna.apply_colour_edit_modifier_88410', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
            op = row_C26BC.operator('sna.remove_colour_edit_modifier_cddb3', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_colour_edit:
            col_5964C = box_1CE63.column(heading='', align=False)
            col_5964C.alert = False
            col_5964C.enabled = True
            col_5964C.active = True
            col_5964C.use_property_split = False
            col_5964C.use_property_decorate = False
            col_5964C.scale_x = 1.0
            col_5964C.scale_y = 1.0
            col_5964C.alignment = 'Expand'.upper()
            col_5964C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_BD8B2 = '["' + str('Socket_4' + '"]') 
            col_5964C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_BD8B2, text='', icon_value=0, emboss=True)
            attr_A7044 = '["' + str('Socket_2' + '"]') 
            col_5964C.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_A7044, text='', icon_value=0, emboss=True)
            if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_4'] == 0) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_4'] == 1)):
                col_0A0A3 = col_5964C.column(heading='', align=False)
                col_0A0A3.alert = False
                col_0A0A3.enabled = True
                col_0A0A3.active = True
                col_0A0A3.use_property_split = False
                col_0A0A3.use_property_decorate = False
                col_0A0A3.scale_x = 1.0
                col_0A0A3.scale_y = 1.0
                col_0A0A3.alignment = 'Expand'.upper()
                col_0A0A3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                attr_8D62F = '["' + str('Socket_3' + '"]') 
                col_0A0A3.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_8D62F, text='Hue Threshold', icon_value=0, emboss=True)
                attr_BB945 = '["' + str('Socket_6' + '"]') 
                col_0A0A3.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_BB945, text='Saturation Threshold', icon_value=0, emboss=True)
                attr_8D869 = '["' + str('Socket_7' + '"]') 
                col_0A0A3.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_8D869, text='Value Threshold', icon_value=0, emboss=True)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Remove_Stray_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_2E82D = layout_function.box()
        box_2E82D.alert = False
        box_2E82D.enabled = True
        box_2E82D.active = True
        box_2E82D.use_property_split = False
        box_2E82D.use_property_decorate = False
        box_2E82D.alignment = 'Expand'.upper()
        box_2E82D.scale_x = 1.0
        box_2E82D.scale_y = 1.0
        if not True: box_2E82D.operator_context = "EXEC_DEFAULT"
        row_520DB = box_2E82D.row(heading='', align=False)
        row_520DB.alert = False
        row_520DB.enabled = True
        row_520DB.active = True
        row_520DB.use_property_split = False
        row_520DB.use_property_decorate = False
        row_520DB.scale_x = 1.0
        row_520DB.scale_y = 1.0
        row_520DB.alignment = 'Expand'.upper()
        row_520DB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_520DB.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_modifier_enable_remove_stray', text=('Remove Stray' if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_stray else 'Enable Remove Stray'), icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_stray:
            op = row_520DB.operator('sna.apply_remove_stray_modifier_3fdf1', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
            op = row_520DB.operator('sna.remove_remove_stray_modifier_95a21', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_stray:
            col_F2224 = box_2E82D.column(heading='', align=False)
            col_F2224.alert = False
            col_F2224.enabled = True
            col_F2224.active = True
            col_F2224.use_property_split = False
            col_F2224.use_property_decorate = False
            col_F2224.scale_x = 1.0
            col_F2224.scale_y = 1.0
            col_F2224.alignment = 'Expand'.upper()
            col_F2224.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_5CF96 = '["' + str('Socket_6' + '"]') 
            col_F2224.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'], attr_5CF96, text='Remove Small Faces', icon_value=0, emboss=True, toggle=True)
            if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN']['Socket_6']:
                attr_5EC3E = '["' + str('Socket_5' + '"]') 
                col_F2224.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'], attr_5EC3E, text='Small Face Threshold', icon_value=0, emboss=True)
            attr_0BF6C = '["' + str('Socket_11' + '"]') 
            col_F2224.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'], attr_0BF6C, text='Remove Stretched Faces', icon_value=0, emboss=True, toggle=True)
            if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN']['Socket_11']:
                attr_C6B2C = '["' + str('Socket_12' + '"]') 
                col_F2224.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'], attr_C6B2C, text='Edge LengthThreshold', icon_value=0, emboss=True)


class SNA_OT_Remove_Decimate_Modifier_63381(bpy.types.Operator):
    bl_idname = "sna.remove_decimate_modifier_63381"
    bl_label = "Remove Decimate Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Remove_Camera_Cull_Modifier_884Cc(bpy.types.Operator):
    bl_idname = "sna.remove_camera_cull_modifier_884cc"
    bl_label = "Remove Camera Cull Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Remove_Crop_Box_Modifier_90Df7(bpy.types.Operator):
    bl_idname = "sna.remove_crop_box_modifier_90df7"
    bl_label = "Remove Crop Box Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Remove_Colour_Edit_Modifier_Cddb3(bpy.types.Operator):
    bl_idname = "sna.remove_colour_edit_modifier_cddb3"
    bl_label = "Remove Colour Edit Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Remove_Remove_Stray_Modifier_95A21(bpy.types.Operator):
    bl_idname = "sna.remove_remove_stray_modifier_95a21"
    bl_label = "Remove Remove Stray Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_Stray_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Auto_Set_Up_Camera_Cull_Properties_78Ea9(bpy.types.Operator):
    bl_idname = "sna.auto_set_up_camera_cull_properties_78ea9"
    bl_label = "Auto Set Up Camera Cull Properties"
    bl_description = "Sets the Camera Cull properties to the current scene/camera settings"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN']['Socket_2'] = bpy.context.scene.render.resolution_x
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN']['Socket_3'] = bpy.context.scene.render.resolution_y
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN']['Socket_4'] = bpy.context.scene.camera.data.lens
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN']['Socket_5'] = bpy.context.scene.camera.data.sensor_width
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Append_Wire_Sphere_2Bf63(bpy.types.Operator):
    bl_idname = "sna.append_wire_sphere_2bf63"
    bl_label = "Append Wire Sphere"
    bl_description = "Appends an object for use as a modifier effector. The object will not render."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        before_data = list(bpy.data.objects)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\Object', filename='Wire Sphere', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_69F39 = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Append_Wire_Cube_56E0F(bpy.types.Operator):
    bl_idname = "sna.append_wire_cube_56e0f"
    bl_label = "Append Wire Cube"
    bl_description = "Appends an object for use as a modifier effector. The object will not render."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        before_data = list(bpy.data.objects)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\Object', filename='Wire Cube', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_8B494 = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Apply_Decimate_Modifier_8C14B(bpy.types.Operator):
    bl_idname = "sna.apply_decimate_modifier_8c14b"
    bl_label = "Apply Decimate Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Decimate_GN'
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Apply_Camera_Cull_Modifier_D55D0(bpy.types.Operator):
    bl_idname = "sna.apply_camera_cull_modifier_d55d0"
    bl_label = "Apply Camera Cull Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Camera_Cull_GN'
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Apply_Crop_Box_Modifier_36522(bpy.types.Operator):
    bl_idname = "sna.apply_crop_box_modifier_36522"
    bl_label = "Apply Crop Box Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Crop_Box_GN'
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Apply_Colour_Edit_Modifier_88410(bpy.types.Operator):
    bl_idname = "sna.apply_colour_edit_modifier_88410"
    bl_label = "Apply Colour Edit Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Colour_Edit_GN'
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Apply_Remove_Stray_Modifier_3Fdf1(bpy.types.Operator):
    bl_idname = "sna.apply_remove_stray_modifier_3fdf1"
    bl_label = "Apply Remove Stray Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Remove_Stray_GN'
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_omnisplat_function_interface_E1B70(layout_function, ):
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Enable Camera Updates'):
            if bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera:
                col_4EC42 = layout_function.column(heading='', align=False)
                col_4EC42.alert = True
                col_4EC42.enabled = True
                col_4EC42.active = True
                col_4EC42.use_property_split = False
                col_4EC42.use_property_decorate = False
                col_4EC42.scale_x = 1.0
                col_4EC42.scale_y = 1.0
                col_4EC42.alignment = 'Expand'.upper()
                col_4EC42.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_4EC42.label(text="Disable 'Active Camera' for the active object", icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
            else:
                col_D7973 = layout_function.column(heading='', align=False)
                col_D7973.alert = False
                col_D7973.enabled = True
                col_D7973.active = True
                col_D7973.use_property_split = False
                col_D7973.use_property_decorate = False
                col_D7973.scale_x = 1.0
                col_D7973.scale_y = 1.0
                col_D7973.alignment = 'Expand'.upper()
                col_D7973.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_D7973.prop(bpy.context.scene, 'sna_kiri3dgs_omnisplat_axes_count', text='', icon_value=0, emboss=True)
                op = col_D7973.operator('sna.create_omniview_object_909fd', text='Create Omniview Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'axis-6796394 (2).png')), emboss=True, depress=False)
        else:
            col_496DA = layout_function.column(heading='', align=False)
            col_496DA.alert = True
            col_496DA.enabled = True
            col_496DA.active = True
            col_496DA.use_property_split = False
            col_496DA.use_property_decorate = False
            col_496DA.scale_x = 1.0
            col_496DA.scale_y = 1.0
            col_496DA.alignment = 'Expand'.upper()
            col_496DA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_496DA.label(text='Camera Updates Disabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
    else:
        col_73743 = layout_function.column(heading='', align=False)
        col_73743.alert = True
        col_73743.enabled = True
        col_73743.active = True
        col_73743.use_property_split = False
        col_73743.use_property_decorate = False
        col_73743.scale_x = 1.0
        col_73743.scale_y = 1.0
        col_73743.alignment = 'Expand'.upper()
        col_73743.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_73743.label(text='3DGS Render Modifier Missing', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))


class SNA_OT_Create_Omniview_Object_909Fd(bpy.types.Operator):
    bl_idname = "sna.create_omniview_object_909fd"
    bl_label = "Create Omniview Object"
    bl_description = "Generates a new version of the active object that can be viewed from several angles (depending on the preset chosen)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (len(bpy.context.view_layer.objects.selected) > 1):
            self.report({'ERROR'}, message='Only select 1 object')
        else:
            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'] = []
                kiri_3dgs_render__omnisplat['sna_omniviewbase'] = None
                kiri_3dgs_render__omnisplat['sna_omniviewmodifierlist'] = []
                # Get all areas in the current screen
                areas = bpy.context.screen.areas
                # Loop through all areas
                for area in areas:
                    # Check if the area is a 3D View
                    if area.type == 'VIEW_3D':
                        # Get the space data
                        space = area.spaces.active
                        # Set shading type to 'SOLID'
                        space.shading.type = 'SOLID'
                        # Set lighting and color settings
                        space.shading.light = 'STUDIO'  # Options: 'STUDIO', 'FLAT', 'MATCAP'
                        space.shading.color_type = 'MATERIAL'  # Options: 'MATERIAL', 'SINGLE', 'OBJECT', 'RANDOM'
                source_obj_name = bpy.context.view_layer.objects.active.name
                offset_x = 2.0
                new_object_name = None
                # Input variables
                #source_obj_name = "Cube"  # Change this to your object's name
                #offset_x = 0.0  # Input float variable for X offset
                # Get the source object
                source_obj = bpy.data.objects.get(source_obj_name)
                # Check if the object exists
                if source_obj:
                    # Create a copy of the object
                    new_obj = source_obj.copy()
                    new_obj.data = source_obj.data.copy()
                    # Link the new object to the scene
                    bpy.context.scene.collection.objects.link(new_obj)
                    # Apply the offset if any
                    new_obj.location.x += offset_x
                    # Store the new object's name in a variable
                    new_object_name = new_obj.name
                else:
                    new_object_name = "ERROR: Source object not found"
                # Output the new object's name (this will be captured by Serpens)
                print(new_object_name)
                bpy.context.view_layer.objects.active = bpy.data.objects[new_object_name]
                bpy.context.view_layer.objects.active.name = bpy.context.view_layer.objects.active.name + '_omni' + '_' + bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count
                kiri_3dgs_render__omnisplat['sna_omniviewbase'] = bpy.context.view_layer.objects.active
                for i_A8F53 in range(len(bpy.data.objects)):
                    bpy.data.objects[i_A8F53].select_set(state=False, view_layer=bpy.context.view_layer, )
                kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                bpy.context.view_layer.objects.active = kiri_3dgs_render__omnisplat['sna_omniviewbase']
                kiri_3dgs_render__omnisplat['sna_omniviewbase'].modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 0
                for i_35F95 in range(len(kiri_3dgs_render__omnisplat['sna_omniviewbase'].modifiers)):
                    kiri_3dgs_render__omnisplat['sna_omniviewmodifierlist'].append(kiri_3dgs_render__omnisplat['sna_omniviewbase'].modifiers[i_35F95])
                for i_C4833 in range(len(kiri_3dgs_render__omnisplat['sna_omniviewmodifierlist'])):
                    if (kiri_3dgs_render__omnisplat['sna_omniviewmodifierlist'][i_C4833].name == 'KIRI_3DGS_Animate_GN'):
                        kiri_3dgs_render__omnisplat['sna_omniviewmodifierlist'][i_C4833]['Socket_35'] = True
                    if (kiri_3dgs_render__omnisplat['sna_omniviewmodifierlist'][i_C4833].name == 'KIRI_3DGS_Render_GN'):
                        pass
                    else:
                        kiri_3dgs_render__omnisplat['sna_omniviewbase'].modifiers.remove(modifier=kiri_3dgs_render__omnisplat['sna_omniviewmodifierlist'][i_C4833], )

                def delayed_A59B5():
                    import math

                    def get_selected_bounds():
                        # Get selected objects
                        selected = bpy.context.selected_objects
                        if not selected:
                            return None
                        # Calculate bounds of all selected objects
                        min_co = Vector((float('inf'),) * 3)
                        max_co = Vector((float('-inf'),) * 3)
                        for obj in selected:
                            matrix = obj.matrix_world
                            if obj.type == 'MESH':
                                for v in obj.data.vertices:
                                    world_co = matrix @ v.co
                                    min_co.x = min(world_co.x, min_co.x)
                                    min_co.y = min(world_co.y, min_co.y)
                                    min_co.z = min(world_co.z, min_co.z)
                                    max_co.x = max(world_co.x, max_co.x)
                                    max_co.y = max(world_co.y, max_co.y)
                                    max_co.z = max(world_co.z, max_co.z)
                            else:
                                # For non-mesh objects, use object location
                                world_co = matrix.translation
                                min_co.x = min(world_co.x, min_co.x)
                                min_co.y = min(world_co.y, min_co.y)
                                min_co.z = min(world_co.z, min_co.z)
                                max_co.x = max(world_co.x, max_co.x)
                                max_co.y = max(world_co.y, max_co.y)
                                max_co.z = max(world_co.z, max_co.z)
                        return min_co, max_co
                    # Get the 3D view
                    for area in bpy.context.screen.areas:
                        if area.type == 'VIEW_3D':
                            view3d = area.spaces[0]
                            region3d = view3d.region_3d
                            # Get bounds of selected objects
                            bounds = get_selected_bounds()
                            if bounds:
                                min_co, max_co = bounds
                                # Calculate center and size
                                center = (max_co + min_co) / 2
                                size = (max_co - min_co).length
                                # Set the view center
                                region3d.view_location = center
                                # Calculate and set zoom to fit
                                if size > 0:
                                    # Calculate distance to fit objects in view
                                    fov = math.radians(45.0)  # typical camera FOV
                                    distance = size / (2 * math.tan(fov / 2))
                                    # Update view distance
                                    region3d.view_distance = distance * 1.5  # 1.5 for some padding
                            break
                    view_type = 'FRONT'
                    view_mode = 'PERSP'
                    from mathutils import Quaternion
                    # Serpens variables
                    #view_type = 'FRONT'
                    #view_mode = 'ORTHO'
                    # Dictionary of view rotations
                    rotations = {
                        # Main views - verified working
                        'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                        'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                        'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                        'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                        'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                        'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                        # Corrected TOPFRONT view (45 degrees up from front)
                        'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                        # 45-degree views from back
                        'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                        'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                        # Other 45-degree views
                        'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                        'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                        'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                        # 45-degree views from RIGHT
                        'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                        'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                    }
                    # Check if view type exists
                    if view_type not in rotations:
                        print(f"Invalid view type: {view_type}")
                    else:
                        # Find and set the 3D view
                        for area in bpy.context.screen.areas:
                            if area.type == 'VIEW_3D':
                                view3d = area.spaces[0]
                                region3d = view3d.region_3d
                                # Set view mode and apply rotation
                                region3d.view_perspective = view_mode
                                region3d.view_rotation = rotations[view_type]
                                break

                    def delayed_7EF56():
                        ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                        from mathutils import Matrix
                        # Define helper function for updating the geometry node sockets

                        def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                            geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                            if not geometryNodes_modifier:
                                print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                return False
                            # Update view matrix
                            geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                            geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                            geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                            geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                            geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                            geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                            geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                            geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                            geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                            geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                            geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                            geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                            geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                            geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                            geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                            geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                            # Update projection matrix
                            geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                            geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                            geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                            geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                            geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                            geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                            geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                            geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                            geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                            geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                            geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                            geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                            geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                            geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                            geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                            geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                            # Update window dimensions
                            geometryNodes_modifier['Socket_34'] = window_width
                            geometryNodes_modifier['Socket_35'] = window_height
                            return True
                        # Main code for updating specific object
                        updated_objects = []
                        # Find view and projection matrices from the 3D view area
                        found_3d_view = False
                        for area in bpy.context.screen.areas:
                            if area.type == 'VIEW_3D':
                                view_matrix = area.spaces.active.region_3d.view_matrix
                                proj_matrix = area.spaces.active.region_3d.window_matrix
                                window_width = area.width
                                window_height = area.height
                                found_3d_view = True
                                break
                        if not found_3d_view:
                            print("Error: No 3D View found to update camera information.")
                        else:
                            # Update only specific object
                            target_object_name = ObjectName  # Serpens Variable
                            obj = bpy.data.objects.get(target_object_name)
                            if obj and obj.visible_get():
                                print(f"Attempting to update object: {obj.name}")  # Debugging print
                                if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                    updated_objects.append(obj.name)  # Add to updated list
                        # Print or output the list of updated objects
                        print("Updated objects:", updated_objects)
                        kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                        if bpy.context and bpy.context.screen:
                            for a in bpy.context.screen.areas:
                                a.tag_redraw()
                        source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                        offset_x = 0.0
                        new_object_name = None
                        # Input variables
                        #source_obj_name = "Cube"  # Change this to your object's name
                        #offset_x = 0.0  # Input float variable for X offset
                        # Get the source object
                        source_obj = bpy.data.objects.get(source_obj_name)
                        # Check if the object exists
                        if source_obj:
                            # Create a copy of the object
                            new_obj = source_obj.copy()
                            new_obj.data = source_obj.data.copy()
                            # Link the new object to the scene
                            bpy.context.scene.collection.objects.link(new_obj)
                            # Apply the offset if any
                            new_obj.location.x += offset_x
                            # Store the new object's name in a variable
                            new_object_name = new_obj.name
                        else:
                            new_object_name = "ERROR: Source object not found"
                        # Output the new object's name (this will be captured by Serpens)
                        print(new_object_name)
                        kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                        for i_4B7A6 in range(len(bpy.context.view_layer.objects.selected)):
                            bpy.context.view_layer.objects.selected[i_4B7A6].select_set(state=False, view_layer=bpy.context.view_layer, )
                        kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                        view_type = 'RIGHT'
                        view_mode = 'PERSP'
                        from mathutils import Quaternion
                        # Serpens variables
                        #view_type = 'FRONT'
                        #view_mode = 'ORTHO'
                        # Dictionary of view rotations
                        rotations = {
                            # Main views - verified working
                            'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                            'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                            'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                            'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                            'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                            'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                            # Corrected TOPFRONT view (45 degrees up from front)
                            'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                            # 45-degree views from back
                            'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                            'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                            # Other 45-degree views
                            'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                            'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                            'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                            # 45-degree views from RIGHT
                            'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                            'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                        }
                        # Check if view type exists
                        if view_type not in rotations:
                            print(f"Invalid view type: {view_type}")
                        else:
                            # Find and set the 3D view
                            for area in bpy.context.screen.areas:
                                if area.type == 'VIEW_3D':
                                    view3d = area.spaces[0]
                                    region3d = view3d.region_3d
                                    # Set view mode and apply rotation
                                    region3d.view_perspective = view_mode
                                    region3d.view_rotation = rotations[view_type]
                                    break

                        def delayed_CF40F():
                            ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                            from mathutils import Matrix
                            # Define helper function for updating the geometry node sockets

                            def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                                if not geometryNodes_modifier:
                                    print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                    return False
                                # Update view matrix
                                geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                                geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                                geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                                geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                                geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                                geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                                geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                                geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                                geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                                geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                                geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                                geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                                geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                                geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                                geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                                geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                                # Update projection matrix
                                geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                                geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                                geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                                geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                                geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                                geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                                geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                                geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                                geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                                geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                                geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                                geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                                geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                                geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                                geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                                geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                                # Update window dimensions
                                geometryNodes_modifier['Socket_34'] = window_width
                                geometryNodes_modifier['Socket_35'] = window_height
                                return True
                            # Main code for updating specific object
                            updated_objects = []
                            # Find view and projection matrices from the 3D view area
                            found_3d_view = False
                            for area in bpy.context.screen.areas:
                                if area.type == 'VIEW_3D':
                                    view_matrix = area.spaces.active.region_3d.view_matrix
                                    proj_matrix = area.spaces.active.region_3d.window_matrix
                                    window_width = area.width
                                    window_height = area.height
                                    found_3d_view = True
                                    break
                            if not found_3d_view:
                                print("Error: No 3D View found to update camera information.")
                            else:
                                # Update only specific object
                                target_object_name = ObjectName  # Serpens Variable
                                obj = bpy.data.objects.get(target_object_name)
                                if obj and obj.visible_get():
                                    print(f"Attempting to update object: {obj.name}")  # Debugging print
                                    if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                        updated_objects.append(obj.name)  # Add to updated list
                            # Print or output the list of updated objects
                            print("Updated objects:", updated_objects)
                            kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                            if bpy.context and bpy.context.screen:
                                for a in bpy.context.screen.areas:
                                    a.tag_redraw()
                            source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                            offset_x = 0.0
                            new_object_name = None
                            # Input variables
                            #source_obj_name = "Cube"  # Change this to your object's name
                            #offset_x = 0.0  # Input float variable for X offset
                            # Get the source object
                            source_obj = bpy.data.objects.get(source_obj_name)
                            # Check if the object exists
                            if source_obj:
                                # Create a copy of the object
                                new_obj = source_obj.copy()
                                new_obj.data = source_obj.data.copy()
                                # Link the new object to the scene
                                bpy.context.scene.collection.objects.link(new_obj)
                                # Apply the offset if any
                                new_obj.location.x += offset_x
                                # Store the new object's name in a variable
                                new_object_name = new_obj.name
                            else:
                                new_object_name = "ERROR: Source object not found"
                            # Output the new object's name (this will be captured by Serpens)
                            print(new_object_name)
                            kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                            for i_DFF57 in range(len(bpy.context.view_layer.objects.selected)):
                                bpy.context.view_layer.objects.selected[i_DFF57].select_set(state=False, view_layer=bpy.context.view_layer, )
                            kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                            view_type = 'TOP'
                            view_mode = 'PERSP'
                            from mathutils import Quaternion
                            # Serpens variables
                            #view_type = 'FRONT'
                            #view_mode = 'ORTHO'
                            # Dictionary of view rotations
                            rotations = {
                                # Main views - verified working
                                'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                                'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                                'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                                'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                                'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                                'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                                # Corrected TOPFRONT view (45 degrees up from front)
                                'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                                # 45-degree views from back
                                'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                                'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                                # Other 45-degree views
                                'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                                'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                                'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                                # 45-degree views from RIGHT
                                'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                                'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                            }
                            # Check if view type exists
                            if view_type not in rotations:
                                print(f"Invalid view type: {view_type}")
                            else:
                                # Find and set the 3D view
                                for area in bpy.context.screen.areas:
                                    if area.type == 'VIEW_3D':
                                        view3d = area.spaces[0]
                                        region3d = view3d.region_3d
                                        # Set view mode and apply rotation
                                        region3d.view_perspective = view_mode
                                        region3d.view_rotation = rotations[view_type]
                                        break

                            def delayed_FE628():
                                ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                from mathutils import Matrix
                                # Define helper function for updating the geometry node sockets

                                def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                    geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                                    if not geometryNodes_modifier:
                                        print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                        return False
                                    # Update view matrix
                                    geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                                    geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                                    geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                                    geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                                    geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                                    geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                                    geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                                    geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                                    geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                                    geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                                    geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                                    geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                                    geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                                    geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                                    geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                                    geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                                    # Update projection matrix
                                    geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                                    geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                                    geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                                    geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                                    geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                                    geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                                    geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                                    geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                                    geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                                    geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                                    geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                                    geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                                    geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                                    geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                                    geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                                    geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                                    # Update window dimensions
                                    geometryNodes_modifier['Socket_34'] = window_width
                                    geometryNodes_modifier['Socket_35'] = window_height
                                    return True
                                # Main code for updating specific object
                                updated_objects = []
                                # Find view and projection matrices from the 3D view area
                                found_3d_view = False
                                for area in bpy.context.screen.areas:
                                    if area.type == 'VIEW_3D':
                                        view_matrix = area.spaces.active.region_3d.view_matrix
                                        proj_matrix = area.spaces.active.region_3d.window_matrix
                                        window_width = area.width
                                        window_height = area.height
                                        found_3d_view = True
                                        break
                                if not found_3d_view:
                                    print("Error: No 3D View found to update camera information.")
                                else:
                                    # Update only specific object
                                    target_object_name = ObjectName  # Serpens Variable
                                    obj = bpy.data.objects.get(target_object_name)
                                    if obj and obj.visible_get():
                                        print(f"Attempting to update object: {obj.name}")  # Debugging print
                                        if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                            updated_objects.append(obj.name)  # Add to updated list
                                # Print or output the list of updated objects
                                print("Updated objects:", updated_objects)
                                kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                if bpy.context and bpy.context.screen:
                                    for a in bpy.context.screen.areas:
                                        a.tag_redraw()
                                source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                offset_x = 0.0
                                new_object_name = None
                                # Input variables
                                #source_obj_name = "Cube"  # Change this to your object's name
                                #offset_x = 0.0  # Input float variable for X offset
                                # Get the source object
                                source_obj = bpy.data.objects.get(source_obj_name)
                                # Check if the object exists
                                if source_obj:
                                    # Create a copy of the object
                                    new_obj = source_obj.copy()
                                    new_obj.data = source_obj.data.copy()
                                    # Link the new object to the scene
                                    bpy.context.scene.collection.objects.link(new_obj)
                                    # Apply the offset if any
                                    new_obj.location.x += offset_x
                                    # Store the new object's name in a variable
                                    new_object_name = new_obj.name
                                else:
                                    new_object_name = "ERROR: Source object not found"
                                # Output the new object's name (this will be captured by Serpens)
                                print(new_object_name)
                                kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                                for i_95077 in range(len(bpy.context.view_layer.objects.selected)):
                                    bpy.context.view_layer.objects.selected[i_95077].select_set(state=False, view_layer=bpy.context.view_layer, )
                                if ((bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '5 Axes') or (bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '7 Axes') or (bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '9 Axes')):
                                    kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                                    view_type = 'BACKLEFT'
                                    view_mode = 'PERSP'
                                    from mathutils import Quaternion
                                    # Serpens variables
                                    #view_type = 'FRONT'
                                    #view_mode = 'ORTHO'
                                    # Dictionary of view rotations
                                    rotations = {
                                        # Main views - verified working
                                        'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                                        'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                                        'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                                        'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                                        'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                                        'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                                        # Corrected TOPFRONT view (45 degrees up from front)
                                        'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                                        # 45-degree views from back
                                        'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                                        'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                                        # Other 45-degree views
                                        'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                                        'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                                        'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                                        # 45-degree views from RIGHT
                                        'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                                        'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                                    }
                                    # Check if view type exists
                                    if view_type not in rotations:
                                        print(f"Invalid view type: {view_type}")
                                    else:
                                        # Find and set the 3D view
                                        for area in bpy.context.screen.areas:
                                            if area.type == 'VIEW_3D':
                                                view3d = area.spaces[0]
                                                region3d = view3d.region_3d
                                                # Set view mode and apply rotation
                                                region3d.view_perspective = view_mode
                                                region3d.view_rotation = rotations[view_type]
                                                break

                                    def delayed_0CFF3():
                                        print(kiri_3dgs_render__omnisplat['sna_omniviewbase'].name)
                                        ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                        from mathutils import Matrix
                                        # Define helper function for updating the geometry node sockets

                                        def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                            geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                                            if not geometryNodes_modifier:
                                                print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                                return False
                                            # Update view matrix
                                            geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                                            geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                                            geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                                            geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                                            geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                                            geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                                            geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                                            geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                                            geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                                            geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                                            geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                                            geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                                            geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                                            geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                                            geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                                            geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                                            # Update projection matrix
                                            geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                                            geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                                            geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                                            geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                                            geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                                            geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                                            geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                                            geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                                            geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                                            geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                                            geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                                            geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                                            geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                                            geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                                            geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                                            geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                                            # Update window dimensions
                                            geometryNodes_modifier['Socket_34'] = window_width
                                            geometryNodes_modifier['Socket_35'] = window_height
                                            return True
                                        # Main code for updating specific object
                                        updated_objects = []
                                        # Find view and projection matrices from the 3D view area
                                        found_3d_view = False
                                        for area in bpy.context.screen.areas:
                                            if area.type == 'VIEW_3D':
                                                view_matrix = area.spaces.active.region_3d.view_matrix
                                                proj_matrix = area.spaces.active.region_3d.window_matrix
                                                window_width = area.width
                                                window_height = area.height
                                                found_3d_view = True
                                                break
                                        if not found_3d_view:
                                            print("Error: No 3D View found to update camera information.")
                                        else:
                                            # Update only specific object
                                            target_object_name = ObjectName  # Serpens Variable
                                            obj = bpy.data.objects.get(target_object_name)
                                            if obj and obj.visible_get():
                                                print(f"Attempting to update object: {obj.name}")  # Debugging print
                                                if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                    updated_objects.append(obj.name)  # Add to updated list
                                        # Print or output the list of updated objects
                                        print("Updated objects:", updated_objects)
                                        print('dsrtghsd')
                                        kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                        if bpy.context and bpy.context.screen:
                                            for a in bpy.context.screen.areas:
                                                a.tag_redraw()
                                        source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                        offset_x = 0.0
                                        new_object_name = None
                                        # Input variables
                                        #source_obj_name = "Cube"  # Change this to your object's name
                                        #offset_x = 0.0  # Input float variable for X offset
                                        # Get the source object
                                        source_obj = bpy.data.objects.get(source_obj_name)
                                        # Check if the object exists
                                        if source_obj:
                                            # Create a copy of the object
                                            new_obj = source_obj.copy()
                                            new_obj.data = source_obj.data.copy()
                                            # Link the new object to the scene
                                            bpy.context.scene.collection.objects.link(new_obj)
                                            # Apply the offset if any
                                            new_obj.location.x += offset_x
                                            # Store the new object's name in a variable
                                            new_object_name = new_obj.name
                                        else:
                                            new_object_name = "ERROR: Source object not found"
                                        # Output the new object's name (this will be captured by Serpens)
                                        print(new_object_name)
                                        kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                                        for i_2AD47 in range(len(bpy.context.view_layer.objects.selected)):
                                            bpy.context.view_layer.objects.selected[i_2AD47].select_set(state=False, view_layer=bpy.context.view_layer, )
                                        kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                                        view_type = 'BACKRIGHT'
                                        view_mode = 'PERSP'
                                        from mathutils import Quaternion
                                        # Serpens variables
                                        #view_type = 'FRONT'
                                        #view_mode = 'ORTHO'
                                        # Dictionary of view rotations
                                        rotations = {
                                            # Main views - verified working
                                            'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                                            'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                                            'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                                            'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                                            'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                                            'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                                            # Corrected TOPFRONT view (45 degrees up from front)
                                            'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                                            # 45-degree views from back
                                            'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                                            'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                                            # Other 45-degree views
                                            'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                                            'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                                            'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                                            # 45-degree views from RIGHT
                                            'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                                            'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                                        }
                                        # Check if view type exists
                                        if view_type not in rotations:
                                            print(f"Invalid view type: {view_type}")
                                        else:
                                            # Find and set the 3D view
                                            for area in bpy.context.screen.areas:
                                                if area.type == 'VIEW_3D':
                                                    view3d = area.spaces[0]
                                                    region3d = view3d.region_3d
                                                    # Set view mode and apply rotation
                                                    region3d.view_perspective = view_mode
                                                    region3d.view_rotation = rotations[view_type]
                                                    break

                                        def delayed_5E158():
                                            ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                            from mathutils import Matrix
                                            # Define helper function for updating the geometry node sockets

                                            def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                                                if not geometryNodes_modifier:
                                                    print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                                    return False
                                                # Update view matrix
                                                geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                                                geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                                                geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                                                geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                                                geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                                                geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                                                geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                                                geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                                                geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                                                geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                                                geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                                                geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                                                geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                                                geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                                                geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                                                geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                                                # Update projection matrix
                                                geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                                                geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                                                geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                                                geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                                                geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                                                geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                                                geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                                                geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                                                geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                                                geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                                                geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                                                geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                                                geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                                                geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                                                geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                                                geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                                                # Update window dimensions
                                                geometryNodes_modifier['Socket_34'] = window_width
                                                geometryNodes_modifier['Socket_35'] = window_height
                                                return True
                                            # Main code for updating specific object
                                            updated_objects = []
                                            # Find view and projection matrices from the 3D view area
                                            found_3d_view = False
                                            for area in bpy.context.screen.areas:
                                                if area.type == 'VIEW_3D':
                                                    view_matrix = area.spaces.active.region_3d.view_matrix
                                                    proj_matrix = area.spaces.active.region_3d.window_matrix
                                                    window_width = area.width
                                                    window_height = area.height
                                                    found_3d_view = True
                                                    break
                                            if not found_3d_view:
                                                print("Error: No 3D View found to update camera information.")
                                            else:
                                                # Update only specific object
                                                target_object_name = ObjectName  # Serpens Variable
                                                obj = bpy.data.objects.get(target_object_name)
                                                if obj and obj.visible_get():
                                                    print(f"Attempting to update object: {obj.name}")  # Debugging print
                                                    if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                        updated_objects.append(obj.name)  # Add to updated list
                                            # Print or output the list of updated objects
                                            print("Updated objects:", updated_objects)
                                            kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                            if bpy.context and bpy.context.screen:
                                                for a in bpy.context.screen.areas:
                                                    a.tag_redraw()
                                            source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                            offset_x = 0.0
                                            new_object_name = None
                                            # Input variables
                                            #source_obj_name = "Cube"  # Change this to your object's name
                                            #offset_x = 0.0  # Input float variable for X offset
                                            # Get the source object
                                            source_obj = bpy.data.objects.get(source_obj_name)
                                            # Check if the object exists
                                            if source_obj:
                                                # Create a copy of the object
                                                new_obj = source_obj.copy()
                                                new_obj.data = source_obj.data.copy()
                                                # Link the new object to the scene
                                                bpy.context.scene.collection.objects.link(new_obj)
                                                # Apply the offset if any
                                                new_obj.location.x += offset_x
                                                # Store the new object's name in a variable
                                                new_object_name = new_obj.name
                                            else:
                                                new_object_name = "ERROR: Source object not found"
                                            # Output the new object's name (this will be captured by Serpens)
                                            print(new_object_name)
                                            kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                                            for i_86603 in range(len(bpy.context.view_layer.objects.selected)):
                                                bpy.context.view_layer.objects.selected[i_86603].select_set(state=False, view_layer=bpy.context.view_layer, )
                                            if ((bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '7 Axes') or (bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '9 Axes')):
                                                kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                view_type = 'TOPFRONT'
                                                view_mode = 'PERSP'
                                                from mathutils import Quaternion
                                                # Serpens variables
                                                #view_type = 'FRONT'
                                                #view_mode = 'ORTHO'
                                                # Dictionary of view rotations
                                                rotations = {
                                                    # Main views - verified working
                                                    'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                                                    'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                                                    'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                                                    'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                                                    'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                                                    'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                                                    # Corrected TOPFRONT view (45 degrees up from front)
                                                    'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                                                    # 45-degree views from back
                                                    'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                                                    'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                                                    # Other 45-degree views
                                                    'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                                                    'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                                                    'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                                                    # 45-degree views from RIGHT
                                                    'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                                                    'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                                                }
                                                # Check if view type exists
                                                if view_type not in rotations:
                                                    print(f"Invalid view type: {view_type}")
                                                else:
                                                    # Find and set the 3D view
                                                    for area in bpy.context.screen.areas:
                                                        if area.type == 'VIEW_3D':
                                                            view3d = area.spaces[0]
                                                            region3d = view3d.region_3d
                                                            # Set view mode and apply rotation
                                                            region3d.view_perspective = view_mode
                                                            region3d.view_rotation = rotations[view_type]
                                                            break

                                                def delayed_096EF():
                                                    ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                                    from mathutils import Matrix
                                                    # Define helper function for updating the geometry node sockets

                                                    def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                        geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                                                        if not geometryNodes_modifier:
                                                            print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                                            return False
                                                        # Update view matrix
                                                        geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                                                        geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                                                        geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                                                        geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                                                        geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                                                        geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                                                        geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                                                        geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                                                        geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                                                        geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                                                        geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                                                        geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                                                        geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                                                        geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                                                        geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                                                        geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                                                        # Update projection matrix
                                                        geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                                                        geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                                                        geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                                                        geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                                                        geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                                                        geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                                                        geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                                                        geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                                                        geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                                                        geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                                                        geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                                                        geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                                                        geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                                                        geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                                                        geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                                                        geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                                                        # Update window dimensions
                                                        geometryNodes_modifier['Socket_34'] = window_width
                                                        geometryNodes_modifier['Socket_35'] = window_height
                                                        return True
                                                    # Main code for updating specific object
                                                    updated_objects = []
                                                    # Find view and projection matrices from the 3D view area
                                                    found_3d_view = False
                                                    for area in bpy.context.screen.areas:
                                                        if area.type == 'VIEW_3D':
                                                            view_matrix = area.spaces.active.region_3d.view_matrix
                                                            proj_matrix = area.spaces.active.region_3d.window_matrix
                                                            window_width = area.width
                                                            window_height = area.height
                                                            found_3d_view = True
                                                            break
                                                    if not found_3d_view:
                                                        print("Error: No 3D View found to update camera information.")
                                                    else:
                                                        # Update only specific object
                                                        target_object_name = ObjectName  # Serpens Variable
                                                        obj = bpy.data.objects.get(target_object_name)
                                                        if obj and obj.visible_get():
                                                            print(f"Attempting to update object: {obj.name}")  # Debugging print
                                                            if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                                updated_objects.append(obj.name)  # Add to updated list
                                                    # Print or output the list of updated objects
                                                    print("Updated objects:", updated_objects)
                                                    kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                                    if bpy.context and bpy.context.screen:
                                                        for a in bpy.context.screen.areas:
                                                            a.tag_redraw()
                                                    source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                                    offset_x = 0.0
                                                    new_object_name = None
                                                    # Input variables
                                                    #source_obj_name = "Cube"  # Change this to your object's name
                                                    #offset_x = 0.0  # Input float variable for X offset
                                                    # Get the source object
                                                    source_obj = bpy.data.objects.get(source_obj_name)
                                                    # Check if the object exists
                                                    if source_obj:
                                                        # Create a copy of the object
                                                        new_obj = source_obj.copy()
                                                        new_obj.data = source_obj.data.copy()
                                                        # Link the new object to the scene
                                                        bpy.context.scene.collection.objects.link(new_obj)
                                                        # Apply the offset if any
                                                        new_obj.location.x += offset_x
                                                        # Store the new object's name in a variable
                                                        new_object_name = new_obj.name
                                                    else:
                                                        new_object_name = "ERROR: Source object not found"
                                                    # Output the new object's name (this will be captured by Serpens)
                                                    print(new_object_name)
                                                    kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                                                    for i_147A0 in range(len(bpy.context.view_layer.objects.selected)):
                                                        bpy.context.view_layer.objects.selected[i_147A0].select_set(state=False, view_layer=bpy.context.view_layer, )
                                                    kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                    view_type = 'BOTTOMFRONT'
                                                    view_mode = 'PERSP'
                                                    from mathutils import Quaternion
                                                    # Serpens variables
                                                    #view_type = 'FRONT'
                                                    #view_mode = 'ORTHO'
                                                    # Dictionary of view rotations
                                                    rotations = {
                                                        # Main views - verified working
                                                        'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                                                        'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                                                        'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                                                        'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                                                        'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                                                        'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                                                        # Corrected TOPFRONT view (45 degrees up from front)
                                                        'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                                                        # 45-degree views from back
                                                        'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                                                        'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                                                        # Other 45-degree views
                                                        'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                                                        'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                                                        'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                                                        # 45-degree views from RIGHT
                                                        'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                                                        'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                                                    }
                                                    # Check if view type exists
                                                    if view_type not in rotations:
                                                        print(f"Invalid view type: {view_type}")
                                                    else:
                                                        # Find and set the 3D view
                                                        for area in bpy.context.screen.areas:
                                                            if area.type == 'VIEW_3D':
                                                                view3d = area.spaces[0]
                                                                region3d = view3d.region_3d
                                                                # Set view mode and apply rotation
                                                                region3d.view_perspective = view_mode
                                                                region3d.view_rotation = rotations[view_type]
                                                                break

                                                    def delayed_FDA7B():
                                                        ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                                        from mathutils import Matrix
                                                        # Define helper function for updating the geometry node sockets

                                                        def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                            geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                                                            if not geometryNodes_modifier:
                                                                print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                                                return False
                                                            # Update view matrix
                                                            geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                                                            geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                                                            geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                                                            geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                                                            geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                                                            geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                                                            geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                                                            geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                                                            geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                                                            geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                                                            geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                                                            geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                                                            geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                                                            geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                                                            geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                                                            geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                                                            # Update projection matrix
                                                            geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                                                            geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                                                            geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                                                            geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                                                            geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                                                            geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                                                            geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                                                            geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                                                            geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                                                            geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                                                            geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                                                            geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                                                            geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                                                            geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                                                            geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                                                            geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                                                            # Update window dimensions
                                                            geometryNodes_modifier['Socket_34'] = window_width
                                                            geometryNodes_modifier['Socket_35'] = window_height
                                                            return True
                                                        # Main code for updating specific object
                                                        updated_objects = []
                                                        # Find view and projection matrices from the 3D view area
                                                        found_3d_view = False
                                                        for area in bpy.context.screen.areas:
                                                            if area.type == 'VIEW_3D':
                                                                view_matrix = area.spaces.active.region_3d.view_matrix
                                                                proj_matrix = area.spaces.active.region_3d.window_matrix
                                                                window_width = area.width
                                                                window_height = area.height
                                                                found_3d_view = True
                                                                break
                                                        if not found_3d_view:
                                                            print("Error: No 3D View found to update camera information.")
                                                        else:
                                                            # Update only specific object
                                                            target_object_name = ObjectName  # Serpens Variable
                                                            obj = bpy.data.objects.get(target_object_name)
                                                            if obj and obj.visible_get():
                                                                print(f"Attempting to update object: {obj.name}")  # Debugging print
                                                                if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                                    updated_objects.append(obj.name)  # Add to updated list
                                                        # Print or output the list of updated objects
                                                        print("Updated objects:", updated_objects)
                                                        kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                                        if bpy.context and bpy.context.screen:
                                                            for a in bpy.context.screen.areas:
                                                                a.tag_redraw()
                                                        source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                                        offset_x = 0.0
                                                        new_object_name = None
                                                        # Input variables
                                                        #source_obj_name = "Cube"  # Change this to your object's name
                                                        #offset_x = 0.0  # Input float variable for X offset
                                                        # Get the source object
                                                        source_obj = bpy.data.objects.get(source_obj_name)
                                                        # Check if the object exists
                                                        if source_obj:
                                                            # Create a copy of the object
                                                            new_obj = source_obj.copy()
                                                            new_obj.data = source_obj.data.copy()
                                                            # Link the new object to the scene
                                                            bpy.context.scene.collection.objects.link(new_obj)
                                                            # Apply the offset if any
                                                            new_obj.location.x += offset_x
                                                            # Store the new object's name in a variable
                                                            new_object_name = new_obj.name
                                                        else:
                                                            new_object_name = "ERROR: Source object not found"
                                                        # Output the new object's name (this will be captured by Serpens)
                                                        print(new_object_name)
                                                        kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                                                        for i_B661A in range(len(bpy.context.view_layer.objects.selected)):
                                                            bpy.context.view_layer.objects.selected[i_B661A].select_set(state=False, view_layer=bpy.context.view_layer, )
                                                        if (bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '9 Axes'):
                                                            kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                            view_type = 'TOPRIGHT'
                                                            view_mode = 'PERSP'
                                                            from mathutils import Quaternion
                                                            # Serpens variables
                                                            #view_type = 'FRONT'
                                                            #view_mode = 'ORTHO'
                                                            # Dictionary of view rotations
                                                            rotations = {
                                                                # Main views - verified working
                                                                'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                                                                'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                                                                'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                                                                'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                                                                'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                                                                'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                                                                # Corrected TOPFRONT view (45 degrees up from front)
                                                                'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                                                                # 45-degree views from back
                                                                'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                                                                'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                                                                # Other 45-degree views
                                                                'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                                                                'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                                                                'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                                                                # 45-degree views from RIGHT
                                                                'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                                                                'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                                                            }
                                                            # Check if view type exists
                                                            if view_type not in rotations:
                                                                print(f"Invalid view type: {view_type}")
                                                            else:
                                                                # Find and set the 3D view
                                                                for area in bpy.context.screen.areas:
                                                                    if area.type == 'VIEW_3D':
                                                                        view3d = area.spaces[0]
                                                                        region3d = view3d.region_3d
                                                                        # Set view mode and apply rotation
                                                                        region3d.view_perspective = view_mode
                                                                        region3d.view_rotation = rotations[view_type]
                                                                        break

                                                            def delayed_EDEBE():
                                                                ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                                                from mathutils import Matrix
                                                                # Define helper function for updating the geometry node sockets

                                                                def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                                    geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                                                                    if not geometryNodes_modifier:
                                                                        print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                                                        return False
                                                                    # Update view matrix
                                                                    geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                                                                    geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                                                                    geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                                                                    geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                                                                    geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                                                                    geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                                                                    geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                                                                    geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                                                                    geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                                                                    geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                                                                    geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                                                                    geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                                                                    geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                                                                    geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                                                                    geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                                                                    geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                                                                    # Update projection matrix
                                                                    geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                                                                    geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                                                                    geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                                                                    geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                                                                    geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                                                                    geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                                                                    geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                                                                    geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                                                                    geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                                                                    geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                                                                    geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                                                                    geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                                                                    geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                                                                    geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                                                                    geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                                                                    geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                                                                    # Update window dimensions
                                                                    geometryNodes_modifier['Socket_34'] = window_width
                                                                    geometryNodes_modifier['Socket_35'] = window_height
                                                                    return True
                                                                # Main code for updating specific object
                                                                updated_objects = []
                                                                # Find view and projection matrices from the 3D view area
                                                                found_3d_view = False
                                                                for area in bpy.context.screen.areas:
                                                                    if area.type == 'VIEW_3D':
                                                                        view_matrix = area.spaces.active.region_3d.view_matrix
                                                                        proj_matrix = area.spaces.active.region_3d.window_matrix
                                                                        window_width = area.width
                                                                        window_height = area.height
                                                                        found_3d_view = True
                                                                        break
                                                                if not found_3d_view:
                                                                    print("Error: No 3D View found to update camera information.")
                                                                else:
                                                                    # Update only specific object
                                                                    target_object_name = ObjectName  # Serpens Variable
                                                                    obj = bpy.data.objects.get(target_object_name)
                                                                    if obj and obj.visible_get():
                                                                        print(f"Attempting to update object: {obj.name}")  # Debugging print
                                                                        if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                                            updated_objects.append(obj.name)  # Add to updated list
                                                                # Print or output the list of updated objects
                                                                print("Updated objects:", updated_objects)
                                                                kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                                                if bpy.context and bpy.context.screen:
                                                                    for a in bpy.context.screen.areas:
                                                                        a.tag_redraw()
                                                                source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                                                offset_x = 0.0
                                                                new_object_name = None
                                                                # Input variables
                                                                #source_obj_name = "Cube"  # Change this to your object's name
                                                                #offset_x = 0.0  # Input float variable for X offset
                                                                # Get the source object
                                                                source_obj = bpy.data.objects.get(source_obj_name)
                                                                # Check if the object exists
                                                                if source_obj:
                                                                    # Create a copy of the object
                                                                    new_obj = source_obj.copy()
                                                                    new_obj.data = source_obj.data.copy()
                                                                    # Link the new object to the scene
                                                                    bpy.context.scene.collection.objects.link(new_obj)
                                                                    # Apply the offset if any
                                                                    new_obj.location.x += offset_x
                                                                    # Store the new object's name in a variable
                                                                    new_object_name = new_obj.name
                                                                else:
                                                                    new_object_name = "ERROR: Source object not found"
                                                                # Output the new object's name (this will be captured by Serpens)
                                                                print(new_object_name)
                                                                kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                                                                for i_95593 in range(len(bpy.context.view_layer.objects.selected)):
                                                                    bpy.context.view_layer.objects.selected[i_95593].select_set(state=False, view_layer=bpy.context.view_layer, )
                                                                kiri_3dgs_render__omnisplat['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                                view_type = 'BOTTOMRIGHT'
                                                                view_mode = 'PERSP'
                                                                from mathutils import Quaternion
                                                                # Serpens variables
                                                                #view_type = 'FRONT'
                                                                #view_mode = 'ORTHO'
                                                                # Dictionary of view rotations
                                                                rotations = {
                                                                    # Main views - verified working
                                                                    'FRONT': Quaternion((0.707107, 0.707107, 0.0, 0.0)),
                                                                    'BACK': Quaternion((0.000000, 0.000000, 0.707107, 0.707107)),
                                                                    'LEFT': Quaternion((0.5, 0.5, -0.5, -0.5)),
                                                                    'RIGHT': Quaternion((0.5, 0.5, 0.5, 0.5)),
                                                                    'TOP': Quaternion((1.0, 0.0, 0.0, 0.0)),
                                                                    'BOTTOM': Quaternion((0.000000, 1.000000, 0.000000, 0.000000)),
                                                                    # Corrected TOPFRONT view (45 degrees up from front)
                                                                    'TOPFRONT': Quaternion((0.923879, 0.382683, 0.0, 0.0)),
                                                                    # 45-degree views from back
                                                                    'BACKLEFT': Quaternion((0.270598, 0.270598, 0.653281, 0.653281)),
                                                                    'BACKRIGHT': Quaternion((-0.270598, -0.270598, 0.653281, 0.653281)),
                                                                    # Other 45-degree views
                                                                    'BOTTOMFRONT': Quaternion((0.382683, 0.923880, 0.000000, 0.000000)),
                                                                    'BACKTOP': Quaternion((0.000000, 0.000000, 0.382683, 0.923880)),
                                                                    'BACKBOTTOM': Quaternion((0.000000, 0.000000, 0.923880, 0.382683)),
                                                                    # 45-degree views from RIGHT
                                                                    'BOTTOMRIGHT': Quaternion((0.183013, 0.683013, 0.683013, 0.183013)),
                                                                    'TOPRIGHT': Quaternion((0.683013, 0.183013, 0.183013, 0.683013))  # Corrected for downward rotation
                                                                }
                                                                # Check if view type exists
                                                                if view_type not in rotations:
                                                                    print(f"Invalid view type: {view_type}")
                                                                else:
                                                                    # Find and set the 3D view
                                                                    for area in bpy.context.screen.areas:
                                                                        if area.type == 'VIEW_3D':
                                                                            view3d = area.spaces[0]
                                                                            region3d = view3d.region_3d
                                                                            # Set view mode and apply rotation
                                                                            region3d.view_perspective = view_mode
                                                                            region3d.view_rotation = rotations[view_type]
                                                                            break

                                                                def delayed_FCFF0():
                                                                    ObjectName = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                                                    from mathutils import Matrix
                                                                    # Define helper function for updating the geometry node sockets

                                                                    def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                                        geometryNodes_modifier = obj.modifiers.get('KIRI_3DGS_Render_GN')
                                                                        if not geometryNodes_modifier:
                                                                            print(f"Error: GeometryNodes modifier not found on object '{obj.name}'.")
                                                                            return False
                                                                        # Update view matrix
                                                                        geometryNodes_modifier['Socket_2'] = view_matrix[0][0]
                                                                        geometryNodes_modifier['Socket_3'] = view_matrix[1][0]
                                                                        geometryNodes_modifier['Socket_4'] = view_matrix[2][0]
                                                                        geometryNodes_modifier['Socket_5'] = view_matrix[3][0]
                                                                        geometryNodes_modifier['Socket_6'] = view_matrix[0][1]
                                                                        geometryNodes_modifier['Socket_7'] = view_matrix[1][1]
                                                                        geometryNodes_modifier['Socket_8'] = view_matrix[2][1]
                                                                        geometryNodes_modifier['Socket_9'] = view_matrix[3][1]
                                                                        geometryNodes_modifier['Socket_10'] = view_matrix[0][2]
                                                                        geometryNodes_modifier['Socket_11'] = view_matrix[1][2]
                                                                        geometryNodes_modifier['Socket_12'] = view_matrix[2][2]
                                                                        geometryNodes_modifier['Socket_13'] = view_matrix[3][2]
                                                                        geometryNodes_modifier['Socket_14'] = view_matrix[0][3]
                                                                        geometryNodes_modifier['Socket_15'] = view_matrix[1][3]
                                                                        geometryNodes_modifier['Socket_16'] = view_matrix[2][3]
                                                                        geometryNodes_modifier['Socket_17'] = view_matrix[3][3]
                                                                        # Update projection matrix
                                                                        geometryNodes_modifier['Socket_18'] = proj_matrix[0][0]
                                                                        geometryNodes_modifier['Socket_19'] = proj_matrix[1][0]
                                                                        geometryNodes_modifier['Socket_20'] = proj_matrix[2][0]
                                                                        geometryNodes_modifier['Socket_21'] = proj_matrix[3][0]
                                                                        geometryNodes_modifier['Socket_22'] = proj_matrix[0][1]
                                                                        geometryNodes_modifier['Socket_23'] = proj_matrix[1][1]
                                                                        geometryNodes_modifier['Socket_24'] = proj_matrix[2][1]
                                                                        geometryNodes_modifier['Socket_25'] = proj_matrix[3][1]
                                                                        geometryNodes_modifier['Socket_26'] = proj_matrix[0][2]
                                                                        geometryNodes_modifier['Socket_27'] = proj_matrix[1][2]
                                                                        geometryNodes_modifier['Socket_28'] = proj_matrix[2][2]
                                                                        geometryNodes_modifier['Socket_29'] = proj_matrix[3][2]
                                                                        geometryNodes_modifier['Socket_30'] = proj_matrix[0][3]
                                                                        geometryNodes_modifier['Socket_31'] = proj_matrix[1][3]
                                                                        geometryNodes_modifier['Socket_32'] = proj_matrix[2][3]
                                                                        geometryNodes_modifier['Socket_33'] = proj_matrix[3][3]
                                                                        # Update window dimensions
                                                                        geometryNodes_modifier['Socket_34'] = window_width
                                                                        geometryNodes_modifier['Socket_35'] = window_height
                                                                        return True
                                                                    # Main code for updating specific object
                                                                    updated_objects = []
                                                                    # Find view and projection matrices from the 3D view area
                                                                    found_3d_view = False
                                                                    for area in bpy.context.screen.areas:
                                                                        if area.type == 'VIEW_3D':
                                                                            view_matrix = area.spaces.active.region_3d.view_matrix
                                                                            proj_matrix = area.spaces.active.region_3d.window_matrix
                                                                            window_width = area.width
                                                                            window_height = area.height
                                                                            found_3d_view = True
                                                                            break
                                                                    if not found_3d_view:
                                                                        print("Error: No 3D View found to update camera information.")
                                                                    else:
                                                                        # Update only specific object
                                                                        target_object_name = ObjectName  # Serpens Variable
                                                                        obj = bpy.data.objects.get(target_object_name)
                                                                        if obj and obj.visible_get():
                                                                            print(f"Attempting to update object: {obj.name}")  # Debugging print
                                                                            if update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
                                                                                updated_objects.append(obj.name)  # Add to updated list
                                                                    # Print or output the list of updated objects
                                                                    print("Updated objects:", updated_objects)
                                                                    kiri_3dgs_render__omnisplat['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                                                    if bpy.context and bpy.context.screen:
                                                                        for a in bpy.context.screen.areas:
                                                                            a.tag_redraw()
                                                                    source_obj_name = kiri_3dgs_render__omnisplat['sna_omniviewbase'].name
                                                                    offset_x = 0.0
                                                                    new_object_name = None
                                                                    # Input variables
                                                                    #source_obj_name = "Cube"  # Change this to your object's name
                                                                    #offset_x = 0.0  # Input float variable for X offset
                                                                    # Get the source object
                                                                    source_obj = bpy.data.objects.get(source_obj_name)
                                                                    # Check if the object exists
                                                                    if source_obj:
                                                                        # Create a copy of the object
                                                                        new_obj = source_obj.copy()
                                                                        new_obj.data = source_obj.data.copy()
                                                                        # Link the new object to the scene
                                                                        bpy.context.scene.collection.objects.link(new_obj)
                                                                        # Apply the offset if any
                                                                        new_obj.location.x += offset_x
                                                                        # Store the new object's name in a variable
                                                                        new_object_name = new_obj.name
                                                                    else:
                                                                        new_object_name = "ERROR: Source object not found"
                                                                    # Output the new object's name (this will be captured by Serpens)
                                                                    print(new_object_name)
                                                                    kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'].append(new_object_name)
                                                                    for i_80970 in range(len(bpy.context.view_layer.objects.selected)):
                                                                        bpy.context.view_layer.objects.selected[i_80970].select_set(state=False, view_layer=bpy.context.view_layer, )
                                                                    for i_D0394 in range(len(kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'])):
                                                                        bpy.data.objects[kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'][i_D0394]].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                                        bpy.context.view_layer.objects.active = bpy.data.objects[kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'][i_D0394]]
                                                                    bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
                                                                    bpy.ops.object.join('INVOKE_DEFAULT', )
                                                                    bpy.data.objects.remove(object=kiri_3dgs_render__omnisplat['sna_omniviewbase'], do_unlink=True, do_id_user=True, do_ui_user=True, )
                                                                    object_name = bpy.context.view_layer.objects.active.name
                                                                    prop_name = 'OmniviewAngle'
                                                                    prop_type = 'float'

                                                                    default_value = 50.0
                                                                    from bpy.props import (FloatProperty, 
                                                                                          IntProperty,
                                                                                          StringProperty,
                                                                                          BoolProperty)
                                                                    # Input variables (to be set by Serpens)
                                                                    #object_name = "OBJECT_NAME"  # Replace with Serpens input
                                                                    #prop_name = "PROP_NAME"      # Replace with Serpens input
                                                                    #prop_type = "PROP_TYPE"      # Replace with Serpens input ('float', 'int', 'string', 'bool')
                                                                    #default_value = "DEFAULT_VALUE"  # Replace with Serpens input
                                                                    # Check if object exists
                                                                    if object_name not in bpy.data.objects:
                                                                        print(f"Error: Object '{object_name}' not found in scene")
                                                                    else:
                                                                        # Get the object
                                                                        obj = bpy.data.objects[object_name]
                                                                        # Create property based on type
                                                                        try:
                                                                            if prop_type.lower() == 'float':
                                                                                obj[prop_name] = float(default_value)
                                                                                obj.id_properties_ui(prop_name).update(
                                                                                    description="Custom float property",

                                                                                    default=float(default_value),
                                                                                    min=-1000.0,
                                                                                    max=1000.0
                                                                                )
                                                                            elif prop_type.lower() == 'int':
                                                                                obj[prop_name] = int(default_value)
                                                                                obj.id_properties_ui(prop_name).update(
                                                                                    description="Custom integer property",

                                                                                    default=int(default_value),
                                                                                    min=-1000,
                                                                                    max=1000
                                                                                )
                                                                            elif prop_type.lower() == 'bool':
                                                                                obj[prop_name] = bool(default_value)
                                                                                obj.id_properties_ui(prop_name).update(
                                                                                    description="Custom boolean property",

                                                                                    default=bool(default_value)
                                                                                )
                                                                            elif prop_type.lower() == 'string':
                                                                                obj[prop_name] = str(default_value)
                                                                                obj.id_properties_ui(prop_name).update(
                                                                                    description="Custom string property",

                                                                                    default=str(default_value)
                                                                                )
                                                                            else:
                                                                                print(f"Error: Unsupported property type '{prop_type}'")
                                                                            print(f"Successfully added {prop_type} property '{prop_name}' to object '{object_name}'")
                                                                        except Exception as e:
                                                                            print(f"Error creating custom property: {str(e)}")
                                                                    object_name = bpy.context.view_layer.objects.active.name
                                                                    property_name = 'GS_ID'
                                                                    # Replace these with your object and property names
                                                                    #object_name = "Cube"
                                                                    #property_name = "my_custom_prop"
                                                                    # Get the object
                                                                    obj = bpy.data.objects.get(object_name)
                                                                    if obj is None:
                                                                        print(f"Error: Object '{object_name}' not found in the scene")
                                                                    else:
                                                                        if property_name in obj:
                                                                            del obj[property_name]
                                                                            print(f"Removed property '{property_name}' from object '{object_name}'")
                                                                        else:
                                                                            print(f"Property '{property_name}' not found on object '{object_name}'")
                                                                    object_name = bpy.context.view_layer.objects.active.name
                                                                    property_name = 'update_rot_to_cam'
                                                                    # Replace these with your object and property names
                                                                    #object_name = "Cube"
                                                                    #property_name = "my_custom_prop"
                                                                    # Get the object
                                                                    obj = bpy.data.objects.get(object_name)
                                                                    if obj is None:
                                                                        print(f"Error: Object '{object_name}' not found in the scene")
                                                                    else:
                                                                        if property_name in obj:
                                                                            del obj[property_name]
                                                                            print(f"Removed property '{property_name}' from object '{object_name}'")
                                                                        else:
                                                                            print(f"Property '{property_name}' not found on object '{object_name}'")
                                                                bpy.app.timers.register(delayed_FCFF0, first_interval=0.10000000149011612)
                                                            bpy.app.timers.register(delayed_EDEBE, first_interval=0.10000000149011612)
                                                        else:
                                                            for i_44E24 in range(len(kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'])):
                                                                bpy.data.objects[kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'][i_44E24]].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                                bpy.context.view_layer.objects.active = bpy.data.objects[kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'][i_44E24]]
                                                            bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
                                                            bpy.ops.object.join('INVOKE_DEFAULT', )
                                                            bpy.data.objects.remove(object=kiri_3dgs_render__omnisplat['sna_omniviewbase'], do_unlink=True, do_id_user=True, do_ui_user=True, )
                                                            object_name = bpy.context.view_layer.objects.active.name
                                                            prop_name = 'OmniviewAngle'
                                                            prop_type = 'float'

                                                            default_value = 50.0
                                                            from bpy.props import (FloatProperty, 
                                                                                  IntProperty,
                                                                                  StringProperty,
                                                                                  BoolProperty)
                                                            # Input variables (to be set by Serpens)
                                                            #object_name = "OBJECT_NAME"  # Replace with Serpens input
                                                            #prop_name = "PROP_NAME"      # Replace with Serpens input
                                                            #prop_type = "PROP_TYPE"      # Replace with Serpens input ('float', 'int', 'string', 'bool')
                                                            #default_value = "DEFAULT_VALUE"  # Replace with Serpens input
                                                            # Check if object exists
                                                            if object_name not in bpy.data.objects:
                                                                print(f"Error: Object '{object_name}' not found in scene")
                                                            else:
                                                                # Get the object
                                                                obj = bpy.data.objects[object_name]
                                                                # Create property based on type
                                                                try:
                                                                    if prop_type.lower() == 'float':
                                                                        obj[prop_name] = float(default_value)
                                                                        obj.id_properties_ui(prop_name).update(
                                                                            description="Custom float property",

                                                                            default=float(default_value),
                                                                            min=-1000.0,
                                                                            max=1000.0
                                                                        )
                                                                    elif prop_type.lower() == 'int':
                                                                        obj[prop_name] = int(default_value)
                                                                        obj.id_properties_ui(prop_name).update(
                                                                            description="Custom integer property",

                                                                            default=int(default_value),
                                                                            min=-1000,
                                                                            max=1000
                                                                        )
                                                                    elif prop_type.lower() == 'bool':
                                                                        obj[prop_name] = bool(default_value)
                                                                        obj.id_properties_ui(prop_name).update(
                                                                            description="Custom boolean property",

                                                                            default=bool(default_value)
                                                                        )
                                                                    elif prop_type.lower() == 'string':
                                                                        obj[prop_name] = str(default_value)
                                                                        obj.id_properties_ui(prop_name).update(
                                                                            description="Custom string property",

                                                                            default=str(default_value)
                                                                        )
                                                                    else:
                                                                        print(f"Error: Unsupported property type '{prop_type}'")
                                                                    print(f"Successfully added {prop_type} property '{prop_name}' to object '{object_name}'")
                                                                except Exception as e:
                                                                    print(f"Error creating custom property: {str(e)}")
                                                            object_name = bpy.context.view_layer.objects.active.name
                                                            property_name = 'GS_ID'
                                                            # Replace these with your object and property names
                                                            #object_name = "Cube"
                                                            #property_name = "my_custom_prop"
                                                            # Get the object
                                                            obj = bpy.data.objects.get(object_name)
                                                            if obj is None:
                                                                print(f"Error: Object '{object_name}' not found in the scene")
                                                            else:
                                                                if property_name in obj:
                                                                    del obj[property_name]
                                                                    print(f"Removed property '{property_name}' from object '{object_name}'")
                                                                else:
                                                                    print(f"Property '{property_name}' not found on object '{object_name}'")
                                                            object_name = bpy.context.view_layer.objects.active.name
                                                            property_name = 'update_rot_to_cam'
                                                            # Replace these with your object and property names
                                                            #object_name = "Cube"
                                                            #property_name = "my_custom_prop"
                                                            # Get the object
                                                            obj = bpy.data.objects.get(object_name)
                                                            if obj is None:
                                                                print(f"Error: Object '{object_name}' not found in the scene")
                                                            else:
                                                                if property_name in obj:
                                                                    del obj[property_name]
                                                                    print(f"Removed property '{property_name}' from object '{object_name}'")
                                                                else:
                                                                    print(f"Property '{property_name}' not found on object '{object_name}'")
                                                    bpy.app.timers.register(delayed_FDA7B, first_interval=0.10000000149011612)
                                                bpy.app.timers.register(delayed_096EF, first_interval=0.10000000149011612)
                                            else:
                                                for i_3BF64 in range(len(kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'])):
                                                    bpy.data.objects[kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'][i_3BF64]].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                    bpy.context.view_layer.objects.active = bpy.data.objects[kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'][i_3BF64]]
                                                bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
                                                bpy.ops.object.join('INVOKE_DEFAULT', )
                                                bpy.data.objects.remove(object=kiri_3dgs_render__omnisplat['sna_omniviewbase'], do_unlink=True, do_id_user=True, do_ui_user=True, )
                                                object_name = bpy.context.view_layer.objects.active.name
                                                prop_name = 'OmniviewAngle'
                                                prop_type = 'float'

                                                default_value = 50.0
                                                from bpy.props import (FloatProperty, 
                                                                      IntProperty,
                                                                      StringProperty,
                                                                      BoolProperty)
                                                # Input variables (to be set by Serpens)
                                                #object_name = "OBJECT_NAME"  # Replace with Serpens input
                                                #prop_name = "PROP_NAME"      # Replace with Serpens input
                                                #prop_type = "PROP_TYPE"      # Replace with Serpens input ('float', 'int', 'string', 'bool')
                                                #default_value = "DEFAULT_VALUE"  # Replace with Serpens input
                                                # Check if object exists
                                                if object_name not in bpy.data.objects:
                                                    print(f"Error: Object '{object_name}' not found in scene")
                                                else:
                                                    # Get the object
                                                    obj = bpy.data.objects[object_name]
                                                    # Create property based on type
                                                    try:
                                                        if prop_type.lower() == 'float':
                                                            obj[prop_name] = float(default_value)
                                                            obj.id_properties_ui(prop_name).update(
                                                                description="Custom float property",

                                                                default=float(default_value),
                                                                min=-1000.0,
                                                                max=1000.0
                                                            )
                                                        elif prop_type.lower() == 'int':
                                                            obj[prop_name] = int(default_value)
                                                            obj.id_properties_ui(prop_name).update(
                                                                description="Custom integer property",

                                                                default=int(default_value),
                                                                min=-1000,
                                                                max=1000
                                                            )
                                                        elif prop_type.lower() == 'bool':
                                                            obj[prop_name] = bool(default_value)
                                                            obj.id_properties_ui(prop_name).update(
                                                                description="Custom boolean property",

                                                                default=bool(default_value)
                                                            )
                                                        elif prop_type.lower() == 'string':
                                                            obj[prop_name] = str(default_value)
                                                            obj.id_properties_ui(prop_name).update(
                                                                description="Custom string property",

                                                                default=str(default_value)
                                                            )
                                                        else:
                                                            print(f"Error: Unsupported property type '{prop_type}'")
                                                        print(f"Successfully added {prop_type} property '{prop_name}' to object '{object_name}'")
                                                    except Exception as e:
                                                        print(f"Error creating custom property: {str(e)}")
                                                object_name = bpy.context.view_layer.objects.active.name
                                                property_name = 'GS_ID'
                                                # Replace these with your object and property names
                                                #object_name = "Cube"
                                                #property_name = "my_custom_prop"
                                                # Get the object
                                                obj = bpy.data.objects.get(object_name)
                                                if obj is None:
                                                    print(f"Error: Object '{object_name}' not found in the scene")
                                                else:
                                                    if property_name in obj:
                                                        del obj[property_name]
                                                        print(f"Removed property '{property_name}' from object '{object_name}'")
                                                    else:
                                                        print(f"Property '{property_name}' not found on object '{object_name}'")
                                                object_name = bpy.context.view_layer.objects.active.name
                                                property_name = 'update_rot_to_cam'
                                                # Replace these with your object and property names
                                                #object_name = "Cube"
                                                #property_name = "my_custom_prop"
                                                # Get the object
                                                obj = bpy.data.objects.get(object_name)
                                                if obj is None:
                                                    print(f"Error: Object '{object_name}' not found in the scene")
                                                else:
                                                    if property_name in obj:
                                                        del obj[property_name]
                                                        print(f"Removed property '{property_name}' from object '{object_name}'")
                                                    else:
                                                        print(f"Property '{property_name}' not found on object '{object_name}'")
                                        bpy.app.timers.register(delayed_5E158, first_interval=0.10000000149011612)
                                    bpy.app.timers.register(delayed_0CFF3, first_interval=0.10000000149011612)
                                else:
                                    for i_C2630 in range(len(kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'])):
                                        bpy.data.objects[kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'][i_C2630]].select_set(state=True, view_layer=bpy.context.view_layer, )
                                        bpy.context.view_layer.objects.active = bpy.data.objects[kiri_3dgs_render__omnisplat['sna_omniviewobjectsformerge'][i_C2630]]
                                    bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
                                    bpy.ops.object.join('INVOKE_DEFAULT', )
                                    bpy.data.objects.remove(object=kiri_3dgs_render__omnisplat['sna_omniviewbase'], do_unlink=True, do_id_user=True, do_ui_user=True, )
                                    object_name = bpy.context.view_layer.objects.active.name
                                    prop_name = 'OmniviewAngle'
                                    prop_type = 'float'

                                    default_value = 50.0
                                    from bpy.props import (FloatProperty, 
                                                          IntProperty,
                                                          StringProperty,
                                                          BoolProperty)
                                    # Input variables (to be set by Serpens)
                                    #object_name = "OBJECT_NAME"  # Replace with Serpens input
                                    #prop_name = "PROP_NAME"      # Replace with Serpens input
                                    #prop_type = "PROP_TYPE"      # Replace with Serpens input ('float', 'int', 'string', 'bool')
                                    #default_value = "DEFAULT_VALUE"  # Replace with Serpens input
                                    # Check if object exists
                                    if object_name not in bpy.data.objects:
                                        print(f"Error: Object '{object_name}' not found in scene")
                                    else:
                                        # Get the object
                                        obj = bpy.data.objects[object_name]
                                        # Create property based on type
                                        try:
                                            if prop_type.lower() == 'float':
                                                obj[prop_name] = float(default_value)
                                                obj.id_properties_ui(prop_name).update(
                                                    description="Custom float property",

                                                    default=float(default_value),
                                                    min=-1000.0,
                                                    max=1000.0
                                                )
                                            elif prop_type.lower() == 'int':
                                                obj[prop_name] = int(default_value)
                                                obj.id_properties_ui(prop_name).update(
                                                    description="Custom integer property",

                                                    default=int(default_value),
                                                    min=-1000,
                                                    max=1000
                                                )
                                            elif prop_type.lower() == 'bool':
                                                obj[prop_name] = bool(default_value)
                                                obj.id_properties_ui(prop_name).update(
                                                    description="Custom boolean property",

                                                    default=bool(default_value)
                                                )
                                            elif prop_type.lower() == 'string':
                                                obj[prop_name] = str(default_value)
                                                obj.id_properties_ui(prop_name).update(
                                                    description="Custom string property",

                                                    default=str(default_value)
                                                )
                                            else:
                                                print(f"Error: Unsupported property type '{prop_type}'")
                                            print(f"Successfully added {prop_type} property '{prop_name}' to object '{object_name}'")
                                        except Exception as e:
                                            print(f"Error creating custom property: {str(e)}")
                                    object_name = bpy.context.view_layer.objects.active.name
                                    property_name = 'GS_ID'
                                    # Replace these with your object and property names
                                    #object_name = "Cube"
                                    #property_name = "my_custom_prop"
                                    # Get the object
                                    obj = bpy.data.objects.get(object_name)
                                    if obj is None:
                                        print(f"Error: Object '{object_name}' not found in the scene")
                                    else:
                                        if property_name in obj:
                                            del obj[property_name]
                                            print(f"Removed property '{property_name}' from object '{object_name}'")
                                        else:
                                            print(f"Property '{property_name}' not found on object '{object_name}'")
                                    object_name = bpy.context.view_layer.objects.active.name
                                    property_name = 'update_rot_to_cam'
                                    # Replace these with your object and property names
                                    #object_name = "Cube"
                                    #property_name = "my_custom_prop"
                                    # Get the object
                                    obj = bpy.data.objects.get(object_name)
                                    if obj is None:
                                        print(f"Error: Object '{object_name}' not found in the scene")
                                    else:
                                        if property_name in obj:
                                            del obj[property_name]
                                            print(f"Removed property '{property_name}' from object '{object_name}'")
                                        else:
                                            print(f"Property '{property_name}' not found on object '{object_name}'")
                            bpy.app.timers.register(delayed_FE628, first_interval=0.10000000149011612)
                        bpy.app.timers.register(delayed_CF40F, first_interval=0.10000000149011612)
                    bpy.app.timers.register(delayed_7EF56, first_interval=0.10000000149011612)
                bpy.app.timers.register(delayed_A59B5, first_interval=0.10000000149011612)
            else:
                self.report({'ERROR'}, message='Active object does not have 3DGS Render modifier')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_E1BE2 = layout.box()
        box_E1BE2.alert = True
        box_E1BE2.enabled = True
        box_E1BE2.active = True
        box_E1BE2.use_property_split = False
        box_E1BE2.use_property_decorate = False
        box_E1BE2.alignment = 'Expand'.upper()
        box_E1BE2.scale_x = 1.0
        box_E1BE2.scale_y = 1.0
        if not True: box_E1BE2.operator_context = "EXEC_DEFAULT"
        box_E1BE2.label(text='This is a very performance intensive task', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'info-3016385-white.png')))
        box_E1BE2.label(text='         It is advised to use this on simple objects, not full scenes', icon_value=0)
        box_E1BE2.label(text='         Perform all edits and decimation first', icon_value=0)
        box_E1BE2.label(text='         Existing modifiers will be removed', icon_value=0)
        box_E1BE2.label(text='         Omniview objects will not HQ render well', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


class SNA_AddonPreferences_03DFE(bpy.types.AddonPreferences):
    bl_idname = 'dgs_render_by_kiri_engine'
    sna_hq_sorter_directory: bpy.props.StringProperty(name='HQ Sorter Directory', description='', default='SELECT SORT FILE', subtype='FILE_PATH', maxlen=0)
    sna_auto_rotate_for_blender_axes_z_up: bpy.props.BoolProperty(name='Auto Rotate For Blender Axes (Z Up)', description='', default=True)

    def sna_default_face_alignment_edit_mode_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_default_face_alignment_edit_mode: bpy.props.EnumProperty(name='Default Face Alignment (Edit Mode)', description='', items=[('To Y Axis', 'To Y Axis', '', 0, 0), ('To X Axis', 'To X Axis', '', 0, 1), ('To Z Axis', 'To Z Axis', '', 0, 2)])

    def draw(self, context):
        if not (False):
            layout = self.layout 
            box_2B885 = layout.box()
            box_2B885.alert = False
            box_2B885.enabled = True
            box_2B885.active = True
            box_2B885.use_property_split = False
            box_2B885.use_property_decorate = False
            box_2B885.alignment = 'Expand'.upper()
            box_2B885.scale_x = 1.0
            box_2B885.scale_y = 1.0
            if not True: box_2B885.operator_context = "EXEC_DEFAULT"
            box_2B885.label(text='Import PLY As Splats Settings', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
            box_5B686 = box_2B885.box()
            box_5B686.alert = False
            box_5B686.enabled = True
            box_5B686.active = True
            box_5B686.use_property_split = False
            box_5B686.use_property_decorate = False
            box_5B686.alignment = 'Expand'.upper()
            box_5B686.scale_x = 1.0
            box_5B686.scale_y = 1.0
            if not True: box_5B686.operator_context = "EXEC_DEFAULT"
            box_5B686.prop(bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences, 'sna_auto_rotate_for_blender_axes_z_up', text='Auto Rotate For Blender Axes (Z Up)', icon_value=0, emboss=True)
            box_9B36B = box_2B885.box()
            box_9B36B.alert = False
            box_9B36B.enabled = True
            box_9B36B.active = True
            box_9B36B.use_property_split = False
            box_9B36B.use_property_decorate = False
            box_9B36B.alignment = 'Expand'.upper()
            box_9B36B.scale_x = 1.0
            box_9B36B.scale_y = 1.0
            if not True: box_9B36B.operator_context = "EXEC_DEFAULT"
            box_9B36B.label(text='Default Face Alignment (Edit Mode)', icon_value=0)
            box_9B36B.prop(bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences, 'sna_default_face_alignment_edit_mode', text='', icon_value=0, emboss=True)
            box_1404F = layout.box()
            box_1404F.alert = False
            box_1404F.enabled = True
            box_1404F.active = True
            box_1404F.use_property_split = False
            box_1404F.use_property_decorate = False
            box_1404F.alignment = 'Expand'.upper()
            box_1404F.scale_x = 1.0
            box_1404F.scale_y = 1.0
            if not True: box_1404F.operator_context = "EXEC_DEFAULT"
            box_1404F.label(text='HQ Render', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
            box_BC98F = box_1404F.box()
            box_BC98F.alert = False
            box_BC98F.enabled = True
            box_BC98F.active = True
            box_BC98F.use_property_split = False
            box_BC98F.use_property_decorate = False
            box_BC98F.alignment = 'Expand'.upper()
            box_BC98F.scale_x = 1.0
            box_BC98F.scale_y = 1.0
            if not True: box_BC98F.operator_context = "EXEC_DEFAULT"
            box_BC98F.label(text='HQ Rendering is available for Mac and Windows operating systems.', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'info-3016385-white.png')))
            box_BC98F.label(text='         Please assign the correct file type for your system', icon_value=0)
            box_BC98F.label(text='         Check the documentation for further assitance', icon_value=0)
            box_1404F.prop(bpy.context.preferences.addons['dgs_render_by_kiri_engine'].preferences, 'sna_hq_sorter_directory', text='', icon_value=0, emboss=True)


def sna_render_function_interface_C67EB(layout_function, ):
    if (bpy.context.scene.camera == None):
        box_0DD63 = layout_function.box()
        box_0DD63.alert = True
        box_0DD63.enabled = True
        box_0DD63.active = True
        box_0DD63.use_property_split = False
        box_0DD63.use_property_decorate = False
        box_0DD63.alignment = 'Expand'.upper()
        box_0DD63.scale_x = 1.0
        box_0DD63.scale_y = 1.0
        if not True: box_0DD63.operator_context = "EXEC_DEFAULT"
        box_0DD63.label(text='No active camera in scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
    else:
        if (bpy.context.scene.render.filepath == ''):
            box_DBC53 = layout_function.box()
            box_DBC53.alert = True
            box_DBC53.enabled = True
            box_DBC53.active = True
            box_DBC53.use_property_split = False
            box_DBC53.use_property_decorate = False
            box_DBC53.alignment = 'Expand'.upper()
            box_DBC53.scale_x = 1.0
            box_DBC53.scale_y = 1.0
            if not True: box_DBC53.operator_context = "EXEC_DEFAULT"
            box_DBC53.label(text='Output path is empty', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
        else:
            col_32C11 = layout_function.column(heading='', align=False)
            col_32C11.alert = False
            col_32C11.enabled = True
            col_32C11.active = True
            col_32C11.use_property_split = False
            col_32C11.use_property_decorate = False
            col_32C11.scale_x = 1.0
            col_32C11.scale_y = 1.0
            col_32C11.alignment = 'Expand'.upper()
            col_32C11.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_78D4A = col_32C11.box()
            box_78D4A.alert = (bpy.context.scene.view_settings.view_transform != 'Standard')
            box_78D4A.enabled = True
            box_78D4A.active = True
            box_78D4A.use_property_split = False
            box_78D4A.use_property_decorate = False
            box_78D4A.alignment = 'Expand'.upper()
            box_78D4A.scale_x = 1.0
            box_78D4A.scale_y = 1.0
            if not True: box_78D4A.operator_context = "EXEC_DEFAULT"
            if (bpy.context.scene.view_settings.view_transform != 'Standard'):
                box_78D4A.label(text='Standard gives most accurate colours', icon_value=0)
            split_9EFC9 = box_78D4A.split(factor=0.5111111402511597, align=False)
            split_9EFC9.alert = False
            split_9EFC9.enabled = True
            split_9EFC9.active = True
            split_9EFC9.use_property_split = False
            split_9EFC9.use_property_decorate = False
            split_9EFC9.scale_x = 1.0
            split_9EFC9.scale_y = 1.0
            split_9EFC9.alignment = 'Expand'.upper()
            if not True: split_9EFC9.operator_context = "EXEC_DEFAULT"
            split_9EFC9.label(text='View Transform', icon_value=0)
            split_9EFC9.prop(bpy.context.scene.view_settings, 'view_transform', text='', icon_value=0, emboss=True)
            split_568C6 = box_78D4A.split(factor=0.5111111402511597, align=False)
            split_568C6.alert = False
            split_568C6.enabled = True
            split_568C6.active = True
            split_568C6.use_property_split = False
            split_568C6.use_property_decorate = False
            split_568C6.scale_x = 1.0
            split_568C6.scale_y = 1.0
            split_568C6.alignment = 'Expand'.upper()
            if not True: split_568C6.operator_context = "EXEC_DEFAULT"
            split_568C6.label(text='Look', icon_value=0)
            split_568C6.prop(bpy.context.scene.view_settings, 'look', text='', icon_value=0, emboss=True)
            col_32C11.prop(bpy.context.scene.eevee, 'taa_render_samples', text='Samples', icon_value=0, emboss=True)
            if (bpy.context.scene.eevee.taa_render_samples < 65):
                box_6E405 = col_32C11.box()
                box_6E405.alert = True
                box_6E405.enabled = True
                box_6E405.active = True
                box_6E405.use_property_split = False
                box_6E405.use_property_decorate = False
                box_6E405.alignment = 'Expand'.upper()
                box_6E405.scale_x = 1.0
                box_6E405.scale_y = 1.0
                if not True: box_6E405.operator_context = "EXEC_DEFAULT"
                box_6E405.label(text='Use higher samples for less noise', icon_value=0)
            col_32C11.prop(bpy.context.scene.render.image_settings, 'file_format', text='', icon_value=0, emboss=True)
            if (bpy.context.scene.render.image_settings.file_format == 'FFMPEG'):
                box_7B61F = col_32C11.box()
                box_7B61F.alert = True
                box_7B61F.enabled = True
                box_7B61F.active = True
                box_7B61F.use_property_split = False
                box_7B61F.use_property_decorate = False
                box_7B61F.alignment = 'Expand'.upper()
                box_7B61F.scale_x = 1.0
                box_7B61F.scale_y = 1.0
                if not True: box_7B61F.operator_context = "EXEC_DEFAULT"
                box_7B61F.label(text='Use an image format', icon_value=0)
            else:
                box_41BC0 = col_32C11.box()
                box_41BC0.alert = False
                box_41BC0.enabled = True
                box_41BC0.active = True
                box_41BC0.use_property_split = False
                box_41BC0.use_property_decorate = False
                box_41BC0.alignment = 'Expand'.upper()
                box_41BC0.scale_x = 1.0
                box_41BC0.scale_y = 1.0
                if not True: box_41BC0.operator_context = "EXEC_DEFAULT"
                op = box_41BC0.operator('sna.dgs_render_offline_aea04', text='Render Offline (Image)', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'images-7391277-white.png')), emboss=True, depress=False)
                op.sna_render_animation = False
                op = box_41BC0.operator('sna.dgs_render_offline_aea04', text='Render Offline (Animation)', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'movie-7390465-white.png')), emboss=True, depress=False)
                op.sna_render_animation = True


class SNA_OT_Dgs_Render_Offline_Aea04(bpy.types.Operator):
    bl_idname = "sna.dgs_render_offline_aea04"
    bl_label = "3DGS Render Offline"
    bl_description = "Sets all 3DGS objects to 'active camera' and offline renders using current render settings."
    bl_options = {"REGISTER", "UNDO"}
    sna_render_animation: bpy.props.BoolProperty(name='Render Animation', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.area.spaces.active.region_3d.view_perspective = 'CAMERA'
        bpy.ops.view3d.zoom_camera_1_to_1('INVOKE_DEFAULT', )
        for i_2F11D in range(len(bpy.data.objects)):
            if (property_exists("bpy.data.objects[i_2F11D].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.data.objects[i_2F11D].modifiers):
                bpy.data.objects[i_2F11D].sna_kiri3dgs_active_object_enable_active_camera = True
                bpy.data.objects[i_2F11D].modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = True

        def delayed_82CC3():
            sna_dgs__update_camera_single_time_function_execute_9C695()

            def delayed_B5B65():
                bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
                if bpy.context and bpy.context.screen:
                    for a in bpy.context.screen.areas:
                        a.tag_redraw()
                scene_name = bpy.context.scene.name
                output_path = bpy.context.scene.render.filepath
                output_filename = os.path.basename(bpy.context.scene.render.filepath)
                file_format = bpy.context.scene.render.image_settings.file_format
                resolution_x = bpy.context.scene.render.resolution_x
                resolution_y = bpy.context.scene.render.resolution_y
                render_quality = None
                render_engine = bpy.context.scene.render.engine
                samples = bpy.context.scene.eevee.taa_render_samples
                resolution_percentage = bpy.context.scene.render.resolution_percentage
                render_animation = self.sna_render_animation
                offline_render = True
                # Define input variables for rendering options
                #scene_name = bpy.data.scenes["Scene"].get("scene_name", "Scene")  # Default scene name
                #output_path = bpy.data.scenes[scene_name].get("output_path", "//")  # Default to current blend file directory
                #output_filename = bpy.data.scenes[scene_name].get("output_filename", "render")
                #file_format = bpy.data.scenes[scene_name].get("file_format", "PNG")
                #resolution_x = bpy.data.scenes[scene_name].get("resolution_x", 1920)
                #resolution_y = bpy.data.scenes[scene_name].get("resolution_y", 1080)
                render_quality = bpy.data.scenes[scene_name].get("render_quality", 100)
                #render_engine = bpy.data.scenes[scene_name].get("render_engine", "CYCLES")
                #samples = bpy.data.scenes[scene_name].get("samples", 128)
                #resolution_percentage = bpy.data.scenes[scene_name].get("resolution_percentage", 100)
                #render_animation = bpy.data.scenes[scene_name].get("render_animation", False)
                #offline_render = bpy.data.scenes[scene_name].get("offline_render", True)  # Boolean for offline rendering
                # Set the active scene
                scene = bpy.data.scenes[scene_name]
                # Ensure the output path is resolved properly
                output_path = bpy.path.abspath(output_path)  # Resolve the absolute path
                scene.render.filepath = os.path.join(output_path, output_filename)
                # Set render settings
                scene.render.image_settings.file_format = file_format
                scene.render.resolution_x = resolution_x
                scene.render.resolution_y = resolution_y
                scene.render.resolution_percentage = resolution_percentage
                if file_format == 'JPEG':
                    scene.render.image_settings.quality = render_quality
                # Set the render engine and samples
                scene.render.engine = render_engine
                if render_engine == 'CYCLES':
                    scene.cycles.samples = samples
                elif render_engine == 'BLENDER_EEVEE':
                    scene.eevee.taa_samples = samples  # Set samples for Eevee
                # Print all render properties for debugging
                print("Render Properties:")
                print(f"Resolved Output Path: {output_path}")
                print(f"Output Filename: {output_filename}.{file_format.lower()}")
                print(f"File Format: {file_format}")
                print(f"Resolution: {resolution_x}x{resolution_y}")
                print(f"Resolution Percentage: {resolution_percentage}%")
                print(f"Render Quality: {render_quality}")
                print(f"Render Engine: {render_engine}")
                print(f"Samples: {samples}")
                print(f"Render Animation: {render_animation}")
                print(f"Offline Render: {offline_render}")
                # Set offline rendering option
                if offline_render:
                    print("Rendering in offline mode.")
                else:
                    print("Rendering in online mode.")
                # Render the scene
                if render_animation:
                    bpy.ops.render.render(animation=True)  # Render the animation
                else:
                    bpy.ops.render.render(write_still=True)  # Render a single frame
                print("Rendering initiated. Please wait for completion.")
            bpy.app.timers.register(delayed_B5B65, first_interval=0.10000000149011612)
        bpy.app.timers.register(delayed_82CC3, first_interval=0.10000000149011612)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_C3AA8 = layout.box()
        box_C3AA8.alert = True
        box_C3AA8.enabled = True
        box_C3AA8.active = True
        box_C3AA8.use_property_split = False
        box_C3AA8.use_property_decorate = False
        box_C3AA8.alignment = 'Expand'.upper()
        box_C3AA8.scale_x = 1.0
        box_C3AA8.scale_y = 1.0
        if not True: box_C3AA8.operator_context = "EXEC_DEFAULT"
        box_C3AA8.label(text="All available objects will be set to use 'Active Camera'", icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'info-3016385-white.png')))
        box_C3AA8.label(text='        To cancel rendering - force close Blender', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


def sna_active_object_shading_function_interface_3A6A5(layout_function, ):
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
    box_E0430.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[2], 'default_value', text='Shadeless', icon_value=0, emboss=True, toggle=True)
    if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[2].default_value:
        pass
    else:
        box_1833D = col_EB8EB.box()
        box_1833D.alert = False
        box_1833D.enabled = True
        box_1833D.active = True
        box_1833D.use_property_split = False
        box_1833D.use_property_decorate = False
        box_1833D.alignment = 'Expand'.upper()
        box_1833D.scale_x = 1.0
        box_1833D.scale_y = 1.0
        if not True: box_1833D.operator_context = "EXEC_DEFAULT"
        box_1833D.prop(bpy.context.view_layer.objects.active.active_material, 'sna_kiri3dgs_shading_bsdf_settings', text='Adjust BSDF Shader', icon_value=0, emboss=True, toggle=True)
        if bpy.context.view_layer.objects.active.active_material.sna_kiri3dgs_shading_bsdf_settings:
            box_E16AF = box_1833D.box()
            box_E16AF.alert = False
            box_E16AF.enabled = True
            box_E16AF.active = True
            box_E16AF.use_property_split = False
            box_E16AF.use_property_decorate = False
            box_E16AF.alignment = 'Expand'.upper()
            box_E16AF.scale_x = 1.0
            box_E16AF.scale_y = 1.0
            if not True: box_E16AF.operator_context = "EXEC_DEFAULT"
            box_E16AF.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[31], 'default_value', text='Metallic', icon_value=0, emboss=True)
            box_E16AF.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[32], 'default_value', text='Roughness', icon_value=0, emboss=True)
            box_E16AF.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[33], 'default_value', text='Emission Strength', icon_value=0, emboss=True)
            box_E16AF.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[34], 'default_value', text='Specular IOR', icon_value=0, emboss=True)
            box_E16AF.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[35], 'default_value', text='Specular Tint', icon_value=0, emboss=True)
    box_4DBC0 = col_EB8EB.box()
    box_4DBC0.alert = False
    box_4DBC0.enabled = True
    box_4DBC0.active = True
    box_4DBC0.use_property_split = False
    box_4DBC0.use_property_decorate = False
    box_4DBC0.alignment = 'Expand'.upper()
    box_4DBC0.scale_x = 1.0
    box_4DBC0.scale_y = 1.0
    if not True: box_4DBC0.operator_context = "EXEC_DEFAULT"
    box_4DBC0.prop(bpy.context.view_layer.objects.active.active_material, 'sna_kiri3dgs_shading_base_colour_adjustments', text='Base Colour Adjustments', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.active_material.sna_kiri3dgs_shading_base_colour_adjustments:
        box_47A8F = box_4DBC0.box()
        box_47A8F.alert = False
        box_47A8F.enabled = True
        box_47A8F.active = True
        box_47A8F.use_property_split = False
        box_47A8F.use_property_decorate = False
        box_47A8F.alignment = 'Expand'.upper()
        box_47A8F.scale_x = 1.0
        box_47A8F.scale_y = 1.0
        if not True: box_47A8F.operator_context = "EXEC_DEFAULT"
        box_47A8F.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[3], 'default_value', text='Brightness', icon_value=0, emboss=True)
        box_47A8F.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[4], 'default_value', text='Contrast', icon_value=0, emboss=True)
        box_47A8F.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[5], 'default_value', text='Hue', icon_value=0, emboss=True)
        box_47A8F.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[6], 'default_value', text='Saturation', icon_value=0, emboss=True)
    box_0E797 = col_EB8EB.box()
    box_0E797.alert = False
    box_0E797.enabled = True
    box_0E797.active = True
    box_0E797.use_property_split = False
    box_0E797.use_property_decorate = False
    box_0E797.alignment = 'Expand'.upper()
    box_0E797.scale_x = 1.0
    box_0E797.scale_y = 1.0
    if not True: box_0E797.operator_context = "EXEC_DEFAULT"
    box_0E797.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[28], 'default_value', text='White Balance', icon_value=0, emboss=True, toggle=True)
    if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[28].default_value:
        box_C0880 = box_0E797.box()
        box_C0880.alert = False
        box_C0880.enabled = True
        box_C0880.active = True
        box_C0880.use_property_split = False
        box_C0880.use_property_decorate = False
        box_C0880.alignment = 'Expand'.upper()
        box_C0880.scale_x = 1.0
        box_C0880.scale_y = 1.0
        if not True: box_C0880.operator_context = "EXEC_DEFAULT"
        box_C0880.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[29], 'default_value', text='Temperature', icon_value=0, emboss=True)
        box_C0880.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[30], 'default_value', text='Tint', icon_value=0, emboss=True)
    box_FB221 = col_EB8EB.box()
    box_FB221.alert = False
    box_FB221.enabled = True
    box_FB221.active = True
    box_FB221.use_property_split = False
    box_FB221.use_property_decorate = False
    box_FB221.alignment = 'Expand'.upper()
    box_FB221.scale_x = 1.0
    box_FB221.scale_y = 1.0
    if not True: box_FB221.operator_context = "EXEC_DEFAULT"
    box_FB221.prop(bpy.context.view_layer.objects.active.active_material, 'sna_kiri3dgs_shading_colour_masks', text='Colour Masks', icon_value=0, emboss=True, toggle=True)
    if bpy.context.view_layer.objects.active.active_material.sna_kiri3dgs_shading_colour_masks:
        box_81155 = box_FB221.box()
        box_81155.alert = False
        box_81155.enabled = True
        box_81155.active = True
        box_81155.use_property_split = False
        box_81155.use_property_decorate = False
        box_81155.alignment = 'Expand'.upper()
        box_81155.scale_x = 1.0
        box_81155.scale_y = 1.0
        if not True: box_81155.operator_context = "EXEC_DEFAULT"
        box_81155.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[7], 'default_value', text='Enable Colour Mask 1', icon_value=0, emboss=True, toggle=True)
        if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[7].default_value:
            col_B3736 = box_81155.column(heading='', align=False)
            col_B3736.alert = False
            col_B3736.enabled = True
            col_B3736.active = True
            col_B3736.use_property_split = False
            col_B3736.use_property_decorate = False
            col_B3736.scale_x = 1.0
            col_B3736.scale_y = 1.0
            col_B3736.alignment = 'Expand'.upper()
            col_B3736.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_B3736.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[8], 'default_value', text='Colour Selection', icon_value=0, emboss=True)
            col_B3736.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[9], 'default_value', text='Change To', icon_value=0, emboss=True)
            col_B3736.prop(bpy.data.node_groups[('3DGS_HQ_Render_Material_Main_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Material_Main_Shader')].nodes['Mask 1 Change Method'], 'blend_type', text='', icon_value=0, emboss=True)
            col_B3736.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[10], 'default_value', text='Mix Factor', icon_value=0, emboss=True)
            col_B3736.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[11], 'default_value', text='Hue Threshold', icon_value=0, emboss=True)
            col_B3736.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[12], 'default_value', text='Saturation Threshold', icon_value=0, emboss=True)
            col_B3736.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[13], 'default_value', text='Value Threshold', icon_value=0, emboss=True)
    if bpy.context.view_layer.objects.active.active_material.sna_kiri3dgs_shading_colour_masks:
        box_EFA39 = box_FB221.box()
        box_EFA39.alert = False
        box_EFA39.enabled = True
        box_EFA39.active = True
        box_EFA39.use_property_split = False
        box_EFA39.use_property_decorate = False
        box_EFA39.alignment = 'Expand'.upper()
        box_EFA39.scale_x = 1.0
        box_EFA39.scale_y = 1.0
        if not True: box_EFA39.operator_context = "EXEC_DEFAULT"
        box_EFA39.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[14], 'default_value', text='Enable Colour Mask 2', icon_value=0, emboss=True, toggle=True)
        if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[14].default_value:
            col_F841E = box_EFA39.column(heading='', align=False)
            col_F841E.alert = False
            col_F841E.enabled = True
            col_F841E.active = True
            col_F841E.use_property_split = False
            col_F841E.use_property_decorate = False
            col_F841E.scale_x = 1.0
            col_F841E.scale_y = 1.0
            col_F841E.alignment = 'Expand'.upper()
            col_F841E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_F841E.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[15], 'default_value', text='Colour Selection', icon_value=0, emboss=True)
            col_F841E.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[16], 'default_value', text='Change To', icon_value=0, emboss=True)
            col_F841E.prop(bpy.data.node_groups[('3DGS_HQ_Render_Material_Main_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Material_Main_Shader')].nodes['Mask 2 Change Method'], 'blend_type', text='', icon_value=0, emboss=True)
            col_F841E.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[17], 'default_value', text='Mix Factor', icon_value=0, emboss=True)
            col_F841E.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[18], 'default_value', text='Hue Threshold', icon_value=0, emboss=True)
            col_F841E.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[19], 'default_value', text='Saturation Threshold', icon_value=0, emboss=True)
            col_F841E.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[20], 'default_value', text='Value Threshold', icon_value=0, emboss=True)
    if bpy.context.view_layer.objects.active.active_material.sna_kiri3dgs_shading_colour_masks:
        box_57787 = box_FB221.box()
        box_57787.alert = False
        box_57787.enabled = True
        box_57787.active = True
        box_57787.use_property_split = False
        box_57787.use_property_decorate = False
        box_57787.alignment = 'Expand'.upper()
        box_57787.scale_x = 1.0
        box_57787.scale_y = 1.0
        if not True: box_57787.operator_context = "EXEC_DEFAULT"
        box_57787.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[21], 'default_value', text='Enable Colour Mask 3', icon_value=0, emboss=True, toggle=True)
        if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[21].default_value:
            col_0A843 = box_57787.column(heading='', align=False)
            col_0A843.alert = False
            col_0A843.enabled = True
            col_0A843.active = True
            col_0A843.use_property_split = False
            col_0A843.use_property_decorate = False
            col_0A843.scale_x = 1.0
            col_0A843.scale_y = 1.0
            col_0A843.alignment = 'Expand'.upper()
            col_0A843.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_0A843.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[22], 'default_value', text='Colour Selection', icon_value=0, emboss=True)
            col_0A843.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[23], 'default_value', text='Change To', icon_value=0, emboss=True)
            col_0A843.prop(bpy.data.node_groups[('3DGS_HQ_Render_Material_Main_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Material_Main_Shader')].nodes['Mask 3 Change Method'], 'blend_type', text='', icon_value=0, emboss=True)
            col_0A843.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[24], 'default_value', text='Mix Factor', icon_value=0, emboss=True)
            col_0A843.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[25], 'default_value', text='Hue Threshold', icon_value=0, emboss=True)
            col_0A843.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[26], 'default_value', text='Saturation Threshold', icon_value=0, emboss=True)
            col_0A843.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[27], 'default_value', text='Value Threshold', icon_value=0, emboss=True)
    if 'OmniviewAngle' in bpy.context.view_layer.objects.active:
        box_162DF = col_EB8EB.box()
        box_162DF.alert = False
        box_162DF.enabled = True
        box_162DF.active = True
        box_162DF.use_property_split = False
        box_162DF.use_property_decorate = False
        box_162DF.alignment = 'Expand'.upper()
        box_162DF.scale_x = 1.0
        box_162DF.scale_y = 1.0
        if not True: box_162DF.operator_context = "EXEC_DEFAULT"
        attr_54DC4 = '["' + str('OmniviewAngle' + '"]') 
        box_162DF.prop(bpy.context.view_layer.objects.active, attr_54DC4, text='View Angle Threshold', icon_value=0, emboss=True, toggle=True)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Set_Material_GN' in bpy.context.view_layer.objects.active.modifiers):
        box_18DD9 = col_EB8EB.box()
        box_18DD9.alert = False
        box_18DD9.enabled = True
        box_18DD9.active = True
        box_18DD9.use_property_split = False
        box_18DD9.use_property_decorate = False
        box_18DD9.alignment = 'Expand'.upper()
        box_18DD9.scale_x = 1.0
        box_18DD9.scale_y = 1.0
        if not True: box_18DD9.operator_context = "EXEC_DEFAULT"
        attr_787E3 = '["' + str('Socket_3' + '"]') 
        box_18DD9.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Set_Material_GN'], attr_787E3, text='Create Extra Attributes', icon_value=0, emboss=True, toggle=True)


class SNA_PT_DGS_RENDER__ABOUT__LINKS_PANEL_CC2AC(bpy.types.Panel):
    bl_label = '3DGS Render - About / Links Panel'
    bl_idname = 'SNA_PT_DGS_RENDER__ABOUT__LINKS_PANEL_CC2AC'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 3
    bl_options = {'HIDE_HEADER'}
    bl_parent_id = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_F216E'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.label(text='--- About KIRI Engine ---', icon_value=0)
        layout.separator(factor=1.0)
        box_98A33 = layout.box()
        box_98A33.alert = False
        box_98A33.enabled = True
        box_98A33.active = True
        box_98A33.use_property_split = False
        box_98A33.use_property_decorate = False
        box_98A33.alignment = 'Expand'.upper()
        box_98A33.scale_x = 1.0
        box_98A33.scale_y = 0.800000011920929
        if not True: box_98A33.operator_context = "EXEC_DEFAULT"
        col_F48EE = box_98A33.column(heading='', align=False)
        col_F48EE.alert = False
        col_F48EE.enabled = True
        col_F48EE.active = True
        col_F48EE.use_property_split = False
        col_F48EE.use_property_decorate = False
        col_F48EE.scale_x = 1.0
        col_F48EE.scale_y = 1.0
        col_F48EE.alignment = 'Expand'.upper()
        col_F48EE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_F48EE.label(text="We're the creators of KIRI Engine, a 3D ", icon_value=0)
        col_F48EE.label(text='scanning app on iPhone, Android and web', icon_value=0)
        col_F48EE.label(text="browsers. When we're not coding, we", icon_value=0)
        col_F48EE.label(text='enjoy messing around with 3D models in', icon_value=0)
        col_F48EE.label(text='Blender. We are excited to share these', icon_value=0)
        col_F48EE.label(text='cool add-ons with you, so you can join', icon_value=0)
        col_F48EE.label(text='in the fun too!', icon_value=0)
        op = layout.operator('sna.launch_blender_market_77f72', text='See All Addons On Blender Market', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.launch_kiri_site_d26bf', text='Learn More About KIRI Engine', icon_value=0, emboss=True, depress=False)


class SNA_PT_DGS_RENDER__DOCUMENTATION_PANEL_21E93(bpy.types.Panel):
    bl_label = '3DGS Render - Documentation Panel'
    bl_idname = 'SNA_PT_DGS_RENDER__DOCUMENTATION_PANEL_21E93'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 2
    bl_options = {'HIDE_HEADER'}
    bl_parent_id = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_F216E'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        box_BDECD = layout.box()
        box_BDECD.alert = False
        box_BDECD.enabled = True
        box_BDECD.active = True
        box_BDECD.use_property_split = False
        box_BDECD.use_property_decorate = False
        box_BDECD.alignment = 'Expand'.upper()
        box_BDECD.scale_x = 1.0
        box_BDECD.scale_y = 1.0
        if not True: box_BDECD.operator_context = "EXEC_DEFAULT"
        op = box_BDECD.operator('sna.open_blender_splat_render_documentation_1eac5', text='Documentation', icon_value=0, emboss=True, depress=False)
        op = box_BDECD.operator('sna.open_blender_splat_render_tutorial_video_a4fe6', text='Tutorial Video', icon_value=0, emboss=True, depress=False)


class SNA_PT_DGS_RENDER__MAIN_FUNCTION_PANEL_2675E(bpy.types.Panel):
    bl_label = '3DGS Render - Main Function Panel'
    bl_idname = 'SNA_PT_DGS_RENDER__MAIN_FUNCTION_PANEL_2675E'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 1
    bl_options = {'HIDE_HEADER'}
    bl_parent_id = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_F216E'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        box_BDC6F = layout.box()
        box_BDC6F.alert = False
        box_BDC6F.enabled = True
        box_BDC6F.active = True
        box_BDC6F.use_property_split = False
        box_BDC6F.use_property_decorate = False
        box_BDC6F.alignment = 'Expand'.upper()
        box_BDC6F.scale_x = 1.0
        box_BDC6F.scale_y = 1.0
        if not True: box_BDC6F.operator_context = "EXEC_DEFAULT"
        if (bpy.context.scene.render.engine == 'BLENDER_EEVEE_NEXT'):
            col_23FAF = box_BDC6F.column(heading='', align=False)
            col_23FAF.alert = False
            col_23FAF.enabled = True
            col_23FAF.active = True
            col_23FAF.use_property_split = False
            col_23FAF.use_property_decorate = False
            col_23FAF.scale_x = 1.0
            col_23FAF.scale_y = 1.0
            col_23FAF.alignment = 'Expand'.upper()
            col_23FAF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            layout_function = col_23FAF
            sna_camera_update_mode_function_interface_B961D(layout_function, )
            col_23FAF.separator(factor=1.0)
            col_0E928 = col_23FAF.column(heading='', align=False)
            col_0E928.alert = False
            col_0E928.enabled = True
            col_0E928.active = True
            col_0E928.use_property_split = False
            col_0E928.use_property_decorate = False
            col_0E928.scale_x = 1.0
            col_0E928.scale_y = 1.0
            col_0E928.alignment = 'Expand'.upper()
            col_0E928.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                if 'update_rot_to_cam' in bpy.context.view_layer.objects.active:
                    box_0C863 = col_0E928.box()
                    box_0C863.alert = False
                    box_0C863.enabled = True
                    box_0C863.active = True
                    box_0C863.use_property_split = False
                    box_0C863.use_property_decorate = False
                    box_0C863.alignment = 'Expand'.upper()
                    box_0C863.scale_x = 1.0
                    box_0C863.scale_y = 1.0
                    if not True: box_0C863.operator_context = "EXEC_DEFAULT"
                    layout_function = box_0C863
                    sna_active_object_camera_update_interface_func_9588F(layout_function, )
            col_23FAF.separator(factor=1.0)
            box_2356A = col_23FAF.box()
            box_2356A.alert = False
            box_2356A.enabled = True
            box_2356A.active = True
            box_2356A.use_property_split = False
            box_2356A.use_property_decorate = False
            box_2356A.alignment = 'Expand'.upper()
            box_2356A.scale_x = 1.0
            box_2356A.scale_y = 1.0
            if not True: box_2356A.operator_context = "EXEC_DEFAULT"
            box_2356A.label(text='Active Mode', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
            col_63AF5 = box_2356A.column(heading='', align=False)
            col_63AF5.alert = True
            col_63AF5.enabled = True
            col_63AF5.active = True
            col_63AF5.use_property_split = False
            col_63AF5.use_property_decorate = False
            col_63AF5.scale_x = 1.0
            col_63AF5.scale_y = 1.0
            col_63AF5.alignment = 'Expand'.upper()
            col_63AF5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_63AF5.prop(bpy.context.scene, 'sna_kiri3dgs_interface_active_mode', text='', icon_value=0, emboss=True)
            col_23FAF.separator(factor=1.0)
            col_657C5 = col_23FAF.column(heading='', align=False)
            col_657C5.alert = False
            col_657C5.enabled = True
            col_657C5.active = True
            col_657C5.use_property_split = False
            col_657C5.use_property_decorate = False
            col_657C5.scale_x = 1.0
            col_657C5.scale_y = 1.0
            col_657C5.alignment = 'Expand'.upper()
            col_657C5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.scene.sna_kiri3dgs_interface_active_mode == 'Import 3DGS'):
                box_2936D = col_657C5.box()
                box_2936D.alert = False
                box_2936D.enabled = True
                box_2936D.active = True
                box_2936D.use_property_split = False
                box_2936D.use_property_decorate = False
                box_2936D.alignment = 'Expand'.upper()
                box_2936D.scale_x = 1.0
                box_2936D.scale_y = 1.0
                if not True: box_2936D.operator_context = "EXEC_DEFAULT"
                layout_function = box_2936D
                sna_import_ply_as_splats_function_interface_94FB1(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_mode == 'Import/Edit Point Cloud'):
                box_14803 = col_657C5.box()
                box_14803.alert = False
                box_14803.enabled = True
                box_14803.active = True
                box_14803.use_property_split = False
                box_14803.use_property_decorate = False
                box_14803.alignment = 'Expand'.upper()
                box_14803.scale_x = 1.0
                box_14803.scale_y = 1.0
                if not True: box_14803.operator_context = "EXEC_DEFAULT"
                layout_function = box_14803
                sna_edit_points_function_interface_906CF(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_mode == 'Shading'):
                if (bpy.context.view_layer.objects.active == None):
                    box_6E7D7 = col_657C5.box()
                    box_6E7D7.alert = True
                    box_6E7D7.enabled = True
                    box_6E7D7.active = True
                    box_6E7D7.use_property_split = False
                    box_6E7D7.use_property_decorate = False
                    box_6E7D7.alignment = 'Expand'.upper()
                    box_6E7D7.scale_x = 1.0
                    box_6E7D7.scale_y = 1.0
                    if not True: box_6E7D7.operator_context = "EXEC_DEFAULT"
                    box_6E7D7.label(text='No active object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                else:
                    if ((property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_Render_Material' in bpy.context.view_layer.objects.active.material_slots) or (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and '3DGS_HQ_Render_Shader' in bpy.context.view_layer.objects.active.material_slots)):
                        box_F79C3 = col_657C5.box()
                        box_F79C3.alert = False
                        box_F79C3.enabled = True
                        box_F79C3.active = True
                        box_F79C3.use_property_split = False
                        box_F79C3.use_property_decorate = False
                        box_F79C3.alignment = 'Expand'.upper()
                        box_F79C3.scale_x = 1.0
                        box_F79C3.scale_y = 1.0
                        if not True: box_F79C3.operator_context = "EXEC_DEFAULT"
                        layout_function = box_F79C3
                        sna_active_object_shading_function_interface_3A6A5(layout_function, )
                    else:
                        box_5182E = col_657C5.box()
                        box_5182E.alert = True
                        box_5182E.enabled = True
                        box_5182E.active = True
                        box_5182E.use_property_split = False
                        box_5182E.use_property_decorate = False
                        box_5182E.alignment = 'Expand'.upper()
                        box_5182E.scale_x = 1.0
                        box_5182E.scale_y = 1.0
                        if not True: box_5182E.operator_context = "EXEC_DEFAULT"
                        box_5182E.label(text='Required material missing', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
            if (bpy.context.scene.sna_kiri3dgs_interface_active_mode == 'Modify - Edit'):
                box_12977 = col_657C5.box()
                box_12977.alert = False
                box_12977.enabled = True
                box_12977.active = True
                box_12977.use_property_split = False
                box_12977.use_property_decorate = False
                box_12977.alignment = 'Expand'.upper()
                box_12977.scale_x = 1.0
                box_12977.scale_y = 1.0
                if not True: box_12977.operator_context = "EXEC_DEFAULT"
                layout_function = box_12977
                sna_modify_edit_function_interface_AEA26(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_mode == 'Modify - Animate'):
                box_9B663 = col_657C5.box()
                box_9B663.alert = False
                box_9B663.enabled = True
                box_9B663.active = True
                box_9B663.use_property_split = False
                box_9B663.use_property_decorate = False
                box_9B663.alignment = 'Expand'.upper()
                box_9B663.scale_x = 1.0
                box_9B663.scale_y = 1.0
                if not True: box_9B663.operator_context = "EXEC_DEFAULT"
                layout_function = box_9B663
                sna_modify_animate_function_interface_57F9E(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_mode == 'Render'):
                box_F9B36 = col_657C5.box()
                box_F9B36.alert = False
                box_F9B36.enabled = True
                box_F9B36.active = True
                box_F9B36.use_property_split = False
                box_F9B36.use_property_decorate = False
                box_F9B36.alignment = 'Expand'.upper()
                box_F9B36.scale_x = 1.0
                box_F9B36.scale_y = 1.0
                if not True: box_F9B36.operator_context = "EXEC_DEFAULT"
                layout_function = box_F9B36
                sna_render_function_interface_C67EB(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_mode == 'HQ Render'):
                box_4FE9F = col_657C5.box()
                box_4FE9F.alert = False
                box_4FE9F.enabled = True
                box_4FE9F.active = True
                box_4FE9F.use_property_split = False
                box_4FE9F.use_property_decorate = False
                box_4FE9F.alignment = 'Expand'.upper()
                box_4FE9F.scale_x = 1.0
                box_4FE9F.scale_y = 1.0
                if not True: box_4FE9F.operator_context = "EXEC_DEFAULT"
                layout_function = box_4FE9F
                sna_hq_render_function_interface_17C41(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_mode == 'Omniview Object (Experimental)'):
                box_00D6C = col_657C5.box()
                box_00D6C.alert = False
                box_00D6C.enabled = True
                box_00D6C.active = True
                box_00D6C.use_property_split = False
                box_00D6C.use_property_decorate = False
                box_00D6C.alignment = 'Expand'.upper()
                box_00D6C.scale_x = 1.0
                box_00D6C.scale_y = 1.0
                if not True: box_00D6C.operator_context = "EXEC_DEFAULT"
                layout_function = box_00D6C
                sna_omnisplat_function_interface_E1B70(layout_function, )
        else:
            layout_function = box_BDC6F
            sna_enable_eevee_function_interface_891B1(layout_function, )


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_kiri3dgs_interface_active_mode = bpy.props.EnumProperty(name='KIRI3DGS Interface Active Mode', description='', items=[('Import 3DGS', 'Import 3DGS', '', 0, 0), ('Import/Edit Point Cloud', 'Import/Edit Point Cloud', '', 0, 1), ('Modify - Edit', 'Modify - Edit', '', 0, 2), ('Shading', 'Shading', '', 0, 3), ('Modify - Animate', 'Modify - Animate', '', 0, 4), ('Render', 'Render', '', 0, 5), ('HQ Render', 'HQ Render', '', 0, 6), ('Omniview Object (Experimental)', 'Omniview Object (Experimental)', '', 0, 7)])
    bpy.types.Scene.sna_kiri3dgs_scene_camera_refresh_mode = bpy.props.EnumProperty(name='KIRI3DGS Scene Camera Refresh Mode', description='', items=[('Continuous', 'Continuous', '', 0, 0), ('Frame Change', 'Frame Change', '', 0, 1)])
    bpy.types.Object.sna_kiri3dgs_active_object_update_mode = bpy.props.EnumProperty(name='KIRI3DGS Active Object Update Mode', description='', items=[('Enable Camera Updates', 'Enable Camera Updates', '', 0, 0), ('Disable Camera Updates', 'Disable Camera Updates', '', 0, 1), ('Show As Point Cloud', 'Show As Point Cloud', '', 0, 2)], update=sna_update_sna_kiri3dgs_active_object_update_mode_868D4)
    bpy.types.Object.sna_kiri3dgs_active_object_enable_active_camera = bpy.props.BoolProperty(name='KIRI3DGS Active Object Enable Active Camera', description='', default=False, update=sna_update_sna_kiri3dgs_active_object_enable_active_camera_DE26E)
    bpy.types.Material.sna_kiri3dgs_shading_base_colour_adjustments = bpy.props.BoolProperty(name='KIRI3DGS Shading Base Colour Adjustments', description='', default=False)
    bpy.types.Material.sna_kiri3dgs_shading_colour_masks = bpy.props.BoolProperty(name='KIRI3DGS Shading Colour Masks', description='', default=False)
    bpy.types.Material.sna_kiri3dgs_shading_bsdf_settings = bpy.props.BoolProperty(name='KIRI3DGS Shading BSDF Settings', description='', default=False)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_decimate = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Decimate', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_decimate_641A7)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_camera_cull = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Camera Cull', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_camera_cull_A98D6)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_crop_box = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Crop Box', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_crop_box_6FCA7)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_colour_edit = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Colour Edit', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_colour_edit_1D6A1)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_remove_stray = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Remove Stray', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_remove_stray_488C9)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_animate = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Animate', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_animate_1F5D0)
    bpy.types.Scene.sna_kiri3dgs_omnisplat_axes_count = bpy.props.EnumProperty(name='KIRI3DGS Omnisplat Axes Count', description='', items=[('3 Axes', '3 Axes', '', 0, 0), ('5 Axes', '5 Axes', '', 0, 1), ('7 Axes', '7 Axes', '', 0, 2), ('9 Axes', '9 Axes', '', 0, 3)])
    bpy.utils.register_class(SNA_OT_Launch_Kiri_Site_D26Bf)
    bpy.utils.register_class(SNA_OT_Launch_Blender_Market_77F72)
    bpy.utils.register_class(SNA_OT_Apply_3Dgs_Modifiers_E67A2)
    bpy.utils.register_class(SNA_OT_Align_Active_To_X_Axis_9B12E)
    bpy.utils.register_class(SNA_OT_Align_Active_To_Y_Axis_9Bd1F)
    bpy.utils.register_class(SNA_OT_Align_Active_To_Z_Axis_720A9)
    bpy.utils.register_class(SNA_OT_Align_Active_To_View_88E3A)
    bpy.utils.register_class(SNA_OT_Dgs__Start_Camera_Update_001Bd)
    bpy.utils.register_class(SNA_OT_Dgs__Stop_Camera_Update_88568)
    bpy.utils.register_class(SNA_OT_Dgs__Update_Camera_Single_Time_03530)
    bpy.app.handlers.load_pre.append(load_pre_handler_F6F13)
    bpy.utils.register_class(SNA_OT_Open_Blender_Splat_Render_Documentation_1Eac5)
    bpy.utils.register_class(SNA_OT_Open_Blender_Splat_Render_Tutorial_Video_A4Fe6)
    bpy.utils.register_class(SNA_OT_Import_Ply_As_Points_E9E21)
    bpy.utils.register_class(SNA_OT_Remove_Point_Edit_Modifier_47851)
    bpy.utils.register_class(SNA_OT_Refresh_Point_Edit_Modifier_Ec829)
    bpy.utils.register_class(SNA_OT_Append_Point_Edit_Modifier_A0188)
    bpy.utils.register_class(SNA_OT_Export_Points_For_3Dgs_63Cd8)
    bpy.utils.register_class(SNA_OT_Apply_Point_Edit_Modifier_D6B08)
    bpy.utils.register_class(SNA_OT_Hq_Render_B89Bf)
    bpy.utils.register_class(SNA_OT_Import_Ply_As_Splats_8458E)
    bpy.utils.register_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_F216E)
    bpy.utils.register_class(SNA_OT_Set_Render_Engine_To_Eevee_D73Ee)
    bpy.utils.register_class(SNA_OT_Remove_Animate_Modifier_5B34D)
    bpy.utils.register_class(SNA_OT_Apply_Animate_Modifier_3938E)
    bpy.utils.register_class(SNA_OT_Remove_Decimate_Modifier_63381)
    bpy.utils.register_class(SNA_OT_Remove_Camera_Cull_Modifier_884Cc)
    bpy.utils.register_class(SNA_OT_Remove_Crop_Box_Modifier_90Df7)
    bpy.utils.register_class(SNA_OT_Remove_Colour_Edit_Modifier_Cddb3)
    bpy.utils.register_class(SNA_OT_Remove_Remove_Stray_Modifier_95A21)
    bpy.utils.register_class(SNA_OT_Auto_Set_Up_Camera_Cull_Properties_78Ea9)
    bpy.utils.register_class(SNA_OT_Append_Wire_Sphere_2Bf63)
    bpy.utils.register_class(SNA_OT_Append_Wire_Cube_56E0F)
    bpy.utils.register_class(SNA_OT_Apply_Decimate_Modifier_8C14B)
    bpy.utils.register_class(SNA_OT_Apply_Camera_Cull_Modifier_D55D0)
    bpy.utils.register_class(SNA_OT_Apply_Crop_Box_Modifier_36522)
    bpy.utils.register_class(SNA_OT_Apply_Colour_Edit_Modifier_88410)
    bpy.utils.register_class(SNA_OT_Apply_Remove_Stray_Modifier_3Fdf1)
    bpy.utils.register_class(SNA_OT_Create_Omniview_Object_909Fd)
    bpy.utils.register_class(SNA_AddonPreferences_03DFE)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Offline_Aea04)
    bpy.utils.register_class(SNA_PT_DGS_RENDER__ABOUT__LINKS_PANEL_CC2AC)
    bpy.utils.register_class(SNA_PT_DGS_RENDER__DOCUMENTATION_PANEL_21E93)
    bpy.utils.register_class(SNA_PT_DGS_RENDER__MAIN_FUNCTION_PANEL_2675E)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_kiri3dgs_omnisplat_axes_count
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_animate
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_remove_stray
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_colour_edit
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_crop_box
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_camera_cull
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_decimate
    del bpy.types.Material.sna_kiri3dgs_shading_bsdf_settings
    del bpy.types.Material.sna_kiri3dgs_shading_colour_masks
    del bpy.types.Material.sna_kiri3dgs_shading_base_colour_adjustments
    del bpy.types.Object.sna_kiri3dgs_active_object_enable_active_camera
    del bpy.types.Object.sna_kiri3dgs_active_object_update_mode
    del bpy.types.Scene.sna_kiri3dgs_scene_camera_refresh_mode
    del bpy.types.Scene.sna_kiri3dgs_interface_active_mode
    bpy.utils.unregister_class(SNA_OT_Launch_Kiri_Site_D26Bf)
    bpy.utils.unregister_class(SNA_OT_Launch_Blender_Market_77F72)
    bpy.utils.unregister_class(SNA_OT_Apply_3Dgs_Modifiers_E67A2)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_X_Axis_9B12E)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_Y_Axis_9Bd1F)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_Z_Axis_720A9)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_View_88E3A)
    bpy.utils.unregister_class(SNA_OT_Dgs__Start_Camera_Update_001Bd)
    bpy.utils.unregister_class(SNA_OT_Dgs__Stop_Camera_Update_88568)
    bpy.utils.unregister_class(SNA_OT_Dgs__Update_Camera_Single_Time_03530)
    bpy.app.handlers.load_pre.remove(load_pre_handler_F6F13)
    bpy.utils.unregister_class(SNA_OT_Open_Blender_Splat_Render_Documentation_1Eac5)
    bpy.utils.unregister_class(SNA_OT_Open_Blender_Splat_Render_Tutorial_Video_A4Fe6)
    bpy.utils.unregister_class(SNA_OT_Import_Ply_As_Points_E9E21)
    bpy.utils.unregister_class(SNA_OT_Remove_Point_Edit_Modifier_47851)
    bpy.utils.unregister_class(SNA_OT_Refresh_Point_Edit_Modifier_Ec829)
    bpy.utils.unregister_class(SNA_OT_Append_Point_Edit_Modifier_A0188)
    bpy.utils.unregister_class(SNA_OT_Export_Points_For_3Dgs_63Cd8)
    bpy.utils.unregister_class(SNA_OT_Apply_Point_Edit_Modifier_D6B08)
    bpy.utils.unregister_class(SNA_OT_Hq_Render_B89Bf)
    bpy.utils.unregister_class(SNA_OT_Import_Ply_As_Splats_8458E)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_F216E)
    bpy.utils.unregister_class(SNA_OT_Set_Render_Engine_To_Eevee_D73Ee)
    bpy.utils.unregister_class(SNA_OT_Remove_Animate_Modifier_5B34D)
    bpy.utils.unregister_class(SNA_OT_Apply_Animate_Modifier_3938E)
    bpy.utils.unregister_class(SNA_OT_Remove_Decimate_Modifier_63381)
    bpy.utils.unregister_class(SNA_OT_Remove_Camera_Cull_Modifier_884Cc)
    bpy.utils.unregister_class(SNA_OT_Remove_Crop_Box_Modifier_90Df7)
    bpy.utils.unregister_class(SNA_OT_Remove_Colour_Edit_Modifier_Cddb3)
    bpy.utils.unregister_class(SNA_OT_Remove_Remove_Stray_Modifier_95A21)
    bpy.utils.unregister_class(SNA_OT_Auto_Set_Up_Camera_Cull_Properties_78Ea9)
    bpy.utils.unregister_class(SNA_OT_Append_Wire_Sphere_2Bf63)
    bpy.utils.unregister_class(SNA_OT_Append_Wire_Cube_56E0F)
    bpy.utils.unregister_class(SNA_OT_Apply_Decimate_Modifier_8C14B)
    bpy.utils.unregister_class(SNA_OT_Apply_Camera_Cull_Modifier_D55D0)
    bpy.utils.unregister_class(SNA_OT_Apply_Crop_Box_Modifier_36522)
    bpy.utils.unregister_class(SNA_OT_Apply_Colour_Edit_Modifier_88410)
    bpy.utils.unregister_class(SNA_OT_Apply_Remove_Stray_Modifier_3Fdf1)
    bpy.utils.unregister_class(SNA_OT_Create_Omniview_Object_909Fd)
    bpy.utils.unregister_class(SNA_AddonPreferences_03DFE)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Offline_Aea04)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER__ABOUT__LINKS_PANEL_CC2AC)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER__DOCUMENTATION_PANEL_21E93)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER__MAIN_FUNCTION_PANEL_2675E)
