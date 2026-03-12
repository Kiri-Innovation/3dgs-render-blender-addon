import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper

class SNA_OT_Dgs_Render_Refresh__Create_Paint_Attribute_84655(bpy.types.Operator):
    bl_idname = "sna.dgs_render_refresh__create_paint_attribute_84655"
    bl_label = "3DGS Render: Refresh - Create Paint Attribute"
    bl_description = "Refreshes or creates the KIRI_3DGS_Paint colour attribute"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        import numpy as np
        # Constants
        SH_0 = 0.28209479177387814
        # Serpens typically passes an object as 'input_obj'. Fall back to active_object if not provided.
        try:
            obj = input_obj  # Serpens input (will be defined if called via Serpens node)
        except NameError:
            obj = bpy.context.active_object  # Fallback for text editor or no Serpens input
            print("No input_obj provided, falling back to active object.")
        # Check if we have a valid object
        if not obj:
            print("Error: No object provided or selected.")
        elif obj.type != 'MESH':
            print(f"Error: Object '{obj.name}' is not a mesh (type: {obj.type}).")
        else:
            mesh = obj.data
            required_attrs = ['f_dc_0', 'f_dc_1', 'f_dc_2', 'opacity']
            # Check for required attributes
            missing_attrs = [attr for attr in required_attrs if attr not in mesh.attributes]
            if missing_attrs:
                print(f"Error: Missing required attributes on '{obj.name}': {missing_attrs}")
            else:
                # Get point count and attribute data
                point_count = len(mesh.vertices)
                expected_length = point_count * 4
                f_dc_0_data = np.array([v.value for v in mesh.attributes['f_dc_0'].data])
                f_dc_1_data = np.array([v.value for v in mesh.attributes['f_dc_1'].data])
                f_dc_2_data = np.array([v.value for v in mesh.attributes['f_dc_2'].data])
                opacity_data = np.array([v.value for v in mesh.attributes['opacity'].data])
                # Verify data lengths
                data_lengths = {
                    'f_dc_0': len(f_dc_0_data),
                    'f_dc_1': len(f_dc_1_data),
                    'f_dc_2': len(f_dc_2_data),
                    'opacity': len(opacity_data)
                }
                if not all(length == point_count for length in data_lengths.values()):
                    print(f"Error: Attribute length mismatch. Expected {point_count}, got: {data_lengths}")
                else:
                    # Calculate RGBA
                    paint_color_data = []
                    for i in range(point_count):
                        R = max(0.0, min(1.0, (f_dc_0_data[i] * SH_0 + 0.5)))
                        G = max(0.0, min(1.0, (f_dc_1_data[i] * SH_0 + 0.5)))
                        B = max(0.0, min(1.0, (f_dc_2_data[i] * SH_0 + 0.5)))
                        A = max(0.0, min(1.0, 1 / (1 + np.exp(-opacity_data[i]))))
                        paint_color_data.extend([R, G, B, A])
                    # Verify output length
                    if len(paint_color_data) != expected_length:
                        print(f"Error: Output length mismatch. Expected {expected_length}, got {len(paint_color_data)}")
                    else:
                        # Update or create attribute
                        if 'KIRI_3DGS_Paint' in mesh.attributes:
                            mesh.attributes.remove(mesh.attributes['KIRI_3DGS_Paint'])
                        paint_attr = mesh.attributes.new(name="KIRI_3DGS_Paint", type='FLOAT_COLOR', domain='POINT')
                        paint_attr.data.foreach_set("color", paint_color_data)
                        mesh.color_attributes.active_color = paint_attr
                        print(f"Successfully updated 'KIRI_3DGS_Paint' on '{obj.name}' with {point_count} points.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
