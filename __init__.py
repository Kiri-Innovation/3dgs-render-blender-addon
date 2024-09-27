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
    "name" : "GS Render by KIRI Engine",
    "author" : "", 
    "description" : "Converts 3DGS Scans into Blender renderable objects",
    "blender" : (4, 2, 0),
    "version" : (1, 0, 0),
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
from bpy_extras.io_utils import ImportHelper, ExportHelper
from mathutils import Matrix
import math
from typing import Tuple


addon_keymaps = {}
_icons = None

import sys

# Add plyfile to the path
addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

try:
    import plyfile
except ImportError as e:
    print(f"Error importing plyfile: {e}")


kiri__blender_splat_render__import__update__render = {'sna_dgs_lq_active': None, }


def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


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


def sna_documentation_interface_function_A1B59(layout_function, ):
    op = layout_function.operator('sna.open_blender_splat_render_documentation_1eac5', text='Documentation', icon_value=0, emboss=True, depress=False)
    op = layout_function.operator('sna.open_blender_splat_render_tutorial_video_a4fe6', text='Tutorial Video', icon_value=0, emboss=True, depress=False)


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
        url = 'https://youtu.be/j9BDi4dMC-A'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


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


def sna_about_and_external_links_interface_function_8E1B8(layout_function, ):
    layout_function.label(text='--- About KIRI Engine ---', icon_value=0)
    layout_function.separator(factor=1.0)
    box_98A33 = layout_function.box()
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
    op = layout_function.operator('sna.launch_blender_market_77f72', text='See All Add-ons on Blender Market', icon_value=0, emboss=True, depress=False)
    op = layout_function.operator('sna.launch_kiri_site_d26bf', text='Learn More About KIRI Engine', icon_value=0, emboss=True, depress=False)


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
        url = 'https://blendermarket.com/creator/products/3dgs-render-by-kiri-engine'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

import bpy
import numpy as np
import os
import math
from bpy_extras.io_utils import ImportHelper

# Move plyfile import to global scope
try:
    from plyfile import PlyData
    PLYFILE_AVAILABLE = True
except ImportError:
    PLYFILE_AVAILABLE = False
    print("plyfile is not installed. Please install it to use this feature.")

