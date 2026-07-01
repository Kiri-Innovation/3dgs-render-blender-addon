import json
import math
import os
import tempfile
import uuid
from datetime import datetime, timezone

import bpy
import numpy as np
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

try:
    import blf
except Exception:
    blf = None


PROXY_BINDING_VERSION = 1
PROXY_BINDING_ROOT_NAME = "_3dgs_proxy_bindings"
PROXY_BINDING_ROOT_OVERRIDE = ""
PROXY_BINDING_UUID_PROP = "proxy_binding_mesh_uuid"
PROXY_BINDING_PROXY_UUID_PROP = "proxy_binding_proxy_uuid"
PROXY_BINDING_PATH_PROP = "proxy_binding_package_path"
PROXY_BINDING_ACTIVE_PROP = "proxy_binding_active"
PROXY_SEQUENCE_BINDING_PROP = "proxy_sequence_binding"
PROXY_BINDING_METHOD_PROP = "proxy_binding_method"
DEFAULT_NEIGHBOR_COUNT = 32
DEFAULT_DEFORM_MODE = "Elastic"
DEFAULT_SCALE_SAFETY_MODE = "Local Clamp"
DEFAULT_BINDING_METHOD = "Volumetric"
DEFAULT_HYBRID_SURFACE_DISTANCE_FACTOR = 1.5
DEFAULT_SH_QUALITY_MODE = "Final"
DEFAULT_UPDATE_SH_ATTRIBUTES = True
SPLAT_ATTR_ROT_NAMES = ("rot_0", "rot_1", "rot_2", "rot_3")
SPLAT_ATTR_SCALE_NAMES = ("scale_0", "scale_1", "scale_2")
SPLAT_ATTR_DC_NAMES = ("f_dc_0", "f_dc_1", "f_dc_2")
SUPPORTED_SH_DEGREES = {0, 1, 2, 3}
EPSILON = 1e-8
GLOBAL_SCALE_CLAMP_MULTIPLIER = 1.75
LOCAL_SCALE_ANISOTROPY_LIMIT = 1.35
LOCAL_CONDITION_BLEND_START = 1.25
LOCAL_CONDITION_BLEND_END = 4.0

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

_SH_ROTATION_CACHE = {}
if not hasattr(bpy, "_proxy_binding_package_cache"):
    bpy._proxy_binding_package_cache = {}
_BINDING_PACKAGE_CACHE = bpy._proxy_binding_package_cache
SH_QUALITY_SAMPLE_COUNTS = {
    "Fast": 24,
    "Balanced": 32,
    "Final": 48,
}
_BAKE_PROGRESS_HANDLER = None
_BAKE_PROGRESS_STATE = {
    "active": False,
    "title": "3DGS Bake Progress",
    "object_name": "",
    "current_step": 0,
    "total_steps": 0,
    "current_frame": None,
    "status_message": "",
}


class ProxyBindingError(RuntimeError):
    pass


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def sanitize_name(name):
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name.strip())
    return safe or "object"


def ensure_object_uuid(obj, prop_name):
    object_uuid = obj.get(prop_name)
    if not object_uuid:
        object_uuid = str(uuid.uuid4())
        obj[prop_name] = object_uuid
    return object_uuid


def get_binding_root_dir():
    override_dir = str(PROXY_BINDING_ROOT_OVERRIDE).strip()
    if override_dir:
        base_dir = bpy.path.abspath(override_dir)
    elif bpy.data.filepath:
        base_dir = bpy.path.abspath("//")
    else:
        base_dir = tempfile.gettempdir()
    binding_root = os.path.join(base_dir, PROXY_BINDING_ROOT_NAME)
    os.makedirs(binding_root, exist_ok=True)
    return binding_root


def get_binding_package_dir(obj, create=False, force_new=False):
    package_dir = None if force_new else obj.get(PROXY_BINDING_PATH_PROP)
    if package_dir:
        if create:
            os.makedirs(package_dir, exist_ok=True)
        return package_dir

    object_uuid = ensure_object_uuid(obj, PROXY_BINDING_UUID_PROP)
    package_name = f"{sanitize_name(obj.name)}_{object_uuid}"
    package_dir = os.path.join(get_binding_root_dir(), package_name)
    if create:
        os.makedirs(package_dir, exist_ok=True)
        obj[PROXY_BINDING_PATH_PROP] = package_dir
    return package_dir


def get_binding_file_paths(obj, create=False, force_new=False):
    package_dir = get_binding_package_dir(obj, create=create, force_new=force_new)
    if not package_dir:
        raise ProxyBindingError(f"'{obj.name}' has no proxy binding package path.")
    binding_dir = os.path.join(package_dir, "binding")
    bake_dir = os.path.join(package_dir, "baked_frames")
    if create:
        os.makedirs(binding_dir, exist_ok=True)
        os.makedirs(bake_dir, exist_ok=True)
    return {
        "package_dir": package_dir,
        "binding_dir": binding_dir,
        "bake_dir": bake_dir,
        "json_path": os.path.join(binding_dir, "binding.json"),
        "rest_path": os.path.join(binding_dir, "rest_state.npz"),
        "binding_path": os.path.join(binding_dir, "binding_data.npz"),
    }


def invalidate_binding_package_cache(mesh_obj=None):
    if mesh_obj is None:
        _BINDING_PACKAGE_CACHE.clear()
        return
    package_path = mesh_obj.get(PROXY_BINDING_PATH_PROP)
    if package_path:
        _BINDING_PACKAGE_CACHE.pop(package_path, None)


def clear_binding_state(mesh_obj, clear_package_path=False, clear_binding_method=False):
    invalidate_binding_package_cache(mesh_obj)
    mesh_obj[PROXY_BINDING_ACTIVE_PROP] = False
    mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = False
    if clear_package_path and PROXY_BINDING_PATH_PROP in mesh_obj:
        del mesh_obj[PROXY_BINDING_PATH_PROP]
    if clear_binding_method and PROXY_BINDING_METHOD_PROP in mesh_obj:
        del mesh_obj[PROXY_BINDING_METHOD_PROP]


def get_binding_package_missing_files(mesh_obj):
    try:
        paths = get_binding_file_paths(mesh_obj, create=False)
    except ProxyBindingError:
        return None, ["package_path"]

    missing = []
    if not os.path.exists(paths["json_path"]):
        missing.append("binding.json")
    if not os.path.exists(paths["rest_path"]):
        missing.append("rest_state.npz")
    if not os.path.exists(paths["binding_path"]):
        missing.append("binding_data.npz")
    return paths, missing


def iter_view3d_areas():
    window_manager = getattr(bpy.context, "window_manager", None)
    if window_manager is None:
        return []
    areas = []
    for window in window_manager.windows:
        screen = getattr(window, "screen", None)
        if screen is None:
            continue
        for area in screen.areas:
            if area.type == "VIEW_3D":
                areas.append(area)
    return areas


def tag_view3d_redraw():
    for area in iter_view3d_areas():
        try:
            area.tag_redraw()
        except Exception:
            pass


def force_viewport_redraw():
    tag_view3d_redraw()
    try:
        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
    except Exception:
        pass


def _draw_bake_progress_overlay():
    if blf is None:
        return
    if not _BAKE_PROGRESS_STATE["active"]:
        return

    total_steps = max(int(_BAKE_PROGRESS_STATE.get("total_steps", 0)), 1)
    current_step = max(0, min(int(_BAKE_PROGRESS_STATE.get("current_step", 0)), total_steps))
    percent = (float(current_step) / float(total_steps)) * 100.0
    current_frame = _BAKE_PROGRESS_STATE.get("current_frame")
    object_name = _BAKE_PROGRESS_STATE.get("object_name") or ""
    status_message = _BAKE_PROGRESS_STATE.get("status_message") or ""

    font_id = 0
    x = 24
    y = 88
    line_height = 22

    lines = [
        str(_BAKE_PROGRESS_STATE.get("title", "3DGS Bake Progress")),
        f"Object: {object_name}" if object_name else "Object: (not set)",
        f"Progress: {current_step}/{total_steps} ({percent:.1f}%)",
    ]
    if current_frame is not None:
        lines.append(f"Current frame: {int(current_frame)}")
    if status_message:
        lines.append(str(status_message))

    try:
        blf.size(font_id, 18.0)
    except TypeError:
        blf.size(font_id, 18, 72)

    if hasattr(blf, "enable") and hasattr(blf, "SHADOW"):
        try:
            blf.enable(font_id, blf.SHADOW)
            blf.shadow(font_id, 4, 0, 0, 0, 180)
        except Exception:
            pass

    if hasattr(blf, "color"):
        try:
            blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
        except Exception:
            pass

    for index, line in enumerate(lines):
        try:
            blf.position(font_id, x, y + (line_height * (len(lines) - index - 1)), 0)
            blf.draw(font_id, line)
        except Exception:
            break


def begin_bake_progress_overlay(total_steps, object_name="", title="3DGS Bake Progress"):
    global _BAKE_PROGRESS_HANDLER

    _BAKE_PROGRESS_STATE["active"] = True
    _BAKE_PROGRESS_STATE["title"] = str(title)
    _BAKE_PROGRESS_STATE["object_name"] = str(object_name) if object_name else ""
    _BAKE_PROGRESS_STATE["current_step"] = 0
    _BAKE_PROGRESS_STATE["total_steps"] = max(int(total_steps), 1)
    _BAKE_PROGRESS_STATE["current_frame"] = None
    _BAKE_PROGRESS_STATE["status_message"] = "Preparing bake..."

    window_manager = getattr(bpy.context, "window_manager", None)
    if window_manager is not None:
        try:
            window_manager.progress_begin(0, _BAKE_PROGRESS_STATE["total_steps"])
            window_manager.progress_update(0)
        except Exception:
            pass

    if blf is not None and _BAKE_PROGRESS_HANDLER is None and iter_view3d_areas():
        try:
            _BAKE_PROGRESS_HANDLER = bpy.types.SpaceView3D.draw_handler_add(
                _draw_bake_progress_overlay,
                (),
                "WINDOW",
                "POST_PIXEL",
            )
        except Exception:
            _BAKE_PROGRESS_HANDLER = None

    force_viewport_redraw()


def update_bake_progress_overlay(current_step, total_steps=None, frame_number=None, status_message=""):
    if total_steps is not None:
        _BAKE_PROGRESS_STATE["total_steps"] = max(int(total_steps), 1)
    _BAKE_PROGRESS_STATE["current_step"] = max(0, int(current_step))
    _BAKE_PROGRESS_STATE["current_frame"] = None if frame_number is None else int(frame_number)
    if status_message:
        _BAKE_PROGRESS_STATE["status_message"] = str(status_message)

    window_manager = getattr(bpy.context, "window_manager", None)
    if window_manager is not None:
        try:
            window_manager.progress_update(min(_BAKE_PROGRESS_STATE["current_step"], _BAKE_PROGRESS_STATE["total_steps"]))
        except Exception:
            pass

    force_viewport_redraw()


def end_bake_progress_overlay(status_message=""):
    global _BAKE_PROGRESS_HANDLER

    if status_message:
        _BAKE_PROGRESS_STATE["status_message"] = str(status_message)
        force_viewport_redraw()

    if _BAKE_PROGRESS_HANDLER is not None:
        try:
            bpy.types.SpaceView3D.draw_handler_remove(_BAKE_PROGRESS_HANDLER, "WINDOW")
        except Exception:
            pass
        _BAKE_PROGRESS_HANDLER = None

    window_manager = getattr(bpy.context, "window_manager", None)
    if window_manager is not None:
        try:
            window_manager.progress_end()
        except Exception:
            pass

    _BAKE_PROGRESS_STATE["active"] = False
    _BAKE_PROGRESS_STATE["status_message"] = ""
    _BAKE_PROGRESS_STATE["current_frame"] = None
    force_viewport_redraw()


def matrix_to_row_affine(matrix):
    matrix_np = np.array(matrix, dtype=np.float64)
    linear = matrix_np[:3, :3].T.copy()
    translation = matrix_np[:3, 3].copy()
    return linear, translation


def transform_points_row(points, linear, translation):
    return np.asarray(points, dtype=np.float64) @ linear + translation


def inverse_transform_points_row(points, linear, translation):
    inv_linear = np.linalg.inv(linear)
    return (np.asarray(points, dtype=np.float64) - translation) @ inv_linear


def points_to_row_affine(X, Y):
    ones = np.ones((X.shape[0], X.shape[1], 1), dtype=np.float64)
    X_aug = np.concatenate([X, ones], axis=2)
    xt = np.transpose(X_aug, (0, 2, 1))
    xtx = np.matmul(xt, X_aug)
    xtx[:, np.arange(4), np.arange(4)] += EPSILON
    xty = np.matmul(xt, Y)
    try:
        solution = np.linalg.solve(xtx, xty)
    except np.linalg.LinAlgError as exc:
        raise ProxyBindingError("Failed to solve local affine transform for bound splats.") from exc
    linear = solution[:, :3, :]
    translation = solution[:, 3, :]
    return linear, translation


