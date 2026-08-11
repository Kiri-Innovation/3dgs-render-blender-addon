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
    "blender" : (5, 1, 0),
    "version" : (5, 0, 0),
    "location" : "N Panel",
    "warning" : "",
    "doc_url": "https://www.kiriengine.app/blender-addon/3dgs-render", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
import webbrowser
import os
import math
from bpy_extras.io_utils import ImportHelper, ExportHelper
import importlib.util
import types
import subprocess
import sys
import platform
import gpu.state
import numpy as np
import time
import gpu.types
from mathutils import Matrix
import re
from mathutils import Vector
from bpy.app.handlers import persistent
from typing import Optional


addon_keymaps = {}
_icons = None
dgs_render__active_3dgs_object = {'sna_apply_modifier_list': [], 'sna_in_camera_view': False, }
dgs_render__collection_snippets = {'sna_collections_temp_list': [], }
dgs_render__export = {'sna_export_base_object': None, 'sna_export_temp_object': None, 'sna_export_frame_count': 0, }
dgs_render__hq_mode = {'sna_lq_object_list': [], }
dgs_renderdb_filter = {'sna_db_filter_input_object': None, 'sna_db_filter_force_scale_factor': 0.0, }
dgs_on_prop_update_on_render = {'sna_dgs_proxies_in_scene': False, }


def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


from .src import *


def sna_update_update_mode_868D4(self, context):
    sna_updated_prop = self.update_mode
    bpy.context.view_layer.objects.active['update_rot_to_cam'] = (sna_updated_prop == 'Enable Camera Updates')
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = (2 if (sna_updated_prop == 'Show As Point Cloud') else (1 if (sna_updated_prop != 'Enable Camera Updates') else 0))
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport = (True if (sna_updated_prop != 'Disable Camera Updates') else False)
    bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


def sna_update_cam_update_DE26E(self, context):
    sna_updated_prop = self.cam_update
    if sna_updated_prop:
        bpy.context.area.spaces.active.region_3d.view_perspective = 'CAMERA'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop

        def delayed_214CF():
            sna_update_camera_single_time_9EF18()
        bpy.app.timers.register(delayed_214CF, first_interval=0.10000000149011612)
    else:
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop


def sna_update_hq_overlap_DDF15(self, context):
    sna_updated_prop = self.hq_overlap
    if sna_updated_prop:
        pass
    else:
        if (property_exists("bpy.context.scene.objects", globals(), locals()) and 'KIRI_HQ_Merged_Object' in bpy.context.scene.objects):
            bpy.ops.sna.dgs_render_disable_hq_overlap_34678('INVOKE_DEFAULT', )


def sna_update_lq_hq_065F9(self, context):
    sna_updated_prop = self.lq_hq
    self.id_data.surface_render_method = ('BLENDED' if (sna_updated_prop == 'HQ Mode (Blended Alpha)') else 'DITHERED')
    for i_DF01B in range(len(bpy.data.objects)):
        if (property_exists("bpy.data.objects[i_DF01B].modifiers", globals(), locals()) and 'KIRI_3DGS_Sorter_GN' in bpy.data.objects[i_DF01B].modifiers):
            for i_19853 in range(len(bpy.data.objects[i_DF01B].material_slots)):
                if (bpy.data.objects[i_DF01B].material_slots[i_19853].material == self.id_data):
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


