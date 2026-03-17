def sna_b2_load_from_blender_object_F0CCB(OBJECT_BASE_NAME):
    OBJECT_BASE_NAME = OBJECT_BASE_NAME
    # ========== VARIABLES (EDIT THESE) ==========
    SOURCE_MESH_OBJECT = None  # Set this to target mesh object, or leave None to use active object
    #OBJECT_BASE_NAME = "GaussianSplat"  # Will auto-number: _001, _002, etc.
    # ============================================
    import numpy as np
    from math import pi
    import bpy
    import time

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
