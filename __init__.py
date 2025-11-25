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
    "author" : "KIRI ENGINE", 
    "description" : "3DGS creation, render and editing suite",
    "blender" : (4, 3, 0),
    "version" : (4, 1, 3),
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
import math
from bpy_extras.io_utils import ImportHelper, ExportHelper
import subprocess
import sys
import numpy as np
import time
import datetime
import gpu
import gpu.types
import mathutils
import gpu.state
from gpu_extras.batch import batch_for_shader
import uuid
from math import pi
from mathutils import Matrix
from typing import Optional
# import debugpy

# DEBUG_MODE = False
# if DEBUG_MODE and not debugpy.is_client_connected():
#     print("[DEBUGPY PATH] Current working directory:", os.getcwd())
#     print("[DEBUGPY PATH] __file__ of this module:", __file__)
#     print("[DEBUGPY PATH] sys.path[0]:", os.path.abspath(sys.path[0]) if sys.path else "N/A")
#     print("[DEBUGPY PATH] Full source path example:", os.path.abspath("your_project/__init__.py"))
#     # Optional: make it super obvious in the console
#     debugpy.listen(5678)
#     debugpy.wait_for_client()
#     debugpy.trace_this_thread(True)
#     debugpy.debug_this_thread()

addon_keymaps = {}
_icons = None
dgs_render__active_3dgs_object = {'sna_apply_modifier_list': [], 'sna_in_camera_view': False, }
dgs_render__collection_snippets = {'sna_collections_temp_list': [], }
dgs_render__hq_mode = {'sna_lq_object_list': [], }
dgs_renderdb_filter = {'sna_db_filter_input_object': None, 'sna_db_filter_force_scale_factor': 0.0, }
dgs_renderrender_modemenu_and_functions = {'sna_dgs_proxies_in_scene': False, }


def sna_update_active_object_update_mode_868D4(self, context):
    sna_updated_prop = self.active_object_update_mode
    bpy.context.view_layer.objects.active['update_rot_to_cam'] = (sna_updated_prop == 'Enable Camera Updates')
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = (2 if (sna_updated_prop == 'Show As Point Cloud') else (1 if (sna_updated_prop != 'Enable Camera Updates') else 0))
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport = (True if (sna_updated_prop != 'Disable Camera Updates') else False)
    bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


def sna_update_enable_active_camera_updates_DE26E(self, context):
    sna_updated_prop = self.enable_active_camera_updates
    if sna_updated_prop:
        bpy.context.area.spaces.active.region_3d.view_perspective = 'CAMERA'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop

        def delayed_214CF():
            sna_update_camera_single_time_9EF18()
        bpy.app.timers.register(delayed_214CF, first_interval=0.10000000149011612)
    else:
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop


def sna_update_hq_objects_overlap_DDF15(self, context):
    sna_updated_prop = self.hq_objects_overlap
    if sna_updated_prop:
        pass
    else:
        if (property_exists("bpy.context.scene.objects", globals(), locals()) and 'KIRI_HQ_Merged_Object' in bpy.context.scene.objects):
            bpy.ops.sna.dgs_render_disable_hq_overlap_34678('INVOKE_DEFAULT', )


def sna_update_sna_lq__hq_9D2FF(self, context):
    sna_updated_prop = self.sna_lq__hq
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


def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


def sna_update_active_mode_7EB87(self, context):
    sna_updated_prop = self.active_mode
    if sna_updated_prop == "Edit":
        for i_4F4AB in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_4F4AB].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_4F4AB].modifiers):
                bpy.context.scene.objects[i_4F4AB].modifiers['KIRI_3DGS_Render_GN'].show_viewport = True
                bpy.context.scene.objects[i_4F4AB].modifiers['KIRI_3DGS_Render_GN'].show_render = True
                if (property_exists("bpy.context.scene.objects[i_4F4AB].modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.scene.objects[i_4F4AB].modifiers):
                    bpy.context.scene.objects[i_4F4AB].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = False
                    bpy.context.scene.objects[i_4F4AB].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = False
                if '3dgs_is_hidden' in bpy.context.scene.objects[i_4F4AB]:
                    bpy.context.scene.objects[i_4F4AB].hide_viewport = bpy.context.scene.objects[i_4F4AB]['3dgs_is_hidden']
                else:
                    bpy.context.scene.objects[i_4F4AB]['3dgs_is_hidden'] = False
                    bpy.context.view_layer.objects.active.hide_viewport = False
                if bpy.context.scene.sna_dgs_scene_properties.render_2_hide_object_on_menu_change:
                    target_object = bpy.context.scene.objects[i_4F4AB]
                    hide_set = False
                    # Input variables
                    #target_object = bpy.data.objects["Cube"]  # Change this to your object
                    #hide_set = True  # True to hide set, False to unhide set
                    if target_object:
                        target_object.hide_set(hide_set)
                        action = "applied" if hide_set else "removed"
                        print(f"Hide set {action} to: {target_object.name}")
                    else:
                        print("Target object not found")
        sna_clean_up_scene_5F1F1(False)
    elif sna_updated_prop == "Render":
        bpy.context.scene.sna_dgs_scene_properties.render_2_interface_mode = 'Update'
        for i_F44D4 in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_F44D4].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_F44D4].modifiers):
                bpy.context.scene.objects[i_F44D4].modifiers['KIRI_3DGS_Render_GN'].show_viewport = False
                bpy.context.scene.objects[i_F44D4].modifiers['KIRI_3DGS_Render_GN'].show_render = False
                if (property_exists("bpy.context.scene.objects[i_F44D4].modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.scene.objects[i_F44D4].modifiers):
                    bpy.context.scene.objects[i_F44D4].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = True
                    bpy.context.scene.objects[i_F44D4].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = True
                bpy.context.scene.objects[i_F44D4]['3dgs_is_hidden'] = bpy.context.scene.objects[i_F44D4].hide_viewport
                if bpy.context.scene.sna_dgs_scene_properties.render_2_hide_object_on_menu_change:
                    target_object = bpy.context.scene.objects[i_F44D4]
                    hide_set = True
                    # Input variables
                    #target_object = bpy.data.objects["Cube"]  # Change this to your object
                    #hide_set = True  # True to hide set, False to unhide set
                    if target_object:
                        target_object.hide_set(hide_set)
                        action = "applied" if hide_set else "removed"
                        print(f"Hide set {action} to: {target_object.name}")
                    else:
                        print("Target object not found")
        dgs_renderrender_modemenu_and_functions['sna_dgs_proxies_in_scene'] = False
        for i_55B06 in range(len(bpy.context.scene.objects)):
            if 'gaussian_source_uuid' in bpy.context.scene.objects[i_55B06]:
                dgs_renderrender_modemenu_and_functions['sna_dgs_proxies_in_scene'] = True
        for i_0415D in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_0415D].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_0415D].modifiers):
                bpy.context.scene.objects[i_0415D].hide_viewport = False
        if dgs_renderrender_modemenu_and_functions['sna_dgs_proxies_in_scene']:
            sna_c2_refresh_all_4D367(True, bpy.context.scene.sna_dgs_scene_properties.render_2_copy_source_transforms, True)
            sna_shader_system_A4AED()
            sna_texture_creation_FD1B2()
            sna_viewport_render_A3941()
        bpy.context.view_layer.objects.active = None
        for i_8C52E in range(len(bpy.context.scene.objects)):
            if ((property_exists("bpy.context.scene.objects[i_8C52E].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_8C52E].modifiers) and '3DGS_Mesh_Type' in bpy.context.scene.objects[i_8C52E]):
                if (bpy.context.scene.objects[i_8C52E]['3DGS_Mesh_Type'] == 'face'):
                    bpy.context.scene.objects[i_8C52E].hide_viewport = True
    elif sna_updated_prop == "Mesh 2 3DGS":
        sna_clean_up_scene_5F1F1(False)
        bpy.context.view_layer.objects.active = None
    else:
        pass


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


class SNA_OT_Dgs_Render_Launch_Kiri_Site_Bf973(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_kiri_site_bf973"
    bl_label = "3DGS Render: Launch KIRI Site"
    bl_description = "Launches a browser for the KIRI Engine main site"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.app/'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Launch_Superhive_Store_08F23(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_superhive_store_08f23"
    bl_label = "3DGS Render: Launch SuperHive Store"
    bl_description = "Launches a browser for the KIRI Engine SuperHive store"
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


def sna_about_kiri_links_docs_3dgs_D02EC(layout_function, ):
    box_12166 = layout_function.box()
    box_12166.alert = False
    box_12166.enabled = True
    box_12166.active = True
    box_12166.use_property_split = False
    box_12166.use_property_decorate = False
    box_12166.alignment = 'Expand'.upper()
    box_12166.scale_x = 1.0
    box_12166.scale_y = 1.0
    if not True: box_12166.operator_context = "EXEC_DEFAULT"
    col_CB7BF = box_12166.column(heading='', align=True)
    col_CB7BF.alert = False
    col_CB7BF.enabled = True
    col_CB7BF.active = True
    col_CB7BF.use_property_split = False
    col_CB7BF.use_property_decorate = False
    col_CB7BF.scale_x = 1.0
    col_CB7BF.scale_y = 1.0
    col_CB7BF.alignment = 'Expand'.upper()
    col_CB7BF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_D36BE = col_CB7BF.box()
    box_D36BE.alert = False
    box_D36BE.enabled = True
    box_D36BE.active = True
    box_D36BE.use_property_split = False
    box_D36BE.use_property_decorate = False
    box_D36BE.alignment = 'Center'.upper()
    box_D36BE.scale_x = 1.0
    box_D36BE.scale_y = 1.0
    if not True: box_D36BE.operator_context = "EXEC_DEFAULT"
    box_D36BE.label(text='About KIRI Engine', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    box_D36BE.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Addon speel 2.png')), scale=10.0)
    op = box_D36BE.operator('sna.dgs_render_launch_kiri_site_bf973', text='Learn More', icon_value=0, emboss=True, depress=False)
    box_28D7F = col_CB7BF.box()
    box_28D7F.alert = False
    box_28D7F.enabled = True
    box_28D7F.active = True
    box_28D7F.use_property_split = False
    box_28D7F.use_property_decorate = True
    box_28D7F.alignment = 'Expand'.upper()
    box_28D7F.scale_x = 1.0
    box_28D7F.scale_y = 1.2000000476837158
    if not True: box_28D7F.operator_context = "EXEC_DEFAULT"
    split_F339F = box_28D7F.split(factor=0.30000001192092896, align=False)
    split_F339F.alert = False
    split_F339F.enabled = True
    split_F339F.active = True
    split_F339F.use_property_split = False
    split_F339F.use_property_decorate = False
    split_F339F.scale_x = 1.0
    split_F339F.scale_y = 1.0
    split_F339F.alignment = 'Expand'.upper()
    if not True: split_F339F.operator_context = "EXEC_DEFAULT"
    split_F339F.prop(bpy.context.scene.sna_dgs_scene_properties, 'show_tips', text='Tips', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')), emboss=True)
    row_273F5 = split_F339F.row(heading='', align=False)
    row_273F5.alert = False
    row_273F5.enabled = True
    row_273F5.active = True
    row_273F5.use_property_split = False
    row_273F5.use_property_decorate = False
    row_273F5.scale_x = 1.0
    row_273F5.scale_y = 1.0
    row_273F5.alignment = 'Right'.upper()
    row_273F5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = row_273F5.operator('sna.dgs_render_open_documentation_3a04f', text='Documentation', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'documentation.svg')), emboss=True, depress=False)
    op = row_273F5.operator('sna.dgs_render_open_tutorial_video_0684a', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'video.svg')), emboss=True, depress=False)
    box_DE3AB = col_CB7BF.box()
    box_DE3AB.alert = False
    box_DE3AB.enabled = True
    box_DE3AB.active = True
    box_DE3AB.use_property_split = False
    box_DE3AB.use_property_decorate = False
    box_DE3AB.alignment = 'Expand'.upper()
    box_DE3AB.scale_x = 1.0
    box_DE3AB.scale_y = 1.0
    if not True: box_DE3AB.operator_context = "EXEC_DEFAULT"
    row_7D004 = box_DE3AB.row(heading='', align=False)
    row_7D004.alert = False
    row_7D004.enabled = True
    row_7D004.active = True
    row_7D004.use_property_split = False
    row_7D004.use_property_decorate = False
    row_7D004.scale_x = 1.0
    row_7D004.scale_y = 1.2000000476837158
    row_7D004.alignment = 'Expand'.upper()
    row_7D004.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_7D004.label(text='Get More Addons', icon_value=0)
    split_649B4 = row_7D004.split(factor=0.5, align=False)
    split_649B4.alert = False
    split_649B4.enabled = True
    split_649B4.active = True
    split_649B4.use_property_split = False
    split_649B4.use_property_decorate = False
    split_649B4.scale_x = 1.0
    split_649B4.scale_y = 1.0
    split_649B4.alignment = 'Expand'.upper()
    if not True: split_649B4.operator_context = "EXEC_DEFAULT"
    op = split_649B4.operator('sna.dgs_render_launch_superhive_store_08f23', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'SuperHive Logo White.png')), emboss=True, depress=False)
    op = split_649B4.operator('sna.dgs_render_launch_kiri_blender_addons_page_9d58c', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine blender addon icon color.svg')), emboss=True, depress=False)


class SNA_OT_Dgs_Render_Launch_Kiri_Blender_Addons_Page_9D58C(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_kiri_blender_addons_page_9d58c"
    bl_label = "3DGS Render: Launch KIRI Blender Addons page"
    bl_description = "Launches a browser for the KIRI Engine Blender Market store"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.app/blender-addon'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Open_Documentation_3A04F(bpy.types.Operator):
    bl_idname = "sna.dgs_render_open_documentation_3a04f"
    bl_label = "3DGS Render: Open Documentation"
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


class SNA_OT_Dgs_Render_Open_Tutorial_Video_0684A(bpy.types.Operator):
    bl_idname = "sna.dgs_render_open_tutorial_video_0684a"
    bl_label = "3DGS Render: Open Tutorial Video"
    bl_description = "Launches a browser with the addon documentation video"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.youtube.com/@BlenderAddon-fromKIRI'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


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
        col_F0A3B.alert = (bpy.context.view_layer.objects.active.sna_dgs_object_properties.active_object_update_mode == 'Disable Camera Updates')
        col_F0A3B.enabled = True
        col_F0A3B.active = True
        col_F0A3B.use_property_split = False
        col_F0A3B.use_property_decorate = False
        col_F0A3B.scale_x = 1.0
        col_F0A3B.scale_y = 1.0
        col_F0A3B.alignment = 'Expand'.upper()
        col_F0A3B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_F0A3B.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'active_object_update_mode', text='', icon_value=0, emboss=True, toggle=True)
        col_A4D20.separator(factor=1.0)
        if ((bpy.context.view_layer.objects.active.sna_dgs_object_properties.active_object_update_mode == 'Enable Camera Updates') and (not bpy.context.view_layer.objects.active.sna_dgs_object_properties.enable_active_camera_updates)):
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
        if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.active_object_update_mode == 'Show As Point Cloud'):
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
        if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.active_object_update_mode == 'Enable Camera Updates'):
            box_DC5A2 = col_A4D20.box()
            box_DC5A2.alert = bpy.context.view_layer.objects.active.sna_dgs_object_properties.enable_active_camera_updates
            box_DC5A2.enabled = True
            box_DC5A2.active = True
            box_DC5A2.use_property_split = False
            box_DC5A2.use_property_decorate = False
            box_DC5A2.alignment = 'Expand'.upper()
            box_DC5A2.scale_x = 1.0
            box_DC5A2.scale_y = 1.0
            if not True: box_DC5A2.operator_context = "EXEC_DEFAULT"
            if ((bpy.context.scene.camera == None) and bpy.context.view_layer.objects.active.sna_dgs_object_properties.enable_active_camera_updates):
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
            box_DC5A2.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'enable_active_camera_updates', text='Use Active Camera', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera.svg')), emboss=True, toggle=True)