def sna_update_active_mode_86E6B(self, context):
    sna_updated_prop = self.active_mode
    if sna_updated_prop == "Edit":
        for i_DE1DF in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_DE1DF].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_DE1DF].modifiers):
                bpy.context.scene.objects[i_DE1DF].modifiers['KIRI_3DGS_Render_GN'].show_viewport = True
                bpy.context.scene.objects[i_DE1DF].modifiers['KIRI_3DGS_Render_GN'].show_render = True
                if (property_exists("bpy.context.scene.objects[i_DE1DF].modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.scene.objects[i_DE1DF].modifiers):
                    bpy.context.scene.objects[i_DE1DF].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = False
                    bpy.context.scene.objects[i_DE1DF].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = False
                    if '3dgs_is_hidden' in bpy.context.scene.objects[i_DE1DF]:
                        bpy.context.scene.objects[i_DE1DF].hide_viewport = bpy.context.scene.objects[i_DE1DF]['3dgs_is_hidden']
                    else:
                        bpy.context.scene.objects[i_DE1DF]['3dgs_is_hidden'] = False
                        bpy.context.view_layer.objects.active.hide_viewport = False
                    if bpy.context.scene.sna_dgs_scene_properties.r2_hide_on_change:
                        target_object = bpy.context.scene.objects[i_DE1DF]
                        hide_set = False
                        # Input variables (Assuming these are passed in from your node setup)
                        # target_object = bpy.data.objects.get("Cube")  # Use .get() instead of [] to avoid KeyErrors!
                        # hide_set = True
                        if target_object:
                            # THE FIX: Verify the object is in the current View Layer
                            if target_object.name in bpy.context.view_layer.objects:
                                target_object.hide_set(hide_set)
                                action = "applied" if hide_set else "removed"
                                print(f"Hide set {action} to: {target_object.name}")
                            else:
                                # Failsafe if the object is in memory but not in the scene
                                print(f"Skipped: '{target_object.name}' exists in data, but is not in the current View Layer.")
                        else:
                            print("Target object not found.")
        sna_clean_up_scene_5F1F1(False)
        if bpy.context.scene.sna_dgs_scene_properties.r2_render_rig_cache_mode == "Enabled Baked":
            sna_rig_5_apply_baked_cache_5656F('All Bound', None)
        else:
            pass
    elif sna_updated_prop == "Render":
        bpy.context.scene.sna_dgs_scene_properties.r2_main_mode = 'Update'
        for i_14280 in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_14280].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_14280].modifiers):
                bpy.context.scene.objects[i_14280].modifiers['KIRI_3DGS_Render_GN'].show_viewport = False
                bpy.context.scene.objects[i_14280].modifiers['KIRI_3DGS_Render_GN'].show_render = False
                bpy.context.scene.objects[i_14280]['3dgs_is_hidden'] = bpy.context.scene.objects[i_14280].hide_viewport
                if bpy.context.scene.sna_dgs_scene_properties.r2_hide_on_change:
                    target_object = bpy.context.scene.objects[i_14280]
                    hide_set = True
                    # Input variables (Assuming these are passed in from your node setup)
                    # target_object = bpy.data.objects.get("Cube")  # Use .get() instead of [] to avoid KeyErrors!
                    # hide_set = True
                    if target_object:
                        # THE FIX: Verify the object is in the current View Layer
                        if target_object.name in bpy.context.view_layer.objects:
                            target_object.hide_set(hide_set)
                            action = "applied" if hide_set else "removed"
                            print(f"Hide set {action} to: {target_object.name}")
                        else:
                            # Failsafe if the object is in memory but not in the scene
                            print(f"Skipped: '{target_object.name}' exists in data, but is not in the current View Layer.")
                    else:
                        print("Target object not found.")
        dgs_on_prop_update_on_render['sna_dgs_proxies_in_scene'] = False
        for i_517A6 in range(len(bpy.context.scene.objects)):
            if 'gaussian_source_uuid' in bpy.context.scene.objects[i_517A6]:
                dgs_on_prop_update_on_render['sna_dgs_proxies_in_scene'] = True
        for i_1DC66 in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_1DC66].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_1DC66].modifiers):
                bpy.context.scene.objects[i_1DC66].hide_viewport = False
        if dgs_on_prop_update_on_render['sna_dgs_proxies_in_scene']:
            if bpy.context.scene.sna_dgs_scene_properties.r2_render_rig_cache_mode == "None":
                sna_c2_refresh_all_4D367(True, bpy.context.scene.sna_dgs_scene_properties.r2_transforms, True)
                sna_shader_system_A4AED()
                sna_texture_creation_FD1B2()
                sna_viewport_render_A3941(bpy.context.scene.sna_dgs_scene_properties.r2_sh_degree, bpy.context.scene.sna_dgs_scene_properties.r2_sort_threshold)
            elif bpy.context.scene.sna_dgs_scene_properties.r2_render_rig_cache_mode == "Enabled Baked":
                sna_rig_5_apply_baked_cache_5656F('All Bound', None)
                sna_clean_up_scene_5F1F1(False)
                sna_shader_system_A4AED()
                sna_texture_creation_FD1B2()
                sna_viewport_render_A3941(bpy.context.scene.sna_dgs_scene_properties.r2_sh_degree, bpy.context.scene.sna_dgs_scene_properties.r2_sort_threshold)
            else:
                pass
    elif sna_updated_prop == "Mesh 2 3DGS":
        sna_clean_up_scene_5F1F1(False)
        bpy.context.view_layer.objects.active = None
    else:
        pass


