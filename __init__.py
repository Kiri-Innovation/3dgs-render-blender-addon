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
    "version" : (4, 1, 5),
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


addon_keymaps = {}

_icons = None


from .src import *

dgs_render__active_3dgs_object = {'sna_apply_modifier_list': [], 'sna_in_camera_view': False, }
dgs_render__collection_snippets = {'sna_collections_temp_list': [], }
dgs_render__hq_mode = {'sna_lq_object_list': [], }
dgs_render_modeon_property_update = {'sna_dgs_proxies_in_scene': False, }
dgs_renderdb_filter = {'sna_db_filter_input_object': None, 'sna_db_filter_force_scale_factor': 0.0, }


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




def sna_update_active_mode_4A881(self, context):
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
        bpy.context.scene.sna_dgs_scene_properties.r2_main_mode = 'Update'
        for i_14280 in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_14280].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_14280].modifiers):
                bpy.context.scene.objects[i_14280].modifiers['KIRI_3DGS_Render_GN'].show_viewport = False
                bpy.context.scene.objects[i_14280].modifiers['KIRI_3DGS_Render_GN'].show_render = False
                if (property_exists("bpy.context.scene.objects[i_14280].modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.scene.objects[i_14280].modifiers):
                    bpy.context.scene.objects[i_14280].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = True
                    bpy.context.scene.objects[i_14280].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = True
                bpy.context.scene.objects[i_14280]['3dgs_is_hidden'] = bpy.context.scene.objects[i_14280].hide_viewport
                if bpy.context.scene.sna_dgs_scene_properties.r2_hide_on_change:
                    target_object = bpy.context.scene.objects[i_14280]
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
        dgs_render_modeon_property_update['sna_dgs_proxies_in_scene'] = False
        for i_517A6 in range(len(bpy.context.scene.objects)):
            if 'gaussian_source_uuid' in bpy.context.scene.objects[i_517A6]:
                dgs_render_modeon_property_update['sna_dgs_proxies_in_scene'] = True
        for i_1DC66 in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_1DC66].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_1DC66].modifiers):
                bpy.context.scene.objects[i_1DC66].hide_viewport = False
        if dgs_render_modeon_property_update['sna_dgs_proxies_in_scene']:
            sna_c2_refresh_all_4D367(True, bpy.context.scene.sna_dgs_scene_properties.r2_transforms, True)
            sna_shader_system_A4AED()
            sna_texture_creation_FD1B2()
            sna_viewport_render_A3941()
        bpy.context.view_layer.objects.active = None
        for i_611D3 in range(len(bpy.context.scene.objects)):
            if ((property_exists("bpy.context.scene.objects[i_611D3].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_611D3].modifiers) and '3DGS_Mesh_Type' in bpy.context.scene.objects[i_611D3]):
                if (bpy.context.scene.objects[i_611D3]['3DGS_Mesh_Type'] == 'face'):
                    bpy.context.scene.objects[i_611D3].hide_viewport = True
    elif sna_updated_prop == "Mesh 2 3DGS":
        sna_clean_up_scene_5F1F1(False)
        bpy.context.view_layer.objects.active = None
    else:
        pass



class SNA_GROUP_sna_dgs_scene_properties_group(bpy.types.PropertyGroup):
    active_mode: bpy.props.EnumProperty(name='Active_Mode', description='', items=[('Edit', 'Edit', '', 0, 0), ('Render', 'Render', '', 0, 1), ('Mesh 2 3DGS', 'Mesh 2 3DGS', '', 0, 2)], update=sna_update_active_mode_4A881)
    edit_mode_menu: bpy.props.EnumProperty(name='Edit_Mode_Menu', description='', items=[('Import', 'Import', '', 0, 0), ('Modifiers', 'Modifiers', '', 0, 1), ('Colour', 'Colour', '', 0, 2), ('Animate', 'Animate', '', 0, 3), ('HQ / LQ', 'HQ / LQ', '', 0, 4), ('Export', 'Export', '', 0, 5)])
    shading_menu: bpy.props.EnumProperty(name='Shading_Menu', description='', items=[('Selective 1', 'Selective 1', '', 0, 0), ('Selective 2', 'Selective 2', '', 0, 1), ('Selective 3', 'Selective 3', '', 0, 2), ('Vertex Paint', 'Vertex Paint', '', 0, 3), ('Image Overlay', 'Image Overlay', '', 0, 4)])
    hq_overlap: bpy.props.BoolProperty(name='HQ_Overlap', description='', default=False, update=sna_update_hq_overlap_DDF15)
    import_face_vert: bpy.props.EnumProperty(name='Import_Face_Vert', description='', items=[('Verts', 'Verts', '', 0, 0), ('Faces', 'Faces', '', 0, 1)])
    import_uv: bpy.props.BoolProperty(name='Import_UV', description='', default=False)
    import_proxy: bpy.props.BoolProperty(name='Import_Proxy', description='', default=False)
    mesh2gs_validate: bpy.props.BoolProperty(name='MESH2GS_Validate', description='', default=False)
    show_tips: bpy.props.BoolProperty(name='Show_Tips', description='', default=False)
    r2_selected: bpy.props.BoolProperty(name='R2_Selected', description='', default=False)
    r2_transforms: bpy.props.BoolProperty(name='R2_Transforms', description='', default=True)
    r2_animation: bpy.props.BoolProperty(name='R2_Animation', description='', default=False)
    r2_color: bpy.props.BoolProperty(name='R2_Color', description='', default=True)
    r2_depth: bpy.props.BoolProperty(name='R2_Depth', description='', default=False)
    r2_comp: bpy.props.BoolProperty(name='R2_Comp', description='', default=False)
    r2_main_mode: bpy.props.EnumProperty(name='R2_Main_Mode', description='', items=[('Update', 'Update', '', 0, 0), ('Render', 'Render', '', 0, 1), ('Create', 'Create', '', 0, 2), ('Clean Up', 'Clean Up', '', 0, 3)])
    r2_clear_empties: bpy.props.BoolProperty(name='R2_Clear_Empties', description='', default=False)
    r2_update_type: bpy.props.EnumProperty(name='R2_Update_Type', description='', items=[('Single Time', 'Single Time', '', 0, 0), ('Interval Update', 'Interval Update', '', 0, 1)])
    r2_interval_stop: bpy.props.BoolProperty(name='R2_Interval_Stop', description='', default=False)
    r2_interval: bpy.props.FloatProperty(name='R2_Interval', description='', default=0.10000000149011612, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)
    r2_hide_on_change: bpy.props.BoolProperty(name='R2_Hide_On_Change', description='', default=True)
    r2_temp_path: bpy.props.StringProperty(name='R2_Temp_Path', description='', default='', subtype='NONE', maxlen=0)


class SNA_GROUP_sna_dgs_object_properties_group(bpy.types.PropertyGroup):
    update_mode: bpy.props.EnumProperty(name='Update_Mode', description='', items=[('Disable Camera Updates', 'Disable Camera Updates', '', 0, 0), ('Enable Camera Updates', 'Enable Camera Updates', '', 0, 1), ('Show As Point Cloud', 'Show As Point Cloud', '', 0, 2)], update=sna_update_update_mode_868D4)
    cam_update: bpy.props.BoolProperty(name='Cam_Update', description='', default=False, update=sna_update_cam_update_DE26E)


class SNA_GROUP_sna_dgs_material_properties_group(bpy.types.PropertyGroup):
    lq_hq: bpy.props.EnumProperty(name='LQ_HQ', description='', items=[('LQ Mode (Dithered Alpha)', 'LQ Mode (Dithered Alpha)', '', 0, 0), ('HQ Mode (Blended Alpha)', 'HQ Mode (Blended Alpha)', '', 0, 1)], update=sna_update_lq_hq_065F9)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_GROUP_sna_dgs_scene_properties_group)
    bpy.utils.register_class(SNA_GROUP_sna_dgs_object_properties_group)
    bpy.utils.register_class(SNA_GROUP_sna_dgs_material_properties_group)
    bpy.types.Scene.sna_dgs_scene_properties = bpy.props.PointerProperty(name='3DGS Scene Properties', description='', type=SNA_GROUP_sna_dgs_scene_properties_group)
    bpy.types.Object.sna_dgs_object_properties = bpy.props.PointerProperty(name='3DGS Object Properties', description='', type=SNA_GROUP_sna_dgs_object_properties_group)
    bpy.types.Material.sna_dgs_material_properties = bpy.props.PointerProperty(name='3DGS Material Properties', description='', type=SNA_GROUP_sna_dgs_material_properties_group)
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
    bpy.types.VIEW3D_MT_object_apply.prepend(sna_add_to_view3d_mt_object_apply_F9005)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Import_Image_Overlay_4A457)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Start_Vertex_Painting_A36E0)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Refresh__Create_Paint_Attribute_84655)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Export_Mesh_Object_As_3Dgs_Ply_Ce2F7)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Generate_Hq_Object_55455)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Disable_Hq_Overlap_34678)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Update_Enabled_3Dgs_Objects_6D7F4)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Mesh23Dgs_3Dfed)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Refresh_Scene_C0B35)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_D5B41)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Advanced_Render_Ba196)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Clean_Up_Advanced_Render_Scene_09450)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Stop_Interval_Updates_5Ac80)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Auto_Generate_Crop_Object_F20D5)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Import_Ply_E0A3A)
    bpy.utils.register_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_A02CB)
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
    del bpy.types.Material.sna_dgs_material_properties
    del bpy.types.Object.sna_dgs_object_properties
    del bpy.types.Scene.sna_dgs_scene_properties
    bpy.utils.unregister_class(SNA_GROUP_sna_dgs_material_properties_group)
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
    bpy.types.VIEW3D_MT_object_apply.remove(sna_add_to_view3d_mt_object_apply_F9005)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Import_Image_Overlay_4A457)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Start_Vertex_Painting_A36E0)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Refresh__Create_Paint_Attribute_84655)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Export_Mesh_Object_As_3Dgs_Ply_Ce2F7)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Generate_Hq_Object_55455)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Disable_Hq_Overlap_34678)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Update_Enabled_3Dgs_Objects_6D7F4)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Mesh23Dgs_3Dfed)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Refresh_Scene_C0B35)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_D5B41)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Advanced_Render_Ba196)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Clean_Up_Advanced_Render_Scene_09450)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Stop_Interval_Updates_5Ac80)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Auto_Generate_Crop_Object_F20D5)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Rotate_For_Blender_Axes_423De)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Import_Ply_E0A3A)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_A02CB)
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