class SNA_OT_Dgs_Render_Align_Active_To_X_Axis_6Ae0E(bpy.types.Operator):
    bl_idname = "sna.dgs_render_align_active_to_x_axis_6ae0e"
    bl_label = "3DGS Render: Align Active To X Axis"
    bl_description = "Updates the 3DGS_Render modifier once to the X axis for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_align_active_values_to_x_4CE1F()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Align_Active_To_Y_Axis_C305D(bpy.types.Operator):
    bl_idname = "sna.dgs_render_align_active_to_y_axis_c305d"
    bl_label = "3DGS Render: Align Active To Y Axis"
    bl_description = "Updates the 3DGS_Render modifier once to the Y axis for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_align_active_values_to_y_E5E9E()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Align_Active_To_Z_Axis_1E184(bpy.types.Operator):
    bl_idname = "sna.dgs_render_align_active_to_z_axis_1e184"
    bl_label = "3DGS Render: Align Active To Z Axis"
    bl_description = "Updates the 3DGS_Render modifier once to the Z axis for the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_align_active_values_to_z_7B9ED()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Align_Active_To_View_30B13(bpy.types.Operator):
    bl_idname = "sna.dgs_render_align_active_to_view_30b13"
    bl_label = "3DGS Render: Align Active To View"
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
                col_44B28.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'], '["Socket_5"]', bpy.context.scene.collection, 'children', text='', icon='NONE')
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
        if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 1) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 2)):
            box_5900C = box_F6C6C.box()
            box_5900C.alert = False
            box_5900C.enabled = True
            box_5900C.active = True
            box_5900C.use_property_split = False
            box_5900C.use_property_decorate = False
            box_5900C.alignment = 'Expand'.upper()
            box_5900C.scale_x = 1.0
            box_5900C.scale_y = 1.0
            if not True: box_5900C.operator_context = "EXEC_DEFAULT"
            box_5900C.label(text='To Points/Curves only ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_5900C.label(text='visible in Edit mode renders.', icon_value=0)
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
        row_07DA9.label(text='Animate Modifier', icon_value=0)
        op = row_07DA9.operator('sna.dgs_render_add_animate_modifier_39c55', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)


class SNA_OT_Dgs_Render_Remove_Animate_Modifier_5B34D(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_animate_modifier_5b34d"
    bl_label = "3DGS Render: Remove Animate Modifier"
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


class SNA_OT_Dgs_Render_Apply_Animate_Modifier_3938E(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_animate_modifier_3938e"
    bl_label = "3DGS Render: Apply Animate Modifier"
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


class SNA_OT_Dgs_Render_Add_Animate_Modifier_39C55(bpy.types.Operator):
    bl_idname = "sna.dgs_render_add_animate_modifier_39c55"
    bl_label = "3DGS Render: Add Animate Modifier"
    bl_description = "Adds a 3DGS animate modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.view_layer.objects.active.type == 'MESH' or bpy.context.view_layer.objects.active.type == 'CURVE'):
            created_modifier_0_3280f = sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Animate_GN', 'KIRI_3DGS_Animate_GN', bpy.context.view_layer.objects.active)
        else:
            self.report({'INFO'}, message='The Active Object is not a mesh or curve object.')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_add_to_view3d_mt_object_apply_3CED8(self, context):
    if not (False):
        layout = self.layout
        op = layout.operator('sna.dgs_render_apply_3dgs_tranforms_5b665', text='Apply 3DGS Transforms and Colour', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine icon.svg')), emboss=True, depress=False)


class SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_3dgs_tranforms_5b665"
    bl_label = "3DGS Render: Apply 3DGS Tranforms"
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
    box_A85FA.prop(bpy.context.scene.sna_dgs_scene_properties, 'active_shading_menu', text=bpy.context.scene.sna_dgs_scene_properties.active_shading_menu, icon_value=0, emboss=True, expand=True)
    col_EB8EB.separator(factor=1.0)
    if bpy.context.scene.sna_dgs_scene_properties.active_shading_menu == "Selective 1":
        layout_function = col_EB8EB
        sna_selective_adjustment_1_function_interface_AD57C(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.active_shading_menu == "Selective 2":
        layout_function = col_EB8EB
        sna_selective_adjustment_2_function_interface_4A09B(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.active_shading_menu == "Selective 3":
        layout_function = col_EB8EB
        sna_selective_adjustment_3_function_interface_69C53(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.active_shading_menu == "Vertex Paint":
        layout_function = col_EB8EB
        sna_vertex_paint_function_interface_BEA3E(layout_function, )
    elif bpy.context.scene.sna_dgs_scene_properties.active_shading_menu == "Image Overlay":
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
    row_4E69D.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'], '["Socket_60"]', bpy.data, 'images', text='', icon='NONE')
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


class SNA_OT_Dgs_Render_Import_Image_Overlay_4A457(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.dgs_render_import_image_overlay_4a457"
    bl_label = "3DGS Render: Import Image Overlay"
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


class SNA_OT_Dgs_Render_Start_Vertex_Painting_A36E0(bpy.types.Operator):
    bl_idname = "sna.dgs_render_start_vertex_painting_a36e0"
    bl_label = "3DGS Render: Start Vertex Painting"
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


class SNA_OT_Dgs_Render_Refresh__Create_Paint_Attribute_84655(bpy.types.Operator):
    bl_idname = "sna.dgs_render_refresh__create_paint_attribute_84655"
    bl_label = "3DGS Render: Refresh - Create Paint Attribute"
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
        grid_B53F5.prop(bpy.context.scene.sna_dgs_scene_properties, 'edit_mode_active_menu', text=bpy.context.scene.sna_dgs_scene_properties.edit_mode_active_menu, icon_value=0, emboss=True, expand=True)
    if bpy.context.scene.sna_dgs_scene_properties.edit_mode_active_menu == "Import":
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
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_active_menu == "Modifiers":
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
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_active_menu == "Colour":
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
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_active_menu == "Animate":
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
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_active_menu == "HQ / LQ":
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
    elif bpy.context.scene.sna_dgs_scene_properties.edit_mode_active_menu == "Export":
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


class SNA_OT_Dgs_Render_Export_Mesh_Object_As_3Dgs_Ply_Ce2F7(bpy.types.Operator):
    bl_idname = "sna.dgs_render_export_mesh_object_as_3dgs_ply_ce2f7"
    bl_label = "3DGS Render: Export Mesh Object As 3DGS PLY"
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
        box_44942.alert = False
        box_44942.enabled = True
        box_44942.active = True
        box_44942.use_property_split = False
        box_44942.use_property_decorate = False
        box_44942.alignment = 'Expand'.upper()
        box_44942.scale_x = 1.0
        box_44942.scale_y = 1.0
        if not True: box_44942.operator_context = "EXEC_DEFAULT"
        box_44942.label(text='All modifiers will be applied. To continue working in Blender', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_44942.label(text='         it is advised to make a duplicate before exporting.', icon_value=0)
        box_44942.label(text='         Press OK to continue exporting', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


def sna_hq_mode_function_interface_17C41(layout_function, ):
    if (bpy.context.scene.render.engine == 'CYCLES'):
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
                box_2E343.prop(bpy.context.view_layer.objects.active.material_slots[i_E3C27].material, 'sna_lq__hq', text='', icon_value=0, emboss=True)
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
    box_D2847.prop(bpy.context.scene.sna_dgs_scene_properties, 'hq_objects_overlap', text='HQ Objects Overlap', icon_value=0, emboss=True, toggle=False)
    if bpy.context.scene.sna_dgs_scene_properties.hq_objects_overlap:
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


class SNA_OT_Dgs_Render_Generate_Hq_Object_55455(bpy.types.Operator):
    bl_idname = "sna.dgs_render_generate_hq_object_55455"
    bl_label = "3DGS Render: Generate HQ Object"
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
                bpy.data.objects[i_3F5D0].sna_dgs_object_properties.enable_active_camera_updates = True
                bpy.data.objects[i_3F5D0].modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = True

        def delayed_CB67D():
            sna_update_camera_single_time_9EF18()

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
                bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V4.blend') + r'\Object', filename='KIRI_HQ_Merged_Object', link=False)
                new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
                appended_D9EAC = None if not new_data else new_data[0]
                sna_move_object_to_collection_create_if_missingfunction_execute_AB682('KIRI_HQ_Merged_Object', '3DGS_HQ_Object', 'COLOR_05')
                sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Instance_HQ', 'KIRI_3DGS_Instance_HQ', bpy.data.objects['KIRI_HQ_Merged_Object'])
                bpy.data.objects['KIRI_HQ_Merged_Object'].modifiers['KIRI_3DGS_Instance_HQ']['Socket_2'] = bpy.data.collections['3DGS_LQ_Objects']
                if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
                    pass
                else:
                    before_data = list(bpy.data.materials)
                    bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V4.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
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
        box_B5524.alert = False
        box_B5524.enabled = True
        box_B5524.active = True
        box_B5524.use_property_split = False
        box_B5524.use_property_decorate = False
        box_B5524.alignment = 'Expand'.upper()
        box_B5524.scale_x = 1.0
        box_B5524.scale_y = 1.0
        if not True: box_B5524.operator_context = "EXEC_DEFAULT"
        box_B5524.label(text="All original 'LQ' objects will be moved into '3DGS_LQ_Objects' collection", icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_B5524.label(text="        A new object -'KIRI_HQ_Merged_Object' - will be created", icon_value=0)
        box_B5524.label(text='        Use the LQ / HQ drop down to toggle between original and HQ object visibilities', icon_value=0)
        box_B5524.label(text='        Do not rename the created collections', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_OT_Dgs_Render_Disable_Hq_Overlap_34678(bpy.types.Operator):
    bl_idname = "sna.dgs_render_disable_hq_overlap_34678"
    bl_label = "3DGS Render: Disable HQ Overlap"
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
        box_2D485.alert = False
        box_2D485.enabled = True
        box_2D485.active = True
        box_2D485.use_property_split = False
        box_2D485.use_property_decorate = False
        box_2D485.alignment = 'Expand'.upper()
        box_2D485.scale_x = 1.0
        box_2D485.scale_y = 1.0
        if not True: box_2D485.operator_context = "EXEC_DEFAULT"
        box_2D485.label(text='HQ Object Found In Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_2D485.label(text='        Remove It?', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


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
    box_DCCA2.enabled = ((not ((bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.render_2_interval_stop))) and 'OBJECT'==bpy.context.mode)
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


class SNA_OT_Dgs_Render_Update_Enabled_3Dgs_Objects_6D7F4(bpy.types.Operator):
    bl_idname = "sna.dgs_render_update_enabled_3dgs_objects_6d7f4"
    bl_label = "3DGS Render: Update Enabled 3DGS Objects"
    bl_description = "Updates all enabled 3DGS objects faces to the current view."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_update_camera_single_time_9EF18()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_update_camera_single_time_9EF18():
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
    for i_56B01 in range(len(bpy.context.scene.objects)):
        bpy.context.scene.objects[i_56B01].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()


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
    box_9766A.prop(bpy.context.scene.sna_dgs_scene_properties, 'mesh2gs_validate_files', text='Validate Mesh, Texture and .MTL', icon_value=0, emboss=True)
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


class SNA_OT_Dgs_Render_Mesh23Dgs_3Dfed(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.dgs_render_mesh23dgs_3dfed"
    bl_label = "3DGS Render: Mesh-2-3DGS"
    bl_description = "Convert a chosen .OBJ to 3DGS .PLY"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.obj', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_dgs_scene_properties.mesh2gs_validate_files:
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
                    try:
                        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
                    except Exception as e:
                        raise RuntimeError(e)
                    print("run successfully. Save in", output_path)
                else:
                    self.report({'ERROR'}, message='File structure is incorrect - see documentation')
            else:
                self.report({'WARNING'}, message='Mesh is not triangulated?')
        else:
            obj_path = bpy.path.abspath(self.filepath)
            output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
            exe_path = bpy.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'mesh2gs'))
            import platform
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
            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
            except Exception as e:
                raise RuntimeError(e)
            print("run successfully. Save in", output_path)
        return {"FINISHED"}


class SNA_OT_Dgs_Render_Auto_Generate_Crop_Object_F20D5(bpy.types.Operator):
    bl_idname = "sna.dgs_render_auto_generate_crop_object_f20d5"
    bl_label = "3DGS Render: Auto Generate Crop Object"
    bl_description = "Generate a crop object based on point clustering"
    bl_options = {"REGISTER", "UNDO"}

    def sna_filter_mode_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_filter_mode: bpy.props.EnumProperty(name='Filter Mode', description='', options={'HIDDEN'}, items=[('quick', 'quick', '', 0, 0), ('gentle', 'gentle', '', 0, 1), ('aggressive', 'aggressive', '', 0, 2)])
    sna_filter_epsilon: bpy.props.FloatProperty(name='Filter Epsilon', description='', options={'HIDDEN'}, default=0.029999999329447746, subtype='NONE', unit='NONE', min=0.009999999776482582, max=0.10000000149011612, step=3, precision=2)
    sna_filter_min_points: bpy.props.IntProperty(name='Filter Min Points', description='', options={'HIDDEN'}, default=10, subtype='NONE', min=1)
    sna_fast_mode: bpy.props.BoolProperty(name='Fast Mode', description='', options={'HIDDEN'}, default=False)
    sna_create_convex_hull_object: bpy.props.BoolProperty(name='Create Convex Hull Object', description='', options={'HIDDEN'}, default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        OPEN3D_AVAILABLE = None
        #!/usr/bin/env python3
        """
        Open3D Availability Checker (ASCII-only)
        ========================================
        Simple standalone script to test if Open3D can be imported in Blender.
        Returns boolean result for programmatic use.
        Usage:
        - Run in Blender's Text Editor
        - Check console for result
        - Use returned boolean in other scripts
        """

        def check_open3d_availability():
            """
            Test if Open3D can be imported successfully.
            Returns:
                bool: True if Open3D is available, False otherwise
            """
            print("Testing Open3D availability...")
            try:
                import open3d as o3d
                # Basic import successful
                print("SUCCESS: Open3D import successful")
                print("Version: " + str(o3d.__version__))
                # Test basic functionality
                try:
                    # Try creating a basic point cloud
                    import numpy as np
                    test_points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
                    pcd = o3d.geometry.PointCloud()
                    pcd.points = o3d.utility.Vector3dVector(test_points)
                    print("SUCCESS: Basic functionality test passed")
                    print("Test point cloud created with " + str(len(pcd.points)) + " points")
                    return True
                except Exception as e:
                    print("WARNING: Open3D imported but basic functionality failed")
                    print("Error: " + str(e))
                    return False
            except ImportError as e:
                print("FAILED: Open3D import failed")
                print("Error: " + str(e))
                print("Install Open3D wheels to enable point cloud filtering")
                return False
            except Exception as e:
                print("ERROR: Open3D import unexpected error")
                print("Error: " + str(e))
                return False

        def main():
            """Main function with detailed output"""
            print("=" * 50)
            print("OPEN3D AVAILABILITY TEST")
            print("=" * 50)
            # Test availability
            is_available = check_open3d_availability()
            print("")
            print("=" * 50)
            print("RESULT")
            print("=" * 50)
            if is_available:
                print("RESULT: Open3D is AVAILABLE")
                print("STATUS: DB filtering can be enabled")
                print("STATUS: Point cloud operations will work")
            else:
                print("RESULT: Open3D is NOT AVAILABLE")
                print("STATUS: DB filtering is disabled")
                print("INFO: Install Open3D wheels to enable functionality")
            print("")
            print("Boolean result: " + str(is_available))
            return is_available
        # Global variable for easy access
        OPEN3D_AVAILABLE = None
        # Auto-execute when script runs
        if __name__ == "__main__" or True:
            OPEN3D_AVAILABLE = main()
            # Store result in a way other scripts can access
            try:
                import bpy
                # Store in scene properties if in Blender
                if hasattr(bpy.context, 'scene'):
                    bpy.context.scene['open3d_available'] = OPEN3D_AVAILABLE
                    print("INFO: Stored result in scene['open3d_available'] = " + str(OPEN3D_AVAILABLE))
            except:
                pass  # Not in Blender or no scene context
        # ===== USAGE EXAMPLES =====
        print("""
        === USAGE EXAMPLES ===
        1. PROGRAMMATIC USE:
           result = check_open3d_availability()
           if result:
               # Run Open3D operations
           else:
               # Show error message
        2. SERPENS INTEGRATION:
           # Check the global variable
           if OPEN3D_AVAILABLE:
               # Enable DB filter UI
           else:
               # Show installation message
        3. SCENE PROPERTY ACCESS:
           # Access from other scripts
           is_available = bpy.context.scene.get('open3d_available', False)
        4. QUICK TEST:
           # Just run this script to see status
        """)
        if OPEN3D_AVAILABLE:
            filter_eps = self.sna_filter_epsilon
            filter_min_points = self.sna_filter_min_points
            filter_mode = self.sna_filter_mode
            filter_fast_mode = self.sna_fast_mode
            filter_result_object = None
            import bmesh
            from mathutils import Vector
            # ===== SAFE OPEN3D AVAILABILITY CHECK =====
            # Global flag to control script execution
            OPEN3D_AVAILABLE = False
            o3d = None
            try:
                import open3d as o3d
                OPEN3D_AVAILABLE = True
                print("✅ Open3D available - DB filtering enabled")
                print(f"   Open3D version: {o3d.__version__}")
            except ImportError as e:
                OPEN3D_AVAILABLE = False
                o3d = None
                print("⚠️ Open3D not available - DB filtering disabled")
                print("   Install Open3D wheels to enable point cloud filtering")
                print("   Script will not execute any filtering operations")
            # ===== SERPENS GLOBAL VARIABLES =====
            # Main filtering mode - change this value in Serpens
            #filter_mode = "quick"  # Default value for when not set by Serpens
            # Optional object name - leave empty to use active object
            filter_obj_name = ""
            # GLOBAL OUTPUT VARIABLE - stores the result of the last filter operation
            filter_result_object = None
            # DBSCAN parameters
            #filter_eps = 0.03  # Default value for when not set by Serpens
            #filter_min_points = 10
            filter_auto_eps = False
            # Statistical outlier removal parameters
            filter_nb_neighbors = 20
            filter_std_ratio = 2.0
            # Radius outlier removal parameters
            filter_radius_nb_points = 16
            filter_radius = 0.05
            # ===== PERFORMANCE OPTIMIZATION VARIABLES =====
            # Speed optimization settings
            filter_use_voxel_downsample = True
            filter_voxel_size = 0.01
            filter_max_points = 100000
            #filter_fast_mode = True  # Default value for when not set by Serpens
            filter_sample_ratio = 0.3
            # ===== TIMING VARIABLES =====
            # Timing control
            filter_show_timing = True  # Set to False to disable timing output
            # ===== TIMING UTILITIES =====

            def format_time(seconds):
                """Format time in a readable way"""
                if seconds < 1:
                    return f"{seconds*1000:.1f}ms"
                elif seconds < 60:
                    return f"{seconds:.2f}s"
                else:
                    minutes = int(seconds // 60)
                    remaining_seconds = seconds % 60
                    return f"{minutes}m {remaining_seconds:.1f}s"

            def time_function(func, *args, **kwargs):
                """Wrapper to time function execution"""
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                if filter_show_timing:
                    print(f"⏱️  {func.__name__} took {format_time(execution_time)}")
                return result, execution_time
            # ===== SAFETY CHECK FUNCTION =====

            def check_open3d_available():
                """Check if Open3D is available and return appropriate message"""
                if not OPEN3D_AVAILABLE:
                    print("❌ DB filtering unavailable - Open3D not installed")
                    print("   Install Open3D wheels and restart Blender to enable filtering")
                    return False
                return True
            # ===== MAIN FUNCTIONS (Only defined if Open3D available) =====
            if OPEN3D_AVAILABLE:

                def mesh_to_point_cloud(obj_name):
                    """Convert Blender mesh to Open3D point cloud"""
                    obj = bpy.data.objects[obj_name]
                    mesh = obj.data
                    # Get world coordinates of vertices
                    points = []
                    for vertex in mesh.vertices:
                        world_coord = obj.matrix_world @ vertex.co
                        points.append([world_coord.x, world_coord.y, world_coord.z])
                    # Create Open3D point cloud
                    pcd = o3d.geometry.PointCloud()
                    pcd.points = o3d.utility.Vector3dVector(np.array(points))
                    return pcd, np.array(points)

                def filter_with_dbscan(pcd, eps=0.1, min_points=10):
                    """Apply DBSCAN clustering to filter point cloud"""
                    print(f"Starting DBSCAN with eps={eps}, min_points={min_points}")
                    print(f"Point cloud has {len(pcd.points)} points")
                    # Apply DBSCAN clustering
                    labels = np.array(pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True))
                    # Analyze clusters
                    max_label = labels.max()
                    print(f"Point cloud has {max_label + 1} clusters")
                    # Count points in each cluster
                    cluster_counts = {}
                    noise_count = np.sum(labels == -1)
                    for i in range(max_label + 1):
                        count = np.sum(labels == i)
                        cluster_counts[i] = count
                        print(f"Cluster {i}: {count} points")
                    print(f"Noise points: {noise_count}")
                    return labels, cluster_counts

                def filter_with_statistical_outlier_removal(pcd, nb_neighbors=20, std_ratio=2.0):
                    """Remove statistical outliers"""
                    print(f"Applying statistical outlier removal (neighbors={nb_neighbors}, std_ratio={std_ratio})")
                    pcd_filtered, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
                    print(f"Removed {len(pcd.points) - len(pcd_filtered.points)} outlier points")
                    return pcd_filtered, ind

                def filter_with_radius_outlier_removal(pcd, nb_points=16, radius=0.05):
                    """Remove points with few neighbors in radius"""
                    print(f"Applying radius outlier removal (nb_points={nb_points}, radius={radius})")
                    pcd_filtered, ind = pcd.remove_radius_outlier(nb_points=nb_points, radius=radius)
                    print(f"Removed {len(pcd.points) - len(pcd_filtered.points)} sparse points")
                    return pcd_filtered, ind

                def optimize_point_cloud_for_speed(pcd, max_points=100000, voxel_size=0.01, sample_ratio=0.3, use_voxel=True):
                    """Optimize point cloud for faster processing"""
                    original_size = len(pcd.points)
                    print(f"Original point cloud: {original_size} points")
                    if original_size <= max_points:
                        print("Point cloud size OK, no optimization needed")
                        return pcd, np.arange(original_size)
                    if use_voxel:
                        # Voxel downsampling - maintains structure better
                        print(f"Applying voxel downsampling (voxel_size={voxel_size})...")
                        pcd_down = pcd.voxel_down_sample(voxel_size)
                        optimized_size = len(pcd_down.points)
                        print(f"Voxel downsampled to {optimized_size} points ({optimized_size/original_size*100:.1f}%)")
                        # Use Open3D's KDTree to find closest original points
                        down_points = np.asarray(pcd_down.points)
                        # Use Open3D KDTree to find closest original points
                        pcd_tree = o3d.geometry.KDTreeFlann(pcd)
                        indices = []
                        for i, point in enumerate(down_points):
                            [_, idx, _] = pcd_tree.search_knn_vector_3d(point, 1)
                            if len(idx) > 0:
                                indices.append(idx[0])
                            else:
                                indices.append(0)  # Fallback
                        return pcd_down, np.array(indices)
                    else:
                        # Random sampling - faster but less structured
                        print(f"Applying random sampling (ratio={sample_ratio})...")
                        sample_size = int(original_size * sample_ratio)
                        sample_indices = np.random.choice(original_size, sample_size, replace=False)
                        pcd_down = pcd.select_by_index(sample_indices)
                        optimized_size = len(pcd_down.points)
                        print(f"Random sampled to {optimized_size} points ({optimized_size/original_size*100:.1f}%)")
                        return pcd_down, sample_indices

                def dbscan_clustering(pcd, eps=0.1, min_points=10):
                    """DBSCAN clustering using Open3D (optimized)"""
                    points = np.asarray(pcd.points)
                    # Safety check for eps value to prevent memory issues
                    if eps > 1.0:
                        print(f"Warning: eps={eps} is very large, capping at 0.5 to prevent memory issues")
                        eps = 0.5
                    print(f"🔧 Using Open3D DBSCAN with eps={eps:.4f}, min_samples={min_points}")
                    clustering_start = time.time()
                    labels = np.array(pcd.cluster_dbscan(
                        eps=eps, 
                        min_points=min_points, 
                        print_progress=False
                    ))
                    clustering_time = time.time() - clustering_start
                    if filter_show_timing:
                        print(f"⏱️  Open3D DBSCAN clustering took {format_time(clustering_time)}")
                    # Analyze clusters
                    unique_labels = np.unique(labels)
                    cluster_counts = {}
                    for label in unique_labels:
                        if label != -1:  # Skip noise
                            count = np.sum(labels == label)
                            cluster_counts[label] = count
                    noise_count = np.sum(labels == -1)
                    print(f"Found {len(cluster_counts)} clusters, {noise_count} noise points")
                    # Print cluster info
                    if len(cluster_counts) > 0:
                        sorted_clusters = sorted(cluster_counts.items(), key=lambda x: x[1], reverse=True)
                        print("Top 5 largest clusters:")
                        for i, (label, count) in enumerate(sorted_clusters[:5]):
                            print(f"  Cluster {label}: {count} points")
                    return labels, cluster_counts

                def estimate_eps_automatically(pcd, k=4):
                    """Estimate eps parameter automatically using k-distance graph"""
                    print(f"Auto-estimating eps using {k}-distance graph...")
                    points = np.asarray(pcd.points)
                    n_points = len(points)
                    if n_points < k:
                        print(f"Warning: Not enough points ({n_points}) for k={k}, using k={n_points-1}")
                        k = max(1, n_points - 1)
                    # Sample points if too many for performance
                    if n_points > 10000:
                        sample_size = 10000
                        sample_indices = np.random.choice(n_points, sample_size, replace=False)
                        sample_points = points[sample_indices]
                        print(f"Sampling {sample_size} points for eps estimation")
                    else:
                        sample_points = points
                    # Build KDTree and find k-nearest neighbors
                    pcd_sample = o3d.geometry.PointCloud()
                    pcd_sample.points = o3d.utility.Vector3dVector(sample_points)
                    pcd_tree = o3d.geometry.KDTreeFlann(pcd_sample)
                    k_distances = []
                    for point in sample_points:
                        [_, idx, distances] = pcd_tree.search_knn_vector_3d(point, k + 1)  # +1 because first is the point itself
                        if len(distances) > k:
                            k_distances.append(np.sqrt(distances[k]))  # k-th distance (skip the first which is 0)
                        elif len(distances) > 1:
                            k_distances.append(np.sqrt(distances[-1]))  # Use the farthest available
                    k_distances = np.array(k_distances)
                    k_distances = np.sort(k_distances)
                    # Use elbow method to find optimal eps
                    # Look for the point where the slope changes most dramatically
                    if len(k_distances) > 10:
                        # Use percentile-based estimation
                        eps_estimate = np.percentile(k_distances, 90)  # 90th percentile often works well
                        print(f"Estimated eps: {eps_estimate:.6f}")
                        print(f"k-distance stats: min={k_distances.min():.6f}, "
                              f"median={np.median(k_distances):.6f}, "
                              f"90th percentile={np.percentile(k_distances, 90):.6f}, "
                              f"max={k_distances.max():.6f}")
                        return eps_estimate
                    else:
                        # Fallback for very small point clouds
                        eps_estimate = np.median(k_distances) if len(k_distances) > 0 else 0.1
                        print(f"Small point cloud, using median k-distance: {eps_estimate:.6f}")
                        return eps_estimate

                def create_mesh_from_indices(original_obj_name, indices, suffix=""):
                    """Create new mesh object from selected vertex indices"""
                    # Get original object and mesh
                    original_obj = bpy.data.objects[original_obj_name]
                    original_mesh = original_obj.data
                    # Create new mesh
                    new_mesh = bpy.data.meshes.new(f"{original_obj_name}{suffix}")
                    # Get vertices at specified indices
                    vertices = []
                    for idx in indices:
                        if 0 <= idx < len(original_mesh.vertices):
                            vert = original_mesh.vertices[idx]
                            vertices.append(vert.co[:])  # Convert to tuple
                    # Create mesh with just vertices (no faces for point cloud)
                    new_mesh.from_pydata(vertices, [], [])
                    new_mesh.update()
                    # Create new object
                    new_obj = bpy.data.objects.new(f"{original_obj_name}{suffix}", new_mesh)
                    # Copy transformation from original
                    new_obj.matrix_world = original_obj.matrix_world.copy()
                    # Add to scene
                    bpy.context.collection.objects.link(new_obj)
                    print(f"Created mesh '{new_obj.name}' with {len(vertices)} vertices")
                    return new_obj

                def point_cloud_filter(mode="quick", obj_name=None, eps=0.1, min_points=10, auto_eps=False):
                    """Main point cloud filtering function with comprehensive timing"""
                    # ===== TOTAL TIMING START =====
                    total_start_time = time.time()
                    print(f"\n🎯 POINT CLOUD FILTER - MODE: {mode.upper()}")
                    print(f"📊 Settings: eps={eps}, min_points={min_points}, auto_eps={auto_eps}")
                    print(f"⏱️  Timing enabled: {filter_show_timing}")
                    # Get target object
                    if obj_name:
                        if obj_name not in bpy.data.objects:
                            print(f"❌ Object '{obj_name}' not found")
                            return None
                        target_obj = bpy.data.objects[obj_name]
                    else:
                        target_obj = bpy.context.active_object
                        if not target_obj:
                            print("❌ No active object selected")
                            return None
                        obj_name = target_obj.name
                    if target_obj.type != 'MESH':
                        print(f"❌ Object '{obj_name}' is not a mesh")
                        return None
                    print(f"🎯 Processing object: {obj_name}")
                    print(f"   Vertices: {len(target_obj.data.vertices)}")
                    try:
                        # ===== STEP 1: CONVERT TO POINT CLOUD =====
                        print(f"\n📍 Step 1: Converting mesh to point cloud...")
                        step_start = time.time()
                        pcd, original_indices = mesh_to_point_cloud(obj_name)
                        step_time = time.time() - step_start
                        if filter_show_timing:
                            print(f"⏱️  Mesh conversion took {format_time(step_time)}")
                        # ===== STEP 2: SPEED OPTIMIZATION =====
                        print(f"\n⚡ Step 2: Speed optimization...")
                        step_start = time.time()
                        pcd_optimized, speed_indices = optimize_point_cloud_for_speed(
                            pcd, filter_max_points, filter_voxel_size, filter_sample_ratio, filter_use_voxel_downsample
                        )
                        step_time = time.time() - step_start
                        if filter_show_timing:
                            print(f"⏱️  Speed optimization took {format_time(step_time)}")
                        # ===== STEP 3: AUTO EPS ESTIMATION =====
                        if auto_eps:
                            print(f"\n🔍 Step 3: Auto-estimating eps...")
                            step_start = time.time()
                            eps = estimate_eps_automatically(pcd_optimized)
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Eps estimation took {format_time(step_time)}")
                        # ===== MAIN FILTERING MODES =====
                        if mode == "quick":
                            print(f"\n🚀 Mode: Quick DBSCAN clustering")
                            step_start = time.time()
                            labels, cluster_counts = dbscan_clustering(pcd_optimized, eps, min_points)
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  DBSCAN clustering took {format_time(step_time)}")
                            # Get largest cluster
                            if len(cluster_counts) > 0:
                                largest_cluster = max(cluster_counts.items(), key=lambda x: x[1])
                                cluster_label, cluster_size = largest_cluster
                                print(f"Selecting largest cluster: {cluster_label} ({cluster_size} points)")
                                # Get indices of points in largest cluster
                                cluster_mask = labels == cluster_label
                                cluster_indices = np.where(cluster_mask)[0]
                                # Map back to original if we did speed optimization
                                if len(speed_indices) != len(original_indices):
                                    final_indices = speed_indices[cluster_indices]
                                else:
                                    final_indices = cluster_indices
                                print(f"\n🔨 Creating result mesh...")
                                step_start = time.time()
                                result_obj = create_mesh_from_indices(obj_name, final_indices, "_quick_filtered")
                                step_time = time.time() - step_start
                                if filter_show_timing:
                                    print(f"⏱️  Mesh creation took {format_time(step_time)}")
                            else:
                                print("❌ No clusters found!")
                                return None
                        elif mode == "aggressive":
                            print(f"\n💪 Mode: Aggressive filtering (DBSCAN + Statistical + Radius)")
                            # Step 1: DBSCAN
                            print("Step 1: DBSCAN clustering...")
                            step_start = time.time()
                            labels, cluster_counts = dbscan_clustering(pcd_optimized, eps, min_points)
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  DBSCAN took {format_time(step_time)}")
                            if len(cluster_counts) == 0:
                                print("❌ No clusters found in DBSCAN!")
                                return None
                            # Get largest cluster
                            largest_cluster = max(cluster_counts.items(), key=lambda x: x[1])
                            cluster_label, cluster_size = largest_cluster
                            cluster_mask = labels == cluster_label
                            cluster_indices = np.where(cluster_mask)[0]
                            # Create point cloud from largest cluster
                            pcd_clustered = pcd_optimized.select_by_index(cluster_indices)
                            # Step 2: Statistical outlier removal
                            print("Step 2: Statistical outlier removal...")
                            step_start = time.time()
                            pcd_stat, stat_indices = filter_with_statistical_outlier_removal(
                                pcd_clustered, filter_nb_neighbors, filter_std_ratio
                            )
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Statistical filtering took {format_time(step_time)}")
                            # Step 3: Radius outlier removal
                            print("Step 3: Radius outlier removal...")
                            step_start = time.time()
                            pcd_final, radius_indices = filter_with_radius_outlier_removal(
                                pcd_stat, filter_radius_nb_points, filter_radius
                            )
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Radius filtering took {format_time(step_time)}")
                            # Map indices back to original
                            # radius_indices -> points in stat result
                            # stat_indices[radius_indices] -> points in clustered result  
                            # cluster_indices[...] -> points in original/speed optimized result
                            temp_indices = stat_indices[radius_indices]
                            final_cluster_indices = cluster_indices[temp_indices]
                            # Map back to original if we did speed optimization
                            if len(speed_indices) != len(original_indices):
                                final_indices = speed_indices[final_cluster_indices]
                            else:
                                final_indices = final_cluster_indices
                            print(f"\n🔨 Creating result mesh...")
                            step_start = time.time()
                            result_obj = create_mesh_from_indices(obj_name, final_indices, "_aggressive_filtered")
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Mesh creation took {format_time(step_time)}")
                        elif mode == "gentle":
                            print(f"\n🌸 Mode: Gentle filtering (Statistical outlier removal only)")
                            step_start = time.time()
                            pcd_filtered, indices = filter_with_statistical_outlier_removal(
                                pcd_optimized, filter_nb_neighbors, filter_std_ratio
                            )
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Statistical filtering took {format_time(step_time)}")
                            # Map back to original if needed
                            if len(speed_indices) != len(original_indices):
                                final_indices = speed_indices[indices]
                            else:
                                final_indices = indices
                            print(f"\n🔨 Creating result mesh...")
                            step_start = time.time()
                            result_obj = create_mesh_from_indices(obj_name, final_indices, "_gentle_filtered")
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Mesh creation took {format_time(step_time)}")
                        # Add other modes as needed...
                        else:
                            print(f"❌ Mode '{mode}' not implemented")
                            return None
                    except Exception as e:
                        print(f"❌ Filtering failed: {e}")
                        import traceback
                        traceback.print_exc()
                        return None
                    # ===== TOTAL TIMING END =====
                    total_end_time = time.time()
                    total_time = total_end_time - total_start_time
                    # Store result in global variable for Serpens
                    filter_result_object = result_obj
                    if result_obj:
                        print(f"\n✅ Filter completed! Created: {result_obj.name}")
                        print(f"📊 Final vertex count: {len(result_obj.data.vertices)}")
                        if filter_show_timing:
                            print(f"⏱️  🎯 TOTAL PROCESSING TIME: {format_time(total_time)}")
                    return result_obj
            # ===== SAFE WRAPPER FUNCTIONS =====

            def point_cloud_filter_safe(*args, **kwargs):
                """Safe wrapper for point cloud filtering"""
                if not check_open3d_available():
                    return None
                return point_cloud_filter(*args, **kwargs)

            def run_point_cloud_filter():
                """Run point cloud filter with current global settings"""
                if not check_open3d_available():
                    return None
                if not OPEN3D_AVAILABLE:
                    return None
                return point_cloud_filter(
                    mode=filter_mode,
                    obj_name=filter_obj_name if filter_obj_name else None,
                    eps=filter_eps,
                    min_points=filter_min_points,
                    auto_eps=filter_auto_eps
                )

            def execute_point_cloud_filter():
                """Auto-execute point cloud filtering using global variables"""
                global filter_result_object
                print(f"\n=== AUTO-EXECUTING POINT CLOUD FILTER ===")
                print(f"Mode: {filter_mode}")
                print(f"Open3D Available: {OPEN3D_AVAILABLE}")
                print(f"Show timing: {filter_show_timing}")
                if not check_open3d_available():
                    filter_result_object = None
                    return None
                # Get object name
                obj_name = filter_obj_name if filter_obj_name else None
                # Execute filtering
                try:
                    result = point_cloud_filter(
                        mode=filter_mode,
                        obj_name=obj_name,
                        eps=filter_eps,
                        min_points=filter_min_points,
                        auto_eps=filter_auto_eps
                    )
                    if result:
                        filter_result_object = result
                        print(f"✓ Filter completed! Created: {result.name}")
                        print(f"✓ Final check - filter_result_object = {filter_result_object}")
                    else:
                        print("✗ Filter completed but no objects created")
                        filter_result_object = None
                    return result
                except Exception as e:
                    print(f"✗ Filter failed: {e}")
                    import traceback
                    traceback.print_exc()
                    filter_result_object = None
                    return None
            # ===== DEBUG FUNCTIONS =====

            def debug_setup():
                """Debug function to check if everything is working"""
                print("=== DEBUGGING SETUP ===")
                if not check_open3d_available():
                    return False
                # Check active object
                if bpy.context.active_object:
                    obj = bpy.context.active_object
                    print(f"✓ Active object: {obj.name}")
                    print(f"  Object type: {obj.type}")
                    if obj.type == 'MESH':
                        print(f"  Vertex count: {len(obj.data.vertices)}")
                    else:
                        print("✗ Active object is not a mesh!")
                        return False
                else:
                    print("✗ No active object selected!")
                    return False
                print(f"✓ Global variables:")
                print(f"  filter_mode: {filter_mode}")
                print(f"  filter_auto_eps: {filter_auto_eps}")
                print(f"  filter_eps: {filter_eps}")
                print(f"  filter_min_points: {filter_min_points}")
                print(f"  filter_show_timing: {filter_show_timing}")
                return True

            def test_quick_filter():
                """Test function - runs quick filter on active object"""
                print("\n=== TESTING QUICK FILTER ===")
                if not debug_setup():
                    print("Setup check failed - cannot run filter")
                    return None
                try:
                    print("Running quick filter...")
                    result = run_point_cloud_filter()
                    if result:
                        print(f"✓ Filter completed successfully!")
                        print(f"  Created object: {result.name}")
                    else:
                        print("✗ Filter returned None - check console for errors")
                    return result
                except Exception as e:
                    print(f"✗ Filter failed with error: {e}")
                    import traceback
                    traceback.print_exc()
                    return None
            # ===== AUTO-EXECUTE ONLY IF OPEN3D IS AVAILABLE =====
            if OPEN3D_AVAILABLE:
                if __name__ == "__main__" or True:
                    result = execute_point_cloud_filter()
                    if result:
                        filter_result_object = result
                        print(f"\n=== FINAL RESULT ===")
                        print(f"filter_result_object = {filter_result_object}")
                        print(f"Object name: {filter_result_object.name}")
                        print(f"Vertex count: {len(filter_result_object.data.vertices)}")
                    else:
                        filter_result_object = None
                        print(f"\n=== FINAL RESULT ===")
                        print("filter_result_object = None")
            else:
                # Don't execute anything if Open3D is not available
                print("\n❌ SCRIPT NOT EXECUTED - OPEN3D REQUIRED")
                print("💡 TO ENABLE DB FILTERING:")
                print("1. Install Open3D wheels in your addon")
                print("2. Update blender_manifest.toml with wheel paths")
                print("3. Restart Blender")
                print("4. Run this script again")
                # Set result to None
                filter_result_object = None
            # ===== USAGE NOTES =====
            if OPEN3D_AVAILABLE:
                print(f"""
            === POINT CLOUD FILTER - LIGHTWEIGHT OPEN3D VERSION ===
            ✅ STATUS: Fully functional
            🎯 FEATURES: All DB filtering operations available
            🚀 Optimized: Open3D only - no sklearn dependencies
            SERPENS SETUP:
            - filter_mode: "quick", "aggressive", "gentle", etc.
            - filter_obj_name: Object name (empty for active)
            - filter_eps: DBSCAN radius
            - filter_min_points: Minimum cluster size
            - filter_auto_eps: Auto-estimate eps
            - filter_show_timing: Show timing information (True/False)
            Main Function: run_point_cloud_filter()
            Debug Function: test_quick_filter()
                """)
            else:
                print("""
            === POINT CLOUD FILTER - OPEN3D DISABLED ===
            ❌ STATUS: Not functional
            ⚠️  REASON: Open3D not installed
            SOLUTION:
            1. Add Open3D wheels to your addon
            2. Update blender_manifest.toml 
            3. Restart Blender
            CURRENT FUNCTIONS: All disabled safely
                """)
            if (filter_result_object == None):
                pass
            else:
                input_object = filter_result_object
                # Input Variables
                #input_object = None  # bpy.types.Object - The object to select and make active
                deselect_all_first = True  # bool - Whether to deselect all objects first
                # Output Variables  
                success = False  # bool - Whether the operation was successful
                error_message = ""  # str - Error message if operation failed

                def safe_deselect_all():
                    """
                    Safely deselect all objects, only touching objects that are in the current view layer
                    """
                    try:
                        # Get current view layer
                        view_layer = bpy.context.view_layer
                        # Only deselect objects that are actually in the current view layer
                        for obj in bpy.context.selected_objects[:]:  # Create a copy of the list to avoid modification during iteration
                            # Check if object is in current view layer
                            if obj.name in view_layer.objects:
                                obj.select_set(False)
                        # Clear active object safely
                        if view_layer.objects.active and view_layer.objects.active.name in view_layer.objects:
                            view_layer.objects.active = None
                        return True, ""
                    except Exception as e:
                        return False, f"Error during deselect all: {str(e)}"

                def select_and_activate_object(obj):
                    """
                    Select and activate the given object, making it visible first if needed
                    """
                    if not obj:
                        return False, "No object provided"
                    try:
                        view_layer = bpy.context.view_layer
                        # Check if object exists in current view layer
                        if obj.name not in view_layer.objects:
                            return False, f"Object '{obj.name}' is not in the current view layer or is excluded"
                        # Get the object from the view layer (this ensures we have the right reference)
                        view_layer_obj = view_layer.objects[obj.name]
                        # Make object visible if it's hidden
                        visibility_changes = []
                        # Unhide in viewport
                        if obj.hide_viewport:
                            obj.hide_viewport = False
                            visibility_changes.append("viewport")
                        # Unhide in view layer
                        if view_layer_obj.hide_get():
                            view_layer_obj.hide_set(False)
                            visibility_changes.append("view layer")
                        # Try to unhide parent collections if they're hidden
                        for collection in obj.users_collection:
                            if collection.hide_viewport:
                                collection.hide_viewport = False
                                visibility_changes.append(f"collection '{collection.name}'")
                        # Select the object
                        view_layer_obj.select_set(True)
                        # Make it active
                        view_layer.objects.active = view_layer_obj
                        success_msg = f"Successfully selected and activated '{obj.name}'"
                        if visibility_changes:
                            success_msg += f" (made visible in: {', '.join(visibility_changes)})"
                        return True, success_msg
                    except Exception as e:
                        return False, f"Error selecting object '{obj.name}': {str(e)}"
                # Main execution
                if input_object:
                    # Deselect all first if requested
                    if deselect_all_first:
                        deselect_success, deselect_error = safe_deselect_all()
                        if not deselect_success:
                            success = False
                            error_message = deselect_error
                            print(error_message)
                        else:
                            print("All objects deselected safely")
                    # Select and activate the input object (only if deselect was successful or not requested)
                    if not deselect_all_first or deselect_success:
                        success, error_message = select_and_activate_object(input_object)
                        print(error_message)
                else:
                    success = False
                    error_message = "No input object provided"
                    print(error_message)
                bpy.context.view_layer.objects.active.name = 'AutoCrop_' + bpy.context.view_layer.objects.active.name
                bpy.context.view_layer.objects.active.hide_render = True
                if self.sna_create_convex_hull_object:
                    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
                    bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
                    bpy.ops.mesh.convex_hull('INVOKE_DEFAULT', )
                    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        else:
            self.report({'ERROR'}, message='Open3D not available')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        col_AFE45 = layout.column(heading='', align=False)
        col_AFE45.alert = False
        col_AFE45.enabled = True
        col_AFE45.active = True
        col_AFE45.use_property_split = False
        col_AFE45.use_property_decorate = False
        col_AFE45.scale_x = 1.0
        col_AFE45.scale_y = 1.0
        col_AFE45.alignment = 'Expand'.upper()
        col_AFE45.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_E9B63 = col_AFE45.box()
        box_E9B63.alert = False
        box_E9B63.enabled = True
        box_E9B63.active = True
        box_E9B63.use_property_split = False
        box_E9B63.use_property_decorate = False
        box_E9B63.alignment = 'Expand'.upper()
        box_E9B63.scale_x = 1.0
        box_E9B63.scale_y = 1.0
        if not True: box_E9B63.operator_context = "EXEC_DEFAULT"
        box_E9B63.label(text="There is no 'one size fits all' setting.", icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_E9B63.label(text='You may need to play with different values.', icon_value=0)
        box_AC64A = col_AFE45.box()
        box_AC64A.alert = False
        box_AC64A.enabled = True
        box_AC64A.active = True
        box_AC64A.use_property_split = False
        box_AC64A.use_property_decorate = False
        box_AC64A.alignment = 'Expand'.upper()
        box_AC64A.scale_x = 1.0
        box_AC64A.scale_y = 1.0
        if not True: box_AC64A.operator_context = "EXEC_DEFAULT"
        row_A0C33 = box_AC64A.row(heading='', align=False)
        row_A0C33.alert = False
        row_A0C33.enabled = True
        row_A0C33.active = True
        row_A0C33.use_property_split = False
        row_A0C33.use_property_decorate = False
        row_A0C33.scale_x = 1.0
        row_A0C33.scale_y = 1.0
        row_A0C33.alignment = 'Expand'.upper()
        row_A0C33.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A0C33.label(text='Mode', icon_value=0)
        row_A0C33.prop(self, 'sna_filter_mode', text=self.sna_filter_mode, icon_value=0, emboss=True, expand=True)
        box_AC64A.prop(self, 'sna_filter_epsilon', text='Filter Epsilon', icon_value=0, emboss=True, slider=True)
        box_AC64A.prop(self, 'sna_filter_min_points', text='Filter Min Points', icon_value=0, emboss=True)
        box_AC64A.prop(self, 'sna_fast_mode', text='Filter Fast Mode (Less Accurate)', icon_value=0, emboss=True)
        box_AC64A.prop(self, 'sna_create_convex_hull_object', text='Create Convex Hull Object', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


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
    row_8F631.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_faces_or_verts', text=bpy.context.scene.sna_dgs_scene_properties.import_faces_or_verts, icon_value=0, emboss=True, expand=True, toggle=True)
    if (bpy.context.scene.sna_dgs_scene_properties.import_faces_or_verts == 'Faces'):
        box_910F6.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_uv_reset', text='UV Reset', icon_value=0, emboss=True, toggle=False)
    box_910F6.prop(bpy.context.scene.sna_dgs_scene_properties, 'import_create_proxy_object', text='Create Proxy Object', icon_value=0, emboss=True, expand=True, toggle=False)
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
        if (bpy.context.scene.render.engine == 'CYCLES'):
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


class SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De(bpy.types.Operator):
    bl_idname = "sna.dgs_render_rotate_for_blender_axes_423de"
    bl_label = "3DGS Render: Rotate for Blender Axes"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.rotation_euler = (math.radians(-90.0), math.radians(0.0), math.radians(-90.0))
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_align_active_values_to_x_4CE1F():
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


def sna_align_active_values_to_y_E5E9E():
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


def sna_align_active_values_to_z_7B9ED():
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


class SNA_OT_Dgs_Render_Import_Ply_E0A3A(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.dgs_render_import_ply_e0a3a"
    bl_label = "3DGS Render: Import PLY"
    bl_description = "Imports a .PLY file and adds 3DGS modifiers and attributes."
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
        if (bpy.context.scene.sna_dgs_scene_properties.import_faces_or_verts == 'Faces'):
            bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] = 'face'
            sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Store_Origpos_GN', 'KIRI_3DGS_Store_Origpos_GN', bpy.context.view_layer.objects.active)
            bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Store_Origpos_GN')
            sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Render_GN', 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active)
            sna_align_active_values_to_x_4CE1F()
            bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Render_GN')
        else:
            bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] = 'vert'
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
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Render_GN', 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Sorter_GN', 'KIRI_3DGS_Sorter_GN', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Adjust_Colour_And_Material', 'KIRI_3DGS_Adjust_Colour_And_Material', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Write F_DC_And_Merge', 'KIRI_3DGS_Write F_DC_And_Merge', bpy.context.view_layer.objects.active)
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'].show_viewport = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'].show_render = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = False
        bpy.context.scene.sna_dgs_scene_properties.active_object_update_mode = 'Disable Camera Updates'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_on_cage = (bpy.context.scene.sna_dgs_scene_properties.import_faces_or_verts == 'Faces')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_in_editmode = (bpy.context.scene.sna_dgs_scene_properties.import_faces_or_verts == 'Faces')
        bpy.context.view_layer.objects.active.sna_dgs_object_properties.enable_active_camera_updates = False
        bpy.context.view_layer.objects.active.sna_dgs_object_properties.active_object_update_mode = 'Disable Camera Updates'
        if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.materials)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V4.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
            appended_C1470 = None if not new_data else new_data[0]
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_viewport = (bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method == 'BLENDED')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_render = (bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method == 'BLENDED')
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
        bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        if (bpy.context.scene.sna_dgs_scene_properties.import_uv_reset and (bpy.context.scene.sna_dgs_scene_properties.import_faces_or_verts == 'Faces')):
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
            bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
            bpy.ops.mesh.dissolve_limited('INVOKE_DEFAULT', )
            bpy.ops.uv.reset('INVOKE_DEFAULT', )
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        if bpy.context.scene.sna_dgs_scene_properties.import_create_proxy_object:
            sna_b2_load_from_blender_object_F0CCB(bpy.context.view_layer.objects.active.name + 'Splat_Proxy')
        return {"FINISHED"}


def sna_append_and_add_geo_nodes_function_execute_6BCD7(Node_Group_Name, Modifier_Name, Object):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V4.blend') + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_65345 = None if not new_data else new_data[0]
    modifier_6D624 = Object.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_6D624.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_6D624


class SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_6D2B1(bpy.types.Panel):
    bl_label = '3DGS Render by KIRI Engine'
    bl_idname = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_6D2B1'
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
        layout.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine icon.svg')), scale=1.0)

    def draw(self, context):
        layout = self.layout
        layout_function = layout
        sna_dgs_render__main_function_menu_019C7(layout_function, )
        layout_function = layout
        sna_about_kiri_links_docs_3dgs_D02EC(layout_function, )


def sna_clean_up_scene_5F1F1(REMOVE_ALL_GAUSSIAN_OBJECTS):
    REMOVE_ALL_GAUSSIAN_OBJECTS = REMOVE_ALL_GAUSSIAN_OBJECTS
    # ========== VARIABLES (EDIT THESE) ==========
    #REMOVE_ALL_GAUSSIAN_OBJECTS = False  # Remove all gaussian objects from scene
    REMOVE_HANDLERS = True               # Remove draw handlers
    REMOVE_GPU_RESOURCES = True          # Clean up GPU textures/shaders
    CLEAR_OBJECT_CACHE = True            # Clear the global object cache
    # ============================================
    #import bpy

    def remove_all_gaussian_objects():
        """Remove all gaussian splat objects from the scene"""
        try:
            objects_to_remove = []
            # Find all objects with gaussian properties
            for obj in bpy.data.objects:
                if obj.get("is_gaussian_splat", False):
                    objects_to_remove.append(obj)
            # Remove them
            for obj in objects_to_remove:
                print(f"Removing gaussian object: {obj.name}")
                bpy.data.objects.remove(obj, do_unlink=True)
            print(f"Removed {len(objects_to_remove)} gaussian objects")
        except Exception as e:
            print(f"Error removing gaussian objects: {e}")

    def cleanup_draw_handlers():
        """Remove gaussian draw handlers"""
        try:
            if hasattr(bpy, 'gaussian_draw_handle'):
                bpy.types.SpaceView3D.draw_handler_remove(bpy.gaussian_draw_handle, 'WINDOW')
                delattr(bpy, 'gaussian_draw_handle')
                print("Draw handler removed")
        except Exception as e:
            print(f"Error removing draw handler: {e}")

    def cleanup_gpu_resources():
        """Clean up all GPU textures and shaders"""
        try:
            gpu_resources = [
                # Shaders and batches
                'gaussian_quad_shader', 'gaussian_quad_batch', 
                'gaussian_composite_shader', 'gaussian_composite_batch',
                # Textures
                'gaussian_texture', 'gaussian_indices_texture',
                'gaussian_metadata_texture', 'gaussian_depth_texture',
                # Texture dimensions
                'gaussian_texture_width', 'gaussian_texture_height', 'gaussian_texture_depth',
                'gaussian_indices_width', 'gaussian_indices_height',
                # Counts
                'gaussian_count'
            ]
            removed_count = 0
            for attr in gpu_resources:
                if hasattr(bpy, attr):
                    delattr(bpy, attr)
                    removed_count += 1
            print(f"Cleaned up {removed_count} GPU resources")
        except Exception as e:
            print(f"Error cleaning GPU resources: {e}")

    def cleanup_framebuffers():
        """Clean up persistent framebuffers"""
        try:
            # Clean up persistent framebuffer
            if hasattr(bpy, 'gaussian_persistent_fb'):
                try:
                    color_tex, depth_tex, fb = bpy.gaussian_persistent_fb
                    del fb, depth_tex, color_tex
                    delattr(bpy, 'gaussian_persistent_fb')
                    print("Persistent framebuffer cleaned up")
                except:
                    delattr(bpy, 'gaussian_persistent_fb')
            # Clean up framebuffer size tracking
            fb_attrs = ['gaussian_fb_width', 'gaussian_fb_height']
            for attr in fb_attrs:
                if hasattr(bpy, attr):
                    delattr(bpy, attr)
        except Exception as e:
            print(f"Error cleaning framebuffers: {e}")

    def cleanup_multi_object_cache():
        """Clean up multi-object specific data structures"""
        try:
            multi_object_attrs = [
                # Object cache and metadata
                'gaussian_object_cache',           # Main object cache
                'gaussian_object_metadata',        # Object metadata for rendering
                # Transform tracking
                'gaussian_last_transforms',        # Per-object transform tracking
                'gaussian_last_transform',         # Single object transform (legacy)
                # Camera tracking  
                'gaussian_last_camera_pos',        # Camera position for depth sorting
                # Update flags
                'gaussian_global_needs_update',    # Global data update flag
            ]
            removed_count = 0
            for attr in multi_object_attrs:
                if hasattr(bpy, attr):
                    delattr(bpy, attr)
                    removed_count += 1
            print(f"Cleaned up {removed_count} multi-object cache attributes")
        except Exception as e:
            print(f"Error cleaning multi-object cache: {e}")

    def force_viewport_update():
        """Force viewport redraw to show cleanup results"""
        try:
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
            print("Viewport updated")
        except Exception as e:
            print(f"Error updating viewport: {e}")
    # ========== MAIN CLEANUP EXECUTION ==========
    print("Starting multi-object gaussian cleanup...")
    # Remove draw handlers first
    if REMOVE_HANDLERS:
        cleanup_draw_handlers()
    # Clean up framebuffers
    cleanup_framebuffers()
    # Remove GPU resources
    if REMOVE_GPU_RESOURCES:
        cleanup_gpu_resources()
    # Clear multi-object cache and tracking data
    if CLEAR_OBJECT_CACHE:
        cleanup_multi_object_cache()
    # Remove all gaussian objects from scene
    if REMOVE_ALL_GAUSSIAN_OBJECTS:
        remove_all_gaussian_objects()
    # Force viewport update
    force_viewport_update()
    print("Multi-object cleanup complete!")
    # Print summary of what was cleaned
    if hasattr(bpy, 'gaussian_object_cache'):
        remaining_objects = len(bpy.gaussian_object_cache)
        print(f"Warning: {remaining_objects} objects still in cache")
    else:
        print("All caches cleared successfully")


def sna_render_temp_scene_913CD(TEMP_RENDER_PATH, RENDER_ANIMATION, FRAME_STEP):
    TEMP_RENDER_PATH = TEMP_RENDER_PATH
    RENDER_ANIMATION = RENDER_ANIMATION
    FRAME_STEP = FRAME_STEP
    # ========== VARIABLES (EDIT THESE) ==========
    #TEMP_RENDER_PATH = r"C:\temp\gaussian_render"  # Shared path for both scripts
    RENDER_WIDTH = 0          # 0 = use scene settings
    RENDER_HEIGHT = 0         # 0 = use scene settings
    #RENDER_ANIMATION = False     # True = render animation frames
    START_FRAME = 0              # 0 = use scene frame_start
    END_FRAME = 0                # 0 = use scene frame_end
    #FRAME_STEP = 1               # Render every Nth frame
    CLEANUP_EXISTING_FILES = True # Remove old temp files before rendering
    SAVE_COLOR = True            # Save color pass
    SAVE_DEPTH = True            # Save Z-pass (needed for gaussian integration)
    # ============================================
    #import bpy
    #import time

    def resolve_blender_path(blender_path):
        """Convert Blender relative path to absolute path"""
        import os
        if os.name == 'posix':
            return blender_path
        # Check if it's a VALID absolute path (has drive letter on Windows)
        if os.path.isabs(blender_path) and (len(blender_path) < 2 or blender_path[1] == ':'):
            return blender_path
        # Handle Windows-style relative paths like \tmp\ or /tmp/ directly
        if blender_path.startswith('\\') or blender_path.startswith('/'):
            # Remove leading slash/backslash and join with C: drive
            clean_path = blender_path.lstrip('\\/').rstrip('\\/')
            resolved = f"C:\\{clean_path}"
            return resolved
        # Try Blender's path resolution
        try:
            resolved = bpy.path.abspath(blender_path)
            if os.path.isabs(resolved) and resolved != blender_path:
                return resolved
        except Exception as e:
            pass
        # Fallback to os.path.abspath for other cases
        resolved = os.path.abspath(blender_path)
        return resolved

    def setup_render_for_regular_scene():
        """Configure scene for regular mesh rendering"""
        try:
            scene = bpy.context.scene
            # Enable Z-pass
            scene.view_layers["ViewLayer"].use_pass_z = True
            # Store original render settings
            original_format = scene.render.image_settings.file_format
            original_color_mode = scene.render.image_settings.color_mode
            original_color_depth = scene.render.image_settings.color_depth
            # Set render format for EXR output
            scene.render.image_settings.file_format = 'OPEN_EXR'
            scene.render.image_settings.color_mode = 'RGBA'
            scene.render.image_settings.color_depth = '32'
            # Set resolution if specified
            if RENDER_WIDTH > 0 and RENDER_HEIGHT > 0:
                original_width = scene.render.resolution_x
                original_height = scene.render.resolution_y
                scene.render.resolution_x = RENDER_WIDTH
                scene.render.resolution_y = RENDER_HEIGHT
            else:
                original_width = None
                original_height = None
            return {
                'format': original_format,
                'color_mode': original_color_mode,
                'color_depth': original_color_depth,
                'width': original_width,
                'height': original_height
            }
        except Exception as e:
            print(f"Error setting up render: {e}")
            return None

    def restore_render_settings(original_settings):
        """Restore original render settings"""
        try:
            if not original_settings:
                return
            scene = bpy.context.scene
            scene.render.image_settings.file_format = original_settings['format']
            scene.render.image_settings.color_mode = original_settings['color_mode']
            scene.render.image_settings.color_depth = original_settings['color_depth']
            if original_settings['width'] and original_settings['height']:
                scene.render.resolution_x = original_settings['width']
                scene.render.resolution_y = original_settings['height']
        except Exception as e:
            print(f"Error restoring render settings: {e}")

    def hide_gaussian_objects():
        """Hide all gaussian objects for regular scene render"""
        try:
            hidden_objects = []
            for obj in bpy.data.objects:
                if obj.get("is_gaussian_splat", False):
                    if obj.visible_get():
                        obj.hide_render = True
                        hidden_objects.append(obj.name)
            return hidden_objects
        except Exception as e:
            print(f"Error hiding gaussian objects: {e}")
            return []

    def show_gaussian_objects(hidden_objects):
        """Restore visibility of gaussian objects"""
        try:
            for obj_name in hidden_objects:
                if obj_name in bpy.data.objects:
                    obj = bpy.data.objects[obj_name]
                    obj.hide_render = False
        except Exception as e:
            print(f"Error showing gaussian objects: {e}")

    def cleanup_temp_directory():
        """Remove existing temp files"""
        try:
            if not CLEANUP_EXISTING_FILES:
                return
            # Resolve Blender path to absolute path for Python file operations
            resolved_path = resolve_blender_path(TEMP_RENDER_PATH)
            if not os.path.exists(resolved_path):
                return
            for file in os.listdir(resolved_path):
                if file.startswith("regular_") and file.endswith(".exr"):
                    file_path = os.path.join(resolved_path, file)
                    try:
                        os.remove(file_path)
                        print(f"Removed: {file}")
                    except:
                        pass
        except Exception as e:
            print(f"Error cleaning temp directory: {e}")

    def get_output_paths(frame_num):
        """Get output file paths for frame (using Blender's automatic frame numbering)"""
        try:
            # Resolve Blender path to absolute path for Python file operations
            resolved_path = resolve_blender_path(TEMP_RENDER_PATH)
            os.makedirs(resolved_path, exist_ok=True)
            # Blender automatically adds frame numbers like _0001, _0002, etc.
            color_path = os.path.join(resolved_path, f"regular_color_{frame_num:04d}.exr")
            depth_path = os.path.join(resolved_path, f"regular_depth_{frame_num:04d}.exr")
            return color_path, depth_path
        except Exception as e:
            print(f"Error generating output paths: {e}")
            return None, None

    def extract_and_save_passes(frame_num):
        """Extract color and depth passes from render result and save"""
        try:
            # Get render result
            render_result = bpy.data.images.get('Render Result')
            if not render_result:
                print("No render result found")
                return False
            color_path, depth_path = get_output_paths(frame_num)
            if not color_path or not depth_path:
                return False
            success_count = 0
            # Save color pass
            if SAVE_COLOR:
                try:
                    # Create a copy for color
                    color_image = render_result.copy()
                    color_image.name = f"regular_color_{frame_num}"
                    color_image.file_format = 'OPEN_EXR'
                    color_image.filepath_raw = color_path
                    color_image.save()
                    bpy.data.images.remove(color_image)
                    print(f"Saved color: {os.path.basename(color_path)}")
                    success_count += 1
                except Exception as e:
                    print(f"Failed to save color: {e}")
            # Save depth pass
            if SAVE_DEPTH:
                try:
                    # Access Z-pass from viewer node
                    # We need to temporarily set up compositor to extract Z
                    scene = bpy.context.scene
                    # Enable compositor
                    scene.use_nodes = True
                    # Clear and set up minimal compositor for Z extraction
                    scene.node_tree.nodes.clear()
                    # Render layers node
                    render_layers = scene.node_tree.nodes.new('CompositorNodeRLayers')
                    render_layers.location = (0, 0)
                    # File output for depth
                    file_output = scene.node_tree.nodes.new('CompositorNodeOutputFile')
                    file_output.location = (200, 0)
                    file_output.format.file_format = 'OPEN_EXR'
                    file_output.format.color_mode = 'BW'  # Grayscale for depth
                    file_output.format.color_depth = '32'
                    file_output.base_path = TEMP_RENDER_PATH  # Use original Blender path here
                    file_output.file_slots[0].path = "regular_depth_"  # Blender will add frame numbers automatically
                    # Connect Z output to file output
                    scene.node_tree.links.new(render_layers.outputs['Depth'], file_output.inputs['Image'])
                    # Re-render to generate depth file
                    bpy.ops.render.render()
                    if os.path.exists(depth_path):
                        print(f"Saved depth: {os.path.basename(depth_path)}")
                        success_count += 1
                    else:
                        print("Depth file was not created")
                except Exception as e:
                    print(f"Failed to save depth: {e}")
            return success_count > 0
        except Exception as e:
            print(f"Error extracting passes: {e}")
            return False

    def render_regular_frame(frame_num):
        """Render single frame of regular scene"""
        try:
            scene = bpy.context.scene
            camera = scene.camera
            if not camera:
                print(f"ERROR: No camera found (Frame {frame_num})")
                return False
            # Set frame
            scene.frame_set(frame_num)
            bpy.context.evaluated_depsgraph_get().update()
            print(f"Rendering regular scene (Frame {frame_num})...")
            # Hide gaussian objects
            hidden_gaussians = hide_gaussian_objects()
            try:
                # Render scene
                bpy.ops.render.render()
                # Extract and save passes
                success = extract_and_save_passes(frame_num)
                if success:
                    print(f"Frame {frame_num}: Regular render completed")
                    return True
                else:
                    print(f"Frame {frame_num}: Failed to save render passes")
                    return False
            finally:
                # Restore gaussian objects
                show_gaussian_objects(hidden_gaussians)
        except Exception as e:
            print(f"Frame {frame_num}: Regular render failed - {e}")
            return False

    def render_regular_animation():
        """Render animation frames of regular scene"""
        try:
            scene = bpy.context.scene
            user_frame = scene.frame_current
            # Determine frame range
            start_frame = START_FRAME if START_FRAME > 0 else scene.frame_start
            end_frame = END_FRAME if END_FRAME > 0 else scene.frame_end
            frames = list(range(start_frame, end_frame + 1, FRAME_STEP))
            num_frames = len(frames)
            print(f"Rendering regular scene animation: {num_frames} frames")
            start_time = time.time()
            successful_frames = 0
            failed_frames = 0
            for i, frame_num in enumerate(frames):
                frame_start = time.time()
                success = render_regular_frame(frame_num)
                if success:
                    successful_frames += 1
                else:
                    failed_frames += 1
                frame_time = time.time() - frame_start
                remaining_frames = num_frames - i - 1
                avg_time = (time.time() - start_time) / (i + 1)
                eta = avg_time * remaining_frames
                print(f"Frame {frame_num} ({i+1}/{num_frames}): {frame_time:.1f}s | ETA: {datetime.timedelta(seconds=int(eta))}")
            # Restore original frame
            scene.frame_set(user_frame)
            total_time = time.time() - start_time
            print(f"Regular scene animation completed in {datetime.timedelta(seconds=int(total_time))}")
            print(f"Successful: {successful_frames}, Failed: {failed_frames}")
            return successful_frames > 0
        except Exception as e:
            print(f"Animation render failed: {e}")
            return False

    def main_regular_render():
        """Main function for regular scene rendering"""
        try:
            scene = bpy.context.scene
            if not scene.camera:
                print("ERROR: No camera found in scene")
                return False
            print(f"Regular scene render starting...")
            print(f"Output directory: {TEMP_RENDER_PATH}")
            # Setup render settings
            original_settings = setup_render_for_regular_scene()
            if not original_settings:
                return False
            # Clean up existing files
            cleanup_temp_directory()
            try:
                # Render based on mode
                if RENDER_ANIMATION:
                    success = render_regular_animation()
                else:
                    success = render_regular_frame(scene.frame_current)
                return success
            finally:
                # Always restore settings
                restore_render_settings(original_settings)
        except Exception as e:
            print(f"Main regular render failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    # ========== MAIN EXECUTION ==========
    print("Starting regular scene render for gaussian integration...")
    render_success = main_regular_render()
    if render_success:
        print("Regular scene render completed successfully!")
        print("Ready for Script 7b - Gaussian render with depth integration")
    else:
        print("Regular scene render failed!")


def sna_render_comp_0DAEE(RENDER_ANIMATION, RENDER_COLOR, RENDER_DEPTH, COMP_WITH_TEMP, TEMP_RENDER_PATH, UPDATE_SOURCE_TRANSFORMS, REFRESH_EVALUATED_DATA, FRAME_STEP):
    RENDER_ANIMATION = RENDER_ANIMATION
    RENDER_GAUSSIAN = RENDER_COLOR
    RENDER_DEPTH = RENDER_DEPTH
    USE_TEMP_RENDERS = COMP_WITH_TEMP
    TEMP_RENDER_PATH = TEMP_RENDER_PATH
    UPDATE_SOURCE_TRANSFORMS = UPDATE_SOURCE_TRANSFORMS
    REFRESH_EVALUATED_DATA = REFRESH_EVALUATED_DATA
    FRAME_STEP = FRAME_STEP
    # ========== VARIABLES (EDIT THESE) ==========
    #RENDER_ANIMATION = False     # True = Animation, False = Single Frame
    RENDER_WIDTH = 0           # Render resolution width (0 = use scene settings)
    RENDER_HEIGHT = 0          # Render resolution height (0 = use scene settings)
    # Multi-pass rendering (enable any combination)
    #RENDER_GAUSSIAN = True        # Render gaussian/color pass
    #RENDER_DEPTH = False   # Render depth visualization pass
    RENDER_SURFEL = False         # Render surfel visualization pass
    SH_DEGREE = 3                 # 0, 1, 2, or 3 (only affects gaussian pass)
    SAVE_TO_FILE = True           # Save render to file
    SAVE_AS_RENDER = True         # Apply Blender's color management when saving
    FORCE_DEPTH_SORT = True       # Force depth sorting for render camera (recommended)
    # COMPOSITING SETTINGS (CORRECTED)
    #USE_TEMP_RENDERS = True       # Use temp renders from script_7 for compositing
    #TEMP_RENDER_PATH = r"C:\temp\gaussian_render"  # Path to temp renders from script_7
    USE_EXTERNAL_DEPTH = True     # Use depth from script_7 for occlusion
    USE_EXTERNAL_COLOR = True     # Use color from script_7 for compositing
    COMPOSITE_OVER_REGULAR = True # Composite gaussians over regular scene
    # Animation-specific settings
    START_FRAME = 0               # Animation start frame (0 = use scene frame_start)
    END_FRAME = 0                 # Animation end frame (0 = use scene frame_end)
    #FRAME_STEP = 1                # Render every Nth frame (1 = every frame)
    SKIP_EXISTING_FILES = False   # Skip frames if output file already exists
    CONTINUE_ON_ERROR = True      # Continue animation if individual frames fail
    # Source object update settings
    #UPDATE_SOURCE_TRANSFORMS = True   # Copy source object transforms to empty objects each frame
    #REFRESH_EVALUATED_DATA = True # Re-extract gaussian data from evaluated source mesh each frame (EXPENSIVE!)
    # DEBUG SETTINGS
    DEBUG_VERBOSE = False          # Enable detailed debug output
    DEBUG_DATA_CHANGES = False     # Log actual data changes between frames
    DEBUG_TIMING = False          # Log operation timing
    # ============================================
    #import bpy
    import gpu.state
    import numpy as np
    import math
    #import time
    import os

    def debug_print(message, force=False):
        """Print debug message if debugging is enabled"""
        if DEBUG_VERBOSE or force:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[DEBUG {timestamp}] {message}")

    def auto_reconstruct_cache():
        """Auto-detect and rebuild cache from existing scene objects"""
        try:
            # Find all gaussian objects in the scene
            gaussian_objects = []
            for obj in bpy.data.objects:
                if obj.get("is_gaussian_splat", False):
                    gaussian_objects.append(obj)
            if not gaussian_objects:
                return False
            debug_print(f"Auto-reconstructing cache from {len(gaussian_objects)} scene objects...")
            # Initialize fresh cache
            bpy.gaussian_object_cache = {}
            total_gaussians = 0
            for obj in gaussian_objects:
                try:
                    # Extract data from object properties
                    data_bytes = obj.get("gaussian_data")
                    gaussian_count = obj.get("gaussian_count", 0)
                    sh_degree = obj.get("sh_degree", 48)
                    ply_filepath = obj.get("ply_filepath", "Unknown")
                    if not data_bytes or gaussian_count == 0:
                        continue
                    # Reconstruct numpy array from bytes
                    gaussian_data = np.frombuffer(data_bytes, dtype=np.float32).reshape(gaussian_count, 59)
                    # Add to cache
                    bpy.gaussian_object_cache[obj.name] = {
                        'gaussian_data': gaussian_data,
                        'gaussian_count': gaussian_count,
                        'sh_degree': sh_degree,
                        'object': obj,
                        'ply_filepath': ply_filepath
                    }
                    total_gaussians += gaussian_count
                except Exception as e:
                    debug_print(f"Failed to reconstruct {obj.name}: {e}")
                    continue
            if bpy.gaussian_object_cache:
                debug_print(f"Cache auto-reconstructed: {len(bpy.gaussian_object_cache)} objects, {total_gaussians:,} gaussians")
                return True
            else:
                return False
        except Exception as e:
            debug_print(f"Auto-reconstruction failed: {e}")
            return False

    def auto_reconstruct_shaders():
        """Auto-reconstruct shaders if missing"""
        try:
            # Check if shaders exist
            if (hasattr(bpy, 'gaussian_quad_shader') and 
                hasattr(bpy, 'gaussian_composite_shader') and
                bpy.gaussian_quad_shader and bpy.gaussian_composite_shader):
                return True
            debug_print("Shaders missing, auto-reconstructing...")
            # Import and run shader creation (adapted from script_2)
            import os
            # You'll need to set these paths to your shader files
            shader_dir = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders"
            vertex_shader_path = os.path.join(shader_dir, "vert.glsl")
            fragment_shader_path = os.path.join(shader_dir, "frag.glsl")
            composite_vertex_path = os.path.join(shader_dir, "composite_vert.glsl")
            composite_fragment_path = os.path.join(shader_dir, "composite_frag.glsl")
            # Check shader files exist
            for path in [vertex_shader_path, fragment_shader_path, composite_vertex_path, composite_fragment_path]:
                if not os.path.exists(path):
                    debug_print(f"Shader file not found: {path}")
                    return False
            # Read shader sources

            def read_shader_file(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            vertex_source = read_shader_file(vertex_shader_path)
            fragment_source = read_shader_file(fragment_shader_path)
            composite_vertex_source = read_shader_file(composite_vertex_path)
            composite_fragment_source = read_shader_file(composite_fragment_path)
            # Create main gaussian shader (adapted from script_2)
            shader_info = gpu.types.GPUShaderCreateInfo()
            shader_info.vertex_in(0, 'VEC2', "quad_coord")
            shader_info.push_constant("MAT4", "ViewMatrix")
            shader_info.push_constant("MAT4", "ProjectionMatrix") 
            shader_info.push_constant("VEC3", "focal_parameters")
            shader_info.push_constant("VEC3", "camera_position")
            shader_info.push_constant("INT", "render_mode")
            shader_info.push_constant("INT", "sh_degree")
            shader_info.push_constant("VEC2", "texture_dimensions")
            shader_info.push_constant("VEC2", "indices_dimensions")
            shader_info.push_constant("VEC2", "depth_texture_size")
            shader_info.sampler(0, 'FLOAT_3D', "gaussian_data")
            shader_info.sampler(1, 'FLOAT_2D', "sorted_indices")
            shader_info.sampler(2, 'FLOAT_2D', "blender_depth")
            shader_info.sampler(3, 'FLOAT_2D', "object_metadata")
            interface = gpu.types.GPUStageInterfaceInfo("splat_forge_quad_interface")
            interface.smooth('VEC3', "v_color")
            interface.smooth('VEC3', "v_conic")
            interface.smooth('VEC2', "v_coordxy")
            interface.smooth('FLOAT', "v_alpha")
            interface.smooth('VEC4', "v_rotation")
            interface.flat('INT', "v_render_mode")
            interface.smooth('FLOAT', "v_depth")
            shader_info.vertex_out(interface)
            shader_info.fragment_out(0, 'VEC4', 'fragColor')
            shader_info.vertex_source(vertex_source)
            shader_info.fragment_source(fragment_source)
            quad_shader = gpu.shader.create_from_info(shader_info)
            del interface
            del shader_info
            # Create composite shader
            composite_shader_info = gpu.types.GPUShaderCreateInfo()
            composite_shader_info.vertex_in(0, 'VEC2', "position")
            composite_shader_info.vertex_in(1, 'VEC2', "uv")
            composite_interface = gpu.types.GPUStageInterfaceInfo("composite_interface")
            composite_interface.smooth('VEC2', "uvInterp")
            composite_shader_info.vertex_out(composite_interface)
            composite_shader_info.sampler(0, 'FLOAT_2D', "image")
            composite_shader_info.fragment_out(0, 'VEC4', "FragColor")
            composite_shader_info.vertex_source(composite_vertex_source)
            composite_shader_info.fragment_source(composite_fragment_source)
            composite_shader = gpu.shader.create_from_info(composite_shader_info)
            del composite_interface
            del composite_shader_info
            # Create batches
            from gpu_extras.batch import batch_for_shader
            base_quad = np.array([
                [-1.0,  1.0],
                [ 1.0,  1.0],
                [ 1.0, -1.0],
                [-1.0, -1.0],
            ], dtype=np.float32)
            base_indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
            quad_batch = batch_for_shader(
                quad_shader, 
                'TRIS',
                {"quad_coord": base_quad},
                indices=base_indices
            )
            composite_batch = batch_for_shader(
                composite_shader, 
                'TRI_FAN',
                {
                    "position": ((-1, -1), (1, -1), (1, 1), (-1, 1)),
                    "uv": ((0, 0), (1, 0), (1, 1), (0, 1)),
                }
            )
            # Store globally
            bpy.gaussian_quad_shader = quad_shader
            bpy.gaussian_quad_batch = quad_batch
            bpy.gaussian_composite_shader = composite_shader  
            bpy.gaussian_composite_batch = composite_batch
            debug_print("Shaders auto-reconstructed successfully")
            return True
        except Exception as e:
            debug_print(f"Shader auto-reconstruction failed: {e}")
            return False

    def auto_reconstruct_textures():
        """Auto-reconstruct global textures if missing"""
        try:
            start_time = time.perf_counter() if DEBUG_TIMING else 0
            # Check if textures exist
            if (hasattr(bpy, 'gaussian_texture') and 
                hasattr(bpy, 'gaussian_indices_texture') and
                bpy.gaussian_texture and bpy.gaussian_indices_texture):
                debug_print("Textures exist, but rebuilding due to data updates...")
            else:
                debug_print("Global textures missing, auto-reconstructing...")
            if not hasattr(bpy, 'gaussian_object_cache') or not bpy.gaussian_object_cache:
                debug_print("ERROR: Cannot reconstruct textures without cache")
                return False
            debug_print(f"Reconstructing textures from {len(bpy.gaussian_object_cache)} cached objects...")
            # Run texture reconstruction logic (adapted from script_3)
            all_gaussian_data = []
            all_object_metadata = []
            current_start_idx = 0
            for obj_name, obj_data in bpy.gaussian_object_cache.items():
                gaussian_data = obj_data['gaussian_data']
                gaussian_count = obj_data['gaussian_count']
                obj = obj_data['object']
                debug_print(f"Processing object {obj_name}: {gaussian_count:,} gaussians")
                all_gaussian_data.append(gaussian_data)
                all_object_metadata.append({
                    'name': obj_name,
                    'start_idx': current_start_idx,
                    'gaussian_count': gaussian_count,
                    'object': obj
                })
                current_start_idx += gaussian_count
            # Merge all gaussian data
            merge_start = time.perf_counter() if DEBUG_TIMING else 0
            merged_gaussian_data = np.concatenate(all_gaussian_data, axis=0)
            total_gaussians = len(merged_gaussian_data)
            if DEBUG_TIMING:
                debug_print(f"Data merge took {(time.perf_counter() - merge_start)*1000:.2f}ms")
            debug_print(f"Merged {total_gaussians:,} total gaussians")
            # Create global 3D gaussian texture
            texture_start = time.perf_counter() if DEBUG_TIMING else 0
            total_floats = merged_gaussian_data.size
            max_texture_dim = 16384
            cube_root = int(np.ceil(np.power(total_floats, 1/3)))
            texture_depth = min(max_texture_dim, cube_root)
            texture_area = (total_floats + texture_depth - 1) // texture_depth
            texture_width = min(max_texture_dim, int(np.ceil(np.sqrt(texture_area))))
            texture_height = (texture_area + texture_width - 1) // texture_width
            flat_data = merged_gaussian_data.flatten()
            expected_size = texture_width * texture_height * texture_depth
            if len(flat_data) < expected_size:
                padded_data = np.zeros(expected_size, dtype=np.float32)
                padded_data[:len(flat_data)] = flat_data
                flat_data = padded_data
            buffer = gpu.types.Buffer('FLOAT', len(flat_data), flat_data.tolist())
            gaussian_texture = gpu.types.GPUTexture(
                (texture_width, texture_height, texture_depth), 
                format='R32F',
                data=buffer
            )
            if DEBUG_TIMING:
                debug_print(f"Gaussian texture creation took {(time.perf_counter() - texture_start)*1000:.2f}ms")
            # Create global indices texture (will be updated by depth sorting)
            indices_start = time.perf_counter() if DEBUG_TIMING else 0
            sorted_indices = np.arange(total_gaussians, dtype=np.float32)
            indices_width = min(max_texture_dim, len(sorted_indices))
            indices_height = (len(sorted_indices) + indices_width - 1) // indices_width
            expected_indices_size = indices_width * indices_height
            if len(sorted_indices) < expected_indices_size:
                padded_indices = np.zeros(expected_indices_size, dtype=np.float32)
                padded_indices[:len(sorted_indices)] = sorted_indices
                indices_data = padded_indices
            else:
                indices_data = sorted_indices
            indices_buffer = gpu.types.Buffer('FLOAT', len(indices_data), indices_data.tolist())
            indices_texture = gpu.types.GPUTexture(
                (indices_width, indices_height),
                format='R32F',
                data=indices_buffer
            )
            if DEBUG_TIMING:
                debug_print(f"Indices texture creation took {(time.perf_counter() - indices_start)*1000:.2f}ms")
            # Create metadata texture
            metadata_start = time.perf_counter() if DEBUG_TIMING else 0
            num_objects = len(all_object_metadata)
            floats_per_object = 15
            total_metadata_floats = num_objects * floats_per_object
            metadata_width = min(max_texture_dim, total_metadata_floats)
            metadata_height = (total_metadata_floats + metadata_width - 1) // metadata_width
            expected_size = metadata_width * metadata_height
            metadata_data = np.zeros(expected_size, dtype=np.float32)
            for obj_idx, obj_meta in enumerate(all_object_metadata):
                base_idx = obj_idx * floats_per_object
                uint32_start_idx = np.uint32(obj_meta['start_idx'])
                metadata_data[base_idx + 0] = uint32_start_idx.view(np.float32)
                metadata_data[base_idx + 1] = float(obj_meta['gaussian_count'])
                metadata_data[base_idx + 2] = 1.0  # Visible
                transform = obj_meta['object'].matrix_world
                matrix_idx = 0
                for col in range(4):
                    for row in range(3):
                        metadata_data[base_idx + 3 + matrix_idx] = transform[row][col]
                        matrix_idx += 1
            metadata_buffer = gpu.types.Buffer('FLOAT', len(metadata_data), metadata_data.tolist())
            metadata_texture = gpu.types.GPUTexture(
                (metadata_width, metadata_height), 
                format='R32F', 
                data=metadata_buffer
            )
            if DEBUG_TIMING:
                debug_print(f"Metadata texture creation took {(time.perf_counter() - metadata_start)*1000:.2f}ms")
            # Store globally
            bpy.gaussian_texture = gaussian_texture
            bpy.gaussian_texture_width = texture_width
            bpy.gaussian_texture_height = texture_height
            bpy.gaussian_texture_depth = texture_depth
            bpy.gaussian_indices_texture = indices_texture
            bpy.gaussian_indices_width = indices_width
            bpy.gaussian_indices_height = indices_height
            bpy.gaussian_metadata_texture = metadata_texture
            bpy.gaussian_count = total_gaussians
            bpy.gaussian_object_metadata = all_object_metadata
            if DEBUG_TIMING:
                total_time = time.perf_counter() - start_time
                debug_print(f"Total texture reconstruction took {total_time*1000:.2f}ms")
            debug_print(f"Global textures auto-reconstructed: {total_gaussians:,} gaussians from {num_objects} objects")
            debug_print(f"Texture dimensions: {texture_width}x{texture_height}x{texture_depth}")
            return True
        except Exception as e:
            debug_print(f"Texture auto-reconstruction failed: {e}")
            import traceback
            debug_print(f"Traceback: {traceback.format_exc()}")
            return False
    # ========== SOURCE OBJECT UPDATE FUNCTIONS ==========

    def find_source_object_by_uuid(source_uuid):
        """Find Blender object by gaussian_source_uuid"""
        for obj in bpy.data.objects:
            if obj.get("gaussian_source_uuid") == source_uuid:
                return obj
        return None

    def update_transforms_from_sources():
        """Update empty object transforms from their source objects"""
        try:
            start_time = time.perf_counter() if DEBUG_TIMING else 0
            if not hasattr(bpy, 'gaussian_object_cache') or not bpy.gaussian_object_cache:
                return False
            updated_count = 0
            for obj_name, obj_data in bpy.gaussian_object_cache.items():
                obj = obj_data['object']
                # Check if this object has a Blender source
                source_uuid = obj.get("source_mesh_uuid")
                if not source_uuid:
                    continue  # PLY source or no source info
                # Find source object
                source_obj = find_source_object_by_uuid(source_uuid)
                if not source_obj:
                    debug_print(f"Warning: Source object for {obj_name} not found (UUID: {source_uuid})")
                    continue
                # Copy transform from source to empty object
                try:
                    old_transform = obj.matrix_world.copy()
                    obj.matrix_world = source_obj.matrix_world.copy()
                    # Check if transform actually changed
                    if DEBUG_DATA_CHANGES:
                        translation_diff = (old_transform.translation - obj.matrix_world.translation).length
                        if translation_diff > 0.001:
                            debug_print(f"Transform updated for {obj_name}: translation change = {translation_diff:.4f}")
                    updated_count += 1
                except Exception as e:
                    debug_print(f"Warning: Failed to update transform for {obj_name}: {e}")
                    continue
            if DEBUG_TIMING:
                debug_print(f"Transform updates took {(time.perf_counter() - start_time)*1000:.2f}ms")
            if updated_count > 0:
                debug_print(f"Updated transforms for {updated_count} objects from source meshes")
            return updated_count > 0
        except Exception as e:
            debug_print(f"Transform update failed: {e}")
            return False

    def extract_attribute_data(mesh_data, attr_name):
        """Extract data from mesh attribute by name - optimized version"""
        if attr_name not in [attr.name for attr in mesh_data.attributes]:
            return None
        attr = mesh_data.attributes[attr_name]
        # Use foreach_get for much faster extraction
        data_array = np.zeros(len(attr.data), dtype=np.float32)
        attr.data.foreach_get("value", data_array)
        return data_array

    def extract_gaussian_data_from_evaluated_mesh(mesh_obj):
        """Extract and process gaussian data from EVALUATED mesh object attributes"""
        extract_start = time.perf_counter() if DEBUG_TIMING else 0
        # Get evaluated mesh data
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated_object = mesh_obj.evaluated_get(depsgraph)
        evaluated_mesh = evaluated_object.data
        debug_print(f"Extracting from evaluated mesh {mesh_obj.name}: {len(evaluated_mesh.vertices)} vertices")
        # Extract positions from evaluated vertices - optimized version
        num_points = len(evaluated_mesh.vertices)
        if num_points == 0:
            raise ValueError("Evaluated mesh has no vertices")
        # Use foreach_get for fast vertex coordinate extraction
        positions = np.zeros(num_points * 3, dtype=np.float32)
        evaluated_mesh.vertices.foreach_get("co", positions)
        positions = positions.reshape(-1, 3)
        if DEBUG_DATA_CHANGES:
            # Log sample positions for debugging
            debug_print(f"Sample positions from {mesh_obj.name}: {positions[:3]}")
        # Get available attributes from evaluated mesh
        available_attrs = [attr.name for attr in evaluated_mesh.attributes]
        # Extract spherical harmonics from evaluated mesh
        if all(attr in available_attrs for attr in ['f_dc_0', 'f_dc_1', 'f_dc_2']):
            dc_0 = extract_attribute_data(evaluated_mesh, 'f_dc_0')
            dc_1 = extract_attribute_data(evaluated_mesh, 'f_dc_1')
            dc_2 = extract_attribute_data(evaluated_mesh, 'f_dc_2')
            features_dc = np.column_stack([dc_0, dc_1, dc_2])
            # Find f_rest fields
            f_rest_fields = [attr for attr in available_attrs if attr.startswith('f_rest_')]
            f_rest_fields = sorted(f_rest_fields, key=lambda x: int(x.split('_')[-1]))
            if f_rest_fields:
                features_extra_list = []
                for field in f_rest_fields:
                    data = extract_attribute_data(evaluated_mesh, field)
                    if data is not None:
                        features_extra_list.append(data)
                if features_extra_list:
                    features_extra = np.column_stack(features_extra_list)
                    num_f_rest = len(f_rest_fields)
                    # Determine degree and coefficients to use
                    if num_f_rest >= 45:
                        actual_degree = 3
                        coeffs_to_use = 45
                    elif num_f_rest >= 24:
                        actual_degree = 2  
                        coeffs_to_use = 24
                    elif num_f_rest >= 9:
                        actual_degree = 1
                        coeffs_to_use = 9
                    else:
                        actual_degree = 0
                        coeffs_to_use = 0
                    if coeffs_to_use > 0:
                        features_extra_used = features_extra[:, :coeffs_to_use]
                        coeffs_per_degree = (actual_degree + 1) ** 2 - 1
                        features_extra_reshaped = features_extra_used.reshape((num_points, 3, coeffs_per_degree))
                        features_extra_reshaped = np.transpose(features_extra_reshaped, [0, 2, 1])
                        features_dc_reshaped = features_dc.reshape(-1, 1, 3)
                        all_features = np.concatenate([features_dc_reshaped, features_extra_reshaped], axis=1)
                        sh_coeffs = all_features.reshape(num_points, -1)
                    else:
                        sh_coeffs = features_dc
                else:
                    sh_coeffs = features_dc
            else:
                sh_coeffs = features_dc
        else:
            # Default SH coeffs if not found
            debug_print(f"Warning: f_dc attributes not found on evaluated mesh, using defaults")
            sh_coeffs = np.ones((num_points, 3)) * 0.28209479177387814
        # Extract scales from evaluated mesh
        if all(attr in available_attrs for attr in ['scale_0', 'scale_1', 'scale_2']):
            scale_0 = extract_attribute_data(evaluated_mesh, 'scale_0')
            scale_1 = extract_attribute_data(evaluated_mesh, 'scale_1')
            scale_2 = extract_attribute_data(evaluated_mesh, 'scale_2')
            scales = np.column_stack([scale_0, scale_1, scale_2])
            scales = np.exp(scales)  # Apply exponential
        else:
            debug_print(f"Warning: scale attributes not found on evaluated mesh, using defaults")
            scales = np.ones((num_points, 3)) * 0.01
        # Extract rotations from evaluated mesh
        if all(attr in available_attrs for attr in ['rot_0', 'rot_1', 'rot_2', 'rot_3']):
            rot_0 = extract_attribute_data(evaluated_mesh, 'rot_0')
            rot_1 = extract_attribute_data(evaluated_mesh, 'rot_1')
            rot_2 = extract_attribute_data(evaluated_mesh, 'rot_2')
            rot_3 = extract_attribute_data(evaluated_mesh, 'rot_3')
            rotations = np.column_stack([rot_0, rot_1, rot_2, rot_3])
            # Normalize quaternions
            norms = np.linalg.norm(rotations, axis=1, keepdims=True)
            rotations = rotations / norms
        else:
            debug_print(f"Warning: rotation attributes not found on evaluated mesh, using defaults")
            rotations = np.zeros((num_points, 4))
            rotations[:, 0] = 1.0  # Identity quaternion
        # Extract opacity from evaluated mesh
        if 'opacity' in available_attrs:
            opacity_raw = extract_attribute_data(evaluated_mesh, 'opacity')
            opacity = 1.0 / (1.0 + np.exp(-opacity_raw))  # Apply sigmoid
        else:
            debug_print(f"Warning: opacity attribute not found on evaluated mesh, using defaults")
            opacity = np.ones(num_points)
        if DEBUG_TIMING:
            debug_print(f"Data extraction took {(time.perf_counter() - extract_start)*1000:.2f}ms")
        return {
            'num_points': num_points,
            'positions': positions,
            'scales': scales,
            'rotations': rotations,
            'opacities': opacity,
            'sh_coeffs': sh_coeffs,
            'sh_dim': sh_coeffs.shape[1]
        }

    def check_mesh_has_gaussian_attributes(mesh_obj):
        """Check if mesh object has basic gaussian attributes"""
        if not mesh_obj or not mesh_obj.data:
            return False
        # Check for basic gaussian attributes
        required_attrs = ['f_dc_0', 'f_dc_1', 'f_dc_2']
        available_attrs = [attr.name for attr in mesh_obj.data.attributes]
        return all(attr in available_attrs for attr in required_attrs)

    def refresh_data_from_evaluated_sources():
        """Re-extract gaussian data from evaluated source meshes (EXPENSIVE!) - WITH DEBUG"""
        try:
            start_time = time.perf_counter() if DEBUG_TIMING else 0
            if not hasattr(bpy, 'gaussian_object_cache') or not bpy.gaussian_object_cache:
                debug_print("ERROR: No gaussian object cache found")
                return False
            debug_print(f"Starting evaluated data refresh for {len(bpy.gaussian_object_cache)} objects...")
            updated_count = 0
            data_changes_detected = []
            for obj_name, obj_data in bpy.gaussian_object_cache.items():
                obj = obj_data['object']
                # Check if this object has a Blender source
                source_uuid = obj.get("source_mesh_uuid")
                if not source_uuid:
                    debug_print(f"Skipping {obj_name}: No source UUID (PLY source)")
                    continue  # PLY source or no source info
                # Find source object
                source_obj = find_source_object_by_uuid(source_uuid)
                if not source_obj:
                    debug_print(f"Warning: Source object for {obj_name} not found (UUID: {source_uuid})")
                    continue
                # Validate that source object has gaussian attributes
                if not check_mesh_has_gaussian_attributes(source_obj):
                    debug_print(f"Warning: Source object '{source_obj.name}' missing gaussian attributes")
                    continue
                try:
                    debug_print(f"Refreshing data for {obj_name} from source {source_obj.name}")
                    # Store old data for comparison
                    old_data = obj_data['gaussian_data'].copy() if DEBUG_DATA_CHANGES else None
                    # Extract fresh data from evaluated mesh
                    gaussian_data_info = extract_gaussian_data_from_evaluated_mesh(source_obj)
                    # Create gaussian data array (59 floats per gaussian)
                    num_gaussians = gaussian_data_info['num_points']
                    sh_dim = 48
                    total_dim = 3 + 4 + 3 + 1 + sh_dim
                    gaussian_data = np.zeros((num_gaussians, total_dim), dtype=np.float32)
                    # Pack data in original order
                    gaussian_data[:, 0:3] = gaussian_data_info['positions']
                    gaussian_data[:, 3:7] = gaussian_data_info['rotations']
                    gaussian_data[:, 7:10] = gaussian_data_info['scales']
                    gaussian_data[:, 10] = gaussian_data_info['opacities'].flatten()
                    # Handle SH coefficients
                    source_sh_coeffs = gaussian_data_info['sh_coeffs']
                    if source_sh_coeffs.shape[1] >= sh_dim:
                        gaussian_data[:, 11:11+sh_dim] = source_sh_coeffs[:, :sh_dim]
                    else:
                        gaussian_data[:, 11:11+source_sh_coeffs.shape[1]] = source_sh_coeffs
                    # Check for actual data changes
                    if DEBUG_DATA_CHANGES and old_data is not None:
                        if old_data.shape == gaussian_data.shape:
                            position_diff = np.linalg.norm(old_data[:, 0:3] - gaussian_data[:, 0:3], axis=1).max()
                            if position_diff > 0.001:
                                data_changes_detected.append(f"{obj_name}: max position change = {position_diff:.6f}")
                            else:
                                debug_print(f"No significant position changes detected for {obj_name}")
                        else:
                            data_changes_detected.append(f"{obj_name}: shape changed from {old_data.shape} to {gaussian_data.shape}")
                    # Update object properties and cache
                    obj["gaussian_data"] = gaussian_data.tobytes()
                    obj["gaussian_count"] = num_gaussians
                    obj["sh_degree"] = gaussian_data_info['sh_dim']
                    obj["last_load_time"] = time.time()
                    # Update cache
                    bpy.gaussian_object_cache[obj_name].update({
                        'gaussian_data': gaussian_data,
                        'gaussian_count': num_gaussians,
                        'sh_degree': gaussian_data_info['sh_dim']
                    })
                    debug_print(f"Successfully refreshed {obj_name}: {num_gaussians:,} gaussians")
                    updated_count += 1
                except Exception as e:
                    debug_print(f"Warning: Failed to refresh data for {obj_name}: {e}")
                    import traceback
                    debug_print(f"Traceback: {traceback.format_exc()}")
                    continue
            if DEBUG_DATA_CHANGES and data_changes_detected:
                debug_print("DATA CHANGES DETECTED:")
                for change in data_changes_detected:
                    debug_print(f"  {change}")
            elif DEBUG_DATA_CHANGES:
                debug_print("No significant data changes detected in any object")
            if updated_count > 0:
                debug_print(f"Refreshed gaussian data for {updated_count} objects from evaluated meshes")
                # Mark that global textures need rebuilding
                bpy.gaussian_global_needs_update = True
                if DEBUG_TIMING:
                    debug_print(f"Data refresh took {(time.perf_counter() - start_time)*1000:.2f}ms")
            return updated_count > 0
        except Exception as e:
            debug_print(f"Data refresh failed: {e}")
            import traceback
            debug_print(f"Traceback: {traceback.format_exc()}")
            return False
    # ========== SIMPLIFIED COMPOSITING FUNCTIONS (Let Blender handle paths) ==========

    def load_external_depth_from_script7a(frame_num, width, height):
        """Load depth texture from Script 7a output (Simplified - let Blender handle paths)"""
        try:
            if not USE_EXTERNAL_DEPTH:
                return None
            # Build path using original TEMP_RENDER_PATH - let Blender resolve it
            depth_path = os.path.join(TEMP_RENDER_PATH, f"regular_depth_{frame_num:04d}.exr")
            debug_print(f"Attempting to load external depth: {depth_path}")
            # Try to load directly - Blender will handle path resolution
            depth_image = bpy.data.images.load(depth_path, check_existing=False)
            if not depth_image:
                debug_print(f"External depth not found or failed to load: {depth_path}")
                return None
            debug_print(f"Loading external depth: {os.path.basename(depth_path)}")
            # Set proper colorspace for depth data
            try:
                depth_image.colorspace_settings.name = 'Non-Color'
            except:
                try:
                    depth_image.colorspace_settings.name = 'Linear Rec.709'
                except:
                    pass
            # Extract depth data using Blender's native orientation
            depth_width, depth_height = depth_image.size
            depth_channels = depth_image.channels
            depth_pixels = np.zeros(depth_width * depth_height * depth_channels, dtype=np.float32)
            depth_image.pixels.foreach_get(depth_pixels)
            # Clean up image datablock
            bpy.data.images.remove(depth_image)
            # Reshape and extract single channel (depth is grayscale)
            if depth_channels == 1:
                depth_array = depth_pixels.reshape(depth_height, depth_width)
            else:
                depth_pixels_reshaped = depth_pixels.reshape(depth_height, depth_width, depth_channels)
                depth_array = depth_pixels_reshaped[:, :, 0]  # Take first channel
            # Resize if needed (simple numpy indexing)
            if depth_array.shape[:2] != (height, width):
                h_indices = np.round(np.linspace(0, depth_array.shape[0]-1, height)).astype(int)
                w_indices = np.round(np.linspace(0, depth_array.shape[1]-1, width)).astype(int)
                depth_array = depth_array[np.ix_(h_indices, w_indices)]
            # Debug: Print depth value range
            debug_print(f"Depth range: {np.min(depth_array):.3f} to {np.max(depth_array):.3f}")
            # Convert from metric depth to GL depth using SplatForge method
            scene = bpy.context.scene
            camera = scene.camera
            if camera and camera.data:
                near_plane = camera.data.clip_start
                far_plane = camera.data.clip_end
                debug_print(f"Camera clips: near={near_plane:.3f}, far={far_plane:.3f}")
                # SplatForge convert_metric_to_gl_depth formula
                near_plane = max(near_plane, 1e-6)
                far_plane = max(far_plane, near_plane + 1e-6)
                metric_depths = np.clip(depth_array, near_plane, far_plane)
                gl_depth = (far_plane / (far_plane - near_plane)) * (1.0 - near_plane / metric_depths)
                gl_depth = np.clip(gl_depth, 0.0, 1.0)
                debug_print(f"GL depth range: {np.min(gl_depth):.3f} to {np.max(gl_depth):.3f}")
            else:
                # Fallback: normalize to 0-1 range
                depth_min = np.min(depth_array)
                depth_max = np.max(depth_array)
                if depth_max > depth_min:
                    gl_depth = (depth_array - depth_min) / (depth_max - depth_min)
                else:
                    gl_depth = depth_array
                debug_print("Warning: No camera found, using normalized depth")
            # Create GPU texture (NO Y-flip - trust Blender's orientation)
            depth_data_flat = gl_depth.flatten()
            depth_buffer = gpu.types.Buffer('FLOAT', len(depth_data_flat), depth_data_flat.tolist())
            depth_texture = gpu.types.GPUTexture((width, height), format='R32F', data=depth_buffer)
            debug_print(f"External depth loaded: {width}x{height}")
            return depth_texture
        except Exception as e:
            debug_print(f"Failed to load external depth: {e}")
            return None

    def load_external_color_from_script7a(frame_num):
        """Load color image from Script 7a output for compositing (Simplified - let Blender handle paths)"""
        try:
            if not USE_EXTERNAL_COLOR:
                return None, None
            # Build path using original TEMP_RENDER_PATH - let Blender resolve it
            color_path = os.path.join(TEMP_RENDER_PATH, f"regular_color_{frame_num:04d}.exr")
            debug_print(f"Attempting to load external color: {color_path}")
            # Try to load directly - Blender will handle path resolution
            color_image = bpy.data.images.load(color_path, check_existing=False)
            if not color_image:
                debug_print(f"External color not found or failed to load: {color_path}")
                return None, None
            debug_print(f"Loading external color: {os.path.basename(color_path)}")
            # Extract color data using Blender's native orientation
            width, height = color_image.size
            channels = color_image.channels
            color_pixels = np.zeros(width * height * channels, dtype=np.float32)
            color_image.pixels.foreach_get(color_pixels)
            # Keep the image for compositing, reshape but don't flip
            color_array = color_pixels.reshape(height, width, channels)
            return color_image, color_array
        except Exception as e:
            debug_print(f"Failed to load external color: {e}")
            return None, None

    def alpha_composite_images(foreground_rgba, background_rgba):
        """Alpha composite gaussian render over regular scene (CPU-based, preserves transparency)"""
        try:
            fg_rgb = foreground_rgba[:, :, :3]
            fg_alpha = foreground_rgba[:, :, 3:4]
            # Handle both RGB and RGBA backgrounds
            if background_rgba.shape[2] == 4:
                bg_rgb = background_rgba[:, :, :3]
                bg_alpha = background_rgba[:, :, 3:4]
            else:
                bg_rgb = background_rgba
                bg_alpha = np.ones_like(fg_alpha)  # Assume opaque if no alpha channel
            # Proper alpha compositing that preserves transparency
            result_alpha = fg_alpha + bg_alpha * (1 - fg_alpha)
            # Use safe division to avoid divide by zero
            # Where result_alpha is 0, the result should be (0,0,0,0)
            safe_alpha = np.where(result_alpha > 1e-8, result_alpha, 1.0)
            result_rgb = (
                fg_rgb * fg_alpha + bg_rgb * bg_alpha * (1 - fg_alpha)
            ) / safe_alpha
            # Set RGB to 0 where alpha is 0 (fully transparent pixels)
            result_rgb = np.where(result_alpha > 1e-8, result_rgb, 0.0)
            result = np.concatenate([result_rgb, result_alpha], axis=2)
            return result
        except Exception as e:
            debug_print(f"Alpha compositing failed: {e}")
            return None
    # ========== CORE RENDERING FUNCTIONS ==========

    def update_metadata_texture():
        """Update metadata texture with current object transforms (for animations)"""
        try:
            start_time = time.perf_counter() if DEBUG_TIMING else 0
            if not hasattr(bpy, 'gaussian_object_metadata') or not bpy.gaussian_object_metadata:
                debug_print("No object metadata found for update")
                return False
            num_objects = len(bpy.gaussian_object_metadata)
            floats_per_object = 15
            total_metadata_floats = num_objects * floats_per_object
            max_texture_dim = 16384
            metadata_width = min(max_texture_dim, total_metadata_floats)
            metadata_height = (total_metadata_floats + metadata_width - 1) // metadata_width
            expected_size = metadata_width * metadata_height
            metadata_data = np.zeros(expected_size, dtype=np.float32)
            # Fill metadata with CURRENT transforms for all objects
            for obj_idx, obj_meta in enumerate(bpy.gaussian_object_metadata):
                base_idx = obj_idx * floats_per_object
                obj = obj_meta['object']
                # Start index as uint32 bitcast to float32
                uint32_start_idx = np.uint32(obj_meta['start_idx'])
                metadata_data[base_idx + 0] = uint32_start_idx.view(np.float32)
                metadata_data[base_idx + 1] = float(obj_meta['gaussian_count'])
                metadata_data[base_idx + 2] = 1.0  # Visible
                # CURRENT object transform matrix
                current_transform = obj.matrix_world
                matrix_idx = 0
                for col in range(4):
                    for row in range(3):
                        metadata_data[base_idx + 3 + matrix_idx] = current_transform[row][col]
                        matrix_idx += 1
            # Create new metadata texture
            metadata_buffer = gpu.types.Buffer('FLOAT', len(metadata_data), metadata_data.tolist())
            bpy.gaussian_metadata_texture = gpu.types.GPUTexture(
                (metadata_width, metadata_height), 
                format='R32F', 
                data=metadata_buffer
            )
            if DEBUG_TIMING:
                debug_print(f"Metadata texture update took {(time.perf_counter() - start_time)*1000:.2f}ms")
            return True
        except Exception as e:
            debug_print(f"Metadata update error: {e}")
            return False

    def perform_depth_sort_for_camera(camera_view_matrix):
        """Perform depth sorting for the given camera matrix"""
        try:
            start_time = time.perf_counter() if DEBUG_TIMING else 0
            if not hasattr(bpy, 'gaussian_object_cache') or not bpy.gaussian_object_cache:
                debug_print("No gaussian cache available for depth sorting")
                return False
            all_camera_positions = []
            view_matrix_np = np.array(camera_view_matrix, dtype=np.float32)
            # Transform gaussians from all objects to camera space
            for obj_name, obj_data in bpy.gaussian_object_cache.items():
                gaussian_data = obj_data['gaussian_data']
                gaussian_count = obj_data['gaussian_count']
                obj = obj_data['object']
                if gaussian_count == 0:
                    continue
                # Extract positions (first 3 columns of gaussian data)
                positions = gaussian_data[:, 0:3]
                # Get current object transform
                object_transform_np = np.array(obj.matrix_world, dtype=np.float32)
                # Combine camera and object transforms
                combined_transform = view_matrix_np @ object_transform_np
                # Transform positions to camera space
                positions_homogeneous = np.ones((len(positions), 4), dtype=np.float32)
                positions_homogeneous[:, 0:3] = positions
                camera_positions = positions_homogeneous @ combined_transform.T
                all_camera_positions.append(camera_positions[:, 0:3])
            if not all_camera_positions:
                debug_print("No valid gaussian positions found for depth sorting")
                return False
            # Merge all camera-space positions
            merged_camera_positions = np.concatenate(all_camera_positions, axis=0)
            # Extract depths (Z values in camera space)
            depths = merged_camera_positions[:, 2]
            if len(depths) == 0:
                debug_print("No depths found for sorting")
                return True
            # Depth sorting algorithm from script_4
            depths_min = np.min(depths)
            depths_max = np.max(depths)
            depth_range = depths_max - depths_min
            if depth_range > 0:
                depths_normalized = (depths - depths_min) / depth_range
                scale_factor = np.float64(np.iinfo(np.uint32).max) - 1.0
                depths_scaled = depths_normalized * scale_factor
                depths_uint32 = depths_scaled.astype(np.uint32)
            else:
                depths_uint32 = np.zeros_like(depths, dtype=np.uint32)
            # Sort indices by depth
            sorted_indices = np.argsort(depths_uint32, kind='stable').astype(np.float32)
            # Update global indices texture
            if hasattr(bpy, 'gaussian_indices_texture') and hasattr(bpy, 'gaussian_indices_width'):
                indices_width = bpy.gaussian_indices_width
                indices_height = bpy.gaussian_indices_height
                expected_indices_size = indices_width * indices_height
                if len(sorted_indices) < expected_indices_size:
                    padded_indices = np.zeros(expected_indices_size, dtype=np.float32)
                    padded_indices[:len(sorted_indices)] = sorted_indices
                    indices_data = padded_indices
                else:
                    indices_data = sorted_indices
                indices_buffer = gpu.types.Buffer('FLOAT', len(indices_data), indices_data.tolist())
                bpy.gaussian_indices_texture = gpu.types.GPUTexture(
                    (indices_width, indices_height),
                    format='R32F',
                    data=indices_buffer
                )
                if DEBUG_TIMING:
                    debug_print(f"Depth sorting took {(time.perf_counter() - start_time)*1000:.2f}ms")
                return True
            else:
                debug_print("No indices texture available to update")
                return False
        except Exception as e:
            debug_print(f"Depth sorting failed: {e}")
            return False

    def create_dummy_depth_texture(width, height):
        """Create a dummy depth texture filled with far plane values"""
        try:
            dummy_data = np.ones(width * height, dtype=np.float32)  # Far plane = 1.0
            dummy_buffer = gpu.types.Buffer('FLOAT', len(dummy_data), dummy_data.tolist())
            dummy_texture = gpu.types.GPUTexture((width, height), format='R32F', data=dummy_buffer)
            return dummy_texture
        except Exception as e:
            debug_print(f"Failed to create dummy depth texture: {e}")
            return None

    def create_render_framebuffer(width, height):
        """Create framebuffer for offline rendering"""
        try:
            color_texture = gpu.types.GPUTexture((width, height), format='RGBA32F')
            depth_texture = gpu.types.GPUTexture((width, height), format='DEPTH_COMPONENT32F')
            framebuffer = gpu.types.GPUFrameBuffer(
                color_slots=[color_texture],
                depth_slot=depth_texture
            )
            return color_texture, depth_texture, framebuffer
        except Exception as e:
            debug_print(f"Failed to create render framebuffer: {e}")
            return None

    def apply_composite_shader(color_texture, width, height):
        """Apply composite shader to final output"""
        try:
            if not hasattr(bpy, 'gaussian_composite_shader') or not bpy.gaussian_composite_shader:
                debug_print("Composite shader not available")
                return None
            # Create temporary framebuffer for composite
            composite_color = gpu.types.GPUTexture((width, height), format='RGBA8')
            composite_depth = gpu.types.GPUTexture((width, height), format='DEPTH_COMPONENT24')
            composite_fb = gpu.types.GPUFrameBuffer(
                color_slots=[composite_color],
                depth_slot=composite_depth
            )
            with composite_fb.bind():
                fb = gpu.state.active_framebuffer_get()
                fb.clear(color=(0.0, 0.0, 0.0, 0.0), depth=1.0)
                gpu.state.depth_test_set('NONE')
                gpu.state.depth_mask_set(False)
                gpu.state.blend_set('NONE')
                gpu.state.viewport_set(0, 0, width, height)
                bpy.gaussian_composite_shader.bind()
                bpy.gaussian_composite_shader.uniform_sampler("image", color_texture)
                bpy.gaussian_composite_batch.draw(bpy.gaussian_composite_shader)
                # Read the result
                buffer = fb.read_color(0, 0, width, height, 4, 0, 'FLOAT')
                buffer.dimensions = (width * height * 4,)
            # Clean up composite framebuffer
            del composite_fb, composite_depth, composite_color
            return np.array(buffer, dtype=np.float32)
        except Exception as e:
            debug_print(f"Composite shader application failed: {e}")
            return None

    def render_gaussian_pass_internal(frame_num=None, is_animation=False, render_mode=0, pass_name="gaussian", pass_suffix="color", external_depth_texture=None):
        """Internal gaussian rendering function for specific pass"""
        try:
            frame_start_time = time.perf_counter() if DEBUG_TIMING else 0
            # Check scene requirements
            scene = bpy.context.scene
            camera = scene.camera
            if not camera:
                error_msg = f"ERROR: No camera found in scene"
                if frame_num:
                    error_msg += f" (Frame {frame_num})"
                debug_print(error_msg)
                return None
            # Set frame if specified
            if frame_num is not None:
                scene.frame_set(frame_num)
                bpy.context.evaluated_depsgraph_get().update()
                # Update metadata texture for animated objects
                if is_animation:
                    update_metadata_texture()
            # Determine render resolution
            if RENDER_WIDTH > 0 and RENDER_HEIGHT > 0:
                width = RENDER_WIDTH
                height = RENDER_HEIGHT
            else:
                render = scene.render
                width = int(render.resolution_x * render.resolution_percentage / 100)
                height = int(render.resolution_y * render.resolution_percentage / 100)
            frame_info = f" (Frame {frame_num}, {pass_name})" if frame_num else f" ({pass_name})"
            if not is_animation:
                debug_print(f"Rendering {width}x{height}{frame_info}")
            # Set up camera matrices
            view_matrix = camera.matrix_world.inverted()
            depsgraph = bpy.context.evaluated_depsgraph_get()
            projection_matrix = camera.calc_matrix_camera(
                depsgraph, 
                x=width, 
                y=height, 
                scale_x=scene.render.pixel_aspect_x, 
                scale_y=scene.render.pixel_aspect_y
            )
            # Perform depth sorting for render camera position
            if FORCE_DEPTH_SORT:
                if not perform_depth_sort_for_camera(view_matrix):
                    debug_print(f"WARNING: Depth sorting failed{frame_info}")
            # Create render framebuffer
            render_fb = create_render_framebuffer(width, height)
            if not render_fb:
                debug_print(f"ERROR: Failed to create render framebuffer{frame_info}")
                return None
            color_texture, depth_texture, framebuffer = render_fb
            # Use external depth or create dummy depth texture
            depth_tex_to_use = external_depth_texture if external_depth_texture else create_dummy_depth_texture(width, height)
            if not depth_tex_to_use:
                debug_print(f"ERROR: Failed to create depth texture{frame_info}")
                return None
            try:
                # Render to framebuffer
                with framebuffer.bind():
                    fb = gpu.state.active_framebuffer_get()
                    fb.clear(color=(0.0, 0.0, 0.0, 0.0), depth=1.0)
                    gpu.state.depth_test_set('ALWAYS')
                    gpu.state.depth_mask_set(True)
                    gpu.state.blend_set('ALPHA')
                    gpu.state.program_point_size_set(False)
                    gpu.state.viewport_set(0, 0, width, height)
                    # Set up matrices
                    with gpu.matrix.push_pop():
                        with gpu.matrix.push_pop_projection():
                            gpu.matrix.load_matrix(view_matrix)
                            gpu.matrix.load_projection_matrix(projection_matrix)
                            # Render gaussians using existing shader system
                            bpy.gaussian_quad_shader.bind()
                            # Set shader uniforms
                            bpy.gaussian_quad_shader.uniform_float("ViewMatrix", view_matrix)
                            bpy.gaussian_quad_shader.uniform_float("ProjectionMatrix", projection_matrix)
                            # Calculate camera parameters
                            fy = projection_matrix[1][1]
                            fov_y = 2 * math.atan(1.0 / fy)
                            tan_half_fovy = math.tan(fov_y * 0.5)
                            aspect_ratio = width / height
                            tan_half_fovx = tan_half_fovy * aspect_ratio
                            focal = height / (2.0 * tan_half_fovy)
                            camera_pos = mathutils.Vector((view_matrix[0][3], view_matrix[1][3], view_matrix[2][3]))
                            bpy.gaussian_quad_shader.uniform_float("focal_parameters", (tan_half_fovx, tan_half_fovy, focal))
                            bpy.gaussian_quad_shader.uniform_float("camera_position", camera_pos)
                            bpy.gaussian_quad_shader.uniform_int("render_mode", render_mode)
                            bpy.gaussian_quad_shader.uniform_int("sh_degree", SH_DEGREE if render_mode == 0 else 0)
                            # Set texture dimensions
                            bpy.gaussian_quad_shader.uniform_float("texture_dimensions", 
                                                                  (bpy.gaussian_texture_width, bpy.gaussian_texture_height))
                            bpy.gaussian_quad_shader.uniform_float("indices_dimensions", 
                                                                  (bpy.gaussian_indices_width, bpy.gaussian_indices_height))
                            bpy.gaussian_quad_shader.uniform_float("depth_texture_size", (width, height))
                            # Bind textures
                            bpy.gaussian_quad_shader.uniform_sampler("gaussian_data", bpy.gaussian_texture)
                            bpy.gaussian_quad_shader.uniform_sampler("sorted_indices", bpy.gaussian_indices_texture)
                            bpy.gaussian_quad_shader.uniform_sampler("blender_depth", depth_tex_to_use)
                            bpy.gaussian_quad_shader.uniform_sampler("object_metadata", bpy.gaussian_metadata_texture)
                            # Draw all gaussians
                            debug_print(f"Drawing {bpy.gaussian_count:,} gaussians...")
                            bpy.gaussian_quad_batch.draw_instanced(bpy.gaussian_quad_shader, instance_count=bpy.gaussian_count)
                    # Read rendered result
                    buffer_read_start = time.perf_counter() if DEBUG_TIMING else 0
                    raw_buffer = fb.read_color(0, 0, width, height, 4, 0, 'FLOAT')
                    raw_buffer.dimensions = (width * height * 4,)
                    if DEBUG_TIMING:
                        debug_print(f"Buffer read took {(time.perf_counter() - buffer_read_start)*1000:.2f}ms")
                if DEBUG_TIMING:
                    gpu_time = time.perf_counter() - frame_start_time
                    debug_print(f"GPU render took {gpu_time*1000:.2f}ms")
                # Apply composite shader
                composite_start = time.perf_counter() if DEBUG_TIMING else 0
                final_buffer = apply_composite_shader(color_texture, width, height)
                if final_buffer is None:
                    debug_print(f"WARNING: Composite shader failed, using raw buffer{frame_info}")
                    final_buffer = np.array(raw_buffer, dtype=np.float32)
                if DEBUG_TIMING:
                    debug_print(f"Composite shader took {(time.perf_counter() - composite_start)*1000:.2f}ms")
                # Return the rendered data as numpy array
                return final_buffer.reshape(height, width, 4)
            finally:
                # Clean up frame resources (but keep external depth)
                if not external_depth_texture and depth_tex_to_use:
                    del depth_tex_to_use
                del framebuffer, depth_texture, color_texture
        except Exception as e:
            frame_info = f" (Frame {frame_num}, {pass_name})" if frame_num else f" ({pass_name})"
            debug_print(f"Gaussian render failed{frame_info}: {e}")
            return None

    def get_enabled_passes():
        """Get list of enabled render passes"""
        passes = []
        if RENDER_GAUSSIAN:
            passes.append(('gaussian', 0, 'color'))
        if RENDER_DEPTH:
            passes.append(('depth', 1, 'depth'))
        if RENDER_SURFEL:
            passes.append(('surfel', 2, 'surfel'))
        return passes

    def get_output_path_for_pass(frame_num, pass_suffix):
        """Get output file path with pass suffix"""
        try:
            scene = bpy.context.scene
            original_frame = scene.frame_current
            if frame_num is not None:
                scene.frame_set(frame_num)
            base_path = scene.render.frame_path(frame=frame_num if frame_num else scene.frame_current)
            # Add pass suffix to filename
            path_parts = os.path.splitext(base_path)
            output_path = f"{path_parts[0]}_{pass_suffix}{path_parts[1]}"
            scene.frame_set(original_frame)
            return output_path
        except Exception as e:
            debug_print(f"Error generating output path: {e}")
            return None

    def check_file_exists(frame_num, pass_suffix):
        """Check if output file for this frame and pass already exists"""
        try:
            output_path = get_output_path_for_pass(frame_num, pass_suffix)
            return os.path.exists(output_path) if output_path else False
        except:
            return False

    def check_all_passes_exist(frame_num, enabled_passes):
        """Check if all enabled passes already exist for this frame"""
        if not SKIP_EXISTING_FILES:
            return False
        for pass_name, pass_mode, pass_suffix in enabled_passes:
            if not check_file_exists(frame_num, pass_suffix):
                return False
        return True

    def render_frame_with_integration(frame_num=None, is_animation=False):
        """Render frame with external depth integration and compositing (CORRECTED VERSION)"""
        try:
            frame_start_time = time.time()
            scene = bpy.context.scene
            frame_info = f" (Frame {frame_num})" if frame_num else ""
            current_frame = frame_num if frame_num else scene.frame_current
            debug_print(f"=== STARTING FRAME RENDER ===", force=True)
            debug_print(f"Frame: {frame_num}, Animation: {is_animation}")
            debug_print(f"Compositing: USE_TEMP_RENDERS={USE_TEMP_RENDERS}, Depth={USE_EXTERNAL_DEPTH}, Color={USE_EXTERNAL_COLOR}")
            # Set frame if specified and handle source object updates
            if frame_num is not None:
                debug_print(f"Setting frame to {frame_num}")
                scene.frame_set(frame_num)
                depsgraph_start = time.perf_counter() if DEBUG_TIMING else 0
                bpy.context.evaluated_depsgraph_get().update()
                if DEBUG_TIMING:
                    debug_print(f"Depsgraph update took {(time.perf_counter() - depsgraph_start)*1000:.2f}ms")
                # NEW: Optional source object updates WITH DEBUG
                if UPDATE_SOURCE_TRANSFORMS:
                    debug_print("Updating transforms from source objects...")
                    update_transforms_from_sources()
                if REFRESH_EVALUATED_DATA:
                    debug_print("=== REFRESHING EVALUATED DATA ===")
                    # Store cache state before refresh for comparison
                    cache_before = {}
                    if DEBUG_DATA_CHANGES:
                        for obj_name, obj_data in bpy.gaussian_object_cache.items():
                            cache_before[obj_name] = {
                                'count': obj_data['gaussian_count'],
                                'data_hash': hash(obj_data['gaussian_data'].tobytes())
                            }
                    data_updated = refresh_data_from_evaluated_sources()
                    if data_updated:
                        debug_print("Data was updated, rebuilding textures...")
                        # Verify cache changes
                        if DEBUG_DATA_CHANGES:
                            debug_print("CACHE STATE COMPARISON:")
                            for obj_name, obj_data in bpy.gaussian_object_cache.items():
                                if obj_name in cache_before:
                                    old_hash = cache_before[obj_name]['data_hash']
                                    new_hash = hash(obj_data['gaussian_data'].tobytes())
                                    if old_hash != new_hash:
                                        debug_print(f"  {obj_name}: DATA CHANGED (hash: {old_hash} -> {new_hash})")
                                    else:
                                        debug_print(f"  {obj_name}: no data change detected")
                        # Rebuild textures
                        texture_rebuild_start = time.perf_counter()
                        rebuild_success = auto_reconstruct_textures()
                        texture_rebuild_time = time.perf_counter() - texture_rebuild_start
                        if not rebuild_success:
                            debug_print(f"ERROR: Failed to rebuild textures after data refresh", force=True)
                            return False
                        else:
                            debug_print(f"Texture rebuild completed in {texture_rebuild_time*1000:.2f}ms")
                    else:
                        debug_print("No data updates detected, skipping texture rebuild")
            # Determine render resolution
            if RENDER_WIDTH > 0 and RENDER_HEIGHT > 0:
                width = RENDER_WIDTH
                height = RENDER_HEIGHT
            else:
                render = scene.render
                width = int(render.resolution_x * render.resolution_percentage / 100)
                height = int(render.resolution_y * render.resolution_percentage / 100)
            # Load external depth if available
            external_depth_texture = None
            if USE_TEMP_RENDERS and USE_EXTERNAL_DEPTH:
                debug_print("=== TEMP RENDER LOADING ===")
                external_depth_texture = load_external_depth_from_script7a(current_frame, width, height)
                if external_depth_texture:
                    debug_print("Using loaded temp depth for compositing")
                else:
                    debug_print("No temp depth found, using dummy depth")
            # Load external color if available
            external_color_image = None
            external_color_array = None
            if USE_TEMP_RENDERS and USE_EXTERNAL_COLOR and COMPOSITE_OVER_REGULAR:
                external_color_image, external_color_array = load_external_color_from_script7a(current_frame)
                if external_color_array is not None:
                    debug_print("External color loaded for compositing")
                else:
                    debug_print("No external color found")
            # Get enabled gaussian passes
            gaussian_passes = []
            if RENDER_GAUSSIAN:
                gaussian_passes.append(('gaussian', 0, 'color'))
            if RENDER_DEPTH:
                gaussian_passes.append(('depth', 1, 'depth'))
            if RENDER_SURFEL:
                gaussian_passes.append(('surfel', 2, 'surfel'))
            # Render each gaussian pass
            rendered_passes = {}
            for pass_name, pass_mode, pass_suffix in gaussian_passes:
                debug_print(f"Rendering {pass_name} pass...")
                result = render_gaussian_pass_internal(
                    frame_num, is_animation, pass_mode, pass_name, pass_suffix, external_depth_texture
                )
                if result is not None:
                    rendered_passes[pass_suffix] = result
                    debug_print(f"Completed {pass_name} pass")
                else:
                    debug_print(f"Failed {pass_name} pass")
            # Composite gaussian over regular scene if both available
            if COMPOSITE_OVER_REGULAR and 'color' in rendered_passes and external_color_array is not None:
                debug_print("=== COLOR COMPOSITING ===")
                composite_start = time.perf_counter() if DEBUG_TIMING else 0
                gaussian_rgba = rendered_passes['color']
                # Resize external color if needed
                if external_color_array.shape[:2] != (height, width):
                    h_indices = np.round(np.linspace(0, external_color_array.shape[0]-1, height)).astype(int)
                    w_indices = np.round(np.linspace(0, external_color_array.shape[1]-1, width)).astype(int)
                    external_color_array = external_color_array[np.ix_(h_indices, w_indices)]
                    debug_print(f"Resized external color to {height}x{width}")
                # Perform alpha compositing (CPU-based)
                composite_result = alpha_composite_images(gaussian_rgba, external_color_array)
                if composite_result is not None:
                    rendered_passes['composite'] = composite_result
                    debug_print("Completed compositing over regular scene")
                    if DEBUG_TIMING:
                        debug_print(f"Color compositing took {(time.perf_counter() - composite_start)*1000:.2f}ms")
            # Save results to files and create image datablocks
            if SAVE_TO_FILE or not is_animation:
                debug_print("Saving render results...")
                for pass_suffix, render_data in rendered_passes.items():
                    # Create image datablock
                    image_name = f"gaussian_render_{pass_suffix}"
                    if image_name in bpy.data.images:
                        image = bpy.data.images[image_name]
                        if image.size[0] != width or image.size[1] != height:
                            image.scale(width, height)
                    else:
                        alpha = (pass_suffix in ['color', 'composite'])
                        image = bpy.data.images.new(image_name, width, height, float_buffer=True, alpha=alpha)
                    # Set pixel data
                    flat_data = render_data.flatten()
                    image.pixels.foreach_set(flat_data)
                    image.file_format = scene.render.image_settings.file_format
                    # Save to file if requested
                    if SAVE_TO_FILE:
                        output_path = get_output_path_for_pass(current_frame, pass_suffix)
                        if output_path:
                            if SAVE_AS_RENDER:
                                image.save_render(output_path)
                            else:
                                image.filepath_raw = output_path
                                image.save()
                            if not is_animation:
                                debug_print(f"Saved {pass_suffix}: {os.path.basename(output_path)}")
            # Cleanup
            if external_depth_texture:
                del external_depth_texture
            if external_color_image:
                bpy.data.images.remove(external_color_image)
            frame_time = time.time() - frame_start_time
            debug_print(f"=== FRAME RENDER COMPLETE ===", force=True)
            debug_print(f"Total frame time: {frame_time*1000:.2f}ms")
            if not is_animation:
                debug_print(f"Frame render completed in {frame_time:.2f}s")
            return True
        except Exception as e:
            frame_info = f" (Frame {frame_num})" if frame_num else ""
            debug_print(f"Frame render failed{frame_info}: {e}", force=True)
            if not is_animation:
                import traceback
                debug_print(f"Traceback: {traceback.format_exc()}")
            return False

    def render_animation():
        """Main animation rendering function with multi-pass support and compositing"""
        try:

            def rm_ms(d):
                return d - datetime.timedelta(microseconds=d.microseconds)
            animation_start_time = time.time()
            scene = bpy.context.scene
            user_frame = scene.frame_current
            # Get enabled passes
            enabled_passes = get_enabled_passes()
            if not enabled_passes:
                debug_print("ERROR: No render passes enabled (set RENDER_GAUSSIAN, RENDER_DEPTH, or RENDER_SURFEL to True)", force=True)
                return False
            # Determine frame range
            start_frame = START_FRAME if START_FRAME > 0 else scene.frame_start
            end_frame = END_FRAME if END_FRAME > 0 else scene.frame_end
            frames = list(range(start_frame, end_frame + 1, FRAME_STEP))
            num_frames = len(frames)
            pass_names = [pass_name for pass_name, _, _ in enabled_passes]
            debug_print(f"Starting animation render: {num_frames} frames", force=True)
            debug_print(f"Enabled passes: {', '.join(pass_names)}", force=True)
            debug_print(f"Source updates: Transforms={UPDATE_SOURCE_TRANSFORMS}, Data={REFRESH_EVALUATED_DATA}", force=True)
            debug_print(f"Compositing: USE_TEMP_RENDERS={USE_TEMP_RENDERS}, Depth={USE_EXTERNAL_DEPTH}, Color={USE_EXTERNAL_COLOR}", force=True)
            # Progress tracking
            times = []
            successful_frames = 0
            failed_frames = 0
            for i, frame_num in enumerate(frames):
                render_start_time = time.time()
                try:
                    # Render frame with integration
                    success = render_frame_with_integration(frame_num, is_animation=True)
                    render_time = time.time() - render_start_time
                    times.append(render_time)
                    if success:
                        successful_frames += 1
                        status = "SUCCESS"
                    else:
                        failed_frames += 1
                        status = "FAILED"
                        if not CONTINUE_ON_ERROR:
                            debug_print(f"Stopping animation render due to failure on frame {frame_num}", force=True)
                            break
                    # Calculate time remaining
                    remaining_frames = num_frames - i - 1
                    avg_time = sum(times) / len(times) if times else 0
                    remaining_time = avg_time * remaining_frames
                    print(f"Frame: {frame_num} ({i + 1}/{num_frames}) | Time: {rm_ms(datetime.timedelta(seconds=render_time))} | Remaining: {rm_ms(datetime.timedelta(seconds=remaining_time))} | Status: {status}")
                except Exception as e:
                    failed_frames += 1
                    render_time = time.time() - render_start_time
                    debug_print(f"Frame {frame_num} ({i + 1}/{num_frames}) | EXCEPTION: {str(e)}", force=True)
                    if not CONTINUE_ON_ERROR:
                        debug_print(f"Stopping animation render due to exception on frame {frame_num}", force=True)
                        break
            # Restore original frame
            scene.frame_set(user_frame)
            # Final report
            total_time = time.time() - animation_start_time
            debug_print(f"Animation render completed!", force=True)
            debug_print(f"Total time: {rm_ms(datetime.timedelta(seconds=total_time))}", force=True)
            debug_print(f"Frames successful: {successful_frames}", force=True)
            debug_print(f"Frames failed: {failed_frames}", force=True)
            debug_print(f"Passes enabled: {', '.join(pass_names)}", force=True)
            return successful_frames > 0
        except Exception as e:
            debug_print(f"Animation render failed: {e}", force=True)
            import traceback
            debug_print(f"Traceback: {traceback.format_exc()}")
            return False

    def main_render():
        """Main render function that handles both single frame and animation with multi-pass support and compositing"""
        try:
            # Check that at least one pass is enabled
            enabled_passes = get_enabled_passes()
            if not enabled_passes:
                debug_print("ERROR: No render passes enabled", force=True)
                debug_print("Set at least one of: RENDER_GAUSSIAN, RENDER_DEPTH, RENDER_SURFEL to True", force=True)
                return False
            # Auto-reconstruct dependencies if needed
            debug_print("Checking dependencies...", force=True)
            if not hasattr(bpy, 'gaussian_object_cache') or not bpy.gaussian_object_cache:
                if not auto_reconstruct_cache():
                    debug_print("ERROR: No gaussian objects found - run script_1 first", force=True)
                    return False
            if not auto_reconstruct_shaders():
                debug_print("ERROR: Failed to create/load shaders - check shader paths", force=True)
                return False
            if not auto_reconstruct_textures():
                debug_print("ERROR: Failed to create global textures", force=True)
                return False
            debug_print("Dependencies ready!", force=True)
            debug_print(f"Source updates: Transforms={UPDATE_SOURCE_TRANSFORMS}, Data={REFRESH_EVALUATED_DATA}", force=True)
            debug_print(f"Compositing enabled: {USE_TEMP_RENDERS} (Depth={USE_EXTERNAL_DEPTH}, Color={USE_EXTERNAL_COLOR})", force=True)
            # Route to appropriate render function
            if RENDER_ANIMATION:
                debug_print("Starting ANIMATION render...", force=True)
                return render_animation()
            else:
                debug_print("Starting SINGLE FRAME render...", force=True)
                return render_frame_with_integration()
        except Exception as e:
            debug_print(f"Main render function failed: {e}", force=True)
            import traceback
            debug_print(f"Traceback: {traceback.format_exc()}")
            return False
    # ========== MAIN EXECUTION ==========
    mode = "ANIMATION" if RENDER_ANIMATION else "SINGLE FRAME"
    mode += " WITH EXTERNAL INTEGRATION" if USE_TEMP_RENDERS else ""
    debug_print(f"Starting {mode} render...", force=True)
    debug_print(f"Source object updates enabled: Transforms={UPDATE_SOURCE_TRANSFORMS}, Data={REFRESH_EVALUATED_DATA}", force=True)
    debug_print(f"Compositing settings: Use={USE_TEMP_RENDERS}, Depth={USE_EXTERNAL_DEPTH}, Color={USE_EXTERNAL_COLOR}", force=True)
    debug_print(f"Debug settings: Verbose={DEBUG_VERBOSE}, DataChanges={DEBUG_DATA_CHANGES}, Timing={DEBUG_TIMING}", force=True)
    render_success = main_render()
    if render_success:
        debug_print(f"{mode} render completed successfully!", force=True)
    else:
        debug_print(f"{mode} render failed!", force=True)


def sna_viewport_render_A3941():
    # ========== VARIABLES (EDIT THESE) ==========
    ENABLE_RENDERING = True
    RENDER_MODE = 0  # 0=Gaussian, 1=Depth, 2=Surfel
    SH_DEGREE = 3    # 0, 1, 2, or 3
    SORT_THRESHOLD = 0.05  # Camera movement threshold for re-sorting
    # ============================================
    #import bpy
    #import gpu
    import mathutils

    def auto_reconstruct_cache():
        """Auto-detect and rebuild cache from existing scene objects"""
        try:
            # Find all gaussian objects in the scene
            gaussian_objects = []
            for obj in bpy.data.objects:
                if obj.get("is_gaussian_splat", False):
                    gaussian_objects.append(obj)
            if not gaussian_objects:
                return False
            print(f"Auto-reconstructing cache from {len(gaussian_objects)} scene objects...")
            # Initialize fresh cache
            bpy.gaussian_object_cache = {}
            total_gaussians = 0
            for obj in gaussian_objects:
                try:
                    # Extract data from object properties
                    data_bytes = obj.get("gaussian_data")
                    gaussian_count = obj.get("gaussian_count", 0)
                    sh_degree = obj.get("sh_degree", 48)
                    ply_filepath = obj.get("ply_filepath", "Unknown")
                    if not data_bytes or gaussian_count == 0:
                        continue
                    # Reconstruct numpy array from bytes
                    gaussian_data = np.frombuffer(data_bytes, dtype=np.float32).reshape(gaussian_count, 59)
                    # Add to cache
                    bpy.gaussian_object_cache[obj.name] = {
                        'gaussian_data': gaussian_data,
                        'gaussian_count': gaussian_count,
                        'sh_degree': sh_degree,
                        'object': obj,
                        'ply_filepath': ply_filepath
                    }
                    total_gaussians += gaussian_count
                except Exception as e:
                    print(f"Failed to reconstruct {obj.name}: {e}")
                    continue
            if bpy.gaussian_object_cache:
                # Mark that global textures need rebuilding
                bpy.gaussian_global_needs_update = True
                print(f"Cache auto-reconstructed: {len(bpy.gaussian_object_cache)} objects, {total_gaussians:,} gaussians")
                return True
            else:
                return False
        except Exception as e:
            print(f"Auto-reconstruction failed: {e}")
            return False

    def create_viewport_framebuffer(width, height):
        try:
            if width <= 0 or height <= 0:
                return None
            color_texture = gpu.types.GPUTexture((width, height), format='RGBA8')
            depth_texture = gpu.types.GPUTexture((width, height), format='DEPTH_COMPONENT24')
            framebuffer = gpu.types.GPUFrameBuffer(
                color_slots=[color_texture],
                depth_slot=depth_texture
            )
            return color_texture, depth_texture, framebuffer
        except Exception as e:
            print(f"Failed to create viewport framebuffer: {e}")
            return None

    def read_blender_depth_buffer():
        try:
            fb = gpu.state.active_framebuffer_get()
            viewport = gpu.state.viewport_get()
            width = viewport[2] - viewport[0]
            height = viewport[3] - viewport[1]
            if width <= 0 or height <= 0:
                return None, 0, 0
            depth_buffer = fb.read_depth(0, 0, width, height)
            depth_buffer.dimensions = width * height
            depth_texture = gpu.types.GPUTexture(
                (width, height), 
                format='R32F',
                data=depth_buffer
            )
            return depth_texture, width, height
        except Exception as e:
            return None, 0, 0

    def cleanup_deleted_objects():
        """Remove deleted objects from cache"""
        if not hasattr(bpy, 'gaussian_object_cache'):
            return False
        objects_to_remove = []
        for obj_name in bpy.gaussian_object_cache.keys():
            if obj_name not in bpy.data.objects:
                objects_to_remove.append(obj_name)
        if objects_to_remove:
            for obj_name in objects_to_remove:
                del bpy.gaussian_object_cache[obj_name]
                print(f"Cleaned up deleted object: {obj_name}")
            bpy.gaussian_global_needs_update = True
            return True
        return False

    def check_any_transforms_changed():
        """Check if ANY object has moved - multi-object version"""
        try:
            if not hasattr(bpy, 'gaussian_object_metadata'):
                return False
            if not hasattr(bpy, 'gaussian_last_transforms'):
                bpy.gaussian_last_transforms = {}
            any_changed = False
            for obj_meta in bpy.gaussian_object_metadata:
                obj_name = obj_meta['name']
                obj = obj_meta['object']
                if obj_name not in bpy.data.objects:
                    continue
                current_transform = obj.matrix_world.copy()
                # Check if we've stored this object's transform before
                if obj_name not in bpy.gaussian_last_transforms:
                    bpy.gaussian_last_transforms[obj_name] = current_transform.copy()
                    any_changed = True
                    continue
                last_transform = bpy.gaussian_last_transforms[obj_name]
                # Check for changes
                translation_diff = (current_transform.translation - last_transform.translation).length
                if translation_diff > 0.0001:
                    bpy.gaussian_last_transforms[obj_name] = current_transform.copy()
                    any_changed = True
                    continue
                rotation_diff = current_transform.to_quaternion().rotation_difference(last_transform.to_quaternion()).angle
                if rotation_diff > 0.001:
                    bpy.gaussian_last_transforms[obj_name] = current_transform.copy()
                    any_changed = True
                    continue
                scale_diff = (current_transform.to_scale() - last_transform.to_scale()).length
                if scale_diff > 0.0001:
                    bpy.gaussian_last_transforms[obj_name] = current_transform.copy()
                    any_changed = True
            return any_changed
        except Exception as e:
            print(f"Transform check error: {e}")
            return False

    def update_metadata_texture():
        """Recreate metadata texture with current transforms for all objects"""
        try:
            if not hasattr(bpy, 'gaussian_object_metadata'):
                return False
            num_objects = len(bpy.gaussian_object_metadata)
            floats_per_object = 15
            total_metadata_floats = num_objects * floats_per_object
            max_texture_dim = 16384
            metadata_width = min(max_texture_dim, total_metadata_floats)
            metadata_height = (total_metadata_floats + metadata_width - 1) // metadata_width
            expected_size = metadata_width * metadata_height
            metadata_data = np.zeros(expected_size, dtype=np.float32)
            # Fill metadata with CURRENT transforms for all objects
            for obj_idx, obj_meta in enumerate(bpy.gaussian_object_metadata):
                base_idx = obj_idx * floats_per_object
                obj = obj_meta['object']
                # Start index as uint32 bitcast to float32
                uint32_start_idx = np.uint32(obj_meta['start_idx'])
                metadata_data[base_idx + 0] = uint32_start_idx.view(np.float32)
                metadata_data[base_idx + 1] = float(obj_meta['gaussian_count'])
                metadata_data[base_idx + 2] = 1.0  # Visible
                # CURRENT object transform matrix
                current_transform = obj.matrix_world
                matrix_idx = 0
                for col in range(4):
                    for row in range(3):
                        metadata_data[base_idx + 3 + matrix_idx] = current_transform[row][col]
                        matrix_idx += 1
            # Create new metadata texture
            metadata_buffer = gpu.types.Buffer('FLOAT', len(metadata_data), metadata_data.tolist())
            bpy.gaussian_metadata_texture = gpu.types.GPUTexture(
                (metadata_width, metadata_height), 
                format='R32F', 
                data=metadata_buffer
            )
            return True
        except Exception as e:
            print(f"Metadata update error: {e}")
            return False

    def update_depth_sorting():
        """Global depth sorting for all objects combined"""
        try:
            if not hasattr(bpy, 'gaussian_object_metadata'):
                return False
            view_matrix = gpu.matrix.get_model_view_matrix()
            # NEW: Check if forced depth sort is requested by script_3
            force_sort = getattr(bpy, 'gaussian_needs_depth_sort', False)
            # Check if camera moved enough to require re-sorting
            update_needed = force_sort  # Start with force flag
            if not force_sort and hasattr(bpy, 'gaussian_last_camera_pos'):
                last_pos = bpy.gaussian_last_camera_pos
                current_pos = [view_matrix[0][3], view_matrix[1][3], view_matrix[2][3]]
                movement = sum((a-b)**2 for a,b in zip(last_pos, current_pos))**0.5
                update_needed = movement > SORT_THRESHOLD
            elif not force_sort:
                update_needed = True  # First time, no stored camera position
            if update_needed:
                # Clear the force sort flag if it was set
                if force_sort:
                    bpy.gaussian_needs_depth_sort = False
                    print("Forced depth sort triggered by script_3")
                # Collect all positions from all objects
                all_camera_positions = []
                view_matrix_np = np.array(view_matrix, dtype=np.float32)
                for obj_meta in bpy.gaussian_object_metadata:
                    obj = obj_meta['object']
                    obj_name = obj_meta['name']
                    if obj_name not in bpy.gaussian_object_cache:
                        continue
                    # Get gaussian data for this object
                    gaussian_data = bpy.gaussian_object_cache[obj_name]['gaussian_data']
                    positions = gaussian_data[:, 0:3]
                    # Transform to camera space using current object transform
                    object_transform_np = np.array(obj.matrix_world, dtype=np.float32)
                    combined_transform = view_matrix_np @ object_transform_np
                    positions_homogeneous = np.ones((len(positions), 4), dtype=np.float32)
                    positions_homogeneous[:, 0:3] = positions
                    camera_positions = positions_homogeneous @ combined_transform.T
                    all_camera_positions.append(camera_positions[:, 0:3])
                if not all_camera_positions:
                    return False
                # Merge all camera positions
                merged_camera_positions = np.concatenate(all_camera_positions, axis=0)
                depths = merged_camera_positions[:, 2]
                # Sort depths
                depths_min = np.min(depths)
                depths_max = np.max(depths)
                depth_range = depths_max - depths_min
                if depth_range > 0:
                    depths_normalized = (depths - depths_min) / depth_range
                    scale_factor = np.float64(np.iinfo(np.uint32).max) - 1.0
                    depths_scaled = depths_normalized * scale_factor
                    depths_uint32 = depths_scaled.astype(np.uint32)
                else:
                    depths_uint32 = np.zeros_like(depths, dtype=np.uint32)
                sorted_indices = np.argsort(depths_uint32, kind='stable').astype(np.float32)
                # Update indices texture
                if hasattr(bpy, 'gaussian_indices_texture'):
                    indices_width = bpy.gaussian_indices_width
                    indices_height = bpy.gaussian_indices_height
                    expected_size = indices_width * indices_height
                    if len(sorted_indices) < expected_size:
                        padded_indices = np.zeros(expected_size, dtype=np.float32)
                        padded_indices[:len(sorted_indices)] = sorted_indices
                        indices_data = padded_indices
                    else:
                        indices_data = sorted_indices
                    indices_buffer = gpu.types.Buffer('FLOAT', len(indices_data), indices_data.tolist())
                    bpy.gaussian_indices_texture = gpu.types.GPUTexture(
                        (indices_width, indices_height),
                        format='R32F',
                        data=indices_buffer
                    )
                bpy.gaussian_last_camera_pos = [view_matrix[0][3], view_matrix[1][3], view_matrix[2][3]]
                return True
            return False
        except Exception as e:
            print(f"Global depth sorting error: {e}")
            return False

    def draw_gaussians():
        """Multi-object rendering with automatic cache reconstruction"""
        try:
            # ========== AUTO-RECONSTRUCTION CHECK ==========
            cache_needs_rebuild = False
            # Check if cache exists and has objects
            if not hasattr(bpy, 'gaussian_object_cache') or not bpy.gaussian_object_cache:
                cache_needs_rebuild = auto_reconstruct_cache()
                if not cache_needs_rebuild:
                    return  # No gaussian objects found
            else:
                # Clean up any deleted objects
                cleanup_deleted_objects()
            # Check if global textures need rebuilding (after file load or new objects)
            if not hasattr(bpy, 'gaussian_texture') or getattr(bpy, 'gaussian_global_needs_update', False):
                print("Global textures missing - run script_3 first")
                return
            # ========== STANDARD RENDERING CHECKS ==========
            required_attrs = [
                'gaussian_quad_shader', 'gaussian_quad_batch', 'gaussian_composite_shader', 
                'gaussian_composite_batch', 'gaussian_texture', 'gaussian_indices_texture', 'gaussian_count'
            ]
            for attr in required_attrs:
                if not hasattr(bpy, attr):
                    print(f"Missing {attr} - run scripts 2 and 3 first")
                    return
            # Check if any object transforms changed
            transforms_changed = check_any_transforms_changed()
            # Update metadata texture if any object moved
            if transforms_changed:
                update_metadata_texture()
            # Update global depth sorting
            sorting_updated = update_depth_sorting()
            viewport = gpu.state.viewport_get()
            viewport_width = viewport[2] - viewport[0]
            viewport_height = viewport[3] - viewport[1]
            if viewport_width <= 0 or viewport_height <= 0:
                return
            # Create/update framebuffer
            fb_needs_update = (
                not hasattr(bpy, 'gaussian_persistent_fb') or 
                not hasattr(bpy, 'gaussian_fb_width') or 
                bpy.gaussian_fb_width != viewport_width or 
                bpy.gaussian_fb_height != viewport_height
            )
            if fb_needs_update:
                if hasattr(bpy, 'gaussian_persistent_fb'):
                    try:
                        color_tex, depth_tex, fb = bpy.gaussian_persistent_fb
                        del fb, depth_tex, color_tex
                    except:
                        pass
                fb_result = create_viewport_framebuffer(viewport_width, viewport_height)
                if not fb_result:
                    return
                bpy.gaussian_persistent_fb = fb_result
                bpy.gaussian_fb_width = viewport_width
                bpy.gaussian_fb_height = viewport_height
            color_texture, depth_texture, framebuffer = bpy.gaussian_persistent_fb
            blender_depth_texture, depth_width, depth_height = read_blender_depth_buffer()
            if not blender_depth_texture:
                return
            # ========== STAGE 1: RENDER ALL GAUSSIANS ==========
            with framebuffer.bind():
                fb = gpu.state.active_framebuffer_get()
                fb.clear(color=(0.0, 0.0, 0.0, 0.0), depth=1.0)
                view_matrix = gpu.matrix.get_model_view_matrix()
                proj_matrix = gpu.matrix.get_projection_matrix()
                fy = proj_matrix[1][1]
                fov_y = 2 * math.atan(1.0 / fy)
                tan_half_fovy = math.tan(fov_y * 0.5)
                aspect_ratio = viewport_width / viewport_height
                tan_half_fovx = tan_half_fovy * aspect_ratio
                focal = viewport_height / (2.0 * tan_half_fovy)
                camera_pos = mathutils.Vector((view_matrix[0][3], view_matrix[1][3], view_matrix[2][3]))
                gpu.state.depth_test_set('NONE')
                gpu.state.depth_mask_set(False) 
                gpu.state.blend_set('ALPHA')
                gpu.state.program_point_size_set(False)
                bpy.gaussian_quad_shader.bind()
                bpy.gaussian_quad_shader.uniform_float("ViewMatrix", view_matrix)
                bpy.gaussian_quad_shader.uniform_float("ProjectionMatrix", proj_matrix)
                bpy.gaussian_quad_shader.uniform_float("focal_parameters", (tan_half_fovx, tan_half_fovy, focal))
                bpy.gaussian_quad_shader.uniform_float("camera_position", camera_pos)
                bpy.gaussian_quad_shader.uniform_int("render_mode", RENDER_MODE)
                bpy.gaussian_quad_shader.uniform_int("sh_degree", SH_DEGREE)
                if hasattr(bpy, 'gaussian_texture_width'):
                    bpy.gaussian_quad_shader.uniform_float("texture_dimensions", 
                                                          (bpy.gaussian_texture_width, bpy.gaussian_texture_height))
                if hasattr(bpy, 'gaussian_indices_width'):
                    bpy.gaussian_quad_shader.uniform_float("indices_dimensions", 
                                                          (bpy.gaussian_indices_width, bpy.gaussian_indices_height))
                if depth_width > 0 and depth_height > 0:
                    bpy.gaussian_quad_shader.uniform_float("depth_texture_size", (depth_width, depth_height))
                # Bind textures (metadata now contains all object transforms)
                bpy.gaussian_quad_shader.uniform_sampler("gaussian_data", bpy.gaussian_texture)
                bpy.gaussian_quad_shader.uniform_sampler("sorted_indices", bpy.gaussian_indices_texture)
                bpy.gaussian_quad_shader.uniform_sampler("blender_depth", blender_depth_texture)
                bpy.gaussian_quad_shader.uniform_sampler("object_metadata", bpy.gaussian_metadata_texture)
                # Draw all gaussians from all objects
                bpy.gaussian_quad_batch.draw_instanced(bpy.gaussian_quad_shader, instance_count=bpy.gaussian_count)
            # ========== STAGE 2: COMPOSITE TO VIEWPORT ==========
            gpu.state.blend_set('ALPHA')
            gpu.state.depth_test_set('NONE') 
            gpu.state.depth_mask_set(False)
            bpy.gaussian_composite_shader.bind()
            bpy.gaussian_composite_shader.uniform_sampler("image", color_texture)
            bpy.gaussian_composite_batch.draw(bpy.gaussian_composite_shader)
            gpu.state.blend_set('NONE')
            gpu.state.program_point_size_set(False)
        except Exception as e:
            print(f"Multi-object render error: {e}")
            import traceback
            traceback.print_exc()
    # Remove existing handler
    if hasattr(bpy, 'gaussian_draw_handle'):
        try:
            bpy.types.SpaceView3D.draw_handler_remove(bpy.gaussian_draw_handle, 'WINDOW')
            delattr(bpy, 'gaussian_draw_handle')
        except:
            pass
    if ENABLE_RENDERING:
        handle = bpy.types.SpaceView3D.draw_handler_add(draw_gaussians, (), 'WINDOW', 'POST_VIEW')
        bpy.gaussian_draw_handle = handle
        print("Auto-reconstructing multi-object gaussian pipeline enabled")
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
    else:
        print("Multi-object renderer disabled")


def sna_texture_creation_FD1B2():
    # ========== VARIABLES (EDIT THESE) ==========
    # No variables needed - builds from all cached objects
    # ============================================
    #import bpy
    #import gpu
    #import os
    # ========== FALLBACK FUNCTIONS FOR CORRUPTED DATA ==========

    def extract_attribute_data(mesh_data, attr_name):
        """Extract data from mesh attribute by name - optimized version"""
        if attr_name not in [attr.name for attr in mesh_data.attributes]:
            return None
        attr = mesh_data.attributes[attr_name]
        # Use foreach_get for much faster extraction
        data_array = np.zeros(len(attr.data), dtype=np.float32)
        attr.data.foreach_get("value", data_array)
        return data_array

    def extract_gaussian_data_from_evaluated_mesh(mesh_obj):
        """Extract and process gaussian data from EVALUATED mesh object attributes"""
        # Get evaluated mesh data
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated_object = mesh_obj.evaluated_get(depsgraph)
        evaluated_mesh = evaluated_object.data
        # Extract positions from evaluated vertices - optimized version
        num_points = len(evaluated_mesh.vertices)
        if num_points == 0:
            raise ValueError("Evaluated mesh has no vertices")
        # Use foreach_get for fast vertex coordinate extraction
        positions = np.zeros(num_points * 3, dtype=np.float32)
        evaluated_mesh.vertices.foreach_get("co", positions)
        positions = positions.reshape(-1, 3)
        # Get available attributes from evaluated mesh
        available_attrs = [attr.name for attr in evaluated_mesh.attributes]
        # Extract spherical harmonics from evaluated mesh
        if all(attr in available_attrs for attr in ['f_dc_0', 'f_dc_1', 'f_dc_2']):
            dc_0 = extract_attribute_data(evaluated_mesh, 'f_dc_0')
            dc_1 = extract_attribute_data(evaluated_mesh, 'f_dc_1')
            dc_2 = extract_attribute_data(evaluated_mesh, 'f_dc_2')
            features_dc = np.column_stack([dc_0, dc_1, dc_2])
            # Find f_rest fields
            f_rest_fields = [attr for attr in available_attrs if attr.startswith('f_rest_')]
            f_rest_fields = sorted(f_rest_fields, key=lambda x: int(x.split('_')[-1]))
            if f_rest_fields:
                features_extra_list = []
                for field in f_rest_fields:
                    data = extract_attribute_data(evaluated_mesh, field)
                    if data is not None:
                        features_extra_list.append(data)
                if features_extra_list:
                    features_extra = np.column_stack(features_extra_list)
                    num_f_rest = len(f_rest_fields)
                    # Determine degree and coefficients to use
                    if num_f_rest >= 45:
                        actual_degree = 3
                        coeffs_to_use = 45
                    elif num_f_rest >= 24:
                        actual_degree = 2  
                        coeffs_to_use = 24
                    elif num_f_rest >= 9:
                        actual_degree = 1
                        coeffs_to_use = 9
                    else:
                        actual_degree = 0
                        coeffs_to_use = 0
                    if coeffs_to_use > 0:
                        features_extra_used = features_extra[:, :coeffs_to_use]
                        coeffs_per_degree = (actual_degree + 1) ** 2 - 1
                        features_extra_reshaped = features_extra_used.reshape((num_points, 3, coeffs_per_degree))
                        features_extra_reshaped = np.transpose(features_extra_reshaped, [0, 2, 1])
                        features_dc_reshaped = features_dc.reshape(-1, 1, 3)
                        all_features = np.concatenate([features_dc_reshaped, features_extra_reshaped], axis=1)
                        sh_coeffs = all_features.reshape(num_points, -1)
                    else:
                        sh_coeffs = features_dc
                else:
                    sh_coeffs = features_dc
            else:
                sh_coeffs = features_dc
        else:
            # Default SH coeffs if not found
            print(f"Warning: f_dc attributes not found on evaluated mesh, using defaults")
            sh_coeffs = np.ones((num_points, 3)) * 0.28209479177387814
        # Extract scales from evaluated mesh
        if all(attr in available_attrs for attr in ['scale_0', 'scale_1', 'scale_2']):
            scale_0 = extract_attribute_data(evaluated_mesh, 'scale_0')
            scale_1 = extract_attribute_data(evaluated_mesh, 'scale_1')
            scale_2 = extract_attribute_data(evaluated_mesh, 'scale_2')
            scales = np.column_stack([scale_0, scale_1, scale_2])
            scales = np.exp(scales)  # Apply exponential
        else:
            print(f"Warning: scale attributes not found on evaluated mesh, using defaults")
            scales = np.ones((num_points, 3)) * 0.01
        # Extract rotations from evaluated mesh
        if all(attr in available_attrs for attr in ['rot_0', 'rot_1', 'rot_2', 'rot_3']):
            rot_0 = extract_attribute_data(evaluated_mesh, 'rot_0')
            rot_1 = extract_attribute_data(evaluated_mesh, 'rot_1')
            rot_2 = extract_attribute_data(evaluated_mesh, 'rot_2')
            rot_3 = extract_attribute_data(evaluated_mesh, 'rot_3')
            rotations = np.column_stack([rot_0, rot_1, rot_2, rot_3])
            # Normalize quaternions
            norms = np.linalg.norm(rotations, axis=1, keepdims=True)
            rotations = rotations / norms
        else:
            print(f"Warning: rotation attributes not found on evaluated mesh, using defaults")
            rotations = np.zeros((num_points, 4))
            rotations[:, 0] = 1.0  # Identity quaternion
        # Extract opacity from evaluated mesh
        if 'opacity' in available_attrs:
            opacity_raw = extract_attribute_data(evaluated_mesh, 'opacity')
            opacity = 1.0 / (1.0 + np.exp(-opacity_raw))  # Apply sigmoid
        else:
            print(f"Warning: opacity attribute not found on evaluated mesh, using defaults")
            opacity = np.ones(num_points)
        return {
            'num_points': num_points,
            'positions': positions,
            'scales': scales,
            'rotations': rotations,
            'opacities': opacity,
            'sh_coeffs': sh_coeffs,
            'sh_dim': sh_coeffs.shape[1]
        }

    def find_source_object_by_uuid(source_uuid):
        """Find Blender object by gaussian_source_uuid"""
        for obj in bpy.data.objects:
            if obj.get("gaussian_source_uuid") == source_uuid:
                return obj
        return None

    def check_mesh_has_gaussian_attributes(mesh_obj):
        """Check if mesh object has basic gaussian attributes"""
        if not mesh_obj or not mesh_obj.data:
            return False
        # Check for basic gaussian attributes
        required_attrs = ['f_dc_0', 'f_dc_1', 'f_dc_2']
        available_attrs = [attr.name for attr in mesh_obj.data.attributes]
        return all(attr in available_attrs for attr in required_attrs)

    def refresh_object_from_blender_source(obj):
        """Refresh gaussian data from Blender mesh source - fallback function"""
        try:
            source_uuid = obj.get("source_mesh_uuid")
            if not source_uuid:
                return False, "No source UUID found"
            # Find source object by UUID
            source_obj = find_source_object_by_uuid(source_uuid)
            if not source_obj:
                return False, f"Source object with UUID {source_uuid} not found"
            # Validate that source object has gaussian attributes
            if not check_mesh_has_gaussian_attributes(source_obj):
                return False, f"Source object '{source_obj.name}' missing gaussian attributes"
            print(f"  🔄 Fallback: Refreshing {obj.name} from source mesh {source_obj.name}")
            # Extract fresh data from evaluated mesh
            gaussian_data_info = extract_gaussian_data_from_evaluated_mesh(source_obj)
            # Create gaussian data array (59 floats per gaussian)
            num_gaussians = gaussian_data_info['num_points']
            sh_dim = 48
            total_dim = 3 + 4 + 3 + 1 + sh_dim
            gaussian_data = np.zeros((num_gaussians, total_dim), dtype=np.float32)
            # Pack data in original order
            gaussian_data[:, 0:3] = gaussian_data_info['positions']
            gaussian_data[:, 3:7] = gaussian_data_info['rotations']
            gaussian_data[:, 7:10] = gaussian_data_info['scales']
            gaussian_data[:, 10] = gaussian_data_info['opacities'].flatten()
            # Handle SH coefficients
            source_sh_coeffs = gaussian_data_info['sh_coeffs']
            if source_sh_coeffs.shape[1] >= sh_dim:
                gaussian_data[:, 11:11+sh_dim] = source_sh_coeffs[:, :sh_dim]
            else:
                gaussian_data[:, 11:11+source_sh_coeffs.shape[1]] = source_sh_coeffs
            # Update object properties with fresh data
            obj["gaussian_data"] = gaussian_data.tobytes()
            obj["gaussian_count"] = num_gaussians
            obj["sh_degree"] = gaussian_data_info['sh_dim']
            obj["last_load_time"] = time.time()
            return True, (gaussian_data, num_gaussians, gaussian_data_info['sh_dim'])
        except Exception as e:
            return False, f"Fallback refresh failed: {e}"

    def refresh_object_from_ply_source(obj):
        """Refresh gaussian data from PLY file - fallback function"""
        try:
            ply_filepath = obj.get("ply_filepath")
            if not ply_filepath or not os.path.exists(ply_filepath):
                return False, "PLY file not found or missing path"
            print(f"  🔄 Fallback: Refreshing {obj.name} from PLY {os.path.basename(ply_filepath)}")
            # Simple PLY loading (minimal implementation for fallback)
            from plyfile import PlyData
            plydata = PlyData.read(ply_filepath)
            vertex_element = plydata.elements[0]
            vertex_data = vertex_element.data
            available_fields = list(vertex_data.dtype.names)
            # Extract positions
            if 'x' in available_fields and 'y' in available_fields and 'z' in available_fields:
                positions = np.column_stack([vertex_data['x'], vertex_data['y'], vertex_data['z']])
                positions = np.ascontiguousarray(positions).astype(np.float32)
            else:
                return False, "PLY missing position coordinates"
            num_points = len(positions)
            # Extract SH coefficients (simplified)
            if all(attr in available_fields for attr in ['f_dc_0', 'f_dc_1', 'f_dc_2']):
                dc_0 = vertex_data['f_dc_0']
                dc_1 = vertex_data['f_dc_1'] 
                dc_2 = vertex_data['f_dc_2']
                sh_coeffs = np.column_stack([dc_0, dc_1, dc_2]).astype(np.float32)
            else:
                sh_coeffs = np.ones((num_points, 3), dtype=np.float32) * 0.28209479177387814
            # Extract scales
            if all(attr in available_fields for attr in ['scale_0', 'scale_1', 'scale_2']):
                scale_0 = vertex_data['scale_0']
                scale_1 = vertex_data['scale_1']
                scale_2 = vertex_data['scale_2']
                scales = np.column_stack([scale_0, scale_1, scale_2])
                scales = np.exp(scales).astype(np.float32)
            else:
                scales = np.ones((num_points, 3), dtype=np.float32) * 0.01
            # Extract rotations
            if all(attr in available_fields for attr in ['rot_0', 'rot_1', 'rot_2', 'rot_3']):
                rot_0 = vertex_data['rot_0']
                rot_1 = vertex_data['rot_1']
                rot_2 = vertex_data['rot_2']
                rot_3 = vertex_data['rot_3']
                rotations = np.column_stack([rot_0, rot_1, rot_2, rot_3])
                norms = np.linalg.norm(rotations, axis=1, keepdims=True)
                rotations = (rotations / norms).astype(np.float32)
            else:
                rotations = np.zeros((num_points, 4), dtype=np.float32)
                rotations[:, 0] = 1.0
            # Extract opacity
            if 'opacity' in available_fields:
                opacity = vertex_data['opacity']
                opacity = (1.0 / (1.0 + np.exp(-opacity))).astype(np.float32)
            else:
                opacity = np.ones(num_points, dtype=np.float32)
            # Create gaussian data array
            sh_dim = 48
            total_dim = 3 + 4 + 3 + 1 + sh_dim
            gaussian_data = np.zeros((num_points, total_dim), dtype=np.float32)
            # Pack data
            gaussian_data[:, 0:3] = positions
            gaussian_data[:, 3:7] = rotations
            gaussian_data[:, 7:10] = scales
            gaussian_data[:, 10] = opacity.flatten()
            if sh_coeffs.shape[1] >= sh_dim:
                gaussian_data[:, 11:11+sh_dim] = sh_coeffs[:, :sh_dim]
            else:
                gaussian_data[:, 11:11+sh_coeffs.shape[1]] = sh_coeffs
            # Update object properties
            obj["gaussian_data"] = gaussian_data.tobytes()
            obj["gaussian_count"] = num_points
            obj["sh_degree"] = sh_coeffs.shape[1]
            obj["last_load_time"] = time.time()
            return True, (gaussian_data, num_points, sh_coeffs.shape[1])
        except Exception as e:
            return False, f"PLY fallback failed: {e}"

    def auto_reconstruct_cache_for_script3():
        """Auto-reconstruct cache from scene objects with fallback for corrupted data"""
        try:
            # Find all gaussian objects in the scene
            gaussian_objects = []
            for obj in bpy.data.objects:
                if obj.get("is_gaussian_splat", False):
                    gaussian_objects.append(obj)
            if not gaussian_objects:
                return False
            print(f"Auto-reconstructing cache from {len(gaussian_objects)} scene objects...")
            # Initialize fresh cache
            bpy.gaussian_object_cache = {}
            total_gaussians = 0
            fallback_count = 0
            for obj in gaussian_objects:
                try:
                    # Extract data from object properties
                    data_bytes = obj.get("gaussian_data")
                    gaussian_count = obj.get("gaussian_count", 0)
                    sh_degree = obj.get("sh_degree", 48)
                    ply_filepath = obj.get("ply_filepath", "")
                    if not data_bytes or gaussian_count == 0:
                        print(f"  ⚠️  {obj.name}: Missing data or zero count, skipping")
                        continue
                    # Try to reconstruct numpy array from bytes
                    try:
                        gaussian_data = np.frombuffer(data_bytes, dtype=np.float32).reshape(gaussian_count, 59)
                        # Validate data integrity
                        if gaussian_data.shape != (gaussian_count, 59):
                            raise ValueError("Data shape validation failed")
                        # Check for reasonable values (basic sanity check)
                        if np.any(np.isnan(gaussian_data)) or np.any(np.isinf(gaussian_data)):
                            raise ValueError("Data contains NaN or infinity values")
                        print(f"  ✅ {obj.name}: Successfully reconstructed from cache")
                    except (ValueError, TypeError) as e:
                        print(f"  ❌ {obj.name}: Cache data corrupted ({e})")
                        print(f"     Attempting fallback refresh...")
                        # Determine source type and attempt fallback
                        is_blender_source = obj.get("source_mesh_uuid") is not None
                        is_ply_source = ply_filepath and ply_filepath.strip()
                        fallback_success = False
                        if is_blender_source:
                            success, result = refresh_object_from_blender_source(obj)
                            if success:
                                gaussian_data, gaussian_count, sh_degree = result
                                fallback_success = True
                                fallback_count += 1
                            else:
                                print(f"     Blender source fallback failed: {result}")
                        elif is_ply_source:
                            success, result = refresh_object_from_ply_source(obj)
                            if success:
                                gaussian_data, gaussian_count, sh_degree = result
                                fallback_success = True
                                fallback_count += 1
                            else:
                                print(f"     PLY source fallback failed: {result}")
                        if not fallback_success:
                            print(f"     All fallback methods failed for {obj.name}, skipping")
                            continue
                    # Add to cache
                    source_info = ""
                    if obj.get("source_mesh_uuid"):
                        source_info = f"Mesh:{obj.get('source_mesh_name', 'Unknown')}"
                    elif ply_filepath:
                        source_info = f"PLY:{os.path.basename(ply_filepath)}"
                    bpy.gaussian_object_cache[obj.name] = {
                        'gaussian_data': gaussian_data,
                        'gaussian_count': gaussian_count,
                        'sh_degree': sh_degree,
                        'object': obj,
                        'ply_filepath': ply_filepath,
                        'source_info': source_info
                    }
                    total_gaussians += gaussian_count
                except Exception as e:
                    print(f"  ❌ {obj.name}: Reconstruction failed completely: {e}")
                    continue
            if bpy.gaussian_object_cache:
                cache_status = f"Cache reconstructed: {len(bpy.gaussian_object_cache)} objects, {total_gaussians:,} gaussians"
                if fallback_count > 0:
                    cache_status += f" ({fallback_count} restored from source)"
                print(cache_status)
                return True
            else:
                return False
        except Exception as e:
            print(f"Auto-reconstruction failed: {e}")
            return False
    # ========== MAIN SCRIPT ==========
    try:
        # ========== AUTO-RECONSTRUCTION CHECK ==========
        # Check if we have cached objects, if not try to reconstruct
        if not hasattr(bpy, 'gaussian_object_cache') or not bpy.gaussian_object_cache:
            reconstruction_success = auto_reconstruct_cache_for_script3()
            if not reconstruction_success:
                raise ValueError("No gaussian objects found in scene - run script_1 first")
        print(f"Building global textures from {len(bpy.gaussian_object_cache)} objects:")
        # ========== MERGE DATA FROM ALL OBJECTS ==========
        all_gaussian_data = []
        all_object_metadata = []
        current_start_idx = 0
        for obj_name, obj_data in bpy.gaussian_object_cache.items():
            gaussian_data = obj_data['gaussian_data']
            gaussian_count = obj_data['gaussian_count']
            obj = obj_data['object']
            source_info = obj_data.get('source_info', 'Unknown')
            print(f"  - {obj_name}: {gaussian_count:,} gaussians ({source_info})")
            # Add to merged data
            all_gaussian_data.append(gaussian_data)
            # Store metadata for this object
            all_object_metadata.append({
                'name': obj_name,
                'start_idx': current_start_idx,
                'gaussian_count': gaussian_count,
                'object': obj
            })
            current_start_idx += gaussian_count
        # Merge all gaussian data into single array
        merged_gaussian_data = np.concatenate(all_gaussian_data, axis=0)
        total_gaussians = len(merged_gaussian_data)
        print(f"Total merged gaussians: {total_gaussians:,}")
        # ========== CREATE GLOBAL 3D GAUSSIAN TEXTURE ==========
        total_floats = merged_gaussian_data.size
        max_texture_dim = 16384
        # Calculate 3D texture dimensions using original method
        cube_root = int(np.ceil(np.power(total_floats, 1/3)))
        texture_depth = min(max_texture_dim, cube_root)
        texture_area = (total_floats + texture_depth - 1) // texture_depth
        texture_width = min(max_texture_dim, int(np.ceil(np.sqrt(texture_area))))
        texture_height = (texture_area + texture_width - 1) // texture_width
        # Pad data if needed
        flat_data = merged_gaussian_data.flatten()
        expected_size = texture_width * texture_height * texture_depth
        if len(flat_data) < expected_size:
            padded_data = np.zeros(expected_size, dtype=np.float32)
            padded_data[:len(flat_data)] = flat_data
            flat_data = padded_data
        # Create 3D texture
        buffer = gpu.types.Buffer('FLOAT', len(flat_data), flat_data.tolist())
        gaussian_texture = gpu.types.GPUTexture(
            (texture_width, texture_height, texture_depth), 
            format='R32F',
            data=buffer
        )
        # ========== CREATE GLOBAL INDICES TEXTURE ==========
        sorted_indices = np.arange(total_gaussians, dtype=np.float32)
        indices_width = min(max_texture_dim, len(sorted_indices))
        indices_height = (len(sorted_indices) + indices_width - 1) // indices_width
        expected_indices_size = indices_width * indices_height
        if len(sorted_indices) < expected_indices_size:
            padded_indices = np.zeros(expected_indices_size, dtype=np.float32)
            padded_indices[:len(sorted_indices)] = sorted_indices
            indices_data = padded_indices
        else:
            indices_data = sorted_indices
        indices_buffer = gpu.types.Buffer('FLOAT', len(indices_data), indices_data.tolist())
        indices_texture = gpu.types.GPUTexture(
            (indices_width, indices_height),
            format='R32F',
            data=indices_buffer
        )
        # ========== CREATE MULTI-OBJECT METADATA TEXTURE ==========
        num_objects = len(all_object_metadata)
        floats_per_object = 15
        total_metadata_floats = num_objects * floats_per_object
        metadata_width = min(max_texture_dim, total_metadata_floats)
        metadata_height = (total_metadata_floats + metadata_width - 1) // metadata_width
        expected_size = metadata_width * metadata_height
        metadata_data = np.zeros(expected_size, dtype=np.float32)
        # Fill metadata for each object
        for obj_idx, obj_meta in enumerate(all_object_metadata):
            base_idx = obj_idx * floats_per_object
            # Start index (uint32 bitcast to float32)
            uint32_start_idx = np.uint32(obj_meta['start_idx'])
            metadata_data[base_idx + 0] = uint32_start_idx.view(np.float32)
            metadata_data[base_idx + 1] = float(obj_meta['gaussian_count'])
            metadata_data[base_idx + 2] = 1.0  # Visible
            # Object transform matrix (3x4 = 12 floats)
            transform = obj_meta['object'].matrix_world
            matrix_idx = 0
            for col in range(4):
                for row in range(3):
                    metadata_data[base_idx + 3 + matrix_idx] = transform[row][col]
                    matrix_idx += 1
        metadata_buffer = gpu.types.Buffer('FLOAT', len(metadata_data), metadata_data.tolist())
        metadata_texture = gpu.types.GPUTexture(
            (metadata_width, metadata_height), 
            format='R32F', 
            data=metadata_buffer
        )
        # ========== STORE GLOBALLY ==========
        bpy.gaussian_texture = gaussian_texture
        bpy.gaussian_texture_width = texture_width
        bpy.gaussian_texture_height = texture_height
        bpy.gaussian_texture_depth = texture_depth
        bpy.gaussian_indices_texture = indices_texture
        bpy.gaussian_indices_width = indices_width
        bpy.gaussian_indices_height = indices_height
        bpy.gaussian_metadata_texture = metadata_texture
        bpy.gaussian_count = total_gaussians
        bpy.gaussian_object_metadata = all_object_metadata  # For transform tracking
        bpy.gaussian_global_needs_update = False  # Mark as updated
        bpy.gaussian_needs_depth_sort = True  # NEW: Signal viewport renderer to force depth sort
        print(f"Global textures created:")
        print(f"  Gaussian: {texture_width}x{texture_height}x{texture_depth}")
        print(f"  Indices: {indices_width}x{indices_height}")
        print(f"  Metadata: {metadata_width}x{metadata_height} for {num_objects} objects")
        print(f"  Depth sort flagged for next viewport render")
    except Exception as e:
        print(f"Error creating global textures: {e}")
        import traceback
        traceback.print_exc()


def sna_shader_system_A4AED():
    VERTEX_SHADER_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'vert.glsl')
    FRAGMENT_SHADER_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'frag.glsl')
    COMPOSITE_VERTEX_SHADER_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'composite_vert.glsl')
    COMPOSITE_FRAGMENT_SHADER_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'composite_frag.glsl')
    # ========== VARIABLES (EDIT THESE) ==========
    #VERTEX_SHADER_PATH = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders\vert.glsl"
    #FRAGMENT_SHADER_PATH = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders\frag.glsl"
    #COMPOSITE_VERTEX_SHADER_PATH = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders\composite_vert.glsl"
    #COMPOSITE_FRAGMENT_SHADER_PATH = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders\composite_frag.glsl"
    MAX_GAUSSIANS = 1000000
    # ============================================
    #import bpy
    import gpu.types
    import numpy as np

    def read_shader_file(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"Error reading shader file {filepath}: {e}")
            return None
    try:
        # ========== CLEANUP EXISTING SHADERS ==========
        print("Cleaning up existing shader resources...")
        cleanup_attrs = [
            'gaussian_quad_shader', 'gaussian_quad_batch', 
            'gaussian_composite_shader', 'gaussian_composite_batch'
        ]
        for attr in cleanup_attrs:
            if hasattr(bpy, attr):
                delattr(bpy, attr)
        # Check shader files exist
        shader_files = [VERTEX_SHADER_PATH, FRAGMENT_SHADER_PATH, 
                       COMPOSITE_VERTEX_SHADER_PATH, COMPOSITE_FRAGMENT_SHADER_PATH]
        for shader_file in shader_files:
            if not os.path.exists(shader_file):
                raise FileNotFoundError(f"Shader not found: {shader_file}")
        # Read shader sources
        vertex_source = read_shader_file(VERTEX_SHADER_PATH)
        fragment_source = read_shader_file(FRAGMENT_SHADER_PATH)
        composite_vertex_source = read_shader_file(COMPOSITE_VERTEX_SHADER_PATH)
        composite_fragment_source = read_shader_file(COMPOSITE_FRAGMENT_SHADER_PATH)
        if not all([vertex_source, fragment_source, composite_vertex_source, composite_fragment_source]):
            raise ValueError("Failed to read shader files")
        print("Loaded all shader files successfully")
        # ========== CREATE MAIN GAUSSIAN SHADER ==========
        shader_info = gpu.types.GPUShaderCreateInfo()
        # Vertex inputs
        shader_info.vertex_in(0, 'VEC2', "quad_coord")
        # Push constants
        shader_info.push_constant("MAT4", "ViewMatrix")
        shader_info.push_constant("MAT4", "ProjectionMatrix") 
        shader_info.push_constant("VEC3", "focal_parameters")
        shader_info.push_constant("VEC3", "camera_position")
        shader_info.push_constant("INT", "render_mode")
        shader_info.push_constant("INT", "sh_degree")
        shader_info.push_constant("VEC2", "texture_dimensions")
        shader_info.push_constant("VEC2", "indices_dimensions")
        shader_info.push_constant("VEC2", "depth_texture_size")
        # Samplers
        shader_info.sampler(0, 'FLOAT_3D', "gaussian_data")
        shader_info.sampler(1, 'FLOAT_2D', "sorted_indices")
        shader_info.sampler(2, 'FLOAT_2D', "blender_depth")
        shader_info.sampler(3, 'FLOAT_2D', "object_metadata")
        # Interface
        interface = gpu.types.GPUStageInterfaceInfo("splat_forge_quad_interface")
        interface.smooth('VEC3', "v_color")
        interface.smooth('VEC3', "v_conic")
        interface.smooth('VEC2', "v_coordxy")
        interface.smooth('FLOAT', "v_alpha")
        interface.smooth('VEC4', "v_rotation")
        interface.flat('INT', "v_render_mode")
        interface.smooth('FLOAT', "v_depth")
        shader_info.vertex_out(interface)
        shader_info.fragment_out(0, 'VEC4', 'fragColor')
        shader_info.vertex_source(vertex_source)
        shader_info.fragment_source(fragment_source)
        # Create main shader
        quad_shader = gpu.shader.create_from_info(shader_info)
        del interface
        del shader_info
        # ========== CREATE COMPOSITE SHADER ==========
        composite_shader_info = gpu.types.GPUShaderCreateInfo()
        composite_shader_info.vertex_in(0, 'VEC2', "position")
        composite_shader_info.vertex_in(1, 'VEC2', "uv")
        composite_interface = gpu.types.GPUStageInterfaceInfo("composite_interface")
        composite_interface.smooth('VEC2', "uvInterp")
        composite_shader_info.vertex_out(composite_interface)
        composite_shader_info.sampler(0, 'FLOAT_2D', "image")
        composite_shader_info.fragment_out(0, 'VEC4', "FragColor")
        composite_shader_info.vertex_source(composite_vertex_source)
        composite_shader_info.fragment_source(composite_fragment_source)
        composite_shader = gpu.shader.create_from_info(composite_shader_info)
        del composite_interface
        del composite_shader_info
        # ========== CREATE BATCHES ==========
        base_quad = np.array([
            [-1.0,  1.0],
            [ 1.0,  1.0],
            [ 1.0, -1.0],
            [-1.0, -1.0],
        ], dtype=np.float32)
        base_indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
        quad_batch = batch_for_shader(
            quad_shader, 
            'TRIS',
            {"quad_coord": base_quad},
            indices=base_indices
        )
        composite_batch = batch_for_shader(
            composite_shader, 
            'TRI_FAN',
            {
                "position": ((-1, -1), (1, -1), (1, 1), (-1, 1)),
                "uv": ((0, 0), (1, 0), (1, 1), (0, 1)),
            }
        )
        # Store globally
        bpy.gaussian_quad_shader = quad_shader
        bpy.gaussian_quad_batch = quad_batch
        bpy.gaussian_composite_shader = composite_shader  
        bpy.gaussian_composite_batch = composite_batch
        print("Multi-object shader system created successfully")
    except Exception as e:
        print(f"Error creating shader system: {e}")
        import traceback
        traceback.print_exc()


def sna_c2_refresh_all_4D367(REFRESH_ALL_OBJECTS, UPDATE_TRANSFORMS, USE_EVALUATED_MESH):
    REFRESH_ALL_OBJECTS = REFRESH_ALL_OBJECTS
    UPDATE_TRANSFORMS = UPDATE_TRANSFORMS
    USE_EVALUATED_MESH = USE_EVALUATED_MESH
    # ========== VARIABLES (EDIT THESE) ==========
    #REFRESH_ALL_OBJECTS = True          # True = refresh all, False = refresh only selected gaussian empties
    #UPDATE_TRANSFORMS = True            # For Blender object sources - sync empty transform to source object
    CHECK_FILE_TIMESTAMPS = True        # For PLY sources - only refresh if file is newer than last load
    #USE_EVALUATED_MESH = True          # Use evaluated mesh data (after modifiers) for Blender mesh sources
    # ============================================
    import numpy as np
    #import time
    from mathutils import Matrix
    # Original PLY loader class (same as script_1a)
    class PlyLoader:

        def __init__(self, ply_path):
            self.load_ply(ply_path)

        def load_ply(self, ply_path):
            from plyfile import PlyData
            plydata = PlyData.read(ply_path)
            vertex_element = plydata.elements[0]
            vertex_data = vertex_element.data
            available_fields = list(vertex_data.dtype.names)
            # Extract positions
            if 'x' in available_fields and 'y' in available_fields and 'z' in available_fields:
                positions = np.column_stack([vertex_data['x'], vertex_data['y'], vertex_data['z']])
                positions = np.ascontiguousarray(positions)
            else:
                raise ValueError("PLY file missing position coordinates (x, y, z)")
            # Extract spherical harmonics
            sh_coeffs = None
            if 'f_dc_0' in available_fields and 'f_dc_1' in available_fields and 'f_dc_2' in available_fields:
                dc_0 = vertex_data['f_dc_0']
                dc_1 = vertex_data['f_dc_1'] 
                dc_2 = vertex_data['f_dc_2']
                features_dc = np.column_stack([dc_0, dc_1, dc_2])
                f_rest_fields = [field for field in available_fields if field.startswith('f_rest_')]
                f_rest_fields = sorted(f_rest_fields, key=lambda x: int(x.split('_')[-1]))
                if f_rest_fields:
                    features_extra = np.column_stack([vertex_data[field] for field in f_rest_fields])
                    num_f_rest = len(f_rest_fields)
                    if num_f_rest >= 45:
                        actual_degree = 3
                        coeffs_to_use = 45
                    elif num_f_rest >= 24:
                        actual_degree = 2  
                        coeffs_to_use = 24
                    elif num_f_rest >= 9:
                        actual_degree = 1
                        coeffs_to_use = 9
                    else:
                        actual_degree = 0
                        coeffs_to_use = 0
                    if coeffs_to_use > 0:
                        features_extra_used = features_extra[:, :coeffs_to_use]
                        coeffs_per_degree = (actual_degree + 1) ** 2 - 1
                        features_extra_reshaped = features_extra_used.reshape((len(positions), 3, coeffs_per_degree))
                        features_extra_reshaped = np.transpose(features_extra_reshaped, [0, 2, 1])
                        features_dc_reshaped = features_dc.reshape(-1, 1, 3)
                        all_features = np.concatenate([features_dc_reshaped, features_extra_reshaped], axis=1)
                        sh_coeffs = all_features.reshape(len(positions), -1)
                    else:
                        sh_coeffs = features_dc
                else:
                    sh_coeffs = features_dc
            else:
                sh_coeffs = np.ones((len(positions), 3)) * 0.28209479177387814
            # Extract scales
            if 'scale_0' in available_fields and 'scale_1' in available_fields and 'scale_2' in available_fields:
                scale_0 = vertex_data['scale_0']
                scale_1 = vertex_data['scale_1']
                scale_2 = vertex_data['scale_2']
                scales = np.column_stack([scale_0, scale_1, scale_2])
                scales = np.exp(scales)
            else:
                scales = np.ones((len(positions), 3)) * 0.01
            # Extract rotations
            if ('rot_0' in available_fields and 'rot_1' in available_fields and 
                'rot_2' in available_fields and 'rot_3' in available_fields):
                rot_0 = vertex_data['rot_0']
                rot_1 = vertex_data['rot_1']
                rot_2 = vertex_data['rot_2']
                rot_3 = vertex_data['rot_3']
                rotations = np.column_stack([rot_0, rot_1, rot_2, rot_3])
                norms = np.linalg.norm(rotations, axis=1, keepdims=True)
                rotations = rotations / norms
            else:
                rotations = np.zeros((len(positions), 4))
                rotations[:, 0] = 1.0
            # Extract opacity
            if 'opacity' in available_fields:
                opacity = vertex_data['opacity']
                opacity = 1.0 / (1.0 + np.exp(-opacity))
            else:
                opacity = np.ones(len(positions))
            # Store results
            self.num_points = len(positions)
            self.positions = positions.astype(np.float32)
            self.scales = scales.astype(np.float32)
            self.rotations = rotations.astype(np.float32)
            self.opacities = opacity.astype(np.float32)
            self.sh_coeffs = sh_coeffs.astype(np.float32)
            self.sh_dim = sh_coeffs.shape[1]
    # Blender mesh attribute extraction functions

    def check_mesh_has_gaussian_attributes(mesh_obj):
        """Check if mesh object has basic gaussian attributes"""
        if not mesh_obj or not mesh_obj.data:
            return False
        # Check for basic gaussian attributes
        required_attrs = ['f_dc_0', 'f_dc_1', 'f_dc_2']
        available_attrs = [attr.name for attr in mesh_obj.data.attributes]
        return all(attr in available_attrs for attr in required_attrs)

    def extract_attribute_data(mesh_data, attr_name):
        """Extract data from mesh attribute by name - optimized version"""
        if attr_name not in [attr.name for attr in mesh_data.attributes]:
            return None
        attr = mesh_data.attributes[attr_name]
        # Use foreach_get for much faster extraction
        data_array = np.zeros(len(attr.data), dtype=np.float32)
        attr.data.foreach_get("value", data_array)
        return data_array

    def extract_gaussian_data_from_evaluated_mesh(mesh_obj):
        """Extract and process gaussian data from EVALUATED mesh object attributes"""
        # Get evaluated mesh data
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated_object = mesh_obj.evaluated_get(depsgraph)
        evaluated_mesh = evaluated_object.data
        # Extract positions from evaluated vertices - optimized version
        num_points = len(evaluated_mesh.vertices)
        if num_points == 0:
            raise ValueError("Evaluated mesh has no vertices")
        # Use foreach_get for fast vertex coordinate extraction
        positions = np.zeros(num_points * 3, dtype=np.float32)
        evaluated_mesh.vertices.foreach_get("co", positions)
        positions = positions.reshape(-1, 3)
        # Get available attributes from evaluated mesh
        available_attrs = [attr.name for attr in evaluated_mesh.attributes]
        # Extract spherical harmonics from evaluated mesh
        if all(attr in available_attrs for attr in ['f_dc_0', 'f_dc_1', 'f_dc_2']):
            dc_0 = extract_attribute_data(evaluated_mesh, 'f_dc_0')
            dc_1 = extract_attribute_data(evaluated_mesh, 'f_dc_1')
            dc_2 = extract_attribute_data(evaluated_mesh, 'f_dc_2')
            features_dc = np.column_stack([dc_0, dc_1, dc_2])
            # Find f_rest fields
            f_rest_fields = [attr for attr in available_attrs if attr.startswith('f_rest_')]
            f_rest_fields = sorted(f_rest_fields, key=lambda x: int(x.split('_')[-1]))
            if f_rest_fields:
                features_extra_list = []
                for field in f_rest_fields:
                    data = extract_attribute_data(evaluated_mesh, field)
                    if data is not None:
                        features_extra_list.append(data)
                if features_extra_list:
                    features_extra = np.column_stack(features_extra_list)
                    num_f_rest = len(f_rest_fields)
                    # Determine degree and coefficients to use
                    if num_f_rest >= 45:
                        actual_degree = 3
                        coeffs_to_use = 45
                    elif num_f_rest >= 24:
                        actual_degree = 2  
                        coeffs_to_use = 24
                    elif num_f_rest >= 9:
                        actual_degree = 1
                        coeffs_to_use = 9
                    else:
                        actual_degree = 0
                        coeffs_to_use = 0
                    if coeffs_to_use > 0:
                        features_extra_used = features_extra[:, :coeffs_to_use]
                        coeffs_per_degree = (actual_degree + 1) ** 2 - 1
                        features_extra_reshaped = features_extra_used.reshape((num_points, 3, coeffs_per_degree))
                        features_extra_reshaped = np.transpose(features_extra_reshaped, [0, 2, 1])
                        features_dc_reshaped = features_dc.reshape(-1, 1, 3)
                        all_features = np.concatenate([features_dc_reshaped, features_extra_reshaped], axis=1)
                        sh_coeffs = all_features.reshape(num_points, -1)
                    else:
                        sh_coeffs = features_dc
                else:
                    sh_coeffs = features_dc
            else:
                sh_coeffs = features_dc
        else:
            # Default SH coeffs if not found
            print(f"Warning: f_dc attributes not found on evaluated mesh, using defaults")
            sh_coeffs = np.ones((num_points, 3)) * 0.28209479177387814
        # Extract scales from evaluated mesh
        if all(attr in available_attrs for attr in ['scale_0', 'scale_1', 'scale_2']):
            scale_0 = extract_attribute_data(evaluated_mesh, 'scale_0')
            scale_1 = extract_attribute_data(evaluated_mesh, 'scale_1')
            scale_2 = extract_attribute_data(evaluated_mesh, 'scale_2')
            scales = np.column_stack([scale_0, scale_1, scale_2])
            scales = np.exp(scales)  # Apply exponential
        else:
            print(f"Warning: scale attributes not found on evaluated mesh, using defaults")
            scales = np.ones((num_points, 3)) * 0.01
        # Extract rotations from evaluated mesh
        if all(attr in available_attrs for attr in ['rot_0', 'rot_1', 'rot_2', 'rot_3']):
            rot_0 = extract_attribute_data(evaluated_mesh, 'rot_0')
            rot_1 = extract_attribute_data(evaluated_mesh, 'rot_1')
            rot_2 = extract_attribute_data(evaluated_mesh, 'rot_2')
            rot_3 = extract_attribute_data(evaluated_mesh, 'rot_3')
            rotations = np.column_stack([rot_0, rot_1, rot_2, rot_3])
            # Normalize quaternions
            norms = np.linalg.norm(rotations, axis=1, keepdims=True)
            rotations = rotations / norms
        else:
            print(f"Warning: rotation attributes not found on evaluated mesh, using defaults")
            rotations = np.zeros((num_points, 4))
            rotations[:, 0] = 1.0  # Identity quaternion
        # Extract opacity from evaluated mesh
        if 'opacity' in available_attrs:
            opacity_raw = extract_attribute_data(evaluated_mesh, 'opacity')
            opacity = 1.0 / (1.0 + np.exp(-opacity_raw))  # Apply sigmoid
        else:
            print(f"Warning: opacity attribute not found on evaluated mesh, using defaults")
            opacity = np.ones(num_points)
        return {
            'num_points': num_points,
            'positions': positions,
            'scales': scales,
            'rotations': rotations,
            'opacities': opacity,
            'sh_coeffs': sh_coeffs,
            'sh_dim': sh_coeffs.shape[1]
        }

    def extract_gaussian_data_from_mesh(mesh_obj):
        """Extract and process gaussian data from ORIGINAL mesh object attributes"""
        # Extract positions from vertices - optimized version
        num_points = len(mesh_obj.data.vertices)
        if num_points == 0:
            raise ValueError("Mesh has no vertices")
        # Use foreach_get for fast vertex coordinate extraction
        positions = np.zeros(num_points * 3, dtype=np.float32)
        mesh_obj.data.vertices.foreach_get("co", positions)
        positions = positions.reshape(-1, 3)
        # Get available attributes
        available_attrs = [attr.name for attr in mesh_obj.data.attributes]
        # Extract spherical harmonics
        if all(attr in available_attrs for attr in ['f_dc_0', 'f_dc_1', 'f_dc_2']):
            dc_0 = extract_attribute_data(mesh_obj.data, 'f_dc_0')
            dc_1 = extract_attribute_data(mesh_obj.data, 'f_dc_1')
            dc_2 = extract_attribute_data(mesh_obj.data, 'f_dc_2')
            features_dc = np.column_stack([dc_0, dc_1, dc_2])
            # Find f_rest fields
            f_rest_fields = [attr for attr in available_attrs if attr.startswith('f_rest_')]
            f_rest_fields = sorted(f_rest_fields, key=lambda x: int(x.split('_')[-1]))
            if f_rest_fields:
                features_extra_list = []
                for field in f_rest_fields:
                    data = extract_attribute_data(mesh_obj.data, field)
                    if data is not None:
                        features_extra_list.append(data)
                if features_extra_list:
                    features_extra = np.column_stack(features_extra_list)
                    num_f_rest = len(f_rest_fields)
                    # Determine degree and coefficients to use
                    if num_f_rest >= 45:
                        actual_degree = 3
                        coeffs_to_use = 45
                    elif num_f_rest >= 24:
                        actual_degree = 2  
                        coeffs_to_use = 24
                    elif num_f_rest >= 9:
                        actual_degree = 1
                        coeffs_to_use = 9
                    else:
                        actual_degree = 0
                        coeffs_to_use = 0
                    if coeffs_to_use > 0:
                        features_extra_used = features_extra[:, :coeffs_to_use]
                        coeffs_per_degree = (actual_degree + 1) ** 2 - 1
                        features_extra_reshaped = features_extra_used.reshape((num_points, 3, coeffs_per_degree))
                        features_extra_reshaped = np.transpose(features_extra_reshaped, [0, 2, 1])
                        features_dc_reshaped = features_dc.reshape(-1, 1, 3)
                        all_features = np.concatenate([features_dc_reshaped, features_extra_reshaped], axis=1)
                        sh_coeffs = all_features.reshape(num_points, -1)
                    else:
                        sh_coeffs = features_dc
                else:
                    sh_coeffs = features_dc
            else:
                sh_coeffs = features_dc
        else:
            # Default SH coeffs if not found
            sh_coeffs = np.ones((num_points, 3)) * 0.28209479177387814
        # Extract scales
        if all(attr in available_attrs for attr in ['scale_0', 'scale_1', 'scale_2']):
            scale_0 = extract_attribute_data(mesh_obj.data, 'scale_0')
            scale_1 = extract_attribute_data(mesh_obj.data, 'scale_1')
            scale_2 = extract_attribute_data(mesh_obj.data, 'scale_2')
            scales = np.column_stack([scale_0, scale_1, scale_2])
            scales = np.exp(scales)  # Apply exponential
        else:
            scales = np.ones((num_points, 3)) * 0.01
        # Extract rotations
        if all(attr in available_attrs for attr in ['rot_0', 'rot_1', 'rot_2', 'rot_3']):
            rot_0 = extract_attribute_data(mesh_obj.data, 'rot_0')
            rot_1 = extract_attribute_data(mesh_obj.data, 'rot_1')
            rot_2 = extract_attribute_data(mesh_obj.data, 'rot_2')
            rot_3 = extract_attribute_data(mesh_obj.data, 'rot_3')
            rotations = np.column_stack([rot_0, rot_1, rot_2, rot_3])
            # Normalize quaternions
            norms = np.linalg.norm(rotations, axis=1, keepdims=True)
            rotations = rotations / norms
        else:
            rotations = np.zeros((num_points, 4))
            rotations[:, 0] = 1.0  # Identity quaternion
        # Extract opacity
        if 'opacity' in available_attrs:
            opacity_raw = extract_attribute_data(mesh_obj.data, 'opacity')
            opacity = 1.0 / (1.0 + np.exp(-opacity_raw))  # Apply sigmoid
        else:
            opacity = np.ones(num_points)
        return {
            'num_points': num_points,
            'positions': positions,
            'scales': scales,
            'rotations': rotations,
            'opacities': opacity,
            'sh_coeffs': sh_coeffs,
            'sh_dim': sh_coeffs.shape[1]
        }

    def get_file_modification_time(filepath):
        """Get file modification time, return 0 if file doesn't exist"""
        try:
            return os.path.getmtime(filepath)
        except (OSError, FileNotFoundError):
            return 0

    def find_source_object_by_uuid(source_uuid):
        """Find Blender object by gaussian_source_uuid"""
        for obj in bpy.data.objects:
            if obj.get("gaussian_source_uuid") == source_uuid:
                return obj
        return None

    def update_empty_transform(empty_obj, source_obj):
        """Update empty object transform to match source object"""
        if not empty_obj or not source_obj:
            return False
        try:
            empty_obj.matrix_world = source_obj.matrix_world.copy()
            return True
        except:
            return False

    def check_if_ply_needs_refresh(obj):
        """Check if PLY file is newer than last load time"""
        ply_filepath = obj.get("ply_filepath")
        if not ply_filepath or not os.path.exists(ply_filepath):
            return False, "PLY file not found or missing path"
        file_mod_time = get_file_modification_time(ply_filepath)
        last_load_time = obj.get("last_load_time", 0)
        if not CHECK_FILE_TIMESTAMPS:
            return True, "Timestamp checking disabled"
        elif file_mod_time > last_load_time:
            return True, f"File modified: {time.ctime(file_mod_time)}"
        else:
            return False, "File not modified since last load"

    def refresh_object_from_ply(obj):
        """Reload PLY data for a single object"""
        try:
            ply_filepath = obj.get("ply_filepath")
            if not ply_filepath:
                return False, "No PLY filepath stored in object"
            if not os.path.exists(ply_filepath):
                return False, f"PLY file not found: {ply_filepath}"
            print(f"Refreshing {obj.name} from {os.path.basename(ply_filepath)}...")
            # Store original transform (preserve user positioning)
            original_transform = obj.matrix_world.copy()
            # Load fresh PLY data
            ply_loader = PlyLoader(ply_filepath)
            # Create gaussian data array (59 floats per gaussian)
            num_gaussians = ply_loader.num_points
            sh_dim = 48
            total_dim = 3 + 4 + 3 + 1 + sh_dim
            gaussian_data = np.zeros((num_gaussians, total_dim), dtype=np.float32)
            # Pack data in original order
            gaussian_data[:, 0:3] = ply_loader.positions
            gaussian_data[:, 3:7] = ply_loader.rotations
            gaussian_data[:, 7:10] = ply_loader.scales
            gaussian_data[:, 10] = ply_loader.opacities.flatten()
            if ply_loader.sh_coeffs.shape[1] >= sh_dim:
                gaussian_data[:, 11:11+sh_dim] = ply_loader.sh_coeffs[:, :sh_dim]
            else:
                gaussian_data[:, 11:11+ply_loader.sh_coeffs.shape[1]] = ply_loader.sh_coeffs
            # Update object properties with new data
            obj["gaussian_data"] = gaussian_data.tobytes()
            obj["gaussian_count"] = num_gaussians
            obj["sh_degree"] = ply_loader.sh_dim
            obj["last_load_time"] = time.time()  # Track when we loaded it
            # Restore original transform
            obj.matrix_world = original_transform
            # Update cache if it exists
            if hasattr(bpy, 'gaussian_object_cache') and obj.name in bpy.gaussian_object_cache:
                bpy.gaussian_object_cache[obj.name].update({
                    'gaussian_data': gaussian_data,
                    'gaussian_count': num_gaussians,
                    'sh_degree': ply_loader.sh_dim,
                    'ply_filepath': ply_filepath
                })
            return True, f"Refreshed: {num_gaussians:,} gaussians (SH degree {ply_loader.sh_dim})"
        except Exception as e:
            return False, f"Failed to refresh: {e}"

    def refresh_object_from_blender_object(obj):
        """Reload data from linked Blender object for a single gaussian empty - USING EVALUATED MESH"""
        try:
            source_uuid = obj.get("source_mesh_uuid")
            if not source_uuid:
                return False, "No source UUID stored in object"
            # Find source object by UUID
            source_obj = find_source_object_by_uuid(source_uuid)
            if not source_obj:
                return False, f"Source object with UUID {source_uuid} not found"
            # Validate that source object has gaussian attributes
            if not check_mesh_has_gaussian_attributes(source_obj):
                return False, f"Source object '{source_obj.name}' does not have required gaussian attributes"
            mesh_type = "EVALUATED" if USE_EVALUATED_MESH else "ORIGINAL"
            print(f"Refreshing {obj.name} from {mesh_type} Blender object {source_obj.name}...")
            # Extract gaussian data from source mesh - CHOOSE EVALUATED OR ORIGINAL
            if USE_EVALUATED_MESH:
                gaussian_data_info = extract_gaussian_data_from_evaluated_mesh(source_obj)
            else:
                gaussian_data_info = extract_gaussian_data_from_mesh(source_obj)
            # Create gaussian data array (59 floats per gaussian)
            num_gaussians = gaussian_data_info['num_points']
            sh_dim = 48
            total_dim = 3 + 4 + 3 + 1 + sh_dim
            gaussian_data = np.zeros((num_gaussians, total_dim), dtype=np.float32)
            # Pack data in original order
            gaussian_data[:, 0:3] = gaussian_data_info['positions']
            gaussian_data[:, 3:7] = gaussian_data_info['rotations']
            gaussian_data[:, 7:10] = gaussian_data_info['scales']
            gaussian_data[:, 10] = gaussian_data_info['opacities'].flatten()
            # Handle SH coefficients
            source_sh_coeffs = gaussian_data_info['sh_coeffs']
            if source_sh_coeffs.shape[1] >= sh_dim:
                gaussian_data[:, 11:11+sh_dim] = source_sh_coeffs[:, :sh_dim]
            else:
                gaussian_data[:, 11:11+source_sh_coeffs.shape[1]] = source_sh_coeffs
            # Update object properties with new data
            obj["gaussian_data"] = gaussian_data.tobytes()
            obj["gaussian_count"] = num_gaussians
            obj["sh_degree"] = gaussian_data_info['sh_dim']
            obj["last_load_time"] = time.time()
            # Mark as using evaluated mesh if that's what we used
            if USE_EVALUATED_MESH:
                obj["is_evaluated_mesh"] = True
            # Update transform if requested
            if UPDATE_TRANSFORMS:
                transform_updated = update_empty_transform(obj, source_obj)
                transform_status = " (transform updated)" if transform_updated else " (transform update failed)"
            else:
                transform_status = ""
            # Update cache if it exists
            if hasattr(bpy, 'gaussian_object_cache') and obj.name in bpy.gaussian_object_cache:
                bpy.gaussian_object_cache[obj.name].update({
                    'gaussian_data': gaussian_data,
                    'gaussian_count': num_gaussians,
                    'sh_degree': gaussian_data_info['sh_dim'],
                    'source_mesh_uuid': source_uuid,
                    'source_mesh_name': source_obj.name
                })
            return True, f"Refreshed: {num_gaussians:,} gaussians from {mesh_type} {source_obj.name} (SH degree {gaussian_data_info['sh_dim']}){transform_status}"
        except Exception as e:
            return False, f"Failed to refresh: {e}"

    def get_objects_to_refresh():
        """Get list of objects to refresh based on REFRESH_ALL_OBJECTS setting"""
        objects_to_refresh = []
        if REFRESH_ALL_OBJECTS:
            # Refresh all gaussian objects
            for obj in bpy.data.objects:
                if obj.get("is_gaussian_splat", False):
                    objects_to_refresh.append(obj)
        else:
            # Refresh only selected gaussian objects
            for obj in bpy.context.selected_objects:
                if obj.get("is_gaussian_splat", False):
                    objects_to_refresh.append(obj)
        return objects_to_refresh

    def refresh_gaussian_objects():
        """Main refresh function - handles both PLY and Blender object sources"""
        try:
            # Find gaussian objects to refresh
            objects_to_refresh = get_objects_to_refresh()
            if not objects_to_refresh:
                print("No gaussian objects found to refresh")
                return False
            mode_text = "all objects" if REFRESH_ALL_OBJECTS else "selected objects"
            mesh_mode_text = "EVALUATED MESH" if USE_EVALUATED_MESH else "ORIGINAL MESH"
            print(f"Checking {len(objects_to_refresh)} gaussian objects for refresh ({mode_text}, {mesh_mode_text})...")
            refreshed_objects = []
            skipped_objects = []
            failed_objects = []
            for obj in objects_to_refresh:
                # Determine source type and handle accordingly
                is_ply_source = obj.get("ply_filepath") is not None
                is_blender_source = obj.get("source_mesh_uuid") is not None
                if is_ply_source:
                    # Handle PLY source
                    if CHECK_FILE_TIMESTAMPS:
                        needs_refresh, reason = check_if_ply_needs_refresh(obj)
                        if not needs_refresh:
                            skipped_objects.append((obj.name, f"PLY: {reason}"))
                            print(f"  ⏭️  {obj.name}: PLY: {reason}")
                            continue
                    success, message = refresh_object_from_ply(obj)
                    if success:
                        refreshed_objects.append((obj.name, f"PLY: {message}"))
                        print(f"  ✅ {obj.name}: PLY: {message}")
                    else:
                        failed_objects.append((obj.name, f"PLY: {message}"))
                        print(f"  ❌ {obj.name}: PLY: {message}")
                elif is_blender_source:
                    # Handle Blender object source (always refresh, no timestamp check)
                    success, message = refresh_object_from_blender_object(obj)
                    if success:
                        refreshed_objects.append((obj.name, f"BlenderObj: {message}"))
                        print(f"  ✅ {obj.name}: BlenderObj: {message}")
                    else:
                        failed_objects.append((obj.name, f"BlenderObj: {message}"))
                        print(f"  ❌ {obj.name}: BlenderObj: {message}")
                else:
                    # Unknown source type
                    failed_objects.append((obj.name, "Unknown source type (no PLY path or UUID)"))
                    print(f"  ❌ {obj.name}: Unknown source type")
            # Print summary
            print(f"\nRefresh Summary:")
            print(f"  Refreshed: {len(refreshed_objects)}")
            print(f"  Skipped: {len(skipped_objects)}")
            print(f"  Failed: {len(failed_objects)}")
            # Mark global data for rebuild if any objects were refreshed
            if refreshed_objects:
                bpy.gaussian_global_needs_update = True
                print(f"\nNext: Run script_3 to rebuild global textures")
                # Force viewport update
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
            return len(refreshed_objects) > 0
        except Exception as e:
            print(f"Error during refresh: {e}")
            import traceback
            traceback.print_exc()
            return False
    # ========== MAIN EXECUTION ==========
    print("Starting PLY and Blender object refresh check...")
    print(f"Mode: {'All objects' if REFRESH_ALL_OBJECTS else 'Selected objects only'}")
    print(f"Update transforms: {UPDATE_TRANSFORMS} (Blender object sources only)")
    print(f"Check PLY timestamps: {CHECK_FILE_TIMESTAMPS}")
    print(f"Use evaluated mesh: {USE_EVALUATED_MESH} (Blender object sources only)")
    print()
    refresh_success = refresh_gaussian_objects()
    if refresh_success:
        print("\n🎉 Refresh completed! Remember to run script_3 to rebuild textures.")
    else:
        print("\n💤 No objects needed refreshing.")


def sna_b2_load_from_blender_object_F0CCB(OBJECT_BASE_NAME):
    OBJECT_BASE_NAME = OBJECT_BASE_NAME
    # ========== VARIABLES (EDIT THESE) ==========
    SOURCE_MESH_OBJECT = None  # Set this to target mesh object, or leave None to use active object
    #OBJECT_BASE_NAME = "GaussianSplat"  # Will auto-number: _001, _002, etc.
    # ============================================
    import numpy as np
    from math import pi
    #import time

    def get_unique_object_name(base_name):
        """Generate unique object name with auto-numbering"""
        if base_name not in bpy.data.objects:
            return base_name
        counter = 1
        while f"{base_name}_{counter:03d}" in bpy.data.objects:
            counter += 1
        return f"{base_name}_{counter:03d}"

    def check_mesh_has_gaussian_attributes(mesh_obj):
        """Check if mesh object has basic gaussian attributes"""
        if not mesh_obj or not mesh_obj.data:
            return False
        # Check for basic gaussian attributes
        required_attrs = ['f_dc_0', 'f_dc_1', 'f_dc_2']
        available_attrs = [attr.name for attr in mesh_obj.data.attributes]
        return all(attr in available_attrs for attr in required_attrs)

    def extract_attribute_data(mesh_data, attr_name):
        """Extract data from mesh attribute by name - optimized version"""
        if attr_name not in [attr.name for attr in mesh_data.attributes]:
            return None
        attr = mesh_data.attributes[attr_name]
        # Use foreach_get for much faster extraction
        data_array = np.zeros(len(attr.data), dtype=np.float32)
        attr.data.foreach_get("value", data_array)
        return data_array

    def extract_gaussian_data_from_evaluated_mesh(mesh_obj):
        """Extract and process gaussian data from EVALUATED mesh object attributes"""
        # Get evaluated mesh data
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated_object = mesh_obj.evaluated_get(depsgraph)
        evaluated_mesh = evaluated_object.data
        # Extract positions from evaluated vertices - optimized version
        num_points = len(evaluated_mesh.vertices)
        if num_points == 0:
            raise ValueError("Evaluated mesh has no vertices")
        # Use foreach_get for fast vertex coordinate extraction
        positions = np.zeros(num_points * 3, dtype=np.float32)
        evaluated_mesh.vertices.foreach_get("co", positions)
        positions = positions.reshape(-1, 3)
        # Get available attributes from evaluated mesh
        available_attrs = [attr.name for attr in evaluated_mesh.attributes]
        # Extract spherical harmonics from evaluated mesh
        if all(attr in available_attrs for attr in ['f_dc_0', 'f_dc_1', 'f_dc_2']):
            dc_0 = extract_attribute_data(evaluated_mesh, 'f_dc_0')
            dc_1 = extract_attribute_data(evaluated_mesh, 'f_dc_1')
            dc_2 = extract_attribute_data(evaluated_mesh, 'f_dc_2')
            features_dc = np.column_stack([dc_0, dc_1, dc_2])
            # Find f_rest fields
            f_rest_fields = [attr for attr in available_attrs if attr.startswith('f_rest_')]
            f_rest_fields = sorted(f_rest_fields, key=lambda x: int(x.split('_')[-1]))
            if f_rest_fields:
                features_extra_list = []
                for field in f_rest_fields:
                    data = extract_attribute_data(evaluated_mesh, field)
                    if data is not None:
                        features_extra_list.append(data)
                if features_extra_list:
                    features_extra = np.column_stack(features_extra_list)
                    num_f_rest = len(f_rest_fields)
                    # Determine degree and coefficients to use
                    if num_f_rest >= 45:
                        actual_degree = 3
                        coeffs_to_use = 45
                    elif num_f_rest >= 24:
                        actual_degree = 2  
                        coeffs_to_use = 24
                    elif num_f_rest >= 9:
                        actual_degree = 1
                        coeffs_to_use = 9
                    else:
                        actual_degree = 0
                        coeffs_to_use = 0
                    if coeffs_to_use > 0:
                        features_extra_used = features_extra[:, :coeffs_to_use]
                        coeffs_per_degree = (actual_degree + 1) ** 2 - 1
                        features_extra_reshaped = features_extra_used.reshape((num_points, 3, coeffs_per_degree))
                        features_extra_reshaped = np.transpose(features_extra_reshaped, [0, 2, 1])
                        features_dc_reshaped = features_dc.reshape(-1, 1, 3)
                        all_features = np.concatenate([features_dc_reshaped, features_extra_reshaped], axis=1)
                        sh_coeffs = all_features.reshape(num_points, -1)
                    else:
                        sh_coeffs = features_dc
                else:
                    sh_coeffs = features_dc
            else:
                sh_coeffs = features_dc
        else:
            # Default SH coeffs if not found
            print(f"Warning: f_dc attributes not found on evaluated mesh, using defaults")
            sh_coeffs = np.ones((num_points, 3)) * 0.28209479177387814
        # Extract scales from evaluated mesh
        if all(attr in available_attrs for attr in ['scale_0', 'scale_1', 'scale_2']):
            scale_0 = extract_attribute_data(evaluated_mesh, 'scale_0')
            scale_1 = extract_attribute_data(evaluated_mesh, 'scale_1')
            scale_2 = extract_attribute_data(evaluated_mesh, 'scale_2')
            scales = np.column_stack([scale_0, scale_1, scale_2])
            scales = np.exp(scales)  # Apply exponential
        else:
            print(f"Warning: scale attributes not found on evaluated mesh, using defaults")
            scales = np.ones((num_points, 3)) * 0.01
        # Extract rotations from evaluated mesh
        if all(attr in available_attrs for attr in ['rot_0', 'rot_1', 'rot_2', 'rot_3']):
            rot_0 = extract_attribute_data(evaluated_mesh, 'rot_0')
            rot_1 = extract_attribute_data(evaluated_mesh, 'rot_1')
            rot_2 = extract_attribute_data(evaluated_mesh, 'rot_2')
            rot_3 = extract_attribute_data(evaluated_mesh, 'rot_3')
            rotations = np.column_stack([rot_0, rot_1, rot_2, rot_3])
            # Normalize quaternions
            norms = np.linalg.norm(rotations, axis=1, keepdims=True)
            rotations = rotations / norms
        else:
            print(f"Warning: rotation attributes not found on evaluated mesh, using defaults")
            rotations = np.zeros((num_points, 4))
            rotations[:, 0] = 1.0  # Identity quaternion
        # Extract opacity from evaluated mesh
        if 'opacity' in available_attrs:
            opacity_raw = extract_attribute_data(evaluated_mesh, 'opacity')
            opacity = 1.0 / (1.0 + np.exp(-opacity_raw))  # Apply sigmoid
        else:
            print(f"Warning: opacity attribute not found on evaluated mesh, using defaults")
            opacity = np.ones(num_points)
        return {
            'num_points': num_points,
            'positions': positions,
            'scales': scales,
            'rotations': rotations,
            'opacities': opacity,
            'sh_coeffs': sh_coeffs,
            'sh_dim': sh_coeffs.shape[1]
        }
    try:
        # Determine source mesh object
        if SOURCE_MESH_OBJECT is not None:
            source_obj = SOURCE_MESH_OBJECT
        else:
            source_obj = bpy.context.active_object
        if not source_obj:
            raise ValueError("No source mesh object specified and no active object")
        if source_obj.type != 'MESH':
            raise ValueError(f"Object '{source_obj.name}' is not a mesh object")
        # Check if mesh has gaussian attributes (check original mesh, not evaluated)
        if not check_mesh_has_gaussian_attributes(source_obj):
            raise ValueError(f"Mesh object '{source_obj.name}' does not have required gaussian attributes (f_dc_0, f_dc_1, f_dc_2)")
        print(f"Extracting gaussian data from EVALUATED mesh: {source_obj.name}")
        # Generate or get UUID for source mesh
        import uuid
        if "gaussian_source_uuid" not in source_obj:
            source_obj["gaussian_source_uuid"] = str(uuid.uuid4())
        source_uuid = source_obj["gaussian_source_uuid"]
        # Extract gaussian data from EVALUATED mesh
        gaussian_data_info = extract_gaussian_data_from_evaluated_mesh(source_obj)
        # Create gaussian data array (59 floats per gaussian)
        num_gaussians = gaussian_data_info['num_points']
        sh_dim = 48
        total_dim = 3 + 4 + 3 + 1 + sh_dim
        gaussian_data = np.zeros((num_gaussians, total_dim), dtype=np.float32)
        # Pack data in original order
        gaussian_data[:, 0:3] = gaussian_data_info['positions']
        gaussian_data[:, 3:7] = gaussian_data_info['rotations']
        gaussian_data[:, 7:10] = gaussian_data_info['scales']
        gaussian_data[:, 10] = gaussian_data_info['opacities'].flatten()
        # Handle SH coefficients
        source_sh_coeffs = gaussian_data_info['sh_coeffs']
        if source_sh_coeffs.shape[1] >= sh_dim:
            gaussian_data[:, 11:11+sh_dim] = source_sh_coeffs[:, :sh_dim]
        else:
            gaussian_data[:, 11:11+source_sh_coeffs.shape[1]] = source_sh_coeffs
        # Generate unique object name
        object_name = get_unique_object_name(OBJECT_BASE_NAME)
        # Create Blender empty object
        empty_object = bpy.data.objects.new(object_name, None)
        empty_object.empty_display_type = 'PLAIN_AXES'
        empty_object.empty_display_size = 0.1
        empty_object.matrix_world = source_obj.matrix_world.copy()  # Match source object transform
        # Store data in object properties
        empty_object["gaussian_data"] = gaussian_data.tobytes()
        empty_object["gaussian_count"] = num_gaussians
        empty_object["sh_degree"] = gaussian_data_info['sh_dim']
        empty_object["is_gaussian_splat"] = True
        empty_object["is_mesh_source"] = True
        empty_object["is_evaluated_mesh"] = True  # Mark as using evaluated mesh
        empty_object["source_mesh_uuid"] = source_uuid  # Store UUID instead of name
        empty_object["source_mesh_name"] = source_obj.name  # Store name for reference/debugging
        empty_object["is_loaded"] = True
        empty_object["last_load_time"] = time.time()
        # Link to scene
        bpy.context.collection.objects.link(empty_object)
        # Initialize global cache if needed
        if not hasattr(bpy, 'gaussian_object_cache'):
            bpy.gaussian_object_cache = {}
        # Add to global cache
        bpy.gaussian_object_cache[object_name] = {
            'gaussian_data': gaussian_data,
            'gaussian_count': num_gaussians,
            'sh_degree': gaussian_data_info['sh_dim'],
            'object': empty_object,
            'source_mesh_uuid': source_uuid,
            'source_mesh_name': source_obj.name  # Keep name for reference
        }
        # Mark that global textures need rebuilding
        bpy.gaussian_global_needs_update = True
        total_objects = len(bpy.gaussian_object_cache)
        total_gaussians = sum(obj['gaussian_count'] for obj in bpy.gaussian_object_cache.values())
        print(f"Loaded {object_name}: {num_gaussians:,} gaussians from EVALUATED mesh '{source_obj.name}' (SH degree {gaussian_data_info['sh_dim']})")
        print(f"Total: {total_objects} objects, {total_gaussians:,} gaussians")
    except Exception as e:
        print(f"Error extracting from evaluated mesh: {e}")
        import traceback
        traceback.print_exc()


def sna_render_new_menu_66133(layout_function, ):
    box_D20F4 = layout_function.box()
    box_D20F4.alert = False
    box_D20F4.enabled = (not ((bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.render_2_interval_stop)))
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
    grid_DDB98.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_interface_mode', text=bpy.context.scene.sna_dgs_scene_properties.render_2_interface_mode, icon_value=0, emboss=True, expand=True)
    if bpy.context.scene.sna_dgs_scene_properties.render_2_interface_mode == "Update":
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
        box_10F75.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_hide_object_on_menu_change', text='Hide / Show Objects On Menu Change*', icon_value=0, emboss=True)
        box_10F75.label(text='*Vert Imported objects only', icon_value=0)
        box_10F75.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_copy_source_transforms', text='Copy Source Transforms', icon_value=0, emboss=True)
        box_10F75.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_refresh_selected_only', text='Selected Empties Only', icon_value=0, emboss=True)
        col_1EFCE = box_10F75.column(heading='', align=False)
        col_1EFCE.alert = False
        col_1EFCE.enabled = (not ((bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.render_2_interval_stop)))
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
        row_F6BE9.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_interval_or_single_update', text=bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update, icon_value=0, emboss=True, expand=True)
        if (bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Interval Update'):
            col_1EFCE.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_interval_time', text='Interval Time (Seconds)', icon_value=0, emboss=True, expand=True)
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
        op = col_5B10D.operator('sna.dgs_render_refresh_scene_c0b35', text='Update Scene', icon_value=(load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'play.svg')) if (bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Interval Update') else load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg'))), emboss=True, depress=False)
        if ((bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Interval Update') and (not bpy.context.scene.sna_dgs_scene_properties.render_2_interval_stop)):
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
            if (bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Interval Update'):
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
    elif bpy.context.scene.sna_dgs_scene_properties.render_2_interface_mode == "Create":
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
    elif bpy.context.scene.sna_dgs_scene_properties.render_2_interface_mode == "Render":
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
        box_AC05E.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_render_animation', text='Render Animation', icon_value=0, emboss=True)
        box_AC05E.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_render_color', text='Color Pass', icon_value=0, emboss=True)
        box_AC05E.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_render_depth', text='Depth Pass', icon_value=0, emboss=True)
        box_AC05E.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_comp_with_temp', text='Combine With Native Render', icon_value=0, emboss=True)
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
    elif bpy.context.scene.sna_dgs_scene_properties.render_2_interface_mode == "Clean Up":
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
        box_32F4A.prop(bpy.context.scene.sna_dgs_scene_properties, 'render_2_remove_all_empties', text='Delete All Proxy Empties', icon_value=0, emboss=True)
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


class SNA_OT_Dgs_Render_Refresh_Scene_C0B35(bpy.types.Operator):
    bl_idname = "sna.dgs_render_refresh_scene_c0b35"
    bl_label = "3DGS Render: Refresh Scene"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Single Time'):
            pass
        else:
            bpy.context.scene.frame_current = bpy.context.scene.frame_start
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        bpy.context.scene.sna_dgs_scene_properties.render_2_interval_stop = (bpy.context.scene.sna_dgs_scene_properties.render_2_interval_or_single_update == 'Single Time')

        def delayed_09B50():
            for i_75739 in range(len(bpy.context.scene.objects)):
                if (property_exists("bpy.context.scene.objects[i_75739].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_75739].modifiers):
                    bpy.context.scene.objects[i_75739].hide_viewport = False
            sna_c2_refresh_all_4D367((not bpy.context.scene.sna_dgs_scene_properties.render_2_refresh_selected_only), bpy.context.scene.sna_dgs_scene_properties.render_2_copy_source_transforms, True)
            sna_shader_system_A4AED()
            sna_texture_creation_FD1B2()
            sna_viewport_render_A3941()
            for i_07D59 in range(len(bpy.context.scene.objects)):
                if ((property_exists("bpy.context.scene.objects[i_07D59].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_07D59].modifiers) and '3DGS_Mesh_Type' in bpy.context.scene.objects[i_07D59]):
                    if (bpy.context.scene.objects[i_07D59]['3DGS_Mesh_Type'] == 'face'):
                        bpy.context.scene.objects[i_07D59].hide_viewport = True
            if bpy.context.scene.sna_dgs_scene_properties.render_2_interval_stop:
                return None
            return bpy.context.scene.sna_dgs_scene_properties.render_2_interval_time
        bpy.app.timers.register(delayed_09B50, first_interval=0.0)
        for i_BD2F9 in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_BD2F9].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_BD2F9].modifiers):
                bpy.context.scene.objects[i_BD2F9].hide_viewport = False
        sna_c2_refresh_all_4D367((not bpy.context.scene.sna_dgs_scene_properties.render_2_refresh_selected_only), bpy.context.scene.sna_dgs_scene_properties.render_2_copy_source_transforms, True)
        sna_shader_system_A4AED()
        sna_texture_creation_FD1B2()
        sna_viewport_render_A3941()
        for i_D854A in range(len(bpy.context.scene.objects)):
            if ((property_exists("bpy.context.scene.objects[i_D854A].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_D854A].modifiers) and '3DGS_Mesh_Type' in bpy.context.scene.objects[i_D854A]):
                if (bpy.context.scene.objects[i_D854A]['3DGS_Mesh_Type'] == 'face'):
                    bpy.context.scene.objects[i_D854A].hide_viewport = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_D5B41(bpy.types.Operator):
    bl_idname = "sna.dgs_render_create_proxy_from_mesh_d5b41"
    bl_label = "3DGS Render: Create Proxy From Mesh"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_b2_load_from_blender_object_F0CCB(bpy.context.view_layer.objects.active.name + 'Splat_Proxy')
        sna_shader_system_A4AED()
        sna_texture_creation_FD1B2()
        sna_viewport_render_A3941()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Advanced_Render_Ba196(bpy.types.Operator):
    bl_idname = "sna.dgs_render_advanced_render_ba196"
    bl_label = "3DGS Render: Advanced Render"
    bl_description = "Renders the proxy Gaussian objects with current settings"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_dgs_scene_properties.render_2_comp_with_temp:
            sna_render_temp_scene_913CD(bpy.context.scene.render.filepath, bpy.context.scene.sna_dgs_scene_properties.render_2_render_animation, bpy.context.scene.frame_step)
        sna_render_comp_0DAEE(bpy.context.scene.sna_dgs_scene_properties.render_2_render_animation, bpy.context.scene.sna_dgs_scene_properties.render_2_render_color, bpy.context.scene.sna_dgs_scene_properties.render_2_render_depth, bpy.context.scene.sna_dgs_scene_properties.render_2_comp_with_temp, bpy.context.scene.render.filepath, bpy.context.scene.sna_dgs_scene_properties.render_2_copy_source_transforms, True, bpy.context.scene.frame_step)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Clean_Up_Advanced_Render_Scene_09450(bpy.types.Operator):
    bl_idname = "sna.dgs_render_clean_up_advanced_render_scene_09450"
    bl_label = "3DGS Render: Clean Up Advanced Render Scene"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_clean_up_scene_5F1F1(bpy.context.scene.sna_dgs_scene_properties.render_2_remove_all_empties)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Stop_Interval_Updates_5Ac80(bpy.types.Operator):
    bl_idname = "sna.dgs_render_stop_interval_updates_5ac80"
    bl_label = "3DGS Render: Stop Interval Updates"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.sna_dgs_scene_properties.render_2_interval_stop = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


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


class SNA_OT_Dgs_Render_Append_Wire_Sphere_2Bf63(bpy.types.Operator):
    bl_idname = "sna.dgs_render_append_wire_sphere_2bf63"
    bl_label = "3DGS Render: Append Wire Sphere"
    bl_description = "Appends an object for use as a modifier effector. The object will not render."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        before_data = list(bpy.data.objects)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V4.blend') + r'\Object', filename='Wire Sphere', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_69F39 = None if not new_data else new_data[0]
        appended_69F39.location = bpy.context.scene.cursor.location
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Append_Wire_Cube_56E0F(bpy.types.Operator):
    bl_idname = "sna.dgs_render_append_wire_cube_56e0f"
    bl_label = "3DGS Render: Append Wire Cube"
    bl_description = "Appends an object for use as a modifier effector. The object will not render."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        before_data = list(bpy.data.objects)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V4.blend') + r'\Object', filename='Wire Cube', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_8B494 = None if not new_data else new_data[0]
        appended_8B494.location = bpy.context.scene.cursor.location
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Append_Geometry_Node_Modifier_C2492(bpy.types.Operator):
    bl_idname = "sna.dgs_render_append_geometry_node_modifier_c2492"
    bl_label = "3DGS Render: Append Geometry Node Modifier"
    bl_description = "Adds a geometry node modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}
    sna_node_group_name: bpy.props.StringProperty(name='Node Group Name', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)
    sna_modifier_name: bpy.props.StringProperty(name='Modifier Name', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.view_layer.objects.active.type == 'MESH' or bpy.context.view_layer.objects.active.type == 'CURVE'):
            created_modifier_0_7a9a7 = sna_append_and_add_geo_nodes_function_execute_6BCD7(self.sna_node_group_name, self.sna_node_group_name, bpy.context.view_layer.objects.active)
            for i_1A879 in range(len(bpy.context.view_layer.objects.active.modifiers)):
                if (bpy.context.view_layer.objects.active.modifiers[i_1A879] == created_modifier_0_7a9a7):
                    bpy.context.view_layer.objects.active.modifiers.move(from_index=i_1A879, to_index=0, )
        else:
            self.report({'INFO'}, message='The Active Object is not a mesh or curve object.')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_Cb703(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_higher_sh_attributes_cb703"
    bl_label = "3DGS Render: Remove Higher SH Attributes"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        TARGET_OBJECT_NAME = bpy.context.view_layer.objects.active.name
        import bmesh
        # ===== GLOBAL INPUT VARIABLES - EDIT THESE =====
        MODE = "remove_named"  # Options: "remove_active", "remove_selected", "remove_named", "list_attributes"
        #TARGET_OBJECT_NAME = ""  # Only used when MODE = "remove_named" - leave empty to use active object
        VERBOSE_OUTPUT = False    # Set to False for minimal console output
        # Additional f_rest patterns to search for (add your specific naming conventions here)
        CUSTOM_F_REST_PATTERNS = [
            # Add any custom patterns your 3DGS implementation uses
            # Examples: "custom_sh_rest", "features_rest", etc.
        ]
        # ===== SCRIPT FUNCTIONS =====

        def remove_f_rest_attributes(obj: Optional[bpy.types.Object] = None) -> dict:
            """
            Remove SH f_rest attributes from a 3DGS object while keeping other 3DGS attributes.
            Args:
                obj: Target object. If None, uses the active object.
            Returns:
                dict: Summary of removed attributes and operation status
            """
            # Get target object
            if obj is None:
                obj = bpy.context.active_object
            if obj is None:
                return {
                    "success": False,
                    "error": "No object provided and no active object found",
                    "removed_attributes": []
                }
            if obj.type != 'MESH':
                return {
                    "success": False,
                    "error": f"Object '{obj.name}' is not a mesh object",
                    "removed_attributes": []
                }
            mesh = obj.data
            removed_attributes = []
            # Common f_rest attribute naming patterns in 3DGS implementations
            f_rest_patterns = [
                "f_rest",           # Simple naming
                "f_rest_0",         # Indexed naming
                "f_rest_1", 
                "f_rest_2",
                "sh_rest",          # Alternative naming
                "sh_features_rest", # Another common pattern
                "spherical_harmonics_rest",
            ]
            # Add custom patterns from global variables
            f_rest_patterns.extend(CUSTOM_F_REST_PATTERNS)
            # Also check for numbered f_rest attributes (up to reasonable limit)
            for i in range(50):  # Adjust range based on your SH degree
                f_rest_patterns.extend([
                    f"f_rest_{i}",
                    f"sh_rest_{i}",
                    f"f_rest_{i:02d}",  # Zero-padded
                ])
            # Get list of attribute names to check
            attribute_names = list(mesh.attributes.keys())
            # Remove f_rest attributes
            for attr_name in attribute_names:
                # Check if attribute name matches f_rest patterns
                is_f_rest = False
                # Direct pattern matching
                if attr_name in f_rest_patterns:
                    is_f_rest = True
                # Pattern matching for variations
                attr_lower = attr_name.lower()
                if any(pattern in attr_lower for pattern in ["f_rest", "sh_rest", "spherical_harmonics_rest"]):
                    # Additional check to avoid false positives
                    if not any(keep_pattern in attr_lower for keep_pattern in ["f_dc", "position", "scale", "rotation", "opacity"]):
                        is_f_rest = True
                if is_f_rest:
                    try:
                        mesh.attributes.remove(mesh.attributes[attr_name])
                        removed_attributes.append(attr_name)
                        if VERBOSE_OUTPUT:
                            print(f"Removed attribute: {attr_name}")
                    except Exception as e:
                        print(f"Failed to remove attribute '{attr_name}': {e}")
            # Update the mesh
            mesh.update()
            return {
                "success": True,
                "object_name": obj.name,
                "removed_attributes": removed_attributes,
                "remaining_attributes": list(mesh.attributes.keys())
            }

        def remove_f_rest_from_selected() -> None:
            """Remove f_rest attributes from all selected mesh objects."""
            selected_meshes = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
            if not selected_meshes:
                print("No mesh objects selected")
                return
            total_removed = 0
            for obj in selected_meshes:
                result = remove_f_rest_attributes(obj)
                if result["success"]:
                    total_removed += len(result["removed_attributes"])
                    print(f"✓ Processed '{result['object_name']}': removed {len(result['removed_attributes'])} f_rest attributes")
                    if VERBOSE_OUTPUT and result["removed_attributes"]:
                        print(f"  Removed: {', '.join(result['removed_attributes'])}")
                else:
                    print(f"✗ Failed to process '{obj.name}': {result['error']}")
            print(f"\nTotal f_rest attributes removed across all objects: {total_removed}")

        def list_3dgs_attributes(obj: Optional[bpy.types.Object] = None) -> dict:
            """
            List all attributes on an object, categorizing them as 3DGS-related or other.
            Args:
                obj: Target object. If None, uses the active object.
            Returns:
                dict: Categorized attribute information
            """
            if obj is None:
                obj = bpy.context.active_object
            if obj is None or obj.type != 'MESH':
                return {"error": "No valid mesh object"}
            mesh = obj.data
            all_attributes = list(mesh.attributes.keys())
            # Categorize attributes
            f_dc_attrs = [name for name in all_attributes if "f_dc" in name.lower()]
            f_rest_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["f_rest", "sh_rest"])]
            position_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["position", "pos", "xyz"])]
            scale_attrs = [name for name in all_attributes if "scale" in name.lower()]
            rotation_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["rotation", "rot", "quaternion", "quat"])]
            opacity_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["opacity", "alpha"])]
            known_3dgs = f_dc_attrs + f_rest_attrs + position_attrs + scale_attrs + rotation_attrs + opacity_attrs
            other_attrs = [name for name in all_attributes if name not in known_3dgs]
            return {
                "object_name": obj.name,
                "total_attributes": len(all_attributes),
                "f_dc": f_dc_attrs,
                "f_rest": f_rest_attrs,
                "position": position_attrs,
                "scale": scale_attrs,
                "rotation": rotation_attrs,
                "opacity": opacity_attrs,
                "other": other_attrs
            }
        # ===== MAIN EXECUTION =====
        print("=== 3DGS f_rest Attribute Removal Script ===")
        print(f"Mode: {MODE}")
        if MODE == "remove_active":
            print("Removing f_rest attributes from active object...")
            result = remove_f_rest_attributes()
            if result["success"]:
                print(f"✓ Successfully processed '{result['object_name']}'")
                print(f"Removed {len(result['removed_attributes'])} f_rest attributes")
                if VERBOSE_OUTPUT and result["removed_attributes"]:
                    print(f"Removed attributes: {', '.join(result['removed_attributes'])}")
                if VERBOSE_OUTPUT:
                    print(f"Remaining attributes: {', '.join(result['remaining_attributes'])}")
            else:
                print(f"✗ Error: {result['error']}")
        elif MODE == "remove_selected":
            print("Removing f_rest attributes from all selected objects...")
            remove_f_rest_from_selected()
        elif MODE == "remove_named":
            if not TARGET_OBJECT_NAME:
                print("✗ Error: TARGET_OBJECT_NAME must be specified when using 'remove_named' mode")
            else:
                target_obj = bpy.data.objects.get(TARGET_OBJECT_NAME)
                if target_obj is None:
                    print(f"✗ Error: Object '{TARGET_OBJECT_NAME}' not found")
                else:
                    print(f"Removing f_rest attributes from object '{TARGET_OBJECT_NAME}'...")
                    result = remove_f_rest_attributes(target_obj)
                    if result["success"]:
                        print(f"✓ Successfully processed '{result['object_name']}'")
                        print(f"Removed {len(result['removed_attributes'])} f_rest attributes")
                        if VERBOSE_OUTPUT and result["removed_attributes"]:
                            print(f"Removed attributes: {', '.join(result['removed_attributes'])}")
                        if VERBOSE_OUTPUT:
                            print(f"Remaining attributes: {', '.join(result['remaining_attributes'])}")
                    else:
                        print(f"✗ Error: {result['error']}")
        elif MODE == "list_attributes":
            target_obj = None
            if TARGET_OBJECT_NAME:
                target_obj = bpy.data.objects.get(TARGET_OBJECT_NAME)
                if target_obj is None:
                    print(f"Warning: Object '{TARGET_OBJECT_NAME}' not found, using active object instead")
            print("Listing 3DGS attributes...")
            attr_info = list_3dgs_attributes(target_obj)
            if "error" not in attr_info:
                print(f"\n=== Attribute Summary for '{attr_info['object_name']}' ===")
                print(f"Total attributes: {attr_info['total_attributes']}")
                print(f"f_dc attributes ({len(attr_info['f_dc'])}): {attr_info['f_dc']}")
                print(f"f_rest attributes ({len(attr_info['f_rest'])}): {attr_info['f_rest']}")
                print(f"Position attributes ({len(attr_info['position'])}): {attr_info['position']}")
                print(f"Scale attributes ({len(attr_info['scale'])}): {attr_info['scale']}")
                print(f"Rotation attributes ({len(attr_info['rotation'])}): {attr_info['rotation']}")
                print(f"Opacity attributes ({len(attr_info['opacity'])}): {attr_info['opacity']}")
                print(f"Other attributes ({len(attr_info['other'])}): {attr_info['other']}")
            else:
                print(f"✗ Error: {attr_info['error']}")
        else:
            print(f"✗ Error: Unknown mode '{MODE}'")
            print("Valid modes: 'remove_active', 'remove_selected', 'remove_named', 'list_attributes'")
        print("=== Script Complete ===")
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_DCA59 = layout.box()
        box_DCA59.alert = False
        box_DCA59.enabled = True
        box_DCA59.active = True
        box_DCA59.use_property_split = False
        box_DCA59.use_property_decorate = False
        box_DCA59.alignment = 'Expand'.upper()
        box_DCA59.scale_x = 1.0
        box_DCA59.scale_y = 1.0
        if not True: box_DCA59.operator_context = "EXEC_DEFAULT"
        box_DCA59.label(text='This action is destructive and not reversible', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_DCA59.label(text='Removing higher SH attributes can save memory and increase performance in some areas.', icon_value=0)
        box_DCA59.label(text='If you are unsure about what to do, try working on a duplicate.', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_OT_Dgs_Render_Remove_Adjust_Attributes_Modifier_Fbc71(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_adjust_attributes_modifier_fbc71"
    bl_label = "3DGS Render: Remove Adjust Attributes Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Apply_Adjust_Attributes_Modifier_Aefe7(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_adjust_attributes_modifier_aefe7"
    bl_label = "3DGS Render: Apply Adjust Attributes Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Adjust_Attributes_GN'
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


class SNA_OT_Dgs_Render_Remove_Adjust_Attribute_Modifier_C5491(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_adjust_attribute_modifier_c5491"
    bl_label = "3DGS Render: Remove Adjust Attribute Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Attributes_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Apply_Adjust_Attribute_Modifier_B24A5(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_adjust_attribute_modifier_b24a5"
    bl_label = "3DGS Render: Apply Adjust Attribute Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Adjust_Attributes_GN'
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


class SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_86F09(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_higher_sh_attributes_86f09"
    bl_label = "3DGS Render: Remove Higher SH Attributes"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        TARGET_OBJECT_NAME = bpy.context.view_layer.objects.active.name
        import bmesh
        # ===== GLOBAL INPUT VARIABLES - EDIT THESE =====
        MODE = "remove_named"  # Options: "remove_active", "remove_selected", "remove_named", "list_attributes"
        #TARGET_OBJECT_NAME = ""  # Only used when MODE = "remove_named" - leave empty to use active object
        VERBOSE_OUTPUT = False    # Set to False for minimal console output
        # Additional f_rest patterns to search for (add your specific naming conventions here)
        CUSTOM_F_REST_PATTERNS = [
            # Add any custom patterns your 3DGS implementation uses
            # Examples: "custom_sh_rest", "features_rest", etc.
        ]
        # ===== SCRIPT FUNCTIONS =====

        def remove_f_rest_attributes(obj: Optional[bpy.types.Object] = None) -> dict:
            """
            Remove SH f_rest attributes from a 3DGS object while keeping other 3DGS attributes.
            Args:
                obj: Target object. If None, uses the active object.
            Returns:
                dict: Summary of removed attributes and operation status
            """
            # Get target object
            if obj is None:
                obj = bpy.context.active_object
            if obj is None:
                return {
                    "success": False,
                    "error": "No object provided and no active object found",
                    "removed_attributes": []
                }
            if obj.type != 'MESH':
                return {
                    "success": False,
                    "error": f"Object '{obj.name}' is not a mesh object",
                    "removed_attributes": []
                }
            mesh = obj.data
            removed_attributes = []
            # Common f_rest attribute naming patterns in 3DGS implementations
            f_rest_patterns = [
                "f_rest",           # Simple naming
                "f_rest_0",         # Indexed naming
                "f_rest_1", 
                "f_rest_2",
                "sh_rest",          # Alternative naming
                "sh_features_rest", # Another common pattern
                "spherical_harmonics_rest",
            ]
            # Add custom patterns from global variables
            f_rest_patterns.extend(CUSTOM_F_REST_PATTERNS)
            # Also check for numbered f_rest attributes (up to reasonable limit)
            for i in range(50):  # Adjust range based on your SH degree
                f_rest_patterns.extend([
                    f"f_rest_{i}",
                    f"sh_rest_{i}",
                    f"f_rest_{i:02d}",  # Zero-padded
                ])
            # Get list of attribute names to check
            attribute_names = list(mesh.attributes.keys())
            # Remove f_rest attributes
            for attr_name in attribute_names:
                # Check if attribute name matches f_rest patterns
                is_f_rest = False
                # Direct pattern matching
                if attr_name in f_rest_patterns:
                    is_f_rest = True
                # Pattern matching for variations
                attr_lower = attr_name.lower()
                if any(pattern in attr_lower for pattern in ["f_rest", "sh_rest", "spherical_harmonics_rest"]):
                    # Additional check to avoid false positives
                    if not any(keep_pattern in attr_lower for keep_pattern in ["f_dc", "position", "scale", "rotation", "opacity"]):
                        is_f_rest = True
                if is_f_rest:
                    try:
                        mesh.attributes.remove(mesh.attributes[attr_name])
                        removed_attributes.append(attr_name)
                        if VERBOSE_OUTPUT:
                            print(f"Removed attribute: {attr_name}")
                    except Exception as e:
                        print(f"Failed to remove attribute '{attr_name}': {e}")
            # Update the mesh
            mesh.update()
            return {
                "success": True,
                "object_name": obj.name,
                "removed_attributes": removed_attributes,
                "remaining_attributes": list(mesh.attributes.keys())
            }

        def remove_f_rest_from_selected() -> None:
            """Remove f_rest attributes from all selected mesh objects."""
            selected_meshes = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
            if not selected_meshes:
                print("No mesh objects selected")
                return
            total_removed = 0
            for obj in selected_meshes:
                result = remove_f_rest_attributes(obj)
                if result["success"]:
                    total_removed += len(result["removed_attributes"])
                    print(f"✓ Processed '{result['object_name']}': removed {len(result['removed_attributes'])} f_rest attributes")
                    if VERBOSE_OUTPUT and result["removed_attributes"]:
                        print(f"  Removed: {', '.join(result['removed_attributes'])}")
                else:
                    print(f"✗ Failed to process '{obj.name}': {result['error']}")
            print(f"\nTotal f_rest attributes removed across all objects: {total_removed}")

        def list_3dgs_attributes(obj: Optional[bpy.types.Object] = None) -> dict:
            """
            List all attributes on an object, categorizing them as 3DGS-related or other.
            Args:
                obj: Target object. If None, uses the active object.
            Returns:
                dict: Categorized attribute information
            """
            if obj is None:
                obj = bpy.context.active_object
            if obj is None or obj.type != 'MESH':
                return {"error": "No valid mesh object"}
            mesh = obj.data
            all_attributes = list(mesh.attributes.keys())
            # Categorize attributes
            f_dc_attrs = [name for name in all_attributes if "f_dc" in name.lower()]
            f_rest_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["f_rest", "sh_rest"])]
            position_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["position", "pos", "xyz"])]
            scale_attrs = [name for name in all_attributes if "scale" in name.lower()]
            rotation_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["rotation", "rot", "quaternion", "quat"])]
            opacity_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["opacity", "alpha"])]
            known_3dgs = f_dc_attrs + f_rest_attrs + position_attrs + scale_attrs + rotation_attrs + opacity_attrs
            other_attrs = [name for name in all_attributes if name not in known_3dgs]
            return {
                "object_name": obj.name,
                "total_attributes": len(all_attributes),
                "f_dc": f_dc_attrs,
                "f_rest": f_rest_attrs,
                "position": position_attrs,
                "scale": scale_attrs,
                "rotation": rotation_attrs,
                "opacity": opacity_attrs,
                "other": other_attrs
            }
        # ===== MAIN EXECUTION =====
        print("=== 3DGS f_rest Attribute Removal Script ===")
        print(f"Mode: {MODE}")
        if MODE == "remove_active":
            print("Removing f_rest attributes from active object...")
            result = remove_f_rest_attributes()
            if result["success"]:
                print(f"✓ Successfully processed '{result['object_name']}'")
                print(f"Removed {len(result['removed_attributes'])} f_rest attributes")
                if VERBOSE_OUTPUT and result["removed_attributes"]:
                    print(f"Removed attributes: {', '.join(result['removed_attributes'])}")
                if VERBOSE_OUTPUT:
                    print(f"Remaining attributes: {', '.join(result['remaining_attributes'])}")
            else:
                print(f"✗ Error: {result['error']}")
        elif MODE == "remove_selected":
            print("Removing f_rest attributes from all selected objects...")
            remove_f_rest_from_selected()
        elif MODE == "remove_named":
            if not TARGET_OBJECT_NAME:
                print("✗ Error: TARGET_OBJECT_NAME must be specified when using 'remove_named' mode")
            else:
                target_obj = bpy.data.objects.get(TARGET_OBJECT_NAME)
                if target_obj is None:
                    print(f"✗ Error: Object '{TARGET_OBJECT_NAME}' not found")
                else:
                    print(f"Removing f_rest attributes from object '{TARGET_OBJECT_NAME}'...")
                    result = remove_f_rest_attributes(target_obj)
                    if result["success"]:
                        print(f"✓ Successfully processed '{result['object_name']}'")
                        print(f"Removed {len(result['removed_attributes'])} f_rest attributes")
                        if VERBOSE_OUTPUT and result["removed_attributes"]:
                            print(f"Removed attributes: {', '.join(result['removed_attributes'])}")
                        if VERBOSE_OUTPUT:
                            print(f"Remaining attributes: {', '.join(result['remaining_attributes'])}")
                    else:
                        print(f"✗ Error: {result['error']}")
        elif MODE == "list_attributes":
            target_obj = None
            if TARGET_OBJECT_NAME:
                target_obj = bpy.data.objects.get(TARGET_OBJECT_NAME)
                if target_obj is None:
                    print(f"Warning: Object '{TARGET_OBJECT_NAME}' not found, using active object instead")
            print("Listing 3DGS attributes...")
            attr_info = list_3dgs_attributes(target_obj)
            if "error" not in attr_info:
                print(f"\n=== Attribute Summary for '{attr_info['object_name']}' ===")
                print(f"Total attributes: {attr_info['total_attributes']}")
                print(f"f_dc attributes ({len(attr_info['f_dc'])}): {attr_info['f_dc']}")
                print(f"f_rest attributes ({len(attr_info['f_rest'])}): {attr_info['f_rest']}")
                print(f"Position attributes ({len(attr_info['position'])}): {attr_info['position']}")
                print(f"Scale attributes ({len(attr_info['scale'])}): {attr_info['scale']}")
                print(f"Rotation attributes ({len(attr_info['rotation'])}): {attr_info['rotation']}")
                print(f"Opacity attributes ({len(attr_info['opacity'])}): {attr_info['opacity']}")
                print(f"Other attributes ({len(attr_info['other'])}): {attr_info['other']}")
            else:
                print(f"✗ Error: {attr_info['error']}")
        else:
            print(f"✗ Error: Unknown mode '{MODE}'")
            print("Valid modes: 'remove_active', 'remove_selected', 'remove_named', 'list_attributes'")
        print("=== Script Complete ===")
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_8FEFB = layout.box()
        box_8FEFB.alert = False
        box_8FEFB.enabled = True
        box_8FEFB.active = True
        box_8FEFB.use_property_split = False
        box_8FEFB.use_property_decorate = False
        box_8FEFB.alignment = 'Expand'.upper()
        box_8FEFB.scale_x = 1.0
        box_8FEFB.scale_y = 1.0
        if not True: box_8FEFB.operator_context = "EXEC_DEFAULT"
        box_8FEFB.label(text='This action is destructive and not reversible', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_8FEFB.label(text='Removing higher SH attributes (f_rest attributes) can save memory and increase performance in some areas.', icon_value=0)
        box_8FEFB.label(text='If you are unsure about what to do, try working on a duplicate.', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_OT_Dgs_Render_Remove_Camera_Cull_Modifier_F15Ee(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_camera_cull_modifier_f15ee"
    bl_label = "3DGS Render: Remove Camera Cull Modifier"
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


class SNA_OT_Dgs_Render_Auto_Set_Up_Camera_Cull_Properties_Aef48(bpy.types.Operator):
    bl_idname = "sna.dgs_render_auto_set_up_camera_cull_properties_aef48"
    bl_label = "3DGS Render: Auto Set Up Camera Cull Properties"
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


class SNA_OT_Dgs_Render_Apply_Camera_Cull_Modifier_7C6F7(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_camera_cull_modifier_7c6f7"
    bl_label = "3DGS Render: Apply Camera Cull Modifier"
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


class SNA_OT_Dgs_Render_Remove_Colour_Edit_Modifier_6255F(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_colour_edit_modifier_6255f"
    bl_label = "3DGS Render: Remove Colour Edit Modifier"
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


class SNA_OT_Dgs_Render_Apply_Colour_Edit_Modifier_C83C4(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_colour_edit_modifier_c83c4"
    bl_label = "3DGS Render: Apply Colour Edit Modifier"
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


class SNA_OT_Dgs_Render_Remove_Convert_To_Rough_Mesh_Modifier_A8C4C(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_convert_to_rough_mesh_modifier_a8c4c"
    bl_label = "3DGS Render: Remove Convert To Rough Mesh Modifier"
    bl_description = "Removes the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Convert_To_Rough_Mesh_GN'], )
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Apply_Convert_To_Rough_Mesh_Modifier_9F4B2(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_convert_to_rough_mesh_modifier_9f4b2"
    bl_label = "3DGS Render: Apply Convert To Rough Mesh Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Convert_To_Rough_Mesh_GN'
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
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


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
        op.sna_create_duplicate_and_remove_other_modifiers = True


class SNA_OT_Dgs_Render_Append_Rough_Mesh_Modifier_65Da3(bpy.types.Operator):
    bl_idname = "sna.dgs_render_append_rough_mesh_modifier_65da3"
    bl_label = "3DGS Render: Append Rough Mesh Modifier"
    bl_description = "Adds a Rough Mesh modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}
    sna_create_duplicate_and_remove_other_modifiers: bpy.props.BoolProperty(name='Create duplicate and remove other modifiers', description='', options={'HIDDEN'}, default=True)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.view_layer.objects.active.type == 'MESH' or bpy.context.view_layer.objects.active.type == 'CURVE'):
            if self.sna_create_duplicate_and_remove_other_modifiers:
                source_obj_name = bpy.context.view_layer.objects.active.name
                # Input variables
                #source_obj_name = "Cube"  # Change this to your object's name
                offset_x = 0.0  # Input float variable for X offset
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
                    # Clear current selection
                    bpy.ops.object.select_all(action='DESELECT')
                    # Select and activate the new object
                    new_obj.select_set(True)
                    bpy.context.view_layer.objects.active = new_obj
                    # Store the new object's name in a variable
                    new_object_name = new_obj.name
                    # Output the new object for Serpens (return the actual object)
                    output_object = new_obj
                else:
                    new_object_name = "ERROR: Source object not found"
                    output_object = None
                # Output the new object's name (this will be captured by Serpens)
                print(new_object_name)
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
                    bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
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
            else:
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
                    bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
            created_modifier_0_827c5 = sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Convert_To_Rough_Mesh_GN', 'KIRI_3DGS_Convert_To_Rough_Mesh_GN', bpy.context.view_layer.objects.active)
            for i_1EB8C in range(len(bpy.context.view_layer.objects.active.modifiers)):
                if (bpy.context.view_layer.objects.active.modifiers[i_1EB8C] == created_modifier_0_827c5):
                    bpy.context.view_layer.objects.active.modifiers.move(from_index=i_1EB8C, to_index=0, )
                    bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
        else:
            self.report({'INFO'}, message='The Active Object is not a mesh or curve object.')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_F6B46 = layout.box()
        box_F6B46.alert = False
        box_F6B46.enabled = True
        box_F6B46.active = True
        box_F6B46.use_property_split = False
        box_F6B46.use_property_decorate = False
        box_F6B46.alignment = 'Expand'.upper()
        box_F6B46.scale_x = 1.0
        box_F6B46.scale_y = 1.0
        if not True: box_F6B46.operator_context = "EXEC_DEFAULT"
        box_F6B46.prop(self, 'sna_create_duplicate_and_remove_other_modifiers', text='Create duplicate and remove other modifiers', icon_value=0, emboss=True)
        box_F6B46.label(text='The 3DGS Render modifier will have Camera Updates disabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


class SNA_OT_Dgs_Render_Remove_Crop_Box_Modifier_64Ea6(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_crop_box_modifier_64ea6"
    bl_label = "3DGS Render: Remove Crop Box Modifier"
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


class SNA_OT_Dgs_Render_Apply_Crop_Box_Modifier_Bfdca(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_crop_box_modifier_bfdca"
    bl_label = "3DGS Render: Apply Crop Box Modifier"
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
            col_3D26B.prop_search(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Crop_Box_GN'], '["Socket_18"]', bpy.data, 'collections', text='collection', icon='NONE')
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


class SNA_OT_Dgs_Render_Remove_Decimate_Modifier_Fff1B(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_decimate_modifier_fff1b"
    bl_label = "3DGS Render: Remove Decimate Modifier"
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


class SNA_OT_Dgs_Render_Apply_Decimate_Modifier_7A32C(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_decimate_modifier_7a32c"
    bl_label = "3DGS Render: Apply Decimate Modifier"
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


class SNA_OT_Dgs_Render_Remove_Remove_By_Size_Modifier_3A0E5(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_remove_by_size_modifier_3a0e5"
    bl_label = "3DGS Render: Remove Remove By Size Modifier"
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


class SNA_OT_Dgs_Render_Apply_Remove_By_Size_Modifier_6Dbab(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_remove_by_size_modifier_6dbab"
    bl_label = "3DGS Render: Apply Remove By Size Modifier"
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


class SNA_GROUP_sna_dgs_scene_properties_group(bpy.types.PropertyGroup):
    active_mode: bpy.props.EnumProperty(name='Active Mode', description='', items=[('Edit', 'Edit', '', 0, 0), ('Render', 'Render', '', 0, 1), ('Mesh 2 3DGS', 'Mesh 2 3DGS', '', 0, 2)], update=sna_update_active_mode_7EB87)
    edit_mode_active_menu: bpy.props.EnumProperty(name='Edit Mode Active Menu', description='', items=[('Import', 'Import', '', 0, 0), ('Modifiers', 'Modifiers', '', 0, 1), ('Colour', 'Colour', '', 0, 2), ('Animate', 'Animate', '', 0, 3), ('HQ / LQ', 'HQ / LQ', '', 0, 4), ('Export', 'Export', '', 0, 5)])
    active_shading_menu: bpy.props.EnumProperty(name='Active Shading Menu', description='', items=[('Selective 1', 'Selective 1', '', 0, 0), ('Selective 2', 'Selective 2', '', 0, 1), ('Selective 3', 'Selective 3', '', 0, 2), ('Vertex Paint', 'Vertex Paint', '', 0, 3), ('Image Overlay', 'Image Overlay', '', 0, 4)])
    hq_objects_overlap: bpy.props.BoolProperty(name='HQ Objects Overlap', description='', default=False, update=sna_update_hq_objects_overlap_DDF15)
    import_faces_or_verts: bpy.props.EnumProperty(name='Import Faces Or Verts', description='', items=[('Verts', 'Verts', '', 0, 0), ('Faces', 'Faces', '', 0, 1)])
    import_uv_reset: bpy.props.BoolProperty(name='Import UV reset', description='', default=False)
    import_create_proxy_object: bpy.props.BoolProperty(name='Import Create Proxy Object', description='', default=True)
    mesh2gs_validate_files: bpy.props.BoolProperty(name='MESH2GS Validate Files', description='', default=False)
    show_tips: bpy.props.BoolProperty(name='Show Tips', description='', default=False)
    render_2_refresh_selected_only: bpy.props.BoolProperty(name='RENDER 2 Refresh Selected Only', description='', default=False)
    render_2_copy_source_transforms: bpy.props.BoolProperty(name='RENDER_2_Copy Source Transforms', description='', default=True)
    render_2_render_animation: bpy.props.BoolProperty(name='RENDER_2_Render Animation', description='', default=False)
    render_2_render_color: bpy.props.BoolProperty(name='RENDER_2_Render Color', description='', default=True)
    render_2_render_depth: bpy.props.BoolProperty(name='RENDER_2_Render Depth', description='', default=False)
    render_2_comp_with_temp: bpy.props.BoolProperty(name='RENDER_2_Comp_With_Temp', description='', default=False)
    render_2_interface_mode: bpy.props.EnumProperty(name='RENDER_2_Interface_Mode', description='', items=[('Update', 'Update', '', 0, 0), ('Render', 'Render', '', 0, 1), ('Create', 'Create', '', 0, 2), ('Clean Up', 'Clean Up', '', 0, 3)])
    render_2_remove_all_empties: bpy.props.BoolProperty(name='RENDER_2_Remove All Empties', description='', default=False)
    render_2_interval_or_single_update: bpy.props.EnumProperty(name='RENDER_2_Interval_Or_Single_Update', description='', items=[('Single Time', 'Single Time', '', 0, 0), ('Interval Update', 'Interval Update', '', 0, 1)])
    render_2_interval_stop: bpy.props.BoolProperty(name='RENDER_2_Interval_Stop', description='', default=False)
    render_2_interval_time: bpy.props.FloatProperty(name='RENDER_2_Interval_Time', description='', default=0.10000000149011612, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    render_2_hide_object_on_menu_change: bpy.props.BoolProperty(name='RENDER_2_Hide_Object_On_Menu_Change', description='', default=True)


class SNA_GROUP_sna_dgs_object_properties_group(bpy.types.PropertyGroup):
    active_object_update_mode: bpy.props.EnumProperty(name='Active Object Update Mode', description='', items=[('Disable Camera Updates', 'Disable Camera Updates', '', 0, 0), ('Enable Camera Updates', 'Enable Camera Updates', '', 0, 1), ('Show As Point Cloud', 'Show As Point Cloud', '', 0, 2)], update=sna_update_active_object_update_mode_868D4)
    enable_active_camera_updates: bpy.props.BoolProperty(name='Enable Active Camera Updates', description='', default=False, update=sna_update_enable_active_camera_updates_DE26E)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_GROUP_sna_dgs_scene_properties_group)
    bpy.utils.register_class(SNA_GROUP_sna_dgs_object_properties_group)
    bpy.types.Scene.sna_kiri3dgs_render_2_use_source_modifiers = bpy.props.BoolProperty(name='KIRI3DGS_RENDER_2_Use_Source_Modifiers', description='', default=True)
    bpy.types.Scene.sna_dgs_scene_properties = bpy.props.PointerProperty(name='3DGS Scene Properties', description='', type=SNA_GROUP_sna_dgs_scene_properties_group)
    bpy.types.Object.sna_dgs_object_properties = bpy.props.PointerProperty(name='3DGS Object Properties', description='', type=SNA_GROUP_sna_dgs_object_properties_group)
    bpy.types.Material.sna_lq__hq = bpy.props.EnumProperty(name='LQ - HQ', description='', items=[('LQ Mode (Dithered Alpha)', 'LQ Mode (Dithered Alpha)', '', 0, 0), ('HQ Mode (Blended Alpha)', 'HQ Mode (Blended Alpha)', '', 0, 1)], update=sna_update_sna_lq__hq_9D2FF)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Launch_Kiri_Site_Bf973)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Launch_Superhive_Store_08F23)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Launch_Kiri_Blender_Addons_Page_9D58C)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Open_Documentation_3A04F)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Open_Tutorial_Video_0684A)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Align_Active_To_X_Axis_6Ae0E)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Align_Active_To_Y_Axis_C305D)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Align_Active_To_Z_Axis_1E184)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Align_Active_To_View_30B13)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Animate_Modifier_5B34D)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Animate_Modifier_3938E)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Add_Animate_Modifier_39C55)
    bpy.types.VIEW3D_MT_object_apply.prepend(sna_add_to_view3d_mt_object_apply_3CED8)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Import_Image_Overlay_4A457)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Start_Vertex_Painting_A36E0)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Refresh__Create_Paint_Attribute_84655)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Export_Mesh_Object_As_3Dgs_Ply_Ce2F7)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Generate_Hq_Object_55455)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Disable_Hq_Overlap_34678)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Update_Enabled_3Dgs_Objects_6D7F4)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Mesh23Dgs_3Dfed)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Auto_Generate_Crop_Object_F20D5)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Import_Ply_E0A3A)
    bpy.utils.register_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_6D2B1)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Refresh_Scene_C0B35)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_D5B41)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Advanced_Render_Ba196)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Clean_Up_Advanced_Render_Scene_09450)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Stop_Interval_Updates_5Ac80)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Append_Wire_Sphere_2Bf63)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Append_Wire_Cube_56E0F)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Append_Geometry_Node_Modifier_C2492)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_Cb703)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Adjust_Attributes_Modifier_Fbc71)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Adjust_Attributes_Modifier_Aefe7)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Adjust_Attribute_Modifier_C5491)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Adjust_Attribute_Modifier_B24A5)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_86F09)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Camera_Cull_Modifier_F15Ee)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Auto_Set_Up_Camera_Cull_Properties_Aef48)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Camera_Cull_Modifier_7C6F7)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Colour_Edit_Modifier_6255F)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Colour_Edit_Modifier_C83C4)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Convert_To_Rough_Mesh_Modifier_A8C4C)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Convert_To_Rough_Mesh_Modifier_9F4B2)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Append_Rough_Mesh_Modifier_65Da3)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Crop_Box_Modifier_64Ea6)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Crop_Box_Modifier_Bfdca)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Decimate_Modifier_Fff1B)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Decimate_Modifier_7A32C)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Remove_Remove_By_Size_Modifier_3A0E5)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_Remove_By_Size_Modifier_6Dbab)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Material.sna_lq__hq
    del bpy.types.Object.sna_dgs_object_properties
    del bpy.types.Scene.sna_dgs_scene_properties
    del bpy.types.Scene.sna_kiri3dgs_render_2_use_source_modifiers
    bpy.utils.unregister_class(SNA_GROUP_sna_dgs_object_properties_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_dgs_scene_properties_group)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Launch_Kiri_Site_Bf973)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Launch_Superhive_Store_08F23)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Launch_Kiri_Blender_Addons_Page_9D58C)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Open_Documentation_3A04F)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Open_Tutorial_Video_0684A)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Align_Active_To_X_Axis_6Ae0E)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Align_Active_To_Y_Axis_C305D)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Align_Active_To_Z_Axis_1E184)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Align_Active_To_View_30B13)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Animate_Modifier_5B34D)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Animate_Modifier_3938E)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Add_Animate_Modifier_39C55)
    bpy.types.VIEW3D_MT_object_apply.remove(sna_add_to_view3d_mt_object_apply_3CED8)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Import_Image_Overlay_4A457)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Start_Vertex_Painting_A36E0)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Refresh__Create_Paint_Attribute_84655)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Export_Mesh_Object_As_3Dgs_Ply_Ce2F7)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Generate_Hq_Object_55455)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Disable_Hq_Overlap_34678)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Update_Enabled_3Dgs_Objects_6D7F4)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Mesh23Dgs_3Dfed)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Auto_Generate_Crop_Object_F20D5)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Import_Ply_E0A3A)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_6D2B1)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Refresh_Scene_C0B35)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_D5B41)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Advanced_Render_Ba196)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Clean_Up_Advanced_Render_Scene_09450)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Stop_Interval_Updates_5Ac80)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Append_Wire_Sphere_2Bf63)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Append_Wire_Cube_56E0F)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Append_Geometry_Node_Modifier_C2492)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_Cb703)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Adjust_Attributes_Modifier_Fbc71)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Adjust_Attributes_Modifier_Aefe7)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Adjust_Attribute_Modifier_C5491)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Adjust_Attribute_Modifier_B24A5)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_86F09)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Camera_Cull_Modifier_F15Ee)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Auto_Set_Up_Camera_Cull_Properties_Aef48)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Camera_Cull_Modifier_7C6F7)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Colour_Edit_Modifier_6255F)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Colour_Edit_Modifier_C83C4)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Convert_To_Rough_Mesh_Modifier_A8C4C)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Convert_To_Rough_Mesh_Modifier_9F4B2)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Append_Rough_Mesh_Modifier_65Da3)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Crop_Box_Modifier_64Ea6)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Crop_Box_Modifier_Bfdca)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Decimate_Modifier_Fff1B)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Decimate_Modifier_7A32C)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Remove_Remove_By_Size_Modifier_3A0E5)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_Remove_By_Size_Modifier_6Dbab)
