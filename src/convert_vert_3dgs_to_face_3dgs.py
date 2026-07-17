import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .align_active_values_to_x import sna_align_active_values_to_x_4CE1F
from .append_and_add_geo_nodes_function_execute import sna_append_and_add_geo_nodes_function_execute_6BCD7
from .move_modifier_index import sna_move_modifier_index_23126

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Convert_Vert_3Dgs_To_Face_3Dgs_E6635(bpy.types.Operator):
    bl_idname = "sna.dgs_render_convert_vert_3dgs_to_face_3dgs_e6635"
    bl_label = "3DGS Render: Convert Vert 3DGS to Face 3DGS"
    bl_description = "Convert the active Vert Imported 3DGS mesh to a Face based 3DGS object and apply transforms."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        target_obj_name = bpy.context.view_layer.objects.active.name
        import numpy as np
        #target_obj_name = ""  # Input: name of the mesh 3DGS object to process
        SCALE_ATTRIBUTES = ("scale_0", "scale_1", "scale_2")
        ROTATION_ATTRIBUTES = ("rot_0", "rot_1", "rot_2", "rot_3")
        DC_ATTRIBUTES = ("f_dc_0", "f_dc_1", "f_dc_2")
        SUPPORTED_SH_COEFFS = {1: 0, 4: 1, 9: 2, 16: 3}
        SH_C0 = 0.28209479177387814
        SH_C1 = 0.4886025119029199
        SH_C2_0 = 1.0925484305920792
        SH_C2_1 = -1.0925484305920792
        SH_C2_2 = 0.31539156525252005
        SH_C2_3 = -1.0925484305920792
        SH_C2_4 = 0.5462742152960396
        SH_C3_0 = -0.5900435899266435
        SH_C3_1 = 2.890611442640554
        SH_C3_2 = -0.4570457994644658
        SH_C3_3 = 0.3731763325901154
        SH_C3_4 = -0.4570457994644658
        SH_C3_5 = 1.445305721320277
        SH_C3_6 = -0.5900435899266435

        def get_target_mesh_object(obj_name):
            obj_name = str(obj_name).strip()
            if not obj_name:
                raise ValueError("target_obj_name is empty. Provide the mesh object name to process.")
            obj = bpy.data.objects.get(obj_name)
            if not obj:
                raise ValueError(f"Object '{obj_name}' was not found.")
            if obj.type != "MESH":
                raise ValueError(f"Object '{obj.name}' is not a mesh.")
            if not hasattr(obj.data, "attributes"):
                raise ValueError(f"Object '{obj.name}' does not have attribute data.")
            return obj

        def get_float_attribute(obj, attr_name):
            if attr_name not in obj.data.attributes:
                raise ValueError(f"Attribute '{attr_name}' not found on object '{obj.name}'.")
            attr = obj.data.attributes[attr_name]
            if attr.data_type != "FLOAT":
                raise ValueError(
                    f"Attribute '{attr_name}' must be FLOAT, found {attr.data_type}."
                )
            values = np.empty(len(attr.data), dtype=np.float32)
            attr.data.foreach_get("value", values)
            return attr, values

        def get_face_quad_vertex_groups(mesh_data):
            """Return one disconnected 4-vertex group per quad face for face-based gaussian meshes."""
            num_polygons = len(mesh_data.polygons)
            if num_polygons == 0:
                return None
            face_vertex_indices = np.empty((num_polygons, 4), dtype=np.int32)
            for poly_index, poly in enumerate(mesh_data.polygons):
                poly_vertices = tuple(poly.vertices)
                if len(poly_vertices) != 4:
                    return None
                face_vertex_indices[poly_index] = poly_vertices
            if np.unique(face_vertex_indices).size != len(mesh_data.vertices):
                return None
            return face_vertex_indices

        def collapse_attribute_values(data_array, face_vertex_indices, expected_vertex_count, attr_name):
            """Collapse per-vertex data to one logical value per disconnected quad when needed."""
            if face_vertex_indices is None:
                return data_array.astype(np.float64)
            if len(data_array) == expected_vertex_count:
                return data_array[face_vertex_indices].mean(axis=1).astype(np.float64)
            if len(data_array) == len(face_vertex_indices):
                return data_array.astype(np.float64)
            raise ValueError(
                f"Attribute '{attr_name}' has {len(data_array)} values, expected {expected_vertex_count} vertices "
                f"or {len(face_vertex_indices)} face islands."
            )

        def expand_attribute_values(logical_values, raw_length, face_vertex_indices, expected_vertex_count, attr_name):
            """Expand logical splat values back to the attribute storage domain."""
            logical_values = np.asarray(logical_values, dtype=np.float64)
            if face_vertex_indices is None:
                if len(logical_values) != raw_length:
                    raise ValueError(
                        f"Attribute '{attr_name}' expects {raw_length} values, got {len(logical_values)}."
                    )
                return logical_values.astype(np.float32)
            if raw_length == len(face_vertex_indices):
                if len(logical_values) != len(face_vertex_indices):
                    raise ValueError(
                        f"Attribute '{attr_name}' expects {len(face_vertex_indices)} logical values, got {len(logical_values)}."
                    )
                return logical_values.astype(np.float32)
            if raw_length == expected_vertex_count:
                if len(logical_values) != len(face_vertex_indices):
                    raise ValueError(
                        f"Attribute '{attr_name}' expects {len(face_vertex_indices)} logical values for face expansion, "
                        f"got {len(logical_values)}."
                    )
                expanded = np.empty(expected_vertex_count, dtype=np.float64)
                expanded[face_vertex_indices] = logical_values[:, None]
                return expanded.astype(np.float32)
            raise ValueError(
                f"Attribute '{attr_name}' has unsupported storage length {raw_length} for face-based expansion."
            )

        def get_float_attribute_context(obj, attr_name, face_vertex_indices=None, expected_vertex_count=None):
            attr, raw_values = get_float_attribute(obj, attr_name)
            if expected_vertex_count is None:
                expected_vertex_count = len(obj.data.vertices)
            logical_values = collapse_attribute_values(
                raw_values,
                face_vertex_indices,
                expected_vertex_count,
                attr_name,
            )
            return {
                "attr": attr,
                "attr_name": attr_name,
                "raw_length": len(raw_values),
                "logical_values": logical_values,
            }

        def set_attribute_context_values(context, logical_values, face_vertex_indices=None, expected_vertex_count=None):
            if expected_vertex_count is None:
                raise ValueError("expected_vertex_count is required when writing attribute values.")
            values = expand_attribute_values(
                logical_values,
                context["raw_length"],
                face_vertex_indices,
                expected_vertex_count,
                context["attr_name"],
            )
            context["attr"].data.foreach_set("value", values)

        def get_rotation_attribute_data(obj, face_vertex_indices=None, expected_vertex_count=None):
            attrs = []
            values = []
            for attr_name in ROTATION_ATTRIBUTES:
                attr_context = get_float_attribute_context(
                    obj,
                    attr_name,
                    face_vertex_indices=face_vertex_indices,
                    expected_vertex_count=expected_vertex_count,
                )
                attrs.append(attr_context)
                values.append(attr_context["logical_values"])
            quaternions = np.stack(values, axis=1)
            norms = np.linalg.norm(quaternions, axis=1, keepdims=True)
            norms = np.maximum(norms, 1e-12)
            quaternions /= norms
            return attrs, quaternions

        def get_scale_attribute_data(obj, face_vertex_indices=None, expected_vertex_count=None):
            attrs = []
            values = []
            for attr_name in SCALE_ATTRIBUTES:
                attr_context = get_float_attribute_context(
                    obj,
                    attr_name,
                    face_vertex_indices=face_vertex_indices,
                    expected_vertex_count=expected_vertex_count,
                )
                attrs.append(attr_context)
                values.append(attr_context["logical_values"])
            log_scales = np.stack(values, axis=1)
            return attrs, log_scales

        def quaternions_to_rotation_matrices(quaternions):
            w = quaternions[:, 0]
            x = quaternions[:, 1]
            y = quaternions[:, 2]
            z = quaternions[:, 3]
            xx = x * x
            yy = y * y
            zz = z * z
            xy = x * y
            xz = x * z
            yz = y * z
            wx = w * x
            wy = w * y
            wz = w * z
            matrices = np.empty((len(quaternions), 3, 3), dtype=np.float64)
            matrices[:, 0, 0] = 1.0 - 2.0 * (yy + zz)
            matrices[:, 0, 1] = 2.0 * (xy - wz)
            matrices[:, 0, 2] = 2.0 * (xz + wy)
            matrices[:, 1, 0] = 2.0 * (xy + wz)
            matrices[:, 1, 1] = 1.0 - 2.0 * (xx + zz)
            matrices[:, 1, 2] = 2.0 * (yz - wx)
            matrices[:, 2, 0] = 2.0 * (xz - wy)
            matrices[:, 2, 1] = 2.0 * (yz + wx)
            matrices[:, 2, 2] = 1.0 - 2.0 * (xx + yy)
            return matrices

        def rotation_matrices_to_quaternions(matrices):
            quaternions = np.zeros((len(matrices), 4), dtype=np.float64)
            trace = matrices[:, 0, 0] + matrices[:, 1, 1] + matrices[:, 2, 2]
            mask = trace > 0.0
            if np.any(mask):
                s = np.sqrt(trace[mask] + 1.0) * 2.0
                quaternions[mask, 0] = 0.25 * s
                quaternions[mask, 1] = (matrices[mask, 2, 1] - matrices[mask, 1, 2]) / s
                quaternions[mask, 2] = (matrices[mask, 0, 2] - matrices[mask, 2, 0]) / s
                quaternions[mask, 3] = (matrices[mask, 1, 0] - matrices[mask, 0, 1]) / s
            mask_x = (~mask) & (matrices[:, 0, 0] > matrices[:, 1, 1]) & (matrices[:, 0, 0] > matrices[:, 2, 2])
            if np.any(mask_x):
                s = np.sqrt(1.0 + matrices[mask_x, 0, 0] - matrices[mask_x, 1, 1] - matrices[mask_x, 2, 2]) * 2.0
                quaternions[mask_x, 0] = (matrices[mask_x, 2, 1] - matrices[mask_x, 1, 2]) / s
                quaternions[mask_x, 1] = 0.25 * s
                quaternions[mask_x, 2] = (matrices[mask_x, 0, 1] + matrices[mask_x, 1, 0]) / s
                quaternions[mask_x, 3] = (matrices[mask_x, 0, 2] + matrices[mask_x, 2, 0]) / s
            mask_y = (~mask) & (~mask_x) & (matrices[:, 1, 1] > matrices[:, 2, 2])
            if np.any(mask_y):
                s = np.sqrt(1.0 + matrices[mask_y, 1, 1] - matrices[mask_y, 0, 0] - matrices[mask_y, 2, 2]) * 2.0
                quaternions[mask_y, 0] = (matrices[mask_y, 0, 2] - matrices[mask_y, 2, 0]) / s
                quaternions[mask_y, 1] = (matrices[mask_y, 0, 1] + matrices[mask_y, 1, 0]) / s
                quaternions[mask_y, 2] = 0.25 * s
                quaternions[mask_y, 3] = (matrices[mask_y, 1, 2] + matrices[mask_y, 2, 1]) / s
            mask_z = (~mask) & (~mask_x) & (~mask_y)
            if np.any(mask_z):
                s = np.sqrt(1.0 + matrices[mask_z, 2, 2] - matrices[mask_z, 0, 0] - matrices[mask_z, 1, 1]) * 2.0
                quaternions[mask_z, 0] = (matrices[mask_z, 1, 0] - matrices[mask_z, 0, 1]) / s
                quaternions[mask_z, 1] = (matrices[mask_z, 0, 2] + matrices[mask_z, 2, 0]) / s
                quaternions[mask_z, 2] = (matrices[mask_z, 1, 2] + matrices[mask_z, 2, 1]) / s
                quaternions[mask_z, 3] = 0.25 * s
            norms = np.linalg.norm(quaternions, axis=1, keepdims=True)
            norms = np.maximum(norms, 1e-12)
            quaternions /= norms
            negative_w = quaternions[:, 0] < 0.0
            quaternions[negative_w] *= -1.0
            return quaternions

        def get_object_linear_transform(obj):
            linear_transform = np.array(obj.matrix_basis.to_3x3(), dtype=np.float64)
            _, rotation_quat, _ = obj.matrix_basis.decompose()
            rotation_matrix = np.array(rotation_quat.to_matrix(), dtype=np.float64)
            return linear_transform, rotation_matrix, rotation_quat

        def bake_scale_and_rotation_attributes(obj, linear_transform, face_vertex_indices=None, expected_vertex_count=None):
            rotation_attrs, quaternions = get_rotation_attribute_data(
                obj,
                face_vertex_indices=face_vertex_indices,
                expected_vertex_count=expected_vertex_count,
            )
            scale_attrs, log_scales = get_scale_attribute_data(
                obj,
                face_vertex_indices=face_vertex_indices,
                expected_vertex_count=expected_vertex_count,
            )
            scales = np.exp(log_scales)
            rotation_mats = quaternions_to_rotation_matrices(quaternions)
            scale_sq = np.zeros((len(scales), 3, 3), dtype=np.float64)
            scale_sq[:, 0, 0] = scales[:, 0] ** 2
            scale_sq[:, 1, 1] = scales[:, 1] ** 2
            scale_sq[:, 2, 2] = scales[:, 2] ** 2
            # Standard 3DGS covariance convention: Sigma = R * diag(scale^2) * R^T
            covariances = np.matmul(rotation_mats, np.matmul(scale_sq, np.transpose(rotation_mats, (0, 2, 1))))
            transformed_covariances = np.matmul(
                linear_transform[None, :, :],
                np.matmul(covariances, linear_transform.T[None, :, :]),
            )
            eigenvalues, eigenvectors = np.linalg.eigh(transformed_covariances)
            order = np.argsort(eigenvalues, axis=1)[:, ::-1]
            sorted_values = np.take_along_axis(eigenvalues, order, axis=1)
            sorted_vectors = np.take_along_axis(eigenvectors, order[:, None, :], axis=2)
            dets = np.linalg.det(sorted_vectors)
            flip_mask = dets < 0.0
            sorted_vectors[flip_mask, :, 2] *= -1.0
            new_quaternions = rotation_matrices_to_quaternions(sorted_vectors)
            new_scales = np.sqrt(np.maximum(sorted_values, 1e-20))
            new_log_scales = np.log(new_scales)
            for attr_index, attr_context in enumerate(rotation_attrs):
                set_attribute_context_values(
                    attr_context,
                    new_quaternions[:, attr_index],
                    face_vertex_indices=face_vertex_indices,
                    expected_vertex_count=expected_vertex_count,
                )
            for attr_index, attr_context in enumerate(scale_attrs):
                set_attribute_context_values(
                    attr_context,
                    new_log_scales[:, attr_index],
                    face_vertex_indices=face_vertex_indices,
                    expected_vertex_count=expected_vertex_count,
                )
            return len(new_quaternions)

        def fibonacci_sphere(sample_count):
            indices = np.arange(sample_count, dtype=np.float64) + 0.5
            phi = np.arccos(1.0 - 2.0 * indices / sample_count)
            theta = math.pi * (1.0 + math.sqrt(5.0)) * indices
            x = np.cos(theta) * np.sin(phi)
            y = np.sin(theta) * np.sin(phi)
            z = np.cos(phi)
            return np.stack([x, y, z], axis=1)

        def evaluate_real_sh_basis(directions):
            x = directions[:, 0]
            y = directions[:, 1]
            z = directions[:, 2]
            xx = x * x
            yy = y * y
            zz = z * z
            xy = x * y
            yz = y * z
            xz = x * z
            basis = np.empty((len(directions), 16), dtype=np.float64)
            basis[:, 0] = SH_C0
            basis[:, 1] = -SH_C1 * y
            basis[:, 2] = SH_C1 * z
            basis[:, 3] = -SH_C1 * x
            basis[:, 4] = SH_C2_0 * xy
            basis[:, 5] = SH_C2_1 * yz
            basis[:, 6] = SH_C2_2 * (2.0 * zz - xx - yy)
            basis[:, 7] = SH_C2_3 * xz
            basis[:, 8] = SH_C2_4 * (xx - yy)
            basis[:, 9] = SH_C3_0 * y * (3.0 * xx - yy)
            basis[:, 10] = SH_C3_1 * xy * z
            basis[:, 11] = SH_C3_2 * y * (4.0 * zz - xx - yy)
            basis[:, 12] = SH_C3_3 * z * (2.0 * zz - 3.0 * xx - 3.0 * yy)
            basis[:, 13] = SH_C3_4 * x * (4.0 * zz - xx - yy)
            basis[:, 14] = SH_C3_5 * z * (xx - yy)
            basis[:, 15] = SH_C3_6 * x * (xx - 3.0 * yy)
            return basis

        def build_sh_rotation_matrix(rotation_matrix, sh_degree):
            total_coeffs = (sh_degree + 1) ** 2
            if total_coeffs == 1:
                return np.eye(1, dtype=np.float64)
            sample_dirs = fibonacci_sphere(256)
            rotated_dirs = sample_dirs @ rotation_matrix
            full_basis = evaluate_real_sh_basis(sample_dirs)
            rotated_basis = evaluate_real_sh_basis(rotated_dirs)
            rotation_matrix_full = np.zeros((total_coeffs, total_coeffs), dtype=np.float64)
            rotation_matrix_full[0, 0] = 1.0
            degree_offsets = {
                1: (1, 4),
                2: (4, 9),
                3: (9, 16),
            }
            for degree in range(1, sh_degree + 1):
                start, end = degree_offsets[degree]
                basis_block = full_basis[:, start:end]
                rotated_block = rotated_basis[:, start:end]
                solved_block, _, _, _ = np.linalg.lstsq(basis_block, rotated_block, rcond=None)
                rotation_matrix_full[start:end, start:end] = solved_block
            return rotation_matrix_full

        def get_sh_attribute_layout(obj, face_vertex_indices=None, expected_vertex_count=None):
            dc_attrs = []
            for attr_name in DC_ATTRIBUTES:
                attr_context = get_float_attribute_context(
                    obj,
                    attr_name,
                    face_vertex_indices=face_vertex_indices,
                    expected_vertex_count=expected_vertex_count,
                )
                dc_attrs.append(attr_context)
            f_rest_fields = [attr.name for attr in obj.data.attributes if attr.name.startswith("f_rest_")]
            f_rest_fields = sorted(f_rest_fields, key=lambda name: int(name.split("_")[-1]))
            if not f_rest_fields:
                return None, 0
            if len(f_rest_fields) % 3 != 0:
                raise ValueError("f_rest attributes are incomplete. Expected 3 matching channels.")
            coeffs_per_channel = 1 + (len(f_rest_fields) // 3)
            if coeffs_per_channel not in SUPPORTED_SH_COEFFS:
                raise ValueError(
                    f"Unsupported SH layout on '{obj.name}'. Found {coeffs_per_channel} coeffs per channel."
                )
            channel_rest_count = coeffs_per_channel - 1
            channel_attrs = []
            for channel_index in range(3):
                attrs = []
                values = []
                dc_context = dc_attrs[channel_index]
                attrs.append(dc_context)
                values.append(dc_context["logical_values"])
                start = channel_index * channel_rest_count
                end = start + channel_rest_count
                for attr_name in f_rest_fields[start:end]:
                    attr_context = get_float_attribute_context(
                        obj,
                        attr_name,
                        face_vertex_indices=face_vertex_indices,
                        expected_vertex_count=expected_vertex_count,
                    )
                    attrs.append(attr_context)
                    values.append(attr_context["logical_values"])
                channel_attrs.append((attrs, np.stack(values, axis=1)))
            sh_degree = SUPPORTED_SH_COEFFS[coeffs_per_channel]
            return channel_attrs, sh_degree

        def bake_sh_attributes(obj, rotation_matrix, face_vertex_indices=None, expected_vertex_count=None):
            channel_data, sh_degree = get_sh_attribute_layout(
                obj,
                face_vertex_indices=face_vertex_indices,
                expected_vertex_count=expected_vertex_count,
            )
            if sh_degree == 0:
                return 0
            sh_rotation = build_sh_rotation_matrix(rotation_matrix, sh_degree)
            for attrs, coeffs in channel_data:
                rotated_coeffs = coeffs @ sh_rotation.T
                for attr_index, attr_context in enumerate(attrs):
                    set_attribute_context_values(
                        attr_context,
                        rotated_coeffs[:, attr_index],
                        face_vertex_indices=face_vertex_indices,
                        expected_vertex_count=expected_vertex_count,
                    )
            return sh_degree

        def apply_object_rotation_and_scale(obj):
            original_mode = obj.mode
            view_layer = bpy.context.view_layer
            original_active = view_layer.objects.active
            originally_selected = list(bpy.context.selected_objects)
            try:
                if original_mode != "OBJECT":
                    bpy.ops.object.mode_set(mode="OBJECT")
                for selected_obj in originally_selected:
                    selected_obj.select_set(False)
                obj.select_set(True)
                view_layer.objects.active = obj
                bpy.ops.object.transform_apply(
                    location=False,
                    rotation=True,
                    scale=True,
                )
            finally:
                obj.select_set(False)
                for selected_obj in originally_selected:
                    if selected_obj and selected_obj.name in bpy.data.objects:
                        selected_obj.select_set(True)
                if original_active and original_active.name in bpy.data.objects:
                    view_layer.objects.active = original_active
                if original_mode != "OBJECT":
                    try:
                        bpy.ops.object.mode_set(mode=original_mode)
                    except Exception:
                        pass

        def main():
            obj = get_target_mesh_object(target_obj_name)
            expected_vertex_count = len(obj.data.vertices)
            face_vertex_indices = get_face_quad_vertex_groups(obj.data)
            if face_vertex_indices is not None:
                print(
                    f"Detected face-based gaussian mesh '{obj.name}', collapsing "
                    f"{expected_vertex_count:,} quad vertices to {len(face_vertex_indices):,} logical splats for transform bake."
                )
            linear_transform, rotation_matrix, rotation_quat = get_object_linear_transform(obj)
            splat_count = bake_scale_and_rotation_attributes(
                obj,
                linear_transform,
                face_vertex_indices=face_vertex_indices,
                expected_vertex_count=expected_vertex_count,
            )
            sh_degree = bake_sh_attributes(
                obj,
                rotation_matrix,
                face_vertex_indices=face_vertex_indices,
                expected_vertex_count=expected_vertex_count,
            )
            apply_object_rotation_and_scale(obj)
            print(f"Baked scale/rotation into {splat_count:,} splats on '{obj.name}'.")
            if sh_degree > 0:
                print(f"Rotated SH attributes up to degree {sh_degree}.")
            else:
                print("No higher SH attributes found to rotate.")
            print(
                "Applied object rotation/scale to mesh and reset object transforms "
                f"(object rotation quaternion was {rotation_quat.w:.6f}, {rotation_quat.x:.6f}, "
                f"{rotation_quat.y:.6f}, {rotation_quat.z:.6f})."
            )
            print("3DGS transform bake completed.")
        main()
        bpy.ops.object.transform_apply('INVOKE_DEFAULT', location=True)
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
            bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], )
        bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] = 'face'
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Render_To_Faces_GN', 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active)
        sna_align_active_values_to_x_4CE1F()
        sna_move_modifier_index_23126(bpy.context.view_layer.objects.active, 'KIRI_3DGS_Render_GN', 0)
        bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_3DGS_Render_GN')
        sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Render_GN', 'KIRI_3DGS_Render_GN', bpy.context.view_layer.objects.active)
        sna_move_modifier_index_23126(bpy.context.view_layer.objects.active, 'KIRI_3DGS_Render_GN', 0)
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_in_editmode = True
            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_on_cage = True
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
        if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
            pass
        else:
            before_data = list(bpy.data.materials)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V5.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
            appended_79374 = None if not new_data else new_data[0]
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
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = bpy.context.view_layer.objects.active.sna_dgs_object_properties.cam_update
        bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