def compute_knn_weights(points, proxy_vertices_world, knn_indices, power=2.0):
    points = np.asarray(points, dtype=np.float64)
    proxy_vertices_world = np.asarray(proxy_vertices_world, dtype=np.float64)
    knn_indices = np.asarray(knn_indices, dtype=np.int32)

    neighbor_positions = proxy_vertices_world[knn_indices]
    distances = np.linalg.norm(neighbor_positions - points[:, None, :], axis=2)
    weights = np.zeros_like(distances, dtype=np.float64)

    zero_mask = distances <= EPSILON
    zero_rows = np.any(zero_mask, axis=1)
    if np.any(zero_rows):
        zero_counts = zero_mask[zero_rows].sum(axis=1, keepdims=True)
        weights[zero_rows] = zero_mask[zero_rows] / np.clip(zero_counts, 1.0, None)

    nonzero_rows = ~zero_rows
    if np.any(nonzero_rows):
        inv_dist = 1.0 / np.power(np.clip(distances[nonzero_rows], EPSILON, None), power)
        weights[nonzero_rows] = inv_dist / np.clip(inv_dist.sum(axis=1, keepdims=True), EPSILON, None)

    return weights


def solve_weighted_rigid_row(X, Y, weights):
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    weights = np.asarray(weights, dtype=np.float64)

    weights = weights / np.clip(weights.sum(axis=1, keepdims=True), EPSILON, None)
    centroid_X = np.sum(X * weights[:, :, None], axis=1)
    centroid_Y = np.sum(Y * weights[:, :, None], axis=1)

    centered_X = X - centroid_X[:, None, :]
    centered_Y = Y - centroid_Y[:, None, :]
    covariance = np.einsum("nki,nkj,nk->nij", centered_X, centered_Y, weights)

    U, _, Vh = np.linalg.svd(covariance)
    rotations = np.matmul(U, Vh)
    negative_mask = np.linalg.det(rotations) < 0.0
    if np.any(negative_mask):
        U[negative_mask, :, -1] *= -1.0
        rotations[negative_mask] = np.matmul(U[negative_mask], Vh[negative_mask])

    translations = centroid_Y - np.einsum("ni,nij->nj", centroid_X, rotations)
    return rotations, translations


def solve_weighted_affine_row(X, Y, weights):
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    weights = np.asarray(weights, dtype=np.float64)

    weights = weights / np.clip(weights.sum(axis=1, keepdims=True), EPSILON, None)
    ones = np.ones((X.shape[0], X.shape[1], 1), dtype=np.float64)
    X_aug = np.concatenate([X, ones], axis=2)
    xtwx = np.einsum("nki,nkj,nk->nij", X_aug, X_aug, weights)
    xtwx[:, np.arange(4), np.arange(4)] += EPSILON
    xtwy = np.einsum("nki,nkj,nk->nij", X_aug, Y, weights)
    try:
        solution = np.linalg.solve(xtwx, xtwy)
    except np.linalg.LinAlgError as exc:
        raise ProxyBindingError("Failed to solve weighted local affine transform for bound splats.") from exc
    linear = solution[:, :3, :]
    translation = solution[:, 3, :]
    return linear, translation


def normalize_deform_mode(deform_mode):
    mode = str(deform_mode).strip().lower().replace("_", " ")
    if mode == "stable":
        return "Stable"
    if mode == "adaptive":
        return "Adaptive"
    if mode == "elastic":
        return "Elastic"
    raise ProxyBindingError(f"Unsupported deform_mode '{deform_mode}'. Use Stable, Adaptive, or Elastic.")


def normalize_scale_safety_mode(scale_safety_mode):
    mode = str(scale_safety_mode).strip().lower().replace("_", " ")
    if mode in ("", "off", "none"):
        return "Off"
    if mode == "global clamp":
        return "Global Clamp"
    if mode == "local clamp":
        return "Local Clamp"
    raise ProxyBindingError(
        f"Unsupported scale_safety_mode '{scale_safety_mode}'. Use Off, Global Clamp, or Local Clamp."
    )


def normalize_sh_quality_mode(sh_quality_mode):
    mode = str(sh_quality_mode).strip().lower().replace("_", " ")
    if mode == "fast":
        return "Fast"
    if mode == "balanced":
        return "Balanced"
    if mode == "final":
        return "Final"
    raise ProxyBindingError(
        f"Unsupported sh_quality_mode '{sh_quality_mode}'. Use Fast, Balanced, or Final."
    )


def normalize_update_sh_attributes(update_sh_attributes):
    if isinstance(update_sh_attributes, str):
        mode = update_sh_attributes.strip().lower()
        if mode in ("", "0", "false", "off", "no"):
            return False
        if mode in ("1", "true", "on", "yes"):
            return True
    return bool(update_sh_attributes)


def compute_proxy_global_scale_ratio(rest_proxy_vertices_world, current_proxy_vertices_world):
    rest_proxy_vertices_world = np.asarray(rest_proxy_vertices_world, dtype=np.float64)
    current_proxy_vertices_world = np.asarray(current_proxy_vertices_world, dtype=np.float64)

    rest_center = rest_proxy_vertices_world.mean(axis=0, keepdims=True)
    current_center = current_proxy_vertices_world.mean(axis=0, keepdims=True)
    rest_extent = np.linalg.norm(rest_proxy_vertices_world - rest_center, axis=1).mean()
    current_extent = np.linalg.norm(current_proxy_vertices_world - current_center, axis=1).mean()
    return float(current_extent / max(rest_extent, EPSILON))


def compute_scale_updates(
    rest_scales,
    candidate_scales,
    local_affine_world,
    rest_proxy_vertices_world,
    current_proxy_vertices_world,
    deform_mode,
    scale_safety_mode,
):
    deform_mode = normalize_deform_mode(deform_mode)
    scale_safety_mode = normalize_scale_safety_mode(scale_safety_mode)

    rest_scales = np.asarray(rest_scales, dtype=np.float64)
    candidate_scales = np.asarray(candidate_scales, dtype=np.float64)

    if deform_mode == "Stable":
        return rest_scales.copy()

    scale_ratios = candidate_scales / np.clip(rest_scales, EPSILON, None)
    uniform_ratio = np.mean(scale_ratios, axis=1, keepdims=True)
    global_ratio = compute_proxy_global_scale_ratio(rest_proxy_vertices_world, current_proxy_vertices_world)
    global_low = global_ratio / GLOBAL_SCALE_CLAMP_MULTIPLIER
    global_high = global_ratio * GLOBAL_SCALE_CLAMP_MULTIPLIER

    if scale_safety_mode in {"Global Clamp", "Local Clamp"}:
        uniform_ratio = np.clip(uniform_ratio, global_low, global_high)

    if deform_mode == "Adaptive":
        adaptive_ratios = np.repeat(uniform_ratio, 3, axis=1)
        return rest_scales * adaptive_ratios

    elastic_ratios = scale_ratios.copy()
    if scale_safety_mode == "Global Clamp":
        elastic_ratios = np.clip(elastic_ratios, global_low, global_high)
    elif scale_safety_mode == "Local Clamp":
        local_low = uniform_ratio / LOCAL_SCALE_ANISOTROPY_LIMIT
        local_high = uniform_ratio * LOCAL_SCALE_ANISOTROPY_LIMIT
        elastic_ratios = np.clip(elastic_ratios, local_low, local_high)
        singular_values = np.linalg.svd(local_affine_world, compute_uv=False)
        conditions = singular_values[:, 0] / np.clip(singular_values[:, -1], EPSILON, None)
        blend = np.clip(
            (conditions - LOCAL_CONDITION_BLEND_START)
            / max(LOCAL_CONDITION_BLEND_END - LOCAL_CONDITION_BLEND_START, EPSILON),
            0.0,
            1.0,
        )[:, None]
        elastic_ratios = elastic_ratios * (1.0 - blend) + np.repeat(uniform_ratio, 3, axis=1) * blend
        elastic_ratios = np.clip(elastic_ratios, global_low, global_high)

    return rest_scales * elastic_ratios


def get_active_3dgs_mesh_object(require_bound=False):
    obj = bpy.context.active_object
    if obj is None or obj.type != "MESH":
        raise ProxyBindingError("Active object must be the mesh 3DGS object.")
    if not check_mesh_has_gaussian_attributes(obj):
        raise ProxyBindingError(f"'{obj.name}' does not look like a mesh 3DGS object.")
    if require_bound and not obj.get(PROXY_BINDING_PATH_PROP):
        raise ProxyBindingError(f"'{obj.name}' is not proxy-bound.")
    return obj


def normalize_target_mode(target_mode, allow_all=True):
    mode = str(target_mode).strip().lower().replace("_", " ")
    if mode in ("", "active"):
        return "Active"
    if mode in ("input object", "input", "object", "target object"):
        return "Input Object"
    if allow_all and mode in ("all bound", "all", "all objects"):
        return "All Bound"
    if allow_all:
        raise ProxyBindingError(
            f"Unsupported target_mode '{target_mode}'. Use Active, Input Object, or All Bound."
        )
    raise ProxyBindingError(
        f"Unsupported target_mode '{target_mode}'. Use Active or Input Object."
    )


def get_input_3dgs_mesh_object(target_obj, require_bound=False):
    if target_obj is None:
        raise ProxyBindingError("target_obj must point to the mesh 3DGS object when target_mode is Input Object.")

    if isinstance(target_obj, str):
        target_name = target_obj.strip()
        if not target_name:
            raise ProxyBindingError("target_obj cannot be blank when target_mode is Input Object.")
        obj = bpy.data.objects.get(target_name)
        if obj is None:
            raise ProxyBindingError(f"Input mesh 3DGS object '{target_name}' was not found.")
    else:
        obj = target_obj

    if getattr(obj, "type", None) != "MESH":
        raise ProxyBindingError("target_obj must point to a mesh object.")
    if not check_mesh_has_gaussian_attributes(obj):
        raise ProxyBindingError(f"'{obj.name}' does not look like a mesh 3DGS object.")
    if require_bound and not obj.get(PROXY_BINDING_PATH_PROP):
        raise ProxyBindingError(f"'{obj.name}' is not proxy-bound.")
    return obj


def get_all_bound_3dgs_mesh_objects(active_only=False):
    objects = []
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        if not obj.get(PROXY_BINDING_PATH_PROP):
            continue
        if active_only and not obj.get(PROXY_BINDING_ACTIVE_PROP):
            continue
        if not check_mesh_has_gaussian_attributes(obj):
            continue
        objects.append(obj)
    return objects


def resolve_target_mesh_objects(
    target_mode="Active",
    target_obj=None,
    require_bound=False,
    allow_all=True,
    active_only=False,
):
    mode = normalize_target_mode(target_mode, allow_all=allow_all)
    if mode == "Active":
        return [get_active_3dgs_mesh_object(require_bound=require_bound)]
    if mode == "Input Object":
        return [get_input_3dgs_mesh_object(target_obj, require_bound=require_bound)]

    objects = get_all_bound_3dgs_mesh_objects(active_only=active_only)
    if require_bound:
        objects = [obj for obj in objects if obj.get(PROXY_BINDING_PATH_PROP)]
    if not objects:
        raise ProxyBindingError("No bound mesh 3DGS objects were found in the scene.")
    return objects


def resolve_target_mesh_object(target_mode="Active", target_obj=None, require_bound=False, allow_all=False):
    objects = resolve_target_mesh_objects(
        target_mode=target_mode,
        target_obj=target_obj,
        require_bound=require_bound,
        allow_all=allow_all,
        active_only=require_bound,
    )
    if len(objects) != 1:
        raise ProxyBindingError("Exactly one mesh 3DGS object must be resolved for this operation.")
    return objects[0]


def normalize_binding_method(binding_method):
    method = str(binding_method).strip().lower().replace("_", " ")
    if method in ("", "volumetric", "volume", "knn", "knn vertices", "knn vertex", "knnvertices"):
        return "Volumetric"
    if method in ("surface", "surface aligned", "surface aligned proxy", "surface triangles", "surfacetriangles"):
        return "Surface"
    if method in ("hybrid", "mixed", "hybrid surface volumetric", "surface volumetric hybrid"):
        return "Hybrid"
    raise ProxyBindingError(f"Unsupported binding_method '{binding_method}'. Use Volumetric, Surface, or Hybrid.")


def get_binding_method_from_metadata(metadata):
    saved_method = metadata.get("binding_method")
    if saved_method:
        return normalize_binding_method(saved_method)
    return normalize_binding_method(metadata.get("binding_mode", DEFAULT_BINDING_METHOD))


def get_selected_proxy_mesh(three_dgs_obj):
    selected_meshes = [obj for obj in bpy.context.selected_objects if obj.type == "MESH" and obj != three_dgs_obj]
    if len(selected_meshes) != 1:
        raise ProxyBindingError("Select exactly one proxy mesh in addition to the active mesh 3DGS object.")
    return selected_meshes[0]


