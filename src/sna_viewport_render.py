from .important import *
import bpy
import gpu

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