class SNA_OT_Dgs__Import_Ply_As_Splats_8458E(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.dgs__import_ply_as_splats_8458e"
    bl_label = "3DGS - Import PLY as Splats"
    bl_description = "Imports a .ply 3DGS scan"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.ply', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        global os
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
        class PlyInfo:

            def __init__(self, filepath: str):
                self.loadPly(filepath)

            def loadPly(self, filepath: str):
                plydata = PlyData.read(filepath)
                self.center = np.stack((np.asarray(plydata.elements[0]["x"]),
                                        np.asarray(plydata.elements[0]["y"]),
                                        np.asarray(plydata.elements[0]["z"])), axis=1)
                self.splat_count = int(len(self.center))
                N = self.splat_count
                if 'opacity' in plydata.elements[0]:
                    log_opacities = np.asarray(plydata.elements[0]["opacity"])[..., np.newaxis]
                    self.opacities = 1 / (1 + np.exp(-log_opacities))
                else:
                    log_opacities = np.asarray(1)[..., np.newaxis]
                    self.opacities = 1 / (1 + np.exp(-log_opacities))
                self.opacities = self.opacities.flatten()
                self.features_dc = np.zeros((N, 3, 1))
                self.features_dc[:, 0, 0] = np.asarray(plydata.elements[0]["f_dc_0"])
                self.features_dc[:, 1, 0] = np.asarray(plydata.elements[0]["f_dc_1"])
                self.features_dc[:, 2, 0] = np.asarray(plydata.elements[0]["f_dc_2"])
                # V2 Update - V4 Remove f names
                log_scales = np.stack((np.asarray(plydata.elements[0]["scale_0"]),
                                       np.asarray(plydata.elements[0]["scale_1"]),
                                       np.asarray(plydata.elements[0]["scale_2"])), axis=1)
                self.scales = np.exp(log_scales)
                self.quats = np.stack((np.asarray(plydata.elements[0]["rot_0"]),
                                       np.asarray(plydata.elements[0]["rot_1"]),
                                       np.asarray(plydata.elements[0]["rot_2"]),
                                       np.asarray(plydata.elements[0]["rot_3"])), axis=1)

        def RS_matrix(quat: np.ndarray, scale: np.ndarray) -> list[float]:
            length = 1 / math.sqrt(quat[0] * quat[0] + quat[1] * quat[1] + quat[2] * quat[2] + quat[3] * quat[3])
            x, y, z, w = quat[0] * length, quat[1] * length, quat[2] * length, quat[3] * length
            matrix = [
                scale[0] * (1 - 2 * (z * z + w * w)),
                scale[0] * (2 * (y * z + x * w)),
                scale[0] * (2 * (y * w - x * z)),
                scale[1] * (2 * (y * z - x * w)),
                scale[1] * (1 - 2 * (y * y + w * w)),
                scale[1] * (2 * (z * w + x * y)),
                scale[2] * (2 * (y * w + x * z)),
                scale[2] * (2 * (z * w - x * y)),
                scale[2] * (1 - 2 * (y * y + z * z))
            ]
            return matrix

        def calculate_bounding_box(centers):
            bound_min = np.min(centers, axis=0)
            bound_max = np.max(centers, axis=0)
            return bound_min.tolist(), bound_max.tolist()
        # Main script execution starts here
        if not ply_import_path:
            print("Error: No file path provided.")
        else:
            if not os.path.exists(ply_import_path):
                print(f"Error: File not found at path: {ply_import_path}")
            else:
                plyInfo = PlyInfo(ply_import_path)
                file_base_name = os.path.splitext(os.path.basename(ply_import_path))[0]
                object_name = f"{file_base_name}"
                vertices = []
                indices = []
                for i in range(plyInfo.splat_count):
                    vertices.append((-2.0, -2.0, float(i)))
                    vertices.append((2.0, -2.0, float(i)))
                    vertices.append((2.0, 2.0, float(i)))
                    vertices.append((-2.0, 2.0, float(i)))
                    b = i * 4
                    indices.append((b, b+1, b+2))
                    indices.append((b, b+2, b+3))
                mesh = bpy.data.meshes.new(name=object_name)
                mesh.from_pydata(vertices, [], indices)
                obj = bpy.data.objects.new(object_name, mesh)
                Vrk_1 = [0.0] * plyInfo.splat_count * 2 * 1 
                Vrk_2 = [0.0] * plyInfo.splat_count * 2 * 1
                Vrk_3 = [0.0] * plyInfo.splat_count * 2 * 1
                Vrk_4 = [0.0] * plyInfo.splat_count * 2 * 1
                Vrk_5 = [0.0] * plyInfo.splat_count * 2 * 1
                Vrk_6 = [0.0] * plyInfo.splat_count * 2 * 1
                center = [0.0] * plyInfo.splat_count * 2 * 3 
                color = [0.0] * plyInfo.splat_count * 2 * 4 
                SH_0 = 0.28209479177387814
                for i in range(plyInfo.splat_count):
                    RS = RS_matrix(plyInfo.quats[i], plyInfo.scales[i])
                    Vrk_1[2 * i + 0] = Vrk_1[2 * i + 1] = RS[0] * RS[0] + RS[3] * RS[3] + RS[6] * RS[6]
                    Vrk_2[2 * i + 0] = Vrk_2[2 * i + 1] = RS[0] * RS[1] + RS[3] * RS[4] + RS[6] * RS[7]
                    Vrk_3[2 * i + 0] = Vrk_3[2 * i + 1] = RS[0] * RS[2] + RS[3] * RS[5] + RS[6] * RS[8]
                    Vrk_4[2 * i + 0] = Vrk_4[2 * i + 1] = RS[1] * RS[1] + RS[4] * RS[4] + RS[7] * RS[7]
                    Vrk_5[2 * i + 0] = Vrk_5[2 * i + 1] = RS[1] * RS[2] + RS[4] * RS[5] + RS[7] * RS[8]
                    Vrk_6[2 * i + 0] = Vrk_6[2 * i + 1] = RS[2] * RS[2] + RS[5] * RS[5] + RS[8] * RS[8]
                    center[6 * i + 0] = center[6 * i + 3] = plyInfo.center[i][0]
                    center[6 * i + 1] = center[6 * i + 4] = plyInfo.center[i][1]
                    center[6 * i + 2] = center[6 * i + 5] = plyInfo.center[i][2]
                    R = (plyInfo.features_dc[i][0][0] * SH_0 + 0.5)
                    G = (plyInfo.features_dc[i][1][0] * SH_0 + 0.5)
                    B = (plyInfo.features_dc[i][2][0] * SH_0 + 0.5)
                    A = plyInfo.opacities[i]
                    color[8 * i + 0] = color[8 * i + 4] = R
                    color[8 * i + 1] = color[8 * i + 5] = G
                    color[8 * i + 2] = color[8 * i + 6] = B
                    color[8 * i + 3] = color[8 * i + 7] = A
                center_attr = mesh.attributes.new(name="center", type='FLOAT_VECTOR', domain='FACE')
                center_attr.data.foreach_set("vector", center)
                color_attr = mesh.attributes.new(name="color", type='FLOAT_COLOR', domain='FACE')
                color_attr.data.foreach_set("color", color)
                Vrk_1_attr = mesh.attributes.new(name="Vrk_1", type='FLOAT', domain='FACE')
                Vrk_1_attr.data.foreach_set("value", Vrk_1)
                Vrk_2_attr = mesh.attributes.new(name="Vrk_2", type='FLOAT', domain='FACE')
                Vrk_2_attr.data.foreach_set("value", Vrk_2)
                Vrk_3_attr = mesh.attributes.new(name="Vrk_3", type='FLOAT', domain='FACE')
                Vrk_3_attr.data.foreach_set("value", Vrk_3)
                Vrk_4_attr = mesh.attributes.new(name="Vrk_4", type='FLOAT', domain='FACE')
                Vrk_4_attr.data.foreach_set("value", Vrk_4)
                Vrk_5_attr = mesh.attributes.new(name="Vrk_5", type='FLOAT', domain='FACE')
                Vrk_5_attr.data.foreach_set("value", Vrk_5)
                Vrk_6_attr = mesh.attributes.new(name="Vrk_6", type='FLOAT', domain='FACE')
                Vrk_6_attr.data.foreach_set("value", Vrk_6)
                # Sort indices V 2.1
                sorted_indices = np.arange(plyInfo.splat_count, dtype=np.int32)
                sorted_indices_attr = mesh.attributes.new(name="sorted_indices", type='INT', domain='FACE')
                sorted_indices_attr.data.foreach_set("value", np.repeat(sorted_indices, 2))
                # Add custom properties
                obj['update_rot_to_cam'] = True
                obj['camera_position'] = (0, 0, 0)
                obj['camera_direction'] = (0, 0, -1)
                bound_min, bound_max = calculate_bounding_box(plyInfo.center)
                obj['bound_min'] = bound_min
                obj['bound_max'] = bound_max
                node_group = bpy.data.node_groups['KIRI_3DGS_Render_GN']
                node_modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
                node_modifier.node_group = node_group
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
                bpy.context.collection.objects.link(obj)
                bpy.context.view_layer.objects.active = obj
                obj.location = bpy.context.scene.cursor.location
                obj.select_set(True)
                print(f"Created Gaussian Splat object: {obj.name}")
        input_update_method = 'Continuous'
        from mathutils import Matrix

        def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
            geometryNodes_modifier = obj.modifiers.get('GeometryNodes')
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

        def delayed_B3750():
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
            if bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences.sna_set_colour_space_on_import:
                bpy.context.scene.view_settings.view_transform = 'Standard'
                bpy.context.scene.view_settings.look = 'None'
            bpy.context.view_layer.objects.active.rotation_euler = (math.radians(-90.0), 0.0, math.radians(180.0))
        bpy.app.timers.register(delayed_B3750, first_interval=0.20000000298023224)
        return {"FINISHED"}


class SNA_OT_Dgs__Start_Camera_Update_9Eaff(bpy.types.Operator):
    bl_idname = "sna.dgs__start_camera_update_9eaff"
    bl_label = "3DGS - Start camera update"
    bl_description = "Starts rotatingall enabled scan's faces to the camera view"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences.sna_enable_header_color_warning:
            bpy.context.preferences.themes['Default'].user_interface.wcol_box.inner = bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences.sna_camera_update_warning_colour
        input_update_method = bpy.context.scene.sna_dgs_camera_refresh_method.replace('Frame Change', 'frame_change')
        from mathutils import Matrix

        def update_gaussian_splat_camera(obj, view_matrix, proj_matrix, window_width, window_height):
            geometryNodes_modifier = obj.modifiers.get('GeometryNodes')
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
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs__Stop_Camera_Update_9Ad85(bpy.types.Operator):
    bl_idname = "sna.dgs__stop_camera_update_9ad85"
    bl_label = "3DGS - Stop camera update"
    bl_description = "Stops camera updates"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.preferences.themes['Default'].user_interface.wcol_box.inner = (0.11372499912977219, 0.11372499912977219, 0.11372499912977219, 0.5019609928131104)
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
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs__Set_Render_Engine_To_Eevee_7516E(bpy.types.Operator):
    bl_idname = "sna.dgs__set_render_engine_to_eevee_7516e"
    bl_label = "3DGS - Set render engine to Eevee"
    bl_description = "Sets the render engine to Eevee"
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


def sna_splat_render__main_functions_3FCFA(layout_function, ):
    if (bpy.context.scene.render.engine == 'BLENDER_EEVEE_NEXT'):
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
        op = box_5C3FC.operator('sna.dgs__import_ply_as_splats_8458e', text='Import PLY as Splats', icon_value=706, emboss=True, depress=False)
        if property_exists("bpy.context.scene['gaussian_splat_updates_active']", globals(), locals()):
            box_A69C5 = col_E3544.box()
            box_A69C5.alert = False
            box_A69C5.enabled = True
            box_A69C5.active = True
            box_A69C5.use_property_split = False
            box_A69C5.use_property_decorate = False
            box_A69C5.alignment = 'Expand'.upper()
            box_A69C5.scale_x = 1.0
            box_A69C5.scale_y = 1.0
            if not True: box_A69C5.operator_context = "EXEC_DEFAULT"
            box_01052 = box_A69C5.box()
            box_01052.alert = False
            box_01052.enabled = True
            box_01052.active = True
            box_01052.use_property_split = False
            box_01052.use_property_decorate = False
            box_01052.alignment = 'Expand'.upper()
            box_01052.scale_x = 1.0
            box_01052.scale_y = 1.0
            if not True: box_01052.operator_context = "EXEC_DEFAULT"
            col_280A9 = box_01052.column(heading='', align=False)
            col_280A9.alert = False
            col_280A9.enabled = True
            col_280A9.active = True
            col_280A9.use_property_split = False
            col_280A9.use_property_decorate = False
            col_280A9.scale_x = 1.0
            col_280A9.scale_y = 1.0
            col_280A9.alignment = 'Expand'.upper()
            col_280A9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_02115 = col_280A9.box()
            box_02115.alert = False
            box_02115.enabled = (not bpy.context.scene['gaussian_splat_updates_active'])
            box_02115.active = True
            box_02115.use_property_split = False
            box_02115.use_property_decorate = False
            box_02115.alignment = 'Expand'.upper()
            box_02115.scale_x = 1.0
            box_02115.scale_y = 1.0
            if not True: box_02115.operator_context = "EXEC_DEFAULT"
            box_02115.label(text='Camera update method', icon_value=0)
            box_02115.prop(bpy.context.scene, 'sna_dgs_camera_refresh_method', text='', icon_value=0, emboss=True)
            col_280A9.separator(factor=1.0)
            box_E25B6 = col_280A9.box()
            box_E25B6.alert = False
            box_E25B6.enabled = True
            box_E25B6.active = True
            box_E25B6.use_property_split = False
            box_E25B6.use_property_decorate = False
            box_E25B6.alignment = 'Expand'.upper()
            box_E25B6.scale_x = 1.0
            box_E25B6.scale_y = 1.0
            if not True: box_E25B6.operator_context = "EXEC_DEFAULT"
            if bpy.context.scene['gaussian_splat_updates_active']:
                op = box_E25B6.operator('sna.dgs__stop_camera_update_9ad85', text='Stop camera update', icon_value=3, emboss=True, depress=False)
            else:
                op = box_E25B6.operator('sna.dgs__start_camera_update_9eaff', text='Start camera update', icon_value=777, emboss=True, depress=False)
        col_E3544.separator(factor=1.0)
        col_6AEEE = col_E3544.column(heading='', align=False)
        col_6AEEE.alert = False
        col_6AEEE.enabled = True
        col_6AEEE.active = True
        col_6AEEE.use_property_split = False
        col_6AEEE.use_property_decorate = False
        col_6AEEE.scale_x = 1.0
        col_6AEEE.scale_y = 1.0
        col_6AEEE.alignment = 'Expand'.upper()
        col_6AEEE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_6AEEE.label(text='--- HQ Splat ---', icon_value=0)
        box_00C21 = col_6AEEE.box()
        box_00C21.alert = False
        box_00C21.enabled = True
        box_00C21.active = True
        box_00C21.use_property_split = False
        box_00C21.use_property_decorate = False
        box_00C21.alignment = 'Expand'.upper()
        box_00C21.scale_x = 1.0
        box_00C21.scale_y = 1.0
        if not True: box_00C21.operator_context = "EXEC_DEFAULT"
        box_00C21.label(text='.PLY Directory', icon_value=0)
        box_00C21.prop(bpy.context.scene, 'sna_dgs_ply_directory', text='', icon_value=0, emboss=True)
        if ((bpy.context.scene.sna_dgs_ply_directory == 'SELECT .PLY ASSETS PATH') or (bpy.context.scene.sna_dgs_ply_directory == '')):
            pass
        else:
            box_B7FC3 = col_6AEEE.box()
            box_B7FC3.alert = True
            box_B7FC3.enabled = True
            box_B7FC3.active = True
            box_B7FC3.use_property_split = False
            box_B7FC3.use_property_decorate = False
            box_B7FC3.alignment = 'Expand'.upper()
            box_B7FC3.scale_x = 1.0
            box_B7FC3.scale_y = 1.0
            if not True: box_B7FC3.operator_context = "EXEC_DEFAULT"
            op = box_B7FC3.operator('sna.generate_hq_splat_view_dependant_eafc2', text='Generate HQ Splat', icon_value=0, emboss=True, depress=False)
    else:
        box_75F0B = layout_function.box()
        box_75F0B.alert = False
        box_75F0B.enabled = True
        box_75F0B.active = True
        box_75F0B.use_property_split = False
        box_75F0B.use_property_decorate = False
        box_75F0B.alignment = 'Expand'.upper()
        box_75F0B.scale_x = 1.0
        box_75F0B.scale_y = 1.0
        if not True: box_75F0B.operator_context = "EXEC_DEFAULT"
        col_BA559 = box_75F0B.column(heading='', align=False)
        col_BA559.alert = False
        col_BA559.enabled = True
        col_BA559.active = True
        col_BA559.use_property_split = False
        col_BA559.use_property_decorate = False
        col_BA559.scale_x = 1.0
        col_BA559.scale_y = 1.0
        col_BA559.alignment = 'Expand'.upper()
        col_BA559.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_BA559.label(text='Eevee render engine required', icon_value=2)
        op = col_BA559.operator('sna.dgs__set_render_engine_to_eevee_7516e', text='Enable Eevee', icon_value=0, emboss=True, depress=False)

import bpy
import numpy as np
import os
from mathutils import Vector, Matrix
from typing import Tuple

# Move plyfile import to global scope
try:
    from plyfile import PlyData
    PLYFILE_AVAILABLE = True
except ImportError:
    PLYFILE_AVAILABLE = False
    print("plyfile is not installed. Please install it to use this feature.")


class SNA_OT_Generate_Hq_Splat_View_Dependant_Eafc2(bpy.types.Operator):
    bl_idname = "sna.generate_hq_splat_view_dependant_eafc2"
    bl_label = "Generate HQ Splat (View Dependant)"
    bl_description = "Generates a camera dependant high quality scan object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.view_layer.objects.active == None):
            self.report({'INFO'}, message='No active object')
        else:
            if (bpy.context.scene.camera == None):
                self.report({'ERROR'}, message='No active camera in scene')
            else:
                if 'update_rot_to_cam' in bpy.context.view_layer.objects.active:
                    if property_exists("bpy.data.materials['KIRI_3DGS_HQ_Render_Material']", globals(), locals()):
                        pass
                    else:
                        before_data = list(bpy.data.materials)
                        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND.blend') + r'\Material', filename='KIRI_3DGS_HQ_Render_Material', link=False)
                        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
                        appended_C2F6A = None if not new_data else new_data[0]
                    kiri__blender_splat_render__import__update__render['sna_dgs_lq_active'] = bpy.context.view_layer.objects.active
                    filepath = bpy.context.scene.sna_dgs_ply_directory + bpy.context.view_layer.objects.active.name + '.ply'
                    name = bpy.context.view_layer.objects.active.name + '_HQ_Splat'
                    origin_obj = bpy.context.view_layer.objects.active
                    output = None
                    from mathutils import Vector, Matrix 
                    import numpy as np
                    try:
                        from plyfile import PlyData
                    except ImportError:
                        print("plyfile is not installed. Please install it to use this feature.")
                        PlyData = None
                    #import time
                    class PlyInfo():

                        def __init__(self, filepath : str):
                            self.loadPly(filepath)

                        def loadPly(self,filepath : str):
                            plydata = PlyData.read(filepath)
                            self.center = np.stack((np.asarray(plydata.elements[0]["x"]),
                                                    np.asarray(plydata.elements[0]["y"]),
                                                    np.asarray(plydata.elements[0]["z"])), axis=1)
                            self.splat_count = int(len(self.center))
                            N =  self.splat_count
                            if 'opacity' in plydata.elements[0]:
                                log_opacities = np.asarray(plydata.elements[0]["opacity"])[..., np.newaxis]
                                self.opacities = 1 / (1 + np.exp(-log_opacities))
                            else:
                                log_opacities = np.asarray(1)[..., np.newaxis]
                                self.opacities = 1 / (1 + np.exp(-log_opacities))
                            self.opacities = self.opacities.flatten()
                            print("self.opacities", self.opacities)
                            self.features_dc = np.zeros((N, 3, 1))
                            self.features_dc[:, 0, 0] = np.asarray(plydata.elements[0]["f_dc_0"])
                            self.features_dc[:, 1, 0] = np.asarray(plydata.elements[0]["f_dc_1"])
                            self.features_dc[:, 2, 0] = np.asarray(plydata.elements[0]["f_dc_2"])
                            extra_f_names = [p.name for p in plydata.elements[0].properties if p.name.startswith("f_rest_")]
                            extra_f_names = sorted(extra_f_names, key=lambda x: int(x.split('_')[-1]))
                            features_extra = np.zeros((N, len(extra_f_names)))
                            for idx, attr_name in enumerate(extra_f_names):
                                features_extra[:, idx] = np.asarray(plydata.elements[0][attr_name])
                            features_extra = features_extra.reshape((N, 3, 15))
                            log_scales = np.stack((np.asarray(plydata.elements[0]["scale_0"]),
                                                   np.asarray(plydata.elements[0]["scale_1"]),
                                                   np.asarray(plydata.elements[0]["scale_2"])), axis=1)
                            self.scales = np.exp(log_scales)
                            self.quats = np.stack((np.asarray(plydata.elements[0]["rot_0"]),
                                              np.asarray(plydata.elements[0]["rot_1"]),
                                              np.asarray(plydata.elements[0]["rot_2"]),
                                              np.asarray(plydata.elements[0]["rot_3"])), axis=1)
                    class GuassianSplat:

                        def __init__(self, name: str, filepath: str, origin_obj: bpy.types.Object):
                            self.name = name
                            self.plyInfo = PlyInfo(filepath)
                            self.count = self.plyInfo.splat_count
                            self.origin_obj = origin_obj
                            self.vertices, self.indices = self.createGeometry()
                            self.sort()
                            self.object = self.createObject()
                            self.update_camera_info()

                        def __del__(self):
                            print(f"Object is being destroyed.")

                        def createGeometry(self) -> Tuple[list[Tuple],list[Tuple]]:
                            vertices = []
                            indices = []
                            for i in range(self.count):
                               vertices.append ([-2.0, -2.0, float(i)]),
                               vertices.append ([ 2.0, -2.0, float(i)]),
                               vertices.append ([ 2.0,  2.0, float(i)]),
                               vertices.append ([-2.0,  2.0, float(i)]),
                               b = i*4
                               indices.append((0+b,1+b,2+b))
                               indices.append((0+b,2+b,3+b))
                            return vertices, indices

                        def createObject(self) -> bpy.types.Object: 
                            count = self.count
                            mesh : bpy.types.Mesh = bpy.data.meshes.new(name= self.name)
                            mesh.from_pydata(self.vertices, [], self.indices)
                            obj : bpy.types.Object = bpy.data.objects.new(self.name, mesh)
                            obj.location = self.origin_obj.location.copy()
                            obj.rotation_euler = self.origin_obj.rotation_euler.copy()
                            obj.scale = self.origin_obj.scale.copy()  
                            Vrk_1 = [0.0] * count * 2 * 1 
                            Vrk_2 = [0.0] * count * 2 * 1
                            Vrk_3 = [0.0] * count * 2 * 1
                            Vrk_4 = [0.0] * count * 2 * 1
                            Vrk_5 = [0.0] * count * 2 * 1
                            Vrk_6 = [0.0] * count * 2 * 1
                            center= [0.0] * count * 2 * 3 
                            color = [0.0] * count * 2 * 4 
                            SH_0 =  0.28209479177387814
                            for i in range(self.count):
                               splat_id = self.splatID_array[i] 
                               RS = self.RS_matrix(self.plyInfo.quats[splat_id],self.plyInfo.scales[splat_id])
                               # Covariance Matrix
                               Vrk_1[2 * i + 0] = RS[0] * RS[0] + RS[3] * RS[3] + RS[6] * RS[6]
                               Vrk_1[2 * i + 1] = RS[0] * RS[0] + RS[3] * RS[3] + RS[6] * RS[6]
                               Vrk_2[2 * i + 0] = RS[0] * RS[1] + RS[3] * RS[4] + RS[6] * RS[7]
                               Vrk_2[2 * i + 1] = RS[0] * RS[1] + RS[3] * RS[4] + RS[6] * RS[7]
                               Vrk_3[2 * i + 0] = RS[0] * RS[2] + RS[3] * RS[5] + RS[6] * RS[8]
                               Vrk_3[2 * i + 1] = RS[0] * RS[2] + RS[3] * RS[5] + RS[6] * RS[8]
                               Vrk_4[2 * i + 0] = RS[1] * RS[1] + RS[4] * RS[4] + RS[7] * RS[7]
                               Vrk_4[2 * i + 1] = RS[1] * RS[1] + RS[4] * RS[4] + RS[7] * RS[7]
                               Vrk_5[2 * i + 0] = RS[1] * RS[2] + RS[4] * RS[5] + RS[7] * RS[8]
                               Vrk_5[2 * i + 1] = RS[1] * RS[2] + RS[4] * RS[5] + RS[7] * RS[8]
                               Vrk_6[2 * i + 0] = RS[2] * RS[2] + RS[5] * RS[5] + RS[8] * RS[8]
                               Vrk_6[2 * i + 1] = RS[2] * RS[2] + RS[5] * RS[5] + RS[8] * RS[8]
                               center[6 * i + 0] =  self.plyInfo.center[splat_id][0]
                               center[6 * i + 1] =  self.plyInfo.center[splat_id][1]
                               center[6 * i + 2] =  self.plyInfo.center[splat_id][2]
                               center[6 * i + 3] =  self.plyInfo.center[splat_id][0]
                               center[6 * i + 4] =  self.plyInfo.center[splat_id][1]
                               center[6 * i + 5] =  self.plyInfo.center[splat_id][2]
                               R = (self.plyInfo.features_dc[splat_id][0][0] * SH_0 + 0.5) 
                               G = (self.plyInfo.features_dc[splat_id][1][0] * SH_0 + 0.5) 
                               B = (self.plyInfo.features_dc[splat_id][2][0] * SH_0 + 0.5) 
                               A = self.plyInfo.opacities[splat_id]
                               color [8 * i + 0] = R
                               color [8 * i + 1] = G
                               color [8 * i + 2] = B
                               color [8 * i + 3] = A
                               color [8 * i + 4] = R
                               color [8 * i + 5] = G 
                               color [8 * i + 6] = B
                               color [8 * i + 7] = A
                            center_attr : bpy.types.FloatVectorAttribute = mesh.attributes.new(name="center", type='FLOAT_VECTOR', domain='FACE')
                            center_attr.data.foreach_set("vector", center)
                            color_attr : bpy.types.ByteColorAttribute = mesh.attributes.new(name="color", type='FLOAT_COLOR', domain='FACE')
                            color_attr.data.foreach_set("color", color)
                            Vrk_1_attr = mesh.attributes.new(name="Vrk_1", type='FLOAT', domain='FACE')
                            Vrk_1_attr.data.foreach_set("value", Vrk_1)
                            Vrk_2_attr = mesh.attributes.new(name="Vrk_2", type='FLOAT', domain='FACE')
                            Vrk_2_attr.data.foreach_set("value", Vrk_2)
                            Vrk_3_attr = mesh.attributes.new(name="Vrk_3", type='FLOAT', domain='FACE')
                            Vrk_3_attr.data.foreach_set("value", Vrk_3)
                            Vrk_4_attr = mesh.attributes.new(name="Vrk_4", type='FLOAT', domain='FACE')
                            Vrk_4_attr.data.foreach_set("value", Vrk_4)
                            Vrk_5_attr = mesh.attributes.new(name="Vrk_5", type='FLOAT', domain='FACE')
                            Vrk_5_attr.data.foreach_set("value", Vrk_5)
                            Vrk_6_attr = mesh.attributes.new(name="Vrk_6", type='FLOAT', domain='FACE')
                            Vrk_6_attr.data.foreach_set("value", Vrk_6)
                            node_group = bpy.data.node_groups['KIRI_3DGS_Render_GN']
                            node_modifier : bpy.types.NodesModifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
                            node_modifier.node_group = node_group
                            material = None
                            for mat in bpy.data.materials:
                                if(mat.name == "KIRI_3DGS_HQ_Render_Material"):
                                    material = mat
                                    break
                            if obj and obj.data:
                                if len(obj.material_slots) < 1:
                                    obj.data.materials.append(material)
                                else:
                                    obj.material_slots[0].material = material
                            bpy.context.collection.objects.link(obj)
                            bpy.context.view_layer.objects.active = obj
                            obj.select_set(True)
                            return obj

                        def getMainCamera(self) -> bpy.types.RegionView3D:
                            for area in bpy.context.screen.areas:
                                if(area.type =='VIEW_3D'):
                                    main_camera  = area.spaces.active.region_3d
                                    return main_camera , area

                        def RS_matrix(self,quat : np.ndarray ,scale : np.ndarray) -> list[int] :
                            matrix = []
                            length = 1/ math.sqrt(quat[0] *quat[0]  + quat[1] *quat[1]  + quat[2] *quat[2] + quat[3] *quat[3] )
                            x = quat[0] * length 
                            y = quat[1] * length 
                            z = quat[2] * length 
                            w = quat[3] * length 
                            matrix.append (scale[0] * (1 - 2 * (z * z + w * w)))
                            matrix.append (scale[0] * (2 * (y * z + x * w)))
                            matrix.append (scale[0] * (2 * (y * w - x * z)))
                            matrix.append (scale[1] * (2 * (y * z - x * w)))
                            matrix.append (scale[1] * (1 - 2 * (y * y + w * w)))
                            matrix.append (scale[1] * (2 * (z * w + x * y)))
                            matrix.append (scale[2] * (2 * (y * w + x * z)))
                            matrix.append (scale[2] * (2 * (z * w - x * y)))
                            matrix.append (scale[2] * (1 - 2* (y * y + z * z)))
                            return matrix

                        def update_camera_info(self, ):
                            camera : bpy.types.Object = bpy.context.scene.camera
                            view_matrix = camera.matrix_world.inverted()
                            depsgraph = bpy.context.evaluated_depsgraph_get()
                            scene = bpy.context.scene
                            resolution_x = scene.render.resolution_x
                            resolution_y = scene.render.resolution_y
                            proj_matrix = camera.calc_matrix_camera(depsgraph,
                                                                    x = resolution_x,
                                                                    y = resolution_y)
                            geometryNodes_modifier : bpy.types.NodesModifier = self.object.modifiers['GeometryNodes']
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
                            geometryNodes_modifier['Socket_34'] = resolution_x
                            geometryNodes_modifier['Socket_35'] = resolution_y
                            geometryNodes_modifier.show_on_cage = True
                            geometryNodes_modifier.show_on_cage = False

                        def create_Tick(self):
                            bpy.app.timers.register(self.update_camera_info)

                        def destroy_Tick(self):
                            if(bpy.app.timers.is_registered(self.update_camera_info)):
                                bpy.app.timers.unregister(self.update_camera_info)
                        #def render(self):        
                            #self.new_collection.hide_render = True
                            #bpy.context.scene.render.filepath = "C:/Users/xiaoh/Desktop/project/3DGS/3DGS-Blender-Addon/RENDER RESULT/render_output.png"
                            #bpy.ops.render.render(write_still=True)
                            #bpy.context.scene.render.use_lock_interface = True
                            #bpy.ops.render.render('EXEC_DEFAULT')
                            #bpy.context.scene.render.use_lock_interface = False
                            #begin = time.time()
                            #end = time.time() 
                            #print("deletime" , end - begin)
                            #print("render finish")

                        def get_camera_info(self):
                            for area in bpy.context.screen.areas:
                                if(area.type == 'VIEW_3D'):
                                    self.mainCamera  = area.spaces.active.region_3d
                                    self.window      = area
                                    break 
                            view_matrix : Matrix =  self.mainCamera.view_matrix
                            proj_matrix : Matrix =  self.mainCamera.window_matrix
                            return view_matrix , proj_matrix

                        def sort(self):
                            count = self.count
                            origin_obj = self.origin_obj
                            camera : bpy.types.Object = bpy.context.scene.camera
                            camera_model_matrix : Matrix = origin_obj.matrix_world.inverted() @  camera.matrix_world
                            self.splatID_array = np.ndarray((count), dtype= np.int32)
                            camera_array = [0.0] * 6
                            # realative position
                            camera_array[0] = camera_model_matrix[0][3] 
                            camera_array[1] = camera_model_matrix[1][3] 
                            camera_array[2] = camera_model_matrix[2][3] 
                            direction : Vector = Vector.Fill(3,0)
                            direction.x = camera_model_matrix[0][2]
                            direction.y = camera_model_matrix[1][2]
                            direction.z = camera_model_matrix[2][2]
                            direction.normalize()
                            # direction
                            camera_array[3] = direction.x
                            camera_array[4] = direction.y
                            camera_array[5] = direction.z
                            bound_min = {"x": 0.0, "y": 0.0, "z": 0.0}
                            bound_max = {"x": 0.0, "y": 0.0, "z": 0.0}
                            bucket_count = 0
                            bound_min["x"] = bound_max["x"] = self.plyInfo.center[0][0]
                            bound_min["y"] = bound_max["y"] = self.plyInfo.center[0][1]
                            bound_min["z"] = bound_max["z"] = self.plyInfo.center[0][2]
                            # Calculate bounding box of all vertices
                            for i in range(1, count):
                                x = self.plyInfo.center[i][0]
                                y = self.plyInfo.center[i][1]
                                z = self.plyInfo.center[i][2]
                                bound_min["x"] = min(bound_min["x"], x)
                                bound_min["y"] = min(bound_min["y"], y)
                                bound_min["z"] = min(bound_min["z"], z)
                                bound_max["x"] = max(bound_max["x"], x)
                                bound_max["y"] = max(bound_max["y"], y)
                                bound_max["z"] = max(bound_max["z"], z)
                            compare_bits = 16
                            bucket_count = 2 ** compare_bits + 1
                            distances = np.zeros(count, dtype= np.int32)
                            count_buffer = np.zeros(bucket_count, dtype= np.int32)  # 与 Uint32Array 相对应
                            px, py, pz = camera_array[0], camera_array[1], camera_array[2]
                            dx, dy, dz = camera_array[3], camera_array[4], camera_array[5]
                            min_dist = max_dist = None
                            # Calculate min/max distance between camera and bounding box
                            for i in range(8):
                                x = bound_min["x"] if i & 1 else bound_max["x"]
                                y = bound_min["y"] if i & 2 else bound_max["y"]
                                z = bound_min["z"] if i & 4 else bound_max["z"]
                                d = (x - px) * dx + (y - py) * dy + (z - pz) * dz
                                if i == 0:
                                    min_dist = max_dist = d
                                else:
                                    min_dist = min(min_dist, d)
                                    max_dist = max(max_dist, d)
                            for i in range(bucket_count):
                                count_buffer[i] = 0
                            range_dist = (max_dist - min_dist + 1e-7)
                            divider = (1 / range_dist) * 2 ** compare_bits
                            for i in range(count):
                                istride = i 
                                d = (self.plyInfo.center[istride][0] - px) * dx + (self.plyInfo.center[istride][1] - py) * dy + (self.plyInfo.center[istride][2] - pz) * dz
                                sort_key = int((d - min_dist) * divider)
                                distances[i] = sort_key
                                count_buffer[sort_key] += 1
                            for i in range(1, bucket_count):
                                count_buffer[i] += count_buffer[i - 1]
                            for i in range(count - 1, -1, -1):
                                distance = distances[i]
                                self.splatID_array[count_buffer[distance] - 1] = i
                                count_buffer[distance] -= 1
                            print(self.splatID_array)
                    # Serpens node function

                    def create_gaussian_splat(filepath: str, name: str, origin_obj: bpy.types.Object):
                        print(f"Creating Gaussian Splat with file: {filepath}, name: {name}, origin object: {origin_obj.name}")
                        gs = GuassianSplat(name, filepath, origin_obj)
                        print(f"Gaussian Splat object created: {gs.object.name}")
                        return gs.object
                    # Serpens node setup
                    inputs = {
                        "filepath": "String",
                        "name": "String",
                        "origin_obj": "Object"
                    }
                    outputs = {
                        "object": "Object"
                    }
                    # This function will be called by Serpens

                    def create_gaussian_splat(filepath, name, origin_obj):
                        print(f"Creating Gaussian Splat with file: {filepath}, name: {name}, origin object: {origin_obj.name}")
                        try:
                            gs = GuassianSplat(name, filepath, origin_obj)
                            print(f"Gaussian Splat object created: {gs.object.name}")
                            return gs.object
                        except Exception as e:
                            print(f"Error occurred: {str(e)}")
                            return None
                    # Serpens will use this dictionary to get the result
                    output = {
                        "object": create_gaussian_splat(filepath, name, origin_obj)
                    }
                    # For testing in Blender Text Editor (comment out when using in Serpens)
                    # filepath = "C:\\Users\\joe and pig\\Documents\\Flamingo.ply"
                    # name = "newGaussianSplat"
                    # origin_obj = bpy.context.active_object
                    # test_output = create_gaussian_splat(filepath, name, origin_obj)
                    # print(f"Test output: {test_output}")
                    if (output == None):
                        self.report({'INFO'}, message='No splat created - check directory contains matching file and files have not been renamed')
                    else:
                        self.report({'INFO'}, message='The generated object will only render correctly from the current active camera view')
                        kiri__blender_splat_render__import__update__render['sna_dgs_lq_active'].hide_viewport = True
                        kiri__blender_splat_render__import__update__render['sna_dgs_lq_active'].hide_render = True
                    kiri__blender_splat_render__import__update__render['sna_dgs_lq_active'] = None
                else:
                    self.report({'ERROR'}, message='Active object is not a 3DGS scan imported by the add-on')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_72797(bpy.types.Panel):
    bl_label = '3DGS Render by KIRI Engine'
    bl_idname = 'SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_72797'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = '3DGS Render by KIRI Engine'
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
        col_D0725 = layout.column(heading='', align=False)
        col_D0725.alert = False
        col_D0725.enabled = True
        col_D0725.active = True
        col_D0725.use_property_split = False
        col_D0725.use_property_decorate = False
        col_D0725.scale_x = 1.0
        col_D0725.scale_y = 1.0
        col_D0725.alignment = 'Expand'.upper()
        col_D0725.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_D0725.label(text='What does it do?', icon_value=0)
        col_D0725.separator(factor=1.0)
        box_55229 = col_D0725.box()
        box_55229.alert = False
        box_55229.enabled = True
        box_55229.active = True
        box_55229.use_property_split = False
        box_55229.use_property_decorate = False
        box_55229.alignment = 'Expand'.upper()
        box_55229.scale_x = 1.0
        box_55229.scale_y = 0.800000011920929
        if not True: box_55229.operator_context = "EXEC_DEFAULT"
        col_9A518 = box_55229.column(heading='', align=False)
        col_9A518.alert = False
        col_9A518.enabled = True
        col_9A518.active = True
        col_9A518.use_property_split = False
        col_9A518.use_property_decorate = False
        col_9A518.scale_x = 1.0
        col_9A518.scale_y = 1.0
        col_9A518.alignment = 'Expand'.upper()
        col_9A518.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_9A518.label(text=' • Automatically converts 3DGS scans ', icon_value=0)
        col_9A518.label(text='    into Eevee renderable objects.', icon_value=0)
        col_9A518.label(text=' • Camera updates can be continuous or', icon_value=0)
        col_9A518.label(text='     enabled on frame changes for animations.', icon_value=0)
        col_D0725.separator(factor=1.0)
        col_D0725.label(text='--- Import / Update ---', icon_value=0)
        col_D0725.separator(factor=1.0)
        layout_function = col_D0725
        sna_splat_render__main_functions_3FCFA(layout_function, )
        col_D0725.separator(factor=1.0)
        if (bpy.context.view_layer.objects.active == None):
            pass
        else:
            col_D0725.label(text='--- Object Update / Shading---', icon_value=0)
        if (bpy.context.view_layer.objects.active == None):
            pass
        else:
            layout_function = col_D0725
            sna_dgs__active_object_interface_func_9588F(layout_function, )
        col_D0725.separator(factor=1.0)
        layout_function = col_D0725
        sna_documentation_interface_function_A1B59(layout_function, )
        col_D0725.separator(factor=1.0)
        layout_function = col_D0725
        sna_about_and_external_links_interface_function_8E1B8(layout_function, )


class SNA_AddonPreferences_10BAB(bpy.types.AddonPreferences):
    bl_idname = 'gs_render_by_kiri_engine'
    sna_set_colour_space_on_import: bpy.props.BoolProperty(name='Set colour space on import', description='', default=True)
    sna_enable_header_color_warning: bpy.props.BoolProperty(name='Enable header color warning', description='', default=True)
    sna_camera_update_warning_colour: bpy.props.FloatVectorProperty(name='Camera update warning colour', description='', size=4, default=(0.06301099807024002, 0.16826699674129486, 0.450778990983963, 1.0), subtype='COLOR', unit='NONE', step=3, precision=6)

    def draw(self, context):
        if not (False):
            layout = self.layout 
            box_33CA0 = layout.box()
            box_33CA0.alert = False
            box_33CA0.enabled = True
            box_33CA0.active = True
            box_33CA0.use_property_split = False
            box_33CA0.use_property_decorate = False
            box_33CA0.alignment = 'Expand'.upper()
            box_33CA0.scale_x = 1.0
            box_33CA0.scale_y = 1.0
            if not True: box_33CA0.operator_context = "EXEC_DEFAULT"
            box_33CA0.label(text='--- Appearance ---', icon_value=0)
            op = box_33CA0.operator('sna.dgs_restore_default_blender_header_colour_0da65', text='Restore default Blender header colour', icon_value=0, emboss=True, depress=False)
            box_33CA0.prop(bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences, 'sna_enable_header_color_warning', text='Enable header color warning when camera update is active', icon_value=0, emboss=True)
            if bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences.sna_enable_header_color_warning:
                prop = bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences.bl_rna.properties['sna_camera_update_warning_colour'].subtype
                if prop in ('COLOR' , 'COLOR_GAMMA'):
                    box_33CA0.template_color_picker(bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences, 'sna_camera_update_warning_colour', value_slider=True, lock=False, lock_luminosity=False, cubic=False)
                    row = box_33CA0.row(heading='', align=False)
                    col = row.column(heading='', align=True)
                    if True:
                        col.prop(bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences, 'sna_camera_update_warning_colour', text='', icon_value=0, emboss=True, expand=False)
                    if False:
                        col.prop(bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences, 'sna_camera_update_warning_colour', text='', icon_value=0, emboss=True, expand=True, slider = True)
                else:
                    box_33CA0.label(text='No Color Property connected!', icon='ERROR')
            box_8546E = layout.box()
            box_8546E.alert = False
            box_8546E.enabled = True
            box_8546E.active = True
            box_8546E.use_property_split = False
            box_8546E.use_property_decorate = False
            box_8546E.alignment = 'Expand'.upper()
            box_8546E.scale_x = 1.0
            box_8546E.scale_y = 1.0
            if not True: box_8546E.operator_context = "EXEC_DEFAULT"
            box_8546E.label(text='--- Render Settings ---', icon_value=0)
            box_8546E.prop(bpy.context.preferences.addons['gs_render_by_kiri_engine'].preferences, 'sna_set_colour_space_on_import', text='Set colour space to standard on .ply import', icon_value=0, emboss=True)


class SNA_OT_Dgs_Restore_Default_Blender_Header_Colour_0Da65(bpy.types.Operator):
    bl_idname = "sna.dgs_restore_default_blender_header_colour_0da65"
    bl_label = "3DGS Restore default Blender header colour"
    bl_description = "Restores the default grey colour of the Blender UI"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.preferences.themes['Default'].user_interface.wcol_box.inner = (0.11372499912977219, 0.11372499912977219, 0.11372499912977219, 0.5019609928131104)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_dgs__active_object_interface_func_9588F(layout_function, ):
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        col_81FEC = layout_function.column(heading='', align=False)
        col_81FEC.alert = False
        col_81FEC.enabled = True
        col_81FEC.active = True
        col_81FEC.use_property_split = False
        col_81FEC.use_property_decorate = False
        col_81FEC.scale_x = 1.0
        col_81FEC.scale_y = 1.0
        col_81FEC.alignment = 'Expand'.upper()
        col_81FEC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if 'update_rot_to_cam' in bpy.context.view_layer.objects.active:
            box_F59B2 = col_81FEC.box()
            box_F59B2.alert = False
            box_F59B2.enabled = True
            box_F59B2.active = True
            box_F59B2.use_property_split = False
            box_F59B2.use_property_decorate = False
            box_F59B2.alignment = 'Expand'.upper()
            box_F59B2.scale_x = 1.0
            box_F59B2.scale_y = 1.0
            if not True: box_F59B2.operator_context = "EXEC_DEFAULT"
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                if 'update_rot_to_cam' in bpy.context.view_layer.objects.active:
                    box_5D1B8 = box_F59B2.box()
                    box_5D1B8.alert = False
                    box_5D1B8.enabled = True
                    box_5D1B8.active = True
                    box_5D1B8.use_property_split = False
                    box_5D1B8.use_property_decorate = False
                    box_5D1B8.alignment = 'Expand'.upper()
                    box_5D1B8.scale_x = 1.0
                    box_5D1B8.scale_y = 1.0
                    if not True: box_5D1B8.operator_context = "EXEC_DEFAULT"
                    box_5D1B8.label(text=bpy.context.view_layer.objects.active.name, icon_value=0)
                    attr_27871 = '["' + str('update_rot_to_cam' + '"]') 
                    box_5D1B8.prop(bpy.context.view_layer.objects.active, attr_27871, text=('Updates are active' if bpy.context.view_layer.objects.active['update_rot_to_cam'] else 'Updates are inactive'), icon_value=0, emboss=True, toggle=True)
        if ((property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_Render_Material' in bpy.context.view_layer.objects.active.material_slots) or (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots)):
            col_CF82B = col_81FEC.column(heading='', align=False)
            col_CF82B.alert = False
            col_CF82B.enabled = True
            col_CF82B.active = True
            col_CF82B.use_property_split = False
            col_CF82B.use_property_decorate = False
            col_CF82B.scale_x = 1.0
            col_CF82B.scale_y = 1.0
            col_CF82B.alignment = 'Expand'.upper()
            col_CF82B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if ((property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_Render_Material' in bpy.context.view_layer.objects.active.material_slots) or (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots)):
                box_E8D95 = col_CF82B.box()
                box_E8D95.alert = False
                box_E8D95.enabled = True
                box_E8D95.active = True
                box_E8D95.use_property_split = False
                box_E8D95.use_property_decorate = False
                box_E8D95.alignment = 'Expand'.upper()
                box_E8D95.scale_x = 1.0
                box_E8D95.scale_y = 1.0
                if not True: box_E8D95.operator_context = "EXEC_DEFAULT"
                col_1DE6F = box_E8D95.column(heading='', align=False)
                col_1DE6F.alert = False
                col_1DE6F.enabled = True
                col_1DE6F.active = True
                col_1DE6F.use_property_split = False
                col_1DE6F.use_property_decorate = False
                col_1DE6F.scale_x = 1.0
                col_1DE6F.scale_y = 1.0
                col_1DE6F.alignment = 'Expand'.upper()
                col_1DE6F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                box_75086 = col_1DE6F.box()
                box_75086.alert = False
                box_75086.enabled = True
                box_75086.active = True
                box_75086.use_property_split = False
                box_75086.use_property_decorate = False
                box_75086.alignment = 'Expand'.upper()
                box_75086.scale_x = 1.0
                box_75086.scale_y = 1.0
                if not True: box_75086.operator_context = "EXEC_DEFAULT"
                box_75086.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[2], 'default_value', text='Shadeless', icon_value=0, emboss=True, toggle=True)
                box_CEF2A = col_1DE6F.box()
                box_CEF2A.alert = False
                box_CEF2A.enabled = True
                box_CEF2A.active = True
                box_CEF2A.use_property_split = False
                box_CEF2A.use_property_decorate = False
                box_CEF2A.alignment = 'Expand'.upper()
                box_CEF2A.scale_x = 1.0
                box_CEF2A.scale_y = 1.0
                if not True: box_CEF2A.operator_context = "EXEC_DEFAULT"
                box_CEF2A.prop(bpy.context.view_layer.objects.active.active_material, 'sna_dgs_show_base_colour_adjustments', text='Show Colour Adjustments', icon_value=0, emboss=True, toggle=True)
                if bpy.context.view_layer.objects.active.active_material.sna_dgs_show_base_colour_adjustments:
                    box_D0687 = box_CEF2A.box()
                    box_D0687.alert = False
                    box_D0687.enabled = True
                    box_D0687.active = True
                    box_D0687.use_property_split = False
                    box_D0687.use_property_decorate = False
                    box_D0687.alignment = 'Expand'.upper()
                    box_D0687.scale_x = 1.0
                    box_D0687.scale_y = 1.0
                    if not True: box_D0687.operator_context = "EXEC_DEFAULT"
                    box_D0687.label(text='Brightness', icon_value=0)
                    box_D0687.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[3], 'default_value', text='', icon_value=0, emboss=True)
                    box_D0687.label(text='Contrast', icon_value=0)
                    box_D0687.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[4], 'default_value', text='', icon_value=0, emboss=True)
                    box_D0687.label(text='Hue', icon_value=0)
                    box_D0687.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[5], 'default_value', text='', icon_value=0, emboss=True)
                    box_D0687.label(text='Saturation', icon_value=0)
                    box_D0687.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[6], 'default_value', text='', icon_value=0, emboss=True)
                box_E9069 = col_1DE6F.box()
                box_E9069.alert = False
                box_E9069.enabled = True
                box_E9069.active = True
                box_E9069.use_property_split = False
                box_E9069.use_property_decorate = False
                box_E9069.alignment = 'Expand'.upper()
                box_E9069.scale_x = 1.0
                box_E9069.scale_y = 1.0
                if not True: box_E9069.operator_context = "EXEC_DEFAULT"
                box_E9069.prop(bpy.context.view_layer.objects.active.active_material, 'sna_dg_show_colour_masks', text='Show Colour Masks', icon_value=0, emboss=True, toggle=True)
                if bpy.context.view_layer.objects.active.active_material.sna_dg_show_colour_masks:
                    box_01114 = box_E9069.box()
                    box_01114.alert = False
                    box_01114.enabled = True
                    box_01114.active = True
                    box_01114.use_property_split = False
                    box_01114.use_property_decorate = False
                    box_01114.alignment = 'Expand'.upper()
                    box_01114.scale_x = 1.0
                    box_01114.scale_y = 1.0
                    if not True: box_01114.operator_context = "EXEC_DEFAULT"
                    box_01114.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[11], 'default_value', text='Enable Colour Mask 1', icon_value=0, emboss=True, toggle=True)
                    if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[11].default_value:
                        col_93035 = box_01114.column(heading='', align=False)
                        col_93035.alert = False
                        col_93035.enabled = True
                        col_93035.active = True
                        col_93035.use_property_split = False
                        col_93035.use_property_decorate = False
                        col_93035.scale_x = 1.0
                        col_93035.scale_y = 1.0
                        col_93035.alignment = 'Expand'.upper()
                        col_93035.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                        col_93035.label(text='Colour Selection', icon_value=0)
                        col_93035.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[12], 'default_value', text='', icon_value=0, emboss=True)
                        col_93035.label(text='Change to', icon_value=0)
                        col_93035.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[13], 'default_value', text='', icon_value=0, emboss=True)
                        col_93035.label(text='Replacement Method', icon_value=0)
                        col_93035.prop(bpy.data.node_groups[('3DGS_HQ_Render_Material_Main_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Material_Main_Shader')].nodes['Mask 1 Change Method'], 'blend_type', text='', icon_value=0, emboss=True)
                        col_93035.label(text='Mix Factor', icon_value=0)
                        col_93035.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[14], 'default_value', text='', icon_value=0, emboss=True)
                        col_93035.label(text='Hue Tolerance', icon_value=0)
                        col_93035.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[15], 'default_value', text='', icon_value=0, emboss=True)
                        col_93035.label(text='Saturation Tolerance', icon_value=0)
                        col_93035.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[16], 'default_value', text='', icon_value=0, emboss=True)
                        col_93035.label(text='Value Tolerance', icon_value=0)
                        col_93035.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[17], 'default_value', text='', icon_value=0, emboss=True)
                if bpy.context.view_layer.objects.active.active_material.sna_dg_show_colour_masks:
                    box_37A8C = box_E9069.box()
                    box_37A8C.alert = False
                    box_37A8C.enabled = True
                    box_37A8C.active = True
                    box_37A8C.use_property_split = False
                    box_37A8C.use_property_decorate = False
                    box_37A8C.alignment = 'Expand'.upper()
                    box_37A8C.scale_x = 1.0
                    box_37A8C.scale_y = 1.0
                    if not True: box_37A8C.operator_context = "EXEC_DEFAULT"
                    box_37A8C.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[18], 'default_value', text='Enable Colour Mask 2', icon_value=0, emboss=True, toggle=True)
                    if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[18].default_value:
                        col_7B27A = box_37A8C.column(heading='', align=False)
                        col_7B27A.alert = False
                        col_7B27A.enabled = True
                        col_7B27A.active = True
                        col_7B27A.use_property_split = False
                        col_7B27A.use_property_decorate = False
                        col_7B27A.scale_x = 1.0
                        col_7B27A.scale_y = 1.0
                        col_7B27A.alignment = 'Expand'.upper()
                        col_7B27A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                        col_7B27A.label(text='Colour Selection', icon_value=0)
                        col_7B27A.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[19], 'default_value', text='', icon_value=0, emboss=True)
                        col_7B27A.label(text='Change to', icon_value=0)
                        col_7B27A.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[20], 'default_value', text='', icon_value=0, emboss=True)
                        col_7B27A.label(text='Replacement Method', icon_value=0)
                        col_7B27A.prop(bpy.data.node_groups[('3DGS_HQ_Render_Material_Main_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Material_Main_Shader')].nodes['Mask 2 Change Method'], 'blend_type', text='', icon_value=0, emboss=True)
                        col_7B27A.label(text='Mix Factor', icon_value=0)
                        col_7B27A.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[21], 'default_value', text='', icon_value=0, emboss=True)
                        col_7B27A.label(text='Hue Tolerance', icon_value=0)
                        col_7B27A.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[22], 'default_value', text='', icon_value=0, emboss=True)
                        col_7B27A.label(text='Saturation Tolerance', icon_value=0)
                        col_7B27A.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[23], 'default_value', text='', icon_value=0, emboss=True)
                        col_7B27A.label(text='Value Tolerance', icon_value=0)
                        col_7B27A.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[24], 'default_value', text='', icon_value=0, emboss=True)
                if bpy.context.view_layer.objects.active.active_material.sna_dg_show_colour_masks:
                    box_42489 = box_E9069.box()
                    box_42489.alert = False
                    box_42489.enabled = True
                    box_42489.active = True
                    box_42489.use_property_split = False
                    box_42489.use_property_decorate = False
                    box_42489.alignment = 'Expand'.upper()
                    box_42489.scale_x = 1.0
                    box_42489.scale_y = 1.0
                    if not True: box_42489.operator_context = "EXEC_DEFAULT"
                    box_42489.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[25], 'default_value', text='Enable Colour Mask 3', icon_value=0, emboss=True, toggle=True)
                    if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[25].default_value:
                        col_8A451 = box_42489.column(heading='', align=False)
                        col_8A451.alert = False
                        col_8A451.enabled = True
                        col_8A451.active = True
                        col_8A451.use_property_split = False
                        col_8A451.use_property_decorate = False
                        col_8A451.scale_x = 1.0
                        col_8A451.scale_y = 1.0
                        col_8A451.alignment = 'Expand'.upper()
                        col_8A451.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                        col_8A451.label(text='Colour Selection', icon_value=0)
                        col_8A451.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[26], 'default_value', text='', icon_value=0, emboss=True)
                        col_8A451.label(text='Change to', icon_value=0)
                        col_8A451.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[27], 'default_value', text='', icon_value=0, emboss=True)
                        col_8A451.label(text='Replacement Method', icon_value=0)
                        col_8A451.prop(bpy.data.node_groups[('3DGS_HQ_Render_Material_Main_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Material_Main_Shader')].nodes['Mask 3 Change Method'], 'blend_type', text='', icon_value=0, emboss=True)
                        col_8A451.label(text='Mix Factor', icon_value=0)
                        col_8A451.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[28], 'default_value', text='', icon_value=0, emboss=True)
                        col_8A451.label(text='Hue Tolerance', icon_value=0)
                        col_8A451.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[29], 'default_value', text='', icon_value=0, emboss=True)
                        col_8A451.label(text='Saturation Tolerance', icon_value=0)
                        col_8A451.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[30], 'default_value', text='', icon_value=0, emboss=True)
                        col_8A451.label(text='Value Tolerance', icon_value=0)
                        col_8A451.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[31], 'default_value', text='', icon_value=0, emboss=True)
                if bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[2].default_value:
                    pass
                else:
                    box_E38D0 = col_1DE6F.box()
                    box_E38D0.alert = False
                    box_E38D0.enabled = True
                    box_E38D0.active = True
                    box_E38D0.use_property_split = False
                    box_E38D0.use_property_decorate = False
                    box_E38D0.alignment = 'Expand'.upper()
                    box_E38D0.scale_x = 1.0
                    box_E38D0.scale_y = 1.0
                    if not True: box_E38D0.operator_context = "EXEC_DEFAULT"
                    box_E38D0.prop(bpy.context.view_layer.objects.active.active_material, 'sna_dgs_show_bsdf_settings', text='Show BSDF Settings', icon_value=0, emboss=True, toggle=True)
                    if bpy.context.view_layer.objects.active.active_material.sna_dgs_show_bsdf_settings:
                        box_90456 = box_E38D0.box()
                        box_90456.alert = False
                        box_90456.enabled = True
                        box_90456.active = True
                        box_90456.use_property_split = False
                        box_90456.use_property_decorate = False
                        box_90456.alignment = 'Expand'.upper()
                        box_90456.scale_x = 1.0
                        box_90456.scale_y = 1.0
                        if not True: box_90456.operator_context = "EXEC_DEFAULT"
                        box_90456.label(text='Metallic', icon_value=0)
                        box_90456.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[32], 'default_value', text='', icon_value=0, emboss=True)
                        box_90456.label(text='Roughness', icon_value=0)
                        box_90456.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[33], 'default_value', text='', icon_value=0, emboss=True)
                        box_90456.label(text='Emission Strength', icon_value=0)
                        box_90456.prop(bpy.data.materials[('KIRI_3DGS_HQ_Render_Material' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else 'KIRI_3DGS_Render_Material')].node_tree.nodes[('3DGS_HQ_Render_Shader' if (property_exists("bpy.context.view_layer.objects.active.material_slots", globals(), locals()) and 'KIRI_3DGS_HQ_Render_Material' in bpy.context.view_layer.objects.active.material_slots) else '3DGS_Render_Shader')].inputs[34], 'default_value', text='', icon_value=0, emboss=True)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_dgs_camera_refresh_method = bpy.props.EnumProperty(name='3DGS Camera Refresh Method', description='', items=[('Continuous', 'Continuous', '', 0, 0), ('Frame Change', 'Frame Change', '', 0, 1)])
    bpy.types.Material.sna_dgs_show_base_colour_adjustments = bpy.props.BoolProperty(name='3DGS Show Base Colour Adjustments', description='', default=False)
    bpy.types.Material.sna_dg_show_colour_masks = bpy.props.BoolProperty(name='3DG Show Colour Masks', description='', default=False)
    bpy.types.Material.sna_dgs_show_bsdf_settings = bpy.props.BoolProperty(name='3DGS Show BSDF Settings', description='', default=False)
    bpy.types.Scene.sna_dgs_ply_directory = bpy.props.StringProperty(name='3DGS PLY Directory', description='', default='SELECT .PLY ASSETS PATH', subtype='DIR_PATH', maxlen=0)
    bpy.utils.register_class(SNA_OT_Open_Blender_Splat_Render_Documentation_1Eac5)
    bpy.utils.register_class(SNA_OT_Open_Blender_Splat_Render_Tutorial_Video_A4Fe6)
    bpy.utils.register_class(SNA_OT_Launch_Kiri_Site_D26Bf)
    bpy.utils.register_class(SNA_OT_Launch_Blender_Market_77F72)
    bpy.utils.register_class(SNA_OT_Dgs__Import_Ply_As_Splats_8458E)
    bpy.utils.register_class(SNA_OT_Dgs__Start_Camera_Update_9Eaff)
    bpy.utils.register_class(SNA_OT_Dgs__Stop_Camera_Update_9Ad85)
    bpy.utils.register_class(SNA_OT_Dgs__Set_Render_Engine_To_Eevee_7516E)
    bpy.utils.register_class(SNA_OT_Generate_Hq_Splat_View_Dependant_Eafc2)
    bpy.utils.register_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_72797)
    bpy.utils.register_class(SNA_AddonPreferences_10BAB)
    bpy.utils.register_class(SNA_OT_Dgs_Restore_Default_Blender_Header_Colour_0Da65)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_dgs_ply_directory
    del bpy.types.Material.sna_dgs_show_bsdf_settings
    del bpy.types.Material.sna_dg_show_colour_masks
    del bpy.types.Material.sna_dgs_show_base_colour_adjustments
    del bpy.types.Scene.sna_dgs_camera_refresh_method
    bpy.utils.unregister_class(SNA_OT_Open_Blender_Splat_Render_Documentation_1Eac5)
    bpy.utils.unregister_class(SNA_OT_Open_Blender_Splat_Render_Tutorial_Video_A4Fe6)
    bpy.utils.unregister_class(SNA_OT_Launch_Kiri_Site_D26Bf)
    bpy.utils.unregister_class(SNA_OT_Launch_Blender_Market_77F72)
    bpy.utils.unregister_class(SNA_OT_Dgs__Import_Ply_As_Splats_8458E)
    bpy.utils.unregister_class(SNA_OT_Dgs__Start_Camera_Update_9Eaff)
    bpy.utils.unregister_class(SNA_OT_Dgs__Stop_Camera_Update_9Ad85)
    bpy.utils.unregister_class(SNA_OT_Dgs__Set_Render_Engine_To_Eevee_7516E)
    bpy.utils.unregister_class(SNA_OT_Generate_Hq_Splat_View_Dependant_Eafc2)
    bpy.utils.unregister_class(SNA_PT_DGS_RENDER_BY_KIRI_ENGINE_72797)
    bpy.utils.unregister_class(SNA_AddonPreferences_10BAB)
    bpy.utils.unregister_class(SNA_OT_Dgs_Restore_Default_Blender_Header_Colour_0Da65)