def resolve_proxy_mesh_input(proxy_input, three_dgs_obj):
    if proxy_input is None:
        return get_selected_proxy_mesh(three_dgs_obj)

    if isinstance(proxy_input, str):
        proxy_name = proxy_input.strip()
        if not proxy_name:
            return get_selected_proxy_mesh(three_dgs_obj)
        proxy_obj = bpy.data.objects.get(proxy_name)
        if proxy_obj is None:
            raise ProxyBindingError(f"Proxy mesh '{proxy_name}' was not found.")
    else:
        proxy_obj = proxy_input

    if getattr(proxy_obj, "type", None) != "MESH":
        raise ProxyBindingError("The proxy mesh input must point to a mesh object.")
    if proxy_obj == three_dgs_obj:
        raise ProxyBindingError("The proxy mesh must be different from the active mesh 3DGS object.")
    return proxy_obj


def find_object_by_uuid(prop_name, object_uuid):
    for obj in bpy.data.objects:
        if obj.get(prop_name) == object_uuid:
            return obj
    return None


def get_bound_proxy_object(binding_info):
    proxy_uuid = binding_info.get("proxy_object_uuid")
    proxy_name = binding_info.get("proxy_object_name")
    proxy_obj = None
    if proxy_uuid:
        proxy_obj = find_object_by_uuid(PROXY_BINDING_PROXY_UUID_PROP, proxy_uuid)
    if proxy_obj is None and proxy_name in bpy.data.objects:
        proxy_obj = bpy.data.objects[proxy_name]
    if proxy_obj is None:
        raise ProxyBindingError("Could not find the bound proxy mesh object.")
    if proxy_obj.type != "MESH":
        raise ProxyBindingError(f"Bound proxy object '{proxy_obj.name}' is no longer a mesh.")
    return proxy_obj


def list_attribute_names(mesh_data):
    return [attribute.name for attribute in mesh_data.attributes]


def check_mesh_has_gaussian_attributes(mesh_obj):
    available = list_attribute_names(mesh_obj.data)
    required = list(SPLAT_ATTR_ROT_NAMES) + list(SPLAT_ATTR_SCALE_NAMES) + list(SPLAT_ATTR_DC_NAMES)
    return all(name in available for name in required)


def get_splat_vertex_groups(mesh_data):
    num_vertices = len(mesh_data.vertices)
    num_polygons = len(mesh_data.polygons)

    if num_vertices == 0:
        raise ProxyBindingError("3DGS mesh has no vertices.")

    if num_polygons == 0:
        return np.arange(num_vertices, dtype=np.int32).reshape(-1, 1), False

    if all(len(poly.vertices) == 4 for poly in mesh_data.polygons) and num_polygons * 4 == num_vertices:
        usage_counts = np.zeros(num_vertices, dtype=np.int32)
        groups = []
        for poly in mesh_data.polygons:
            poly_indices = np.array(poly.vertices[:], dtype=np.int32)
            usage_counts[poly_indices] += 1
            groups.append(poly_indices)
        if np.all(usage_counts == 1):
            return np.stack(groups, axis=0), True

    raise ProxyBindingError(
        "3DGS mesh topology is not supported. Use a point cloud mesh or a pure disconnected quad mesh."
    )


def read_vertex_positions_local(mesh_data):
    coords = np.empty(len(mesh_data.vertices) * 3, dtype=np.float64)
    mesh_data.vertices.foreach_get("co", coords)
    return coords.reshape(-1, 3)


def write_vertex_positions_local(mesh_data, positions_local):
    mesh_data.vertices.foreach_set("co", np.asarray(positions_local, dtype=np.float32).reshape(-1))
    mesh_data.update()


def get_point_attribute(mesh_data, attr_name):
    if attr_name not in mesh_data.attributes:
        raise ProxyBindingError(f"Required attribute '{attr_name}' is missing.")
    attr = mesh_data.attributes[attr_name]
    values = np.empty(len(attr.data), dtype=np.float64)
    attr.data.foreach_get("value", values)
    return values


def set_point_attribute(mesh_data, attr_name, values):
    if attr_name not in mesh_data.attributes:
        raise ProxyBindingError(f"Required attribute '{attr_name}' is missing.")
    attr = mesh_data.attributes[attr_name]
    attr.data.foreach_set("value", np.asarray(values, dtype=np.float32).reshape(-1))


def scatter_logical_to_vertices(logical_values, splat_vertex_groups, num_vertices):
    logical_values = np.asarray(logical_values)
    repeated = np.repeat(logical_values, splat_vertex_groups.shape[1], axis=0)
    vertex_values = np.zeros((num_vertices,) + logical_values.shape[1:], dtype=logical_values.dtype)
    vertex_values[splat_vertex_groups.reshape(-1)] = repeated
    return vertex_values


def get_sh_degree(mesh_data):
    available = list_attribute_names(mesh_data)
    if not all(name in available for name in SPLAT_ATTR_DC_NAMES):
        raise ProxyBindingError("Mesh is missing one or more SH DC attributes.")

    rest_names = sorted(
        [name for name in available if name.startswith("f_rest_")],
        key=lambda item: int(item.split("_")[-1]),
    )
    total_coeffs = 1 + len(rest_names) // 3
    sh_degree = int(round(math.sqrt(total_coeffs) - 1))
    if sh_degree not in SUPPORTED_SH_DEGREES:
        raise ProxyBindingError(f"Unsupported SH degree {sh_degree}. Only degrees 0-3 are supported.")
    if 3 * ((sh_degree + 1) ** 2 - 1) != len(rest_names):
        raise ProxyBindingError("Mesh SH attribute layout does not match the expected 3DGS convention.")
    return sh_degree, rest_names


def read_logical_gaussian_state(mesh_obj):
    mesh_data = mesh_obj.data
    splat_vertex_groups, is_face_based = get_splat_vertex_groups(mesh_data)
    vertex_positions_local = read_vertex_positions_local(mesh_data)
    logical_positions_local = vertex_positions_local[splat_vertex_groups].mean(axis=1)
    representative_indices = splat_vertex_groups[:, 0]

    log_scales = np.column_stack([get_point_attribute(mesh_data, name) for name in SPLAT_ATTR_SCALE_NAMES])
    quaternions = np.column_stack([get_point_attribute(mesh_data, name) for name in SPLAT_ATTR_ROT_NAMES])
    opacities = get_point_attribute(mesh_data, "opacity")

    log_scales = log_scales[representative_indices]
    quaternions = quaternions[representative_indices]
    opacities = opacities[representative_indices]

    quat_norms = np.linalg.norm(quaternions, axis=1, keepdims=True)
    quat_norms = np.clip(quat_norms, EPSILON, None)
    quaternions = quaternions / quat_norms

    sh_degree, rest_names = get_sh_degree(mesh_data)
    total_coeffs = (sh_degree + 1) ** 2
    sh_coeffs = np.zeros((len(representative_indices), 3, total_coeffs), dtype=np.float64)
    sh_coeffs[:, 0, 0] = get_point_attribute(mesh_data, SPLAT_ATTR_DC_NAMES[0])[representative_indices]
    sh_coeffs[:, 1, 0] = get_point_attribute(mesh_data, SPLAT_ATTR_DC_NAMES[1])[representative_indices]
    sh_coeffs[:, 2, 0] = get_point_attribute(mesh_data, SPLAT_ATTR_DC_NAMES[2])[representative_indices]

    if sh_degree > 0:
        rest_flat = np.column_stack([get_point_attribute(mesh_data, name) for name in rest_names])
        rest_flat = rest_flat[representative_indices]
        sh_coeffs[:, :, 1:] = rest_flat.reshape(len(representative_indices), 3, total_coeffs - 1)

    return {
        "vertex_positions_local": vertex_positions_local.astype(np.float64),
        "logical_positions_local": logical_positions_local.astype(np.float64),
        "log_scales": log_scales.astype(np.float64),
        "quaternions": quaternions.astype(np.float64),
        "opacities": opacities.astype(np.float64),
        "sh_coeffs": sh_coeffs.astype(np.float64),
        "sh_degree": int(sh_degree),
        "splat_vertex_groups": splat_vertex_groups.astype(np.int32),
        "is_face_based": bool(is_face_based),
    }


def write_logical_gaussian_state(mesh_obj, state):
    mesh_data = mesh_obj.data
    splat_vertex_groups = state["splat_vertex_groups"]
    num_vertices = len(mesh_data.vertices)

    write_vertex_positions_local(mesh_data, state["vertex_positions_local"])

    vertex_log_scales = scatter_logical_to_vertices(state["log_scales"], splat_vertex_groups, num_vertices)
    vertex_quaternions = scatter_logical_to_vertices(state["quaternions"], splat_vertex_groups, num_vertices)
    vertex_opacities = scatter_logical_to_vertices(state["opacities"][:, None], splat_vertex_groups, num_vertices)[:, 0]

    for attr_index, attr_name in enumerate(SPLAT_ATTR_SCALE_NAMES):
        set_point_attribute(mesh_data, attr_name, vertex_log_scales[:, attr_index])

    for attr_index, attr_name in enumerate(SPLAT_ATTR_ROT_NAMES):
        set_point_attribute(mesh_data, attr_name, vertex_quaternions[:, attr_index])

    set_point_attribute(mesh_data, "opacity", vertex_opacities)

    sh_degree = int(state["sh_degree"])
    total_coeffs = (sh_degree + 1) ** 2
    vertex_sh = scatter_logical_to_vertices(state["sh_coeffs"], splat_vertex_groups, num_vertices)

    for channel_index, attr_name in enumerate(SPLAT_ATTR_DC_NAMES):
        set_point_attribute(mesh_data, attr_name, vertex_sh[:, channel_index, 0])

    if sh_degree > 0:
        flat_rest = vertex_sh[:, :, 1:].reshape(num_vertices, 3 * (total_coeffs - 1))
        rest_names = sorted(
            [name for name in list_attribute_names(mesh_data) if name.startswith("f_rest_")],
            key=lambda item: int(item.split("_")[-1]),
        )
        if len(rest_names) != flat_rest.shape[1]:
            raise ProxyBindingError("Mesh SH attributes no longer match the bound rest state.")
        for attr_index, attr_name in enumerate(rest_names):
            set_point_attribute(mesh_data, attr_name, flat_rest[:, attr_index])

    mesh_data.update()


def quaternions_to_rotation_matrices(quaternions):
    quaternions = np.asarray(quaternions, dtype=np.float64)
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
    matrices = np.asarray(matrices, dtype=np.float64)
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
    norms = np.clip(norms, EPSILON, None)
    quaternions /= norms
    negative_w = quaternions[:, 0] < 0.0
    quaternions[negative_w] *= -1.0
    return quaternions


def build_row_axes_from_scales_and_quaternions(log_scales, quaternions):
    scales = np.exp(np.asarray(log_scales, dtype=np.float64))
    rotation_matrices = quaternions_to_rotation_matrices(np.asarray(quaternions, dtype=np.float64))
    column_axes = rotation_matrices * scales[:, None, :]
    return np.transpose(column_axes, (0, 2, 1))


def orthogonalize_row_basis(basis_rows):
    basis_rows = np.asarray(basis_rows, dtype=np.float64)
    norms = np.linalg.norm(basis_rows, axis=2)
    order = np.argsort(norms, axis=1)[:, ::-1]
    sorted_basis = np.take_along_axis(basis_rows, order[:, :, None], axis=1)

    axis_0 = sorted_basis[:, 0, :]
    axis_1 = sorted_basis[:, 1, :]
    axis_2 = sorted_basis[:, 2, :]

    axis_0_norm_sq = np.sum(axis_0 * axis_0, axis=1, keepdims=True)
    axis_0_norm_sq = np.clip(axis_0_norm_sq, EPSILON, None)

    ortho_1 = axis_1 - (np.sum(axis_1 * axis_0, axis=1, keepdims=True) / axis_0_norm_sq) * axis_0
    ortho_1_norm_sq = np.sum(ortho_1 * ortho_1, axis=1, keepdims=True)
    ortho_1_norm_sq = np.clip(ortho_1_norm_sq, EPSILON, None)

    ortho_2 = axis_2
    ortho_2 -= (np.sum(axis_2 * axis_0, axis=1, keepdims=True) / axis_0_norm_sq) * axis_0
    ortho_2 -= (np.sum(axis_2 * ortho_1, axis=1, keepdims=True) / ortho_1_norm_sq) * ortho_1

    ortho_basis = np.stack([axis_0, ortho_1, ortho_2], axis=1)
    determinants = np.linalg.det(ortho_basis)
    negative_mask = determinants <= 0.0
    if np.any(negative_mask):
        ortho_basis[negative_mask] *= -1.0
    return ortho_basis


def nearest_rotation_matrices(linear_mats):
    linear_mats = np.asarray(linear_mats, dtype=np.float64)
    u, _, vh = np.linalg.svd(linear_mats)
    rotations = np.matmul(u, vh)
    negative_mask = np.linalg.det(rotations) < 0.0
    if np.any(negative_mask):
        u[negative_mask, :, -1] *= -1.0
        rotations[negative_mask] = np.matmul(u[negative_mask], vh[negative_mask])
    return rotations


