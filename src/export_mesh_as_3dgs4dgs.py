import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .apply_all_modifiers_for_export import sna_apply_all_modifiers_for_export_B90C0
from .duplicate_object import sna_duplicate_object_ED1F0
from .. import dgs_render__export

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Export_Mesh_As_3Dgs4Dgs_Ce2F7(bpy.types.Operator):
    bl_idname = "sna.dgs_render_export_mesh_as_3dgs4dgs_ce2f7"
    bl_label = "3DGS Render: Export Mesh As 3DGS/4DGS"
    bl_description = "Applies scale and rotation transforms, applies color modifiers and exports the active object as a 3DGS .ply"
    bl_options = {"REGISTER", "UNDO"}
    sna_send_to_world_centre: bpy.props.BoolProperty(name='Send to World Centre', description='', options={'HIDDEN'}, default=True)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if os.path.isdir(bpy.context.scene.sna_dgs_scene_properties.export_output_path):
            if (bpy.context.view_layer.objects.active == None):
                self.report({'ERROR'}, message='No Active Object')
            else:
                if (len(bpy.context.view_layer.objects.selected) > 1):
                    self.report({'ERROR'}, message='Only select 1 object please.')
                else:
                    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Write F_DC_And_Merge' in bpy.context.view_layer.objects.active.modifiers):
                        dgs_render__export['sna_export_base_object'] = bpy.context.view_layer.objects.active
                        if self.sna_send_to_world_centre:
                            bpy.context.view_layer.objects.active.location = (0.0, 0.0, 0.0)
                        if bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == "3DGS":
                            new_object_name_0_52da7 = sna_duplicate_object_ED1F0(dgs_render__export['sna_export_base_object'].name)
                            dgs_render__export['sna_export_temp_object'] = bpy.data.objects[new_object_name_0_52da7]
                            dgs_render__export['sna_export_temp_object'].select_set(state=True, view_layer=bpy.context.view_layer, )
                            dgs_render__export['sna_export_temp_object'].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = True
                            dgs_render__export['sna_export_temp_object'].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = True

                            def delayed_C77D9():
                                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                                    dgs_render__export['sna_export_base_object'].sna_dgs_object_properties.update_mode = 'Disable Camera Updates'
                                sna_apply_all_modifiers_for_export_B90C0(dgs_render__export['sna_export_temp_object'].name)
                                target_obj_name = dgs_render__export['sna_export_temp_object'].name
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

                                def delayed_5B08A():
                                    bpy.ops.wm.ply_export(filepath=os.path.join(bpy.context.scene.sna_dgs_scene_properties.export_output_path,dgs_render__export['sna_export_base_object'].name + bpy.context.scene.sna_dgs_scene_properties.export_suffix + '.ply'), export_selected_objects=True, export_attributes=True)
                                    bpy.data.objects.remove(object=dgs_render__export['sna_export_temp_object'], do_unlink=True, do_id_user=True, do_ui_user=True, )
                                bpy.app.timers.register(delayed_5B08A, first_interval=0.10000000149011612)
                            bpy.app.timers.register(delayed_C77D9, first_interval=0.10000000149011612)
                        elif bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == "4DGS":
                            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                                bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
                                bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode = 'Disable Camera Updates'
                            if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Animate_GN' in bpy.context.view_layer.objects.active.modifiers):
                                if bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN'].show_viewport:
                                    if ((bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 1) or (bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 2)):
                                        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] = 0
                            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = True
                            bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = True
                            bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
                            if bpy.context and bpy.context.screen:
                                for a in bpy.context.screen.areas:
                                    a.tag_redraw()
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
                            source_obj_name = bpy.context.view_layer.objects.active.name
                            start_frame = bpy.context.scene.frame_start
                            end_frame = bpy.context.scene.frame_end
                            RIG_BAKED_UPDATE_MODE = bpy.context.scene.sna_dgs_scene_properties.r2_render_rig_cache_mode
                            output_object_list = None
                            import inspect
                            import sys
                            #source_obj_name = ""  # Input: source mesh object name; blank = active object
                            #start_frame = None  # Input: first frame to duplicate; blank/None = scene frame_start
                            #end_frame = None  # Input: last frame to duplicate; blank/None = scene frame_end
                            frame_step = 1  # Input: duplicate every Nth frame
                            #RIG_BAKED_UPDATE_MODE = "None"  # Input: None, Enabled Baked, or All Baked
                            RIG_BAKED_ENABLED_PROP_NAME = "rig_baked_render_enabled"  # Input: source object custom property checked when mode is Enabled Baked
                            MISSING_BAKED_FRAME_MODE = "Keep Current"  # Input: Keep Current, Skip Frame, Restore Rest, or Error
                            proxy_binding_utils_path = "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"  # Input: full path to proxy_binding_utils.py
                            raise_on_error = False  # Input: when False, missing/corrupt baked data reports softly instead of raising
                            output_object_list = []
                            success = False
                            status_message = ""
                            generated_count = 0
                            processed_frame_count = 0
                            skipped_frame_count = 0
                            failed_frame_count = 0
                            rig_applied_frame_count = 0
                            rig_missing_frame_count = 0
                            used_baked_rig_updates = False

                            def load_proxy_binding_utils():
                                module_name = "proxy_binding_utils"
                                candidate_paths = []
                                override_path = str(proxy_binding_utils_path).strip()
                                if override_path:
                                    candidate_paths.append(os.path.abspath(bpy.path.abspath(override_path)))
                                file_hint = globals().get("__file__") or inspect.getsourcefile(lambda: 0)
                                if file_hint and os.path.exists(file_hint):
                                    script_dir = os.path.dirname(os.path.abspath(file_hint))
                                    candidate_paths.append(os.path.join(script_dir, "proxy_binding_utils.py"))
                                    candidate_paths.append(os.path.join(script_dir, "..", "rigging", "proxy_binding_utils.py"))
                                cwd = os.getcwd()
                                candidate_paths.append(os.path.join(cwd, "proxy_binding_utils.py"))
                                candidate_paths.append(os.path.join(cwd, "rigging", "proxy_binding_utils.py"))
                                blend_dir = bpy.path.abspath("//")
                                if blend_dir:
                                    candidate_paths.append(os.path.join(blend_dir, "proxy_binding_utils.py"))
                                    candidate_paths.append(os.path.join(blend_dir, "rigging", "proxy_binding_utils.py"))
                                checked_paths = set()
                                for module_path in candidate_paths:
                                    normalized = os.path.normpath(module_path)
                                    if normalized in checked_paths:
                                        continue
                                    checked_paths.add(normalized)
                                    if os.path.exists(normalized):
                                        spec = importlib.util.spec_from_file_location(module_name, normalized)
                                        module = importlib.util.module_from_spec(spec)
                                        spec.loader.exec_module(module)
                                        sys.modules[module_name] = module
                                        return module
                                text_name_candidates = (
                                    "proxy_binding_utils.py",
                                    "Rigging - proxy_binding_utils.py",
                                    "proxy_binding_utils",
                                    "Rigging - proxy_binding_utils",
                                )
                                for text_name in text_name_candidates:
                                    text_block = bpy.data.texts.get(text_name)
                                    if text_block:
                                        module = types.ModuleType(module_name)
                                        module.__file__ = text_name
                                        exec(compile(text_block.as_string(), text_name, "exec"), module.__dict__)
                                        sys.modules[module_name] = module
                                        return module
                                raise RuntimeError(
                                    "Could not find proxy_binding_utils.py. Set 'proxy_binding_utils_path' to the helper file on disk "
                                    "or load proxy_binding_utils.py as a Blender text block."
                                )

                            def get_source_object():
                                obj_name = str(source_obj_name).strip()
                                if obj_name:
                                    obj = bpy.data.objects.get(obj_name)
                                    if obj is None:
                                        raise ValueError(f"Object '{obj_name}' not found.")
                                else:
                                    obj = bpy.context.view_layer.objects.active
                                    if obj is None:
                                        raise ValueError("No active object found and source_obj_name is blank.")
                                if obj.type != "MESH":
                                    raise ValueError(f"Object '{obj.name}' is not a mesh.")
                                return obj

                            def normalize_rig_baked_update_mode(value):
                                text = str(value).strip().lower()
                                if text in {"", "none"}:
                                    return "None"
                                if text in {"enabled baked", "enabled_baked", "enabled"}:
                                    return "Enabled Baked"
                                if text in {"all baked", "all_baked", "all"}:
                                    return "All Baked"
                                raise ValueError("RIG_BAKED_UPDATE_MODE must be None, Enabled Baked, or All Baked.")

                            def normalize_missing_baked_frame_mode(value):
                                text = str(value).strip().lower()
                                if text in {"", "keep current", "keep_current", "keep"}:
                                    return "Keep Current"
                                if text in {"skip frame", "skip_frame", "skip"}:
                                    return "Skip Frame"
                                if text in {"restore rest", "restore_rest", "rest"}:
                                    return "Restore Rest"
                                if text in {"error", "raise"}:
                                    return "Error"
                                raise ValueError(
                                    "MISSING_BAKED_FRAME_MODE must be Keep Current, Skip Frame, Restore Rest, or Error."
                                )

                            def resolve_frame_range(scene):
                                resolved_start = int(scene.frame_start if start_frame in (None, "") else start_frame)
                                resolved_end = int(scene.frame_end if end_frame in (None, "") else end_frame)
                                resolved_step = max(1, int(frame_step))
                                if resolved_end < resolved_start:
                                    raise ValueError("end_frame must be greater than or equal to start_frame.")
                                return resolved_start, resolved_end, resolved_step

                            def duplicate_evaluated_mesh(source_obj, collection, depsgraph, frame_number):
                                eval_obj = source_obj.evaluated_get(depsgraph)
                                new_mesh = bpy.data.meshes.new_from_object(eval_obj)
                                new_obj = bpy.data.objects.new(f"{source_obj.name}_baked_f{frame_number}", new_mesh)
                                new_obj.matrix_world = source_obj.matrix_world.copy()
                                collection.objects.link(new_obj)
                                return new_obj
                            scene = bpy.context.scene
                            collection = scene.collection
                            try:
                                source_obj = get_source_object()
                                rig_baked_update_mode = normalize_rig_baked_update_mode(RIG_BAKED_UPDATE_MODE)
                                missing_baked_frame_mode = normalize_missing_baked_frame_mode(MISSING_BAKED_FRAME_MODE)
                                resolved_start, resolved_end, resolved_step = resolve_frame_range(scene)
                                frame_numbers = list(range(resolved_start, resolved_end + 1, resolved_step))
                                print(f"Duplicating evaluated mesh '{source_obj.name}' for {len(frame_numbers)} frame(s)...")
                                print(
                                    f"Rig baked settings: Mode={rig_baked_update_mode}, "
                                    f"MissingFrame={missing_baked_frame_mode}, EnabledProp={RIG_BAKED_ENABLED_PROP_NAME}"
                                )
                                original_frame = int(scene.frame_current)
                                original_hide_viewport = bool(source_obj.hide_viewport)
                                depsgraph = bpy.context.evaluated_depsgraph_get()
                                proxy_utils = None
                                rig_should_apply = False
                                rig_paths = None
                                rig_metadata = None
                                rig_rest_state = None
                                original_3dgs_state = None
                                if rig_baked_update_mode != "None":
                                    proxy_utils = load_proxy_binding_utils()
                                    if rig_baked_update_mode == "Enabled Baked":
                                        rig_should_apply = bool(source_obj.get(RIG_BAKED_ENABLED_PROP_NAME, False))
                                    else:
                                        rig_should_apply = True
                                    if rig_should_apply:
                                        try:
                                            if not proxy_utils.check_mesh_has_gaussian_attributes(source_obj):
                                                raise proxy_utils.ProxyBindingError(
                                                    f"'{source_obj.name}' does not look like a valid mesh 3DGS object."
                                                )
                                            original_3dgs_state = proxy_utils.read_logical_gaussian_state(source_obj)
                                            rig_paths, rig_metadata, rig_rest_state, _ = proxy_utils.load_binding_package(source_obj)
                                            proxy_utils.validate_current_3dgs_object(source_obj, rig_metadata)
                                            used_baked_rig_updates = True
                                            print(f"Baked rig package found for '{source_obj.name}'.")
                                        except Exception as exc:
                                            used_baked_rig_updates = False
                                            rig_should_apply = False
                                            print(f"Rig baked updates disabled for '{source_obj.name}': {exc}")
                                            if raise_on_error:
                                                raise
                                    else:
                                        print(f"Rig baked updates not enabled for '{source_obj.name}'.")
                                try:
                                    if original_hide_viewport:
                                        source_obj.hide_viewport = False
                                    for frame_number in frame_numbers:
                                        scene.frame_set(frame_number)
                                        processed_frame_count += 1
                                        if rig_should_apply:
                                            bake_path = proxy_utils.bake_state_file_path(rig_paths["bake_dir"], frame_number)
                                            if os.path.exists(bake_path):
                                                state = proxy_utils.load_baked_state(rig_paths["bake_dir"], frame_number)
                                                proxy_utils.apply_bound_state(source_obj, state)
                                                rig_applied_frame_count += 1
                                            else:
                                                rig_missing_frame_count += 1
                                                if missing_baked_frame_mode == "Skip Frame":
                                                    skipped_frame_count += 1
                                                    print(
                                                        f"Skipping frame {frame_number}: no baked rig frame exists for '{source_obj.name}'."
                                                    )
                                                    continue
                                                if missing_baked_frame_mode == "Restore Rest":
                                                    proxy_utils.apply_bound_state(source_obj, rig_rest_state)
                                                    print(
                                                        f"Restored rest rig state for frame {frame_number} on '{source_obj.name}'."
                                                    )
                                                elif missing_baked_frame_mode == "Error":
                                                    raise proxy_utils.ProxyBindingError(
                                                        f"No baked rig frame exists for frame {frame_number} on '{source_obj.name}'."
                                                    )
                                                else:
                                                    print(
                                                        f"Keeping current rig state for frame {frame_number}: no baked rig frame exists "
                                                        f"for '{source_obj.name}'."
                                                    )
                                        bpy.context.view_layer.update()
                                        new_obj = duplicate_evaluated_mesh(source_obj, collection, depsgraph, frame_number)
                                        output_object_list.append(new_obj)
                                        generated_count += 1
                                    success = failed_frame_count == 0
                                    status_message = (
                                        f"Generated {generated_count} duplicate object(s) from '{source_obj.name}'. "
                                        f"Rig-applied frames: {rig_applied_frame_count}. "
                                        f"Skipped frames: {skipped_frame_count}. Missing baked frames: {rig_missing_frame_count}."
                                    )
                                    print(status_message)
                                finally:
                                    if original_3dgs_state is not None:
                                        try:
                                            proxy_utils.write_logical_gaussian_state(source_obj, original_3dgs_state)
                                        except Exception as restore_exc:
                                            print(f"Warning: failed to restore original 3DGS state on '{source_obj.name}': {restore_exc}")
                                    scene.frame_set(original_frame)
                                    source_obj.hide_viewport = original_hide_viewport
                                    bpy.context.view_layer.update()
                            except Exception as exc:
                                status_message = f"Export duplicate-per-frame failed: {exc}"
                                failed_frame_count = max(failed_frame_count, 1)
                                print(status_message)
                                if raise_on_error:
                                    raise
                            for i_4588B in range(len(output_object_list)):
                                input_object = output_object_list[i_4588B]
                                # --- Input Variables (For testing or Serpens integration) ---
                                #input_object = bpy.context.object  # The target object
                                deselect_all_first = True          # Clear selection before starting?
                                make_active = True                 # NEW: Toggle between just selecting or selecting + activating
                                # --- Output Variables ---
                                success = False
                                error_message = ""

                                def safe_deselect_all():
                                    try:
                                        view_layer = bpy.context.view_layer
                                        for obj in bpy.context.selected_objects[:]:
                                            if obj.name in view_layer.objects:
                                                obj.select_set(False)
                                        # Only clear active if we actually want to reset everything
                                        if view_layer.objects.active:
                                            view_layer.objects.active = None
                                        return True, ""
                                    except Exception as e:
                                        return False, f"Deselect error: {str(e)}"

                                def select_object_logic(obj, should_activate):
                                    if not obj:
                                        return False, "No object provided"
                                    try:
                                        view_layer = bpy.context.view_layer
                                        if obj.name not in view_layer.objects:
                                            return False, f"Object '{obj.name}' not in current view layer"
                                        # 1. Unhide Object
                                        if obj.hide_viewport:
                                            obj.hide_viewport = False
                                        view_layer_obj = view_layer.objects[obj.name]
                                        if view_layer_obj.hide_get():
                                            view_layer_obj.hide_set(False)
                                        # 2. Unhide Direct Parent Collections
                                        for col in obj.users_collection:
                                            if col.hide_viewport:
                                                col.hide_viewport = False
                                        # 3. Select 
                                        view_layer_obj.select_set(True)
                                        # 4. Conditionally Activate
                                        if should_activate:
                                            view_layer.objects.active = view_layer_obj
                                            msg = f"Selected and activated {obj.name}"
                                        else:
                                            msg = f"Selected {obj.name} (Active object remains {view_layer.objects.active})"
                                        return True, msg
                                    except Exception as e:
                                        return False, f"Selection error: {str(e)}"
                                # --- Execution Logic ---
                                # 1. Handle Deselection
                                if deselect_all_first:
                                    success, error_message = safe_deselect_all()
                                else:
                                    success = True # Skip deselect, proceed to selection
                                # 2. Handle Selection
                                if success:
                                    if input_object:
                                        success, error_message = select_object_logic(input_object, make_active)
                                    else:
                                        success = False
                                        error_message = "No input object provided"
                                print(f"Result -> Success: {success}, Message: {error_message}")
                                bpy.ops.wm.ply_export(filepath=os.path.join(bpy.context.scene.sna_dgs_scene_properties.export_output_path,dgs_render__export['sna_export_base_object'].name + '_frame_000' + str(int(bpy.context.scene.frame_start + i_4588B)) + '.ply'), export_selected_objects=True, export_attributes=True)
                            for i_C1E70 in range(len(output_object_list)):
                                bpy.data.objects.remove(object=output_object_list[i_C1E70], do_unlink=True, do_id_user=True, do_ui_user=True, )
                        else:
                            pass
                        bpy.context.view_layer.objects.active = dgs_render__export['sna_export_base_object']
                        dgs_render__export['sna_export_base_object'].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_viewport = False
                        dgs_render__export['sna_export_base_object'].modifiers['KIRI_3DGS_Write F_DC_And_Merge'].show_render = False
                        if (property_exists("dgs_render__export['sna_export_base_object'].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in dgs_render__export['sna_export_base_object'].modifiers):
                            dgs_render__export['sna_export_base_object'].sna_dgs_object_properties.update_mode = 'Enable Camera Updates'
                    else:
                        self.report({'ERROR'}, message='Object is missing the KIRI_3DGS_Write F_DC_And_Merge Modifier')
        else:
            self.report({'ERROR'}, message='Output Directory is not valid')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        if (bpy.context.scene.sna_dgs_scene_properties.export_single_or_sequence == '4DGS'):
            box_5A7F8 = layout.box()
            box_5A7F8.alert = False
            box_5A7F8.enabled = True
            box_5A7F8.active = True
            box_5A7F8.use_property_split = False
            box_5A7F8.use_property_decorate = False
            box_5A7F8.alignment = 'Expand'.upper()
            box_5A7F8.scale_x = 1.0
            box_5A7F8.scale_y = 1.0
            if not True: box_5A7F8.operator_context = "EXEC_DEFAULT"
            box_5A7F8.label(text='Exporting large scans as .PLY sequences is not recommended,', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            box_5A7F8.label(text='        it can be best to export a cropped subset of points', icon_value=0)
            box_5A7F8.label(text='        Exporting large numbers of frames can take a while', icon_value=0)
        box_44942 = layout.box()
        box_44942.alert = False
        box_44942.enabled = True
        box_44942.active = True
        box_44942.use_property_split = False
        box_44942.use_property_decorate = False
        box_44942.alignment = 'Expand'.upper()
        box_44942.scale_x = 1.0
        box_44942.scale_y = 1.0
        if not True: box_44942.operator_context = "EXEC_DEFAULT"
        box_44942.label(text='Camera updates will be set to Disabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_44942.label(text='        Any enabled Animate modifiers found will be set to Displace Only', icon_value=0)
        box_44942.label(text='        3DGS Transforms will be applied to the input object', icon_value=0)
        box_44942.label(text='        The World Centre will be the exported model origin', icon_value=0)
        box_2A27F = layout.box()
        box_2A27F.alert = False
        box_2A27F.enabled = True
        box_2A27F.active = True
        box_2A27F.use_property_split = False
        box_2A27F.use_property_decorate = False
        box_2A27F.alignment = 'Expand'.upper()
        box_2A27F.scale_x = 1.0
        box_2A27F.scale_y = 1.0
        if not True: box_2A27F.operator_context = "EXEC_DEFAULT"
        box_2A27F.prop(self, 'sna_send_to_world_centre', text='Reset Position (Rig locked objects ignore this)', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)
