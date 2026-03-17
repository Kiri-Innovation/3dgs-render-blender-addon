from .important import *
def sna_shader_system_A4AED():
    import bpy
    import os
    from gpu_extras.batch import batch_for_shader
    import gpu.types
    import numpy as np
    VERTEX_SHADER_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'vert.glsl')
    FRAGMENT_SHADER_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'frag.glsl')
    COMPOSITE_VERTEX_SHADER_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'composite_vert.glsl')
    COMPOSITE_FRAGMENT_SHADER_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'composite_frag.glsl')
    # ========== VARIABLES (EDIT THESE) ==========
    #VERTEX_SHADER_PATH = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders\vert.glsl"
    #FRAGMENT_SHADER_PATH = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders\frag.glsl"
    #COMPOSITE_VERTEX_SHADER_PATH = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders\composite_vert.glsl"
    #COMPOSITE_FRAGMENT_SHADER_PATH = r"D:\3d\Blender\my work\KIRI\KIRI - Tools\KIRI - Blender 3DGS Render\SplatForge Adaption\shaders\composite_frag.glsl"
    MAX_GAUSSIANS = 1000000
    # ============================================

    def read_shader_file(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"Error reading shader file {filepath}: {e}")
            return None
    try:
        # ========== CLEANUP EXISTING SHADERS ==========
        print("Cleaning up existing shader resources...")
        cleanup_attrs = [
            'gaussian_quad_shader', 'gaussian_quad_batch', 
            'gaussian_composite_shader', 'gaussian_composite_batch'
        ]
        for attr in cleanup_attrs:
            if hasattr(bpy, attr):
                delattr(bpy, attr)
        # Check shader files exist
        shader_files = [VERTEX_SHADER_PATH, FRAGMENT_SHADER_PATH, 
                       COMPOSITE_VERTEX_SHADER_PATH, COMPOSITE_FRAGMENT_SHADER_PATH]
        for shader_file in shader_files:
            if not os.path.exists(shader_file):
                raise FileNotFoundError(f"Shader not found: {shader_file}")
        # Read shader sources
        vertex_source = read_shader_file(VERTEX_SHADER_PATH)
        fragment_source = read_shader_file(FRAGMENT_SHADER_PATH)
        composite_vertex_source = read_shader_file(COMPOSITE_VERTEX_SHADER_PATH)
        composite_fragment_source = read_shader_file(COMPOSITE_FRAGMENT_SHADER_PATH)
        if not all([vertex_source, fragment_source, composite_vertex_source, composite_fragment_source]):
            raise ValueError("Failed to read shader files")
        print("Loaded all shader files successfully")
        # ========== CREATE MAIN GAUSSIAN SHADER ==========
        shader_info = gpu.types.GPUShaderCreateInfo()
        # Vertex inputs
        shader_info.vertex_in(0, 'VEC2', "quad_coord")
        # Push constants
        shader_info.push_constant("MAT4", "ViewMatrix")
        shader_info.push_constant("MAT4", "ProjectionMatrix") 
        shader_info.push_constant("VEC3", "focal_parameters")
        shader_info.push_constant("VEC3", "camera_position")
        shader_info.push_constant("INT", "render_mode")
        shader_info.push_constant("INT", "sh_degree")
        shader_info.push_constant("VEC2", "texture_dimensions")
        shader_info.push_constant("VEC2", "indices_dimensions")
        shader_info.push_constant("VEC2", "depth_texture_size")
        # Samplers
        shader_info.sampler(0, 'FLOAT_3D', "gaussian_data")
        shader_info.sampler(1, 'FLOAT_2D', "sorted_indices")
        shader_info.sampler(2, 'FLOAT_2D', "blender_depth")
        shader_info.sampler(3, 'FLOAT_2D', "object_metadata")
        # Interface
        interface = gpu.types.GPUStageInterfaceInfo("splat_forge_quad_interface")
        interface.smooth('VEC3', "v_color")
        interface.smooth('VEC3', "v_conic")
        interface.smooth('VEC2', "v_coordxy")
        interface.smooth('FLOAT', "v_alpha")
        interface.smooth('VEC4', "v_rotation")
        interface.flat('INT', "v_render_mode")
        interface.smooth('FLOAT', "v_depth")
        shader_info.vertex_out(interface)
        shader_info.fragment_out(0, 'VEC4', 'fragColor')
        shader_info.vertex_source(vertex_source)
        shader_info.fragment_source(fragment_source)
        # Create main shader
        quad_shader = gpu.shader.create_from_info(shader_info)
        del interface
        del shader_info
        # ========== CREATE COMPOSITE SHADER ==========
        composite_shader_info = gpu.types.GPUShaderCreateInfo()
        composite_shader_info.vertex_in(0, 'VEC2', "position")
        composite_shader_info.vertex_in(1, 'VEC2', "uv")
        composite_interface = gpu.types.GPUStageInterfaceInfo("composite_interface")
        composite_interface.smooth('VEC2', "uvInterp")
        composite_shader_info.vertex_out(composite_interface)
        composite_shader_info.sampler(0, 'FLOAT_2D', "image")
        composite_shader_info.fragment_out(0, 'VEC4', "FragColor")
        composite_shader_info.vertex_source(composite_vertex_source)
        composite_shader_info.fragment_source(composite_fragment_source)
        composite_shader = gpu.shader.create_from_info(composite_shader_info)
        del composite_interface
        del composite_shader_info
        # ========== CREATE BATCHES ==========
        base_quad = np.array([
            [-1.0,  1.0],
            [ 1.0,  1.0],
            [ 1.0, -1.0],
            [-1.0, -1.0],
        ], dtype=np.float32)
        base_indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
        quad_batch = batch_for_shader(
            quad_shader, 
            'TRIS',
            {"quad_coord": base_quad},
            indices=base_indices
        )
        composite_batch = batch_for_shader(
            composite_shader, 
            'TRI_FAN',
            {
                "position": ((-1, -1), (1, -1), (1, 1), (-1, 1)),
                "uv": ((0, 0), (1, 0), (1, 1), (0, 1)),
            }
        )
        # Store globally
        bpy.gaussian_quad_shader = quad_shader
        bpy.gaussian_quad_batch = quad_batch
        bpy.gaussian_composite_shader = composite_shader  
        bpy.gaussian_composite_batch = composite_batch
        print("Multi-object shader system created successfully")
    except Exception as e:
        print(f"Error creating shader system: {e}")
        import traceback
        traceback.print_exc()