def evaluate_real_sh_basis(directions):
    directions = np.asarray(directions, dtype=np.float64)
    x = directions[:, 0]
    y = directions[:, 1]
    z = directions[:, 2]

    basis = np.zeros((len(directions), 16), dtype=np.float64)
    basis[:, 0] = SH_C0
    basis[:, 1] = -SH_C1 * y
    basis[:, 2] = SH_C1 * z
    basis[:, 3] = -SH_C1 * x

    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    yz = y * z
    xz = x * z

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


def fibonacci_sphere(num_samples=48):
    indices = np.arange(num_samples, dtype=np.float64) + 0.5
    phi = math.pi * (3.0 - math.sqrt(5.0))
    y = 1.0 - (indices / num_samples) * 2.0
    radius = np.sqrt(np.clip(1.0 - y * y, 0.0, None))
    theta = phi * indices
    x = np.cos(theta) * radius
    z = np.sin(theta) * radius
    samples = np.stack([x, y, z], axis=1)
    return samples / np.clip(np.linalg.norm(samples, axis=1, keepdims=True), EPSILON, None)


def get_sh_rotation_precompute(max_degree, sh_quality_mode=DEFAULT_SH_QUALITY_MODE):
    quality_mode = normalize_sh_quality_mode(sh_quality_mode)
    sample_count = SH_QUALITY_SAMPLE_COUNTS[quality_mode]
    cache_key = (int(max_degree), int(sample_count))
    if cache_key in _SH_ROTATION_CACHE:
        return _SH_ROTATION_CACHE[cache_key]

    sample_dirs = fibonacci_sphere(num_samples=sample_count)
    full_basis = evaluate_real_sh_basis(sample_dirs)
    precompute = {
        "sample_dirs": sample_dirs,
        "pinv_blocks": {},
        "sample_count": int(sample_count),
        "quality_mode": quality_mode,
    }

    for degree in range(1, max_degree + 1):
        start = degree * degree
        end = (degree + 1) * (degree + 1)
        block = full_basis[:, start:end]
        precompute["pinv_blocks"][degree] = np.linalg.pinv(block)

    _SH_ROTATION_CACHE[cache_key] = precompute
    return precompute


def _get_sh_gpu_state():
    if not hasattr(bpy, "_proxy_sh_gpu_state"):
        bpy._proxy_sh_gpu_state = {"sticky_cpu": False, "enabled": True, "gpu_module": None}
    return bpy._proxy_sh_gpu_state


def _try_rotate_sh_coeffs_gpu(sh_coeffs, rotation_matrices, sh_degree, precompute):
    state = _get_sh_gpu_state()
    if state["sticky_cpu"] or not state["enabled"]:
        return None
    gpu_mod = state["gpu_module"]
    if gpu_mod is None:
        import sys as _sys
        gpu_mod = _sys.modules.get("proxy_binding_gpu")
        if gpu_mod is None:
            return None
        state["gpu_module"] = gpu_mod
    if not gpu_mod.is_available():
        return None
    try:
        result = gpu_mod.rotate_sh_coeffs_gpu(sh_coeffs, rotation_matrices, sh_degree, precompute)
    except Exception as exc:
        state["sticky_cpu"] = True
        print(f"[proxy_binding] GPU SH rotation raised ({exc}); CPU for the rest of session.")
        return None
    if result is None:
        state["sticky_cpu"] = True
        err = getattr(gpu_mod, "last_error", lambda: "unknown")()
        print(f"[proxy_binding] GPU SH rotation unavailable ({err}); CPU for the rest of session.")
        return None
    return result


def rotate_sh_coeffs(
    sh_coeffs,
    rotation_matrices,
    sh_degree,
    sh_quality_mode=DEFAULT_SH_QUALITY_MODE,
    chunk_size=512,
):
    sh_coeffs = np.asarray(sh_coeffs, dtype=np.float64)
    rotation_matrices = np.asarray(rotation_matrices, dtype=np.float64)

    if sh_degree <= 0:
        return sh_coeffs.copy()

    total_coeffs = (sh_degree + 1) ** 2
    precompute = get_sh_rotation_precompute(sh_degree, sh_quality_mode=sh_quality_mode)

    gpu_result = _try_rotate_sh_coeffs_gpu(sh_coeffs, rotation_matrices, sh_degree, precompute)
    if gpu_result is not None:
        return gpu_result[:, :, :total_coeffs]

    rotated = sh_coeffs.copy()
    sample_dirs = precompute["sample_dirs"]

    for start_index in range(0, len(sh_coeffs), chunk_size):
        end_index = min(start_index + chunk_size, len(sh_coeffs))
        chunk_rotations = rotation_matrices[start_index:end_index]
        rotated_dirs = np.einsum("sd,ndk->nsk", sample_dirs, chunk_rotations)
        chunk_basis = evaluate_real_sh_basis(rotated_dirs.reshape(-1, 3)).reshape(
            end_index - start_index,
            sample_dirs.shape[0],
            16,
        )

        for degree in range(1, sh_degree + 1):
            block_start = degree * degree
            block_end = (degree + 1) * (degree + 1)
            pinv_block = precompute["pinv_blocks"][degree]
            rotated_block_basis = chunk_basis[:, :, block_start:block_end]
            rotation_block = np.einsum("ds,nsk->ndk", pinv_block, rotated_block_basis)
            coeff_block = sh_coeffs[start_index:end_index, :, block_start:block_end]
            rotated[start_index:end_index, :, block_start:block_end] = np.einsum(
                "nci,nji->ncj",
                coeff_block,
                rotation_block,
            )

    return rotated[:, :, :total_coeffs]


def compute_updated_sh_coeffs(
    rest_state,
    sh_rotations,
    update_sh_attributes=DEFAULT_UPDATE_SH_ATTRIBUTES,
    sh_quality_mode=DEFAULT_SH_QUALITY_MODE,
):
    update_sh_attributes = normalize_update_sh_attributes(update_sh_attributes)
    if not update_sh_attributes or int(rest_state["sh_degree"]) <= 0:
        return rest_state["sh_coeffs"].copy()
    return rotate_sh_coeffs(
        rest_state["sh_coeffs"],
        sh_rotations,
        rest_state["sh_degree"],
        sh_quality_mode=sh_quality_mode,
    )


def collect_proxy_vertices_world(proxy_obj):
    proxy_vertices_world, _ = collect_proxy_surface_geometry_world(proxy_obj)
    return proxy_vertices_world


def collect_proxy_surface_geometry_world(proxy_obj):
    view_layer = bpy.context.view_layer
    original_hide_viewport = bool(getattr(proxy_obj, "hide_viewport", False))
    original_hide_state = None
    try:
        original_hide_state = bool(proxy_obj.hide_get())
    except Exception:
        original_hide_state = None

    if original_hide_viewport:
        proxy_obj.hide_viewport = False
    if original_hide_state:
        try:
            proxy_obj.hide_set(False)
        except Exception:
            pass
    view_layer.update()

    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated_obj = proxy_obj.evaluated_get(depsgraph)
    evaluated_mesh = evaluated_obj.to_mesh()
    try:
        vertex_positions_local = read_vertex_positions_local(evaluated_mesh)
        linear, translation = matrix_to_row_affine(evaluated_obj.matrix_world)
        vertex_positions_world = transform_points_row(vertex_positions_local, linear, translation)
        evaluated_mesh.calc_loop_triangles()
        if not evaluated_mesh.loop_triangles:
            raise ProxyBindingError(f"Proxy mesh '{proxy_obj.name}' needs polygons for Surface binding.")
        triangle_vertex_indices = np.array(
            [triangle.vertices[:] for triangle in evaluated_mesh.loop_triangles],
            dtype=np.int32,
        )
        return vertex_positions_world, triangle_vertex_indices
    finally:
        evaluated_obj.to_mesh_clear()
        if original_hide_state:
            try:
                proxy_obj.hide_set(True)
            except Exception:
                pass
        if original_hide_viewport:
            proxy_obj.hide_viewport = True
        if original_hide_viewport or original_hide_state:
            view_layer.update()


def build_surface_bvh(proxy_vertices_world, triangle_vertex_indices):
    vertices = [tuple(point.tolist()) for point in np.asarray(proxy_vertices_world, dtype=np.float64)]
    polygons = [tuple(int(index) for index in triangle) for triangle in np.asarray(triangle_vertex_indices, dtype=np.int32)]
    return BVHTree.FromPolygons(vertices, polygons, all_triangles=True)


def build_triangle_bases_row(triangle_vertices_world):
    triangle_vertices_world = np.asarray(triangle_vertices_world, dtype=np.float64)
    origins = triangle_vertices_world[:, 0, :]
    edge_u = triangle_vertices_world[:, 1, :] - origins
    edge_v_raw = triangle_vertices_world[:, 2, :] - origins

    edge_u_lengths = np.linalg.norm(edge_u, axis=1, keepdims=True)
    edge_u_lengths = np.clip(edge_u_lengths, EPSILON, None)
    edge_u_dir = edge_u / edge_u_lengths

    edge_v_ortho = edge_v_raw - np.sum(edge_v_raw * edge_u_dir, axis=1, keepdims=True) * edge_u_dir
    edge_v_lengths = np.linalg.norm(edge_v_ortho, axis=1, keepdims=True)
    edge_v_lengths = np.clip(edge_v_lengths, EPSILON, None)

    normal = np.cross(edge_u_dir, edge_v_ortho / edge_v_lengths)
    normal_lengths = np.linalg.norm(normal, axis=1, keepdims=True)
    if np.any(normal_lengths[:, 0] <= EPSILON * 10.0):
        raise ProxyBindingError("Proxy mesh has degenerate triangles that cannot be used for Surface binding.")
    normal = normal / np.clip(normal_lengths, EPSILON, None)

    normal_lengths_scaled = np.sqrt(edge_u_lengths * edge_v_lengths)
    basis = np.stack(
        [
            edge_u,
            edge_v_ortho,
            normal * normal_lengths_scaled,
        ],
        axis=1,
    )
    return origins, basis


def compute_surface_binding_data(points_world, proxy_vertices_world, triangle_vertex_indices):
    points_world = np.asarray(points_world, dtype=np.float64)
    proxy_vertices_world = np.asarray(proxy_vertices_world, dtype=np.float64)
    triangle_vertex_indices = np.asarray(triangle_vertex_indices, dtype=np.int32)

    bvh = build_surface_bvh(proxy_vertices_world, triangle_vertex_indices)
    triangle_indices = np.zeros(len(points_world), dtype=np.int32)
    nearest_points = np.zeros_like(points_world)
    for point_index, point in enumerate(points_world):
        nearest = bvh.find_nearest(point.tolist())
        if nearest is None or nearest[2] is None:
            raise ProxyBindingError("Failed to find a nearest proxy surface triangle for one or more splats.")
        nearest_points[point_index] = nearest[0]
        triangle_indices[point_index] = int(nearest[2])

    surface_triangle_indices = triangle_vertex_indices[triangle_indices]
    rest_triangle_vertices_world = proxy_vertices_world[surface_triangle_indices]
    rest_origins, rest_bases = build_triangle_bases_row(rest_triangle_vertices_world)
    rest_basis_inv = np.linalg.inv(rest_bases)
    surface_local_coords = np.einsum(
        "ni,nij->nj",
        points_world - rest_origins,
        rest_basis_inv,
    )

    return {
        "rest_proxy_vertices_world": proxy_vertices_world.astype(np.float64),
        "surface_triangle_indices": surface_triangle_indices.astype(np.int32),
        "surface_local_coords": surface_local_coords.astype(np.float64),
        "surface_distances": np.linalg.norm(points_world - nearest_points, axis=1).astype(np.float64),
    }


def compute_hybrid_binding_data(
    points_world,
    proxy_vertices_world,
    triangle_vertex_indices,
    neighbor_count,
    hybrid_surface_distance_factor=DEFAULT_HYBRID_SURFACE_DISTANCE_FACTOR,
):
    knn_indices, _ = compute_knn_indices(points_world, proxy_vertices_world, neighbor_count)
    surface_binding_data = compute_surface_binding_data(points_world, proxy_vertices_world, triangle_vertex_indices)

    surface_triangle_vertices = proxy_vertices_world[surface_binding_data["surface_triangle_indices"]]
    edge_01 = np.linalg.norm(surface_triangle_vertices[:, 1, :] - surface_triangle_vertices[:, 0, :], axis=1)
    edge_12 = np.linalg.norm(surface_triangle_vertices[:, 2, :] - surface_triangle_vertices[:, 1, :], axis=1)
    edge_20 = np.linalg.norm(surface_triangle_vertices[:, 0, :] - surface_triangle_vertices[:, 2, :], axis=1)
    local_spacing = np.clip((edge_01 + edge_12 + edge_20) / 3.0, EPSILON, None)
    surface_distances = surface_binding_data["surface_distances"]
    hybrid_use_surface = surface_distances <= (local_spacing * float(hybrid_surface_distance_factor))

    binding_payload = {
        "rest_proxy_vertices_world": proxy_vertices_world.astype(np.float32),
        "knn_indices": knn_indices.astype(np.int32),
        "surface_triangle_indices": surface_binding_data["surface_triangle_indices"].astype(np.int32),
        "surface_local_coords": surface_binding_data["surface_local_coords"].astype(np.float32),
        "hybrid_use_surface": hybrid_use_surface.astype(np.int32),
        "surface_distances": surface_distances.astype(np.float32),
        "hybrid_local_spacing": local_spacing.astype(np.float32),
    }
    extra_metadata = {
        "hybrid_surface_distance_factor": float(hybrid_surface_distance_factor),
        "hybrid_surface_count": int(hybrid_use_surface.sum()),
        "hybrid_volumetric_count": int(len(hybrid_use_surface) - hybrid_use_surface.sum()),
    }
    return binding_payload, extra_metadata


