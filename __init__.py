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
    "description" : "3DGS creation and editing suite",
    "blender" : (4, 2, 0),
    "version" : (3, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
import webbrowser
import os
import numpy as np
import math
from bpy_extras.io_utils import ImportHelper, ExportHelper
import subprocess
from time import time
import platform
from mathutils import Vector, Matrix
from bpy.app.handlers import persistent




def string_to_int(value):
    if value.isdigit():
        return int(value)
    return 0


def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)


addon_keymaps = {}
_icons = None
dgs_render__active_3dgs_object = {'sna_apply_modifier_list': [], 'sna_in_camera_view': False, }
dgs_render__collection_snippets = {'sna_collections_temp_list': [], }
dgs_render__hq_mode = {'sna_lq_object_list': [], }


dgs_render__import = {'sna_dgs_lq_active': None, }
dgs_render__omniview = {'sna_omniviewobjectsformerge': [], 'sna_omniviewbase': None, 'sna_omniviewmodifierlist': [], }


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
        bpy.app.timers.register(delayed_214CF, first_interval=0.30000001192092896)
    else:
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop


def sna_update_sna_kiri3dgs_modifier_enable_animate_1F5D0(self, context):
    sna_updated_prop = self.sna_kiri3dgs_modifier_enable_animate
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_viewport = sna_updated_prop
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_render = sna_updated_prop


def sna_update_sna_kiri3dgs_hq_objects_overlap_DDF15(self, context):
    sna_updated_prop = self.sna_kiri3dgs_hq_objects_overlap
    if sna_updated_prop:
        pass
    else:
        if (property_exists("bpy.context.scene.objects", globals(), locals()) and 'KIRI_HQ_Merged_Object' in bpy.context.scene.objects):
            bpy.ops.sna.disable_hq_overlap_34678('INVOKE_DEFAULT', )


def sna_update_sna_kiri3dgs_lq__hq_065F9(self, context):
    sna_updated_prop = self.sna_kiri3dgs_lq__hq
    print(sna_updated_prop)
    self.surface_render_method = ('BLENDED' if (sna_updated_prop == 'HQ Mode (Blended Alpha)') else 'DITHERED')
    for i_DF01B in range(len(bpy.data.objects)):
        if (property_exists("bpy.data.objects[i_DF01B].modifiers", globals(), locals()) and 'KIRI_3DGS_Sorter_GN' in bpy.data.objects[i_DF01B].modifiers):
            for i_19853 in range(len(bpy.data.objects[i_DF01B].material_slots)):
                if (bpy.data.objects[i_DF01B].material_slots[i_19853].material == self):
                    bpy.data.objects[i_DF01B].modifiers['KIRI_3DGS_Sorter_GN'].show_viewport = (sna_updated_prop == 'HQ Mode (Blended Alpha)')
                    bpy.data.objects[i_DF01B].modifiers['KIRI_3DGS_Sorter_GN'].show_render = (sna_updated_prop == 'HQ Mode (Blended Alpha)')
                    if (property_exists("bpy.context.scene.objects", globals(), locals()) and 'KIRI_HQ_Merged_Object' in bpy.context.scene.objects):
                        if (sna_updated_prop == 'HQ Mode (Blended Alpha)'):
                            bpy.data.objects[i_DF01B].hide_viewport = True
                            bpy.data.objects[i_DF01B].hide_render = True
                            bpy.data.objects['KIRI_HQ_Merged_Object'].hide_viewport = False
                            bpy.data.objects['KIRI_HQ_Merged_Object'].hide_render = False
                        else:
                            bpy.data.objects['KIRI_HQ_Merged_Object'].hide_viewport = True
                            bpy.data.objects['KIRI_HQ_Merged_Object'].hide_render = True
                            bpy.data.objects[i_DF01B].hide_viewport = False
                            bpy.data.objects[i_DF01B].hide_render = False


def sna_update_sna_kiri3dgs_active_mode_BA558(self, context):
    sna_updated_prop = self.sna_kiri3dgs_active_mode
    bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode = 'Import'


def open_folder_skd(directory):
    # Normalize the path
    path = os.path.abspath(directory)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    else:  # Linux and other Unix-based systems
        subprocess.Popen(["xdg-open", path])


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


def sna_update_sna_kiri3dgs_modifier_enable_remove_by_size_488C9(self, context):
    sna_updated_prop = self.sna_kiri3dgs_modifier_enable_remove_by_size
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'].show_viewport = sna_updated_prop
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'].show_render = sna_updated_prop


def sna_add_geo_nodes__append_group_2D522_90019(Append_Path, Node_Group_Name, Objects, Modifier_Name):
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


def sna_add_geo_nodes__append_group_2D522_9D3B3(Append_Path, Node_Group_Name, Objects, Modifier_Name):
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


def sna_add_geo_nodes__append_group_2D522_E5645(Append_Path, Node_Group_Name, Objects, Modifier_Name):
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


def sna_add_geo_nodes__append_group_2D522_9D9CF(Append_Path, Node_Group_Name, Objects, Modifier_Name):
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


class SNA_OT_Launch_Kiri_Site__3Dgs_D26Bf(bpy.types.Operator):
    bl_idname = "sna.launch_kiri_site__3dgs_d26bf"
    bl_label = "Launch Kiri Site - 3DGS"
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


class SNA_OT_Launch_Blender_Market__3Dgs_77F72(bpy.types.Operator):
    bl_idname = "sna.launch_blender_market__3dgs_77f72"
    bl_label = "Launch Blender Market - 3DGS"
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


def sna_dgs__active_3dgs_object_interface_func_9588F(layout_function, ):
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
        col_A4D20 = col_33976.column(heading='', align=False)
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
        col_247F1.label(text='Active 3DGS Object:', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
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
        if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
            if bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked:
                pass
            else:
                col_F0A3B = col_A4D20.column(heading='', align=False)
                col_F0A3B.alert = (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Disable Camera Updates')
                col_F0A3B.enabled = True
                col_F0A3B.active = True
                col_F0A3B.use_property_split = False
                col_F0A3B.use_property_decorate = False
                col_F0A3B.scale_x = 1.0
                col_F0A3B.scale_y = 1.0
                col_F0A3B.alignment = 'Expand'.upper()
                col_F0A3B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_F0A3B.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_active_object_update_mode', text='', icon_value=0, emboss=True, toggle=True)
        else:
            col_67EEA = col_A4D20.column(heading='', align=False)
            col_67EEA.alert = (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Disable Camera Updates')
            col_67EEA.enabled = True
            col_67EEA.active = True
            col_67EEA.use_property_split = False
            col_67EEA.use_property_decorate = False
            col_67EEA.scale_x = 1.0
            col_67EEA.scale_y = 1.0
            col_67EEA.alignment = 'Expand'.upper()
            col_67EEA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_67EEA.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_active_object_update_mode', text='', icon_value=0, emboss=True, toggle=True)
        col_A4D20.separator(factor=1.0)
        if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
            if bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked:
                pass
            else:
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
                            op = box_D2CC1.operator('sna.align_active_to_view_88e3a', text='Update Active To View', icon_value=string_to_icon('HIDE_OFF'), emboss=True, depress=False)
        else:
            if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Enable Camera Updates'):
                if bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera:
                    pass
                else:
                    if 'EDIT_MESH'==bpy.context.mode:
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
                        op = row_A3F2D.operator('sna.align_active_to_x_axis_9b12e', text='X', icon_value=0, emboss=True, depress=False)
                        op = row_A3F2D.operator('sna.align_active_to_y_axis_9bd1f', text='Y', icon_value=0, emboss=True, depress=False)
                        op = row_A3F2D.operator('sna.align_active_to_z_axis_720a9', text='Z', icon_value=0, emboss=True, depress=False)
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
                        op = box_1444A.operator('sna.align_active_to_view_88e3a', text='Update Active To View', icon_value=string_to_icon('HIDE_OFF'), emboss=True, depress=False)
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Show As Point Cloud'):
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
            box_AA375.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], '["Socket_61"]', bpy.data, 'materials', text='Material', icon='NONE')
        if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
            if bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked:
                pass
            else:
                if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Enable Camera Updates'):
                    box_85B7C = col_A4D20.box()
                    box_85B7C.alert = bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera
                    box_85B7C.enabled = True
                    box_85B7C.active = True
                    box_85B7C.use_property_split = False
                    box_85B7C.use_property_decorate = False
                    box_85B7C.alignment = 'Expand'.upper()
                    box_85B7C.scale_x = 1.0
                    box_85B7C.scale_y = 1.0
                    if not True: box_85B7C.operator_context = "EXEC_DEFAULT"
                    if ((bpy.context.scene.camera == None) and bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera):
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
                    box_85B7C.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_active_object_enable_active_camera', text='Use Active Camera', icon_value=string_to_icon('OUTLINER_OB_CAMERA'), emboss=True, toggle=True)
        else:
            if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Enable Camera Updates'):
                box_DC5A2 = col_A4D20.box()
                box_DC5A2.alert = bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera
                box_DC5A2.enabled = True
                box_DC5A2.active = True
                box_DC5A2.use_property_split = False
                box_DC5A2.use_property_decorate = False
                box_DC5A2.alignment = 'Expand'.upper()
                box_DC5A2.scale_x = 1.0
                box_DC5A2.scale_y = 1.0
                if not True: box_DC5A2.operator_context = "EXEC_DEFAULT"
                if ((bpy.context.scene.camera == None) and bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera):
                    box_A3A41 = box_DC5A2.box()
                    box_A3A41.alert = True
                    box_A3A41.enabled = True
                    box_A3A41.active = True
                    box_A3A41.use_property_split = False
                    box_A3A41.use_property_decorate = False
                    box_A3A41.alignment = 'Expand'.upper()
                    box_A3A41.scale_x = 1.0
                    box_A3A41.scale_y = 1.0
                    if not True: box_A3A41.operator_context = "EXEC_DEFAULT"
                    box_A3A41.label(text='No active camera in scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                box_DC5A2.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_active_object_enable_active_camera', text='Use Active Camera', icon_value=string_to_icon('OUTLINER_OB_CAMERA'), emboss=True, toggle=True)
    if (bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode == 'Enable Camera Updates'):
        grid_4D240 = col_33976.grid_flow(columns=6, row_major=False, even_columns=False, even_rows=False, align=False)
        grid_4D240.enabled = True
        grid_4D240.active = True
        grid_4D240.use_property_split = False
        grid_4D240.use_property_decorate = False
        grid_4D240.alignment = 'Expand'.upper()
        grid_4D240.scale_x = 1.0
        grid_4D240.scale_y = 1.0
        if not True: grid_4D240.operator_context = "EXEC_DEFAULT"
        box_A2473 = grid_4D240.box()
        box_A2473.alert = False
        box_A2473.enabled = True
        box_A2473.active = True
        box_A2473.use_property_split = False
        box_A2473.use_property_decorate = False
        box_A2473.alignment = 'Expand'.upper()
        box_A2473.scale_x = 1.0
        box_A2473.scale_y = 1.0
        if not True: box_A2473.operator_context = "EXEC_DEFAULT"
        op = box_A2473.operator('sna.bake_menu_c5fca', text='BAKE', icon_value=0, emboss=True, depress=False)
        box_7D5E1 = grid_4D240.box()
        box_7D5E1.alert = bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked
        box_7D5E1.enabled = True
        box_7D5E1.active = True
        box_7D5E1.use_property_split = False
        box_7D5E1.use_property_decorate = False
        box_7D5E1.alignment = 'Expand'.upper()
        box_7D5E1.scale_x = 1.0
        box_7D5E1.scale_y = 1.0
        if not True: box_7D5E1.operator_context = "EXEC_DEFAULT"
        op = box_7D5E1.operator('sna.remove_bake_532e8', text='Delete Bake', icon_value=string_to_icon('TRASH'), emboss=True, depress=False)
    if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked:
            pass
        else:
            box_1FAE3 = col_33976.box()
            box_1FAE3.alert = False
            box_1FAE3.enabled = 'OBJECT'==bpy.context.mode
            box_1FAE3.active = True
            box_1FAE3.use_property_split = False
            box_1FAE3.use_property_decorate = False
            box_1FAE3.alignment = 'Expand'.upper()
            box_1FAE3.scale_x = 1.0
            box_1FAE3.scale_y = 1.0
            if not True: box_1FAE3.operator_context = "EXEC_DEFAULT"
            op = box_1FAE3.operator('sna.apply_3dgs_modifiers_e67a2', text='Apply Modifiers', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
            op.sna_apply_3dgs_render_modifier = False
            op.sna_apply_decimate_modifier = False
            op.sna_apply_camera_cull_modifier = False
            op.sna_apply_crop_box_modifier = False
            op.sna_apply_colour_edit_modifier = False
            op.sna_apply_remove_by_size_modifier = False
            op.sna_apply_animate_modifier = False
    else:
        box_0FE2E = col_33976.box()
        box_0FE2E.alert = False
        box_0FE2E.enabled = 'OBJECT'==bpy.context.mode
        box_0FE2E.active = True
        box_0FE2E.use_property_split = False
        box_0FE2E.use_property_decorate = False
        box_0FE2E.alignment = 'Expand'.upper()
        box_0FE2E.scale_x = 1.0
        box_0FE2E.scale_y = 1.0
        if not True: box_0FE2E.operator_context = "EXEC_DEFAULT"
        op = box_0FE2E.operator('sna.apply_3dgs_modifiers_e67a2', text='Apply Modifiers', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
        op.sna_apply_3dgs_render_modifier = False
        op.sna_apply_decimate_modifier = False
        op.sna_apply_camera_cull_modifier = False
        op.sna_apply_crop_box_modifier = False
        op.sna_apply_colour_edit_modifier = False
        op.sna_apply_remove_by_size_modifier = False
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
    sna_apply_remove_by_size_modifier: bpy.props.BoolProperty(name='Apply Remove By Size Modifier', description='', default=False)
    sna_apply_animate_modifier: bpy.props.BoolProperty(name='Apply Animate Modifier', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        dgs_render__active_3dgs_object['sna_apply_modifier_list'] = []
        if self.sna_apply_3dgs_render_modifier:
            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_57'] = True
        if self.sna_apply_animate_modifier:
            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_35'] = True
        bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        if self.sna_apply_3dgs_render_modifier:
            dgs_render__active_3dgs_object['sna_apply_modifier_list'].append('KIRI_3DGS_Render_GN')
        if self.sna_apply_decimate_modifier:
            dgs_render__active_3dgs_object['sna_apply_modifier_list'].append('KIRI_3DGS_Decimate_GN')
        if self.sna_apply_camera_cull_modifier:
            dgs_render__active_3dgs_object['sna_apply_modifier_list'].append('KIRI_3DGS_Camera_Cull_GN')
        if self.sna_apply_crop_box_modifier:
            dgs_render__active_3dgs_object['sna_apply_modifier_list'].append('KIRI_3DGS_Crop_Box_GN')
        if self.sna_apply_colour_edit_modifier:
            dgs_render__active_3dgs_object['sna_apply_modifier_list'].append('KIRI_3DGS_Colour_Edit_GN')
        if self.sna_apply_remove_by_size_modifier:
            dgs_render__active_3dgs_object['sna_apply_modifier_list'].append('KIRI_3DGS_Remove_By Size_GN')
        if self.sna_apply_animate_modifier:
            dgs_render__active_3dgs_object['sna_apply_modifier_list'].append('KIRI_3DGS_Animate_GN')
        for i_E1E08 in range(len(dgs_render__active_3dgs_object['sna_apply_modifier_list'])):
            object_name = bpy.context.view_layer.objects.active.name
            modifier_name = dgs_render__active_3dgs_object['sna_apply_modifier_list'][i_E1E08]
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
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Remove_By Size_GN' in bpy.context.view_layer.objects.active.modifiers):
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
            row_E5905.label(text='Apply Remove By Size Modifier', icon_value=0)
            row_E5905.prop(self, 'sna_apply_remove_by_size_modifier', text='', icon_value=0, emboss=True)
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


class SNA_OT_Bake_Menu_C5Fca(bpy.types.Operator):
    bl_idname = "sna.bake_menu_c5fca"
    bl_label = "Bake Menu"
    bl_description = "Opens the Bake window"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode = 'Import'
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_25038 = layout.box()
        box_25038.alert = False
        box_25038.enabled = True
        box_25038.active = True
        box_25038.use_property_split = False
        box_25038.use_property_decorate = False
        box_25038.alignment = 'Expand'.upper()
        box_25038.scale_x = 1.0
        box_25038.scale_y = 1.0
        if not True: box_25038.operator_context = "EXEC_DEFAULT"
        box_2EDE2 = box_25038.box()
        box_2EDE2.alert = True
        box_2EDE2.enabled = True
        box_2EDE2.active = True
        box_2EDE2.use_property_split = False
        box_2EDE2.use_property_decorate = False
        box_2EDE2.alignment = 'Expand'.upper()
        box_2EDE2.scale_x = 1.0
        box_2EDE2.scale_y = 1.0
        if not True: box_2EDE2.operator_context = "EXEC_DEFAULT"
        box_2EDE2.label(text='Baking can lead to very high file sizes', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
        box_2EDE2.label(text='        Baking a very high number of faces and modifiers can freeze / crash Blender', icon_value=0)
        box_2EDE2.label(text='        Baking should be used on smaller, single object scans', icon_value=0)
        box_2EDE2.label(text='        For more information see the documentation and tutorial videos', icon_value=0)
        box_25038.label(text='Bake Type', icon_value=0)
        box_BF0BA = box_25038.box()
        box_BF0BA.alert = False
        box_BF0BA.enabled = True
        box_BF0BA.active = True
        box_BF0BA.use_property_split = False
        box_BF0BA.use_property_decorate = False
        box_BF0BA.alignment = 'Expand'.upper()
        box_BF0BA.scale_x = 1.0
        box_BF0BA.scale_y = 1.0
        if not True: box_BF0BA.operator_context = "EXEC_DEFAULT"
        if bpy.data.is_saved:
            col_5D230 = box_BF0BA.column(heading='', align=False)
            col_5D230.alert = False
            col_5D230.enabled = True
            col_5D230.active = True
            col_5D230.use_property_split = False
            col_5D230.use_property_decorate = False
            col_5D230.scale_x = 1.0
            col_5D230.scale_y = 1.0
            col_5D230.alignment = 'Expand'.upper()
            col_5D230.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                box_E13A4 = col_5D230.box()
                box_E13A4.alert = (not bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport)
                box_E13A4.enabled = True
                box_E13A4.active = True
                box_E13A4.use_property_split = False
                box_E13A4.use_property_decorate = False
                box_E13A4.alignment = 'Expand'.upper()
                box_E13A4.scale_x = 1.0
                box_E13A4.scale_y = 1.0
                if not True: box_E13A4.operator_context = "EXEC_DEFAULT"
                col_510D6 = box_E13A4.column(heading='', align=False)
                col_510D6.alert = False
                col_510D6.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport
                col_510D6.active = True
                col_510D6.use_property_split = False
                col_510D6.use_property_decorate = False
                col_510D6.scale_x = 1.0
                col_510D6.scale_y = 1.0
                col_510D6.alignment = 'Expand'.upper()
                col_510D6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = col_510D6.operator('sna.bake_3dgs_render_and_edit_modifiers_68092', text='3DGS Render + Edit Modifiers', icon_value=0, emboss=True, depress=False)
                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport:
                    pass
                else:
                    box_E13A4.label(text='Render modifier is disabled', icon_value=0)
            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Animate_GN' in bpy.context.view_layer.objects.active.modifiers):
                box_2FCF6 = col_5D230.box()
                box_2FCF6.alert = (not bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_viewport)
                box_2FCF6.enabled = True
                box_2FCF6.active = True
                box_2FCF6.use_property_split = False
                box_2FCF6.use_property_decorate = False
                box_2FCF6.alignment = 'Expand'.upper()
                box_2FCF6.scale_x = 1.0
                box_2FCF6.scale_y = 1.0
                if not True: box_2FCF6.operator_context = "EXEC_DEFAULT"
                col_5D79D = box_2FCF6.column(heading='', align=False)
                col_5D79D.alert = False
                col_5D79D.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_viewport
                col_5D79D.active = True
                col_5D79D.use_property_split = False
                col_5D79D.use_property_decorate = False
                col_5D79D.scale_x = 1.0
                col_5D79D.scale_y = 1.0
                col_5D79D.alignment = 'Expand'.upper()
                col_5D79D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = col_5D79D.operator('sna.bake_3dgs_renderedit_and_animation_modifiers_48bf9', text='3DGS Render + Edit + Animation Modifiers', icon_value=0, emboss=True, depress=False)
                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_viewport:
                    pass
                else:
                    box_2FCF6.label(text='Animate modifier is disabled', icon_value=0)
            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Sorter_GN' in bpy.context.view_layer.objects.active.modifiers):
                box_49CD9 = col_5D230.box()
                box_49CD9.alert = (not bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_viewport)
                box_49CD9.enabled = True
                box_49CD9.active = True
                box_49CD9.use_property_split = False
                box_49CD9.use_property_decorate = False
                box_49CD9.alignment = 'Expand'.upper()
                box_49CD9.scale_x = 1.0
                box_49CD9.scale_y = 1.0
                if not True: box_49CD9.operator_context = "EXEC_DEFAULT"
                col_71EAF = box_49CD9.column(heading='', align=False)
                col_71EAF.alert = False
                col_71EAF.enabled = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_viewport
                col_71EAF.active = True
                col_71EAF.use_property_split = False
                col_71EAF.use_property_decorate = False
                col_71EAF.scale_x = 1.0
                col_71EAF.scale_y = 1.0
                col_71EAF.alignment = 'Expand'.upper()
                col_71EAF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = col_71EAF.operator('sna.bake_3dgs_render_edit_animation_and_sort_modifiers_76100', text='3DGS Render + Edit + Animation + Sorter Modifiers', icon_value=0, emboss=True, depress=False)
                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_viewport:
                    pass
                else:
                    box_49CD9.label(text='HQ Mode / Sorter modifier is disabled', icon_value=0)
        else:
            box_BF0BA.label(text='Blend file is unsaved', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_OT_Remove_Bake_532E8(bpy.types.Operator):
    bl_idname = "sna.remove_bake_532e8"
    bl_label = "Remove Bake"
    bl_description = "Removes baked data."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked = False
        sna_remove_all_bakes_function_execute_A1149()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_bake_3dgs_render_function_execute_825F6(Modifier):
    bpy.ops.sna.remove_bake_532e8('INVOKE_DEFAULT', )
    bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked = True
    bpy.ops.object.geometry_node_bake_single('INVOKE_DEFAULT', session_uid=bpy.context.view_layer.objects.active.modifiers[Modifier].bakes[int(len(bpy.context.view_layer.objects.active.modifiers[Modifier].bakes) - 1.0)].id_data.session_uid, modifier_name=Modifier, bake_id=bpy.context.view_layer.objects.active.modifiers[Modifier].bakes[int(len(bpy.context.view_layer.objects.active.modifiers[Modifier].bakes) - 1.0)].bake_id)


def sna_remove_all_bakes_function_execute_A1149():
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
        for i_3E223 in range(len(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].bakes)):
            bpy.ops.object.geometry_node_bake_delete_single('INVOKE_DEFAULT', session_uid=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].bakes[i_3E223].id_data.session_uid, modifier_name='KIRI_3DGS_Render_GN', bake_id=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].bakes[i_3E223].bake_id)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Animate_GN' in bpy.context.view_layer.objects.active.modifiers):
        for i_318BB in range(len(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].bakes)):
            bpy.ops.object.geometry_node_bake_delete_single('INVOKE_DEFAULT', session_uid=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].bakes[i_318BB].id_data.session_uid, modifier_name='KIRI_3DGS_Animate_GN', bake_id=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].bakes[i_318BB].bake_id)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Sorter_GN' in bpy.context.view_layer.objects.active.modifiers):
        for i_E5A14 in range(len(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].bakes)):
            bpy.ops.object.geometry_node_bake_delete_single('INVOKE_DEFAULT', session_uid=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].bakes[i_E5A14].id_data.session_uid, modifier_name='KIRI_3DGS_Sorter_GN', bake_id=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].bakes[i_E5A14].bake_id)


class SNA_OT_Align_Active_To_X_Axis001_6Ae0E(bpy.types.Operator):
    bl_idname = "sna.align_active_to_x_axis001_6ae0e"
    bl_label = "Align Active To X Axis.001"
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


class SNA_OT_Align_Active_To_Y_Axis001_C305D(bpy.types.Operator):
    bl_idname = "sna.align_active_to_y_axis001_c305d"
    bl_label = "Align Active To Y Axis.001"
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


class SNA_OT_Align_Active_To_Z_Axis001_1E184(bpy.types.Operator):
    bl_idname = "sna.align_active_to_z_axis001_1e184"
    bl_label = "Align Active To Z Axis.001"
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


class SNA_OT_Align_Active_To_View001_30B13(bpy.types.Operator):
    bl_idname = "sna.align_active_to_view001_30b13"
    bl_label = "Align Active To View.001"
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


class SNA_OT_Bake_3Dgs_Render_And_Edit_Modifiers_68092(bpy.types.Operator):
    bl_idname = "sna.bake_3dgs_render_and_edit_modifiers_68092"
    bl_label = "Bake 3DGS Render and Edit Modifiers"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_bake_3dgs_render_function_execute_825F6('KIRI_3DGS_Render_GN')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Bake_3Dgs_Renderedit_And_Animation_Modifiers_48Bf9(bpy.types.Operator):
    bl_idname = "sna.bake_3dgs_renderedit_and_animation_modifiers_48bf9"
    bl_label = "Bake 3DGS Render,Edit and Animation Modifiers"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_bake_3dgs_render_function_execute_825F6('KIRI_3DGS_Animate_GN')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Bake_3Dgs_Render_Edit_Animation_And_Sort_Modifiers_76100(bpy.types.Operator):
    bl_idname = "sna.bake_3dgs_render_edit_animation_and_sort_modifiers_76100"
    bl_label = "Bake 3DGS Render, Edit, Animation and Sort Modifiers"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_bake_3dgs_render_function_execute_825F6('KIRI_3DGS_Sorter_GN')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


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
                    col_44B28.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_5"]', bpy.context.scene.collection, 'children', text='', icon='OUTLINER_DATA_POINTCLOUD')
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
                box_6DFC4.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_44"]', bpy.data, 'materials', text='Material', icon='NONE')
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
                box_91071.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_44"]', bpy.data, 'materials', text='Material', icon='NONE')
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
        op = row_07DA9.operator('sna.add_animate_modifier_39c55', text='', icon_value=45, emboss=True, depress=False)


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


