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

def sna_render_comp_0DAEE(RENDER_ANIMATION, RENDER_COLOR, RENDER_DEPTH, COMP_WITH_TEMP, UPDATE_SOURCE_TRANSFORMS, REFRESH_EVALUATED_DATA, FRAME_STEP, TEMP_RENDER_PATH):
    RENDER_ANIMATION = RENDER_ANIMATION
    RENDER_GAUSSIAN = RENDER_COLOR
    RENDER_DEPTH = RENDER_DEPTH
    USE_TEMP_RENDERS = COMP_WITH_TEMP
    UPDATE_SOURCE_TRANSFORMS = UPDATE_SOURCE_TRANSFORMS
    REFRESH_EVALUATED_DATA = REFRESH_EVALUATED_DATA
    FRAME_STEP = FRAME_STEP
    TEMP_RENDER_PATH = TEMP_RENDER_PATH
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
    # COMPOSITING SETTINGS
    #USE_TEMP_RENDERS = True        # Use temp renders from script_7 for compositing
    #TEMP_RENDER_PATH = r"C:\temp\gaussian_render"  # RESTORED: Serpens can inject the correct path here
    USE_EXTERNAL_DEPTH = True      # Use depth from script_7 for occlusion
    USE_EXTERNAL_COLOR = True      # Use color from script_7 for compositing
    COMPOSITE_OVER_REGULAR = True # Composite gaussians over regular scene
    # Animation-specific settings
    START_FRAME = 0               # Animation start frame (0 = use scene frame_start)
    END_FRAME = 0                 # Animation end frame (0 = use scene frame_end)
    #FRAME_STEP = 1                # Render every Nth frame (1 = every frame)
    SKIP_EXISTING_FILES = False   # Skip frames if output file already exists
    CONTINUE_ON_ERROR = True      # Continue animation if individual frames fail
    #FRAME_STEP = 1
    # Source object update settings
    #UPDATE_SOURCE_TRANSFORMS = True   # Copy source object transforms to empty objects each frame
    #REFRESH_EVALUATED_DATA = True # Re-extract gaussian data from evaluated source mesh each frame (EXPENSIVE!)
    # DEBUG SETTINGS
    DEBUG_VERBOSE = False          # Enable detailed debug output
    DEBUG_DATA_CHANGES = False     # Log actual data changes between frames
    DEBUG_TIMING = False          # Log operation timing
    # ============================================
    import gpu
    import gpu.types
    import mathutils
    import datetime
    import time
    import platform

    def debug_print(message, force=False):
        """Print debug message if debugging is enabled"""
        if DEBUG_VERBOSE or force:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[DEBUG {timestamp}] {message}")

    def resolve_blender_path(blender_path):
        """
        Convert path to absolute.
        Safety Feature: If Mac/Linux sees a Windows path (C:\...), 
        it automatically switches to the system Temp folder to prevent errors.
        """
        import os
        # 1. Fallback Logic for Mac/Linux Users
        system_is_windows = platform.system() == 'Windows'
        # Check if this looks like a Windows path (e.g. starts with C:)
        path_is_windows_style = len(blender_path) > 1 and blender_path[1] == ':'
        # If we are NOT on Windows, but the path is for Windows, use System Temp
        if not system_is_windows and path_is_windows_style:
            safe_temp = os.path.join(tempfile.gettempdir(), "gaussian_render")
            # Print warning only once
            if not hasattr(resolve_blender_path, "_warned"):
                print(f"Mac/Linux detected with Windows path ('{blender_path}').")
                print(f"Auto-switching to safe system path: {safe_temp}")
                resolve_blender_path._warned = True
            return safe_temp
        # 2. Standard Path Resolution
        path = os.path.normpath(blender_path)
        try:
            resolved = bpy.path.abspath(path)
            if os.path.isabs(resolved):
                 return os.path.normpath(resolved)
        except Exception:
            pass
        return os.path.abspath(path)

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
        """Load depth texture from Script 7a output (Uses variable with safety check)"""
        try:
            if not USE_EXTERNAL_DEPTH:
                return None
            # Resolve path safely (handles Mac/Linux fix)
            render_dir = resolve_blender_path(TEMP_RENDER_PATH)
            depth_path = os.path.join(render_dir, f"regular_depth_{frame_num:04d}.exr")
            debug_print(f"Attempting to load external depth: {depth_path}")
            # Try to load directly
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
        """Load color image from Script 7a output for compositing (Uses variable with safety check)"""
        try:
            if not USE_EXTERNAL_COLOR:
                return None, None
            # Resolve path safely (handles Mac/Linux fix)
            render_dir = resolve_blender_path(TEMP_RENDER_PATH)
            color_path = os.path.join(render_dir, f"regular_color_{frame_num:04d}.exr")
            debug_print(f"Attempting to load external color: {color_path}")
            # Try to load directly
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