class SNA_GROUP_sna_dgs_scene_properties_group(bpy.types.PropertyGroup):
    active_mode: bpy.props.EnumProperty(name='Active_Mode', description='', items=[('Edit', 'Edit', '', 0, 0), ('Render', 'Render', '', 0, 1), ('Mesh 2 3DGS', 'Mesh 2 3DGS', '', 0, 2)], update=sna_update_active_mode_86E6B)
    edit_mode_menu: bpy.props.EnumProperty(name='Edit_Mode_Menu', description='', items=[('Import', 'Import', '', 0, 0), ('Modifiers', 'Modifiers', '', 0, 1), ('Colour', 'Colour', '', 0, 2), ('Animate', 'Animate', '', 0, 3), ('HQ / LQ', 'HQ / LQ', '', 0, 4), ('Rig', 'Rig', '', 0, 5), ('Light Bake', 'Light Bake', '', 0, 6), ('Export', 'Export', '', 0, 7)])
    shading_menu: bpy.props.EnumProperty(name='Shading_Menu', description='', items=[('Selective 1', 'Selective 1', '', 0, 0), ('Selective 2', 'Selective 2', '', 0, 1), ('Selective 3', 'Selective 3', '', 0, 2), ('Vertex Paint', 'Vertex Paint', '', 0, 3), ('Image Overlay', 'Image Overlay', '', 0, 4)])
    hq_overlap: bpy.props.BoolProperty(name='HQ_Overlap', description='', default=False, update=sna_update_hq_overlap_DDF15)
    import_face_vert: bpy.props.EnumProperty(name='Import_Face_Vert', description='', items=[('Verts', 'Verts', '', 0, 0), ('Faces', 'Faces', '', 0, 1)])
    import_uv: bpy.props.BoolProperty(name='Import_UV', description='', default=False)
    import_proxy: bpy.props.BoolProperty(name='Import_Proxy', description='', default=False)
    mesh2gs_validate: bpy.props.BoolProperty(name='MESH2GS_Validate', description='', default=False)
    r2_selected: bpy.props.BoolProperty(name='R2_Selected', description='', default=False)
    r2_transforms: bpy.props.BoolProperty(name='R2_Transforms', description='', default=True)
    r2_animation: bpy.props.BoolProperty(name='R2_Animation', description='', default=False)
    r2_color: bpy.props.BoolProperty(name='R2_Color', description='', default=True)
    r2_depth: bpy.props.BoolProperty(name='R2_Depth', description='', default=False)
    r2_comp: bpy.props.BoolProperty(name='R2_Comp', description='', default=False)
    r2_main_mode: bpy.props.EnumProperty(name='R2_Main_Mode', description='', items=[('Update', 'Update', '', 0, 0), ('Render', 'Render', '', 0, 1), ('Create', 'Create', '', 0, 2), ('Clean Up', 'Clean Up', '', 0, 3)])
    r2_clear_empties: bpy.props.BoolProperty(name='R2_Clear_Empties', description='', default=False)
    r2_update_type: bpy.props.EnumProperty(name='R2_Update_Type', description='', items=[('Single', 'Single', '', 0, 0), ('Interval', 'Interval', '', 0, 1)])
    r2_interval_stop: bpy.props.BoolProperty(name='R2_Interval_Stop', description='', default=False)
    r2_interval: bpy.props.FloatProperty(name='R2_Interval', description='', default=0.10000000149011612, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    r2_hide_on_change: bpy.props.BoolProperty(name='R2_Hide_On_Change', description='', default=True)
    r2_delete_temp_files: bpy.props.BoolProperty(name='R2_Delete_Temp_Files', description='', default=False)
    export_single_or_sequence: bpy.props.EnumProperty(name='Export_Single_Or_Sequence', description='', items=[('3DGS', '3DGS', '', 0, 0), ('4DGS', '4DGS', '', 0, 1)])
    export_suffix: bpy.props.StringProperty(name='Export_Suffix', description='', default='_export', subtype='NONE', maxlen=0)
    export_output_path: bpy.props.StringProperty(name='Export_Output_Path', description='', default='', subtype='DIR_PATH', maxlen=0)
    rig_temp_directory: bpy.props.StringProperty(name='RIG_Temp_Directory', description='', default='', subtype='DIR_PATH', maxlen=0)
    rig_update_mode: bpy.props.EnumProperty(name='RIG_Update_Mode', description='', items=[('Single', 'Single', '', 0, 0), ('Interval', 'Interval', '', 0, 1)])
    rig_deform_mode: bpy.props.EnumProperty(name='RIG_Deform_Mode', description='', items=[('Elastic', 'Elastic', '', 0, 0), ('Stable', 'Stable', '', 0, 1), ('Adaptive', 'Adaptive', '', 0, 2)])
    rig_scale_safety_mode: bpy.props.EnumProperty(name='RIG_Scale_Safety_Mode', description='', items=[('Local Clamp', 'Local Clamp', '', 0, 0), ('Global Clamp', 'Global Clamp', '', 0, 1), ('Off', 'Off', '', 0, 2)])
    rig_bake_start_frame: bpy.props.IntProperty(name='RIG_Bake_Start_Frame', description='', default=1, subtype='NONE', soft_min=0)
    rig_bake_end_frame: bpy.props.IntProperty(name='RIG_Bake_End_Frame', description='', default=10, subtype='NONE', soft_min=0)
    rig_update_interval: bpy.props.FloatProperty(name='RIG_Update_Interval', description='', default=0.5, subtype='TIME', unit='TIME', min=0.0, step=3, precision=2)
    rig_interval_stop: bpy.props.BoolProperty(name='RIG_Interval_Stop', description='', default=True)
    rig_bake_frame_step: bpy.props.IntProperty(name='RIG_Bake_Frame_Step', description='', default=1, subtype='NONE', min=1)
    rig_bind_method: bpy.props.EnumProperty(name='RIG_Bind_Method', description='', items=[('Volumetric', 'Volumetric', '', 0, 0), ('Surface', 'Surface', '', 0, 1), ('Hybrid', 'Hybrid', '', 0, 2)])
    rig_target_mode: bpy.props.EnumProperty(name='RIG_Target_Mode', description='', items=[('Active', 'Active', '', 0, 0), ('Input Object', 'Input Object', '', 0, 1), ('All Bound', 'All Bound', '', 0, 2)])
    rig_target_obj: bpy.props.PointerProperty(name='RIG_Target_Obj', description='', type=bpy.types.Object)
    rig_surface_dist_factor: bpy.props.FloatProperty(name='RIG_Surface_Dist_Factor', description='', default=1.5, subtype='NONE', unit='NONE', min=0.10000000149011612, step=3, precision=2)
    rig_update_sh_attributes: bpy.props.BoolProperty(name='RIG_update_sh_attributes', description='', default=True)
    rig_sh_quality_mode: bpy.props.EnumProperty(name='RIG_sh_quality_mode', description='', items=[('Fast', 'Fast', '', 0, 0), ('Balanced', 'Balanced', '', 0, 1), ('Final', 'Final', '', 0, 2)])
    rig_bind_samples: bpy.props.IntProperty(name='RIG_Bind Samples', description='', default=32, subtype='NONE', soft_min=8)
    r2_render_rig_cache_mode: bpy.props.EnumProperty(name='R2_Render_Rig_Cache_Mode', description='', items=[('None', 'None', '', 0, 0), ('Enabled Baked', 'Enabled Baked', '', 0, 1)])
    r2_sh_degree: bpy.props.IntProperty(name='R2_SH_Degree', description='', default=3, subtype='NONE', min=0, max=3)
    r2_sort_threshold: bpy.props.FloatProperty(name='R2_Sort_Threshold', description='', default=0.05000000074505806, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    r2_relight: bpy.props.BoolProperty(name='Relight', description='Use Blender lights in the Gaussian renderer', default=False)
    r2_relight_mode: bpy.props.EnumProperty(name='Relight_Mode', items=[('1', 'Multiply SH', 'Preserve learned appearance and modulate it with new light'), ('2', 'DC Albedo', 'Use DC color as approximate diffuse albedo')], default='1')
    r2_relight_response: bpy.props.EnumProperty(name='Relight_Response', items=[('3', 'Captured', 'Relight by visibility without inferred normals'), ('0', 'Solid', 'One-sided inferred Gaussian normals'), ('1', 'Thin', 'Controlled rear-light transmission'), ('2', 'Two-Sided', 'Two-sided inferred Gaussian normals')], default='3')
    r2_relight_strength: bpy.props.FloatProperty(name='Relight_Strength', default=0.01, min=0.0, max=10.0, precision=3)
    r2_relight_ambient: bpy.props.FloatVectorProperty(name='Relight_Ambient', subtype='COLOR', default=(0.05, 0.05, 0.05), min=0.0, max=1.0)
    r2_relight_ambient_strength: bpy.props.FloatProperty(name='Relight_Ambient_Strength', default=1.0, min=0.0, max=10.0)
    r2_shadows: bpy.props.BoolProperty(name='Shadows', description='Use cached shadow maps when available', default=False)
    r2_shadow_bias: bpy.props.FloatProperty(name='Shadow_Bias', default=0.002, min=0.0, max=0.1, precision=4)
    r2_shadow_normal_bias: bpy.props.FloatProperty(name='Shadow_Normal_Bias', default=0.01, min=0.0, max=0.25, precision=4)
    r2_shadow_filter_radius: bpy.props.FloatProperty(name='Shadow_Filter_Radius', default=1.5, min=0.0, max=4.0, precision=2)
    r2_shadow_density: bpy.props.FloatProperty(name='Shadow_Density', default=1.0, min=0.0, max=4.0)
    r2_shadow_light: bpy.props.PointerProperty(name='Shadow_Light', type=bpy.types.Object)
    r2_shadow_resolution: bpy.props.IntProperty(name='Shadow_Resolution', default=1024, min=256, max=4096)
    r2_shadow_light_limit: bpy.props.IntProperty(name='Shadow_Light_Limit', default=4, min=1, max=4)
    r2_shadow_update_mode: bpy.props.EnumProperty(name='Shadow_Update_Mode', items=[('Auto', 'Auto', 'Rebuild only dirty light maps after frame evaluation', 0, 0), ('Every Frame', 'Every Frame', 'Rebuild all active shadow maps every frame', 0, 1), ('Manual', 'Manual', 'Only rebuild from Refresh Gaussian Shadows', 0, 2)], default='Auto')
    r2_shadow_proxy: bpy.props.BoolProperty(name='Shadow_Proxy', description='Build Eevee shadow cards for Gaussian splats', default=False)
    r2_shadow_proxy_limit: bpy.props.IntProperty(name='Shadow_Proxy_Limit', default=50000, min=1000, max=1000000)
    r2_shadow_proxy_cutoff: bpy.props.FloatProperty(name='Shadow_Proxy_Cutoff', default=0.02, min=0.0, max=1.0, precision=3)
    select_select_by_obj: bpy.props.PointerProperty(name='Select_select_by_obj', description='', type=bpy.types.Object)
    select_obj_select_mode: bpy.props.EnumProperty(name='Select_obj_select_mode', description='', items=[('INSIDE', 'INSIDE', '', 0, 0), ('OUTSIDE', 'OUTSIDE', '', 0, 1)])
    select_attribute_type: bpy.props.EnumProperty(name='Select_attribute_type', description='', items=[('SCALE', 'SCALE', '', 0, 0), ('STRETCH', 'STRETCH', '', 0, 1), ('ROT', 'ROT', '', 0, 2)])
    select_attribute_scale_factor: bpy.props.FloatProperty(name='Select_attribute_scale_factor', description='', default=0.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    select_attribute_scale_select_type: bpy.props.EnumProperty(name='Select_attribute_scale_select_type', description='', items=[('GREATER', 'GREATER', '', 0, 0), ('LESS', 'LESS', '', 0, 1), ('Equal to', 'Equal to', '', 0, 2)])
    select_color_attribute: bpy.props.FloatVectorProperty(name='Select_color_attribute', description='', size=3, default=(10000.0, 10000.0, 10000.0), subtype='COLOR_GAMMA', unit='NONE', step=3, precision=6)
    select_attribute_color_select_type: bpy.props.EnumProperty(name='Select_attribute_color_select_type', description='', items=[('Equal to', 'Equal to', '', 0, 0), ('Brighter than', 'Brighter than', '', 0, 1), ('Darker than', 'Darker than', '', 0, 2)])
    relight_lighting_factor_mode: bpy.props.EnumProperty(name='RELIGHT_lighting_factor_mode', description='', items=[('Tinted Luminance', 'Tinted Luminance', '', 0, 0), ('Luminance', 'Luminance', '', 0, 1), ('RGB', 'RGB', '', 0, 2)])
    relight_factor_curve_mode: bpy.props.EnumProperty(name='RELIGHT_factor_curve_mode', description='', items=[('Reinhard', 'Reinhard', '', 0, 0), ('Linear', 'Linear', '', 0, 1)])
    relight_colorize_mix: bpy.props.FloatProperty(name='RELIGHT_colorize_mix', description='', default=1.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    relight_max_color_tint: bpy.props.FloatProperty(name='RELIGHT_max_color_tint', description='', default=2.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2)
    relight_include_world_environment: bpy.props.BoolProperty(name='RELIGHT_include_world_environment', description='', default=True)
    relight_include_scene_lights: bpy.props.BoolProperty(name='RELIGHT_include_scene_lights', description='', default=True)
    relight_scene_light_gain: bpy.props.FloatProperty(name='RELIGHT_scene_light_gain', description='', default=1.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    relight_use_light_shadows: bpy.props.BoolProperty(name='RELIGHT_use_light_shadows', description='', default=True)
    include_hidden_lights: bpy.props.BoolProperty(name='include_hidden_lights', description='', default=False)
    use_proxy_occlusion: bpy.props.BoolProperty(name='use_proxy_occlusion', description='', default=True)
    occlusion_sample_count: bpy.props.IntProperty(name='occlusion_sample_count', description='', default=6, subtype='NONE', min=1)
    occlusion_bias: bpy.props.FloatProperty(name='occlusion_bias', description='', default=0.0020000000949949026, subtype='NONE', unit='NONE', min=0.0, step=3, precision=3)
    occlusion_max_distance: bpy.props.FloatProperty(name='occlusion_max_distance', description='', default=0.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2)
    light_shadow_bias: bpy.props.FloatProperty(name='light_shadow_bias', description='', default=0.0020000000949949026, subtype='NONE', unit='NONE', min=0.0, step=3, precision=3)
    ambient_floor: bpy.props.FloatProperty(name='ambient_floor', description='Minimum ambient light factor before multiplying the base color', default=0.07999999821186066, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2)
    light_gain: bpy.props.FloatProperty(name='light_gain', description='Overall light factor multiplier', default=0.8500000238418579, subtype='NONE', unit='NONE', min=0.0, soft_max=1.0, step=3, precision=2)
    light_power: bpy.props.FloatProperty(name='light_power', description='Contrast/power applied to the normalized light factor', default=0.75, subtype='NONE', unit='NONE', min=0.0, soft_max=1.0, step=3, precision=2)
    max_light_factor: bpy.props.FloatProperty(name='max_light_factor', description='Clamp for the final light factor to avoid blow-outs', default=1.75, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2)
    irradiance_resolution: bpy.props.IntProperty(name='irradiance_resolution', description='', default=32, subtype='NONE', min=1)
    irradiance_blur_strength: bpy.props.IntProperty(name='irradiance_blur_strength', description='', default=8, subtype='NONE', min=0)
    irradiance_luminance_clamp: bpy.props.FloatProperty(name='irradiance_luminance_clamp', description='', default=10.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2)
    normal_smoothing: bpy.props.FloatProperty(name='normal_smoothing', description='Input: 0 = use proxy normals as-is, 1 = heavily smooth proxy normals before lighting', default=0.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    pre_light_smoothing: bpy.props.FloatProperty(name='pre_light_smoothing', description='Input: 0 = use raw proxy-vertex lighting, 1 = strongly smooth proxy lighting before transfer', default=0.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    post_light_smoothing: bpy.props.FloatProperty(name='post_light_smoothing', description='Input: 0 = keep transferred lighting detail, 1 = strongly smooth the transferred light cache', default=0.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    transfer_style: bpy.props.EnumProperty(name='transfer_style', description='', items=[('Accurate', 'Accurate', '', 0, 0), ('Balanced', 'Balanced', '', 0, 1), ('Smooth', 'Smooth', '', 0, 2)])
    transfer_smoothness: bpy.props.FloatProperty(name='transfer_smoothness', description='Extra smoothing amount used by Balanced and Smooth transfer styles', default=0.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    indirect_strength: bpy.props.FloatProperty(name='indirect_strength', description='Overall strength of the baked indirect / HDRI fill', default=1.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    direct_strength: bpy.props.FloatProperty(name='direct_strength', description='Overall strength of the baked direct light contribution', default=1.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    occlusion_strength: bpy.props.FloatProperty(name='occlusion_strength', description='', default=0.699999988079071, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    shadow_strength: bpy.props.FloatProperty(name='shadow_strength', description='Input: 0 = ignore baked direct-light shadowing, 1 = use baked shadowing fully', default=1.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    export_mode: bpy.props.EnumProperty(name='export_mode', description='Compatible: writes final color to f_dc and zeros f_rest', items=[('Dampen Original SH', 'Dampen Original SH', '', 0, 0), ('Preserve Original SH', 'Preserve Original SH', '', 0, 1), ('Flatten SH', 'Flatten SH', '', 0, 2)])
    directionality_strength: bpy.props.FloatProperty(name='directionality_strength', description='Only used by Dampen Saved Original Directionality; 0 = flat, 1 = full saved original directional strength', default=0.25, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    light_bake_active_menu: bpy.props.EnumProperty(name='Light Bake Active Menu', description='', items=[('1. Store Light', '1. Store Light', '', 0, 0), ('2. Bake Light', '2. Bake Light', '', 0, 1), ('3. Apply Light', '3. Apply Light', '', 0, 2)])
    max_color_tint_mode: bpy.props.EnumProperty(name='max_color_tint_mode', description='', items=[('Perceived Brightness', 'Perceived Brightness', '', 0, 0), ('Preserve Luminance', 'Preserve Luminance', '', 0, 1)])
    hdri_max_width: bpy.props.IntProperty(name='hdri_max_width', description='Max HDRI width used for bake processing; 0 = full source resolution.', default=1024, subtype='NONE', min=0)
    relight_baked_update_mode: bpy.props.EnumProperty(name='RELIGHT_BAKED_UPDATE_MODE', description='', items=[('None', 'None', '', 0, 0), ('Enabled Baked', 'Enabled Baked', '', 0, 1)])


class SNA_GROUP_sna_dgs_object_properties_group(bpy.types.PropertyGroup):
    update_mode: bpy.props.EnumProperty(name='Update_Mode', description='', items=[('Disable Camera Updates', 'Disable Camera Updates', '', 0, 0), ('Enable Camera Updates', 'Enable Camera Updates', '', 0, 1), ('Show As Point Cloud', 'Show As Point Cloud', '', 0, 2)], update=sna_update_update_mode_868D4)
    cam_update: bpy.props.BoolProperty(name='Cam_Update', description='', default=False, update=sna_update_cam_update_DE26E)
    rig_proxy_mesh: bpy.props.PointerProperty(name='RIG_Proxy_Mesh', description='', type=bpy.types.Object)


class SNA_GROUP_sna_dgs_material_properties_group(bpy.types.PropertyGroup):
    lq_hq: bpy.props.EnumProperty(name='LQ_HQ', description='', items=[('LQ Mode (Dithered Alpha)', 'LQ Mode (Dithered Alpha)', '', 0, 0), ('HQ Mode (Blended Alpha)', 'HQ Mode (Blended Alpha)', '', 0, 1)], update=sna_update_lq_hq_065F9)


_bpy_register_class = bpy.utils.register_class
_bpy_unregister_class = bpy.utils.unregister_class


def _safe_register_class(cls):
    """Register a class; if it's already registered (stale state from a
    previously-failed unregister cycle), unregister it first and try again."""
    try:
        _bpy_register_class(cls)
    except ValueError:
        try:
            _bpy_unregister_class(cls)
        except Exception:
            pass
        _bpy_register_class(cls)


def _safe_unregister_class(cls):
    """Unregister a class; silently tolerate already-unregistered state so a
    single failure can't cascade and leave the rest of unregister un-run."""
    try:
        _bpy_unregister_class(cls)
    except Exception:
        pass


def _safe_append_handler(handler_list, fn):
    if fn not in handler_list:
        handler_list.append(fn)


def _safe_remove_handler(handler_list, fn):
    try:
        handler_list.remove(fn)
    except ValueError:
        pass


def _safe_delattr(obj, name):
    try:
        delattr(obj, name)
    except AttributeError:
        pass


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    _safe_register_class(SNA_GROUP_sna_dgs_scene_properties_group)
    _safe_register_class(SNA_GROUP_sna_dgs_object_properties_group)
    _safe_register_class(SNA_GROUP_sna_dgs_material_properties_group)
    bpy.types.Scene.sna_dgs_scene_properties = bpy.props.PointerProperty(name='3DGS Scene Properties', description='', type=SNA_GROUP_sna_dgs_scene_properties_group)
    bpy.types.Object.sna_dgs_object_properties = bpy.props.PointerProperty(name='3DGS Object Properties', description='', type=SNA_GROUP_sna_dgs_object_properties_group)
    bpy.types.Material.sna_dgs_material_properties = bpy.props.PointerProperty(name='3DGS Material Properties', description='', type=SNA_GROUP_sna_dgs_material_properties_group)
    _safe_register_class(SNA_OT_Dgs_Render_Launch_Site_Bf973)
    _safe_register_class(SNA_OT_Dgs_Render_Align_Active_To_X_Axis_6Ae0E)
    _safe_register_class(SNA_OT_Dgs_Render_Align_Active_To_Y_Axis_C305D)
    _safe_register_class(SNA_OT_Dgs_Render_Align_Active_To_Z_Axis_1E184)
    _safe_register_class(SNA_OT_Dgs_Render_Align_Active_To_View_30B13)
    _safe_register_class(SNA_OT_Dgs_Render_Apply_Animate_Modifier_3938E)
    _safe_register_class(SNA_OT_Dgs_Render_Add_Animate_Modifier_39C55)
    bpy.types.VIEW3D_MT_object_apply.prepend(sna_add_to_view3d_mt_object_apply_4C860)
    _safe_register_class(SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665)
    _safe_register_class(SNA_OT_Dgs_Render_Convert_Face_3Dgs_To_Vert_3Dgs_Fc49C)
    _safe_register_class(SNA_OT_Dgs_Render_Convert_Vert_3Dgs_To_Face_3Dgs_E6635)
    _safe_register_class(SNA_OT_Dgs_Render_Import_Image_Overlay_4A457)
    _safe_register_class(SNA_OT_Dgs_Render_Start_Vertex_Painting_A36E0)
    _safe_register_class(SNA_OT_Dgs_Render_Refresh__Create_Paint_Attribute_84655)
    _safe_register_class(SNA_OT_Dgs_Render_Export_Mesh_As_3Dgs4Dgs_Ce2F7)
    _safe_register_class(SNA_OT_Dgs_Render_Generate_Hq_Object_55455)
    _safe_register_class(SNA_OT_Dgs_Render_Disable_Hq_Overlap_34678)
    _safe_register_class(SNA_OT_Dgs_Render_Update_Enabled_3Dgs_Objects_6D7F4)
    _safe_register_class(SNA_OT_Dgs_Render_Mesh23Dgs_3Dfed)
    _safe_register_class(SNA_OT_Dgs_Render_Clean_Up_Scene_80052)
    _safe_register_class(SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_Eafbb)
    _safe_register_class(SNA_OT_Dgs_Render_Build_Shadow_Proxies_5B787)
    _safe_register_class(SNA_OT_Dgs_Render_Refresh_Shadows_16F2B)
    _safe_register_class(SNA_OT_Dgs_Render_Advanced_Render_147Af)
    _safe_register_class(SNA_OT_Dgs_Render_Refresh_Scene_A6719)
    _safe_register_class(SNA_OT_Dgs_Render_Stop_Interval_Updates_83370)
    _safe_register_class(SNA_OT_Dgs_Render_Auto_Generate_Crop_Object_F20D5)
    _safe_register_class(SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De)
    _safe_register_class(SNA_OT_Dgs_Render_Import_Ply_E0A3A)
    _safe_register_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_E1A83)
    _safe_register_class(SNA_OT_Dgs_Render_Apply_Modifier_0F5F2)
    _safe_register_class(SNA_OT_Dgs_Render_Remove_Modifier_9Cf0D)
    _safe_register_class(SNA_OT_Dgs_Render_Select_Object_B1F49)
    _safe_register_class(SNA_OT_Dgs_Render_Open_Output_Folder_82000)
    _safe_register_class(SNA_OT_Dgs_Render_Attribute_Select_51C86)
    _safe_register_class(SNA_OT_Dgs_Render_Select_By_Object_92F9C)
    _safe_register_class(SNA_OT_Dgs_Render_Build_Light_Data_Ab375)
    _safe_register_class(SNA_OT_Dgs_Render_Restore_Original_Light_9A7Fe)
    _safe_register_class(SNA_OT_Dgs_Render_Store_Original_Lighting_99939)
    _safe_register_class(SNA_OT_Dgs_Render_Apply_Light_Data_6C5Ad)
    _safe_register_class(SNA_OT_Dgs_Render_Add_Uv_Edit_Modifier_E8Ae6)
    _safe_append_handler(bpy.app.handlers.render_pre, render_pre_handler_77179)
    _safe_register_class(SNA_AddonPreferences_AB8B3)
    _safe_register_class(SNA_OT_Dgs_Render_Bind_To_Proxy_Mesh_6C58F)
    _safe_register_class(SNA_OT_Dgs_Render_Select_Proxy_Mesh_E76B7)
    _safe_register_class(SNA_OT_Dgs_Render_Update_Bound_3Dgs_From_Proxy_Mesh_951A0)
    _safe_register_class(SNA_OT_Dgs_Render_Bake_Frames_To_Cache_90885)
    _safe_register_class(SNA_OT_Dgs_Render_Unbind_From_Proxy_Mesh_7648D)
    _safe_register_class(SNA_OT_Dgs_Render_Update_Bound_3Dgs_From_Cache_385Ec)
    _safe_register_class(SNA_OT_Dgs_Render_End_Proxy_Rig_Updates_60C6A)
    _safe_register_class(SNA_OT_Dgs_Render_Clear_Rig_Cache_F38Be)
    _safe_register_class(SNA_OT_Dgs_Render_Apply_Armature_Pose_As_Rest_Pose_A8C68)
    _safe_register_class(SNA_OT_Dgs_Render_Append_Wire_Sphere_2Bf63)
    _safe_register_class(SNA_OT_Dgs_Render_Append_Wire_Cube_56E0F)
    _safe_register_class(SNA_OT_Dgs_Render_Append_Geometry_Node_Modifier_C2492)
    _safe_register_class(SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_Cb703)
    _safe_register_class(SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_86F09)
    _safe_register_class(SNA_OT_Dgs_Render_Auto_Set_Up_Camera_Cull_Properties_Aef48)
    _safe_register_class(SNA_OT_Dgs_Render_Append_Rough_Mesh_Modifier_65Da3)
    _safe_register_class(SNA_OT_Dgs_Render_Build_Shadow_Proxies_5B787)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    _safe_delattr(bpy.types.Material, "sna_dgs_material_properties")
    _safe_delattr(bpy.types.Object, "sna_dgs_object_properties")
    _safe_delattr(bpy.types.Scene, "sna_dgs_scene_properties")
    _safe_unregister_class(SNA_GROUP_sna_dgs_material_properties_group)
    _safe_unregister_class(SNA_GROUP_sna_dgs_object_properties_group)
    _safe_unregister_class(SNA_GROUP_sna_dgs_scene_properties_group)
    _safe_unregister_class(SNA_OT_Dgs_Render_Launch_Site_Bf973)
    _safe_unregister_class(SNA_OT_Dgs_Render_Align_Active_To_X_Axis_6Ae0E)
    _safe_unregister_class(SNA_OT_Dgs_Render_Align_Active_To_Y_Axis_C305D)
    _safe_unregister_class(SNA_OT_Dgs_Render_Align_Active_To_Z_Axis_1E184)
    _safe_unregister_class(SNA_OT_Dgs_Render_Align_Active_To_View_30B13)
    _safe_unregister_class(SNA_OT_Dgs_Render_Apply_Animate_Modifier_3938E)
    _safe_unregister_class(SNA_OT_Dgs_Render_Add_Animate_Modifier_39C55)
    bpy.types.VIEW3D_MT_object_apply.remove(sna_add_to_view3d_mt_object_apply_4C860)
    _safe_unregister_class(SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665)
    _safe_unregister_class(SNA_OT_Dgs_Render_Convert_Face_3Dgs_To_Vert_3Dgs_Fc49C)
    _safe_unregister_class(SNA_OT_Dgs_Render_Convert_Vert_3Dgs_To_Face_3Dgs_E6635)
    _safe_unregister_class(SNA_OT_Dgs_Render_Import_Image_Overlay_4A457)
    _safe_unregister_class(SNA_OT_Dgs_Render_Start_Vertex_Painting_A36E0)
    _safe_unregister_class(SNA_OT_Dgs_Render_Refresh__Create_Paint_Attribute_84655)
    _safe_unregister_class(SNA_OT_Dgs_Render_Export_Mesh_As_3Dgs4Dgs_Ce2F7)
    _safe_unregister_class(SNA_OT_Dgs_Render_Generate_Hq_Object_55455)
    _safe_unregister_class(SNA_OT_Dgs_Render_Disable_Hq_Overlap_34678)
    _safe_unregister_class(SNA_OT_Dgs_Render_Update_Enabled_3Dgs_Objects_6D7F4)
    _safe_unregister_class(SNA_OT_Dgs_Render_Mesh23Dgs_3Dfed)
    _safe_unregister_class(SNA_OT_Dgs_Render_Clean_Up_Scene_80052)
    _safe_unregister_class(SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_Eafbb)
    _safe_unregister_class(SNA_OT_Dgs_Render_Build_Shadow_Proxies_5B787)
    _safe_unregister_class(SNA_OT_Dgs_Render_Refresh_Shadows_16F2B)
    _safe_unregister_class(SNA_OT_Dgs_Render_Advanced_Render_147Af)
    _safe_unregister_class(SNA_OT_Dgs_Render_Refresh_Scene_A6719)
    _safe_unregister_class(SNA_OT_Dgs_Render_Stop_Interval_Updates_83370)
    _safe_unregister_class(SNA_OT_Dgs_Render_Auto_Generate_Crop_Object_F20D5)
    _safe_unregister_class(SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De)
    _safe_unregister_class(SNA_OT_Dgs_Render_Import_Ply_E0A3A)
    _safe_unregister_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_E1A83)
    _safe_unregister_class(SNA_OT_Dgs_Render_Apply_Modifier_0F5F2)
    _safe_unregister_class(SNA_OT_Dgs_Render_Remove_Modifier_9Cf0D)
    _safe_unregister_class(SNA_OT_Dgs_Render_Select_Object_B1F49)
    _safe_unregister_class(SNA_OT_Dgs_Render_Open_Output_Folder_82000)
    _safe_unregister_class(SNA_OT_Dgs_Render_Attribute_Select_51C86)
    _safe_unregister_class(SNA_OT_Dgs_Render_Select_By_Object_92F9C)
    _safe_unregister_class(SNA_OT_Dgs_Render_Build_Light_Data_Ab375)
    _safe_unregister_class(SNA_OT_Dgs_Render_Restore_Original_Light_9A7Fe)
    _safe_unregister_class(SNA_OT_Dgs_Render_Store_Original_Lighting_99939)
    _safe_unregister_class(SNA_OT_Dgs_Render_Apply_Light_Data_6C5Ad)
    _safe_unregister_class(SNA_OT_Dgs_Render_Add_Uv_Edit_Modifier_E8Ae6)
    _safe_remove_handler(bpy.app.handlers.render_pre, render_pre_handler_77179)
    _safe_unregister_class(SNA_AddonPreferences_AB8B3)
    _safe_unregister_class(SNA_OT_Dgs_Render_Bind_To_Proxy_Mesh_6C58F)
    _safe_unregister_class(SNA_OT_Dgs_Render_Select_Proxy_Mesh_E76B7)
    _safe_unregister_class(SNA_OT_Dgs_Render_Update_Bound_3Dgs_From_Proxy_Mesh_951A0)
    _safe_unregister_class(SNA_OT_Dgs_Render_Bake_Frames_To_Cache_90885)
    _safe_unregister_class(SNA_OT_Dgs_Render_Unbind_From_Proxy_Mesh_7648D)
    _safe_unregister_class(SNA_OT_Dgs_Render_Update_Bound_3Dgs_From_Cache_385Ec)
    _safe_unregister_class(SNA_OT_Dgs_Render_End_Proxy_Rig_Updates_60C6A)
    _safe_unregister_class(SNA_OT_Dgs_Render_Clear_Rig_Cache_F38Be)
    _safe_unregister_class(SNA_OT_Dgs_Render_Apply_Armature_Pose_As_Rest_Pose_A8C68)
    _safe_unregister_class(SNA_OT_Dgs_Render_Append_Wire_Sphere_2Bf63)
    _safe_unregister_class(SNA_OT_Dgs_Render_Append_Wire_Cube_56E0F)
    _safe_unregister_class(SNA_OT_Dgs_Render_Append_Geometry_Node_Modifier_C2492)
    _safe_unregister_class(SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_Cb703)
    _safe_unregister_class(SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_86F09)
    _safe_unregister_class(SNA_OT_Dgs_Render_Auto_Set_Up_Camera_Cull_Properties_Aef48)
    _safe_unregister_class(SNA_OT_Dgs_Render_Append_Rough_Mesh_Modifier_65Da3)
    _safe_unregister_class(SNA_OT_Dgs_Render_Build_Shadow_Proxies_5B787)