class SNA_OT_Add_Animate_Modifier_39C55(bpy.types.Operator):
    bl_idname = "sna.add_animate_modifier_39c55"
    bl_label = "Add animate modifier"
    bl_description = "Adds a 3DGS animate modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        created_modifier_0_3280f = sna_append_and_add_geo_nodes_function_execute_8BC99('KIRI_3DGS_Animate_GN', 'KIRI_3DGS_Animate_GN', bpy.context.view_layer.objects.active)
        for i_C8AC5 in range(len(bpy.context.view_layer.objects.active.modifiers)):
            if (bpy.context.view_layer.objects.active.modifiers[i_C8AC5] == created_modifier_0_3280f):
                bpy.context.view_layer.objects.active.modifiers.move(from_index=i_C8AC5, to_index=int(len(bpy.context.view_layer.objects.active.modifiers) - 4.0), )
        bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_animate = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_add_to_view3d_mt_object_apply_24C48(self, context):
    if not (False):
        layout = self.layout
        op = layout.operator('sna.apply_3dgs_tranforms_5b665', text='Apply 3DGS Transforms and Colour', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine icon.png')), emboss=True, depress=False)


class SNA_OT_Apply_3Dgs_Tranforms_5B665(bpy.types.Operator):
    bl_idname = "sna.apply_3dgs_tranforms_5b665"
    bl_label = "Apply 3DGS Tranforms"
    bl_description = "Applies the 3DGS Render modifier if present, makes colour edits permanent and updates 3DGS rotation and scale values"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
            modifier_name = 'KIRI_3DGS_Render_GN'
            object_name = bpy.context.view_layer.objects.active.name
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
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Colour_And_Material' in bpy.context.view_layer.objects.active.modifiers):
            modifier_name = 'KIRI_3DGS_Adjust_Colour_And_Material'
            object_name = bpy.context.view_layer.objects.active.name
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
        APPLY_SCALE = True
        APPLY_ROTATION = True
        TRANSFORM_ORDER = 'ROTATION_FIRST'
        import numpy as np
        from mathutils import Quaternion, Matrix, Euler
        #------ INPUT VARIABLES (modify these) ------#
        # The attributes to update
        SCALE_ATTRIBUTES = ["scale_0", "scale_1", "scale_2"]
        ROTATION_ATTRIBUTES = ["rot_0", "rot_1", "rot_2", "rot_3"]
        # Whether to apply transformations after updating attributes
        #APPLY_SCALE = True
        #APPLY_ROTATION = True
        # The order of operations: either "SCALE_FIRST" or "ROTATION_FIRST"
        # 3DGS typically uses SCALE_FIRST (scale, then rotate)
        #TRANSFORM_ORDER = "SCALE_FIRST"
        # Whether to print debug information
        VERBOSE = True
        # Whether to normalize quaternions after transformation (PostShot does this)
        NORMALIZE_QUATERNIONS = True
        #------------------------------------------#

        def quaternion_multiply(q1, q2):
            """
            Multiply two quaternions (compose rotations)
            q1 and q2 are in form [w, x, y, z]
            """
            w1, x1, y1, z1 = q1
            w2, x2, y2, z2 = q2
            w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
            x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
            y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
            z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
            return [w, x, y, z]

        def normalize_quaternion(q):
            """
            Normalize a quaternion to unit length
            q is in form [w, x, y, z]
            """
            magnitude = math.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)
            if magnitude > 0.00001:  # Avoid division by near-zero
                return [q[0]/magnitude, q[1]/magnitude, q[2]/magnitude, q[3]/magnitude]
            else:
                return [1.0, 0.0, 0.0, 0.0]  # Default to identity quaternion

        def update_scale_attributes(obj, scale_attributes, log_scale_factors, verbose=False):
            """
            Update the scale attributes with logarithmic scale factors
            """
            success = True
            for attr_idx, attr_name in enumerate(scale_attributes):
                if attr_name not in obj.data.attributes:
                    print(f"Attribute '{attr_name}' not found on object.")
                    success = False
                    continue
                attr = obj.data.attributes[attr_name]
                if verbose:
                    print(f"\nUpdating attribute: {attr_name}")
                    print(f"Data type: {attr.data_type}")
                    print(f"Domain: {attr.domain}")
                    print(f"Length: {len(attr.data)}")
                # Determine which scale factor to use based on attribute name
                if attr_name == "scale_0":
                    log_scale = log_scale_factors[0]
                elif attr_name == "scale_1":
                    log_scale = log_scale_factors[1]
                elif attr_name == "scale_2":
                    log_scale = log_scale_factors[2]
                else:
                    # For custom-named attributes, use the index in the scale_attributes list
                    log_scale = log_scale_factors[min(attr_idx, 2)]
                if verbose:
                    print(f"Using log scale factor: {log_scale}")
                # Update the attribute values
                if attr.data_type == 'FLOAT':
                    # Sample a few values before and after for verification
                    sample_size = min(5, len(attr.data))
                    before_values = []
                    for i in range(sample_size):
                        before_values.append(attr.data[i].value)
                    # Update all values
                    for i in range(len(attr.data)):
                        # In 3DGS, adding the log of the scale factor to the log-space scale value
                        attr.data[i].value += log_scale
                    # Print sample values after update
                    if verbose:
                        print("Sample values before and after update:")
                        for i in range(sample_size):
                            print(f"  [{i}]: {before_values[i]} -> {attr.data[i].value}")
                else:
                    print(f"Attribute '{attr_name}' is not of type FLOAT (found {attr.data_type}). Skipping.")
                    success = False
            return success

        def update_rotation_attributes(obj, rotation_attributes, blender_quat, verbose=False, normalize=True):
            """
            Update the rotation attributes with the object's rotation quaternion
            """
            # First, gather all data to avoid processing incomplete sets
            attribute_data = {}
            valid_attributes = True
            for attr_name in rotation_attributes:
                if attr_name not in obj.data.attributes:
                    print(f"Attribute '{attr_name}' not found on object.")
                    valid_attributes = False
                    break
                attr = obj.data.attributes[attr_name]
                if attr.data_type != 'FLOAT':
                    print(f"Attribute '{attr_name}' is not of type FLOAT (found {attr.data_type}). Skipping.")
                    valid_attributes = False
                    break
                # Store the attribute for processing
                attribute_data[attr_name] = attr
            if not valid_attributes:
                print("Unable to process rotation due to missing or invalid attributes.")
                return False
            # Sample a few values before the update for verification
            sample_size = min(5, len(attribute_data[rotation_attributes[0]].data))
            before_values = {attr_name: [] for attr_name in rotation_attributes}
            for attr_name in rotation_attributes:
                for i in range(sample_size):
                    before_values[attr_name].append(attribute_data[attr_name].data[i].value)
            # Process all points
            num_points = len(attribute_data[rotation_attributes[0]].data)
            print(f"Processing {num_points} points...")
            for i in range(num_points):
                # Get current quaternion values [w, x, y, z]
                point_quat = [
                    attribute_data[rotation_attributes[0]].data[i].value,  # w
                    attribute_data[rotation_attributes[1]].data[i].value,  # x
                    attribute_data[rotation_attributes[2]].data[i].value,  # y
                    attribute_data[rotation_attributes[3]].data[i].value   # z
                ]
                # Apply rotation by multiplying quaternions
                # The order matters: PostShot appears to use the object_rotation * point_quat
                # format (rotating the local frame)
                new_quat = quaternion_multiply(blender_quat, point_quat)
                # Normalize the quaternion if requested (PostShot does this)
                if normalize:
                    new_quat = normalize_quaternion(new_quat)
                # Enforce positive w component to match PostShot's convention
                # Since q and -q represent the same rotation, we can flip all signs if w is negative
                if new_quat[0] < 0:
                    new_quat = [-q for q in new_quat]
                # Update attribute values
                attribute_data[rotation_attributes[0]].data[i].value = new_quat[0]  # w
                attribute_data[rotation_attributes[1]].data[i].value = new_quat[1]  # x
                attribute_data[rotation_attributes[2]].data[i].value = new_quat[2]  # y
                attribute_data[rotation_attributes[3]].data[i].value = new_quat[3]  # z
            # Print sample values after update for verification
            if verbose:
                print("\nSample values before and after update:")
                for i in range(sample_size):
                    print(f"Point [{i}]:")
                    for j, attr_name in enumerate(rotation_attributes):
                        print(f"  {attr_name}: {before_values[attr_name][i]} -> {attribute_data[attr_name].data[i].value}")
            return True

        def apply_transformations(obj, apply_rotation=False, apply_scale=False):
            """
            Apply the transformations to the object
            """
            if not (apply_rotation or apply_scale):
                return
            # Store current context
            original_mode = obj.mode
            # Switch to object mode if needed
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            # Apply transformations
            bpy.ops.object.transform_apply(
                location=False, 
                rotation=apply_rotation, 
                scale=apply_scale
            )
            # Restore original mode
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=original_mode)
            transformations = []
            if apply_rotation:
                transformations.append("rotation")
            if apply_scale:
                transformations.append("scale")
            print(f"Object {', '.join(transformations)} applied.")
        # MAIN SCRIPT EXECUTION
        # Get the active object
        obj = bpy.context.active_object
        if not obj:
            print("No active object found.")
        else:
            print(f"Processing 3DGS transformations for object: {obj.name}")
            # Get current object rotation (ensuring quaternion is updated)
            original_rotation_mode = obj.rotation_mode
            # If not already in quaternion mode, ensure the quaternion gets updated
            if original_rotation_mode != 'QUATERNION':
                # Switch to quaternion mode to ensure quaternion is updated
                obj.rotation_mode = 'QUATERNION'
                # Switch back to original mode
                obj.rotation_mode = original_rotation_mode
            # Get the quaternion values
            obj_rotation_quat = obj.rotation_quaternion.copy()
            # Convert to w, x, y, z format (from Blender's x, y, z, w)
            blender_quat = [obj_rotation_quat.w, obj_rotation_quat.x, 
                          obj_rotation_quat.y, obj_rotation_quat.z]
            if VERBOSE:
                print(f"Current object rotation quaternion [w,x,y,z]: {blender_quat}")
            # Get current object scale
            scale_x, scale_y, scale_z = obj.scale
            if VERBOSE:
                print(f"Current object scale: X={scale_x}, Y={scale_y}, Z={scale_z}")
            # Calculate the logarithm of scale factors
            log_scale_x = math.log(scale_x) if scale_x > 0 else 0
            log_scale_y = math.log(scale_y) if scale_y > 0 else 0
            log_scale_z = math.log(scale_z) if scale_z > 0 else 0
            log_scale_factors = [log_scale_x, log_scale_y, log_scale_z]
            if VERBOSE:
                print(f"Log scale factors: X={log_scale_x}, Y={log_scale_y}, Z={log_scale_z}")
            # Check if the object has attribute data
            if not hasattr(obj.data, "attributes"):
                print("Object does not have attribute data.")
            else:
                # Perform transformations in the specified order
                if TRANSFORM_ORDER == "SCALE_FIRST":
                    # First update scale attributes
                    scale_success = update_scale_attributes(obj, SCALE_ATTRIBUTES, log_scale_factors, VERBOSE)
                    print("Scale attributes update", "succeeded" if scale_success else "failed")
                    # Then update rotation attributes
                    rotation_success = update_rotation_attributes(obj, ROTATION_ATTRIBUTES, blender_quat, VERBOSE, NORMALIZE_QUATERNIONS)
                    print("Rotation attributes update", "succeeded" if rotation_success else "failed")
                else:  # ROTATION_FIRST
                    # First update rotation attributes
                    rotation_success = update_rotation_attributes(obj, ROTATION_ATTRIBUTES, blender_quat, VERBOSE, NORMALIZE_QUATERNIONS)
                    print("Rotation attributes update", "succeeded" if rotation_success else "failed")
                    # Then update scale attributes
                    scale_success = update_scale_attributes(obj, SCALE_ATTRIBUTES, log_scale_factors, VERBOSE)
                    print("Scale attributes update", "succeeded" if scale_success else "failed")
                # Apply transformations to reset object transforms
                apply_transformations(obj, APPLY_ROTATION, APPLY_SCALE)
                print("\nTransformation operations completed.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_move_object_to_collection_create_if_missingfunction_execute_AB682(Object_to_move, Target_Collection, Collection_Color_Tag):
    if (property_exists("bpy.data.collections", globals(), locals()) and Target_Collection in bpy.data.collections):
        pass
    else:
        collection_CF177 = bpy.data.collections.new(name=Target_Collection, )
        bpy.context.scene.collection.children.link(child=collection_CF177, )
        bpy.data.collections[Target_Collection].color_tag = Collection_Color_Tag
    if (property_exists("bpy.data.collections[Target_Collection].objects", globals(), locals()) and Object_to_move in bpy.data.collections[Target_Collection].objects):
        pass
    else:
        bpy.data.collections[Target_Collection].objects.link(object=bpy.data.objects[Object_to_move], )
    for i_7587C in range(len(bpy.context.scene.collection.children)):
        if (property_exists("bpy.context.scene.collection.children[i_7587C].objects", globals(), locals()) and Object_to_move in bpy.context.scene.collection.children[i_7587C].objects):
            if (bpy.context.scene.collection.children[i_7587C].name == Target_Collection):
                pass
            else:
                bpy.context.scene.collection.children[i_7587C].objects.unlink(object=bpy.data.objects[Object_to_move], )
    if (property_exists("bpy.context.scene.collection.objects", globals(), locals()) and Object_to_move in bpy.context.scene.collection.objects):
        bpy.context.scene.collection.objects.unlink(object=bpy.data.objects[Object_to_move], )


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
    box_E0430.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_17916, text='Shadeless', icon_value=0, emboss=True, toggle=True)
    attr_787E3 = '["' + str('Socket_71' + '"]') 
    box_E0430.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_787E3, text='Create Extra Attributes', icon_value=0, emboss=True, toggle=True)
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
    attr_032D8 = '["' + str('Socket_6' + '"]') 
    box_47A8F.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_032D8, text='Brightness', icon_value=0, emboss=True)
    attr_18662 = '["' + str('Socket_2' + '"]') 
    box_47A8F.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_18662, text='Contrast', icon_value=0, emboss=True)
    attr_000D9 = '["' + str('Socket_4' + '"]') 
    box_47A8F.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_000D9, text='Hue', icon_value=0, emboss=True)
    attr_9DF33 = '["' + str('Socket_3' + '"]') 
    box_47A8F.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], attr_9DF33, text='Saturation', icon_value=0, emboss=True)
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
    box_A85FA.label(text='Active Colour Menu', icon_value=0)
    grid_142F0 = box_A85FA.grid_flow(columns=3, row_major=False, even_columns=False, even_rows=False, align=True)
    grid_142F0.enabled = True
    grid_142F0.active = True
    grid_142F0.use_property_split = False
    grid_142F0.use_property_decorate = False
    grid_142F0.alignment = 'Expand'.upper()
    grid_142F0.scale_x = 1.0
    grid_142F0.scale_y = 1.0
    if not True: grid_142F0.operator_context = "EXEC_DEFAULT"
    col_EA13B = grid_142F0.column(heading='', align=True)
    col_EA13B.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_10']
    col_EA13B.enabled = True
    col_EA13B.active = True
    col_EA13B.use_property_split = False
    col_EA13B.use_property_decorate = False
    col_EA13B.scale_x = 1.0
    col_EA13B.scale_y = 1.0
    col_EA13B.alignment = 'Expand'.upper()
    col_EA13B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_EA13B.operator('sna.set_shading_menu_10891', text='Selective 1', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Selective 1') else 'RADIOBUT_OFF')), emboss=True, depress=False)
    op.sna_shading_menu_set = 'Selective 1'
    col_BD940 = grid_142F0.column(heading='', align=True)
    col_BD940.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_16']
    col_BD940.enabled = True
    col_BD940.active = True
    col_BD940.use_property_split = False
    col_BD940.use_property_decorate = False
    col_BD940.scale_x = 1.0
    col_BD940.scale_y = 1.0
    col_BD940.alignment = 'Expand'.upper()
    col_BD940.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_BD940.operator('sna.set_shading_menu_10891', text='Selective 2', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Selective 2') else 'RADIOBUT_OFF')), emboss=True, depress=False)
    op.sna_shading_menu_set = 'Selective 2'
    col_8FA9B = grid_142F0.column(heading='', align=True)
    col_8FA9B.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_23']
    col_8FA9B.enabled = True
    col_8FA9B.active = True
    col_8FA9B.use_property_split = False
    col_8FA9B.use_property_decorate = False
    col_8FA9B.scale_x = 1.0
    col_8FA9B.scale_y = 1.0
    col_8FA9B.alignment = 'Expand'.upper()
    col_8FA9B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_8FA9B.operator('sna.set_shading_menu_10891', text='Selective 3', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Selective 3') else 'RADIOBUT_OFF')), emboss=True, depress=False)
    op.sna_shading_menu_set = 'Selective 3'
    col_45328 = box_A85FA.column(heading='', align=True)
    col_45328.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_55']
    col_45328.enabled = True
    col_45328.active = True
    col_45328.use_property_split = False
    col_45328.use_property_decorate = False
    col_45328.scale_x = 1.0
    col_45328.scale_y = 1.0
    col_45328.alignment = 'Expand'.upper()
    col_45328.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_45328.operator('sna.set_shading_menu_10891', text='Vertex Paint', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Vertex Paint') else 'RADIOBUT_OFF')), emboss=True, depress=False)
    op.sna_shading_menu_set = 'Vertex Paint'
    col_FC4F2 = box_A85FA.column(heading='', align=True)
    col_FC4F2.alert = bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_56']
    col_FC4F2.enabled = True
    col_FC4F2.active = True
    col_FC4F2.use_property_split = False
    col_FC4F2.use_property_decorate = False
    col_FC4F2.scale_x = 1.0
    col_FC4F2.scale_y = 1.0
    col_FC4F2.alignment = 'Expand'.upper()
    col_FC4F2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_FC4F2.operator('sna.set_shading_menu_10891', text='Image Overlay', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Image Overlay') else 'RADIOBUT_OFF')), emboss=True, depress=False)
    op.sna_shading_menu_set = 'Image Overlay'
    col_EB8EB.separator(factor=1.0)
    box_9A43D = col_EB8EB.box()
    box_9A43D.alert = False
    box_9A43D.enabled = True
    box_9A43D.active = True
    box_9A43D.use_property_split = False
    box_9A43D.use_property_decorate = False
    box_9A43D.alignment = 'Expand'.upper()
    box_9A43D.scale_x = 1.0
    box_9A43D.scale_y = 1.0
    if not True: box_9A43D.operator_context = "EXEC_DEFAULT"
    if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Selective 1'):
        layout_function = box_9A43D
        sna_selective_adjustment_1_function_interface_AD57C(layout_function, )
    if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Selective 2'):
        layout_function = box_9A43D
        sna_selective_adjustment_2_function_interface_4A09B(layout_function, )
    if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Selective 3'):
        layout_function = box_9A43D
        sna_selective_adjustment_3_function_interface_69C53(layout_function, )
    if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Vertex Paint'):
        layout_function = box_9A43D
        sna_vertex_paint_function_interface_BEA3E(layout_function, )
    if (bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu == 'Image Overlay'):
        layout_function = box_9A43D
        sna_image_overlay_function_interface_64796(layout_function, )


class SNA_OT_Set_Shading_Menu_10891(bpy.types.Operator):
    bl_idname = "sna.set_shading_menu_10891"
    bl_label = "Set Shading Menu"
    bl_description = "Sets the actively displayed shading menu"
    bl_options = {"REGISTER", "UNDO"}
    sna_shading_menu_set: bpy.props.StringProperty(name='Shading_Menu_Set', description='', default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_set_shading_menu_function_execute_39CEB(self.sna_shading_menu_set)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_set_shading_menu_function_execute_39CEB(Shading_Menu_Set):
    bpy.context.scene.sna_kiri3dgs_interface_active_shading_menu = Shading_Menu_Set


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
    op = box_C9715.operator('sna.append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'sphere-6796353-white.png')), emboss=True, depress=False)
    op = box_C9715.operator('sna.append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cube-4212258-white.png')), emboss=True, depress=False)


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
    op = box_D2552.operator('sna.append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'sphere-6796353-white.png')), emboss=True, depress=False)
    op = box_D2552.operator('sna.append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cube-4212258-white.png')), emboss=True, depress=False)


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
    op = box_008E7.operator('sna.append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'sphere-6796353-white.png')), emboss=True, depress=False)
    op = box_008E7.operator('sna.append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cube-4212258-white.png')), emboss=True, depress=False)


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
    row_4E69D.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], '["Socket_60"]', bpy.data, 'images', text='Image', icon='NONE')
    op = row_4E69D.operator('sna.import_image_overlay_4a457', text='', icon_value=string_to_icon('FILE_FOLDER'), emboss=True, depress=False)
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
    op = box_A11BE.operator('sna.append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'sphere-6796353-white.png')), emboss=True, depress=False)
    op = box_A11BE.operator('sna.append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cube-4212258-white.png')), emboss=True, depress=False)


