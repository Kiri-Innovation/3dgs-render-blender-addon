
def sna_clean_up_scene_5F1F1(REMOVE_ALL_GAUSSIAN_OBJECTS):
    REMOVE_ALL_GAUSSIAN_OBJECTS = REMOVE_ALL_GAUSSIAN_OBJECTS
    # ========== VARIABLES (EDIT THESE) ==========
    #REMOVE_ALL_GAUSSIAN_OBJECTS = False  # Remove all gaussian objects from scene
    REMOVE_HANDLERS = True               # Remove draw handlers
    REMOVE_GPU_RESOURCES = True          # Clean up GPU textures/shaders
    CLEAR_OBJECT_CACHE = True            # Clear the global object cache
    # ============================================
    import bpy

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