def build_kdtree(points):
    kd_tree = KDTree(len(points))
    for index, point in enumerate(points):
        kd_tree.insert(point.tolist(), index)
    kd_tree.balance()
    return kd_tree


def compute_knn_indices(points, proxy_vertices_world, neighbor_count):
    kd_tree = build_kdtree(proxy_vertices_world)
    all_indices = np.zeros((len(points), neighbor_count), dtype=np.int32)
    all_distances = np.zeros((len(points), neighbor_count), dtype=np.float64)
    for point_index, point in enumerate(points):
        nearest = kd_tree.find_n(point.tolist(), neighbor_count)
        if len(nearest) < neighbor_count:
            raise ProxyBindingError("Proxy mesh does not have enough vertices for KNN binding.")
        all_indices[point_index] = [item[1] for item in nearest]
        all_distances[point_index] = [item[2] for item in nearest]
    return all_indices, all_distances


def _atomic_savez_compressed(path, **arrays):
    tmp_path = f"{path}.tmp.{os.getpid()}.{uuid.uuid4().hex}"
    try:
        with open(tmp_path, "wb") as fh:
            np.savez_compressed(fh, **arrays)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise


def _atomic_write_json(path, payload):
    tmp_path = f"{path}.tmp.{os.getpid()}.{uuid.uuid4().hex}"
    try:
        with open(tmp_path, "w", encoding="utf-8") as json_file:
            json.dump(payload, json_file, indent=2)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise


BAKED_STATE_FORMAT_VERSION = 2


def _serialize_baked_state(state, include_sh):
    arrays = {
        "format_version": np.array([BAKED_STATE_FORMAT_VERSION], dtype=np.int32),
        "logical_positions_local": state["logical_positions_local"].astype(np.float32),
        "log_scales": state["log_scales"].astype(np.float32),
        "quaternions": state["quaternions"].astype(np.float32),
        "opacities": state["opacities"].astype(np.float32),
    }
    if state["is_face_based"]:
        arrays["vertex_positions_local"] = state["vertex_positions_local"].astype(np.float32)
    if include_sh and "sh_coeffs" in state:
        arrays["sh_coeffs"] = state["sh_coeffs"].astype(np.float32)
        arrays["sh_degree"] = np.array([state["sh_degree"]], dtype=np.int32)
    return arrays


def _deserialize_baked_state(npz_data, rest_state):
    npz_keys = set(npz_data.files)
    state = {
        "logical_positions_local": npz_data["logical_positions_local"].astype(np.float64),
        "log_scales": npz_data["log_scales"].astype(np.float64),
        "quaternions": npz_data["quaternions"].astype(np.float64),
        "opacities": npz_data["opacities"].astype(np.float64),
    }

    if "splat_vertex_groups" in npz_keys:
        state["splat_vertex_groups"] = npz_data["splat_vertex_groups"].astype(np.int32)
    else:
        state["splat_vertex_groups"] = rest_state["splat_vertex_groups"].astype(np.int32)

    if "is_face_based" in npz_keys:
        state["is_face_based"] = bool(int(npz_data["is_face_based"][0]))
    else:
        state["is_face_based"] = bool(rest_state["is_face_based"])

    if "vertex_positions_local" in npz_keys:
        state["vertex_positions_local"] = npz_data["vertex_positions_local"].astype(np.float64)
    else:
        num_vertices = rest_state["vertex_positions_local"].shape[0]
        state["vertex_positions_local"] = scatter_logical_to_vertices(
            state["logical_positions_local"],
            state["splat_vertex_groups"],
            num_vertices,
        )

    if "sh_coeffs" in npz_keys:
        state["sh_coeffs"] = npz_data["sh_coeffs"].astype(np.float64)
        state["sh_degree"] = int(npz_data["sh_degree"][0])
    else:
        state["sh_coeffs"] = rest_state["sh_coeffs"].astype(np.float64)
        state["sh_degree"] = int(rest_state["sh_degree"])

    return state


def serialize_state_for_save(state):
    return {
        "vertex_positions_local": state["vertex_positions_local"].astype(np.float32),
        "logical_positions_local": state["logical_positions_local"].astype(np.float32),
        "log_scales": state["log_scales"].astype(np.float32),
        "quaternions": state["quaternions"].astype(np.float32),
        "opacities": state["opacities"].astype(np.float32),
        "sh_coeffs": state["sh_coeffs"].astype(np.float32),
        "sh_degree": np.array([state["sh_degree"]], dtype=np.int32),
        "splat_vertex_groups": state["splat_vertex_groups"].astype(np.int32),
        "is_face_based": np.array([1 if state["is_face_based"] else 0], dtype=np.int32),
    }


def deserialize_saved_state(npz_data):
    return {
        "vertex_positions_local": npz_data["vertex_positions_local"].astype(np.float64),
        "logical_positions_local": npz_data["logical_positions_local"].astype(np.float64),
        "log_scales": npz_data["log_scales"].astype(np.float64),
        "quaternions": npz_data["quaternions"].astype(np.float64),
        "opacities": npz_data["opacities"].astype(np.float64),
        "sh_coeffs": npz_data["sh_coeffs"].astype(np.float64),
        "sh_degree": int(npz_data["sh_degree"][0]),
        "splat_vertex_groups": npz_data["splat_vertex_groups"].astype(np.int32),
        "is_face_based": bool(int(npz_data["is_face_based"][0])),
    }


def save_binding_package(mesh_obj, proxy_obj, rest_state, binding_method, binding_payload, extra_metadata=None):
    paths = get_binding_file_paths(mesh_obj, create=True, force_new=True)
    mesh_uuid = ensure_object_uuid(mesh_obj, PROXY_BINDING_UUID_PROP)
    proxy_uuid = ensure_object_uuid(proxy_obj, PROXY_BINDING_PROXY_UUID_PROP)
    binding_method = normalize_binding_method(binding_method)

    linear_3dgs, translation_3dgs = matrix_to_row_affine(mesh_obj.matrix_world)
    linear_proxy, translation_proxy = matrix_to_row_affine(proxy_obj.matrix_world)
    binding_arrays = {
        key: np.asarray(value)
        for key, value in binding_payload.items()
    }

    logical_points_world = transform_points_row(rest_state["logical_positions_local"], linear_3dgs, translation_3dgs)
    proxy_vertices_world = np.asarray(binding_arrays["rest_proxy_vertices_world"], dtype=np.float64)
    binding_mode = "knn_vertices"
    neighbors_per_splat = None
    if binding_method in {"Volumetric", "Hybrid"}:
        knn_indices = np.asarray(binding_arrays["knn_indices"], dtype=np.int32)
        knn_weights = compute_knn_weights(logical_points_world, proxy_vertices_world, knn_indices)
        binding_arrays["knn_indices"] = knn_indices
        binding_arrays["knn_weights"] = knn_weights.astype(np.float32)
        neighbors_per_splat = int(knn_indices.shape[1])
        if binding_method == "Hybrid":
            binding_mode = "hybrid_surface_volumetric"
    else:
        binding_mode = "surface_triangles"

    metadata = {
        "version": PROXY_BINDING_VERSION,
        "created_utc": _utc_now_iso(),
        "binding_method": binding_method,
        "binding_mode": binding_mode,
        "neighbors_per_splat": neighbors_per_splat,
        "rest_frame": int(bpy.context.scene.frame_current),
        "mesh_object_name": mesh_obj.name,
        "mesh_object_uuid": mesh_uuid,
        "proxy_object_name": proxy_obj.name,
        "proxy_object_uuid": proxy_uuid,
        "mesh_vertex_count": int(len(mesh_obj.data.vertices)),
        "mesh_polygon_count": int(len(mesh_obj.data.polygons)),
        "proxy_vertex_count": int(len(proxy_vertices_world)),
        "proxy_polygon_count": int(len(proxy_obj.data.polygons)),
        "proxy_data_name": proxy_obj.data.name,
        "rest_object_matrix_world": np.array(mesh_obj.matrix_world, dtype=np.float64).tolist(),
        "rest_proxy_matrix_world": np.array(proxy_obj.matrix_world, dtype=np.float64).tolist(),
        "rest_object_linear_row": linear_3dgs.tolist(),
        "rest_object_translation_row": translation_3dgs.tolist(),
        "rest_proxy_linear_row": linear_proxy.tolist(),
        "rest_proxy_translation_row": translation_proxy.tolist(),
        "is_face_based": bool(rest_state["is_face_based"]),
        "splat_count": int(len(rest_state["logical_positions_local"])),
        "paths": {
            "rest_state": "binding/rest_state.npz",
            "binding_data": "binding/binding_data.npz",
            "baked_frames": "baked_frames",
        },
        "baked_frames": [],
    }
    if extra_metadata:
        metadata.update(extra_metadata)

    _atomic_savez_compressed(paths["rest_path"], **serialize_state_for_save(rest_state))
    _atomic_savez_compressed(paths["binding_path"], **binding_arrays)
    _atomic_write_json(paths["json_path"], metadata)

    _BINDING_PACKAGE_CACHE.pop(paths["package_dir"], None)
    mesh_obj[PROXY_BINDING_PATH_PROP] = paths["package_dir"]
    mesh_obj[PROXY_BINDING_ACTIVE_PROP] = True
    mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = False
    mesh_obj[PROXY_BINDING_METHOD_PROP] = binding_method
    return metadata


def load_binding_package(mesh_obj):
    paths, missing_files = get_binding_package_missing_files(mesh_obj)
    if missing_files:
        clear_binding_state(mesh_obj, clear_package_path=True, clear_binding_method=True)
        if missing_files == ["package_path"]:
            raise ProxyBindingError(
                f"Binding package path is missing for '{mesh_obj.name}'. The object was marked unbound."
            )
        missing_text = ", ".join(missing_files)
        raise ProxyBindingError(
            f"Binding package files are missing for '{mesh_obj.name}' ({missing_text}). "
            f"The object was marked unbound."
        )

    package_path = paths["package_dir"]
    cached = _BINDING_PACKAGE_CACHE.get(package_path)
    if cached is not None:
        try:
            current_mtime = max(
                os.path.getmtime(paths["json_path"]),
                os.path.getmtime(paths["rest_path"]),
                os.path.getmtime(paths["binding_path"]),
            )
        except OSError:
            current_mtime = None
        if current_mtime is not None and current_mtime <= cached["mtime"]:
            mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = bool(cached["metadata"].get("baked_frames"))
            mesh_obj[PROXY_BINDING_METHOD_PROP] = cached["metadata"]["binding_method"]
            return paths, cached["metadata"], cached["rest_state"], cached["binding_data"]

    with open(paths["json_path"], "r", encoding="utf-8") as json_file:
        metadata = json.load(json_file)
    metadata["binding_method"] = get_binding_method_from_metadata(metadata)

    with np.load(paths["rest_path"]) as rest_npz:
        rest_state = deserialize_saved_state(rest_npz)
    with np.load(paths["binding_path"]) as binding_npz:
        binding_data = {}
        for key in binding_npz.files:
            array = binding_npz[key]
            if np.issubdtype(array.dtype, np.integer):
                binding_data[key] = array.astype(np.int32)
            else:
                binding_data[key] = array.astype(np.float64)

    mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = bool(metadata.get("baked_frames"))
    mesh_obj[PROXY_BINDING_METHOD_PROP] = metadata["binding_method"]

    try:
        loaded_mtime = max(
            os.path.getmtime(paths["json_path"]),
            os.path.getmtime(paths["rest_path"]),
            os.path.getmtime(paths["binding_path"]),
        )
    except OSError:
        loaded_mtime = 0.0
    _BINDING_PACKAGE_CACHE[package_path] = {
        "mtime": loaded_mtime,
        "metadata": metadata,
        "rest_state": rest_state,
        "binding_data": binding_data,
    }

    return paths, metadata, rest_state, binding_data


def save_binding_metadata(json_path, metadata):
    _atomic_write_json(json_path, metadata)


