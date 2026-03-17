import bpy
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


class SNA_OT_Dgs_Render_Auto_Generate_Crop_Object_F20D5(bpy.types.Operator):
    bl_idname = "sna.dgs_render_auto_generate_crop_object_f20d5"
    bl_label = "3DGS Render: Auto Generate Crop Object"
    bl_description = "Generate a crop object based on point clustering"
    bl_options = {"REGISTER", "UNDO"}

    def sna_filter_mode_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_filter_mode: bpy.props.EnumProperty(name='Filter Mode', description='', options={'HIDDEN'}, items=[('quick', 'quick', '', 0, 0), ('gentle', 'gentle', '', 0, 1), ('aggressive', 'aggressive', '', 0, 2)])
    sna_filter_epsilon: bpy.props.FloatProperty(name='Filter Epsilon', description='', options={'HIDDEN'}, default=0.029999999329447746, subtype='NONE', unit='NONE', min=0.009999999776482582, max=0.10000000149011612, step=3, precision=2)
    sna_filter_min_points: bpy.props.IntProperty(name='Filter Min Points', description='', options={'HIDDEN'}, default=10, subtype='NONE', min=1)
    sna_fast_mode: bpy.props.BoolProperty(name='Fast Mode', description='', options={'HIDDEN'}, default=False)
    sna_create_convex_hull_object: bpy.props.BoolProperty(name='Create Convex Hull Object', description='', options={'HIDDEN'}, default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        OPEN3D_AVAILABLE = None
        #!/usr/bin/env python3
        """
        Open3D Availability Checker (ASCII-only)
        ========================================
        Simple standalone script to test if Open3D can be imported in Blender.
        Returns boolean result for programmatic use.
        Usage:
        - Run in Blender's Text Editor
        - Check console for result
        - Use returned boolean in other scripts
        """

        def check_open3d_availability():
            """
            Test if Open3D can be imported successfully.
            Returns:
                bool: True if Open3D is available, False otherwise
            """
            print("Testing Open3D availability...")
            try:
                import open3d as o3d
                # Basic import successful
                print("SUCCESS: Open3D import successful")
                print("Version: " + str(o3d.__version__))
                # Test basic functionality
                try:
                    # Try creating a basic point cloud
                    import numpy as np
                    test_points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
                    pcd = o3d.geometry.PointCloud()
                    pcd.points = o3d.utility.Vector3dVector(test_points)
                    print("SUCCESS: Basic functionality test passed")
                    print("Test point cloud created with " + str(len(pcd.points)) + " points")
                    return True
                except Exception as e:
                    print("WARNING: Open3D imported but basic functionality failed")
                    print("Error: " + str(e))
                    return False
            except ImportError as e:
                print("FAILED: Open3D import failed")
                print("Error: " + str(e))
                print("Install Open3D wheels to enable point cloud filtering")
                return False
            except Exception as e:
                print("ERROR: Open3D import unexpected error")
                print("Error: " + str(e))
                return False

        def main():
            """Main function with detailed output"""
            print("=" * 50)
            print("OPEN3D AVAILABILITY TEST")
            print("=" * 50)
            # Test availability
            is_available = check_open3d_availability()
            print("")
            print("=" * 50)
            print("RESULT")
            print("=" * 50)
            if is_available:
                print("RESULT: Open3D is AVAILABLE")
                print("STATUS: DB filtering can be enabled")
                print("STATUS: Point cloud operations will work")
            else:
                print("RESULT: Open3D is NOT AVAILABLE")
                print("STATUS: DB filtering is disabled")
                print("INFO: Install Open3D wheels to enable functionality")
            print("")
            print("Boolean result: " + str(is_available))
            return is_available
        # Global variable for easy access
        OPEN3D_AVAILABLE = None
        # Auto-execute when script runs
        if __name__ == "__main__" or True:
            OPEN3D_AVAILABLE = main()
            # Store result in a way other scripts can access
            try:
                import bpy
                # Store in scene properties if in Blender
                if hasattr(bpy.context, 'scene'):
                    bpy.context.scene['open3d_available'] = OPEN3D_AVAILABLE
                    print("INFO: Stored result in scene['open3d_available'] = " + str(OPEN3D_AVAILABLE))
            except:
                pass  # Not in Blender or no scene context
        # ===== USAGE EXAMPLES =====
        print("""
        === USAGE EXAMPLES ===
        1. PROGRAMMATIC USE:
           result = check_open3d_availability()
           if result:
               # Run Open3D operations
           else:
               # Show error message
        2. SERPENS INTEGRATION:
           # Check the global variable
           if OPEN3D_AVAILABLE:
               # Enable DB filter UI
           else:
               # Show installation message
        3. SCENE PROPERTY ACCESS:
           # Access from other scripts
           is_available = bpy.context.scene.get('open3d_available', False)
        4. QUICK TEST:
           # Just run this script to see status
        """)
        if OPEN3D_AVAILABLE:
            filter_eps = self.sna_filter_epsilon
            filter_min_points = self.sna_filter_min_points
            filter_mode = self.sna_filter_mode
            filter_fast_mode = self.sna_fast_mode
            filter_result_object = None
            import bmesh
            from mathutils import Vector
            # ===== SAFE OPEN3D AVAILABILITY CHECK =====
            # Global flag to control script execution
            OPEN3D_AVAILABLE = False
            o3d = None
            try:
                import open3d as o3d
                OPEN3D_AVAILABLE = True
                print("✅ Open3D available - DB filtering enabled")
                print(f"   Open3D version: {o3d.__version__}")
            except ImportError as e:
                OPEN3D_AVAILABLE = False
                o3d = None
                print("⚠️ Open3D not available - DB filtering disabled")
                print("   Install Open3D wheels to enable point cloud filtering")
                print("   Script will not execute any filtering operations")
            # ===== SERPENS GLOBAL VARIABLES =====
            # Main filtering mode - change this value in Serpens
            #filter_mode = "quick"  # Default value for when not set by Serpens
            # Optional object name - leave empty to use active object
            filter_obj_name = ""
            # GLOBAL OUTPUT VARIABLE - stores the result of the last filter operation
            filter_result_object = None
            # DBSCAN parameters
            #filter_eps = 0.03  # Default value for when not set by Serpens
            #filter_min_points = 10
            filter_auto_eps = False
            # Statistical outlier removal parameters
            filter_nb_neighbors = 20
            filter_std_ratio = 2.0
            # Radius outlier removal parameters
            filter_radius_nb_points = 16
            filter_radius = 0.05
            # ===== PERFORMANCE OPTIMIZATION VARIABLES =====
            # Speed optimization settings
            filter_use_voxel_downsample = True
            filter_voxel_size = 0.01
            filter_max_points = 100000
            #filter_fast_mode = True  # Default value for when not set by Serpens
            filter_sample_ratio = 0.3
            # ===== TIMING VARIABLES =====
            # Timing control
            filter_show_timing = True  # Set to False to disable timing output
            # ===== TIMING UTILITIES =====

            def format_time(seconds):
                """Format time in a readable way"""
                if seconds < 1:
                    return f"{seconds*1000:.1f}ms"
                elif seconds < 60:
                    return f"{seconds:.2f}s"
                else:
                    minutes = int(seconds // 60)
                    remaining_seconds = seconds % 60
                    return f"{minutes}m {remaining_seconds:.1f}s"

            def time_function(func, *args, **kwargs):
                """Wrapper to time function execution"""
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                if filter_show_timing:
                    print(f"⏱️  {func.__name__} took {format_time(execution_time)}")
                return result, execution_time
            # ===== SAFETY CHECK FUNCTION =====

            def check_open3d_available():
                """Check if Open3D is available and return appropriate message"""
                if not OPEN3D_AVAILABLE:
                    print("❌ DB filtering unavailable - Open3D not installed")
                    print("   Install Open3D wheels and restart Blender to enable filtering")
                    return False
                return True
            # ===== MAIN FUNCTIONS (Only defined if Open3D available) =====
            if OPEN3D_AVAILABLE:

                def mesh_to_point_cloud(obj_name):
                    """Convert Blender mesh to Open3D point cloud"""
                    obj = bpy.data.objects[obj_name]
                    mesh = obj.data
                    # Get world coordinates of vertices
                    points = []
                    for vertex in mesh.vertices:
                        world_coord = obj.matrix_world @ vertex.co
                        points.append([world_coord.x, world_coord.y, world_coord.z])
                    # Create Open3D point cloud
                    pcd = o3d.geometry.PointCloud()
                    pcd.points = o3d.utility.Vector3dVector(np.array(points))
                    return pcd, np.array(points)

                def filter_with_dbscan(pcd, eps=0.1, min_points=10):
                    """Apply DBSCAN clustering to filter point cloud"""
                    print(f"Starting DBSCAN with eps={eps}, min_points={min_points}")
                    print(f"Point cloud has {len(pcd.points)} points")
                    # Apply DBSCAN clustering
                    labels = np.array(pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True))
                    # Analyze clusters
                    max_label = labels.max()
                    print(f"Point cloud has {max_label + 1} clusters")
                    # Count points in each cluster
                    cluster_counts = {}
                    noise_count = np.sum(labels == -1)
                    for i in range(max_label + 1):
                        count = np.sum(labels == i)
                        cluster_counts[i] = count
                        print(f"Cluster {i}: {count} points")
                    print(f"Noise points: {noise_count}")
                    return labels, cluster_counts

                def filter_with_statistical_outlier_removal(pcd, nb_neighbors=20, std_ratio=2.0):
                    """Remove statistical outliers"""
                    print(f"Applying statistical outlier removal (neighbors={nb_neighbors}, std_ratio={std_ratio})")
                    pcd_filtered, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
                    print(f"Removed {len(pcd.points) - len(pcd_filtered.points)} outlier points")
                    return pcd_filtered, ind

                def filter_with_radius_outlier_removal(pcd, nb_points=16, radius=0.05):
                    """Remove points with few neighbors in radius"""
                    print(f"Applying radius outlier removal (nb_points={nb_points}, radius={radius})")
                    pcd_filtered, ind = pcd.remove_radius_outlier(nb_points=nb_points, radius=radius)
                    print(f"Removed {len(pcd.points) - len(pcd_filtered.points)} sparse points")
                    return pcd_filtered, ind

                def optimize_point_cloud_for_speed(pcd, max_points=100000, voxel_size=0.01, sample_ratio=0.3, use_voxel=True):
                    """Optimize point cloud for faster processing"""
                    original_size = len(pcd.points)
                    print(f"Original point cloud: {original_size} points")
                    if original_size <= max_points:
                        print("Point cloud size OK, no optimization needed")
                        return pcd, np.arange(original_size)
                    if use_voxel:
                        # Voxel downsampling - maintains structure better
                        print(f"Applying voxel downsampling (voxel_size={voxel_size})...")
                        pcd_down = pcd.voxel_down_sample(voxel_size)
                        optimized_size = len(pcd_down.points)
                        print(f"Voxel downsampled to {optimized_size} points ({optimized_size/original_size*100:.1f}%)")
                        # Use Open3D's KDTree to find closest original points
                        down_points = np.asarray(pcd_down.points)
                        # Use Open3D KDTree to find closest original points
                        pcd_tree = o3d.geometry.KDTreeFlann(pcd)
                        indices = []
                        for i, point in enumerate(down_points):
                            [_, idx, _] = pcd_tree.search_knn_vector_3d(point, 1)
                            if len(idx) > 0:
                                indices.append(idx[0])
                            else:
                                indices.append(0)  # Fallback
                        return pcd_down, np.array(indices)
                    else:
                        # Random sampling - faster but less structured
                        print(f"Applying random sampling (ratio={sample_ratio})...")
                        sample_size = int(original_size * sample_ratio)
                        sample_indices = np.random.choice(original_size, sample_size, replace=False)
                        pcd_down = pcd.select_by_index(sample_indices)
                        optimized_size = len(pcd_down.points)
                        print(f"Random sampled to {optimized_size} points ({optimized_size/original_size*100:.1f}%)")
                        return pcd_down, sample_indices

                def dbscan_clustering(pcd, eps=0.1, min_points=10):
                    """DBSCAN clustering using Open3D (optimized)"""
                    points = np.asarray(pcd.points)
                    # Safety check for eps value to prevent memory issues
                    if eps > 1.0:
                        print(f"Warning: eps={eps} is very large, capping at 0.5 to prevent memory issues")
                        eps = 0.5
                    print(f"🔧 Using Open3D DBSCAN with eps={eps:.4f}, min_samples={min_points}")
                    clustering_start = time.time()
                    labels = np.array(pcd.cluster_dbscan(
                        eps=eps, 
                        min_points=min_points, 
                        print_progress=False
                    ))
                    clustering_time = time.time() - clustering_start
                    if filter_show_timing:
                        print(f"⏱️  Open3D DBSCAN clustering took {format_time(clustering_time)}")
                    # Analyze clusters
                    unique_labels = np.unique(labels)
                    cluster_counts = {}
                    for label in unique_labels:
                        if label != -1:  # Skip noise
                            count = np.sum(labels == label)
                            cluster_counts[label] = count
                    noise_count = np.sum(labels == -1)
                    print(f"Found {len(cluster_counts)} clusters, {noise_count} noise points")
                    # Print cluster info
                    if len(cluster_counts) > 0:
                        sorted_clusters = sorted(cluster_counts.items(), key=lambda x: x[1], reverse=True)
                        print("Top 5 largest clusters:")
                        for i, (label, count) in enumerate(sorted_clusters[:5]):
                            print(f"  Cluster {label}: {count} points")
                    return labels, cluster_counts

                def estimate_eps_automatically(pcd, k=4):
                    """Estimate eps parameter automatically using k-distance graph"""
                    print(f"Auto-estimating eps using {k}-distance graph...")
                    points = np.asarray(pcd.points)
                    n_points = len(points)
                    if n_points < k:
                        print(f"Warning: Not enough points ({n_points}) for k={k}, using k={n_points-1}")
                        k = max(1, n_points - 1)
                    # Sample points if too many for performance
                    if n_points > 10000:
                        sample_size = 10000
                        sample_indices = np.random.choice(n_points, sample_size, replace=False)
                        sample_points = points[sample_indices]
                        print(f"Sampling {sample_size} points for eps estimation")
                    else:
                        sample_points = points
                    # Build KDTree and find k-nearest neighbors
                    pcd_sample = o3d.geometry.PointCloud()
                    pcd_sample.points = o3d.utility.Vector3dVector(sample_points)
                    pcd_tree = o3d.geometry.KDTreeFlann(pcd_sample)
                    k_distances = []
                    for point in sample_points:
                        [_, idx, distances] = pcd_tree.search_knn_vector_3d(point, k + 1)  # +1 because first is the point itself
                        if len(distances) > k:
                            k_distances.append(np.sqrt(distances[k]))  # k-th distance (skip the first which is 0)
                        elif len(distances) > 1:
                            k_distances.append(np.sqrt(distances[-1]))  # Use the farthest available
                    k_distances = np.array(k_distances)
                    k_distances = np.sort(k_distances)
                    # Use elbow method to find optimal eps
                    # Look for the point where the slope changes most dramatically
                    if len(k_distances) > 10:
                        # Use percentile-based estimation
                        eps_estimate = np.percentile(k_distances, 90)  # 90th percentile often works well
                        print(f"Estimated eps: {eps_estimate:.6f}")
                        print(f"k-distance stats: min={k_distances.min():.6f}, "
                              f"median={np.median(k_distances):.6f}, "
                              f"90th percentile={np.percentile(k_distances, 90):.6f}, "
                              f"max={k_distances.max():.6f}")
                        return eps_estimate
                    else:
                        # Fallback for very small point clouds
                        eps_estimate = np.median(k_distances) if len(k_distances) > 0 else 0.1
                        print(f"Small point cloud, using median k-distance: {eps_estimate:.6f}")
                        return eps_estimate

                def create_mesh_from_indices(original_obj_name, indices, suffix=""):
                    """Create new mesh object from selected vertex indices"""
                    # Get original object and mesh
                    original_obj = bpy.data.objects[original_obj_name]
                    original_mesh = original_obj.data
                    # Create new mesh
                    new_mesh = bpy.data.meshes.new(f"{original_obj_name}{suffix}")
                    # Get vertices at specified indices
                    vertices = []
                    for idx in indices:
                        if 0 <= idx < len(original_mesh.vertices):
                            vert = original_mesh.vertices[idx]
                            vertices.append(vert.co[:])  # Convert to tuple
                    # Create mesh with just vertices (no faces for point cloud)
                    new_mesh.from_pydata(vertices, [], [])
                    new_mesh.update()
                    # Create new object
                    new_obj = bpy.data.objects.new(f"{original_obj_name}{suffix}", new_mesh)
                    # Copy transformation from original
                    new_obj.matrix_world = original_obj.matrix_world.copy()
                    # Add to scene
                    bpy.context.collection.objects.link(new_obj)
                    print(f"Created mesh '{new_obj.name}' with {len(vertices)} vertices")
                    return new_obj

                def point_cloud_filter(mode="quick", obj_name=None, eps=0.1, min_points=10, auto_eps=False):
                    """Main point cloud filtering function with comprehensive timing"""
                    # ===== TOTAL TIMING START =====
                    total_start_time = time.time()
                    print(f"\n🎯 POINT CLOUD FILTER - MODE: {mode.upper()}")
                    print(f"📊 Settings: eps={eps}, min_points={min_points}, auto_eps={auto_eps}")
                    print(f"⏱️  Timing enabled: {filter_show_timing}")
                    # Get target object
                    if obj_name:
                        if obj_name not in bpy.data.objects:
                            print(f"❌ Object '{obj_name}' not found")
                            return None
                        target_obj = bpy.data.objects[obj_name]
                    else:
                        target_obj = bpy.context.active_object
                        if not target_obj:
                            print("❌ No active object selected")
                            return None
                        obj_name = target_obj.name
                    if target_obj.type != 'MESH':
                        print(f"❌ Object '{obj_name}' is not a mesh")
                        return None
                    print(f"🎯 Processing object: {obj_name}")
                    print(f"   Vertices: {len(target_obj.data.vertices)}")
                    try:
                        # ===== STEP 1: CONVERT TO POINT CLOUD =====
                        print(f"\n📍 Step 1: Converting mesh to point cloud...")
                        step_start = time.time()
                        pcd, original_indices = mesh_to_point_cloud(obj_name)
                        step_time = time.time() - step_start
                        if filter_show_timing:
                            print(f"⏱️  Mesh conversion took {format_time(step_time)}")
                        # ===== STEP 2: SPEED OPTIMIZATION =====
                        print(f"\n⚡ Step 2: Speed optimization...")
                        step_start = time.time()
                        pcd_optimized, speed_indices = optimize_point_cloud_for_speed(
                            pcd, filter_max_points, filter_voxel_size, filter_sample_ratio, filter_use_voxel_downsample
                        )
                        step_time = time.time() - step_start
                        if filter_show_timing:
                            print(f"⏱️  Speed optimization took {format_time(step_time)}")
                        # ===== STEP 3: AUTO EPS ESTIMATION =====
                        if auto_eps:
                            print(f"\n🔍 Step 3: Auto-estimating eps...")
                            step_start = time.time()
                            eps = estimate_eps_automatically(pcd_optimized)
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Eps estimation took {format_time(step_time)}")
                        # ===== MAIN FILTERING MODES =====
                        if mode == "quick":
                            print(f"\n🚀 Mode: Quick DBSCAN clustering")
                            step_start = time.time()
                            labels, cluster_counts = dbscan_clustering(pcd_optimized, eps, min_points)
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  DBSCAN clustering took {format_time(step_time)}")
                            # Get largest cluster
                            if len(cluster_counts) > 0:
                                largest_cluster = max(cluster_counts.items(), key=lambda x: x[1])
                                cluster_label, cluster_size = largest_cluster
                                print(f"Selecting largest cluster: {cluster_label} ({cluster_size} points)")
                                # Get indices of points in largest cluster
                                cluster_mask = labels == cluster_label
                                cluster_indices = np.where(cluster_mask)[0]
                                # Map back to original if we did speed optimization
                                if len(speed_indices) != len(original_indices):
                                    final_indices = speed_indices[cluster_indices]
                                else:
                                    final_indices = cluster_indices
                                print(f"\n🔨 Creating result mesh...")
                                step_start = time.time()
                                result_obj = create_mesh_from_indices(obj_name, final_indices, "_quick_filtered")
                                step_time = time.time() - step_start
                                if filter_show_timing:
                                    print(f"⏱️  Mesh creation took {format_time(step_time)}")
                            else:
                                print("❌ No clusters found!")
                                return None
                        elif mode == "aggressive":
                            print(f"\n💪 Mode: Aggressive filtering (DBSCAN + Statistical + Radius)")
                            # Step 1: DBSCAN
                            print("Step 1: DBSCAN clustering...")
                            step_start = time.time()
                            labels, cluster_counts = dbscan_clustering(pcd_optimized, eps, min_points)
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  DBSCAN took {format_time(step_time)}")
                            if len(cluster_counts) == 0:
                                print("❌ No clusters found in DBSCAN!")
                                return None
                            # Get largest cluster
                            largest_cluster = max(cluster_counts.items(), key=lambda x: x[1])
                            cluster_label, cluster_size = largest_cluster
                            cluster_mask = labels == cluster_label
                            cluster_indices = np.where(cluster_mask)[0]
                            # Create point cloud from largest cluster
                            pcd_clustered = pcd_optimized.select_by_index(cluster_indices)
                            # Step 2: Statistical outlier removal
                            print("Step 2: Statistical outlier removal...")
                            step_start = time.time()
                            pcd_stat, stat_indices = filter_with_statistical_outlier_removal(
                                pcd_clustered, filter_nb_neighbors, filter_std_ratio
                            )
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Statistical filtering took {format_time(step_time)}")
                            # Step 3: Radius outlier removal
                            print("Step 3: Radius outlier removal...")
                            step_start = time.time()
                            pcd_final, radius_indices = filter_with_radius_outlier_removal(
                                pcd_stat, filter_radius_nb_points, filter_radius
                            )
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Radius filtering took {format_time(step_time)}")
                            # Map indices back to original
                            # radius_indices -> points in stat result
                            # stat_indices[radius_indices] -> points in clustered result  
                            # cluster_indices[...] -> points in original/speed optimized result
                            temp_indices = stat_indices[radius_indices]
                            final_cluster_indices = cluster_indices[temp_indices]
                            # Map back to original if we did speed optimization
                            if len(speed_indices) != len(original_indices):
                                final_indices = speed_indices[final_cluster_indices]
                            else:
                                final_indices = final_cluster_indices
                            print(f"\n🔨 Creating result mesh...")
                            step_start = time.time()
                            result_obj = create_mesh_from_indices(obj_name, final_indices, "_aggressive_filtered")
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Mesh creation took {format_time(step_time)}")
                        elif mode == "gentle":
                            print(f"\n🌸 Mode: Gentle filtering (Statistical outlier removal only)")
                            step_start = time.time()
                            pcd_filtered, indices = filter_with_statistical_outlier_removal(
                                pcd_optimized, filter_nb_neighbors, filter_std_ratio
                            )
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Statistical filtering took {format_time(step_time)}")
                            # Map back to original if needed
                            if len(speed_indices) != len(original_indices):
                                final_indices = speed_indices[indices]
                            else:
                                final_indices = indices
                            print(f"\n🔨 Creating result mesh...")
                            step_start = time.time()
                            result_obj = create_mesh_from_indices(obj_name, final_indices, "_gentle_filtered")
                            step_time = time.time() - step_start
                            if filter_show_timing:
                                print(f"⏱️  Mesh creation took {format_time(step_time)}")
                        # Add other modes as needed...
                        else:
                            print(f"❌ Mode '{mode}' not implemented")
                            return None
                    except Exception as e:
                        print(f"❌ Filtering failed: {e}")
                        import traceback
                        traceback.print_exc()
                        return None
                    # ===== TOTAL TIMING END =====
                    total_end_time = time.time()
                    total_time = total_end_time - total_start_time
                    # Store result in global variable for Serpens
                    filter_result_object = result_obj
                    if result_obj:
                        print(f"\n✅ Filter completed! Created: {result_obj.name}")
                        print(f"📊 Final vertex count: {len(result_obj.data.vertices)}")
                        if filter_show_timing:
                            print(f"⏱️  🎯 TOTAL PROCESSING TIME: {format_time(total_time)}")
                    return result_obj
            # ===== SAFE WRAPPER FUNCTIONS =====

            def point_cloud_filter_safe(*args, **kwargs):
                """Safe wrapper for point cloud filtering"""
                if not check_open3d_available():
                    return None
                return point_cloud_filter(*args, **kwargs)

            def run_point_cloud_filter():
                """Run point cloud filter with current global settings"""
                if not check_open3d_available():
                    return None
                if not OPEN3D_AVAILABLE:
                    return None
                return point_cloud_filter(
                    mode=filter_mode,
                    obj_name=filter_obj_name if filter_obj_name else None,
                    eps=filter_eps,
                    min_points=filter_min_points,
                    auto_eps=filter_auto_eps
                )

            def execute_point_cloud_filter():
                """Auto-execute point cloud filtering using global variables"""
                global filter_result_object
                print(f"\n=== AUTO-EXECUTING POINT CLOUD FILTER ===")
                print(f"Mode: {filter_mode}")
                print(f"Open3D Available: {OPEN3D_AVAILABLE}")
                print(f"Show timing: {filter_show_timing}")
                if not check_open3d_available():
                    filter_result_object = None
                    return None
                # Get object name
                obj_name = filter_obj_name if filter_obj_name else None
                # Execute filtering
                try:
                    result = point_cloud_filter(
                        mode=filter_mode,
                        obj_name=obj_name,
                        eps=filter_eps,
                        min_points=filter_min_points,
                        auto_eps=filter_auto_eps
                    )
                    if result:
                        filter_result_object = result
                        print(f"✓ Filter completed! Created: {result.name}")
                        print(f"✓ Final check - filter_result_object = {filter_result_object}")
                    else:
                        print("✗ Filter completed but no objects created")
                        filter_result_object = None
                    return result
                except Exception as e:
                    print(f"✗ Filter failed: {e}")
                    import traceback
                    traceback.print_exc()
                    filter_result_object = None
                    return None
            # ===== DEBUG FUNCTIONS =====

            def debug_setup():
                """Debug function to check if everything is working"""
                print("=== DEBUGGING SETUP ===")
                if not check_open3d_available():
                    return False
                # Check active object
                if bpy.context.active_object:
                    obj = bpy.context.active_object
                    print(f"✓ Active object: {obj.name}")
                    print(f"  Object type: {obj.type}")
                    if obj.type == 'MESH':
                        print(f"  Vertex count: {len(obj.data.vertices)}")
                    else:
                        print("✗ Active object is not a mesh!")
                        return False
                else:
                    print("✗ No active object selected!")
                    return False
                print(f"✓ Global variables:")
                print(f"  filter_mode: {filter_mode}")
                print(f"  filter_auto_eps: {filter_auto_eps}")
                print(f"  filter_eps: {filter_eps}")
                print(f"  filter_min_points: {filter_min_points}")
                print(f"  filter_show_timing: {filter_show_timing}")
                return True

            def test_quick_filter():
                """Test function - runs quick filter on active object"""
                print("\n=== TESTING QUICK FILTER ===")
                if not debug_setup():
                    print("Setup check failed - cannot run filter")
                    return None
                try:
                    print("Running quick filter...")
                    result = run_point_cloud_filter()
                    if result:
                        print(f"✓ Filter completed successfully!")
                        print(f"  Created object: {result.name}")
                    else:
                        print("✗ Filter returned None - check console for errors")
                    return result
                except Exception as e:
                    print(f"✗ Filter failed with error: {e}")
                    import traceback
                    traceback.print_exc()
                    return None
            # ===== AUTO-EXECUTE ONLY IF OPEN3D IS AVAILABLE =====
            if OPEN3D_AVAILABLE:
                if __name__ == "__main__" or True:
                    result = execute_point_cloud_filter()
                    if result:
                        filter_result_object = result
                        print(f"\n=== FINAL RESULT ===")
                        print(f"filter_result_object = {filter_result_object}")
                        print(f"Object name: {filter_result_object.name}")
                        print(f"Vertex count: {len(filter_result_object.data.vertices)}")
                    else:
                        filter_result_object = None
                        print(f"\n=== FINAL RESULT ===")
                        print("filter_result_object = None")
            else:
                # Don't execute anything if Open3D is not available
                print("\n❌ SCRIPT NOT EXECUTED - OPEN3D REQUIRED")
                print("💡 TO ENABLE DB FILTERING:")
                print("1. Install Open3D wheels in your addon")
                print("2. Update blender_manifest.toml with wheel paths")
                print("3. Restart Blender")
                print("4. Run this script again")
                # Set result to None
                filter_result_object = None
            # ===== USAGE NOTES =====
            if OPEN3D_AVAILABLE:
                print(f"""
            === POINT CLOUD FILTER - LIGHTWEIGHT OPEN3D VERSION ===
            ✅ STATUS: Fully functional
            🎯 FEATURES: All DB filtering operations available
            🚀 Optimized: Open3D only - no sklearn dependencies
            SERPENS SETUP:
            - filter_mode: "quick", "aggressive", "gentle", etc.
            - filter_obj_name: Object name (empty for active)
            - filter_eps: DBSCAN radius
            - filter_min_points: Minimum cluster size
            - filter_auto_eps: Auto-estimate eps
            - filter_show_timing: Show timing information (True/False)
            Main Function: run_point_cloud_filter()
            Debug Function: test_quick_filter()
                """)
            else:
                print("""
            === POINT CLOUD FILTER - OPEN3D DISABLED ===
            ❌ STATUS: Not functional
            ⚠️  REASON: Open3D not installed
            SOLUTION:
            1. Add Open3D wheels to your addon
            2. Update blender_manifest.toml 
            3. Restart Blender
            CURRENT FUNCTIONS: All disabled safely
                """)
            if (filter_result_object == None):
                pass
            else:
                input_object = filter_result_object
                # Input Variables
                #input_object = None  # bpy.types.Object - The object to select and make active
                deselect_all_first = True  # bool - Whether to deselect all objects first
                # Output Variables  
                success = False  # bool - Whether the operation was successful
                error_message = ""  # str - Error message if operation failed

                def safe_deselect_all():
                    """
                    Safely deselect all objects, only touching objects that are in the current view layer
                    """
                    try:
                        # Get current view layer
                        view_layer = bpy.context.view_layer
                        # Only deselect objects that are actually in the current view layer
                        for obj in bpy.context.selected_objects[:]:  # Create a copy of the list to avoid modification during iteration
                            # Check if object is in current view layer
                            if obj.name in view_layer.objects:
                                obj.select_set(False)
                        # Clear active object safely
                        if view_layer.objects.active and view_layer.objects.active.name in view_layer.objects:
                            view_layer.objects.active = None
                        return True, ""
                    except Exception as e:
                        return False, f"Error during deselect all: {str(e)}"

                def select_and_activate_object(obj):
                    """
                    Select and activate the given object, making it visible first if needed
                    """
                    if not obj:
                        return False, "No object provided"
                    try:
                        view_layer = bpy.context.view_layer
                        # Check if object exists in current view layer
                        if obj.name not in view_layer.objects:
                            return False, f"Object '{obj.name}' is not in the current view layer or is excluded"
                        # Get the object from the view layer (this ensures we have the right reference)
                        view_layer_obj = view_layer.objects[obj.name]
                        # Make object visible if it's hidden
                        visibility_changes = []
                        # Unhide in viewport
                        if obj.hide_viewport:
                            obj.hide_viewport = False
                            visibility_changes.append("viewport")
                        # Unhide in view layer
                        if view_layer_obj.hide_get():
                            view_layer_obj.hide_set(False)
                            visibility_changes.append("view layer")
                        # Try to unhide parent collections if they're hidden
                        for collection in obj.users_collection:
                            if collection.hide_viewport:
                                collection.hide_viewport = False
                                visibility_changes.append(f"collection '{collection.name}'")
                        # Select the object
                        view_layer_obj.select_set(True)
                        # Make it active
                        view_layer.objects.active = view_layer_obj
                        success_msg = f"Successfully selected and activated '{obj.name}'"
                        if visibility_changes:
                            success_msg += f" (made visible in: {', '.join(visibility_changes)})"
                        return True, success_msg
                    except Exception as e:
                        return False, f"Error selecting object '{obj.name}': {str(e)}"
                # Main execution
                if input_object:
                    # Deselect all first if requested
                    if deselect_all_first:
                        deselect_success, deselect_error = safe_deselect_all()
                        if not deselect_success:
                            success = False
                            error_message = deselect_error
                            print(error_message)
                        else:
                            print("All objects deselected safely")
                    # Select and activate the input object (only if deselect was successful or not requested)
                    if not deselect_all_first or deselect_success:
                        success, error_message = select_and_activate_object(input_object)
                        print(error_message)
                else:
                    success = False
                    error_message = "No input object provided"
                    print(error_message)
                bpy.context.view_layer.objects.active.name = 'AutoCrop_' + bpy.context.view_layer.objects.active.name
                bpy.context.view_layer.objects.active.hide_render = True
                if self.sna_create_convex_hull_object:
                    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
                    bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
                    bpy.ops.mesh.convex_hull('INVOKE_DEFAULT', )
                    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        else:
            self.report({'ERROR'}, message='Open3D not available')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        col_AFE45 = layout.column(heading='', align=False)
        col_AFE45.alert = False
        col_AFE45.enabled = True
        col_AFE45.active = True
        col_AFE45.use_property_split = False
        col_AFE45.use_property_decorate = False
        col_AFE45.scale_x = 1.0
        col_AFE45.scale_y = 1.0
        col_AFE45.alignment = 'Expand'.upper()
        col_AFE45.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_E9B63 = col_AFE45.box()
        box_E9B63.alert = False
        box_E9B63.enabled = True
        box_E9B63.active = True
        box_E9B63.use_property_split = False
        box_E9B63.use_property_decorate = False
        box_E9B63.alignment = 'Expand'.upper()
        box_E9B63.scale_x = 1.0
        box_E9B63.scale_y = 1.0
        if not True: box_E9B63.operator_context = "EXEC_DEFAULT"
        box_E9B63.label(text="There is no 'one size fits all' setting.", icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_E9B63.label(text='You may need to play with different values.', icon_value=0)
        box_AC64A = col_AFE45.box()
        box_AC64A.alert = False
        box_AC64A.enabled = True
        box_AC64A.active = True
        box_AC64A.use_property_split = False
        box_AC64A.use_property_decorate = False
        box_AC64A.alignment = 'Expand'.upper()
        box_AC64A.scale_x = 1.0
        box_AC64A.scale_y = 1.0
        if not True: box_AC64A.operator_context = "EXEC_DEFAULT"
        row_A0C33 = box_AC64A.row(heading='', align=False)
        row_A0C33.alert = False
        row_A0C33.enabled = True
        row_A0C33.active = True
        row_A0C33.use_property_split = False
        row_A0C33.use_property_decorate = False
        row_A0C33.scale_x = 1.0
        row_A0C33.scale_y = 1.0
        row_A0C33.alignment = 'Expand'.upper()
        row_A0C33.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A0C33.label(text='Mode', icon_value=0)
        row_A0C33.prop(self, 'sna_filter_mode', text=self.sna_filter_mode, icon_value=0, emboss=True, expand=True)
        box_AC64A.prop(self, 'sna_filter_epsilon', text='Filter Epsilon', icon_value=0, emboss=True, slider=True)
        box_AC64A.prop(self, 'sna_filter_min_points', text='Filter Min Points', icon_value=0, emboss=True)
        box_AC64A.prop(self, 'sna_fast_mode', text='Filter Fast Mode (Less Accurate)', icon_value=0, emboss=True)
        box_AC64A.prop(self, 'sna_create_convex_hull_object', text='Create Convex Hull Object', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

