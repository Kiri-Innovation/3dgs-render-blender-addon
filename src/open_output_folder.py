import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Open_Output_Folder_82000(bpy.types.Operator):
    bl_idname = "sna.dgs_render_open_output_folder_82000"
    bl_label = "3DGS Render: Open Output Folder"
    bl_description = "Open a file directory"
    bl_options = {"REGISTER", "UNDO"}
    sna_path: bpy.props.StringProperty(name='path', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        folder_path = self.sna_path
        # Open Folder Script for Serpens
        # This script opens a folder from a given path, compatible with all operating systems
        # Input variables
        #folder_path = # String: path to folder to open
        # Default: ""
        # Description: Full path to the folder you want to open
        # Output variables
        #success = # Boolean: whether the folder was opened successfully
        #error_message = # String: error message if any
        # Import necessary modules
        import platform
        # Initialize output variables
        success = False
        error_message = ""
        # Check if the folder path is provided and exists
        if not folder_path:
            error_message = "No folder path provided"
        else:
            # Normalize path for OS consistency
            folder_path = os.path.normpath(folder_path)
            # Check if path exists
            if not os.path.exists(folder_path):
                error_message = f"Path does not exist: {folder_path}"
            elif not os.path.isdir(folder_path):
                error_message = f"Path is not a directory: {folder_path}"
            else:
                # Determine which OS we're on and use the appropriate command to open the folder
                try:
                    system = platform.system()
                    if system == "Windows":
                        # Windows - use explorer
                        subprocess.Popen(["explorer", folder_path])
                        success = True
                    elif system == "Darwin":
                        # macOS - use open command
                        subprocess.Popen(["open", folder_path])
                        success = True
                    elif system == "Linux":
                        # Linux - try xdg-open first (most common)
                        try:
                            subprocess.Popen(["xdg-open", folder_path])
                            success = True
                        except FileNotFoundError:
                            # If xdg-open isn't available, try a few alternatives
                            try:
                                subprocess.Popen(["nautilus", folder_path])
                                success = True
                            except FileNotFoundError:
                                try:
                                    subprocess.Popen(["dolphin", folder_path])
                                    success = True
                                except FileNotFoundError:
                                    try:
                                        subprocess.Popen(["thunar", folder_path])
                                        success = True
                                    except FileNotFoundError:
                                        error_message = "Unable to find a file manager on your Linux system"
                    else:
                        error_message = f"Unsupported operating system: {system}"
                except Exception as e:
                    error_message = f"Error opening folder: {str(e)}"
        # Print status for debugging (can be removed in production)
        if success:
            print(f"Successfully opened folder: {folder_path}")
        else:
            print(f"Failed to open folder: {error_message}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