def get_runtime_binding_cache(mesh_obj, metadata, rest_state, binding_data):
    cache = binding_data.get("_runtime_cache")
    if cache is not None:
        return cache

    object_linear_row = np.array(metadata["rest_object_linear_row"], dtype=np.float64)
    object_translation_row = np.array(metadata["rest_object_translation_row"], dtype=np.float64)
    object_rotation_row = nearest_rotation_matrices(object_linear_row[None, :, :])[0]
    object_rotation_inv_row = object_rotation_row.T
    object_linear_inv_row = np.linalg.inv(object_linear_row)
    splat_vertex_groups = rest_state["splat_vertex_groups"]

    rest_rotation_matrices_local = quaternions_to_rotation_matrices(rest_state["quaternions"])
    rest_row_axes_local = build_row_axes_from_scales_and_quaternions(
        rest_state["log_scales"],
        rest_state["quaternions"],
    )
    rest_vertex_positions_world = transform_points_row(
        rest_state["vertex_positions_local"],
        object_linear_row,
        object_translation_row,
    )
    rest_group_positions_world = rest_vertex_positions_world[splat_vertex_groups]
    rest_center_points_world = transform_points_row(
        rest_state["logical_positions_local"],
        object_linear_row,
        object_translation_row,
    )

    cache = {
        "object_linear_row": object_linear_row,
        "object_translation_row": object_translation_row,
        "object_rotation_row": object_rotation_row,
        "object_rotation_inv_row": object_rotation_inv_row,
        "object_linear_inv_row": object_linear_inv_row,
        "rest_rotation_matrices_local": rest_rotation_matrices_local,
        "rest_row_axes_local": rest_row_axes_local,
        "rest_vertex_positions_world": rest_vertex_positions_world,
        "rest_group_positions_world": rest_group_positions_world,
        "rest_center_points_world": rest_center_points_world,
    }

    rest_proxy_vertices_world = binding_data["rest_proxy_vertices_world"]
    if "knn_indices" in binding_data:
        cache["rest_neighbor_positions"] = rest_proxy_vertices_world[binding_data["knn_indices"]]
        if "knn_weights" not in binding_data:
            binding_data["knn_weights"] = compute_knn_weights(
                rest_center_points_world,
                rest_proxy_vertices_world,
                binding_data["knn_indices"],
            )

    if "surface_triangle_indices" in binding_data:
        rest_triangle_vertices_world = rest_proxy_vertices_world[binding_data["surface_triangle_indices"]]
        surface_rest_origins_world, surface_rest_bases_world = build_triangle_bases_row(rest_triangle_vertices_world)
        cache["surface_rest_origins_world"] = surface_rest_origins_world
        cache["surface_rest_bases_world"] = surface_rest_bases_world
        cache["surface_rest_basis_inv_world"] = np.linalg.inv(surface_rest_bases_world)

    binding_data["_runtime_cache"] = cache
    return cache


def validate_current_3dgs_object(mesh_obj, metadata):
    if len(mesh_obj.data.vertices) != int(metadata["mesh_vertex_count"]):
        raise ProxyBindingError("3DGS mesh vertex count changed after binding. Restore or rebind before updating.")
    if len(mesh_obj.data.polygons) != int(metadata["mesh_polygon_count"]):
        raise ProxyBindingError("3DGS mesh polygon count changed after binding. Restore or rebind before updating.")

    rest_matrix = np.array(metadata["rest_object_matrix_world"], dtype=np.float64)
    current_matrix = np.array(mesh_obj.matrix_world, dtype=np.float64)
    if not np.allclose(rest_matrix, current_matrix, atol=1e-6):
        raise ProxyBindingError(
            "3DGS object transform changed after bind. Keep the 3DGS object transform fixed and animate the proxy mesh instead."
        )


def validate_proxy_mesh(proxy_obj, metadata, current_proxy_vertices_world):
    if len(current_proxy_vertices_world) != int(metadata["proxy_vertex_count"]):
        raise ProxyBindingError(
            "Proxy mesh vertex count changed after bind. Topology-changing edits are not supported after binding."
        )
    expected_polygon_count = metadata.get("proxy_polygon_count")
    if expected_polygon_count is not None and len(proxy_obj.data.polygons) != int(expected_polygon_count):
        raise ProxyBindingError(
            "Proxy mesh polygon count changed after bind. Topology-changing edits are not supported after binding."
        )


def compute_bound_state_volumetric(
    mesh_obj,
    metadata,
    rest_state,
    binding_data,
    current_proxy_vertices_world,
    deform_mode=DEFAULT_DEFORM_MODE,
    scale_safety_mode=DEFAULT_SCALE_SAFETY_MODE,
    sh_quality_mode=DEFAULT_SH_QUALITY_MODE,
    update_sh_attributes=DEFAULT_UPDATE_SH_ATTRIBUTES,
):
    validate_current_3dgs_object(mesh_obj, metadata)
    proxy_obj = get_bound_proxy_object(metadata)
    validate_proxy_mesh(proxy_obj, metadata, current_proxy_vertices_world)
    deform_mode = normalize_deform_mode(deform_mode)
    scale_safety_mode = normalize_scale_safety_mode(scale_safety_mode)
    sh_quality_mode = normalize_sh_quality_mode(sh_quality_mode)
    update_sh_attributes = normalize_update_sh_attributes(update_sh_attributes)
    runtime_cache = get_runtime_binding_cache(mesh_obj, metadata, rest_state, binding_data)

    knn_indices = binding_data["knn_indices"]
    rest_proxy_vertices_world = binding_data["rest_proxy_vertices_world"]
    knn_weights = binding_data.get("knn_weights")
    rest_neighbor_positions = runtime_cache["rest_neighbor_positions"]
    current_neighbor_positions = current_proxy_vertices_world[knn_indices]
    object_linear_row = runtime_cache["object_linear_row"]
    object_translation_row = runtime_cache["object_translation_row"]

    if knn_weights is None:
        knn_weights = binding_data["knn_weights"]

    local_affine_world, _ = solve_weighted_affine_row(
        rest_neighbor_positions,
        current_neighbor_positions,
        knn_weights,
    )
    local_rotation_world, local_translation_world = solve_weighted_rigid_row(
        rest_neighbor_positions,
        current_neighbor_positions,
        knn_weights,
    )

    object_rotation_row = runtime_cache["object_rotation_row"]
    object_rotation_inv_row = runtime_cache["object_rotation_inv_row"]

    splat_vertex_groups = rest_state["splat_vertex_groups"]
    rest_group_positions_world = runtime_cache["rest_group_positions_world"]
    transformed_group_positions_world = np.einsum(
        "ngi,nij->ngj",
        rest_group_positions_world,
        local_rotation_world,
    ) + local_translation_world[:, None, :]

    transformed_vertex_positions_world = np.zeros_like(runtime_cache["rest_vertex_positions_world"])
    transformed_vertex_positions_world[splat_vertex_groups.reshape(-1)] = transformed_group_positions_world.reshape(-1, 3)
    transformed_vertex_positions_local = inverse_transform_points_row(
        transformed_vertex_positions_world,
        object_linear_row,
        object_translation_row,
    )

    local_rotation_local_row = np.einsum(
        "ab,nbc,cd->nad",
        object_rotation_row,
        local_rotation_world,
        object_rotation_inv_row,
    )
    local_rotation_local_col = np.transpose(local_rotation_local_row, (0, 2, 1))
    rest_rotation_matrices_local = runtime_cache["rest_rotation_matrices_local"]
    object_linear_inv_row = runtime_cache["object_linear_inv_row"]
    local_affine_local_row = np.einsum(
        "ab,nbc,cd->nad",
        object_linear_row,
        local_affine_world,
        object_linear_inv_row,
    )

    rest_row_axes_local = runtime_cache["rest_row_axes_local"]
    candidate_row_axes_local = np.einsum(
        "nri,nij->nrj",
        rest_row_axes_local,
        local_affine_local_row,
    )
    candidate_row_axes_local = orthogonalize_row_basis(candidate_row_axes_local)
    candidate_scales = np.linalg.norm(candidate_row_axes_local, axis=2)
    candidate_scales = np.clip(candidate_scales, EPSILON, None)
    candidate_row_axes_normalized = candidate_row_axes_local / candidate_scales[:, :, None]
    candidate_rotation_matrices_local = np.transpose(candidate_row_axes_normalized, (0, 2, 1))

    rigid_rotation_matrices_local = np.einsum(
        "nij,njk->nik",
        local_rotation_local_col,
        rest_rotation_matrices_local,
    )
    rigid_quaternions = rotation_matrices_to_quaternions(rigid_rotation_matrices_local)

    rest_scales = np.exp(rest_state["log_scales"])
    new_scales = compute_scale_updates(
        rest_scales,
        candidate_scales,
        local_affine_world,
        rest_proxy_vertices_world,
        current_proxy_vertices_world,
        deform_mode,
        scale_safety_mode,
    )
    new_scales = np.clip(new_scales, EPSILON, None)
    new_log_scales = np.log(new_scales)

    if deform_mode == "Elastic":
        new_rotation_matrices_local = candidate_rotation_matrices_local
        sh_rotations = nearest_rotation_matrices(local_affine_local_row)
    else:
        new_rotation_matrices_local = rigid_rotation_matrices_local
        sh_rotations = local_rotation_local_row

    new_quaternions = rotation_matrices_to_quaternions(new_rotation_matrices_local)

    center_points_world = transform_points_row(
        rest_state["logical_positions_local"],
        object_linear_row,
        object_translation_row,
    )
    center_points_world = runtime_cache["rest_center_points_world"]
    transformed_center_points_world = np.einsum(
        "ni,nij->nj",
        center_points_world,
        local_rotation_world,
    ) + local_translation_world
    transformed_center_points_local = inverse_transform_points_row(
        transformed_center_points_world,
        object_linear_row,
        object_translation_row,
    )

    new_sh_coeffs = compute_updated_sh_coeffs(
        rest_state,
        sh_rotations,
        update_sh_attributes=update_sh_attributes,
        sh_quality_mode=sh_quality_mode,
    )

    return {
        "vertex_positions_local": transformed_vertex_positions_local.astype(np.float64),
        "logical_positions_local": transformed_center_points_local.astype(np.float64),
        "log_scales": new_log_scales.astype(np.float64),
        "quaternions": new_quaternions.astype(np.float64),
        "opacities": rest_state["opacities"].astype(np.float64),
        "sh_coeffs": new_sh_coeffs.astype(np.float64),
        "sh_degree": int(rest_state["sh_degree"]),
        "splat_vertex_groups": splat_vertex_groups.astype(np.int32),
        "is_face_based": bool(rest_state["is_face_based"]),
    }


