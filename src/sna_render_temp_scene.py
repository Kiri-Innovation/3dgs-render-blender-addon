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


def sna_render_temp_scene_913CD(RENDER_ANIMATION, FRAME_STEP):
    RENDER_ANIMATION = RENDER_ANIMATION
    FRAME_STEP = FRAME_STEP
    ACTUAL_RENDER_PATH = None
    # ========== VARIABLES (EDIT THESE) ==========
    # NOTE: Output path is now determined by your Scene Output Settings in Blender Properties panel
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
    import os
    import platform
    import time
    # GLOBAL OUTPUT VARIABLE FOR SERPENS
    ACTUAL_RENDER_PATH = ""

    def get_safe_render_dir():
        """Get the render directory from the active Scene Output settings."""
        scene_path = bpy.context.scene.render.filepath
        system_temp = os.path.join(tempfile.gettempdir(), "gaussian_render")
        if not scene_path: return system_temp
        # Handle Windows paths on Mac/Linux
        system_is_windows = platform.system() == 'Windows'
        path_is_windows_style = len(scene_path) > 1 and scene_path[1] == ':'
        if not system_is_windows and path_is_windows_style:
            if not hasattr(get_safe_render_dir, "_warned"):
                print(f"Mac/Linux detected with Windows path. Auto-switching to safe system path.")
                get_safe_render_dir._warned = True
            return system_temp
        try:
            abs_path = bpy.path.abspath(scene_path)
            final_dir = os.path.dirname(abs_path)
            if not final_dir: return system_temp
            return os.path.normpath(final_dir)
        except Exception:
            return system_temp

    def get_compositor_node_tree(scene):
        """Version-agnostic way to get the compositor node tree."""
        try: scene.use_nodes = True
        except: pass       # Blender 5.x Check
        if hasattr(scene, "compositing_node_group"):
            if not scene.compositing_node_group:
                tree = bpy.data.node_groups.new(name="Compositor", type="CompositorNodeTree")
                scene.compositing_node_group = tree
            return scene.compositing_node_group
        # Blender 4.x Check
        if hasattr(scene, "node_tree") and scene.node_tree:
            return scene.node_tree
        return None

    def setup_render_for_regular_scene():
        """Configure scene for regular mesh rendering"""
        try:
            scene = bpy.context.scene
            # CRITICAL: Enable Z-Pass so the socket appears in Compositor
            if "ViewLayer" in scene.view_layers:
                scene.view_layers["ViewLayer"].use_pass_z = True
            # Store original render settings
            original_settings = {
                'format': scene.render.image_settings.file_format,
                'color_mode': scene.render.image_settings.color_mode,
                'color_depth': scene.render.image_settings.color_depth,
                'width': scene.render.resolution_x,
                'height': scene.render.resolution_y,
                'media_type': getattr(scene.render.image_settings, 'media_type', None)
            }
            # BLENDER 5 FIX: Set Media Type First
            if hasattr(scene.render.image_settings, "media_type"):
                try: scene.render.image_settings.media_type = 'IMAGE'
                except: pass
            scene.render.image_settings.file_format = 'OPEN_EXR'
            scene.render.image_settings.color_mode = 'RGBA'
            scene.render.image_settings.color_depth = '32'
            if RENDER_WIDTH > 0 and RENDER_HEIGHT > 0:
                scene.render.resolution_x = RENDER_WIDTH
                scene.render.resolution_y = RENDER_HEIGHT
            return original_settings
        except Exception as e:
            print(f"Error setting up render: {e}")
            return None

    def restore_render_settings(original_settings):
        """Restore original render settings"""
        try:
            if not original_settings: return
            scene = bpy.context.scene
            if hasattr(scene.render.image_settings, "media_type") and original_settings.get('media_type'):
                 scene.render.image_settings.media_type = original_settings['media_type']
            scene.render.image_settings.file_format = original_settings['format']
            scene.render.image_settings.color_mode = original_settings['color_mode']
            scene.render.image_settings.color_depth = original_settings['color_depth']
            if original_settings['width'] and original_settings['height']:
                scene.render.resolution_x = original_settings['width']
                scene.render.resolution_y = original_settings['height']
        except Exception as e:
            print(f"Error restoring render settings: {e}")

    def get_output_paths(frame_num):
        resolved_path = get_safe_render_dir()
        os.makedirs(resolved_path, exist_ok=True)
        color_path = os.path.join(resolved_path, f"regular_color_{frame_num:04d}.exr")
        depth_path = os.path.join(resolved_path, f"regular_depth_{frame_num:04d}.exr")
        return color_path, depth_path

    def add_file_output_slot(node, name, socket_type="FLOAT"):
        """
        Version-agnostic wrapper to add a slot to the File Output Node.
        """
        target_socket = None
        # Blender 5.0+ Logic
        if hasattr(node, "file_output_items"):
            try:
                node.file_output_items.new(socket_type, name)
                for socket in node.inputs:
                    if socket.name == name:
                        target_socket = socket
                        break
                if not target_socket and len(node.inputs) > 0:
                    target_socket = node.inputs[-1]
            except Exception as e:
                print(f"Failed adding slot (Blender 5): {e}")
        # Blender 4.x Logic
        elif hasattr(node, "file_slots"):
            target_socket = node.file_slots.new(name)
        return target_socket

    def extract_and_save_passes(frame_num):
        try:
            render_result = bpy.data.images.get('Render Result')
            if not render_result: return False
            color_path, depth_path = get_output_paths(frame_num)
            output_dir = get_safe_render_dir()
            # --- SAVE COLOR ---
            if SAVE_COLOR:
                try:
                    color_image = render_result.copy()
                    color_image.name = f"regular_color_{frame_num}"
                    try: color_image.file_format = 'OPEN_EXR'
                    except: pass 
                    color_image.filepath_raw = color_path
                    color_image.save()
                    bpy.data.images.remove(color_image)
                except Exception as e:
                    print(f"Failed to save color: {e}")
            # --- SAVE DEPTH ---
            if SAVE_DEPTH:
                try:
                    scene = bpy.context.scene
                    node_tree = get_compositor_node_tree(scene)
                    if not node_tree: return False
                    node_tree.nodes.clear()
                    render_layers = node_tree.nodes.new('CompositorNodeRLayers')
                    render_layers.location = (0, 0)
                    file_output = node_tree.nodes.new('CompositorNodeOutputFile')
                    file_output.location = (300, 0)
                    # Format Config
                    if hasattr(file_output.format, "media_type"):
                        file_output.format.media_type = 'IMAGE'
                    try: file_output.format.file_format = 'OPEN_EXR'
                    except: file_output.format.file_format = 'OPEN_EXR_MULTILAYER'
                    file_output.format.color_mode = 'BW'
                    file_output.format.color_depth = '32'
                    # Use a specific temp name for the slot
                    # We save as 'depth_temp_' and then rename to 'regular_depth_XXXX'
                    temp_slot_name = "depth_temp_"
                    # --- SET PATHS (Hybrid) ---
                    if hasattr(file_output, "directory"):
                        file_output.directory = output_dir  # Blender 5
                        # CRITICAL FIX: Clear default file name so it doesn't prepend
                        if hasattr(file_output, "file_name"):
                            file_output.file_name = "" 
                    elif hasattr(file_output, "base_path"):
                        file_output.base_path = output_dir  # Blender 4
                    # --- ADD SLOT ---
                    target_input = add_file_output_slot(file_output, temp_slot_name, "FLOAT")
                    # --- LINK ---
                    source_output = None
                    possible_names = ["Depth", "Z"]
                    for name in possible_names:
                        if name in render_layers.outputs:
                            source_output = render_layers.outputs[name]
                            break
                    if not source_output and len(render_layers.outputs) > 2:
                        source_output = render_layers.outputs[2]
                    if target_input and source_output:
                        node_tree.links.new(source_output, target_input)
                        # RENDER DEPTH
                        bpy.ops.render.render()
                        # === RENAME LOGIC (The Safety Catch) ===
                        # Blender might save it as "depth_temp_.exr", "depth_temp_0001.exr", etc.
                        # We look for ANY file that matches our temp prefix.
                        renamed = False
                        # 1. Exact Name Check (Common in Still Renders)
                        exact_temp = os.path.join(output_dir, f"{temp_slot_name}.exr")
                        if os.path.exists(exact_temp):
                            if os.path.exists(depth_path): os.remove(depth_path)
                            os.rename(exact_temp, depth_path)
                            renamed = True
                        # 2. Wildcard Check (If Blender added frame numbers anyway)
                        if not renamed:
                            for f in os.listdir(output_dir):
                                if f.startswith(temp_slot_name) and f.endswith(".exr"):
                                    old_file = os.path.join(output_dir, f)
                                    if os.path.exists(depth_path): os.remove(depth_path)
                                    os.rename(old_file, depth_path)
                                    renamed = True
                                    break # Stop after finding the first match
                        if not renamed:
                            print(f"Depth file generation failed. looked for {temp_slot_name}...")
                    else:
                        print("Could not link depth sockets")
                except Exception as e:
                    print(f"Failed to save depth: {e}")
                    import traceback
                    traceback.print_exc()
            return True 
        except Exception as e:
            print(f"Error extracting passes: {e}")
            return False

    def render_regular_frame(frame_num):
        try:
            scene = bpy.context.scene
            if not scene.camera: return False
            scene.frame_set(frame_num)
            hidden_gaussians = []
            for obj in bpy.data.objects:
                if obj.get("is_gaussian_splat", False) and obj.visible_get():
                    obj.hide_render = True
                    hidden_gaussians.append(obj.name)
            try:
                bpy.ops.render.render()
                success = extract_and_save_passes(frame_num)
                return success
            finally:
                for obj_name in hidden_gaussians:
                    if obj_name in bpy.data.objects:
                        bpy.data.objects[obj_name].hide_render = False
        except Exception as e:
            print(f"Render failed: {e}")
            return False

    def main_regular_render():
        try:
            scene = bpy.context.scene
            if not scene.camera: return False, None
            current_safe_path = get_safe_render_dir()
            scene["3DGS_TEMP_PATH"] = current_safe_path
            original_settings = setup_render_for_regular_scene()
            if not original_settings: return False, current_safe_path
            # Cleanup
            if CLEANUP_EXISTING_FILES:
                try:
                    for f in os.listdir(current_safe_path):
                        if f.startswith("regular_") and f.endswith(".exr"):
                            os.remove(os.path.join(current_safe_path, f))
                except: pass
            success = False
            try:
                if RENDER_ANIMATION:
                    start = START_FRAME if START_FRAME > 0 else scene.frame_start
                    end = END_FRAME if END_FRAME > 0 else scene.frame_end
                    frames = list(range(start, end + 1))
                    all_good = True
                    for f in frames:
                        print(f"Processing Frame {f}...")
                        if not render_regular_frame(f):
                            all_good = False
                    success = all_good
                else:
                    print(f"Processing Single Frame {scene.frame_current}...")
                    success = render_regular_frame(scene.frame_current)
            finally:
                restore_render_settings(original_settings)
            return success, current_safe_path
        except Exception:
            return False, None
    # ========== MAIN EXECUTION ==========
    print("Starting regular scene render...")
    render_success, ACTUAL_RENDER_PATH = main_regular_render()
    if render_success:
        print("Regular scene render completed!")
        print(f"Files saved to: {ACTUAL_RENDER_PATH}")
    else:
        print("Regular scene render failed!")
    return ACTUAL_RENDER_PATH
