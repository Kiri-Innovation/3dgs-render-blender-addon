from .important import property_exists
import bpy
from .append_and_add_geo_nodes_function_execute import sna_append_and_add_geo_nodes_function_execute_6BCD7
from .load_from_blender_object import sna_b2_load_from_blender_object_F0CCB
from bpy_extras.io_utils import ImportHelper, ExportHelper


class SNA_OT_Dgs_Render_Import_Ply_E0A3A(bpy.types.Operator, ImportHelper):

    bl_idname = "sna.dgs_render_import_ply_e0a3a"
    bl_label = "3DGS Render: Import PLY"
    bl_description = "Imports a .PLY file and adds 3DGS modifiers and attributes."
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.ply', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        ply_import_path = self.filepath
        output_object = None
        attributes_missing = None
        message = None
        import os
        # Input file path
        #ply_import_path = "C:\\Users\\joe and pig\\Documents\\Flamingo.ply"  # Example path; update as needed
        # Check if the file path is provided and exists
        if not ply_import_path or not os.path.exists(ply_import_path):
            print("Error: No file path provided or file not found.")
            attributes_missing = True
            message = f"Error: No file path provided or file not found at {ply_import_path}."
            output_object = None
        else:
            try:
                # Import the PLY file using Blender's native importer (Blender 4.0+)
                try:
                    bpy.ops.wm.ply_import(filepath=ply_import_path)
                except AttributeError:
                    print("Error: PLY importer operator 'bpy.ops.wm.ply_import' not found. Ensure Blender 4.0 or later is used.")
                    attributes_missing = True
                    message = f"Error: PLY importer operator not found for {os.path.basename(ply_import_path)}. Ensure Blender 4.0 or later is used."
                    output_object = None
                else:
                    # Get the last imported object (assuming it's the PLY mesh)
                    imported_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
                    if not imported_objects:
                        print("Error: No objects were imported from the PLY file.")
                        attributes_missing = True
                        message = f"Error: No objects were imported from the PLY file {os.path.basename(ply_import_path)}."
                        output_object = None
                    else:
                        # Use the first imported object (assuming it's a mesh)
                        obj = imported_objects[0]
                        if obj.type != 'MESH':
                            print("Error: Imported object is not a mesh.")
                            attributes_missing = True
                            message = f"Error: Imported object from {os.path.basename(ply_import_path)} is not a mesh."
                            output_object = None
                        else:
                            # Get the mesh data
                            mesh = obj.data
                            # List of required 3DGS attributes
                            required_attributes = ['f_dc_0', 'f_dc_1', 'f_dc_2', 'opacity', 'scale_0', 'scale_1', 'scale_2', 'rot_0', 'rot_1', 'rot_2', 'rot_3', 'f_rest_0']
                            # Check if all required attributes exist on the mesh
                            attributes_missing = False
                            missing_attrs = []
                            for attr_name in required_attributes:
                                if attr_name not in mesh.attributes:
                                    attributes_missing = True
                                    missing_attrs.append(attr_name)
                            # Set the message and output object based on success or failure
                            if attributes_missing:
                                message = f"Error: One or more required 3DGS attributes ({', '.join(missing_attrs)}) are missing on {obj.name}. Check that .ply is a 3DGS scan."
                                print(message)
                                output_object = None
                            else:
                                message = f"Successfully imported PLY file {os.path.basename(ply_import_path)} and all required 3DGS attributes ({', '.join(required_attributes)}) are present on {obj.name}."
                                print(message)
                                output_object = obj
            except Exception as e:
                print(f"Error importing PLY file: {e}")
                attributes_missing = True
                message = f"Error importing PLY file {os.path.basename(ply_import_path)}: {str(e)}"
                output_object = None
        # The variables are now available for use
        # You can access 'attributes_missing' (boolean), 'message' (string), and 'output_object' (bpy.types.Object or None) in other scripts or logic
        if (bpy.context.scene.sna_dgs_scene_properties.import_face_vert == 'Faces'):
            bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] = 'face'
            sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Store_Origpos_GN', 'KIRI_3DGS_Store_Origpos_GN', bpy.context.view_layer.objects.active)
            bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Store_Origpos_GN')
            sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Render_GN', 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active)
            sna_align_active_values_to_x_4CE1F()
            bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Render_GN')
        else:
            bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] = 'vert'
        import numpy as np
        # Constants from your script
        SH_0 = 0.28209479177387814
        # Get the active object
        obj = bpy.context.active_object
        if not obj or obj.type != 'MESH':
            print("Error: No active mesh object selected.")
        else:
            # Get the mesh data
            mesh = obj.data
            # Check if the required attributes exist
            if not all(attr.name in mesh.attributes for attr in mesh.attributes if attr.name in ['f_dc_0', 'f_dc_1', 'f_dc_2', 'opacity']):
                print("Error: Required attributes (f_dc_0, f_dc_1, f_dc_2, opacity) not found on the mesh.")
            else:
                # Get the number of points (vertices)
                point_count = len(mesh.vertices)
                expected_length = point_count * 4  # Each point has 1 RGBA set (4 values) for both Col and KIRI_3DGS_Paint
                # Extract data from attributes (assuming they are on POINT domain)
                f_dc_0_data = np.array([v.value for v in mesh.attributes['f_dc_0'].data])
                f_dc_1_data = np.array([v.value for v in mesh.attributes['f_dc_1'].data])
                f_dc_2_data = np.array([v.value for v in mesh.attributes['f_dc_2'].data])
                opacity_data = np.array([v.value for v in mesh.attributes['opacity'].data])
                # Debug: Check lengths of input attribute data
                print(f"Number of points (vertices): {point_count}")
                print(f"Length of f_dc_0_data: {len(f_dc_0_data)}")
                print(f"Length of f_dc_1_data: {len(f_dc_1_data)}")
                print(f"Length of f_dc_2_data: {len(f_dc_2_data)}")
                print(f"Length of opacity_data: {len(opacity_data)}")
                # Verify that attribute data lengths match the number of points
                if not (len(f_dc_0_data) == len(f_dc_1_data) == len(f_dc_2_data) == len(opacity_data) == point_count):
                    print("Error: Mismatch in attribute data lengths. Expected length matches point_count.")
                else:
                    # Calculate RGB and Alpha for each point (same calculation for both Col and KIRI_3DGS_Paint)
                    color_data = []  # For both Col and KIRI_3DGS_Paint, one RGBA per point
                    for i in range(point_count):
                        # Calculate RGB (matching your script)
                        R = (f_dc_0_data[i] * SH_0 + 0.5)
                        G = (f_dc_1_data[i] * SH_0 + 0.5)
                        B = (f_dc_2_data[i] * SH_0 + 0.5)
                        # Calculate Alpha (using sigmoid if opacity is in log-space, or raw if [0, 1])
                        # Here, we assume opacity is in log-space (logits) as in your script
                        log_opacity = opacity_data[i]
                        A = 1 / (1 + np.exp(-log_opacity))
                        # Ensure values are in [0, 1]
                        R = max(0.0, min(1.0, R))
                        G = max(0.0, min(1.0, G))
                        B = max(0.0, min(1.0, B))
                        A = max(0.0, min(1.0, A))
                        # Add RGBA for both Col and KIRI_3DGS_Paint (one set per point)
                        color_data.extend([R, G, B, A])
                    # Debug: Check calculated data length
                    print(f"Length of color_data (Col and KIRI_3DGS_Paint): {len(color_data)}")
                    print(f"Expected length for POINT domain: {expected_length}")
                    # Verify data length matches expectation
                    if len(color_data) != expected_length:
                        print(f"Error: Array length mismatch (expected {expected_length}, got {len(color_data)})")
                    else:
                        # Create or update the Col attribute on the point domain
                        if 'Col' in mesh.attributes:
                            mesh.attributes.remove(mesh.attributes['Col'])
                        col_attr = mesh.attributes.new(name="Col", type='FLOAT_COLOR', domain='POINT')
                        col_attr.data.foreach_set("color", color_data)
                        # Create or update the KIRI_3DGS_Paint attribute on the point domain
                        if 'KIRI_3DGS_Paint' in mesh.attributes:
                            mesh.attributes.remove(mesh.attributes['KIRI_3DGS_Paint'])
                        paint_attr = mesh.attributes.new(name="KIRI_3DGS_Paint", type='FLOAT_COLOR', domain='POINT')
                        paint_attr.data.foreach_set("color", color_data)
                        # Set KIRI_3DGS_Paint as the active color attribute
                        mesh.color_attributes.active_color = paint_attr
                        print(f"Created Col attribute on {obj.name} with {point_count} points.")
                        print(f"Created KIRI_3DGS_Paint attribute on {obj.name} with {point_count} color values on the POINT domain.")
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Render_GN', 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Sorter_GN', 'KIRI_3DGS_Sorter_GN', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Adjust_Colour_And_Material', 'KIRI_3DGS_Adjust_Colour_And_Material', bpy.context.view_layer.objects.active)
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Write F_DC_And_Merge', 'KIRI_3DGS_Write F_DC_And_Merge', bpy.context.view_layer.objects.active)
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'].show_viewport = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = False
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material'].show_render = True
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = False
        bpy.context.scene.sna_dgs_scene_properties.update_mode = 'Disable Camera Updates'
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_on_cage = (bpy.context.scene.sna_dgs_scene_properties.import_face_vert == 'Faces')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_in_editmode = (bpy.context.scene.sna_dgs_scene_properties.import_face_vert == 'Faces')
        bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update = False
        bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode = 'Disable Camera Updates'
        if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.materials)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), '..', 'assets', '3DGS Render APPEND V4.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
            appended_C1470 = None if not new_data else new_data[0]
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_viewport = (bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method == 'BLENDED')
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Sorter_GN'].show_render = (bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method == 'BLENDED')
        input_object = bpy.context.view_layer.objects.active
        material_name = 'KIRI_3DGS_Render_Material'
        # Input Variable Names
        #input_object = None  # Should be set to a bpy.types.Object pointer before running
        #material_name = "KIRI_3DGS_Render_Material"  # Name of the material to assign
        # Check if the input object is provided and is valid
        if not input_object or input_object.type != 'MESH':
            print("Error: No valid mesh object provided as input.")
        else:
            # Get the object and its mesh data
            obj = input_object
            mesh = obj.data
            try:
                # Remove all existing material slots
                while len(obj.material_slots) > 0:
                    bpy.context.object.active_material_index = 0  # Set to the first slot to remove
                    bpy.ops.object.material_slot_remove()
                # Check if the material exists; create it if it doesn’t
                if material_name not in bpy.data.materials:
                    new_material = bpy.data.materials.new(name=material_name)
                    new_material.use_nodes = True  # Enable node-based shading (optional, matching your original script)
                else:
                    new_material = bpy.data.materials[material_name]
                # Add the material to the object as a new slot
                obj.data.materials.append(new_material)
                print(f"Assigned material '{material_name}' to {obj.name} and removed existing material slots.")
            except Exception as e:
                print(f"Error assigning material to {obj.name}: {e}")
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_61'] = bpy.data.materials['KIRI_3DGS_Render_Material']
        bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        if (bpy.context.scene.sna_dgs_scene_properties.import_uv and (bpy.context.scene.sna_dgs_scene_properties.import_face_vert == 'Faces')):
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
            bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
            bpy.ops.mesh.dissolve_limited('INVOKE_DEFAULT', )
            bpy.ops.uv.reset('INVOKE_DEFAULT', )
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        if bpy.context.scene.sna_dgs_scene_properties.import_proxy:
            sna_b2_load_from_blender_object_F0CCB(bpy.context.view_layer.objects.active.name + 'Splat_Proxy')
        return {"FINISHED"}