def compute_bound_state_surface(
    mesh_obj,
    metadata,
    rest_state,
    binding_data,
    current_proxy_vertices_world,
    deform_mode=DEFAULT_DEFORM_MODE,
    scale_safety_mode=DEFAULT_SCALE_SAFETY_MODE,
    sh_quality_mode=DEFAULT_SH_QUALITY_MODE,
    update_sh_attributes=DEFAULT_UPDATE_SH_ATTRIBUTES,
):
    validate_current_3dgs_object(mesh_obj, metadata)
    proxy_obj = get_bound_proxy_object(metadata)
    validate_proxy_mesh(proxy_obj, metadata, current_proxy_vertices_world)
    deform_mode = normalize_deform_mode(deform_mode)
    scale_safety_mode = normalize_scale_safety_mode(scale_safety_mode)
    sh_quality_mode = normalize_sh_quality_mode(sh_quality_mode)
    update_sh_attributes = normalize_update_sh_attributes(update_sh_attributes)
    runtime_cache = get_runtime_binding_cache(mesh_obj, metadata, rest_state, binding_data)

    surface_triangle_indices = binding_data["surface_triangle_indices"]
    surface_local_coords = binding_data["surface_local_coords"]
    rest_proxy_vertices_world = binding_data["rest_proxy_vertices_world"]

    current_triangle_vertices_world = current_proxy_vertices_world[surface_triangle_indices]
    rest_origins_world = runtime_cache["surface_rest_origins_world"]
    current_origins_world, current_bases_world = build_triangle_bases_row(current_triangle_vertices_world)
    rest_basis_inv_world = runtime_cache["surface_rest_basis_inv_world"]
    local_affine_world = np.einsum("nij,njk->nik", rest_basis_inv_world, current_bases_world)
    local_rotation_world = nearest_rotation_matrices(local_affine_world)

    object_linear_row = runtime_cache["object_linear_row"]
    object_translation_row = runtime_cache["object_translation_row"]
    object_rotation_row = runtime_cache["object_rotation_row"]
    object_rotation_inv_row = runtime_cache["object_rotation_inv_row"]
    object_linear_inv_row = runtime_cache["object_linear_inv_row"]

    transformed_center_points_world = np.einsum(
        "ni,nij->nj",
        surface_local_coords,
        current_bases_world,
    ) + current_origins_world
    transformed_center_points_local = inverse_transform_points_row(
        transformed_center_points_world,
        object_linear_row,
        object_translation_row,
    )

    splat_vertex_groups = rest_state["splat_vertex_groups"]
    rest_group_positions_world = runtime_cache["rest_group_positions_world"]
    transformed_group_positions_world = np.einsum(
        "ngi,nij->ngj",
        rest_group_positions_world - rest_origins_world[:, None, :],
        local_affine_world,
    ) + current_origins_world[:, None, :]
    transformed_vertex_positions_world = np.zeros_like(runtime_cache["rest_vertex_positions_world"])
    transformed_vertex_positions_world[splat_vertex_groups.reshape(-1)] = transformed_group_positions_world.reshape(-1, 3)
    transformed_vertex_positions_local = inverse_transform_points_row(
        transformed_vertex_positions_world,
        object_linear_row,
        object_translation_row,
    )

    local_rotation_local_row = np.einsum(
        "ab,nbc,cd->nad",
        object_rotation_row,
        local_rotation_world,
        object_rotation_inv_row,
    )
    local_rotation_local_col = np.transpose(local_rotation_local_row, (0, 2, 1))
    rest_rotation_matrices_local = runtime_cache["rest_rotation_matrices_local"]

    local_affine_local_row = np.einsum(
        "ab,nbc,cd->nad",
        object_linear_row,
        local_affine_world,
        object_linear_inv_row,
    )

    rest_row_axes_local = runtime_cache["rest_row_axes_local"]
    candidate_row_axes_local = np.einsum(
        "nri,nij->nrj",
        rest_row_axes_local,
        local_affine_local_row,
    )
    candidate_row_axes_local = orthogonalize_row_basis(candidate_row_axes_local)
    candidate_scales = np.linalg.norm(candidate_row_axes_local, axis=2)
    candidate_scales = np.clip(candidate_scales, EPSILON, None)
    candidate_row_axes_normalized = candidate_row_axes_local / candidate_scales[:, :, None]
    candidate_rotation_matrices_local = np.transpose(candidate_row_axes_normalized, (0, 2, 1))

    rigid_rotation_matrices_local = np.einsum(
        "nij,njk->nik",
        local_rotation_local_col,
        rest_rotation_matrices_local,
    )

    rest_scales = np.exp(rest_state["log_scales"])
    new_scales = compute_scale_updates(
        rest_scales,
        candidate_scales,
        local_affine_world,
        rest_proxy_vertices_world,
        current_proxy_vertices_world,
        deform_mode,
        scale_safety_mode,
    )
    new_scales = np.clip(new_scales, EPSILON, None)
    new_log_scales = np.log(new_scales)

    if deform_mode == "Elastic":
        new_rotation_matrices_local = candidate_rotation_matrices_local
        sh_rotations = nearest_rotation_matrices(local_affine_local_row)
    else:
        new_rotation_matrices_local = rigid_rotation_matrices_local
        sh_rotations = local_rotation_local_row

    new_quaternions = rotation_matrices_to_quaternions(new_rotation_matrices_local)
    new_sh_coeffs = compute_updated_sh_coeffs(
        rest_state,
        sh_rotations,
        update_sh_attributes=update_sh_attributes,
        sh_quality_mode=sh_quality_mode,
    )

    return {
        "vertex_positions_local": transformed_vertex_positions_local.astype(np.float64),
        "logical_positions_local": transformed_center_points_local.astype(np.float64),
        "log_scales": new_log_scales.astype(np.float64),
        "quaternions": new_quaternions.astype(np.float64),
        "opacities": rest_state["opacities"].astype(np.float64),
        "sh_coeffs": new_sh_coeffs.astype(np.float64),
        "sh_degree": int(rest_state["sh_degree"]),
        "splat_vertex_groups": splat_vertex_groups.astype(np.int32),
        "is_face_based": bool(rest_state["is_face_based"]),
    }


def merge_bound_states(surface_state, volumetric_state, use_surface_mask):
    use_surface_mask = np.asarray(use_surface_mask, dtype=bool)
    merged_state = {
        "vertex_positions_local": volumetric_state["vertex_positions_local"].copy(),
        "logical_positions_local": volumetric_state["logical_positions_local"].copy(),
        "log_scales": volumetric_state["log_scales"].copy(),
        "quaternions": volumetric_state["quaternions"].copy(),
        "opacities": volumetric_state["opacities"].copy(),
        "sh_coeffs": volumetric_state["sh_coeffs"].copy(),
        "sh_degree": int(volumetric_state["sh_degree"]),
        "splat_vertex_groups": volumetric_state["splat_vertex_groups"].copy(),
        "is_face_based": bool(volumetric_state["is_face_based"]),
    }

    merged_state["logical_positions_local"][use_surface_mask] = surface_state["logical_positions_local"][use_surface_mask]
    merged_state["log_scales"][use_surface_mask] = surface_state["log_scales"][use_surface_mask]
    merged_state["quaternions"][use_surface_mask] = surface_state["quaternions"][use_surface_mask]
    merged_state["opacities"][use_surface_mask] = surface_state["opacities"][use_surface_mask]
    merged_state["sh_coeffs"][use_surface_mask] = surface_state["sh_coeffs"][use_surface_mask]

    group_mask = use_surface_mask[merged_state["splat_vertex_groups"][:, 0]]
    merged_state["vertex_positions_local"][merged_state["splat_vertex_groups"][group_mask].reshape(-1)] = (
        surface_state["vertex_positions_local"][surface_state["splat_vertex_groups"][group_mask].reshape(-1)]
    )
    return merged_state


def compute_bound_state_hybrid(
    mesh_obj,
    metadata,
    rest_state,
    binding_data,
    current_proxy_vertices_world,
    deform_mode=DEFAULT_DEFORM_MODE,
    scale_safety_mode=DEFAULT_SCALE_SAFETY_MODE,
    sh_quality_mode=DEFAULT_SH_QUALITY_MODE,
    update_sh_attributes=DEFAULT_UPDATE_SH_ATTRIBUTES,
):
    use_surface_mask = np.asarray(binding_data["hybrid_use_surface"], dtype=np.int32).astype(bool)
    surface_state = compute_bound_state_surface(
        mesh_obj,
        metadata,
        rest_state,
        binding_data,
        current_proxy_vertices_world,
        deform_mode=deform_mode,
        scale_safety_mode=scale_safety_mode,
        sh_quality_mode=sh_quality_mode,
        update_sh_attributes=update_sh_attributes,
    )
    volumetric_state = compute_bound_state_volumetric(
        mesh_obj,
        metadata,
        rest_state,
        binding_data,
        current_proxy_vertices_world,
        deform_mode=deform_mode,
        scale_safety_mode=scale_safety_mode,
        sh_quality_mode=sh_quality_mode,
        update_sh_attributes=update_sh_attributes,
    )
    return merge_bound_states(surface_state, volumetric_state, use_surface_mask)


def compute_bound_state(
    mesh_obj,
    metadata,
    rest_state,
    binding_data,
    current_proxy_vertices_world,
    deform_mode=DEFAULT_DEFORM_MODE,
    scale_safety_mode=DEFAULT_SCALE_SAFETY_MODE,
    sh_quality_mode=DEFAULT_SH_QUALITY_MODE,
    update_sh_attributes=DEFAULT_UPDATE_SH_ATTRIBUTES,
):
    binding_method = get_binding_method_from_metadata(metadata)
    if binding_method == "Surface":
        return compute_bound_state_surface(
            mesh_obj,
            metadata,
            rest_state,
            binding_data,
            current_proxy_vertices_world,
            deform_mode=deform_mode,
            scale_safety_mode=scale_safety_mode,
            sh_quality_mode=sh_quality_mode,
            update_sh_attributes=update_sh_attributes,
        )
    if binding_method == "Hybrid":
        return compute_bound_state_hybrid(
            mesh_obj,
            metadata,
            rest_state,
            binding_data,
            current_proxy_vertices_world,
            deform_mode=deform_mode,
            scale_safety_mode=scale_safety_mode,
            sh_quality_mode=sh_quality_mode,
            update_sh_attributes=update_sh_attributes,
        )
    return compute_bound_state_volumetric(
        mesh_obj,
        metadata,
        rest_state,
        binding_data,
        current_proxy_vertices_world,
        deform_mode=deform_mode,
        scale_safety_mode=scale_safety_mode,
        sh_quality_mode=sh_quality_mode,
        update_sh_attributes=update_sh_attributes,
    )


def apply_bound_state(mesh_obj, state):
    write_logical_gaussian_state(mesh_obj, state)


