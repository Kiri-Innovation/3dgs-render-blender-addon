import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_render_temp_scene_913CD(RENDER_ANIMATION, FRAME_STEP):
    RENDER_ANIMATION = RENDER_ANIMATION
    FRAME_STEP = FRAME_STEP
    ACTUAL_RENDER_PATH = None
    # ========== VARIABLES (EDIT THESE) ==========
    # NOTE: Temp output path is derived from your Scene Output settings and stored inside a _3dgs_temp subfolder
    RENDER_WIDTH = 0           # 0 = use scene settings
    RENDER_HEIGHT = 0          # 0 = use scene settings
    #RENDER_ANIMATION = False  # True = render animation frames
    START_FRAME = 0            # 0 = use scene frame_start
    END_FRAME = 0              # 0 = use scene frame_end
    #FRAME_STEP = 1            # Optional Serpens input if you expose stepped temp rendering later
    CLEANUP_EXISTING_FILES = True  # Remove old temp files before rendering
    SAVE_COLOR = True          # Save color pass
    SAVE_DEPTH = True          # Save Z-pass (needed for gaussian integration)
    # ============================================
    #import os
    import tempfile
    # GLOBAL OUTPUT VARIABLE FOR SERPENS
    ACTUAL_RENDER_PATH = ""
    TEMP_SUBFOLDER_NAME = "_3dgs_temp"
    TEMP_COLOR_SLOT_PREFIX = "color_temp_"
    TEMP_DEPTH_SLOT_PREFIX = "depth_temp_"

    def is_supported_absolute_dir(path):
        """Return True when a path is absolute for the current OS, not just root-relative."""
        if not path:
            return False
        if platform.system() == "Windows":
            drive, _ = os.path.splitdrive(path)
            return bool(drive) or path.startswith("\\\\")
        return os.path.isabs(path)

    def get_safe_render_dir(scene=None):
        """Get the base render directory from the active Scene Output settings."""
        scene = scene or bpy.context.scene
        scene_path = scene.render.filepath
        system_temp = os.path.join(tempfile.gettempdir(), "gaussian_render")
        if not scene_path:
            return system_temp
        system_is_windows = platform.system() == "Windows"
        path_is_windows_style = len(scene_path) > 1 and scene_path[1] == ":"
        path_is_unsaved_relative = not bpy.data.filepath and scene_path.startswith("//")
        if not system_is_windows and path_is_windows_style:
            if not hasattr(get_safe_render_dir, "_warned"):
                print("Mac/Linux detected with a Windows render path. Using a safe temp folder instead.")
                get_safe_render_dir._warned = True
            return system_temp
        if path_is_unsaved_relative:
            return system_temp
        try:
            abs_path = bpy.path.abspath(scene_path)
            final_dir = os.path.dirname(abs_path)
            if not is_supported_absolute_dir(final_dir):
                return system_temp
            return os.path.normpath(final_dir)
        except Exception:
            return system_temp

    def get_temp_render_dir(scene=None):
        """Store temp regular-scene renders under the main render directory."""
        return os.path.join(get_safe_render_dir(scene), TEMP_SUBFOLDER_NAME)

    def get_output_paths(frame_num, scene=None):
        temp_dir = get_temp_render_dir(scene)
        os.makedirs(temp_dir, exist_ok=True)
        color_path = os.path.join(temp_dir, f"regular_color_{frame_num:04d}.exr")
        depth_path = os.path.join(temp_dir, f"regular_depth_{frame_num:04d}.exr")
        return color_path, depth_path

    def get_compositor_node_tree(scene):
        """Version-agnostic way to get the compositor node tree."""
        try:
            scene.use_nodes = True
        except Exception:
            pass
        if hasattr(scene, "compositing_node_group"):
            if not scene.compositing_node_group:
                tree = bpy.data.node_groups.new(name="Compositor", type="CompositorNodeTree")
                scene.compositing_node_group = tree
            return scene.compositing_node_group
        if hasattr(scene, "node_tree") and scene.node_tree:
            return scene.node_tree
        return None

    def add_file_output_slot(node, name, socket_type="FLOAT"):
        """Version-agnostic wrapper to add a slot to the File Output node."""
        target_socket = None
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
        elif hasattr(node, "file_slots"):
            target_socket = node.file_slots.new(name)
        return target_socket

    def make_unique_scene_name(base_name):
        """Create a unique scene name for the temporary render copy."""
        if base_name not in bpy.data.scenes:
            return base_name
        counter = 1
        while f"{base_name}_{counter:03d}" in bpy.data.scenes:
            counter += 1
        return f"{base_name}_{counter:03d}"

    def make_unique_tree_name(base_name):
        """Create a unique compositor node-tree name for temporary helper scenes."""
        if base_name not in bpy.data.node_groups:
            return base_name
        counter = 1
        while f"{base_name}_{counter:03d}" in bpy.data.node_groups:
            counter += 1
        return f"{base_name}_{counter:03d}"

    def localize_temp_scene_compositor(source_scene, temp_scene):
        """Detach shared compositor data so edits stay inside the temporary scene only."""
        if hasattr(temp_scene, "compositing_node_group") and temp_scene.compositing_node_group:
            if (
                hasattr(source_scene, "compositing_node_group")
                and source_scene.compositing_node_group
                and temp_scene.compositing_node_group == source_scene.compositing_node_group
            ):
                temp_scene.compositing_node_group = temp_scene.compositing_node_group.copy()
            return
        if hasattr(temp_scene, "node_tree") and temp_scene.node_tree:
            try:
                if hasattr(source_scene, "node_tree") and source_scene.node_tree and temp_scene.node_tree == source_scene.node_tree:
                    temp_scene.node_tree = temp_scene.node_tree.copy()
            except Exception:
                pass

    def capture_source_scene_state(scene):
        """Remember user-owned scene state that the temporary render must not disturb."""
        state = {
            "frame_current": scene.frame_current,
            "use_nodes": getattr(scene, "use_nodes", None),
            "render_use_compositing": getattr(scene.render, "use_compositing", None),
            "render_use_sequencer": getattr(scene.render, "use_sequencer", None),
        }
        if hasattr(scene, "compositing_node_group"):
            state["compositing_node_group"] = scene.compositing_node_group
        return state

    def restore_source_scene_state(scene, state):
        """Restore the user's compositor/render state after temporary rendering."""
        if not scene or not state:
            return
        try:
            scene.frame_set(state["frame_current"])
        except Exception:
            pass
        if state.get("use_nodes") is not None:
            try:
                scene.use_nodes = state["use_nodes"]
            except Exception:
                pass
        if state.get("render_use_compositing") is not None and hasattr(scene.render, "use_compositing"):
            try:
                scene.render.use_compositing = state["render_use_compositing"]
            except Exception:
                pass
        if state.get("render_use_sequencer") is not None and hasattr(scene.render, "use_sequencer"):
            try:
                scene.render.use_sequencer = state["render_use_sequencer"]
            except Exception:
                pass
        if "compositing_node_group" in state and hasattr(scene, "compositing_node_group"):
            try:
                scene.compositing_node_group = state["compositing_node_group"]
            except Exception:
                pass

    def create_linked_temp_scene(source_scene):
        """Create a linked scene copy. The temp compositor tree is created later from scratch."""
        window = bpy.context.window
        if not window:
            raise RuntimeError("No Blender window context available to create a temporary render scene")
        previous_scene = window.scene
        window.scene = source_scene
        bpy.ops.scene.new(type='LINK_COPY')
        temp_scene = window.scene
        temp_scene.name = make_unique_scene_name("3DGS_TEMP_RENDER")
        window.scene = previous_scene
        return temp_scene

    def remove_temp_scene(temp_scene, fallback_scene):
        """Delete the temporary scene once rendering is complete."""
        temp_tree = None
        if temp_scene:
            try:
                if hasattr(temp_scene, "compositing_node_group"):
                    temp_tree = temp_scene.compositing_node_group
                elif hasattr(temp_scene, "node_tree"):
                    temp_tree = temp_scene.node_tree
            except Exception:
                temp_tree = None
        window = bpy.context.window
        if window and window.scene == temp_scene:
            window.scene = fallback_scene
        if temp_scene and temp_scene.name in bpy.data.scenes:
            bpy.data.scenes.remove(temp_scene)
        if temp_tree and temp_tree.users == 0:
            try:
                bpy.data.node_groups.remove(temp_tree)
            except Exception:
                pass

    def setup_render_for_regular_scene(scene):
        """Configure the temporary scene for regular mesh rendering."""
        for view_layer in scene.view_layers:
            try:
                view_layer.use_pass_z = True
            except Exception:
                pass
        if hasattr(scene.render.image_settings, "media_type"):
            try:
                scene.render.image_settings.media_type = "IMAGE"
            except Exception:
                pass
        scene.render.image_settings.file_format = "OPEN_EXR"
        scene.render.image_settings.color_mode = "RGBA"
        scene.render.image_settings.color_depth = "32"
        if RENDER_WIDTH > 0 and RENDER_HEIGHT > 0:
            scene.render.resolution_x = RENDER_WIDTH
            scene.render.resolution_y = RENDER_HEIGHT
        if hasattr(scene.render, "use_compositing"):
            scene.render.use_compositing = True
        if hasattr(scene.render, "use_sequencer"):
            scene.render.use_sequencer = False

    def setup_temp_depth_compositor(scene):
        """Build a compositor in the temp scene that only outputs the Z pass to files."""
        if not SAVE_DEPTH:
            return True
        for view_layer in scene.view_layers:
            try:
                view_layer.use_pass_z = True
            except Exception:
                pass
        if hasattr(scene, "compositing_node_group"):
            node_tree = bpy.data.node_groups.new(
                name=make_unique_tree_name("3DGS_TEMP_DEPTH"),
                type="CompositorNodeTree",
            )
            scene.compositing_node_group = node_tree
        else:
            node_tree = get_compositor_node_tree(scene)
        if not node_tree:
            return False
        node_tree.nodes.clear()
        node_tree.links.clear()
        render_layers = node_tree.nodes.new("CompositorNodeRLayers")
        render_layers.location = (0, 0)
        try:
            render_layers.scene = scene
        except Exception:
            pass
        try:
            if scene.view_layers:
                render_layers.layer = scene.view_layers[0].name
        except Exception:
            pass
        image_output = render_layers.outputs.get("Image") if hasattr(render_layers.outputs, "get") else None
        if image_output is None and render_layers.outputs:
            image_output = render_layers.outputs[0]
        temp_dir = get_temp_render_dir(scene)
        os.makedirs(temp_dir, exist_ok=True)
        if SAVE_COLOR:
            color_output = node_tree.nodes.new("CompositorNodeOutputFile")
            color_output.location = (300, 120)
            if hasattr(color_output.format, "media_type"):
                try:
                    color_output.format.media_type = "IMAGE"
                except Exception:
                    pass
            try:
                color_output.format.file_format = "OPEN_EXR"
            except Exception:
                color_output.format.file_format = "OPEN_EXR_MULTILAYER"
            color_output.format.color_mode = "RGBA"
            color_output.format.color_depth = "32"
            if hasattr(color_output, "directory"):
                color_output.directory = temp_dir
                if hasattr(color_output, "file_name"):
                    color_output.file_name = ""
            elif hasattr(color_output, "base_path"):
                color_output.base_path = temp_dir
            color_input = add_file_output_slot(color_output, TEMP_COLOR_SLOT_PREFIX, "RGBA")
            if image_output and color_input:
                node_tree.links.new(image_output, color_input)
                scene["3DGS_TEMP_COLOR_OUTPUT_AVAILABLE"] = True
            else:
                scene["3DGS_TEMP_COLOR_OUTPUT_AVAILABLE"] = False
        else:
            scene["3DGS_TEMP_COLOR_OUTPUT_AVAILABLE"] = False
        file_output = node_tree.nodes.new("CompositorNodeOutputFile")
        file_output.location = (300, -120)
        if hasattr(file_output.format, "media_type"):
            try:
                file_output.format.media_type = "IMAGE"
            except Exception:
                pass
        try:
            file_output.format.file_format = "OPEN_EXR"
        except Exception:
            file_output.format.file_format = "OPEN_EXR_MULTILAYER"
        file_output.format.color_mode = "BW"
        file_output.format.color_depth = "32"
        if hasattr(file_output, "directory"):
            file_output.directory = temp_dir
            if hasattr(file_output, "file_name"):
                file_output.file_name = ""
        elif hasattr(file_output, "base_path"):
            file_output.base_path = temp_dir
        target_input = add_file_output_slot(file_output, TEMP_DEPTH_SLOT_PREFIX, "FLOAT")
        source_output = None
        for name in ("Depth", "Z"):
            if name in render_layers.outputs:
                source_output = render_layers.outputs[name]
                break
        if not source_output and len(render_layers.outputs) > 2:
            source_output = render_layers.outputs[2]
        if not target_input or not source_output:
            available_outputs = ", ".join(socket.name or "<unnamed>" for socket in render_layers.outputs)
            print(f"Could not link depth sockets in the temporary compositor. Available outputs: {available_outputs}")
            scene["3DGS_TEMP_DEPTH_OUTPUT_AVAILABLE"] = False
            return True
        node_tree.links.new(source_output, target_input)
        scene["3DGS_TEMP_DEPTH_OUTPUT_AVAILABLE"] = True
        return True

    def cleanup_existing_temp_files(scene=None):
        """Remove stale temp outputs before starting a new run."""
        temp_dir = get_temp_render_dir(scene)
        os.makedirs(temp_dir, exist_ok=True)
        try:
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Temp cleanup warning: {e}")

    def rename_latest_temp_output(prefix, target_path, label, scene=None):
        """Rename Blender's newest file-output result to the stable temp filename."""
        temp_dir = get_temp_render_dir(scene)
        candidates = []
        try:
            for file_name in os.listdir(temp_dir):
                if file_name.startswith(prefix) and file_name.endswith(".exr"):
                    candidates.append(os.path.join(temp_dir, file_name))
        except Exception:
            candidates = []
        if not candidates:
            print(f"{label} file generation failed. Looked for files starting with {prefix}")
            return False
        latest_output = max(candidates, key=os.path.getmtime)
        os.replace(latest_output, target_path)
        return True

    def extract_and_save_passes(frame_num, scene=None):
        """Rename temporary compositor file outputs to stable color/depth paths."""
        color_path, depth_path = get_output_paths(frame_num, scene)
        success = True
        color_output_available = True
        if scene is not None:
            color_output_available = bool(scene.get("3DGS_TEMP_COLOR_OUTPUT_AVAILABLE", True))
        if SAVE_COLOR and color_output_available and not rename_latest_temp_output(
            TEMP_COLOR_SLOT_PREFIX,
            color_path,
            "Color",
            scene,
        ):
            success = False
        depth_output_available = True
        if scene is not None:
            depth_output_available = bool(scene.get("3DGS_TEMP_DEPTH_OUTPUT_AVAILABLE", True))
        if SAVE_DEPTH and depth_output_available and not rename_latest_temp_output(
            TEMP_DEPTH_SLOT_PREFIX,
            depth_path,
            "Depth",
            scene,
        ):
            success = False
        return success

    def render_regular_frame(frame_num, source_scene, temp_scene):
        """Render one frame from the temp scene while hiding gaussian objects."""
        if not temp_scene.camera:
            temp_scene.camera = source_scene.camera
        source_scene.frame_set(frame_num)
        temp_scene.frame_set(frame_num)
        hidden_gaussians = []
        for obj in bpy.data.objects:
            if obj.get("is_gaussian_splat", False) and obj.visible_get():
                hidden_gaussians.append((obj, obj.hide_render))
                obj.hide_render = True
        try:
            bpy.ops.render.render(scene=temp_scene.name, write_still=False, use_viewport=False)
            return extract_and_save_passes(frame_num, temp_scene)
        finally:
            for obj, was_hide_render in hidden_gaussians:
                if obj and obj.name in bpy.data.objects:
                    obj.hide_render = was_hide_render

    def main_regular_render():
        source_scene = bpy.context.scene
        if not source_scene.camera:
            return False, None
        temp_render_dir = get_temp_render_dir(source_scene)
        os.makedirs(temp_render_dir, exist_ok=True)
        source_scene["3DGS_TEMP_PATH"] = temp_render_dir
        user_frame = source_scene.frame_current
        source_state = capture_source_scene_state(source_scene)
        temp_scene = None
        try:
            temp_scene = create_linked_temp_scene(source_scene)
            localize_temp_scene_compositor(source_scene, temp_scene)
            temp_scene.camera = source_scene.camera
            temp_scene.render.filepath = source_scene.render.filepath
            setup_render_for_regular_scene(temp_scene)
            if not setup_temp_depth_compositor(temp_scene):
                return False, temp_render_dir
            if CLEANUP_EXISTING_FILES:
                cleanup_existing_temp_files(source_scene)
            success = False
            if RENDER_ANIMATION:
                start = START_FRAME if START_FRAME > 0 else source_scene.frame_start
                end = END_FRAME if END_FRAME > 0 else source_scene.frame_end
                frames = list(range(start, end + 1))
                all_good = True
                for frame_num in frames:
                    print(f"Processing Frame {frame_num}...")
                    if not render_regular_frame(frame_num, source_scene, temp_scene):
                        all_good = False
                success = all_good
            else:
                print(f"Processing Single Frame {source_scene.frame_current}...")
                success = render_regular_frame(source_scene.frame_current, source_scene, temp_scene)
            return success, temp_render_dir
        except Exception as e:
            print(f"Temp regular render failed: {e}")
            return False, temp_render_dir
        finally:
            restore_source_scene_state(source_scene, source_state)
            source_scene.frame_set(user_frame)
            if temp_scene:
                remove_temp_scene(temp_scene, source_scene)
    # ========== MAIN EXECUTION ==========
    print("Starting regular scene temp render with preserved user compositor...")
    render_success, ACTUAL_RENDER_PATH = main_regular_render()
    if render_success:
        print("Regular scene temp render completed!")
        print(f"Temp files saved to: {ACTUAL_RENDER_PATH}")
    else:
        print("Regular scene temp render failed!")
    return ACTUAL_RENDER_PATH
