import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_b2_load_from_blender_object_F0CCB(OBJECT_BASE_NAME):
    OBJECT_BASE_NAME = OBJECT_BASE_NAME
    # ========== VARIABLES (EDIT THESE) ==========
    SOURCE_MESH_OBJECT = None  # Set this to target mesh object, or leave None to use active object
    #OBJECT_BASE_NAME = "GaussianSplat"  # Will auto-number: _001, _002, etc.
    # ============================================
    import numpy as np
    from math import pi

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

    def get_face_quad_vertex_groups(mesh_data):
        """Return one 4-vertex group per quad face for face-based gaussian sources."""
        num_polygons = len(mesh_data.polygons)
        if num_polygons == 0:
            return None
        face_vertex_indices = np.empty((num_polygons, 4), dtype=np.int32)
        for poly_index, poly in enumerate(mesh_data.polygons):
            poly_vertices = tuple(poly.vertices)
            if len(poly_vertices) != 4:
                return None
            face_vertex_indices[poly_index] = poly_vertices
        return face_vertex_indices

    def collapse_attribute_values(data_array, face_vertex_indices, expected_vertex_count, attr_name):
        """Collapse per-vertex attribute data down to one value per disconnected quad."""
        if face_vertex_indices is None:
            return data_array.astype(np.float32)
        if len(data_array) == expected_vertex_count:
            return data_array[face_vertex_indices].mean(axis=1).astype(np.float32)
        if len(data_array) == len(face_vertex_indices):
            return data_array.astype(np.float32)
        raise ValueError(
            f"Attribute '{attr_name}' has {len(data_array)} values, expected {expected_vertex_count} vertices "
            f"or {len(face_vertex_indices)} face islands"
        )

    def extract_attribute_data(mesh_data, attr_name, face_vertex_indices=None, expected_vertex_count=None):
        """Extract data from mesh attribute by name, with optional face-quad collapse."""
        if attr_name not in [attr.name for attr in mesh_data.attributes]:
            return None
        attr = mesh_data.attributes[attr_name]
        # Use foreach_get for much faster extraction
        data_array = np.zeros(len(attr.data), dtype=np.float32)
        attr.data.foreach_get("value", data_array)
        if expected_vertex_count is None:
            expected_vertex_count = len(mesh_data.vertices)
        return collapse_attribute_values(data_array, face_vertex_indices, expected_vertex_count, attr_name)

    def extract_gaussian_data_from_mesh_data(mesh_data, mesh_name):
        """Extract gaussian data and collapse disconnected face quads to one virtual point each."""
        num_vertices = len(mesh_data.vertices)
        if num_vertices == 0:
            raise ValueError("Mesh has no vertices")
        face_vertex_indices = get_face_quad_vertex_groups(mesh_data)
        if face_vertex_indices is not None:
            print(
                f"Detected face-based gaussian mesh '{mesh_name}', collapsing "
                f"{num_vertices:,} quad vertices to {len(face_vertex_indices):,} splats"
            )
        positions = np.zeros(num_vertices * 3, dtype=np.float32)
        mesh_data.vertices.foreach_get("co", positions)
        positions = positions.reshape(-1, 3)
        if face_vertex_indices is not None:
            positions = positions[face_vertex_indices].mean(axis=1).astype(np.float32)
        num_points = len(positions)
        available_attrs = [attr.name for attr in mesh_data.attributes]
        if all(attr in available_attrs for attr in ['f_dc_0', 'f_dc_1', 'f_dc_2']):
            dc_0 = extract_attribute_data(mesh_data, 'f_dc_0', face_vertex_indices, num_vertices)
            dc_1 = extract_attribute_data(mesh_data, 'f_dc_1', face_vertex_indices, num_vertices)
            dc_2 = extract_attribute_data(mesh_data, 'f_dc_2', face_vertex_indices, num_vertices)
            features_dc = np.column_stack([dc_0, dc_1, dc_2]).astype(np.float32)
            f_rest_fields = [attr for attr in available_attrs if attr.startswith('f_rest_')]
            f_rest_fields = sorted(f_rest_fields, key=lambda x: int(x.split('_')[-1]))
            if f_rest_fields:
                features_extra_list = []
                for field in f_rest_fields:
                    data = extract_attribute_data(mesh_data, field, face_vertex_indices, num_vertices)
                    if data is not None:
                        features_extra_list.append(data)
                if features_extra_list:
                    features_extra = np.column_stack(features_extra_list).astype(np.float32)
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
                        features_extra_reshaped = features_extra_used.reshape((num_points, 3, coeffs_per_degree))
                        features_extra_reshaped = np.transpose(features_extra_reshaped, [0, 2, 1])
                        features_dc_reshaped = features_dc.reshape(-1, 1, 3)
                        all_features = np.concatenate([features_dc_reshaped, features_extra_reshaped], axis=1)
                        sh_coeffs = all_features.reshape(num_points, -1).astype(np.float32)
                    else:
                        sh_coeffs = features_dc
                else:
                    sh_coeffs = features_dc
            else:
                sh_coeffs = features_dc
        else:
            print(f"Warning: f_dc attributes not found on evaluated mesh, using defaults")
            sh_coeffs = np.ones((num_points, 3), dtype=np.float32) * 0.28209479177387814
        if all(attr in available_attrs for attr in ['scale_0', 'scale_1', 'scale_2']):
            scale_0 = extract_attribute_data(mesh_data, 'scale_0', face_vertex_indices, num_vertices)
            scale_1 = extract_attribute_data(mesh_data, 'scale_1', face_vertex_indices, num_vertices)
            scale_2 = extract_attribute_data(mesh_data, 'scale_2', face_vertex_indices, num_vertices)
            scales = np.column_stack([scale_0, scale_1, scale_2]).astype(np.float32)
            scales = np.exp(scales)
        else:
            print(f"Warning: scale attributes not found on evaluated mesh, using defaults")
            scales = np.ones((num_points, 3), dtype=np.float32) * 0.01
        if all(attr in available_attrs for attr in ['rot_0', 'rot_1', 'rot_2', 'rot_3']):
            rot_0 = extract_attribute_data(mesh_data, 'rot_0', face_vertex_indices, num_vertices)
            rot_1 = extract_attribute_data(mesh_data, 'rot_1', face_vertex_indices, num_vertices)
            rot_2 = extract_attribute_data(mesh_data, 'rot_2', face_vertex_indices, num_vertices)
            rot_3 = extract_attribute_data(mesh_data, 'rot_3', face_vertex_indices, num_vertices)
            rotations = np.column_stack([rot_0, rot_1, rot_2, rot_3]).astype(np.float32)
            norms = np.linalg.norm(rotations, axis=1, keepdims=True)
            norms[norms == 0.0] = 1.0
            rotations = rotations / norms
        else:
            print(f"Warning: rotation attributes not found on evaluated mesh, using defaults")
            rotations = np.zeros((num_points, 4), dtype=np.float32)
            rotations[:, 0] = 1.0
        if 'opacity' in available_attrs:
            opacity_raw = extract_attribute_data(mesh_data, 'opacity', face_vertex_indices, num_vertices)
            opacity = 1.0 / (1.0 + np.exp(-opacity_raw))
        else:
            print(f"Warning: opacity attribute not found on evaluated mesh, using defaults")
            opacity = np.ones(num_points, dtype=np.float32)
        return {
            'num_points': num_points,
            'positions': positions.astype(np.float32),
            'scales': scales.astype(np.float32),
            'rotations': rotations.astype(np.float32),
            'opacities': opacity.astype(np.float32),
            'sh_coeffs': sh_coeffs.astype(np.float32),
            'sh_dim': sh_coeffs.shape[1],
            'used_face_quad_collapse': face_vertex_indices is not None,
        }

    def extract_gaussian_data_from_evaluated_mesh(mesh_obj):
        """Extract and process gaussian data from EVALUATED mesh object attributes"""
        # Get evaluated mesh data
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated_object = mesh_obj.evaluated_get(depsgraph)
        evaluated_mesh = evaluated_object.data
        return extract_gaussian_data_from_mesh_data(evaluated_mesh, mesh_obj.name)
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
        empty_object["kiri_gaussian_proxy_uuid"] = str(uuid.uuid4())
        empty_object["kiri_gaussian_instance"] = False
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