def sna_vertex_paint_function_interface_BEA3E(layout_function, ):
    col_453E1 = layout_function.column(heading='', align=False)
    col_453E1.alert = False
    col_453E1.enabled = True
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
        op = box_2E9CF.operator('sna.start_vertex_painting_a36e0', text='Start Painting', icon_value=0, emboss=True, depress=False)
    else:
        box_ACBF2 = box_2E9CF.box()
        box_ACBF2.alert = True
        box_ACBF2.enabled = True
        box_ACBF2.active = True
        box_ACBF2.use_property_split = False
        box_ACBF2.use_property_decorate = False
        box_ACBF2.alignment = 'Expand'.upper()
        box_ACBF2.scale_x = 1.0
        box_ACBF2.scale_y = 1.0
        if not True: box_ACBF2.operator_context = "EXEC_DEFAULT"
        box_ACBF2.label(text='KIRI_3DGS_Paint attribute is missing', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
    op = box_2E9CF.operator('sna.refresh__create_paint_attribute_84655', text='Reset Paint', icon_value=647, emboss=True, depress=False)
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
    op = box_95EA8.operator('sna.append_wire_sphere_2bf63', text='Add Wire Sphere', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'sphere-6796353-white.png')), emboss=True, depress=False)
    op = box_95EA8.operator('sna.append_wire_cube_56e0f', text='Add Wire Cube', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cube-4212258-white.png')), emboss=True, depress=False)


class SNA_OT_Import_Image_Overlay_4A457(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.import_image_overlay_4a457"
    bl_label = "Import Image Overlay"
    bl_description = "Import an image an assign it as the image overlay."
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.png;*.jpg;*.exr', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        image_AB939 = bpy.data.images.load(filepath=self.filepath, check_existing=True, )
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_60'] = image_AB939
        bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}


class SNA_OT_Start_Vertex_Painting_A36E0(bpy.types.Operator):
    bl_idname = "sna.start_vertex_painting_a36e0"
    bl_label = "Start Vertex Painting"
    bl_description = "Enters vertex paint mode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.data.color_attributes.active_color = bpy.context.view_layer.objects.active.data.color_attributes['KIRI_3DGS_Paint']
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='VERTEX_PAINT')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Refresh__Create_Paint_Attribute_84655(bpy.types.Operator):
    bl_idname = "sna.refresh__create_paint_attribute_84655"
    bl_label = "Refresh / Create Paint Attribute"
    bl_description = "Refreshes or creates the KIRI_3DGS_Paint colour attribute"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        import numpy as np
        # Constants
        SH_0 = 0.28209479177387814
        # Serpens typically passes an object as 'input_obj'. Fall back to active_object if not provided.
        try:
            obj = input_obj  # Serpens input (will be defined if called via Serpens node)
        except NameError:
            obj = bpy.context.active_object  # Fallback for text editor or no Serpens input
            print("No input_obj provided, falling back to active object.")
        # Check if we have a valid object
        if not obj:
            print("Error: No object provided or selected.")
        elif obj.type != 'MESH':
            print(f"Error: Object '{obj.name}' is not a mesh (type: {obj.type}).")
        else:
            mesh = obj.data
            required_attrs = ['f_dc_0', 'f_dc_1', 'f_dc_2', 'opacity']
            # Check for required attributes
            missing_attrs = [attr for attr in required_attrs if attr not in mesh.attributes]
            if missing_attrs:
                print(f"Error: Missing required attributes on '{obj.name}': {missing_attrs}")
            else:
                # Get point count and attribute data
                point_count = len(mesh.vertices)
                expected_length = point_count * 4
                f_dc_0_data = np.array([v.value for v in mesh.attributes['f_dc_0'].data])
                f_dc_1_data = np.array([v.value for v in mesh.attributes['f_dc_1'].data])
                f_dc_2_data = np.array([v.value for v in mesh.attributes['f_dc_2'].data])
                opacity_data = np.array([v.value for v in mesh.attributes['opacity'].data])
                # Verify data lengths
                data_lengths = {
                    'f_dc_0': len(f_dc_0_data),
                    'f_dc_1': len(f_dc_1_data),
                    'f_dc_2': len(f_dc_2_data),
                    'opacity': len(opacity_data)
                }
                if not all(length == point_count for length in data_lengths.values()):
                    print(f"Error: Attribute length mismatch. Expected {point_count}, got: {data_lengths}")
                else:
                    # Calculate RGBA
                    paint_color_data = []
                    for i in range(point_count):
                        R = max(0.0, min(1.0, (f_dc_0_data[i] * SH_0 + 0.5)))
                        G = max(0.0, min(1.0, (f_dc_1_data[i] * SH_0 + 0.5)))
                        B = max(0.0, min(1.0, (f_dc_2_data[i] * SH_0 + 0.5)))
                        A = max(0.0, min(1.0, 1 / (1 + np.exp(-opacity_data[i]))))
                        paint_color_data.extend([R, G, B, A])
                    # Verify output length
                    if len(paint_color_data) != expected_length:
                        print(f"Error: Output length mismatch. Expected {expected_length}, got {len(paint_color_data)}")
                    else:
                        # Update or create attribute
                        if 'KIRI_3DGS_Paint' in mesh.attributes:
                            mesh.attributes.remove(mesh.attributes['KIRI_3DGS_Paint'])
                        paint_attr = mesh.attributes.new(name="KIRI_3DGS_Paint", type='FLOAT_COLOR', domain='POINT')
                        paint_attr.data.foreach_set("color", paint_color_data)
                        mesh.color_attributes.active_color = paint_attr
                        print(f"Successfully updated 'KIRI_3DGS_Paint' on '{obj.name}' with {point_count} points.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Open_Blender_3Dgs_Render_Documentation_1Eac5(bpy.types.Operator):
    bl_idname = "sna.open_blender_3dgs_render_documentation_1eac5"
    bl_label = "Open Blender 3DGS Render Documentation"
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


class SNA_OT_Open_Blender_3Dgs_Render_Tutorial_Video_A4Fe6(bpy.types.Operator):
    bl_idname = "sna.open_blender_3dgs_render_tutorial_video_a4fe6"
    bl_label = "Open Blender 3DGS Render Tutorial Video"
    bl_description = "Launches a browser with the addon documentation video"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://youtu.be/ubeD3Vp_7hU'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_export_3dgs_function_interface_CDF59(layout_function, ):
    box_9553E = layout_function.box()
    box_9553E.alert = True
    box_9553E.enabled = True
    box_9553E.active = True
    box_9553E.use_property_split = False
    box_9553E.use_property_decorate = False
    box_9553E.alignment = 'Expand'.upper()
    box_9553E.scale_x = 1.0
    box_9553E.scale_y = 1.0
    if not True: box_9553E.operator_context = "EXEC_DEFAULT"
    box_9553E.label(text="If you have 'applied' scale or rotation values", icon_value=133)
    box_9553E.label(text="         using Blender's native Apply Rotation/", icon_value=0)
    box_9553E.label(text='         Scale, 3DGS attributes will be corrupted', icon_value=0)
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
    box_E30D3.prop(bpy.context.scene, 'sna_kiri3dgs_export__reset_origin', text='Reset Origin', icon_value=0, emboss=True)
    op = box_E30D3.operator('sna.export_mesh_object_as_3dgs_ply_ce2f7', text='Export 3DGS', icon_value=634, emboss=True, depress=False)


class SNA_OT_Export_Mesh_Object_As_3Dgs_Ply_Ce2F7(bpy.types.Operator):
    bl_idname = "sna.export_mesh_object_as_3dgs_ply_ce2f7"
    bl_label = "Export Mesh Object As 3DGS PLY"
    bl_description = "Resets scale and rotation transforms, applies the Point Edit modifier and exports the active object for as a 3DGS .ply"
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
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.view_layer.objects.active.modifiers):
                    bpy.context.view_layer.objects.active.select_set(state=True, view_layer=bpy.context.view_layer, )
                    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = True
                    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = True
                    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge']['Socket_2'] = True
                    object_name = bpy.context.view_layer.objects.active.name
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
                    if bpy.context.scene.sna_kiri3dgs_export__reset_origin:
                        bpy.context.view_layer.objects.active.location = (0.0, 0.0, 0.0)
                    APPLY_SCALE = True
                    APPLY_ROTATION = True
                    TRANSFORM_ORDER = 'ROTATION_FIRST'
                    import numpy as np
                    from mathutils import Quaternion, Matrix, Euler
                    #------ INPUT VARIABLES (modify these) ------#
                    # The attributes to update
                    SCALE_ATTRIBUTES = ["scale_0", "scale_1", "scale_2"]
                    ROTATION_ATTRIBUTES = ["rot_0", "rot_1", "rot_2", "rot_3"]
                    # Whether to apply transformations after updating attributes
                    #APPLY_SCALE = True
                    #APPLY_ROTATION = True
                    # The order of operations: either "SCALE_FIRST" or "ROTATION_FIRST"
                    # 3DGS typically uses SCALE_FIRST (scale, then rotate)
                    #TRANSFORM_ORDER = "SCALE_FIRST"
                    # Whether to print debug information
                    VERBOSE = True
                    # Whether to normalize quaternions after transformation (PostShot does this)
                    NORMALIZE_QUATERNIONS = True
                    #------------------------------------------#

                    def quaternion_multiply(q1, q2):
                        """
                        Multiply two quaternions (compose rotations)
                        q1 and q2 are in form [w, x, y, z]
                        """
                        w1, x1, y1, z1 = q1
                        w2, x2, y2, z2 = q2
                        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
                        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
                        y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
                        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
                        return [w, x, y, z]

                    def normalize_quaternion(q):
                        """
                        Normalize a quaternion to unit length
                        q is in form [w, x, y, z]
                        """
                        magnitude = math.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)
                        if magnitude > 0.00001:  # Avoid division by near-zero
                            return [q[0]/magnitude, q[1]/magnitude, q[2]/magnitude, q[3]/magnitude]
                        else:
                            return [1.0, 0.0, 0.0, 0.0]  # Default to identity quaternion

                    def update_scale_attributes(obj, scale_attributes, log_scale_factors, verbose=False):
                        """
                        Update the scale attributes with logarithmic scale factors
                        """
                        success = True
                        for attr_idx, attr_name in enumerate(scale_attributes):
                            if attr_name not in obj.data.attributes:
                                print(f"Attribute '{attr_name}' not found on object.")
                                success = False
                                continue
                            attr = obj.data.attributes[attr_name]
                            if verbose:
                                print(f"\nUpdating attribute: {attr_name}")
                                print(f"Data type: {attr.data_type}")
                                print(f"Domain: {attr.domain}")
                                print(f"Length: {len(attr.data)}")
                            # Determine which scale factor to use based on attribute name
                            if attr_name == "scale_0":
                                log_scale = log_scale_factors[0]
                            elif attr_name == "scale_1":
                                log_scale = log_scale_factors[1]
                            elif attr_name == "scale_2":
                                log_scale = log_scale_factors[2]
                            else:
                                # For custom-named attributes, use the index in the scale_attributes list
                                log_scale = log_scale_factors[min(attr_idx, 2)]
                            if verbose:
                                print(f"Using log scale factor: {log_scale}")
                            # Update the attribute values
                            if attr.data_type == 'FLOAT':
                                # Sample a few values before and after for verification
                                sample_size = min(5, len(attr.data))
                                before_values = []
                                for i in range(sample_size):
                                    before_values.append(attr.data[i].value)
                                # Update all values
                                for i in range(len(attr.data)):
                                    # In 3DGS, adding the log of the scale factor to the log-space scale value
                                    attr.data[i].value += log_scale
                                # Print sample values after update
                                if verbose:
                                    print("Sample values before and after update:")
                                    for i in range(sample_size):
                                        print(f"  [{i}]: {before_values[i]} -> {attr.data[i].value}")
                            else:
                                print(f"Attribute '{attr_name}' is not of type FLOAT (found {attr.data_type}). Skipping.")
                                success = False
                        return success

                    def update_rotation_attributes(obj, rotation_attributes, blender_quat, verbose=False, normalize=True):
                        """
                        Update the rotation attributes with the object's rotation quaternion
                        """
                        # First, gather all data to avoid processing incomplete sets
                        attribute_data = {}
                        valid_attributes = True
                        for attr_name in rotation_attributes:
                            if attr_name not in obj.data.attributes:
                                print(f"Attribute '{attr_name}' not found on object.")
                                valid_attributes = False
                                break
                            attr = obj.data.attributes[attr_name]
                            if attr.data_type != 'FLOAT':
                                print(f"Attribute '{attr_name}' is not of type FLOAT (found {attr.data_type}). Skipping.")
                                valid_attributes = False
                                break
                            # Store the attribute for processing
                            attribute_data[attr_name] = attr
                        if not valid_attributes:
                            print("Unable to process rotation due to missing or invalid attributes.")
                            return False
                        # Sample a few values before the update for verification
                        sample_size = min(5, len(attribute_data[rotation_attributes[0]].data))
                        before_values = {attr_name: [] for attr_name in rotation_attributes}
                        for attr_name in rotation_attributes:
                            for i in range(sample_size):
                                before_values[attr_name].append(attribute_data[attr_name].data[i].value)
                        # Process all points
                        num_points = len(attribute_data[rotation_attributes[0]].data)
                        print(f"Processing {num_points} points...")
                        for i in range(num_points):
                            # Get current quaternion values [w, x, y, z]
                            point_quat = [
                                attribute_data[rotation_attributes[0]].data[i].value,  # w
                                attribute_data[rotation_attributes[1]].data[i].value,  # x
                                attribute_data[rotation_attributes[2]].data[i].value,  # y
                                attribute_data[rotation_attributes[3]].data[i].value   # z
                            ]
                            # Apply rotation by multiplying quaternions
                            # The order matters: PostShot appears to use the object_rotation * point_quat
                            # format (rotating the local frame)
                            new_quat = quaternion_multiply(blender_quat, point_quat)
                            # Normalize the quaternion if requested (PostShot does this)
                            if normalize:
                                new_quat = normalize_quaternion(new_quat)
                            # Enforce positive w component to match PostShot's convention
                            # Since q and -q represent the same rotation, we can flip all signs if w is negative
                            if new_quat[0] < 0:
                                new_quat = [-q for q in new_quat]
                            # Update attribute values
                            attribute_data[rotation_attributes[0]].data[i].value = new_quat[0]  # w
                            attribute_data[rotation_attributes[1]].data[i].value = new_quat[1]  # x
                            attribute_data[rotation_attributes[2]].data[i].value = new_quat[2]  # y
                            attribute_data[rotation_attributes[3]].data[i].value = new_quat[3]  # z
                        # Print sample values after update for verification
                        if verbose:
                            print("\nSample values before and after update:")
                            for i in range(sample_size):
                                print(f"Point [{i}]:")
                                for j, attr_name in enumerate(rotation_attributes):
                                    print(f"  {attr_name}: {before_values[attr_name][i]} -> {attribute_data[attr_name].data[i].value}")
                        return True

                    def apply_transformations(obj, apply_rotation=False, apply_scale=False):
                        """
                        Apply the transformations to the object
                        """
                        if not (apply_rotation or apply_scale):
                            return
                        # Store current context
                        original_mode = obj.mode
                        # Switch to object mode if needed
                        if original_mode != 'OBJECT':
                            bpy.ops.object.mode_set(mode='OBJECT')
                        # Apply transformations
                        bpy.ops.object.transform_apply(
                            location=False, 
                            rotation=apply_rotation, 
                            scale=apply_scale
                        )
                        # Restore original mode
                        if original_mode != 'OBJECT':
                            bpy.ops.object.mode_set(mode=original_mode)
                        transformations = []
                        if apply_rotation:
                            transformations.append("rotation")
                        if apply_scale:
                            transformations.append("scale")
                        print(f"Object {', '.join(transformations)} applied.")
                    # MAIN SCRIPT EXECUTION
                    # Get the active object
                    obj = bpy.context.active_object
                    if not obj:
                        print("No active object found.")
                    else:
                        print(f"Processing 3DGS transformations for object: {obj.name}")
                        # Get current object rotation (ensuring quaternion is updated)
                        original_rotation_mode = obj.rotation_mode
                        # If not already in quaternion mode, ensure the quaternion gets updated
                        if original_rotation_mode != 'QUATERNION':
                            # Switch to quaternion mode to ensure quaternion is updated
                            obj.rotation_mode = 'QUATERNION'
                            # Switch back to original mode
                            obj.rotation_mode = original_rotation_mode
                        # Get the quaternion values
                        obj_rotation_quat = obj.rotation_quaternion.copy()
                        # Convert to w, x, y, z format (from Blender's x, y, z, w)
                        blender_quat = [obj_rotation_quat.w, obj_rotation_quat.x, 
                                      obj_rotation_quat.y, obj_rotation_quat.z]
                        if VERBOSE:
                            print(f"Current object rotation quaternion [w,x,y,z]: {blender_quat}")
                        # Get current object scale
                        scale_x, scale_y, scale_z = obj.scale
                        if VERBOSE:
                            print(f"Current object scale: X={scale_x}, Y={scale_y}, Z={scale_z}")
                        # Calculate the logarithm of scale factors
                        log_scale_x = math.log(scale_x) if scale_x > 0 else 0
                        log_scale_y = math.log(scale_y) if scale_y > 0 else 0
                        log_scale_z = math.log(scale_z) if scale_z > 0 else 0
                        log_scale_factors = [log_scale_x, log_scale_y, log_scale_z]
                        if VERBOSE:
                            print(f"Log scale factors: X={log_scale_x}, Y={log_scale_y}, Z={log_scale_z}")
                        # Check if the object has attribute data
                        if not hasattr(obj.data, "attributes"):
                            print("Object does not have attribute data.")
                        else:
                            # Perform transformations in the specified order
                            if TRANSFORM_ORDER == "SCALE_FIRST":
                                # First update scale attributes
                                scale_success = update_scale_attributes(obj, SCALE_ATTRIBUTES, log_scale_factors, VERBOSE)
                                print("Scale attributes update", "succeeded" if scale_success else "failed")
                                # Then update rotation attributes
                                rotation_success = update_rotation_attributes(obj, ROTATION_ATTRIBUTES, blender_quat, VERBOSE, NORMALIZE_QUATERNIONS)
                                print("Rotation attributes update", "succeeded" if rotation_success else "failed")
                            else:  # ROTATION_FIRST
                                # First update rotation attributes
                                rotation_success = update_rotation_attributes(obj, ROTATION_ATTRIBUTES, blender_quat, VERBOSE, NORMALIZE_QUATERNIONS)
                                print("Rotation attributes update", "succeeded" if rotation_success else "failed")
                                # Then update scale attributes
                                scale_success = update_scale_attributes(obj, SCALE_ATTRIBUTES, log_scale_factors, VERBOSE)
                                print("Scale attributes update", "succeeded" if scale_success else "failed")
                            # Apply transformations to reset object transforms
                            apply_transformations(obj, APPLY_ROTATION, APPLY_SCALE)
                            print("\nTransformation operations completed.")

                    def delayed_5B08A():
                        bpy.ops.wm.ply_export('INVOKE_DEFAULT', apply_modifiers=True, export_selected_objects=True, export_attributes=True)
                    bpy.app.timers.register(delayed_5B08A, first_interval=0.10000000149011612)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_44942 = layout.box()
        box_44942.alert = True
        box_44942.enabled = True
        box_44942.active = True
        box_44942.use_property_split = False
        box_44942.use_property_decorate = False
        box_44942.alignment = 'Expand'.upper()
        box_44942.scale_x = 1.0
        box_44942.scale_y = 1.0
        if not True: box_44942.operator_context = "EXEC_DEFAULT"
        box_44942.label(text='All modifiers will be applied. To continue working in Blender', icon_value=133)
        box_44942.label(text='         it is advised to make a duplicate before exporting.', icon_value=0)
        box_44942.label(text='         Press OK to continue exporting', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


def sna_hq_mode_function_interface_17C41(layout_function, ):
    if (bpy.context.scene.render.engine == 'BLENDER_EEVEE_NEXT'):
        pass
    else:
        box_5B434 = layout_function.box()
        box_5B434.alert = True
        box_5B434.enabled = True
        box_5B434.active = True
        box_5B434.use_property_split = False
        box_5B434.use_property_decorate = False
        box_5B434.alignment = 'Expand'.upper()
        box_5B434.scale_x = 1.0
        box_5B434.scale_y = 1.0
        if not True: box_5B434.operator_context = "EXEC_DEFAULT"
        box_5B434.label(text='LQ / HQ Materials are only effective', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
        box_5B434.label(text='        when using Eevee.', icon_value=0)
    if (bpy.context.scene.camera == None):
        box_9AC8C = layout_function.box()
        box_9AC8C.alert = True
        box_9AC8C.enabled = True
        box_9AC8C.active = True
        box_9AC8C.use_property_split = False
        box_9AC8C.use_property_decorate = False
        box_9AC8C.alignment = 'Expand'.upper()
        box_9AC8C.scale_x = 1.0
        box_9AC8C.scale_y = 1.0
        if not True: box_9AC8C.operator_context = "EXEC_DEFAULT"
        box_9AC8C.label(text='No active camera in scene.', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
        box_9AC8C.label(text='         A camera is required for HQ materials.', icon_value=0)
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
    box_AEE3F = col_249D2.box()
    box_AEE3F.alert = True
    box_AEE3F.enabled = True
    box_AEE3F.active = True
    box_AEE3F.use_property_split = False
    box_AEE3F.use_property_decorate = False
    box_AEE3F.alignment = 'Expand'.upper()
    box_AEE3F.scale_x = 1.0
    box_AEE3F.scale_y = 1.0
    if not True: box_AEE3F.operator_context = "EXEC_DEFAULT"
    box_AEE3F.label(text='LQ Mode requires high samples (64+)', icon_value=string_to_icon('INFO'))
    box_AEE3F.label(text='         Samples can often be reduced to 1 in HQ Mode', icon_value=0)
    box_AEE3F.label(text="         if 'Shadeless' materials are used", icon_value=0)
    box_AEE3F.prop(bpy.context.scene.eevee, 'taa_samples', text='Viewport Samples', icon_value=0, emboss=True)
    box_AEE3F.prop(bpy.context.scene.eevee, 'taa_render_samples', text='Render Samples', icon_value=0, emboss=True)
    if bpy.context.scene.eevee.use_taa_reprojection:
        box_06ADA = col_249D2.box()
        box_06ADA.alert = True
        box_06ADA.enabled = True
        box_06ADA.active = True
        box_06ADA.use_property_split = False
        box_06ADA.use_property_decorate = False
        box_06ADA.alignment = 'Expand'.upper()
        box_06ADA.scale_x = 1.0
        box_06ADA.scale_y = 1.0
        if not True: box_06ADA.operator_context = "EXEC_DEFAULT"
        box_06ADA.label(text='         Temporal Reprojection is a enabled ', icon_value=0)
        box_06ADA.label(text='         This can cause flickering', icon_value=0)
        box_06ADA.label(text='         It should be disabled', icon_value=0)
        box_06ADA.prop(bpy.context.scene.eevee, 'use_taa_reprojection', text='Temporal Reprojection', icon_value=0, emboss=True)
    col_249D2.separator(factor=1.0)
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        for i_E3C27 in range(len(bpy.context.view_layer.objects.active.material_slots)):
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
            box_2E343.prop(bpy.context.view_layer.objects.active.material_slots[i_E3C27].material, 'sna_kiri3dgs_lq__hq', text='', icon_value=0, emboss=True)
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
    box_D2847.prop(bpy.context.scene, 'sna_kiri3dgs_hq_objects_overlap', text='Objects Overlap?', icon_value=0, emboss=True, toggle=True)
    if bpy.context.scene.sna_kiri3dgs_hq_objects_overlap:
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
            box_BEFDD.alert = True
            box_BEFDD.enabled = False
            box_BEFDD.active = True
            box_BEFDD.use_property_split = False
            box_BEFDD.use_property_decorate = False
            box_BEFDD.alignment = 'Expand'.upper()
            box_BEFDD.scale_x = 1.0
            box_BEFDD.scale_y = 1.0
            if not True: box_BEFDD.operator_context = "EXEC_DEFAULT"
            box_BEFDD.label(text='HQ Object already exists', icon_value=133)
            op = box_BEFDD.operator('sna.generate_hq_object_55455', text='Generate HQ Object', icon_value=0, emboss=True, depress=False)
        else:
            op = box_0826A.operator('sna.generate_hq_object_55455', text='Generate HQ Object', icon_value=0, emboss=True, depress=False)


class SNA_OT_Generate_Hq_Object_55455(bpy.types.Operator):
    bl_idname = "sna.generate_hq_object_55455"
    bl_label = "Generate HQ Object"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        dgs_render__hq_mode['sna_lq_object_list'] = []
        for i_3F5D0 in range(len(bpy.data.objects)):
            if (property_exists("bpy.data.objects[i_3F5D0].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.data.objects[i_3F5D0].modifiers):
                bpy.data.objects[i_3F5D0].sna_kiri3dgs_active_object_enable_active_camera = True
                bpy.data.objects[i_3F5D0].modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = True

        def delayed_CB67D():
            sna_dgs__update_camera_single_time_function_execute_9C695()

            def delayed_013E4():
                bpy.data.objects[i_3F5D0].update_tag(refresh={'DATA'}, )
                if bpy.context and bpy.context.screen:
                    for a in bpy.context.screen.areas:
                        a.tag_redraw()
                for i_294E7 in range(len(bpy.context.scene.objects)):
                    if (bpy.context.scene.objects[i_294E7] == None):
                        pass
                    else:
                        if (property_exists("bpy.context.scene.objects[i_294E7].modifiers", globals(), locals()) and 'KIRI_3DGS_Sorter_GN' in bpy.context.scene.objects[i_294E7].modifiers):
                            dgs_render__hq_mode['sna_lq_object_list'].append(bpy.context.scene.objects[i_294E7].name)
                for i_6C743 in range(len(dgs_render__hq_mode['sna_lq_object_list'])):
                    bpy.data.objects[dgs_render__hq_mode['sna_lq_object_list'][i_6C743]].hide_viewport = True
                    bpy.data.objects[dgs_render__hq_mode['sna_lq_object_list'][i_6C743]].hide_render = True
                    sna_move_object_to_collection_create_if_missingfunction_execute_AB682(dgs_render__hq_mode['sna_lq_object_list'][i_6C743], '3DGS_LQ_Objects', 'COLOR_06')
                before_data = list(bpy.data.objects)
                bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend') + r'\Object', filename='KIRI_HQ_Merged_Object', link=False)
                new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
                appended_D9EAC = None if not new_data else new_data[0]
                sna_move_object_to_collection_create_if_missingfunction_execute_AB682('KIRI_HQ_Merged_Object', '3DGS_HQ_Object', 'COLOR_05')
                sna_append_and_add_geo_nodes_function_execute_8BC99('KIRI_3DGS_Instance_HQ', 'KIRI_3DGS_Instance_HQ', bpy.data.objects['KIRI_HQ_Merged_Object'])
                bpy.data.objects['KIRI_HQ_Merged_Object'].modifiers['KIRI_3DGS_Instance_HQ']['Socket_2'] = bpy.data.collections['3DGS_LQ_Objects']
                if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
                    pass
                else:
                    before_data = list(bpy.data.materials)
                    bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
                    new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
                    appended_061FB = None if not new_data else new_data[0]
                input_object = bpy.data.objects['KIRI_HQ_Merged_Object']
                material_name = 'KIRI_3DGS_Render_Material'
                # Input Variable Names
                #input_object = None  # Should be set to a bpy.types.Object pointer before running
                #material_name = "KIRI_3DGS_Render_Material"  # Name of the material to assign
                # Check if the input object is provided and is valid
                if not input_object or input_object.type != 'MESH':
                    print("Error: No valid mesh object provided as input.")
                else:
                    # Get the object and its mesh data
                    obj = input_object
                    mesh = obj.data
                    try:
                        # Remove all existing material slots
                        while len(obj.material_slots) > 0:
                            bpy.context.object.active_material_index = 0  # Set to the first slot to remove
                            bpy.ops.object.material_slot_remove()
                        # Check if the material exists; create it if it doesn’t
                        if material_name not in bpy.data.materials:
                            new_material = bpy.data.materials.new(name=material_name)
                            new_material.use_nodes = True  # Enable node-based shading (optional, matching your original script)
                        else:
                            new_material = bpy.data.materials[material_name]
                        # Add the material to the object as a new slot
                        obj.data.materials.append(new_material)
                        print(f"Assigned material '{material_name}' to {obj.name} and removed existing material slots.")
                    except Exception as e:
                        print(f"Error assigning material to {obj.name}: {e}")
                bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method = 'BLENDED'
                bpy.data.objects['KIRI_HQ_Merged_Object'].update_tag(refresh={'OBJECT'}, )
                if bpy.context and bpy.context.screen:
                    for a in bpy.context.screen.areas:
                        a.tag_redraw()
            bpy.app.timers.register(delayed_013E4, first_interval=0.10000000149011612)
        bpy.app.timers.register(delayed_CB67D, first_interval=0.10000000149011612)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_B5524 = layout.box()
        box_B5524.alert = True
        box_B5524.enabled = True
        box_B5524.active = True
        box_B5524.use_property_split = False
        box_B5524.use_property_decorate = False
        box_B5524.alignment = 'Expand'.upper()
        box_B5524.scale_x = 1.0
        box_B5524.scale_y = 1.0
        if not True: box_B5524.operator_context = "EXEC_DEFAULT"
        box_B5524.label(text="All original 'LQ' objects will be moved into '3DGS_LQ_Objects' collection", icon_value=133)
        box_B5524.label(text="        A new object -'KIRI_HQ_Merged_Object' - will be created", icon_value=0)
        box_B5524.label(text='        Use the LQ / HQ drop down to toggle between original and HQ object visibilities', icon_value=0)
        box_B5524.label(text='        Do not rename the created collections', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_OT_Disable_Hq_Overlap_34678(bpy.types.Operator):
    bl_idname = "sna.disable_hq_overlap_34678"
    bl_label = "Disable HQ Overlap"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.data.objects.remove(object=bpy.data.objects['KIRI_HQ_Merged_Object'], do_unlink=True, do_id_user=True, do_ui_user=True, )
        if property_exists("bpy.data.collections['3DGS_HQ_Object']", globals(), locals()):
            bpy.data.collections.remove(collection=bpy.data.collections['3DGS_HQ_Object'], do_unlink=True, do_id_user=True, do_ui_user=True, )
        if property_exists("bpy.data.collections['3DGS_LQ_Objects']", globals(), locals()):
            for i_EF373 in range(len(bpy.data.collections['3DGS_LQ_Objects'].all_objects)):
                bpy.data.collections['3DGS_LQ_Objects'].all_objects[i_EF373].hide_viewport = False
                bpy.data.collections['3DGS_LQ_Objects'].all_objects[i_EF373].hide_render = False
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_2D485 = layout.box()
        box_2D485.alert = True
        box_2D485.enabled = True
        box_2D485.active = True
        box_2D485.use_property_split = False
        box_2D485.use_property_decorate = False
        box_2D485.alignment = 'Expand'.upper()
        box_2D485.scale_x = 1.0
        box_2D485.scale_y = 1.0
        if not True: box_2D485.operator_context = "EXEC_DEFAULT"
        box_2D485.label(text='HQ Object found in scene', icon_value=string_to_icon('INFO'))
        box_2D485.label(text='        Delete it?', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


class SNA_OT_Import_Ply_As_Splats_8458E(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.import_ply_as_splats_8458e"
    bl_label = "Import PLY As Splats"
    bl_description = "Import a .PLY using the chosen 3DGS import settings"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.ply', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        ply_import_path = self.filepath
        output_object = None
        attributes_missing = None
        message = None
        import os
        # Input file path
        #ply_import_path = "C:\\Users\\joe and pig\\Documents\\Flamingo.ply"  # Example path; update as needed
        # Check if the file path is provided and exists
        if not ply_import_path or not os.path.exists(ply_import_path):
            print("Error: No file path provided or file not found.")
            attributes_missing = True
            message = f"Error: No file path provided or file not found at {ply_import_path}."
            output_object = None
        else:
            try:
                # Import the PLY file using Blender's native importer (Blender 4.0+)
                try:
                    bpy.ops.wm.ply_import(filepath=ply_import_path)
                except AttributeError:
                    print("Error: PLY importer operator 'bpy.ops.wm.ply_import' not found. Ensure Blender 4.0 or later is used.")
                    attributes_missing = True
                    message = f"Error: PLY importer operator not found for {os.path.basename(ply_import_path)}. Ensure Blender 4.0 or later is used."
                    output_object = None
                else:
                    # Get the last imported object (assuming it's the PLY mesh)
                    imported_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
                    if not imported_objects:
                        print("Error: No objects were imported from the PLY file.")
                        attributes_missing = True
                        message = f"Error: No objects were imported from the PLY file {os.path.basename(ply_import_path)}."
                        output_object = None
                    else:
                        # Use the first imported object (assuming it's a mesh)
                        obj = imported_objects[0]
                        if obj.type != 'MESH':
                            print("Error: Imported object is not a mesh.")
                            attributes_missing = True
                            message = f"Error: Imported object from {os.path.basename(ply_import_path)} is not a mesh."
                            output_object = None
                        else:
                            # Get the mesh data
                            mesh = obj.data
                            # List of required 3DGS attributes
                            required_attributes = ['f_dc_0', 'f_dc_1', 'f_dc_2', 'opacity', 'scale_0', 'scale_1', 'scale_2', 'rot_0', 'rot_1', 'rot_2', 'rot_3', 'f_rest_0']
                            # Check if all required attributes exist on the mesh
                            attributes_missing = False
                            missing_attrs = []
                            for attr_name in required_attributes:
                                if attr_name not in mesh.attributes:
                                    attributes_missing = True
                                    missing_attrs.append(attr_name)
                            # Set the message and output object based on success or failure
                            if attributes_missing:
                                message = f"Error: One or more required 3DGS attributes ({', '.join(missing_attrs)}) are missing on {obj.name}. Check that .ply is a 3DGS scan."
                                print(message)
                                output_object = None
                            else:
                                message = f"Successfully imported PLY file {os.path.basename(ply_import_path)} and all required 3DGS attributes ({', '.join(required_attributes)}) are present on {obj.name}."
                                print(message)
                                output_object = obj
            except Exception as e:
                print(f"Error importing PLY file: {e}")
                attributes_missing = True
                message = f"Error importing PLY file {os.path.basename(ply_import_path)}: {str(e)}"
                output_object = None
        # The variables are now available for use
        # You can access 'attributes_missing' (boolean), 'message' (string), and 'output_object' (bpy.types.Object or None) in other scripts or logic
        if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.materials)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
            appended_6CC4A = None if not new_data else new_data[0]
        sna_append_and_add_geo_nodes_function_execute_8BC99('KIRI_3DGS_Store_Origpos_GN', 'KIRI_3DGS_Store_Origpos_GN', bpy.context.view_layer.objects.active)
        bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Store_Origpos_GN')
        sna_append_and_add_geo_nodes_function_execute_8BC99('KIRI_3DGS_Render_GN', 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active)
        sna_align_active_values_to_x_function_execute_03E8D()
        bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Render_GN')
        import numpy as np
        # Constants from your script
        SH_0 = 0.28209479177387814
        # Get the active object
        obj = bpy.context.active_object
        if not obj or obj.type != 'MESH':
            print("Error: No active mesh object selected.")
        else:
            # Get the mesh data
            mesh = obj.data
            # Check if the required attributes exist
            if not all(attr.name in mesh.attributes for attr in mesh.attributes if attr.name in ['f_dc_0', 'f_dc_1', 'f_dc_2', 'opacity']):
                print("Error: Required attributes (f_dc_0, f_dc_1, f_dc_2, opacity) not found on the mesh.")
            else:
                # Get the number of points (vertices)
                point_count = len(mesh.vertices)
                expected_length = point_count * 4  # Each point has 1 RGBA set (4 values) for both Col and KIRI_3DGS_Paint
                # Extract data from attributes (assuming they are on POINT domain)
                f_dc_0_data = np.array([v.value for v in mesh.attributes['f_dc_0'].data])
                f_dc_1_data = np.array([v.value for v in mesh.attributes['f_dc_1'].data])
                f_dc_2_data = np.array([v.value for v in mesh.attributes['f_dc_2'].data])
                opacity_data = np.array([v.value for v in mesh.attributes['opacity'].data])
                # Debug: Check lengths of input attribute data
                print(f"Number of points (vertices): {point_count}")
                print(f"Length of f_dc_0_data: {len(f_dc_0_data)}")
                print(f"Length of f_dc_1_data: {len(f_dc_1_data)}")
                print(f"Length of f_dc_2_data: {len(f_dc_2_data)}")
                print(f"Length of opacity_data: {len(opacity_data)}")
                # Verify that attribute data lengths match the number of points
                if not (len(f_dc_0_data) == len(f_dc_1_data) == len(f_dc_2_data) == len(opacity_data) == point_count):
                    print("Error: Mismatch in attribute data lengths. Expected length matches point_count.")
                else:
                    # Calculate RGB and Alpha for each point (same calculation for both Col and KIRI_3DGS_Paint)
                    color_data = []  # For both Col and KIRI_3DGS_Paint, one RGBA per point
                    for i in range(point_count):
                        # Calculate RGB (matching your script)
                        R = (f_dc_0_data[i] * SH_0 + 0.5)
                        G = (f_dc_1_data[i] * SH_0 + 0.5)
                        B = (f_dc_2_data[i] * SH_0 + 0.5)
                        # Calculate Alpha (using sigmoid if opacity is in log-space, or raw if [0, 1])
                        # Here, we assume opacity is in log-space (logits) as in your script
                        log_opacity = opacity_data[i]
                        A = 1 / (1 + np.exp(-log_opacity))
                        # Ensure values are in [0, 1]
                        R = max(0.0, min(1.0, R))
                        G = max(0.0, min(1.0, G))
                        B = max(0.0, min(1.0, B))
                        A = max(0.0, min(1.0, A))
                        # Add RGBA for both Col and KIRI_3DGS_Paint (one set per point)
                        color_data.extend([R, G, B, A])
                    # Debug: Check calculated data length
                    print(f"Length of color_data (Col and KIRI_3DGS_Paint): {len(color_data)}")
                    print(f"Expected length for POINT domain: {expected_length}")
                    # Verify data length matches expectation
                    if len(color_data) != expected_length:
                        print(f"Error: Array length mismatch (expected {expected_length}, got {len(color_data)})")
                    else:
                        # Create or update the Col attribute on the point domain
                        if 'Col' in mesh.attributes:
                            mesh.attributes.remove(mesh.attributes['Col'])
                        col_attr = mesh.attributes.new(name="Col", type='FLOAT_COLOR', domain='POINT')
                        col_attr.data.foreach_set("color", color_data)
                        # Create or update the KIRI_3DGS_Paint attribute on the point domain
                        if 'KIRI_3DGS_Paint' in mesh.attributes:
                            mesh.attributes.remove(mesh.attributes['KIRI_3DGS_Paint'])
                        paint_attr = mesh.attributes.new(name="KIRI_3DGS_Paint", type='FLOAT_COLOR', domain='POINT')
                        paint_attr.data.foreach_set("color", color_data)
                        # Set KIRI_3DGS_Paint as the active color attribute
                        mesh.color_attributes.active_color = paint_attr
                        print(f"Created Col attribute on {obj.name} with {point_count} points.")
                        print(f"Created KIRI_3DGS_Paint attribute on {obj.name} with {point_count} color values on the POINT domain.")
        sna_append_and_add_geo_nodes_function_execute_8BC99('KIRI_3DGS_Render_GN', 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_8BC99('KIRI_3DGS_Sorter_GN', 'KIRI_3DGS_Sorter_GN', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_8BC99('KIRI_3DGS_Adjust_Colour_And_Material', 'KIRI_3DGS_Adjust_Colour_And_Material', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_8BC99('KIRI_3DGS_Write F_DC_And_Merge', 'KIRI_3DGS_Write F_DC_And_Merge', bpy.context.view_layer.objects.active)
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'].show_viewport = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'].show_render = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].bakes[0].bake_mode = 'ANIMATION'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].bakes[0].bake_mode = 'ANIMATION'
        bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode = 'Disable Camera Updates'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_on_cage = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_in_editmode = True
        bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_enable_active_camera = False
        bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_update_mode = 'Disable Camera Updates'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_viewport = (bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method == 'BLENDED')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_render = (bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method == 'BLENDED')
        bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        input_object = bpy.context.view_layer.objects.active
        material_name = 'KIRI_3DGS_Render_Material'
        # Input Variable Names
        #input_object = None  # Should be set to a bpy.types.Object pointer before running
        #material_name = "KIRI_3DGS_Render_Material"  # Name of the material to assign
        # Check if the input object is provided and is valid
        if not input_object or input_object.type != 'MESH':
            print("Error: No valid mesh object provided as input.")
        else:
            # Get the object and its mesh data
            obj = input_object
            mesh = obj.data
            try:
                # Remove all existing material slots
                while len(obj.material_slots) > 0:
                    bpy.context.object.active_material_index = 0  # Set to the first slot to remove
                    bpy.ops.object.material_slot_remove()
                # Check if the material exists; create it if it doesn’t
                if material_name not in bpy.data.materials:
                    new_material = bpy.data.materials.new(name=material_name)
                    new_material.use_nodes = True  # Enable node-based shading (optional, matching your original script)
                else:
                    new_material = bpy.data.materials[material_name]
                # Add the material to the object as a new slot
                obj.data.materials.append(new_material)
                print(f"Assigned material '{material_name}' to {obj.name} and removed existing material slots.")
            except Exception as e:
                print(f"Error assigning material to {obj.name}: {e}")
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_61'] = bpy.data.materials['KIRI_3DGS_Render_Material']
        if bpy.context.scene.sna_kiri3dgs_quads_and_uv_reset:
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
            bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
            bpy.ops.mesh.dissolve_limited('INVOKE_DEFAULT', )
            bpy.ops.uv.reset('INVOKE_DEFAULT', )
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
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
    op = box_5C3FC.operator('sna.dgs_import_settings_bf139', text='Import PLY As Splats', icon_value=string_to_icon('IMPORT'), emboss=True, depress=False)


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


class SNA_OT_Dgs_Import_Settings_Bf139(bpy.types.Operator):
    bl_idname = "sna.dgs_import_settings_bf139"
    bl_label = "3DGS Import Settings"
    bl_description = "Imports a .ply file and adds a series of 3DGS modifiers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.sna.import_ply_as_splats_8458e('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_D19E8 = layout.box()
        box_D19E8.alert = False
        box_D19E8.enabled = True
        box_D19E8.active = True
        box_D19E8.use_property_split = False
        box_D19E8.use_property_decorate = False
        box_D19E8.alignment = 'Expand'.upper()
        box_D19E8.scale_x = 1.0
        box_D19E8.scale_y = 1.0
        if not True: box_D19E8.operator_context = "EXEC_DEFAULT"
        box_599AC = box_D19E8.box()
        box_599AC.alert = True
        box_599AC.enabled = True
        box_599AC.active = True
        box_599AC.use_property_split = False
        box_599AC.use_property_decorate = False
        box_599AC.alignment = 'Expand'.upper()
        box_599AC.scale_x = 1.0
        box_599AC.scale_y = 1.0
        if not True: box_599AC.operator_context = "EXEC_DEFAULT"
        box_599AC.label(text='Do not apply rotation or scale transforms', icon_value=133)
        box_599AC.label(text="         using Blender's native Appy Scale / Rotation", icon_value=0)
        box_599AC.label(text='         if you want to apply transforms, use the', icon_value=0)
        box_599AC.label(text='         Apply 3DGS Transforms and Colour function', icon_value=0)
        box_D19E8.label(text='Import Settings', icon_value=string_to_icon('IMPORT'))
        box_910F6 = box_D19E8.box()
        box_910F6.alert = False
        box_910F6.enabled = True
        box_910F6.active = True
        box_910F6.use_property_split = False
        box_910F6.use_property_decorate = False
        box_910F6.alignment = 'Expand'.upper()
        box_910F6.scale_x = 1.0
        box_910F6.scale_y = 1.0
        if not True: box_910F6.operator_context = "EXEC_DEFAULT"
        box_910F6.prop(bpy.context.scene, 'sna_kiri3dgs_quads_and_uv_reset', text='UV Reset', icon_value=0, emboss=True, toggle=True)
        if bpy.context.scene.sna_kiri3dgs_quads_and_uv_reset:
            box_6806A = box_910F6.box()
            box_6806A.alert = True
            box_6806A.enabled = True
            box_6806A.active = True
            box_6806A.use_property_split = False
            box_6806A.use_property_decorate = False
            box_6806A.alignment = 'Expand'.upper()
            box_6806A.scale_x = 1.0
            box_6806A.scale_y = 1.0
            if not True: box_6806A.operator_context = "EXEC_DEFAULT"
            box_6806A.label(text='This can make the import process take considerably longer for large scans', icon_value=string_to_icon('INFO'))

    def invoke(self, context, event):
        bpy.context.scene.eevee.use_taa_reprojection = False
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
        for i_67C88 in range(len(bpy.context.scene.objects)):
            bpy.context.scene.objects[i_67C88].select_set(state=False, )
        return context.window_manager.invoke_props_dialog(self, width=500)


def sna_append_and_add_geo_nodes_function_execute_8BC99(Node_Group_Name, Modifier_Name, Object):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend') + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_CAEF1 = None if not new_data else new_data[0]
    modifier_B4020 = Object.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_B4020.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_B4020


class SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_77E7E(bpy.types.Panel):
    bl_label = '3DGS Render by KIRI Engine'
    bl_idname = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_77E7E'
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


class SNA_OT_Set_Menu_Active_Mode_6Dc45(bpy.types.Operator):
    bl_idname = "sna.set_menu_active_mode_6dc45"
    bl_label = "Set Menu Active Mode"
    bl_description = "Sets the active interface mode"
    bl_options = {"REGISTER", "UNDO"}
    sna_active_mode_set: bpy.props.StringProperty(name='Active_Mode_Set', description='', default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_set_active_mode_function_execute_64515(self.sna_active_mode_set)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_set_active_mode_function_execute_64515(Active_Mode_Set):
    bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode = Active_Mode_Set


def sna_mesh_to_3dgs_function_interface_8DDDC(layout_function, ):
    box_58AE4 = layout_function.box()
    box_58AE4.alert = True
    box_58AE4.enabled = True
    box_58AE4.active = True
    box_58AE4.use_property_split = False
    box_58AE4.use_property_decorate = False
    box_58AE4.alignment = 'Expand'.upper()
    box_58AE4.scale_x = 1.0
    box_58AE4.scale_y = 1.0
    if not True: box_58AE4.operator_context = "EXEC_DEFAULT"
    box_58AE4.label(text='Linux and Mac are not supported', icon_value=string_to_icon('INFO'))
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
    box_9766A.prop(bpy.context.scene, 'sna_mesh2gs__validate_meshtexturemtl', text='Validate Mesh, Texture and .MTL', icon_value=0, emboss=True)
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
    op = box_8C171.operator('sna.mesh_2_gs_3dfed', text='Select .OBJ', icon_value=0, emboss=True, depress=False)


class SNA_OT_Mesh_2_Gs_3Dfed(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.mesh_2_gs_3dfed"
    bl_label = "Mesh 2 GS"
    bl_description = "Convert a chosen .OBJ to 3DGS .PLY"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.obj', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_mesh2gs__validate_meshtexturemtl:
            obj_path = bpy.path.abspath(self.filepath)
            face_count = None
            triangular_face_count = None
            non_triangular_face_count = None
            is_triangulated = None
            error_message = None
            #import bpy  # For text editor
            # Set the path to your .obj file here
            #obj_path = "/path/to/your/file.obj"  # CHANGE THIS TO YOUR FILE PATH
            # Initialize variables
            face_count = 0
            triangular_face_count = 0
            non_triangular_face_count = 0
            is_triangulated = True
            error_message = None
            # Check if file exists
            if not os.path.exists(obj_path):
                is_triangulated = False
                error_message = "File not found"
                triangular_face_count = 0
                non_triangular_face_count = 0
            else:
                # Try to read the file
                try:
                    with open(obj_path, 'r') as file:
                        for line in file:
                            line = line.strip()
                            if line.startswith('f '):
                                face_count += 1
                                # Split the face line and count vertices
                                vertices = [v.split('/')[0] for v in line[2:].split()]
                                if len(vertices) == 3:
                                    triangular_face_count += 1
                                else:
                                    non_triangular_face_count += 1
                    is_triangulated = non_triangular_face_count == 0
                except Exception as e:
                    is_triangulated = False
                    error_message = str(e)
                    triangular_face_count = 0
                    non_triangular_face_count = 0
            # Named output variables for Serpens
            TRIANGULAR_FACE_COUNT = triangular_face_count
            NON_TRIANGULAR_FACE_COUNT = non_triangular_face_count
            IS_TRIANGULATED = is_triangulated
            TOTAL_FACE_COUNT = face_count
            ERROR_MESSAGE = error_message
            # Print results (optional, can be removed if using only Serpens)
            print(f"TRIANGULAR_FACE_COUNT: {TRIANGULAR_FACE_COUNT}")
            print(f"NON_TRIANGULAR_FACE_COUNT: {NON_TRIANGULAR_FACE_COUNT}")
            print(f"IS_TRIANGULATED: {IS_TRIANGULATED}")
            print(f"TOTAL_FACE_COUNT: {TOTAL_FACE_COUNT}")
            if ERROR_MESSAGE:
                print(f"ERROR_MESSAGE: {ERROR_MESSAGE}")
            if is_triangulated:
                obj_path = bpy.path.abspath(self.filepath)
                HAS_MTL = None
                HAS_TEXTURE = None
                ALL_FILES_SAME_FOLDER = None
                #import bpy  # Included for Blender compatibility
                # Set the path to your .obj file here
                #obj_path = "/path/to/your/file.obj"  # CHANGE THIS TO YOUR FILE PATH
                # Initialize output variables
                HAS_MTL = False
                MTL_PATH = ""
                HAS_TEXTURE = False
                TEXTURE_PATHS = []
                TEXTURE_EXTENSIONS = []
                ALL_FILES_SAME_FOLDER = False
                ERROR_MESSAGE = None
                try:
                    # Check if obj file exists
                    if not os.path.exists(obj_path):
                        ERROR_MESSAGE = "OBJ file not found"
                    else:
                        obj_dir = os.path.dirname(os.path.abspath(obj_path))
                        # Parse OBJ file to find MTL reference
                        mtl_filename = None
                        with open(obj_path, 'r', errors='replace') as obj_file:
                            for line in obj_file:
                                line = line.strip()
                                if line.startswith('mtllib '):
                                    mtl_filename = line[7:].strip()  # Remove 'mtllib ' prefix
                                    break
                        # Check if MTL file exists
                        if mtl_filename:
                            # Handle relative paths in the OBJ file
                            if os.path.isabs(mtl_filename):
                                mtl_path = mtl_filename
                            else:
                                mtl_path = os.path.join(obj_dir, mtl_filename)
                            if os.path.exists(mtl_path):
                                HAS_MTL = True
                                MTL_PATH = mtl_path
                                mtl_dir = os.path.dirname(os.path.abspath(mtl_path))
                                # Parse MTL file to find texture references
                                with open(mtl_path, 'r', errors='replace') as mtl_file:
                                    for line in mtl_file:
                                        line = line.strip()
                                        # Look for map_Kd (diffuse color texture)
                                        if line.startswith('map_Kd '):
                                            parts = line.split(' ', 1)
                                            if len(parts) > 1:
                                                texture_filename = parts[1].strip()
                                                # Handle relative paths in the MTL file
                                                if os.path.isabs(texture_filename):
                                                    texture_path = texture_filename
                                                else:
                                                    texture_path = os.path.join(mtl_dir, texture_filename)
                                                if os.path.exists(texture_path):
                                                    HAS_TEXTURE = True
                                                    TEXTURE_PATHS.append(texture_path)
                                                    # Get the extension
                                                    _, extension = os.path.splitext(texture_filename)
                                                    TEXTURE_EXTENSIONS.append(extension.lstrip('.'))
                                # Check if all files are in the same folder
                                if HAS_MTL:
                                    # Start with checking if OBJ and MTL are in the same folder
                                    ALL_FILES_SAME_FOLDER = (os.path.normcase(obj_dir) == os.path.normcase(mtl_dir))
                                    # Then check if all textures are also in the same folder
                                    if ALL_FILES_SAME_FOLDER and HAS_TEXTURE:
                                        for texture_path in TEXTURE_PATHS:
                                            texture_dir = os.path.dirname(os.path.abspath(texture_path))
                                            if os.path.normcase(obj_dir) != os.path.normcase(texture_dir):
                                                ALL_FILES_SAME_FOLDER = False
                                                break
                except Exception as e:
                    ERROR_MESSAGE = str(e)
                # Print results (optional, can be removed if using only Serpens)
                print(f"HAS_MTL: {HAS_MTL}")
                print(f"MTL_PATH: {MTL_PATH}")
                print(f"HAS_TEXTURE: {HAS_TEXTURE}")
                print(f"TEXTURE_PATHS: {TEXTURE_PATHS}")
                print(f"TEXTURE_EXTENSIONS: {TEXTURE_EXTENSIONS}")
                print(f"ALL_FILES_SAME_FOLDER: {ALL_FILES_SAME_FOLDER}")
                if ERROR_MESSAGE:
                    print(f"ERROR_MESSAGE: {ERROR_MESSAGE}")
                if ALL_FILES_SAME_FOLDER:
                    obj_path = bpy.path.abspath(self.filepath)
                    output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
                    exe_path = bpy.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'mesh2gs'))
                    import platform
                    import sys
                    # Get paths
                    #obj_path = bpy.path.abspath(self.filepath)
                    #output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
                    #exe_path = bpy.path.abspath(bpy.context.scene.sna_mesh2gs_exe_path)
                    os_name = platform.system()
                    if(sys.platform == 'darwin'):
                        print("mac")
                        exe_path = os.path.join(exe_path, "mac", "mesh2gs")
                        os.chmod(exe_path, 0o777)
                    elif(sys.platform.startswith('win')):
                        print("win")
                        exe_path = os.path.join(exe_path, "win", "mesh2gs_win.exe")
                    else:
                        raise RuntimeError("Unsupported operating system. Only support mac and win!")
                    command = [
                        exe_path,
                        "--mesh",
                        obj_path,
                        "--output_path",
                        output_path
                    ]
                    # Debug prints
                    print("Final exe_path:", exe_path)
                    print("Full command:", command)
                    print("Path exists check:", os.path.exists(exe_path))
                    begin = time()
                    try:
                        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
                    except Exception as e:
                        raise RuntimeError(e)
                    end = time()
                    print("run successfully. Save in", output_path)
                    print("cost " + str(end-begin) + "s")
                    open_folder_skd(os.path.dirname(bpy.path.abspath(self.filepath)))
                    open_folder_skd(os.path.dirname(bpy.path.abspath(self.filepath)))
                    open_folder_skd(os.path.dirname(bpy.path.abspath(self.filepath)))
                else:
                    self.report({'ERROR'}, message='File structure is incorrect - see documentation')
            else:
                self.report({'WARNING'}, message='Mesh is not triangulated?')
        else:
            obj_path = bpy.path.abspath(self.filepath)
            output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
            exe_path = bpy.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'mesh2gs'))
            import platform
            import sys
            # Get paths
            #obj_path = bpy.path.abspath(self.filepath)
            #output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
            #exe_path = bpy.path.abspath(bpy.context.scene.sna_mesh2gs_exe_path)
            os_name = platform.system()
            if(sys.platform == 'darwin'):
                print("mac")
                exe_path = os.path.join(exe_path, "mac", "mesh2gs")
                os.chmod(exe_path, 0o777)
            elif(sys.platform.startswith('win')):
                print("win")
                exe_path = os.path.join(exe_path, "win", "mesh2gs_win.exe")
            else:
                raise RuntimeError("Unsupported operating system. Only support mac and win!")
            command = [
                exe_path,
                "--mesh",
                obj_path,
                "--output_path",
                output_path
            ]
            # Debug prints
            print("Final exe_path:", exe_path)
            print("Full command:", command)
            print("Path exists check:", os.path.exists(exe_path))
            begin = time()
            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
            except Exception as e:
                raise RuntimeError(e)
            end = time()
            print("run successfully. Save in", output_path)
            print("cost " + str(end-begin) + "s")
            open_folder_skd(os.path.dirname(bpy.path.abspath(self.filepath)))
            open_folder_skd(os.path.dirname(bpy.path.abspath(self.filepath)))
            open_folder_skd(os.path.dirname(bpy.path.abspath(self.filepath)))
        return {"FINISHED"}


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
    layout_function.separator(factor=1.0)
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
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_camera_cull and 'OBJECT'==bpy.context.mode):
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
    else:
        box_36F76 = layout_function.box()
        box_36F76.alert = False
        box_36F76.enabled = 'OBJECT'==bpy.context.mode
        box_36F76.active = True
        box_36F76.use_property_split = False
        box_36F76.use_property_decorate = False
        box_36F76.alignment = 'Expand'.upper()
        box_36F76.scale_x = 1.0
        box_36F76.scale_y = 1.0
        if not True: box_36F76.operator_context = "EXEC_DEFAULT"
        row_25C78 = box_36F76.row(heading='', align=False)
        row_25C78.alert = False
        row_25C78.enabled = True
        row_25C78.active = True
        row_25C78.use_property_split = False
        row_25C78.use_property_decorate = False
        row_25C78.scale_x = 1.0
        row_25C78.scale_y = 1.0
        row_25C78.alignment = 'Expand'.upper()
        row_25C78.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_25C78.label(text='Camera Cull Modifier Is Missing', icon_value=0)
        op = row_25C78.operator('sna.append_and_add_geometry_node_modifier_c2492', text='', icon_value=45, emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Camera_Cull_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Camera_Cull_GN'
        op.sna_property_to_update = 'CameraCull'
    layout_function.separator(factor=1.0)
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
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_decimate and 'OBJECT'==bpy.context.mode):
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
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_decimate:
            col_5CC38 = box_A8194.column(heading='', align=False)
            col_5CC38.alert = False
            col_5CC38.enabled = True
            col_5CC38.active = True
            col_5CC38.use_property_split = False
            col_5CC38.use_property_decorate = False
            col_5CC38.scale_x = 1.0
            col_5CC38.scale_y = 1.0
            col_5CC38.alignment = 'Expand'.upper()
            col_5CC38.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_29E12 = '["' + str('Socket_18' + '"]') 
            col_5CC38.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_29E12, text='Decimate Masking', icon_value=0, emboss=True, toggle=True)
            if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_18']:
                col_287D9 = col_5CC38.column(heading='', align=False)
                col_287D9.alert = False
                col_287D9.enabled = True
                col_287D9.active = True
                col_287D9.use_property_split = False
                col_287D9.use_property_decorate = False
                col_287D9.scale_x = 1.0
                col_287D9.scale_y = 1.0
                col_287D9.alignment = 'Expand'.upper()
                col_287D9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                attr_2CA2E = '["' + str('Socket_20' + '"]') 
                col_287D9.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_2CA2E, text='', icon_value=0, emboss=True, toggle=True)
                attr_52425 = '["' + str('Socket_21' + '"]') 
                col_287D9.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_52425, text='', icon_value=0, emboss=True, toggle=True)
                if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_20'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN']['Socket_20'] == 3)):
                    attr_07523 = '["' + str('Socket_22' + '"]') 
                    col_287D9.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Decimate_GN'], attr_07523, text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_7C03A = layout_function.box()
        box_7C03A.alert = False
        box_7C03A.enabled = 'OBJECT'==bpy.context.mode
        box_7C03A.active = True
        box_7C03A.use_property_split = False
        box_7C03A.use_property_decorate = False
        box_7C03A.alignment = 'Expand'.upper()
        box_7C03A.scale_x = 1.0
        box_7C03A.scale_y = 1.0
        if not True: box_7C03A.operator_context = "EXEC_DEFAULT"
        row_022DB = box_7C03A.row(heading='', align=False)
        row_022DB.alert = False
        row_022DB.enabled = True
        row_022DB.active = True
        row_022DB.use_property_split = False
        row_022DB.use_property_decorate = False
        row_022DB.scale_x = 1.0
        row_022DB.scale_y = 1.0
        row_022DB.alignment = 'Expand'.upper()
        row_022DB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_022DB.label(text='Decimate Modifier Is Missing', icon_value=0)
        op = row_022DB.operator('sna.append_and_add_geometry_node_modifier_c2492', text='', icon_value=45, emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Decimate_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Decimate_GN'
        op.sna_property_to_update = 'CameraCull'
    layout_function.separator(factor=1.0)
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
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_crop_box and 'OBJECT'==bpy.context.mode):
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
    else:
        box_B0857 = layout_function.box()
        box_B0857.alert = False
        box_B0857.enabled = 'OBJECT'==bpy.context.mode
        box_B0857.active = True
        box_B0857.use_property_split = False
        box_B0857.use_property_decorate = False
        box_B0857.alignment = 'Expand'.upper()
        box_B0857.scale_x = 1.0
        box_B0857.scale_y = 1.0
        if not True: box_B0857.operator_context = "EXEC_DEFAULT"
        row_E7E64 = box_B0857.row(heading='', align=False)
        row_E7E64.alert = False
        row_E7E64.enabled = True
        row_E7E64.active = True
        row_E7E64.use_property_split = False
        row_E7E64.use_property_decorate = False
        row_E7E64.scale_x = 1.0
        row_E7E64.scale_y = 1.0
        row_E7E64.alignment = 'Expand'.upper()
        row_E7E64.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_E7E64.label(text='Crop Box Modifier Is Missing', icon_value=0)
        op = row_E7E64.operator('sna.append_and_add_geometry_node_modifier_c2492', text='', icon_value=45, emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Crop_Box_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Crop_Box_GN'
        op.sna_property_to_update = 'CameraCull'
    layout_function.separator(factor=1.0)
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
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_colour_edit and 'OBJECT'==bpy.context.mode):
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
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_colour_edit:
            col_495F5 = box_1CE63.column(heading='', align=False)
            col_495F5.alert = False
            col_495F5.enabled = True
            col_495F5.active = True
            col_495F5.use_property_split = False
            col_495F5.use_property_decorate = False
            col_495F5.scale_x = 1.0
            col_495F5.scale_y = 1.0
            col_495F5.alignment = 'Expand'.upper()
            col_495F5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_050AB = '["' + str('Socket_11' + '"]') 
            col_495F5.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_050AB, text='Colour Edit Masking', icon_value=0, emboss=True, toggle=True)
            if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_11']:
                col_AC53E = col_495F5.column(heading='', align=False)
                col_AC53E.alert = False
                col_AC53E.enabled = True
                col_AC53E.active = True
                col_AC53E.use_property_split = False
                col_AC53E.use_property_decorate = False
                col_AC53E.scale_x = 1.0
                col_AC53E.scale_y = 1.0
                col_AC53E.alignment = 'Expand'.upper()
                col_AC53E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                attr_6048B = '["' + str('Socket_8' + '"]') 
                col_AC53E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_6048B, text='', icon_value=0, emboss=True, toggle=True)
                attr_2ABCB = '["' + str('Socket_9' + '"]') 
                col_AC53E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_2ABCB, text='', icon_value=0, emboss=True, toggle=True)
                if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_8'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN']['Socket_8'] == 3)):
                    attr_74EE2 = '["' + str('Socket_12' + '"]') 
                    col_AC53E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Colour_Edit_GN'], attr_74EE2, text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_6D0A1 = layout_function.box()
        box_6D0A1.alert = False
        box_6D0A1.enabled = 'OBJECT'==bpy.context.mode
        box_6D0A1.active = True
        box_6D0A1.use_property_split = False
        box_6D0A1.use_property_decorate = False
        box_6D0A1.alignment = 'Expand'.upper()
        box_6D0A1.scale_x = 1.0
        box_6D0A1.scale_y = 1.0
        if not True: box_6D0A1.operator_context = "EXEC_DEFAULT"
        row_88971 = box_6D0A1.row(heading='', align=False)
        row_88971.alert = False
        row_88971.enabled = True
        row_88971.active = True
        row_88971.use_property_split = False
        row_88971.use_property_decorate = False
        row_88971.scale_x = 1.0
        row_88971.scale_y = 1.0
        row_88971.alignment = 'Expand'.upper()
        row_88971.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_88971.label(text='Colour Edit Modifier Is Missing', icon_value=0)
        op = row_88971.operator('sna.append_and_add_geometry_node_modifier_c2492', text='', icon_value=45, emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Colour_Edit_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Colour_Edit_GN'
        op.sna_property_to_update = 'CameraCull'
    layout_function.separator(factor=1.0)
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Remove_By Size_GN' in bpy.context.view_layer.objects.active.modifiers):
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
        row_520DB.prop(bpy.context.view_layer.objects.active, 'sna_kiri3dgs_modifier_enable_remove_by_size', text=('Remove by Size' if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_by_size else 'Enable Remove By Size'), icon_value=0, emboss=True, toggle=True)
        if (bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_by_size and 'OBJECT'==bpy.context.mode):
            op = row_520DB.operator('sna.apply_remove_by_size_modifier_3fdf1', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'checked-5690873-white.png')), emboss=True, depress=False)
            op = row_520DB.operator('sna.remove_remove_by_size_modifier_95a21', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'cancel-7207310 - white.png')), emboss=True, depress=False)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_by_size:
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
            col_F2224.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_5CF96, text='Remove Small Faces', icon_value=0, emboss=True, toggle=True)
            if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_6']:
                attr_5EC3E = '["' + str('Socket_5' + '"]') 
                col_F2224.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_5EC3E, text='Small Face Threshold', icon_value=0, emboss=True)
            attr_0BF6C = '["' + str('Socket_11' + '"]') 
            col_F2224.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_0BF6C, text='Remove By Long Edges', icon_value=0, emboss=True, toggle=True)
            if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_11']:
                attr_C6B2C = '["' + str('Socket_12' + '"]') 
                col_F2224.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_C6B2C, text='Edge LengthThreshold', icon_value=0, emboss=True)
        if bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_by_size:
            col_B2AA1 = box_2E82D.column(heading='', align=False)
            col_B2AA1.alert = False
            col_B2AA1.enabled = True
            col_B2AA1.active = True
            col_B2AA1.use_property_split = False
            col_B2AA1.use_property_decorate = False
            col_B2AA1.scale_x = 1.0
            col_B2AA1.scale_y = 1.0
            col_B2AA1.alignment = 'Expand'.upper()
            col_B2AA1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_1D68E = '["' + str('Socket_13' + '"]') 
            col_B2AA1.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_1D68E, text='Remove By Size Masking', icon_value=0, emboss=True, toggle=True)
            if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_13']:
                col_64BFB = col_B2AA1.column(heading='', align=False)
                col_64BFB.alert = False
                col_64BFB.enabled = True
                col_64BFB.active = True
                col_64BFB.use_property_split = False
                col_64BFB.use_property_decorate = False
                col_64BFB.scale_x = 1.0
                col_64BFB.scale_y = 1.0
                col_64BFB.alignment = 'Expand'.upper()
                col_64BFB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                attr_6D9F4 = '["' + str('Socket_15' + '"]') 
                col_64BFB.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_6D9F4, text='', icon_value=0, emboss=True, toggle=True)
                attr_178B7 = '["' + str('Socket_14' + '"]') 
                col_64BFB.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_178B7, text='', icon_value=0, emboss=True, toggle=True)
                if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_15'] == 2) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN']['Socket_15'] == 3)):
                    attr_1ED67 = '["' + str('Socket_16' + '"]') 
                    col_64BFB.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], attr_1ED67, text='Distance Threshold', icon_value=0, emboss=True, toggle=True)
    else:
        box_A5A30 = layout_function.box()
        box_A5A30.alert = False
        box_A5A30.enabled = 'OBJECT'==bpy.context.mode
        box_A5A30.active = True
        box_A5A30.use_property_split = False
        box_A5A30.use_property_decorate = False
        box_A5A30.alignment = 'Expand'.upper()
        box_A5A30.scale_x = 1.0
        box_A5A30.scale_y = 1.0
        if not True: box_A5A30.operator_context = "EXEC_DEFAULT"
        row_948AD = box_A5A30.row(heading='', align=False)
        row_948AD.alert = False
        row_948AD.enabled = True
        row_948AD.active = True
        row_948AD.use_property_split = False
        row_948AD.use_property_decorate = False
        row_948AD.scale_x = 1.0
        row_948AD.scale_y = 1.0
        row_948AD.alignment = 'Expand'.upper()
        row_948AD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_948AD.label(text='Remove By Size Modifier Is Missing', icon_value=0)
        op = row_948AD.operator('sna.append_and_add_geometry_node_modifier_c2492', text='', icon_value=45, emboss=True, depress=False)
        op.sna_node_group_name = 'KIRI_3DGS_Remove_By Size_GN'
        op.sna_modifier_name = 'KIRI_3DGS_Remove_By Size_GN'
        op.sna_property_to_update = 'CameraCull'


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


