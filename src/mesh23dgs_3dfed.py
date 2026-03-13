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

class SNA_OT_Dgs_Render_Mesh23Dgs_3Dfed(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.dgs_render_mesh23dgs_3dfed"
    bl_label = "3DGS Render: Mesh-2-3DGS"
    bl_description = "Convert a chosen .OBJ to 3DGS .PLY"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.obj', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_dgs_scene_properties.mesh2gs_validate:
            obj_path = bpy.path.abspath(self.filepath)
            face_count = None
            triangular_face_count = None
            non_triangular_face_count = None
            is_triangulated = None
            error_message = None
            #import bpy  # For text editor
            # Set the path to your .obj file here
            #obj_path = "/path/to/your/file.obj"  # CHANGE THIS TO YOUR FILE PATH
            # Initialize variables
            face_count = 0
            triangular_face_count = 0
            non_triangular_face_count = 0
            is_triangulated = True
            error_message = None
            # Check if file exists
            if not os.path.exists(obj_path):
                is_triangulated = False
                error_message = "File not found"
                triangular_face_count = 0
                non_triangular_face_count = 0
            else:
                # Try to read the file
                try:
                    with open(obj_path, 'r') as file:
                        for line in file:
                            line = line.strip()
                            if line.startswith('f '):
                                face_count += 1
                                # Split the face line and count vertices
                                vertices = [v.split('/')[0] for v in line[2:].split()]
                                if len(vertices) == 3:
                                    triangular_face_count += 1
                                else:
                                    non_triangular_face_count += 1
                    is_triangulated = non_triangular_face_count == 0
                except Exception as e:
                    is_triangulated = False
                    error_message = str(e)
                    triangular_face_count = 0
                    non_triangular_face_count = 0
            # Named output variables for Serpens
            TRIANGULAR_FACE_COUNT = triangular_face_count
            NON_TRIANGULAR_FACE_COUNT = non_triangular_face_count
            IS_TRIANGULATED = is_triangulated
            TOTAL_FACE_COUNT = face_count
            ERROR_MESSAGE = error_message
            # Print results (optional, can be removed if using only Serpens)
            print(f"TRIANGULAR_FACE_COUNT: {TRIANGULAR_FACE_COUNT}")
            print(f"NON_TRIANGULAR_FACE_COUNT: {NON_TRIANGULAR_FACE_COUNT}")
            print(f"IS_TRIANGULATED: {IS_TRIANGULATED}")
            print(f"TOTAL_FACE_COUNT: {TOTAL_FACE_COUNT}")
            if ERROR_MESSAGE:
                print(f"ERROR_MESSAGE: {ERROR_MESSAGE}")
            if is_triangulated:
                obj_path = bpy.path.abspath(self.filepath)
                HAS_MTL = None
                HAS_TEXTURE = None
                ALL_FILES_SAME_FOLDER = None
                #import bpy  # Included for Blender compatibility
                # Set the path to your .obj file here
                #obj_path = "/path/to/your/file.obj"  # CHANGE THIS TO YOUR FILE PATH
                # Initialize output variables
                HAS_MTL = False
                MTL_PATH = ""
                HAS_TEXTURE = False
                TEXTURE_PATHS = []
                TEXTURE_EXTENSIONS = []
                ALL_FILES_SAME_FOLDER = False
                ERROR_MESSAGE = None
                try:
                    # Check if obj file exists
                    if not os.path.exists(obj_path):
                        ERROR_MESSAGE = "OBJ file not found"
                    else:
                        obj_dir = os.path.dirname(os.path.abspath(obj_path))
                        # Parse OBJ file to find MTL reference
                        mtl_filename = None
                        with open(obj_path, 'r', errors='replace') as obj_file:
                            for line in obj_file:
                                line = line.strip()
                                if line.startswith('mtllib '):
                                    mtl_filename = line[7:].strip()  # Remove 'mtllib ' prefix
                                    break
                        # Check if MTL file exists
                        if mtl_filename:
                            # Handle relative paths in the OBJ file
                            if os.path.isabs(mtl_filename):
                                mtl_path = mtl_filename
                            else:
                                mtl_path = os.path.join(obj_dir, mtl_filename)
                            if os.path.exists(mtl_path):
                                HAS_MTL = True
                                MTL_PATH = mtl_path
                                mtl_dir = os.path.dirname(os.path.abspath(mtl_path))
                                # Parse MTL file to find texture references
                                with open(mtl_path, 'r', errors='replace') as mtl_file:
                                    for line in mtl_file:
                                        line = line.strip()
                                        # Look for map_Kd (diffuse color texture)
                                        if line.startswith('map_Kd '):
                                            parts = line.split(' ', 1)
                                            if len(parts) > 1:
                                                texture_filename = parts[1].strip()
                                                # Handle relative paths in the MTL file
                                                if os.path.isabs(texture_filename):
                                                    texture_path = texture_filename
                                                else:
                                                    texture_path = os.path.join(mtl_dir, texture_filename)
                                                if os.path.exists(texture_path):
                                                    HAS_TEXTURE = True
                                                    TEXTURE_PATHS.append(texture_path)
                                                    # Get the extension
                                                    _, extension = os.path.splitext(texture_filename)
                                                    TEXTURE_EXTENSIONS.append(extension.lstrip('.'))
                                # Check if all files are in the same folder
                                if HAS_MTL:
                                    # Start with checking if OBJ and MTL are in the same folder
                                    ALL_FILES_SAME_FOLDER = (os.path.normcase(obj_dir) == os.path.normcase(mtl_dir))
                                    # Then check if all textures are also in the same folder
                                    if ALL_FILES_SAME_FOLDER and HAS_TEXTURE:
                                        for texture_path in TEXTURE_PATHS:
                                            texture_dir = os.path.dirname(os.path.abspath(texture_path))
                                            if os.path.normcase(obj_dir) != os.path.normcase(texture_dir):
                                                ALL_FILES_SAME_FOLDER = False
                                                break
                except Exception as e:
                    ERROR_MESSAGE = str(e)
                # Print results (optional, can be removed if using only Serpens)
                print(f"HAS_MTL: {HAS_MTL}")
                print(f"MTL_PATH: {MTL_PATH}")
                print(f"HAS_TEXTURE: {HAS_TEXTURE}")
                print(f"TEXTURE_PATHS: {TEXTURE_PATHS}")
                print(f"TEXTURE_EXTENSIONS: {TEXTURE_EXTENSIONS}")
                print(f"ALL_FILES_SAME_FOLDER: {ALL_FILES_SAME_FOLDER}")
                if ERROR_MESSAGE:
                    print(f"ERROR_MESSAGE: {ERROR_MESSAGE}")
                if ALL_FILES_SAME_FOLDER:
                    obj_path = bpy.path.abspath(self.filepath)
                    output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
                    exe_path = bpy.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'mesh2gs'))
                    import platform
                    # Get paths
                    #obj_path = bpy.path.abspath(self.filepath)
                    #output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
                    #exe_path = bpy.path.abspath(bpy.context.scene.sna_mesh2gs_exe_path)
                    os_name = platform.system()
                    if(sys.platform == 'darwin'):
                        print("mac")
                        exe_path = os.path.join(exe_path, "mac", "mesh2gs")
                        os.chmod(exe_path, 0o777)
                    elif(sys.platform.startswith('win')):
                        print("win")
                        exe_path = os.path.join(exe_path, "win", "mesh2gs_win.exe")
                    else:
                        raise RuntimeError("Unsupported operating system. Only support mac and win!")
                    command = [
                        exe_path,
                        "--mesh",
                        obj_path,
                        "--output_path",
                        output_path
                    ]
                    # Debug prints
                    print("Final exe_path:", exe_path)
                    print("Full command:", command)
                    print("Path exists check:", os.path.exists(exe_path))
                    try:
                        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
                    except Exception as e:
                        raise RuntimeError(e)
                    print("run successfully. Save in", output_path)
                else:
                    self.report({'ERROR'}, message='File structure is incorrect - see documentation')
            else:
                self.report({'WARNING'}, message='Mesh is not triangulated?')
        else:
            obj_path = bpy.path.abspath(self.filepath)
            output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
            exe_path = bpy.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'mesh2gs'))
            import platform
            # Get paths
            #obj_path = bpy.path.abspath(self.filepath)
            #output_path = bpy.path.abspath(os.path.dirname(bpy.path.abspath(self.filepath)) + '\\' + os.path.basename(bpy.path.abspath(bpy.path.abspath(self.filepath))).replace('.obj', '_mesh2gs.ply'))
            #exe_path = bpy.path.abspath(bpy.context.scene.sna_mesh2gs_exe_path)
            os_name = platform.system()
            if(sys.platform == 'darwin'):
                print("mac")
                exe_path = os.path.join(exe_path, "mac", "mesh2gs")
                os.chmod(exe_path, 0o777)
            elif(sys.platform.startswith('win')):
                print("win")
                exe_path = os.path.join(exe_path, "win", "mesh2gs_win.exe")
            else:
                raise RuntimeError("Unsupported operating system. Only support mac and win!")
            command = [
                exe_path,
                "--mesh",
                obj_path,
                "--output_path",
                output_path
            ]
            # Debug prints
            print("Final exe_path:", exe_path)
            print("Full command:", command)
            print("Path exists check:", os.path.exists(exe_path))
            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
            except Exception as e:
                raise RuntimeError(e)
            print("run successfully. Save in", output_path)
        return {"FINISHED"}
