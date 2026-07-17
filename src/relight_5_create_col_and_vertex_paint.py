import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_relight_5__create_col_and_vertex_paint_2AE5F():
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