class SNA_OT_Remove_Remove_By_Size_Modifier_95A21(bpy.types.Operator):
    bl_idname = "sna.remove_remove_by_size_modifier_95a21"
    bl_label = "Remove Remove By Size Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Remove_By Size_GN'], )
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
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend') + r'\Object', filename='Wire Sphere', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_69F39 = None if not new_data else new_data[0]
        appended_69F39.location = bpy.context.scene.cursor.location
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
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend') + r'\Object', filename='Wire Cube', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_8B494 = None if not new_data else new_data[0]
        appended_8B494.location = bpy.context.scene.cursor.location
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


class SNA_OT_Apply_Remove_By_Size_Modifier_3Fdf1(bpy.types.Operator):
    bl_idname = "sna.apply_remove_by_size_modifier_3fdf1"
    bl_label = "Apply Remove By Size Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Remove_By Size_GN'
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


class SNA_OT_Append_And_Add_Geometry_Node_Modifier_C2492(bpy.types.Operator):
    bl_idname = "sna.append_and_add_geometry_node_modifier_c2492"
    bl_label = "Append and add geometry node modifier"
    bl_description = "Adds a geometry node modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}
    sna_node_group_name: bpy.props.StringProperty(name='Node Group Name', description='', default='', subtype='NONE', maxlen=0)
    sna_modifier_name: bpy.props.StringProperty(name='Modifier Name', description='', default='', subtype='NONE', maxlen=0)

    def sna_property_to_update_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_property_to_update: bpy.props.EnumProperty(name='Property To Update', description='', items=[('CameraCull', 'CameraCull', '', 0, 0), ('Decimate', 'Decimate', '', 0, 1), ('CropBox', 'CropBox', '', 0, 2), ('ColourEdit', 'ColourEdit', '', 0, 3), ('EditBySize', 'EditBySize', '', 0, 4)])

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        created_modifier_0_7a9a7 = sna_append_and_add_geo_nodes_function_execute_8BC99(self.sna_node_group_name, self.sna_node_group_name, bpy.context.view_layer.objects.active)
        for i_1A879 in range(len(bpy.context.view_layer.objects.active.modifiers)):
            if (bpy.context.view_layer.objects.active.modifiers[i_1A879] == created_modifier_0_7a9a7):
                bpy.context.view_layer.objects.active.modifiers.move(from_index=i_1A879, to_index=0, )
        if self.sna_property_to_update == "CameraCull":
            bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_camera_cull = True
        elif self.sna_property_to_update == "Decimate":
            bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_decimate = True
        elif self.sna_property_to_update == "CropBox":
            bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_crop_box = True
        elif self.sna_property_to_update == "ColourEdit":
            bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_colour_edit = True
        elif self.sna_property_to_update == "EditBySize":
            bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_remove_by_size = True
        else:
            pass
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
                col_D7973.separator(factor=1.0)
                op = col_D7973.operator('sna.create_omniview_object_909fd', text='Create Omniview Object', icon_value=0, emboss=True, depress=False)
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
                dgs_render__omniview['sna_omniviewobjectsformerge'] = []
                dgs_render__omniview['sna_omniviewbase'] = None
                dgs_render__omniview['sna_omniviewmodifierlist'] = []
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
                dgs_render__omniview['sna_omniviewbase'] = bpy.context.view_layer.objects.active
                for i_A8F53 in range(len(bpy.data.objects)):
                    bpy.data.objects[i_A8F53].select_set(state=False, view_layer=bpy.context.view_layer, )
                dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
                bpy.context.view_layer.objects.active = dgs_render__omniview['sna_omniviewbase']
                dgs_render__omniview['sna_omniviewbase'].modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 0
                for i_35F95 in range(len(dgs_render__omniview['sna_omniviewbase'].modifiers)):
                    dgs_render__omniview['sna_omniviewmodifierlist'].append(dgs_render__omniview['sna_omniviewbase'].modifiers[i_35F95])
                for i_C4833 in range(len(dgs_render__omniview['sna_omniviewmodifierlist'])):
                    if (dgs_render__omniview['sna_omniviewmodifierlist'][i_C4833].name == 'KIRI_3DGS_Animate_GN'):
                        dgs_render__omniview['sna_omniviewmodifierlist'][i_C4833]['Socket_35'] = True
                    if (dgs_render__omniview['sna_omniviewmodifierlist'][i_C4833].name == 'KIRI_3DGS_Render_GN'):
                        pass
                    else:
                        dgs_render__omniview['sna_omniviewbase'].modifiers.remove(modifier=dgs_render__omniview['sna_omniviewmodifierlist'][i_C4833], )

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
                        ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                        dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                        if bpy.context and bpy.context.screen:
                            for a in bpy.context.screen.areas:
                                a.tag_redraw()
                        source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                        dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                        for i_4B7A6 in range(len(bpy.context.view_layer.objects.selected)):
                            bpy.context.view_layer.objects.selected[i_4B7A6].select_set(state=False, view_layer=bpy.context.view_layer, )
                        dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
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
                            ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                            dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                            if bpy.context and bpy.context.screen:
                                for a in bpy.context.screen.areas:
                                    a.tag_redraw()
                            source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                            dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                            for i_DFF57 in range(len(bpy.context.view_layer.objects.selected)):
                                bpy.context.view_layer.objects.selected[i_DFF57].select_set(state=False, view_layer=bpy.context.view_layer, )
                            dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
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
                                ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                                dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                if bpy.context and bpy.context.screen:
                                    for a in bpy.context.screen.areas:
                                        a.tag_redraw()
                                source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                                dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                                for i_95077 in range(len(bpy.context.view_layer.objects.selected)):
                                    bpy.context.view_layer.objects.selected[i_95077].select_set(state=False, view_layer=bpy.context.view_layer, )
                                if ((bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '5 Axes') or (bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '7 Axes') or (bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '9 Axes')):
                                    dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
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
                                        print(dgs_render__omniview['sna_omniviewbase'].name)
                                        ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                                        dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                        if bpy.context and bpy.context.screen:
                                            for a in bpy.context.screen.areas:
                                                a.tag_redraw()
                                        source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                                        dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                                        for i_2AD47 in range(len(bpy.context.view_layer.objects.selected)):
                                            bpy.context.view_layer.objects.selected[i_2AD47].select_set(state=False, view_layer=bpy.context.view_layer, )
                                        dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
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
                                            ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                                            dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                            if bpy.context and bpy.context.screen:
                                                for a in bpy.context.screen.areas:
                                                    a.tag_redraw()
                                            source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                                            dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                                            for i_86603 in range(len(bpy.context.view_layer.objects.selected)):
                                                bpy.context.view_layer.objects.selected[i_86603].select_set(state=False, view_layer=bpy.context.view_layer, )
                                            if ((bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '7 Axes') or (bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '9 Axes')):
                                                dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
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
                                                    ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                                                    dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                                    if bpy.context and bpy.context.screen:
                                                        for a in bpy.context.screen.areas:
                                                            a.tag_redraw()
                                                    source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                                                    dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                                                    for i_147A0 in range(len(bpy.context.view_layer.objects.selected)):
                                                        bpy.context.view_layer.objects.selected[i_147A0].select_set(state=False, view_layer=bpy.context.view_layer, )
                                                    dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
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
                                                        ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                                                        dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                                        if bpy.context and bpy.context.screen:
                                                            for a in bpy.context.screen.areas:
                                                                a.tag_redraw()
                                                        source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                                                        dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                                                        for i_B661A in range(len(bpy.context.view_layer.objects.selected)):
                                                            bpy.context.view_layer.objects.selected[i_B661A].select_set(state=False, view_layer=bpy.context.view_layer, )
                                                        if (bpy.context.scene.sna_kiri3dgs_omnisplat_axes_count == '9 Axes'):
                                                            dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
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
                                                                ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                                                                dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                                                if bpy.context and bpy.context.screen:
                                                                    for a in bpy.context.screen.areas:
                                                                        a.tag_redraw()
                                                                source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                                                                dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                                                                for i_95593 in range(len(bpy.context.view_layer.objects.selected)):
                                                                    bpy.context.view_layer.objects.selected[i_95593].select_set(state=False, view_layer=bpy.context.view_layer, )
                                                                dgs_render__omniview['sna_omniviewbase'].select_set(state=True, view_layer=bpy.context.view_layer, )
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
                                                                    ObjectName = dgs_render__omniview['sna_omniviewbase'].name
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
                                                                    dgs_render__omniview['sna_omniviewbase'].update_tag(refresh={'OBJECT'}, )
                                                                    if bpy.context and bpy.context.screen:
                                                                        for a in bpy.context.screen.areas:
                                                                            a.tag_redraw()
                                                                    source_obj_name = dgs_render__omniview['sna_omniviewbase'].name
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
                                                                    dgs_render__omniview['sna_omniviewobjectsformerge'].append(new_object_name)
                                                                    for i_80970 in range(len(bpy.context.view_layer.objects.selected)):
                                                                        bpy.context.view_layer.objects.selected[i_80970].select_set(state=False, view_layer=bpy.context.view_layer, )
                                                                    for i_D0394 in range(len(dgs_render__omniview['sna_omniviewobjectsformerge'])):
                                                                        bpy.data.objects[dgs_render__omniview['sna_omniviewobjectsformerge'][i_D0394]].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                                        bpy.context.view_layer.objects.active = bpy.data.objects[dgs_render__omniview['sna_omniviewobjectsformerge'][i_D0394]]
                                                                    bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
                                                                    bpy.ops.object.join('INVOKE_DEFAULT', )
                                                                    bpy.data.objects.remove(object=dgs_render__omniview['sna_omniviewbase'], do_unlink=True, do_id_user=True, do_ui_user=True, )
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
                                                                    geonodemodreturn_0_90019 = sna_add_geo_nodes__append_group_2D522_90019(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend'), 'KIRI_3DGS_Sorter_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Sorter_GN')
                                                                bpy.app.timers.register(delayed_FCFF0, first_interval=0.10000000149011612)
                                                            bpy.app.timers.register(delayed_EDEBE, first_interval=0.10000000149011612)
                                                        else:
                                                            for i_44E24 in range(len(dgs_render__omniview['sna_omniviewobjectsformerge'])):
                                                                bpy.data.objects[dgs_render__omniview['sna_omniviewobjectsformerge'][i_44E24]].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                                bpy.context.view_layer.objects.active = bpy.data.objects[dgs_render__omniview['sna_omniviewobjectsformerge'][i_44E24]]
                                                            bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
                                                            bpy.ops.object.join('INVOKE_DEFAULT', )
                                                            bpy.data.objects.remove(object=dgs_render__omniview['sna_omniviewbase'], do_unlink=True, do_id_user=True, do_ui_user=True, )
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
                                                            geonodemodreturn_0_9d3b3 = sna_add_geo_nodes__append_group_2D522_9D3B3(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend'), 'KIRI_3DGS_Sorter_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Sorter_GN')
                                                    bpy.app.timers.register(delayed_FDA7B, first_interval=0.10000000149011612)
                                                bpy.app.timers.register(delayed_096EF, first_interval=0.10000000149011612)
                                            else:
                                                for i_3BF64 in range(len(dgs_render__omniview['sna_omniviewobjectsformerge'])):
                                                    bpy.data.objects[dgs_render__omniview['sna_omniviewobjectsformerge'][i_3BF64]].select_set(state=True, view_layer=bpy.context.view_layer, )
                                                    bpy.context.view_layer.objects.active = bpy.data.objects[dgs_render__omniview['sna_omniviewobjectsformerge'][i_3BF64]]
                                                bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
                                                bpy.ops.object.join('INVOKE_DEFAULT', )
                                                bpy.data.objects.remove(object=dgs_render__omniview['sna_omniviewbase'], do_unlink=True, do_id_user=True, do_ui_user=True, )
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
                                                geonodemodreturn_0_e5645 = sna_add_geo_nodes__append_group_2D522_E5645(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend'), 'KIRI_3DGS_Sorter_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Sorter_GN')
                                        bpy.app.timers.register(delayed_5E158, first_interval=0.10000000149011612)
                                    bpy.app.timers.register(delayed_0CFF3, first_interval=0.10000000149011612)
                                else:
                                    for i_C2630 in range(len(dgs_render__omniview['sna_omniviewobjectsformerge'])):
                                        bpy.data.objects[dgs_render__omniview['sna_omniviewobjectsformerge'][i_C2630]].select_set(state=True, view_layer=bpy.context.view_layer, )
                                        bpy.context.view_layer.objects.active = bpy.data.objects[dgs_render__omniview['sna_omniviewobjectsformerge'][i_C2630]]
                                    bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
                                    bpy.ops.object.join('INVOKE_DEFAULT', )
                                    bpy.data.objects.remove(object=dgs_render__omniview['sna_omniviewbase'], do_unlink=True, do_id_user=True, do_ui_user=True, )
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
                                    geonodemodreturn_0_9d9cf = sna_add_geo_nodes__append_group_2D522_9D9CF(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend'), 'KIRI_3DGS_Sorter_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Sorter_GN')
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
        box_E1BE2.label(text='This is a very performance intensive task', icon_value=133)
        box_E1BE2.label(text='         It is advised to use this on simple objects, not full scenes', icon_value=0)
        box_E1BE2.label(text='         Perform all edits and decimation first', icon_value=0)
        box_E1BE2.label(text='         Existing modifiers will be removed', icon_value=0)
        box_E1BE2.label(text='         Omniview objects will not HQ render well', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


def sna_point_cloud_export_function_interface_0D64D(layout_function, ):
    box_70806 = layout_function.box()
    box_70806.alert = True
    box_70806.enabled = True
    box_70806.active = True
    box_70806.use_property_split = False
    box_70806.use_property_decorate = False
    box_70806.alignment = 'Expand'.upper()
    box_70806.scale_x = 1.0
    box_70806.scale_y = 1.0
    if not True: box_70806.operator_context = "EXEC_DEFAULT"
    box_70806.label(text="If you have 'applied' scale or rotation values", icon_value=133)
    box_70806.label(text="         using Blender's native Apply Rotation/", icon_value=0)
    box_70806.label(text='         Scale, 3DGS attributes will be corrupted', icon_value=0)
    box_696CD = layout_function.box()
    box_696CD.alert = False
    box_696CD.enabled = 'OBJECT'==bpy.context.mode
    box_696CD.active = True
    box_696CD.use_property_split = False
    box_696CD.use_property_decorate = False
    box_696CD.alignment = 'Expand'.upper()
    box_696CD.scale_x = 1.0
    box_696CD.scale_y = 1.0
    if not True: box_696CD.operator_context = "EXEC_DEFAULT"
    box_696CD.prop(bpy.context.scene, 'sna_kiri3dgs_export__reset_origin', text='Reset Origin', icon_value=0, emboss=True)
    op = box_696CD.operator('sna.export_points_for_3dgs_63cd8', text='Export Points For 3DGS', icon_value=634, emboss=True, depress=False)


class SNA_OT_Import_Ply_As_Points_E9E21(bpy.types.Operator):
    bl_idname = "sna.import_ply_as_points_e9e21"
    bl_label = "Import PLY As Points"
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
        box_AFD26 = layout.box()
        box_AFD26.alert = True
        box_AFD26.enabled = True
        box_AFD26.active = True
        box_AFD26.use_property_split = False
        box_AFD26.use_property_decorate = False
        box_AFD26.alignment = 'Expand'.upper()
        box_AFD26.scale_x = 1.0
        box_AFD26.scale_y = 1.0
        if not True: box_AFD26.operator_context = "EXEC_DEFAULT"
        box_AFD26.label(text='Do not apply rotation or scale transforms', icon_value=133)
        box_AFD26.label(text="         using Blender's native Appy Scale / Rotation", icon_value=0)
        box_AFD26.label(text='         if you want to apply transforms, use the', icon_value=0)
        box_AFD26.label(text='         Apply 3DGS Transforms and Colour function', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


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
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend') + r'\NodeTree', filename='KIRI_3DGS_Point_Edit_GN', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
            appended_B2734 = None if not new_data else new_data[0]
        if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.materials)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
            appended_459F4 = None if not new_data else new_data[0]
        geonodemodreturn_0_f22b7 = sna_add_geo_nodes__append_group_2D522_F22B7(os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V3.blend'), 'KIRI_3DGS_Point_Edit_GN', bpy.context.view_layer.objects.active, 'KIRI_3DGS_Point_Edit_GN')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_6'] = bpy.data.materials['KIRI_3DGS_Render_Material']
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_point_cloud_import_function_interface_8E4CD(layout_function, ):
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
    op = box_70822.operator('sna.import_ply_as_points_e9e21', text='Import PLY As Points', icon_value=string_to_icon('IMPORT'), emboss=True, depress=False)
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
                        box_F9AE6 = box_70822.box()
                        box_F9AE6.alert = False
                        box_F9AE6.enabled = True
                        box_F9AE6.active = True
                        box_F9AE6.use_property_split = False
                        box_F9AE6.use_property_decorate = False
                        box_F9AE6.alignment = 'Expand'.upper()
                        box_F9AE6.scale_x = 1.0
                        box_F9AE6.scale_y = 1.0
                        if not True: box_F9AE6.operator_context = "EXEC_DEFAULT"
                        row_11D44 = box_F9AE6.row(heading='', align=False)
                        row_11D44.alert = False
                        row_11D44.enabled = True
                        row_11D44.active = True
                        row_11D44.use_property_split = False
                        row_11D44.use_property_decorate = False
                        row_11D44.scale_x = 1.0
                        row_11D44.scale_y = 1.0
                        row_11D44.alignment = 'Expand'.upper()
                        row_11D44.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                        row_11D44.label(text='Point Edit Modifier Is Missing', icon_value=0)
                        op = row_11D44.operator('sna.append_point_edit_modifier_a0188', text='', icon_value=45, emboss=True, depress=False)


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
                if bpy.context.scene.sna_kiri3dgs_export__reset_origin:
                    bpy.context.view_layer.objects.active.location = (0.0, 0.0, 0.0)
                APPLY_SCALE = True
                APPLY_ROTATION = True
                TRANSFORM_ORDER = 'ROTATION_FIRST'
                import numpy as np
                from mathutils import Quaternion, Matrix, Euler
                #------ INPUT VARIABLES (modify these) ------#
                # The attributes to update
                SCALE_ATTRIBUTES = ["scale_0", "scale_1", "scale_2"]
                ROTATION_ATTRIBUTES = ["rot_0", "rot_1", "rot_2", "rot_3"]
                # Whether to apply transformations after updating attributes
                #APPLY_SCALE = True
                #APPLY_ROTATION = True
                # The order of operations: either "SCALE_FIRST" or "ROTATION_FIRST"
                # 3DGS typically uses SCALE_FIRST (scale, then rotate)
                #TRANSFORM_ORDER = "SCALE_FIRST"
                # Whether to print debug information
                VERBOSE = True
                # Whether to normalize quaternions after transformation (PostShot does this)
                NORMALIZE_QUATERNIONS = True
                #------------------------------------------#

                def quaternion_multiply(q1, q2):
                    """
                    Multiply two quaternions (compose rotations)
                    q1 and q2 are in form [w, x, y, z]
                    """
                    w1, x1, y1, z1 = q1
                    w2, x2, y2, z2 = q2
                    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
                    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
                    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
                    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
                    return [w, x, y, z]

                def normalize_quaternion(q):
                    """
                    Normalize a quaternion to unit length
                    q is in form [w, x, y, z]
                    """
                    magnitude = math.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)
                    if magnitude > 0.00001:  # Avoid division by near-zero
                        return [q[0]/magnitude, q[1]/magnitude, q[2]/magnitude, q[3]/magnitude]
                    else:
                        return [1.0, 0.0, 0.0, 0.0]  # Default to identity quaternion

                def update_scale_attributes(obj, scale_attributes, log_scale_factors, verbose=False):
                    """
                    Update the scale attributes with logarithmic scale factors
                    """
                    success = True
                    for attr_idx, attr_name in enumerate(scale_attributes):
                        if attr_name not in obj.data.attributes:
                            print(f"Attribute '{attr_name}' not found on object.")
                            success = False
                            continue
                        attr = obj.data.attributes[attr_name]
                        if verbose:
                            print(f"\nUpdating attribute: {attr_name}")
                            print(f"Data type: {attr.data_type}")
                            print(f"Domain: {attr.domain}")
                            print(f"Length: {len(attr.data)}")
                        # Determine which scale factor to use based on attribute name
                        if attr_name == "scale_0":
                            log_scale = log_scale_factors[0]
                        elif attr_name == "scale_1":
                            log_scale = log_scale_factors[1]
                        elif attr_name == "scale_2":
                            log_scale = log_scale_factors[2]
                        else:
                            # For custom-named attributes, use the index in the scale_attributes list
                            log_scale = log_scale_factors[min(attr_idx, 2)]
                        if verbose:
                            print(f"Using log scale factor: {log_scale}")
                        # Update the attribute values
                        if attr.data_type == 'FLOAT':
                            # Sample a few values before and after for verification
                            sample_size = min(5, len(attr.data))
                            before_values = []
                            for i in range(sample_size):
                                before_values.append(attr.data[i].value)
                            # Update all values
                            for i in range(len(attr.data)):
                                # In 3DGS, adding the log of the scale factor to the log-space scale value
                                attr.data[i].value += log_scale
                            # Print sample values after update
                            if verbose:
                                print("Sample values before and after update:")
                                for i in range(sample_size):
                                    print(f"  [{i}]: {before_values[i]} -> {attr.data[i].value}")
                        else:
                            print(f"Attribute '{attr_name}' is not of type FLOAT (found {attr.data_type}). Skipping.")
                            success = False
                    return success

                def update_rotation_attributes(obj, rotation_attributes, blender_quat, verbose=False, normalize=True):
                    """
                    Update the rotation attributes with the object's rotation quaternion
                    """
                    # First, gather all data to avoid processing incomplete sets
                    attribute_data = {}
                    valid_attributes = True
                    for attr_name in rotation_attributes:
                        if attr_name not in obj.data.attributes:
                            print(f"Attribute '{attr_name}' not found on object.")
                            valid_attributes = False
                            break
                        attr = obj.data.attributes[attr_name]
                        if attr.data_type != 'FLOAT':
                            print(f"Attribute '{attr_name}' is not of type FLOAT (found {attr.data_type}). Skipping.")
                            valid_attributes = False
                            break
                        # Store the attribute for processing
                        attribute_data[attr_name] = attr
                    if not valid_attributes:
                        print("Unable to process rotation due to missing or invalid attributes.")
                        return False
                    # Sample a few values before the update for verification
                    sample_size = min(5, len(attribute_data[rotation_attributes[0]].data))
                    before_values = {attr_name: [] for attr_name in rotation_attributes}
                    for attr_name in rotation_attributes:
                        for i in range(sample_size):
                            before_values[attr_name].append(attribute_data[attr_name].data[i].value)
                    # Process all points
                    num_points = len(attribute_data[rotation_attributes[0]].data)
                    print(f"Processing {num_points} points...")
                    for i in range(num_points):
                        # Get current quaternion values [w, x, y, z]
                        point_quat = [
                            attribute_data[rotation_attributes[0]].data[i].value,  # w
                            attribute_data[rotation_attributes[1]].data[i].value,  # x
                            attribute_data[rotation_attributes[2]].data[i].value,  # y
                            attribute_data[rotation_attributes[3]].data[i].value   # z
                        ]
                        # Apply rotation by multiplying quaternions
                        # The order matters: PostShot appears to use the object_rotation * point_quat
                        # format (rotating the local frame)
                        new_quat = quaternion_multiply(blender_quat, point_quat)
                        # Normalize the quaternion if requested (PostShot does this)
                        if normalize:
                            new_quat = normalize_quaternion(new_quat)
                        # Enforce positive w component to match PostShot's convention
                        # Since q and -q represent the same rotation, we can flip all signs if w is negative
                        if new_quat[0] < 0:
                            new_quat = [-q for q in new_quat]
                        # Update attribute values
                        attribute_data[rotation_attributes[0]].data[i].value = new_quat[0]  # w
                        attribute_data[rotation_attributes[1]].data[i].value = new_quat[1]  # x
                        attribute_data[rotation_attributes[2]].data[i].value = new_quat[2]  # y
                        attribute_data[rotation_attributes[3]].data[i].value = new_quat[3]  # z
                    # Print sample values after update for verification
                    if verbose:
                        print("\nSample values before and after update:")
                        for i in range(sample_size):
                            print(f"Point [{i}]:")
                            for j, attr_name in enumerate(rotation_attributes):
                                print(f"  {attr_name}: {before_values[attr_name][i]} -> {attribute_data[attr_name].data[i].value}")
                    return True

                def apply_transformations(obj, apply_rotation=False, apply_scale=False):
                    """
                    Apply the transformations to the object
                    """
                    if not (apply_rotation or apply_scale):
                        return
                    # Store current context
                    original_mode = obj.mode
                    # Switch to object mode if needed
                    if original_mode != 'OBJECT':
                        bpy.ops.object.mode_set(mode='OBJECT')
                    # Apply transformations
                    bpy.ops.object.transform_apply(
                        location=False, 
                        rotation=apply_rotation, 
                        scale=apply_scale
                    )
                    # Restore original mode
                    if original_mode != 'OBJECT':
                        bpy.ops.object.mode_set(mode=original_mode)
                    transformations = []
                    if apply_rotation:
                        transformations.append("rotation")
                    if apply_scale:
                        transformations.append("scale")
                    print(f"Object {', '.join(transformations)} applied.")
                # MAIN SCRIPT EXECUTION
                # Get the active object
                obj = bpy.context.active_object
                if not obj:
                    print("No active object found.")
                else:
                    print(f"Processing 3DGS transformations for object: {obj.name}")
                    # Get current object rotation (ensuring quaternion is updated)
                    original_rotation_mode = obj.rotation_mode
                    # If not already in quaternion mode, ensure the quaternion gets updated
                    if original_rotation_mode != 'QUATERNION':
                        # Switch to quaternion mode to ensure quaternion is updated
                        obj.rotation_mode = 'QUATERNION'
                        # Switch back to original mode
                        obj.rotation_mode = original_rotation_mode
                    # Get the quaternion values
                    obj_rotation_quat = obj.rotation_quaternion.copy()
                    # Convert to w, x, y, z format (from Blender's x, y, z, w)
                    blender_quat = [obj_rotation_quat.w, obj_rotation_quat.x, 
                                  obj_rotation_quat.y, obj_rotation_quat.z]
                    if VERBOSE:
                        print(f"Current object rotation quaternion [w,x,y,z]: {blender_quat}")
                    # Get current object scale
                    scale_x, scale_y, scale_z = obj.scale
                    if VERBOSE:
                        print(f"Current object scale: X={scale_x}, Y={scale_y}, Z={scale_z}")
                    # Calculate the logarithm of scale factors
                    log_scale_x = math.log(scale_x) if scale_x > 0 else 0
                    log_scale_y = math.log(scale_y) if scale_y > 0 else 0
                    log_scale_z = math.log(scale_z) if scale_z > 0 else 0
                    log_scale_factors = [log_scale_x, log_scale_y, log_scale_z]
                    if VERBOSE:
                        print(f"Log scale factors: X={log_scale_x}, Y={log_scale_y}, Z={log_scale_z}")
                    # Check if the object has attribute data
                    if not hasattr(obj.data, "attributes"):
                        print("Object does not have attribute data.")
                    else:
                        # Perform transformations in the specified order
                        if TRANSFORM_ORDER == "SCALE_FIRST":
                            # First update scale attributes
                            scale_success = update_scale_attributes(obj, SCALE_ATTRIBUTES, log_scale_factors, VERBOSE)
                            print("Scale attributes update", "succeeded" if scale_success else "failed")
                            # Then update rotation attributes
                            rotation_success = update_rotation_attributes(obj, ROTATION_ATTRIBUTES, blender_quat, VERBOSE, NORMALIZE_QUATERNIONS)
                            print("Rotation attributes update", "succeeded" if rotation_success else "failed")
                        else:  # ROTATION_FIRST
                            # First update rotation attributes
                            rotation_success = update_rotation_attributes(obj, ROTATION_ATTRIBUTES, blender_quat, VERBOSE, NORMALIZE_QUATERNIONS)
                            print("Rotation attributes update", "succeeded" if rotation_success else "failed")
                            # Then update scale attributes
                            scale_success = update_scale_attributes(obj, SCALE_ATTRIBUTES, log_scale_factors, VERBOSE)
                            print("Scale attributes update", "succeeded" if scale_success else "failed")
                        # Apply transformations to reset object transforms
                        apply_transformations(obj, APPLY_ROTATION, APPLY_SCALE)
                        print("\nTransformation operations completed.")

                def delayed_1B018():
                    bpy.ops.wm.ply_export('INVOKE_DEFAULT', apply_modifiers=True, export_selected_objects=True, export_attributes=True)
                bpy.app.timers.register(delayed_1B018, first_interval=0.10000000149011612)
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


def sna_point_cloud_modifier_function_interface_F1E94(layout_function, ):
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
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Point_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
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
        box_C2D6E.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_F84FA, text=('Auto Crop BG Sphere' if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_2'] else 'Enable Auto Crop BG Sphere'), icon_value=0, emboss=True, toggle=True)
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
        box_3294E.separator(factor=1.0)
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
        box_BFED0.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_D8FF2, text=('Crop Box' if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_20'] else 'Enable Crop Box'), icon_value=0, emboss=True, toggle=True)
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
        box_3294E.separator(factor=1.0)
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
        box_FEB97.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_FB39D, text=('Remove Isolated Points' if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_9'] else 'Enable Remove Isolated Points'), icon_value=0, emboss=True, toggle=True)
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
        box_3294E.separator(factor=1.0)
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
        box_713CF.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_23921, text=('Colour Edit' if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_13'] else 'Enable Colour Edit'), icon_value=0, emboss=True, toggle=True)
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
        box_3294E.separator(factor=1.0)
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
        box_9FF22.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_CFACB, text=('Decimate' if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN']['Socket_24'] else 'Enable Decimate'), icon_value=0, emboss=True, toggle=True)
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
    else:
        box_832BC = layout_function.box()
        box_832BC.alert = False
        box_832BC.enabled = 'OBJECT'==bpy.context.mode
        box_832BC.active = True
        box_832BC.use_property_split = False
        box_832BC.use_property_decorate = False
        box_832BC.alignment = 'Expand'.upper()
        box_832BC.scale_x = 1.0
        box_832BC.scale_y = 1.0
        if not True: box_832BC.operator_context = "EXEC_DEFAULT"
        row_78EBE = box_832BC.row(heading='', align=False)
        row_78EBE.alert = False
        row_78EBE.enabled = True
        row_78EBE.active = True
        row_78EBE.use_property_split = False
        row_78EBE.use_property_decorate = False
        row_78EBE.scale_x = 1.0
        row_78EBE.scale_y = 1.0
        row_78EBE.alignment = 'Expand'.upper()
        row_78EBE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_78EBE.label(text='Point Edit Modifier Is Missing', icon_value=0)
        op = row_78EBE.operator('sna.append_point_edit_modifier_a0188', text='', icon_value=45, emboss=True, depress=False)


def sna_point_cloud_active_object_function_interface_31AB0(layout_function, ):
    col_5A956 = layout_function.column(heading='', align=False)
    col_5A956.alert = False
    col_5A956.enabled = True
    col_5A956.active = True
    col_5A956.use_property_split = False
    col_5A956.use_property_decorate = False
    col_5A956.scale_x = 1.0
    col_5A956.scale_y = 1.0
    col_5A956.alignment = 'Expand'.upper()
    col_5A956.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_6A0F6 = col_5A956.column(heading='', align=False)
    col_6A0F6.alert = False
    col_6A0F6.enabled = True
    col_6A0F6.active = True
    col_6A0F6.use_property_split = False
    col_6A0F6.use_property_decorate = False
    col_6A0F6.scale_x = 1.0
    col_6A0F6.scale_y = 1.0
    col_6A0F6.alignment = 'Expand'.upper()
    col_6A0F6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_6A0F6.label(text='Active Point Cloud:', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
    box_BF097 = col_6A0F6.box()
    box_BF097.alert = False
    box_BF097.enabled = True
    box_BF097.active = True
    box_BF097.use_property_split = False
    box_BF097.use_property_decorate = False
    box_BF097.alignment = 'Expand'.upper()
    box_BF097.scale_x = 1.0
    box_BF097.scale_y = 1.0
    if not True: box_BF097.operator_context = "EXEC_DEFAULT"
    box_BF097.label(text=bpy.context.view_layer.objects.active.name, icon_value=0)
    box_F8921 = col_5A956.box()
    box_F8921.alert = False
    box_F8921.enabled = True
    box_F8921.active = True
    box_F8921.use_property_split = False
    box_F8921.use_property_decorate = False
    box_F8921.alignment = 'Expand'.upper()
    box_F8921.scale_x = 1.0
    box_F8921.scale_y = 1.0
    if not True: box_F8921.operator_context = "EXEC_DEFAULT"
    attr_C7885 = '["' + str('Socket_19' + '"]') 
    box_F8921.prop(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Point_Edit_GN'], attr_C7885, text='Point Scale', icon_value=0, emboss=True)
    if 'OBJECT'==bpy.context.mode:
        box_81CE8 = col_5A956.box()
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
        op = row_69E53.operator('sna.remove_point_edit_modifier_47851', text='', icon_value=string_to_icon('TRASH'), emboss=True, depress=False)
        op = row_69E53.operator('sna.refresh_point_edit_modifier_ec829', text='Refresh', icon_value=string_to_icon('FILE_REFRESH'), emboss=True, depress=False)
        op = row_69E53.operator('sna.apply_point_edit_modifier_d6b08', text='Apply', icon_value=string_to_icon('CHECKMARK'), emboss=True, depress=False)


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
                box_78D4A.label(text='Standard gives most accurate scan colours', icon_value=string_to_icon('INFO'))
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
            box_B7424 = col_32C11.box()
            box_B7424.alert = True
            box_B7424.enabled = True
            box_B7424.active = True
            box_B7424.use_property_split = False
            box_B7424.use_property_decorate = False
            box_B7424.alignment = 'Expand'.upper()
            box_B7424.scale_x = 1.0
            box_B7424.scale_y = 1.0
            if not True: box_B7424.operator_context = "EXEC_DEFAULT"
            box_B7424.label(text='HQ mode should be used for final renders', icon_value=string_to_icon('INFO'))
            box_B7424.label(text='         to avoid flickering artifacts', icon_value=0)
            box_B7424.label(text='         Samples can often be reduced to 1 in HQ Mode', icon_value=0)
            box_B7424.label(text="         if 'Shadeless' materials are used", icon_value=0)
            box_B7424.prop(bpy.context.scene.eevee, 'taa_render_samples', text='Render Samples', icon_value=0, emboss=True)
            box_AA140 = col_32C11.box()
            box_AA140.alert = False
            box_AA140.enabled = True
            box_AA140.active = True
            box_AA140.use_property_split = False
            box_AA140.use_property_decorate = False
            box_AA140.alignment = 'Expand'.upper()
            box_AA140.scale_x = 1.0
            box_AA140.scale_y = 1.0
            if not True: box_AA140.operator_context = "EXEC_DEFAULT"
            box_AA140.prop(bpy.context.scene.render.image_settings, 'file_format', text='Format', icon_value=0, emboss=True)
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
                op = box_41BC0.operator('sna.dgs_render_offline_aea04', text='Render Image', icon_value=string_to_icon('IMAGE_DATA'), emboss=True, depress=False)
                op.sna_render_animation = False
                op = box_41BC0.operator('sna.dgs_render_offline_aea04', text='Render Animation', icon_value=string_to_icon('FILE_MOVIE'), emboss=True, depress=False)
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
                bpy.data.objects[i_2F11D].update_tag(refresh={'OBJECT'}, )
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
        box_C3AA8.label(text="All available objects will be set to use 'Active Camera'", icon_value=133)
        box_C3AA8.label(text='        To cancel rendering - force close Blender', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


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
    row_98360 = box_3A687.row(heading='', align=False)
    row_98360.alert = False
    row_98360.enabled = True
    row_98360.active = True
    row_98360.use_property_split = False
    row_98360.use_property_decorate = False
    row_98360.scale_x = 1.0
    row_98360.scale_y = 1.0
    row_98360.alignment = 'Expand'.upper()
    row_98360.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_98360.label(text='Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
    op = row_98360.operator('sna.dgs_render_refresh_scene_eded7', text='', icon_value=647, emboss=True, depress=False)
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
        op = box_BB246.operator('sna.dgs__start_camera_update_001bd', text='Start Camera Updates', icon_value=string_to_icon('OUTLINER_OB_CAMERA'), emboss=True, depress=False)
    op = box_BB246.operator('sna.dgs__update_camera_single_time_03530', text='Update All To View', icon_value=string_to_icon('HIDE_OFF'), emboss=True, depress=False)


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
        bpy.data.objects[updated_objects[i_13DD6]].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()


@persistent
def load_pre_handler_F6F13(dummy):
    bpy.context.scene['gaussian_splat_updates_active'] = False
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


class SNA_OT_Dgs_Render_Refresh_Scene_Eded7(bpy.types.Operator):
    bl_idname = "sna.dgs_render_refresh_scene_eded7"
    bl_label = "3DGS Render- Refresh Scene"
    bl_description = "Updates all scene properties, and object properties for objects with the 3DGS_Render modifier. Useful for moving objects between files."
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
        bpy.context.scene['gaussian_splat_updates_active'] = False
        for i_13D2E in range(len(bpy.data.objects)):
            if (property_exists("bpy.data.objects[i_13D2E].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.data.objects[i_13D2E].modifiers):
                bpy.data.objects[bpy.data.objects[i_13D2E].name]['update_rot_to_cam'] = False
                bpy.data.objects[i_13D2E].sna_kiri3dgs_active_object_update_mode = 'Disable Camera Updates'
                bpy.data.objects[i_13D2E].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_DGS_RENDER__ABOUT__LINKS_PANEL_BA803(bpy.types.Panel):
    bl_label = '3DGS Render - About / Links Panel'
    bl_idname = 'SNA_PT_DGS_RENDER__ABOUT__LINKS_PANEL_BA803'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 3
    bl_options = {'HIDE_HEADER'}
    bl_parent_id = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_77E7E'
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
        op = layout.operator('sna.launch_blender_market__3dgs_77f72', text='See All Addons On Blender Market', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.launch_kiri_site__3dgs_d26bf', text='Learn More About KIRI Engine', icon_value=0, emboss=True, depress=False)


class SNA_PT_DGS_RENDER__DOCUMENTATION_PANEL_88B3E(bpy.types.Panel):
    bl_label = '3DGS Render - Documentation Panel'
    bl_idname = 'SNA_PT_DGS_RENDER__DOCUMENTATION_PANEL_88B3E'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 2
    bl_options = {'HIDE_HEADER'}
    bl_parent_id = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_77E7E'
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
        op = box_BDECD.operator('sna.open_blender_3dgs_render_documentation_1eac5', text='Documentation', icon_value=0, emboss=True, depress=False)
        op = box_BDECD.operator('sna.open_blender_3dgs_render_tutorial_video_a4fe6', text='Tutorial Video', icon_value=0, emboss=True, depress=False)


class SNA_PT_DGS_RENDER__MAIN_FUNCTION_PANEL_9D9BF(bpy.types.Panel):
    bl_label = '3DGS Render - Main Function Panel'
    bl_idname = 'SNA_PT_DGS_RENDER__MAIN_FUNCTION_PANEL_9D9BF'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 1
    bl_options = {'HIDE_HEADER'}
    bl_parent_id = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_77E7E'
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
            pass
        else:
            box_48E23 = box_BDC6F.box()
            box_48E23.alert = True
            box_48E23.enabled = True
            box_48E23.active = True
            box_48E23.use_property_split = False
            box_48E23.use_property_decorate = False
            box_48E23.alignment = 'Expand'.upper()
            box_48E23.scale_x = 1.0
            box_48E23.scale_y = 1.0
            if not True: box_48E23.operator_context = "EXEC_DEFAULT"
            col_3F32E = box_48E23.column(heading='', align=False)
            col_3F32E.alert = False
            col_3F32E.enabled = True
            col_3F32E.active = True
            col_3F32E.use_property_split = False
            col_3F32E.use_property_decorate = False
            col_3F32E.scale_x = 1.0
            col_3F32E.scale_y = 1.0
            col_3F32E.alignment = 'Expand'.upper()
            col_3F32E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_3F32E.label(text='Eevee is recommended.', icon_value=string_to_icon('INFO'))
            col_3F32E.label(text='        When using Cycles,', icon_value=0)
            col_3F32E.label(text='        Use high transparent bounces.', icon_value=0)
            col_3F32E.separator(factor=1.0)
            if (bpy.context.scene.render.engine == 'CYCLES'):
                col_3F32E.prop(bpy.context.scene.cycles, 'transparent_max_bounces', text='Transparent Bounces', icon_value=0, emboss=True)
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
        if (bpy.context.view_layer.objects.active == None):
            pass
        else:
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
            sna_dgs__active_3dgs_object_interface_func_9588F(layout_function, )
            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Point_Edit_GN' in bpy.context.view_layer.objects.active.modifiers):
                box_D79CA = col_0E928.box()
                box_D79CA.alert = False
                box_D79CA.enabled = True
                box_D79CA.active = True
                box_D79CA.use_property_split = False
                box_D79CA.use_property_decorate = False
                box_D79CA.alignment = 'Expand'.upper()
                box_D79CA.scale_x = 1.0
                box_D79CA.scale_y = 1.0
                if not True: box_D79CA.operator_context = "EXEC_DEFAULT"
                layout_function = box_D79CA
                sna_point_cloud_active_object_function_interface_31AB0(layout_function, )
        col_23FAF.separator(factor=1.0)
        box_DCCA2 = col_23FAF.box()
        box_DCCA2.alert = False
        box_DCCA2.enabled = True
        box_DCCA2.active = True
        box_DCCA2.use_property_split = False
        box_DCCA2.use_property_decorate = False
        box_DCCA2.alignment = 'Expand'.upper()
        box_DCCA2.scale_x = 1.0
        box_DCCA2.scale_y = 1.0
        if not True: box_DCCA2.operator_context = "EXEC_DEFAULT"
        box_DCCA2.label(text='Active Menu', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'bullet-point-4084289 - light blue.png')))
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
        row_A59C6.prop(bpy.context.scene, 'sna_kiri3dgs_active_mode', text=bpy.context.scene.sna_kiri3dgs_active_mode, icon_value=0, emboss=True, expand=True)
        col_79CB4 = box_DCCA2.column(heading='', align=False)
        col_79CB4.alert = False
        col_79CB4.enabled = True
        col_79CB4.active = True
        col_79CB4.use_property_split = False
        col_79CB4.use_property_decorate = False
        col_79CB4.scale_x = 1.0
        col_79CB4.scale_y = 1.0
        col_79CB4.alignment = 'Expand'.upper()
        col_79CB4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (bpy.context.scene.sna_kiri3dgs_active_mode == '3DGS'):
            box_48E40 = col_79CB4.box()
            box_48E40.alert = False
            box_48E40.enabled = True
            box_48E40.active = True
            box_48E40.use_property_split = False
            box_48E40.use_property_decorate = False
            box_48E40.alignment = 'Expand'.upper()
            box_48E40.scale_x = 1.0
            box_48E40.scale_y = 1.0
            if not True: box_48E40.operator_context = "EXEC_DEFAULT"
            grid_DD1AC = box_48E40.grid_flow(columns=2, row_major=False, even_columns=False, even_rows=False, align=False)
            grid_DD1AC.enabled = True
            grid_DD1AC.active = True
            grid_DD1AC.use_property_split = False
            grid_DD1AC.use_property_decorate = False
            grid_DD1AC.alignment = 'Expand'.upper()
            grid_DD1AC.scale_x = 1.0
            grid_DD1AC.scale_y = 1.0
            if not True: grid_DD1AC.operator_context = "EXEC_DEFAULT"
            col_A283E = grid_DD1AC.column(heading='', align=True)
            col_A283E.alert = False
            col_A283E.enabled = True
            col_A283E.active = True
            col_A283E.use_property_split = False
            col_A283E.use_property_decorate = False
            col_A283E.scale_x = 1.0
            col_A283E.scale_y = 1.0
            col_A283E.alignment = 'Expand'.upper()
            col_A283E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_A283E.operator('sna.set_menu_active_mode_6dc45', text='Import', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Import') else 'RADIOBUT_OFF')), emboss=True, depress=False)
            op.sna_active_mode_set = 'Import'
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
                    col_897C3 = grid_DD1AC.column(heading='', align=True)
                    col_897C3.alert = False
                    col_897C3.enabled = (not bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked)
                    col_897C3.active = True
                    col_897C3.use_property_split = False
                    col_897C3.use_property_decorate = False
                    col_897C3.scale_x = 1.0
                    col_897C3.scale_y = 1.0
                    col_897C3.alignment = 'Expand'.upper()
                    col_897C3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_897C3.operator('sna.set_menu_active_mode_6dc45', text='Modifiers', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Modifiers') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'Modifiers'
                else:
                    col_892D7 = grid_DD1AC.column(heading='', align=True)
                    col_892D7.alert = False
                    col_892D7.enabled = True
                    col_892D7.active = True
                    col_892D7.use_property_split = False
                    col_892D7.use_property_decorate = False
                    col_892D7.scale_x = 1.0
                    col_892D7.scale_y = 1.0
                    col_892D7.alignment = 'Expand'.upper()
                    col_892D7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_892D7.operator('sna.set_menu_active_mode_6dc45', text='Modifiers', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Modifiers') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'Modifiers'
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
                    col_F45A6 = grid_DD1AC.column(heading='', align=True)
                    col_F45A6.alert = False
                    col_F45A6.enabled = (not bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked)
                    col_F45A6.active = True
                    col_F45A6.use_property_split = False
                    col_F45A6.use_property_decorate = False
                    col_F45A6.scale_x = 1.0
                    col_F45A6.scale_y = 1.0
                    col_F45A6.alignment = 'Expand'.upper()
                    col_F45A6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_F45A6.operator('sna.set_menu_active_mode_6dc45', text='Colour', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Colour') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'Colour'
                else:
                    col_1B189 = grid_DD1AC.column(heading='', align=True)
                    col_1B189.alert = False
                    col_1B189.enabled = True
                    col_1B189.active = True
                    col_1B189.use_property_split = False
                    col_1B189.use_property_decorate = False
                    col_1B189.scale_x = 1.0
                    col_1B189.scale_y = 1.0
                    col_1B189.alignment = 'Expand'.upper()
                    col_1B189.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_1B189.operator('sna.set_menu_active_mode_6dc45', text='Colour', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Colour') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'Colour'
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
                    col_6A6A6 = grid_DD1AC.column(heading='', align=True)
                    col_6A6A6.alert = False
                    col_6A6A6.enabled = (not bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked)
                    col_6A6A6.active = True
                    col_6A6A6.use_property_split = False
                    col_6A6A6.use_property_decorate = False
                    col_6A6A6.scale_x = 1.0
                    col_6A6A6.scale_y = 1.0
                    col_6A6A6.alignment = 'Expand'.upper()
                    col_6A6A6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_6A6A6.operator('sna.set_menu_active_mode_6dc45', text='Animate', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Animate') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'Animate'
                else:
                    col_885AA = grid_DD1AC.column(heading='', align=True)
                    col_885AA.alert = False
                    col_885AA.enabled = bpy.context.view_layer.objects.active.sna_kiri3dgs_modifier_enable_animate
                    col_885AA.active = True
                    col_885AA.use_property_split = False
                    col_885AA.use_property_decorate = False
                    col_885AA.scale_x = 1.0
                    col_885AA.scale_y = 1.0
                    col_885AA.alignment = 'Expand'.upper()
                    col_885AA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_885AA.operator('sna.set_menu_active_mode_6dc45', text='Animate', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Animate') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'Animate'
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
                    col_D1692 = grid_DD1AC.column(heading='', align=True)
                    col_D1692.alert = False
                    col_D1692.enabled = (not bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked)
                    col_D1692.active = True
                    col_D1692.use_property_split = False
                    col_D1692.use_property_decorate = False
                    col_D1692.scale_x = 1.0
                    col_D1692.scale_y = 1.0
                    col_D1692.alignment = 'Expand'.upper()
                    col_D1692.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_D1692.operator('sna.set_menu_active_mode_6dc45', text='HQ / LQ', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'HQ / LQ') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'HQ / LQ'
                else:
                    col_FF836 = grid_DD1AC.column(heading='', align=True)
                    col_FF836.alert = False
                    col_FF836.enabled = True
                    col_FF836.active = True
                    col_FF836.use_property_split = False
                    col_FF836.use_property_decorate = False
                    col_FF836.scale_x = 1.0
                    col_FF836.scale_y = 1.0
                    col_FF836.alignment = 'Expand'.upper()
                    col_FF836.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_FF836.operator('sna.set_menu_active_mode_6dc45', text='HQ / LQ', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'HQ / LQ') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'HQ / LQ'
            col_78711 = grid_DD1AC.column(heading='', align=True)
            col_78711.alert = False
            col_78711.enabled = True
            col_78711.active = True
            col_78711.use_property_split = False
            col_78711.use_property_decorate = False
            col_78711.scale_x = 1.0
            col_78711.scale_y = 1.0
            col_78711.alignment = 'Expand'.upper()
            col_78711.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_78711.operator('sna.set_menu_active_mode_6dc45', text='Render', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Render') else 'RADIOBUT_OFF')), emboss=True, depress=False)
            op.sna_active_mode_set = 'Render'
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                if property_exists("bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked", globals(), locals()):
                    col_ED3B5 = grid_DD1AC.column(heading='', align=True)
                    col_ED3B5.alert = False
                    col_ED3B5.enabled = (not bpy.context.view_layer.objects.active.sna_kiri3dgs_active_object_3dgs_baked)
                    col_ED3B5.active = True
                    col_ED3B5.use_property_split = False
                    col_ED3B5.use_property_decorate = False
                    col_ED3B5.scale_x = 1.0
                    col_ED3B5.scale_y = 1.0
                    col_ED3B5.alignment = 'Expand'.upper()
                    col_ED3B5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_ED3B5.operator('sna.set_menu_active_mode_6dc45', text='Omniview', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Omniview') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'Omniview'
                else:
                    col_191A9 = grid_DD1AC.column(heading='', align=True)
                    col_191A9.alert = False
                    col_191A9.enabled = True
                    col_191A9.active = True
                    col_191A9.use_property_split = False
                    col_191A9.use_property_decorate = False
                    col_191A9.scale_x = 1.0
                    col_191A9.scale_y = 1.0
                    col_191A9.alignment = 'Expand'.upper()
                    col_191A9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_191A9.operator('sna.set_menu_active_mode_6dc45', text='Omniview', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Omniview') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                    op.sna_active_mode_set = 'Omniview'
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                col_DCE6B = grid_DD1AC.column(heading='', align=True)
                col_DCE6B.alert = False
                col_DCE6B.enabled = True
                col_DCE6B.active = True
                col_DCE6B.use_property_split = False
                col_DCE6B.use_property_decorate = False
                col_DCE6B.scale_x = 1.0
                col_DCE6B.scale_y = 1.0
                col_DCE6B.alignment = 'Expand'.upper()
                col_DCE6B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = col_DCE6B.operator('sna.set_menu_active_mode_6dc45', text='Export', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Export') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                op.sna_active_mode_set = 'Export'
        if (bpy.context.scene.sna_kiri3dgs_active_mode == 'Point Cloud'):
            box_8B3FE = col_79CB4.box()
            box_8B3FE.alert = False
            box_8B3FE.enabled = True
            box_8B3FE.active = True
            box_8B3FE.use_property_split = False
            box_8B3FE.use_property_decorate = False
            box_8B3FE.alignment = 'Expand'.upper()
            box_8B3FE.scale_x = 1.0
            box_8B3FE.scale_y = 1.0
            if not True: box_8B3FE.operator_context = "EXEC_DEFAULT"
            grid_D1418 = box_8B3FE.grid_flow(columns=2, row_major=False, even_columns=False, even_rows=False, align=False)
            grid_D1418.enabled = True
            grid_D1418.active = True
            grid_D1418.use_property_split = False
            grid_D1418.use_property_decorate = False
            grid_D1418.alignment = 'Expand'.upper()
            grid_D1418.scale_x = 1.0
            grid_D1418.scale_y = 1.0
            if not True: grid_D1418.operator_context = "EXEC_DEFAULT"
            col_F5758 = grid_D1418.column(heading='', align=True)
            col_F5758.alert = False
            col_F5758.enabled = True
            col_F5758.active = True
            col_F5758.use_property_split = False
            col_F5758.use_property_decorate = False
            col_F5758.scale_x = 1.0
            col_F5758.scale_y = 1.0
            col_F5758.alignment = 'Expand'.upper()
            col_F5758.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_F5758.operator('sna.set_menu_active_mode_6dc45', text='Import', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Import') else 'RADIOBUT_OFF')), emboss=True, depress=False)
            op.sna_active_mode_set = 'Import'
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                col_0FC16 = grid_D1418.column(heading='', align=True)
                col_0FC16.alert = False
                col_0FC16.enabled = True
                col_0FC16.active = True
                col_0FC16.use_property_split = False
                col_0FC16.use_property_decorate = False
                col_0FC16.scale_x = 1.0
                col_0FC16.scale_y = 1.0
                col_0FC16.alignment = 'Expand'.upper()
                col_0FC16.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = col_0FC16.operator('sna.set_menu_active_mode_6dc45', text='Modifiers', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Modifiers') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                op.sna_active_mode_set = 'Modifiers'
            col_C5EB2 = grid_D1418.column(heading='', align=True)
            col_C5EB2.alert = False
            col_C5EB2.enabled = True
            col_C5EB2.active = True
            col_C5EB2.use_property_split = False
            col_C5EB2.use_property_decorate = False
            col_C5EB2.scale_x = 1.0
            col_C5EB2.scale_y = 1.0
            col_C5EB2.alignment = 'Expand'.upper()
            col_C5EB2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_C5EB2.operator('sna.set_menu_active_mode_6dc45', text='Render', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Render') else 'RADIOBUT_OFF')), emboss=True, depress=False)
            op.sna_active_mode_set = 'Render'
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                col_F07CF = grid_D1418.column(heading='', align=True)
                col_F07CF.alert = False
                col_F07CF.enabled = True
                col_F07CF.active = True
                col_F07CF.use_property_split = False
                col_F07CF.use_property_decorate = False
                col_F07CF.scale_x = 1.0
                col_F07CF.scale_y = 1.0
                col_F07CF.alignment = 'Expand'.upper()
                col_F07CF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = col_F07CF.operator('sna.set_menu_active_mode_6dc45', text='Export', icon_value=string_to_icon(('RADIOBUT_ON' if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Export') else 'RADIOBUT_OFF')), emboss=True, depress=False)
                op.sna_active_mode_set = 'Export'
        col_E242B = col_23FAF.column(heading='', align=False)
        col_E242B.alert = False
        col_E242B.enabled = True
        col_E242B.active = True
        col_E242B.use_property_split = False
        col_E242B.use_property_decorate = False
        col_E242B.scale_x = 1.0
        col_E242B.scale_y = 1.0
        col_E242B.alignment = 'Expand'.upper()
        col_E242B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (bpy.context.scene.sna_kiri3dgs_active_mode == '3DGS'):
            col_ABD31 = col_E242B.column(heading='', align=False)
            col_ABD31.alert = False
            col_ABD31.enabled = True
            col_ABD31.active = True
            col_ABD31.use_property_split = False
            col_ABD31.use_property_decorate = False
            col_ABD31.scale_x = 1.0
            col_ABD31.scale_y = 1.0
            col_ABD31.alignment = 'Expand'.upper()
            col_ABD31.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Import'):
                box_AF28C = col_ABD31.box()
                box_AF28C.alert = False
                box_AF28C.enabled = True
                box_AF28C.active = True
                box_AF28C.use_property_split = False
                box_AF28C.use_property_decorate = False
                box_AF28C.alignment = 'Expand'.upper()
                box_AF28C.scale_x = 1.0
                box_AF28C.scale_y = 1.0
                if not True: box_AF28C.operator_context = "EXEC_DEFAULT"
                layout_function = box_AF28C
                sna_import_ply_as_splats_function_interface_94FB1(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Modifiers'):
                if (bpy.context.view_layer.objects.active == None):
                    box_1A133 = col_ABD31.box()
                    box_1A133.alert = True
                    box_1A133.enabled = True
                    box_1A133.active = True
                    box_1A133.use_property_split = False
                    box_1A133.use_property_decorate = False
                    box_1A133.alignment = 'Expand'.upper()
                    box_1A133.scale_x = 1.0
                    box_1A133.scale_y = 1.0
                    if not True: box_1A133.operator_context = "EXEC_DEFAULT"
                    box_1A133.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                else:
                    box_01FD3 = col_ABD31.box()
                    box_01FD3.alert = False
                    box_01FD3.enabled = True
                    box_01FD3.active = True
                    box_01FD3.use_property_split = False
                    box_01FD3.use_property_decorate = False
                    box_01FD3.alignment = 'Expand'.upper()
                    box_01FD3.scale_x = 1.0
                    box_01FD3.scale_y = 1.0
                    if not True: box_01FD3.operator_context = "EXEC_DEFAULT"
                    layout_function = box_01FD3
                    sna_modify_edit_function_interface_AEA26(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Colour'):
                if (bpy.context.view_layer.objects.active == None):
                    box_9821A = col_ABD31.box()
                    box_9821A.alert = True
                    box_9821A.enabled = True
                    box_9821A.active = True
                    box_9821A.use_property_split = False
                    box_9821A.use_property_decorate = False
                    box_9821A.alignment = 'Expand'.upper()
                    box_9821A.scale_x = 1.0
                    box_9821A.scale_y = 1.0
                    if not True: box_9821A.operator_context = "EXEC_DEFAULT"
                    box_9821A.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                else:
                    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Colour_And_Material' in bpy.context.view_layer.objects.active.modifiers):
                        box_5ED5C = col_ABD31.box()
                        box_5ED5C.alert = False
                        box_5ED5C.enabled = True
                        box_5ED5C.active = True
                        box_5ED5C.use_property_split = False
                        box_5ED5C.use_property_decorate = False
                        box_5ED5C.alignment = 'Expand'.upper()
                        box_5ED5C.scale_x = 1.0
                        box_5ED5C.scale_y = 1.0
                        if not True: box_5ED5C.operator_context = "EXEC_DEFAULT"
                        layout_function = box_5ED5C
                        sna_colour_function_interface_3A6A5(layout_function, )
                    else:
                        box_0BF3B = col_ABD31.box()
                        box_0BF3B.alert = True
                        box_0BF3B.enabled = True
                        box_0BF3B.active = True
                        box_0BF3B.use_property_split = False
                        box_0BF3B.use_property_decorate = False
                        box_0BF3B.alignment = 'Expand'.upper()
                        box_0BF3B.scale_x = 1.0
                        box_0BF3B.scale_y = 1.0
                        if not True: box_0BF3B.operator_context = "EXEC_DEFAULT"
                        box_0BF3B.label(text="Active Object is missing 'Adjust_Colour_And_Material' modifier", icon_value=0)
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Animate'):
                if (bpy.context.view_layer.objects.active == None):
                    box_8986E = col_ABD31.box()
                    box_8986E.alert = True
                    box_8986E.enabled = True
                    box_8986E.active = True
                    box_8986E.use_property_split = False
                    box_8986E.use_property_decorate = False
                    box_8986E.alignment = 'Expand'.upper()
                    box_8986E.scale_x = 1.0
                    box_8986E.scale_y = 1.0
                    if not True: box_8986E.operator_context = "EXEC_DEFAULT"
                    box_8986E.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                else:
                    box_9D661 = col_ABD31.box()
                    box_9D661.alert = False
                    box_9D661.enabled = True
                    box_9D661.active = True
                    box_9D661.use_property_split = False
                    box_9D661.use_property_decorate = False
                    box_9D661.alignment = 'Expand'.upper()
                    box_9D661.scale_x = 1.0
                    box_9D661.scale_y = 1.0
                    if not True: box_9D661.operator_context = "EXEC_DEFAULT"
                    layout_function = box_9D661
                    sna_animate_function_interface_57F9E(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'HQ / LQ'):
                box_37F76 = col_ABD31.box()
                box_37F76.alert = False
                box_37F76.enabled = True
                box_37F76.active = True
                box_37F76.use_property_split = False
                box_37F76.use_property_decorate = False
                box_37F76.alignment = 'Expand'.upper()
                box_37F76.scale_x = 1.0
                box_37F76.scale_y = 1.0
                if not True: box_37F76.operator_context = "EXEC_DEFAULT"
                layout_function = box_37F76
                sna_hq_mode_function_interface_17C41(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Render'):
                box_8E19B = col_ABD31.box()
                box_8E19B.alert = False
                box_8E19B.enabled = True
                box_8E19B.active = True
                box_8E19B.use_property_split = False
                box_8E19B.use_property_decorate = False
                box_8E19B.alignment = 'Expand'.upper()
                box_8E19B.scale_x = 1.0
                box_8E19B.scale_y = 1.0
                if not True: box_8E19B.operator_context = "EXEC_DEFAULT"
                layout_function = box_8E19B
                sna_render_function_interface_C67EB(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Omniview'):
                if (bpy.context.view_layer.objects.active == None):
                    box_88A02 = col_ABD31.box()
                    box_88A02.alert = True
                    box_88A02.enabled = True
                    box_88A02.active = True
                    box_88A02.use_property_split = False
                    box_88A02.use_property_decorate = False
                    box_88A02.alignment = 'Expand'.upper()
                    box_88A02.scale_x = 1.0
                    box_88A02.scale_y = 1.0
                    if not True: box_88A02.operator_context = "EXEC_DEFAULT"
                    box_88A02.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                else:
                    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                        box_01DD4 = col_ABD31.box()
                        box_01DD4.alert = False
                        box_01DD4.enabled = True
                        box_01DD4.active = True
                        box_01DD4.use_property_split = False
                        box_01DD4.use_property_decorate = False
                        box_01DD4.alignment = 'Expand'.upper()
                        box_01DD4.scale_x = 1.0
                        box_01DD4.scale_y = 1.0
                        if not True: box_01DD4.operator_context = "EXEC_DEFAULT"
                        layout_function = box_01DD4
                        sna_omnisplat_function_interface_E1B70(layout_function, )
                    else:
                        box_12A7D = col_ABD31.box()
                        box_12A7D.alert = True
                        box_12A7D.enabled = True
                        box_12A7D.active = True
                        box_12A7D.use_property_split = False
                        box_12A7D.use_property_decorate = False
                        box_12A7D.alignment = 'Expand'.upper()
                        box_12A7D.scale_x = 1.0
                        box_12A7D.scale_y = 1.0
                        if not True: box_12A7D.operator_context = "EXEC_DEFAULT"
                        box_12A7D.label(text='Active Object is missing 3DGS Render modifier', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Export'):
                if (bpy.context.view_layer.objects.active == None):
                    box_D35F6 = col_ABD31.box()
                    box_D35F6.alert = True
                    box_D35F6.enabled = True
                    box_D35F6.active = True
                    box_D35F6.use_property_split = False
                    box_D35F6.use_property_decorate = False
                    box_D35F6.alignment = 'Expand'.upper()
                    box_D35F6.scale_x = 1.0
                    box_D35F6.scale_y = 1.0
                    if not True: box_D35F6.operator_context = "EXEC_DEFAULT"
                    box_D35F6.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                else:
                    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.view_layer.objects.active.modifiers):
                        if (len(bpy.context.view_layer.objects.selected) > 1):
                            box_897FA = col_ABD31.box()
                            box_897FA.alert = True
                            box_897FA.enabled = True
                            box_897FA.active = True
                            box_897FA.use_property_split = False
                            box_897FA.use_property_decorate = False
                            box_897FA.alignment = 'Expand'.upper()
                            box_897FA.scale_x = 1.0
                            box_897FA.scale_y = 1.0
                            if not True: box_897FA.operator_context = "EXEC_DEFAULT"
                            box_897FA.label(text='Only select 1 object for export', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                        else:
                            box_AA8F1 = col_ABD31.box()
                            box_AA8F1.alert = False
                            box_AA8F1.enabled = True
                            box_AA8F1.active = True
                            box_AA8F1.use_property_split = False
                            box_AA8F1.use_property_decorate = False
                            box_AA8F1.alignment = 'Expand'.upper()
                            box_AA8F1.scale_x = 1.0
                            box_AA8F1.scale_y = 1.0
                            if not True: box_AA8F1.operator_context = "EXEC_DEFAULT"
                            layout_function = box_AA8F1
                            sna_export_3dgs_function_interface_CDF59(layout_function, )
                    else:
                        box_0FD34 = col_ABD31.box()
                        box_0FD34.alert = True
                        box_0FD34.enabled = True
                        box_0FD34.active = True
                        box_0FD34.use_property_split = False
                        box_0FD34.use_property_decorate = False
                        box_0FD34.alignment = 'Expand'.upper()
                        box_0FD34.scale_x = 1.0
                        box_0FD34.scale_y = 1.0
                        if not True: box_0FD34.operator_context = "EXEC_DEFAULT"
                        box_0FD34.label(text='Active Object is missing Write F_DC_And_Merge modifier', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
        if (bpy.context.scene.sna_kiri3dgs_active_mode == 'Point Cloud'):
            col_DF2EE = col_E242B.column(heading='', align=False)
            col_DF2EE.alert = False
            col_DF2EE.enabled = True
            col_DF2EE.active = True
            col_DF2EE.use_property_split = False
            col_DF2EE.use_property_decorate = False
            col_DF2EE.scale_x = 1.0
            col_DF2EE.scale_y = 1.0
            col_DF2EE.alignment = 'Expand'.upper()
            col_DF2EE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Import'):
                box_456D4 = col_DF2EE.box()
                box_456D4.alert = False
                box_456D4.enabled = True
                box_456D4.active = True
                box_456D4.use_property_split = False
                box_456D4.use_property_decorate = False
                box_456D4.alignment = 'Expand'.upper()
                box_456D4.scale_x = 1.0
                box_456D4.scale_y = 1.0
                if not True: box_456D4.operator_context = "EXEC_DEFAULT"
                layout_function = box_456D4
                sna_point_cloud_import_function_interface_8E4CD(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Modifiers'):
                if (bpy.context.view_layer.objects.active == None):
                    box_0AEC8 = col_DF2EE.box()
                    box_0AEC8.alert = True
                    box_0AEC8.enabled = True
                    box_0AEC8.active = True
                    box_0AEC8.use_property_split = False
                    box_0AEC8.use_property_decorate = False
                    box_0AEC8.alignment = 'Expand'.upper()
                    box_0AEC8.scale_x = 1.0
                    box_0AEC8.scale_y = 1.0
                    if not True: box_0AEC8.operator_context = "EXEC_DEFAULT"
                    box_0AEC8.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                else:
                    if bpy.context.view_layer.objects.active.type == 'MESH':
                        if (len(bpy.context.view_layer.objects.active.data.polygons) > 0):
                            box_1FFE1 = col_DF2EE.box()
                            box_1FFE1.alert = True
                            box_1FFE1.enabled = True
                            box_1FFE1.active = True
                            box_1FFE1.use_property_split = False
                            box_1FFE1.use_property_decorate = False
                            box_1FFE1.alignment = 'Expand'.upper()
                            box_1FFE1.scale_x = 1.0
                            box_1FFE1.scale_y = 1.0
                            if not True: box_1FFE1.operator_context = "EXEC_DEFAULT"
                            box_1FFE1.label(text='Active Object is not a Point Cloud', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                        else:
                            box_C25D2 = col_DF2EE.box()
                            box_C25D2.alert = False
                            box_C25D2.enabled = True
                            box_C25D2.active = True
                            box_C25D2.use_property_split = False
                            box_C25D2.use_property_decorate = False
                            box_C25D2.alignment = 'Expand'.upper()
                            box_C25D2.scale_x = 1.0
                            box_C25D2.scale_y = 1.0
                            if not True: box_C25D2.operator_context = "EXEC_DEFAULT"
                            layout_function = box_C25D2
                            sna_point_cloud_modifier_function_interface_F1E94(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Render'):
                box_66592 = col_DF2EE.box()
                box_66592.alert = False
                box_66592.enabled = True
                box_66592.active = True
                box_66592.use_property_split = False
                box_66592.use_property_decorate = False
                box_66592.alignment = 'Expand'.upper()
                box_66592.scale_x = 1.0
                box_66592.scale_y = 1.0
                if not True: box_66592.operator_context = "EXEC_DEFAULT"
                layout_function = box_66592
                sna_render_function_interface_C67EB(layout_function, )
            if (bpy.context.scene.sna_kiri3dgs_interface_active_sub_interface_mode == 'Export'):
                if (bpy.context.view_layer.objects.active == None):
                    box_5A0C0 = col_DF2EE.box()
                    box_5A0C0.alert = True
                    box_5A0C0.enabled = True
                    box_5A0C0.active = True
                    box_5A0C0.use_property_split = False
                    box_5A0C0.use_property_decorate = False
                    box_5A0C0.alignment = 'Expand'.upper()
                    box_5A0C0.scale_x = 1.0
                    box_5A0C0.scale_y = 1.0
                    if not True: box_5A0C0.operator_context = "EXEC_DEFAULT"
                    box_5A0C0.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                else:
                    if bpy.context.view_layer.objects.active.type == 'MESH':
                        if (len(bpy.context.view_layer.objects.active.data.polygons) > 0):
                            box_C34BE = col_DF2EE.box()
                            box_C34BE.alert = True
                            box_C34BE.enabled = True
                            box_C34BE.active = True
                            box_C34BE.use_property_split = False
                            box_C34BE.use_property_decorate = False
                            box_C34BE.alignment = 'Expand'.upper()
                            box_C34BE.scale_x = 1.0
                            box_C34BE.scale_y = 1.0
                            if not True: box_C34BE.operator_context = "EXEC_DEFAULT"
                            box_C34BE.label(text='Active Object is not a Point Cloud', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                        else:
                            if (len(bpy.context.view_layer.objects.selected) > 1):
                                box_43CB3 = col_DF2EE.box()
                                box_43CB3.alert = True
                                box_43CB3.enabled = True
                                box_43CB3.active = True
                                box_43CB3.use_property_split = False
                                box_43CB3.use_property_decorate = False
                                box_43CB3.alignment = 'Expand'.upper()
                                box_43CB3.scale_x = 1.0
                                box_43CB3.scale_y = 1.0
                                if not True: box_43CB3.operator_context = "EXEC_DEFAULT"
                                box_43CB3.label(text='Only select 1 object for export', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning-7381086-red.png')))
                            else:
                                box_886B7 = col_DF2EE.box()
                                box_886B7.alert = False
                                box_886B7.enabled = True
                                box_886B7.active = True
                                box_886B7.use_property_split = False
                                box_886B7.use_property_decorate = False
                                box_886B7.alignment = 'Expand'.upper()
                                box_886B7.scale_x = 1.0
                                box_886B7.scale_y = 1.0
                                if not True: box_886B7.operator_context = "EXEC_DEFAULT"
                                layout_function = box_886B7
                                sna_point_cloud_export_function_interface_0D64D(layout_function, )
        if (bpy.context.scene.sna_kiri3dgs_active_mode == 'Mesh 2 3DGS'):
            box_E139A = col_E242B.box()
            box_E139A.alert = False
            box_E139A.enabled = True
            box_E139A.active = True
            box_E139A.use_property_split = False
            box_E139A.use_property_decorate = False
            box_E139A.alignment = 'Expand'.upper()
            box_E139A.scale_x = 1.0
            box_E139A.scale_y = 1.0
            if not True: box_E139A.operator_context = "EXEC_DEFAULT"
            layout_function = box_E139A
            sna_mesh_to_3dgs_function_interface_8DDDC(layout_function, )


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_kiri3dgs_interface_active_sub_interface_mode = bpy.props.EnumProperty(name='KIRI3DGS Interface Active Sub Interface Mode', description='', items=[('Import', 'Import', '', 0, 0), ('Modifiers', 'Modifiers', '', 0, 1), ('Colour', 'Colour', '', 0, 2), ('Animate', 'Animate', '', 0, 3), ('HQ / LQ', 'HQ / LQ', '', 0, 4), ('Render', 'Render', '', 0, 5), ('Omniview', 'Omniview', '', 0, 6), ('Export', 'Export', '', 0, 7)])
    bpy.types.Scene.sna_kiri3dgs_interface_active_shading_menu = bpy.props.EnumProperty(name='KIRI3DGS Interface Active Shading Menu', description='', items=[('Selective 1', 'Selective 1', '', 0, 0), ('Selective 2', 'Selective 2', '', 0, 1), ('Selective 3', 'Selective 3', '', 0, 2), ('Vertex Paint', 'Vertex Paint', '', 0, 3), ('Image Overlay', 'Image Overlay', '', 0, 4)])
    bpy.types.Scene.sna_kiri3dgs_active_mode = bpy.props.EnumProperty(name='KIRI3DGS Active Mode', description='', items=[('3DGS', '3DGS', '', 0, 0), ('Point Cloud', 'Point Cloud', '', 0, 1), ('Mesh 2 3DGS', 'Mesh 2 3DGS', '', 0, 2)], update=sna_update_sna_kiri3dgs_active_mode_BA558)
    bpy.types.Scene.sna_kiri3dgs_scene_camera_refresh_mode = bpy.props.EnumProperty(name='KIRI3DGS Scene Camera Refresh Mode', description='', items=[('Continuous', 'Continuous', '', 0, 0), ('Frame Change', 'Frame Change', '', 0, 1)])
    bpy.types.Object.sna_kiri3dgs_active_object_update_mode = bpy.props.EnumProperty(name='KIRI3DGS Active Object Update Mode', description='', items=[('Enable Camera Updates', 'Enable Camera Updates', '', 0, 0), ('Disable Camera Updates', 'Disable Camera Updates', '', 0, 1), ('Show As Point Cloud', 'Show As Point Cloud', '', 0, 2)], update=sna_update_sna_kiri3dgs_active_object_update_mode_868D4)
    bpy.types.Object.sna_kiri3dgs_active_object_enable_active_camera = bpy.props.BoolProperty(name='KIRI3DGS Active Object Enable Active Camera', description='', default=False, update=sna_update_sna_kiri3dgs_active_object_enable_active_camera_DE26E)
    bpy.types.Object.sna_kiri3dgs_active_object_3dgs_baked = bpy.props.BoolProperty(name='KIRI3DGS Active Object 3DGS Baked', description='', default=False)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_decimate = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Decimate', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_decimate_641A7)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_camera_cull = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Camera Cull', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_camera_cull_A98D6)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_crop_box = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Crop Box', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_crop_box_6FCA7)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_colour_edit = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Colour Edit', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_colour_edit_1D6A1)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_remove_by_size = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Remove By Size', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_remove_by_size_488C9)
    bpy.types.Object.sna_kiri3dgs_modifier_enable_animate = bpy.props.BoolProperty(name='KIRI3DGS Modifier Enable Animate', description='', default=False, update=sna_update_sna_kiri3dgs_modifier_enable_animate_1F5D0)
    bpy.types.Scene.sna_kiri3dgs_omnisplat_axes_count = bpy.props.EnumProperty(name='KIRI3DGS Omnisplat Axes Count', description='', items=[('3 Axes', '3 Axes', '', 0, 0), ('5 Axes', '5 Axes', '', 0, 1), ('7 Axes', '7 Axes', '', 0, 2), ('9 Axes', '9 Axes', '', 0, 3)])
    bpy.types.Scene.sna_kiri3dgs_hq_objects_overlap = bpy.props.BoolProperty(name='KIRI3DGS HQ Objects Overlap', description='', default=False, update=sna_update_sna_kiri3dgs_hq_objects_overlap_DDF15)
    bpy.types.Material.sna_kiri3dgs_lq__hq = bpy.props.EnumProperty(name='KIRI3DGS LQ - HQ', description='', items=[('LQ Mode (Dithered Alpha)', 'LQ Mode (Dithered Alpha)', '', 0, 0), ('HQ Mode (Blended Alpha)', 'HQ Mode (Blended Alpha)', '', 0, 1)], update=sna_update_sna_kiri3dgs_lq__hq_065F9)
    bpy.types.Scene.sna_kiri3dgs_quads_and_uv_reset = bpy.props.BoolProperty(name='KIRI3DGS Quads and UV reset', description='', default=False)
    bpy.types.Scene.sna_mesh2gs__validate_meshtexturemtl = bpy.props.BoolProperty(name='MESH2GS - Validate Mesh-Texture-MTL', description='', default=True)
    bpy.types.Scene.sna_kiri3dgs_export__reset_origin = bpy.props.BoolProperty(name='KIRI3DGS- Export - Reset Origin', description='', default=True)
    bpy.types.Scene.sna_mesh2gs__exe_folder = bpy.props.StringProperty(name='MESH2GS - EXE FOLDER', description='', default='Go into mesh2gs folder and - Accept -', subtype='DIR_PATH', maxlen=0)
    bpy.utils.register_class(SNA_OT_Launch_Kiri_Site__3Dgs_D26Bf)
    bpy.utils.register_class(SNA_OT_Launch_Blender_Market__3Dgs_77F72)
    bpy.utils.register_class(SNA_OT_Apply_3Dgs_Modifiers_E67A2)
    bpy.utils.register_class(SNA_OT_Align_Active_To_X_Axis_9B12E)
    bpy.utils.register_class(SNA_OT_Align_Active_To_Y_Axis_9Bd1F)
    bpy.utils.register_class(SNA_OT_Align_Active_To_Z_Axis_720A9)
    bpy.utils.register_class(SNA_OT_Align_Active_To_View_88E3A)
    bpy.utils.register_class(SNA_OT_Bake_Menu_C5Fca)
    bpy.utils.register_class(SNA_OT_Remove_Bake_532E8)
    bpy.utils.register_class(SNA_OT_Align_Active_To_X_Axis001_6Ae0E)
    bpy.utils.register_class(SNA_OT_Align_Active_To_Y_Axis001_C305D)
    bpy.utils.register_class(SNA_OT_Align_Active_To_Z_Axis001_1E184)
    bpy.utils.register_class(SNA_OT_Align_Active_To_View001_30B13)
    bpy.utils.register_class(SNA_OT_Bake_3Dgs_Render_And_Edit_Modifiers_68092)
    bpy.utils.register_class(SNA_OT_Bake_3Dgs_Renderedit_And_Animation_Modifiers_48Bf9)
    bpy.utils.register_class(SNA_OT_Bake_3Dgs_Render_Edit_Animation_And_Sort_Modifiers_76100)
    bpy.utils.register_class(SNA_OT_Remove_Animate_Modifier_5B34D)
    bpy.utils.register_class(SNA_OT_Apply_Animate_Modifier_3938E)
    bpy.utils.register_class(SNA_OT_Add_Animate_Modifier_39C55)
    bpy.types.VIEW3D_MT_object_apply.prepend(sna_add_to_view3d_mt_object_apply_24C48)
    bpy.utils.register_class(SNA_OT_Apply_3Dgs_Tranforms_5B665)
    bpy.utils.register_class(SNA_OT_Set_Shading_Menu_10891)
    bpy.utils.register_class(SNA_OT_Import_Image_Overlay_4A457)
    bpy.utils.register_class(SNA_OT_Start_Vertex_Painting_A36E0)
    bpy.utils.register_class(SNA_OT_Refresh__Create_Paint_Attribute_84655)
    bpy.utils.register_class(SNA_OT_Open_Blender_3Dgs_Render_Documentation_1Eac5)
    bpy.utils.register_class(SNA_OT_Open_Blender_3Dgs_Render_Tutorial_Video_A4Fe6)
    bpy.utils.register_class(SNA_OT_Export_Mesh_Object_As_3Dgs_Ply_Ce2F7)
    bpy.utils.register_class(SNA_OT_Generate_Hq_Object_55455)
    bpy.utils.register_class(SNA_OT_Disable_Hq_Overlap_34678)
    bpy.utils.register_class(SNA_OT_Import_Ply_As_Splats_8458E)
    bpy.utils.register_class(SNA_OT_Dgs_Import_Settings_Bf139)
    bpy.utils.register_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_77E7E)
    bpy.utils.register_class(SNA_OT_Set_Menu_Active_Mode_6Dc45)
    bpy.utils.register_class(SNA_OT_Mesh_2_Gs_3Dfed)
    bpy.utils.register_class(SNA_OT_Remove_Decimate_Modifier_63381)
    bpy.utils.register_class(SNA_OT_Remove_Camera_Cull_Modifier_884Cc)
    bpy.utils.register_class(SNA_OT_Remove_Crop_Box_Modifier_90Df7)
    bpy.utils.register_class(SNA_OT_Remove_Colour_Edit_Modifier_Cddb3)
    bpy.utils.register_class(SNA_OT_Remove_Remove_By_Size_Modifier_95A21)
    bpy.utils.register_class(SNA_OT_Auto_Set_Up_Camera_Cull_Properties_78Ea9)
    bpy.utils.register_class(SNA_OT_Append_Wire_Sphere_2Bf63)
    bpy.utils.register_class(SNA_OT_Append_Wire_Cube_56E0F)
    bpy.utils.register_class(SNA_OT_Apply_Decimate_Modifier_8C14B)
    bpy.utils.register_class(SNA_OT_Apply_Camera_Cull_Modifier_D55D0)
    bpy.utils.register_class(SNA_OT_Apply_Crop_Box_Modifier_36522)
    bpy.utils.register_class(SNA_OT_Apply_Colour_Edit_Modifier_88410)
    bpy.utils.register_class(SNA_OT_Apply_Remove_By_Size_Modifier_3Fdf1)
    bpy.utils.register_class(SNA_OT_Append_And_Add_Geometry_Node_Modifier_C2492)
    bpy.utils.register_class(SNA_OT_Create_Omniview_Object_909Fd)
    bpy.utils.register_class(SNA_OT_Import_Ply_As_Points_E9E21)
    bpy.utils.register_class(SNA_OT_Remove_Point_Edit_Modifier_47851)
    bpy.utils.register_class(SNA_OT_Refresh_Point_Edit_Modifier_Ec829)
    bpy.utils.register_class(SNA_OT_Append_Point_Edit_Modifier_A0188)
    bpy.utils.register_class(SNA_OT_Export_Points_For_3Dgs_63Cd8)
    bpy.utils.register_class(SNA_OT_Apply_Point_Edit_Modifier_D6B08)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Offline_Aea04)
    bpy.utils.register_class(SNA_OT_Dgs__Start_Camera_Update_001Bd)
    bpy.utils.register_class(SNA_OT_Dgs__Stop_Camera_Update_88568)
    bpy.utils.register_class(SNA_OT_Dgs__Update_Camera_Single_Time_03530)
    bpy.app.handlers.load_pre.append(load_pre_handler_F6F13)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Refresh_Scene_Eded7)
    bpy.utils.register_class(SNA_PT_DGS_RENDER__ABOUT__LINKS_PANEL_BA803)
    bpy.utils.register_class(SNA_PT_DGS_RENDER__DOCUMENTATION_PANEL_88B3E)
    bpy.utils.register_class(SNA_PT_DGS_RENDER__MAIN_FUNCTION_PANEL_9D9BF)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_mesh2gs__exe_folder
    del bpy.types.Scene.sna_kiri3dgs_export__reset_origin
    del bpy.types.Scene.sna_mesh2gs__validate_meshtexturemtl
    del bpy.types.Scene.sna_kiri3dgs_quads_and_uv_reset
    del bpy.types.Material.sna_kiri3dgs_lq__hq
    del bpy.types.Scene.sna_kiri3dgs_hq_objects_overlap
    del bpy.types.Scene.sna_kiri3dgs_omnisplat_axes_count
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_animate
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_remove_by_size
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_colour_edit
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_crop_box
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_camera_cull
    del bpy.types.Object.sna_kiri3dgs_modifier_enable_decimate
    del bpy.types.Object.sna_kiri3dgs_active_object_3dgs_baked
    del bpy.types.Object.sna_kiri3dgs_active_object_enable_active_camera
    del bpy.types.Object.sna_kiri3dgs_active_object_update_mode
    del bpy.types.Scene.sna_kiri3dgs_scene_camera_refresh_mode
    del bpy.types.Scene.sna_kiri3dgs_active_mode
    del bpy.types.Scene.sna_kiri3dgs_interface_active_shading_menu
    del bpy.types.Scene.sna_kiri3dgs_interface_active_sub_interface_mode
    bpy.utils.unregister_class(SNA_OT_Launch_Kiri_Site__3Dgs_D26Bf)
    bpy.utils.unregister_class(SNA_OT_Launch_Blender_Market__3Dgs_77F72)
    bpy.utils.unregister_class(SNA_OT_Apply_3Dgs_Modifiers_E67A2)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_X_Axis_9B12E)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_Y_Axis_9Bd1F)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_Z_Axis_720A9)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_View_88E3A)
    bpy.utils.unregister_class(SNA_OT_Bake_Menu_C5Fca)
    bpy.utils.unregister_class(SNA_OT_Remove_Bake_532E8)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_X_Axis001_6Ae0E)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_Y_Axis001_C305D)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_Z_Axis001_1E184)
    bpy.utils.unregister_class(SNA_OT_Align_Active_To_View001_30B13)
    bpy.utils.unregister_class(SNA_OT_Bake_3Dgs_Render_And_Edit_Modifiers_68092)
    bpy.utils.unregister_class(SNA_OT_Bake_3Dgs_Renderedit_And_Animation_Modifiers_48Bf9)
    bpy.utils.unregister_class(SNA_OT_Bake_3Dgs_Render_Edit_Animation_And_Sort_Modifiers_76100)
    bpy.utils.unregister_class(SNA_OT_Remove_Animate_Modifier_5B34D)
    bpy.utils.unregister_class(SNA_OT_Apply_Animate_Modifier_3938E)
    bpy.utils.unregister_class(SNA_OT_Add_Animate_Modifier_39C55)
    bpy.types.VIEW3D_MT_object_apply.remove(sna_add_to_view3d_mt_object_apply_24C48)
    bpy.utils.unregister_class(SNA_OT_Apply_3Dgs_Tranforms_5B665)
    bpy.utils.unregister_class(SNA_OT_Set_Shading_Menu_10891)
    bpy.utils.unregister_class(SNA_OT_Import_Image_Overlay_4A457)
    bpy.utils.unregister_class(SNA_OT_Start_Vertex_Painting_A36E0)
    bpy.utils.unregister_class(SNA_OT_Refresh__Create_Paint_Attribute_84655)
    bpy.utils.unregister_class(SNA_OT_Open_Blender_3Dgs_Render_Documentation_1Eac5)
    bpy.utils.unregister_class(SNA_OT_Open_Blender_3Dgs_Render_Tutorial_Video_A4Fe6)
    bpy.utils.unregister_class(SNA_OT_Export_Mesh_Object_As_3Dgs_Ply_Ce2F7)
    bpy.utils.unregister_class(SNA_OT_Generate_Hq_Object_55455)
    bpy.utils.unregister_class(SNA_OT_Disable_Hq_Overlap_34678)
    bpy.utils.unregister_class(SNA_OT_Import_Ply_As_Splats_8458E)
    bpy.utils.unregister_class(SNA_OT_Dgs_Import_Settings_Bf139)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_77E7E)
    bpy.utils.unregister_class(SNA_OT_Set_Menu_Active_Mode_6Dc45)
    bpy.utils.unregister_class(SNA_OT_Mesh_2_Gs_3Dfed)
    bpy.utils.unregister_class(SNA_OT_Remove_Decimate_Modifier_63381)
    bpy.utils.unregister_class(SNA_OT_Remove_Camera_Cull_Modifier_884Cc)
    bpy.utils.unregister_class(SNA_OT_Remove_Crop_Box_Modifier_90Df7)
    bpy.utils.unregister_class(SNA_OT_Remove_Colour_Edit_Modifier_Cddb3)
    bpy.utils.unregister_class(SNA_OT_Remove_Remove_By_Size_Modifier_95A21)
    bpy.utils.unregister_class(SNA_OT_Auto_Set_Up_Camera_Cull_Properties_78Ea9)
    bpy.utils.unregister_class(SNA_OT_Append_Wire_Sphere_2Bf63)
    bpy.utils.unregister_class(SNA_OT_Append_Wire_Cube_56E0F)
    bpy.utils.unregister_class(SNA_OT_Apply_Decimate_Modifier_8C14B)
    bpy.utils.unregister_class(SNA_OT_Apply_Camera_Cull_Modifier_D55D0)
    bpy.utils.unregister_class(SNA_OT_Apply_Crop_Box_Modifier_36522)
    bpy.utils.unregister_class(SNA_OT_Apply_Colour_Edit_Modifier_88410)
    bpy.utils.unregister_class(SNA_OT_Apply_Remove_By_Size_Modifier_3Fdf1)
    bpy.utils.unregister_class(SNA_OT_Append_And_Add_Geometry_Node_Modifier_C2492)
    bpy.utils.unregister_class(SNA_OT_Create_Omniview_Object_909Fd)
    bpy.utils.unregister_class(SNA_OT_Import_Ply_As_Points_E9E21)
    bpy.utils.unregister_class(SNA_OT_Remove_Point_Edit_Modifier_47851)
    bpy.utils.unregister_class(SNA_OT_Refresh_Point_Edit_Modifier_Ec829)
    bpy.utils.unregister_class(SNA_OT_Append_Point_Edit_Modifier_A0188)
    bpy.utils.unregister_class(SNA_OT_Export_Points_For_3Dgs_63Cd8)
    bpy.utils.unregister_class(SNA_OT_Apply_Point_Edit_Modifier_D6B08)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Offline_Aea04)
    bpy.utils.unregister_class(SNA_OT_Dgs__Start_Camera_Update_001Bd)
    bpy.utils.unregister_class(SNA_OT_Dgs__Stop_Camera_Update_88568)
    bpy.utils.unregister_class(SNA_OT_Dgs__Update_Camera_Single_Time_03530)
    bpy.app.handlers.load_pre.remove(load_pre_handler_F6F13)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Refresh_Scene_Eded7)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER__ABOUT__LINKS_PANEL_BA803)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER__DOCUMENTATION_PANEL_88B3E)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER__MAIN_FUNCTION_PANEL_9D9BF)