def _pack_state_to_gaussian_texture_layout(state):
    """Pack baked state into the 59-float-per-gaussian layout used by the renderer's
    bpy.gaussian_object_cache (see src/render_comp.py 836-851 for the canonical layout).
    Layout per splat: positions[3], rotations[4], scales[3] (exp of log_scales),
    opacity[1] (sigmoid of raw), sh_coeffs[48] band-major (K bands of 3 channels each)."""
    logical_positions = np.asarray(state["logical_positions_local"], dtype=np.float32)
    quaternions = np.asarray(state["quaternions"], dtype=np.float32)
    norms = np.linalg.norm(quaternions, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    quaternions = quaternions / norms
    log_scales = np.asarray(state["log_scales"], dtype=np.float32)
    scales = np.exp(log_scales)
    opacities_raw = np.asarray(state["opacities"], dtype=np.float32).reshape(-1)
    opacities = 1.0 / (1.0 + np.exp(-opacities_raw))
    sh_coeffs_bake = np.asarray(state["sh_coeffs"], dtype=np.float32)
    N = logical_positions.shape[0]
    sh_band_major = np.transpose(sh_coeffs_bake, (0, 2, 1)).reshape(N, -1)
    out = np.zeros((N, 59), dtype=np.float32)
    out[:, 0:3] = logical_positions
    out[:, 3:7] = quaternions
    out[:, 7:10] = scales
    out[:, 10] = opacities
    sh_dim = 48
    take = min(sh_band_major.shape[1], sh_dim)
    out[:, 11:11 + take] = sh_band_major[:, :take]
    return out


def apply_baked_state_to_gpu_texture(mesh_obj, state):
    """Update the renderer's per-object gaussian_data cache entry directly so the
    next texture rebuild reflects this frame, bypassing the 18x foreach_set mesh
    attribute writes in write_logical_gaussian_state. Returns True on success,
    False if no render-side cache entry exists for mesh_obj (caller should fall
    back to apply_bound_state)."""
    cache = getattr(bpy, "gaussian_object_cache", None)
    if not cache:
        return False
    entry = cache.get(mesh_obj.name)
    if entry is None:
        source_uuid = mesh_obj.get("gaussian_source_uuid")
        if source_uuid:
            for candidate in cache.values():
                cached_obj = candidate.get("object")
                if cached_obj is None:
                    continue
                if cached_obj.get("gaussian_source_uuid") == source_uuid or cached_obj.get("source_mesh_uuid") == source_uuid:
                    entry = candidate
                    break
    if entry is None:
        return False
    packed = _pack_state_to_gaussian_texture_layout(state)
    entry["gaussian_data"] = packed
    entry["gaussian_count"] = int(packed.shape[0])
    return True


def bake_state_file_path(bake_dir, frame_number):
    return os.path.join(bake_dir, f"frame_{int(frame_number):04d}.npz")


def save_baked_state(bake_dir, frame_number, state, include_sh=True):
    os.makedirs(bake_dir, exist_ok=True)
    save_path = bake_state_file_path(bake_dir, frame_number)
    _atomic_savez_compressed(save_path, **_serialize_baked_state(state, include_sh))
    return save_path


def load_baked_state(bake_dir, frame_number, rest_state):
    bake_path = bake_state_file_path(bake_dir, frame_number)
    if not os.path.exists(bake_path):
        raise ProxyBindingError(f"No baked state found for frame {frame_number}.")
    with np.load(bake_path) as baked_npz:
        return _deserialize_baked_state(baked_npz, rest_state)


def clear_bake_dir(bake_dir):
    if not os.path.isdir(bake_dir):
        return 0
    removed = 0
    for entry in os.listdir(bake_dir):
        if entry.lower().endswith(".npz"):
            os.remove(os.path.join(bake_dir, entry))
            removed += 1
    return removed


def clear_baked_sequence_preserve_binding(mesh_obj):
    paths, metadata, _, _ = load_binding_package(mesh_obj)
    removed_files = clear_bake_dir(paths["bake_dir"])
    metadata["baked_frames"] = []
    for key in (
        "last_bake_utc",
        "last_deform_mode",
        "last_scale_safety_mode",
        "last_sh_quality_mode",
        "last_update_sh_attributes",
        "last_bake_frame_start",
        "last_bake_frame_end",
        "last_bake_frame_step",
    ):
        metadata.pop(key, None)
    save_binding_metadata(paths["json_path"], metadata)
    mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = False
    return removed_files, metadata


def resolve_bake_frame_range(scene, frame_start=None, frame_end=None, frame_step=1):
    start = scene.frame_start if frame_start is None else int(frame_start)
    end = scene.frame_end if frame_end is None else int(frame_end)
    step = int(frame_step)

    if step < 1:
        raise ProxyBindingError("frame_step must be at least 1.")
    if end < start:
        raise ProxyBindingError("frame_end must be greater than or equal to frame_start.")
    return start, end, step


def bind_3dgs_object_to_proxy(
    mesh_obj,
    proxy_input=None,
    neighbor_count=DEFAULT_NEIGHBOR_COUNT,
    binding_method=DEFAULT_BINDING_METHOD,
    hybrid_surface_distance_factor=DEFAULT_HYBRID_SURFACE_DISTANCE_FACTOR,
):
    if mesh_obj is None or getattr(mesh_obj, "type", None) != "MESH":
        raise ProxyBindingError("A valid mesh 3DGS object is required for binding.")
    if not check_mesh_has_gaussian_attributes(mesh_obj):
        raise ProxyBindingError(f"'{mesh_obj.name}' does not look like a mesh 3DGS object.")

    proxy_obj = resolve_proxy_mesh_input(proxy_input, mesh_obj)
    binding_method = normalize_binding_method(binding_method)

    existing_package_path = mesh_obj.get(PROXY_BINDING_PATH_PROP)
    if existing_package_path:
        _, missing_files = get_binding_package_missing_files(mesh_obj)
        if missing_files:
            clear_binding_state(mesh_obj, clear_package_path=True, clear_binding_method=True)

    if mesh_obj.get(PROXY_BINDING_ACTIVE_PROP):
        raise ProxyBindingError(f"'{mesh_obj.name}' is already bound. Unbind it before binding again.")

    neighbor_count = int(neighbor_count)
    if binding_method in {"Volumetric", "Hybrid"} and neighbor_count < 4:
        raise ProxyBindingError("neighbor_count must be at least 4 for stable proxy binding.")

    rest_state = read_logical_gaussian_state(mesh_obj)
    mesh_linear_row, mesh_translation_row = matrix_to_row_affine(mesh_obj.matrix_world)
    logical_points_world = transform_points_row(rest_state["logical_positions_local"], mesh_linear_row, mesh_translation_row)
    proxy_vertices_world, triangle_vertex_indices = collect_proxy_surface_geometry_world(proxy_obj)

    extra_metadata = None
    if binding_method == "Volumetric":
        if len(proxy_vertices_world) < neighbor_count:
            raise ProxyBindingError(
                f"Proxy mesh '{proxy_obj.name}' needs at least {neighbor_count} vertices for binding."
            )
        knn_indices, _ = compute_knn_indices(logical_points_world, proxy_vertices_world, neighbor_count)
        binding_payload = {
            "rest_proxy_vertices_world": proxy_vertices_world.astype(np.float32),
            "knn_indices": knn_indices.astype(np.int32),
        }
    elif binding_method == "Surface":
        binding_payload = compute_surface_binding_data(
            logical_points_world,
            proxy_vertices_world,
            triangle_vertex_indices,
        )
        binding_payload = {
            key: value.astype(np.float32) if value.dtype.kind == "f" else value.astype(np.int32)
            for key, value in binding_payload.items()
        }
    else:
        if len(proxy_vertices_world) < neighbor_count:
            raise ProxyBindingError(
                f"Proxy mesh '{proxy_obj.name}' needs at least {neighbor_count} vertices for binding."
            )
        binding_payload, extra_metadata = compute_hybrid_binding_data(
            logical_points_world,
            proxy_vertices_world,
            triangle_vertex_indices,
            neighbor_count,
            hybrid_surface_distance_factor=hybrid_surface_distance_factor,
        )

    metadata = save_binding_package(
        mesh_obj,
        proxy_obj,
        rest_state,
        binding_method,
        binding_payload,
        extra_metadata=extra_metadata,
    )
    return mesh_obj, proxy_obj, metadata


def bind_active_3dgs_to_selected_proxy(
    neighbor_count=DEFAULT_NEIGHBOR_COUNT,
    proxy_input=None,
    binding_method=DEFAULT_BINDING_METHOD,
    hybrid_surface_distance_factor=DEFAULT_HYBRID_SURFACE_DISTANCE_FACTOR,
):
    mesh_obj = get_active_3dgs_mesh_object(require_bound=False)
    return bind_3dgs_object_to_proxy(
        mesh_obj,
        proxy_input=proxy_input,
        neighbor_count=neighbor_count,
        binding_method=binding_method,
        hybrid_surface_distance_factor=hybrid_surface_distance_factor,
    )


def restore_original_bound_state(mesh_obj):
    _, metadata, rest_state, _ = load_binding_package(mesh_obj)
    validate_current_3dgs_object(mesh_obj, metadata)
    apply_bound_state(mesh_obj, rest_state)
    mesh_obj[PROXY_BINDING_ACTIVE_PROP] = False
    return rest_state


def update_bound_3dgs_from_proxy(mesh_obj):
    _, metadata, rest_state, binding_data = load_binding_package(mesh_obj)
    if not mesh_obj.get(PROXY_BINDING_ACTIVE_PROP):
        raise ProxyBindingError(f"'{mesh_obj.name}' is not currently active as a live proxy binding.")
    proxy_obj = get_bound_proxy_object(metadata)
    current_proxy_vertices_world = collect_proxy_vertices_world(proxy_obj)
    state = compute_bound_state(
        mesh_obj,
        metadata,
        rest_state,
        binding_data,
        current_proxy_vertices_world,
    )
    apply_bound_state(mesh_obj, state)
    return proxy_obj, state


def update_bound_3dgs_from_proxy_with_options(
    mesh_obj,
    deform_mode=DEFAULT_DEFORM_MODE,
    scale_safety_mode=DEFAULT_SCALE_SAFETY_MODE,
    sh_quality_mode=DEFAULT_SH_QUALITY_MODE,
    update_sh_attributes=DEFAULT_UPDATE_SH_ATTRIBUTES,
):
    _, metadata, rest_state, binding_data = load_binding_package(mesh_obj)
    if not mesh_obj.get(PROXY_BINDING_ACTIVE_PROP):
        raise ProxyBindingError(f"'{mesh_obj.name}' is not currently active as a live proxy binding.")
    proxy_obj = get_bound_proxy_object(metadata)
    current_proxy_vertices_world = collect_proxy_vertices_world(proxy_obj)
    state = compute_bound_state(
        mesh_obj,
        metadata,
        rest_state,
        binding_data,
        current_proxy_vertices_world,
        deform_mode=deform_mode,
        scale_safety_mode=scale_safety_mode,
        sh_quality_mode=sh_quality_mode,
        update_sh_attributes=update_sh_attributes,
    )
    apply_bound_state(mesh_obj, state)
    return proxy_obj, state


def bake_bound_animation(mesh_obj, frame_start=None, frame_end=None, frame_step=1):
    paths, metadata, rest_state, binding_data = load_binding_package(mesh_obj)
    if not mesh_obj.get(PROXY_BINDING_ACTIVE_PROP):
        raise ProxyBindingError(f"'{mesh_obj.name}' is not currently active as a live proxy binding.")

    proxy_obj = get_bound_proxy_object(metadata)
    scene = bpy.context.scene
    original_frame = int(scene.frame_current)
    removed_files = clear_bake_dir(paths["bake_dir"])
    metadata["baked_frames"] = []
    mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = False
    save_binding_metadata(paths["json_path"], metadata)
    resolved_frame_start, resolved_frame_end, resolved_frame_step = resolve_bake_frame_range(
        scene,
        frame_start=frame_start,
        frame_end=frame_end,
        frame_step=frame_step,
    )

    baked_frames = []
    try:
        for frame_number in range(resolved_frame_start, resolved_frame_end + 1, resolved_frame_step):
            scene.frame_set(frame_number)
            current_proxy_vertices_world = collect_proxy_vertices_world(proxy_obj)
            state = compute_bound_state(mesh_obj, metadata, rest_state, binding_data, current_proxy_vertices_world)
            save_baked_state(paths["bake_dir"], frame_number, state, include_sh=True)
            baked_frames.append(int(frame_number))
    finally:
        scene.frame_set(original_frame)

    metadata["baked_frames"] = baked_frames
    metadata["last_bake_utc"] = _utc_now_iso()
    metadata["last_bake_frame_start"] = int(resolved_frame_start)
    metadata["last_bake_frame_end"] = int(resolved_frame_end)
    metadata["last_bake_frame_step"] = int(resolved_frame_step)
    save_binding_metadata(paths["json_path"], metadata)
    mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = bool(baked_frames)
    return proxy_obj, baked_frames, removed_files


def bake_bound_animation_with_options(
    mesh_obj,
    deform_mode=DEFAULT_DEFORM_MODE,
    scale_safety_mode=DEFAULT_SCALE_SAFETY_MODE,
    sh_quality_mode=DEFAULT_SH_QUALITY_MODE,
    update_sh_attributes=DEFAULT_UPDATE_SH_ATTRIBUTES,
    show_bake_progress_overlay=True,
    frame_start=None,
    frame_end=None,
    frame_step=1,
):
    paths, metadata, rest_state, binding_data = load_binding_package(mesh_obj)
    if not mesh_obj.get(PROXY_BINDING_ACTIVE_PROP):
        raise ProxyBindingError(f"'{mesh_obj.name}' is not currently active as a live proxy binding.")

    show_bake_progress_overlay = normalize_update_sh_attributes(show_bake_progress_overlay)
    include_sh_in_baked_frames = normalize_update_sh_attributes(update_sh_attributes)
    proxy_obj = get_bound_proxy_object(metadata)
    scene = bpy.context.scene
    original_frame = int(scene.frame_current)
    removed_files = clear_bake_dir(paths["bake_dir"])
    metadata["baked_frames"] = []
    mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = False
    save_binding_metadata(paths["json_path"], metadata)
    resolved_frame_start, resolved_frame_end, resolved_frame_step = resolve_bake_frame_range(
        scene,
        frame_start=frame_start,
        frame_end=frame_end,
        frame_step=frame_step,
    )

    frame_numbers = list(range(resolved_frame_start, resolved_frame_end + 1, resolved_frame_step))
    if show_bake_progress_overlay:
        begin_bake_progress_overlay(
            total_steps=len(frame_numbers),
            object_name=mesh_obj.name,
            title="3DGS Bake Progress",
        )

    baked_frames = []
    try:
        for step_index, frame_number in enumerate(frame_numbers, start=1):
            scene.frame_set(frame_number)
            current_proxy_vertices_world = collect_proxy_vertices_world(proxy_obj)
            state = compute_bound_state(
                mesh_obj,
                metadata,
                rest_state,
                binding_data,
                current_proxy_vertices_world,
                deform_mode=deform_mode,
                scale_safety_mode=scale_safety_mode,
                sh_quality_mode=sh_quality_mode,
                update_sh_attributes=update_sh_attributes,
            )
            save_baked_state(paths["bake_dir"], frame_number, state, include_sh=include_sh_in_baked_frames)
            baked_frames.append(int(frame_number))
            if show_bake_progress_overlay:
                update_bake_progress_overlay(
                    current_step=step_index,
                    total_steps=len(frame_numbers),
                    frame_number=frame_number,
                    status_message=f"Baked frame {frame_number}",
                )
    finally:
        scene.frame_set(original_frame)
        if show_bake_progress_overlay:
            end_bake_progress_overlay(
                status_message=f"Finished baking {len(baked_frames)} frame(s) for {mesh_obj.name}."
            )

    metadata["baked_frames"] = baked_frames
    metadata["last_bake_utc"] = _utc_now_iso()
    metadata["last_deform_mode"] = normalize_deform_mode(deform_mode)
    metadata["last_scale_safety_mode"] = normalize_scale_safety_mode(scale_safety_mode)
    metadata["last_sh_quality_mode"] = normalize_sh_quality_mode(sh_quality_mode)
    metadata["last_update_sh_attributes"] = normalize_update_sh_attributes(update_sh_attributes)
    metadata["last_bake_frame_start"] = int(resolved_frame_start)
    metadata["last_bake_frame_end"] = int(resolved_frame_end)
    metadata["last_bake_frame_step"] = int(resolved_frame_step)
    save_binding_metadata(paths["json_path"], metadata)
    mesh_obj[PROXY_SEQUENCE_BINDING_PROP] = bool(baked_frames)
    return proxy_obj, baked_frames, removed_files


def apply_baked_frame_to_mesh(mesh_obj, frame_number):
    paths, metadata, rest_state, _ = load_binding_package(mesh_obj)
    validate_current_3dgs_object(mesh_obj, metadata)
    state = load_baked_state(paths["bake_dir"], frame_number, rest_state)
    used_fast_path = False
    scene = getattr(bpy.context, "scene", None)
    if scene is not None and scene.get("__proxy_render_fast_path", False):
        used_fast_path = apply_baked_state_to_gpu_texture(mesh_obj, state)
    if not used_fast_path:
        apply_bound_state(mesh_obj, state)
    else:
        if not hasattr(bpy, "_proxy_render_fast_path_uuids"):
            bpy._proxy_render_fast_path_uuids = set()
        source_uuid = mesh_obj.get("gaussian_source_uuid")
        if source_uuid:
            bpy._proxy_render_fast_path_uuids.add(source_uuid)
    return state
