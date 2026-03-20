import bpy
from .important import *
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
