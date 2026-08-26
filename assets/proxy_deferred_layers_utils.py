import importlib.util
import json
import math
import os
import tempfile
import uuid
from datetime import datetime, timezone

import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

try:
    import blf
except Exception:
    blf = None

try:
    from bpy.app.handlers import persistent
except Exception:
    def persistent(function):
        return function


DEFAULT_PROXY_BINDING_UTILS_PATH = (
    "D:/GithubRepos/3DGS Render_Render Updates/rigging/proxy_binding_utils.py"
)
DEFAULT_RELIGHT_CACHE_ROOT = "D:/GithubRepos/3DGS Render_Render Updates/relighting"

PROXY_RELIGHT_STAGE_SAVED_PROP = "proxy_deferred_relight_stage_saved"
PROXY_RELIGHT_STAGE_BAKED_PROP = "proxy_deferred_relight_stage_baked"

PROXY_RELIGHT_METADATA_FILENAME = "proxy_deferred_relight.json"
PROXY_RELIGHT_STATE_FILENAME = "original_color_state.npz"
PROXY_RELIGHT_BAKE_METADATA_FILENAME = "baked_lighting_cache.json"
PROXY_RELIGHT_BAKE_STATE_FILENAME = "baked_lighting_cache.npz"

DEFAULT_BASE_COLOR_ATTR = "proxy_deferred_relight_base_color"
DEFAULT_DIRECT_COLOR_ATTR = "proxy_deferred_relight_direct_color"
DEFAULT_INDIRECT_COLOR_ATTR = "proxy_deferred_relight_indirect_color"
DEFAULT_SHADOW_FACTOR_ATTR = "proxy_deferred_relight_shadow_factor"
DEFAULT_OCCLUSION_FACTOR_ATTR = "proxy_deferred_relight_occlusion_factor"
DEFAULT_LIGHT_TINT_ATTR = "proxy_deferred_relight_light_tint_color"
DEFAULT_LIGHT_FACTOR_ATTR = "proxy_deferred_relight_combined_light_factor"
DEFAULT_RELIT_COLOR_ATTR = "proxy_deferred_relight_final_color"
LAYER_SCHEMA_VERSION = "1"

SH_C0 = 0.28209479177387814
EPSILON = 1.0e-8

PROGRESS_STATE_KEY = "_proxy_deferred_relight_progress_state"
PROGRESS_HANDLER_KEY = "_proxy_deferred_relight_progress_draw_handler"


def _driver_namespace():
    try:
        return bpy.app.driver_namespace
    except Exception:
        return {}


def get_proxy_deferred_progress_state():
    namespace = _driver_namespace()
    state = namespace.get(PROGRESS_STATE_KEY)
    if not isinstance(state, dict):
        state = {
            "active": False,
            "title": "Proxy Deferred Relight",
            "object_name": "",
            "current_step": 0,
            "total_steps": 1,
            "status_message": "",
        }
        namespace[PROGRESS_STATE_KEY] = state
    return state


def iter_view3d_areas():
    window_manager = getattr(bpy.context, "window_manager", None)
    if window_manager is None:
        return []
    areas = []
    for window in getattr(window_manager, "windows", []):
        screen = getattr(window, "screen", None)
        if screen is None:
            continue
        for area in getattr(screen, "areas", []):
            if getattr(area, "type", None) == "VIEW_3D":
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
    if getattr(bpy.app, "background", False):
        return
    try:
        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
    except Exception:
        pass


def _draw_proxy_deferred_progress_overlay():
    if blf is None:
        return
    state = get_proxy_deferred_progress_state()
    if not state.get("active", False):
        return

    total_steps = max(int(state.get("total_steps", 1)), 1)
    current_step = max(0, min(int(state.get("current_step", 0)), total_steps))
    percent = (float(current_step) / float(total_steps)) * 100.0
    title = str(state.get("title", "Proxy Deferred Relight"))
    object_name = str(state.get("object_name", ""))
    status_message = str(state.get("status_message", ""))

    lines = [
        title,
        f"Object: {object_name}" if object_name else "Object: (not set)",
        f"Progress: {current_step}/{total_steps} ({percent:.1f}%)",
    ]
    if status_message:
        lines.append(status_message)

    font_id = 0
    x = 24
    y = 92
    line_height = 22

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


def end_proxy_deferred_progress_overlay(status_message="", clear_message=False):
    namespace = _driver_namespace()
    state = get_proxy_deferred_progress_state()
    if status_message and not clear_message:
        state["status_message"] = str(status_message)
        force_viewport_redraw()

    handle = namespace.get(PROGRESS_HANDLER_KEY)
    if handle is not None:
        try:
            bpy.types.SpaceView3D.draw_handler_remove(handle, "WINDOW")
        except Exception:
            pass
        namespace[PROGRESS_HANDLER_KEY] = None

    window_manager = getattr(bpy.context, "window_manager", None)
    if window_manager is not None:
        try:
            window_manager.progress_end()
        except Exception:
            pass

    state["active"] = False
    state["current_step"] = 0
    if clear_message:
        state["status_message"] = ""
    force_viewport_redraw()


@persistent
def _cleanup_proxy_deferred_progress_overlay_on_load(_dummy=None):
    try:
        end_proxy_deferred_progress_overlay(clear_message=True)
    except Exception:
        pass


_cleanup_proxy_deferred_progress_overlay_on_load._proxy_deferred_progress_cleanup = True


def ensure_proxy_deferred_progress_cleanup_handler():
    try:
        handlers = bpy.app.handlers.load_pre
    except Exception:
        return
    for handler in list(handlers):
        if getattr(handler, "_proxy_deferred_progress_cleanup", False):
            return
    try:
        handlers.append(_cleanup_proxy_deferred_progress_overlay_on_load)
    except Exception:
        pass


def begin_proxy_deferred_progress_overlay(total_steps, object_name="", title="Proxy Deferred Relight"):
    namespace = _driver_namespace()
    end_proxy_deferred_progress_overlay(clear_message=True)
    ensure_proxy_deferred_progress_cleanup_handler()

    state = get_proxy_deferred_progress_state()
    state["active"] = True
    state["title"] = str(title)
    state["object_name"] = str(object_name) if object_name else ""
    state["current_step"] = 0
    state["total_steps"] = max(int(total_steps), 1)
    state["status_message"] = "Preparing..."

    window_manager = getattr(bpy.context, "window_manager", None)
    if window_manager is not None:
        try:
            window_manager.progress_begin(0, state["total_steps"])
            window_manager.progress_update(0)
        except Exception:
            pass

    if (
        blf is not None
        and not getattr(bpy.app, "background", False)
        and namespace.get(PROGRESS_HANDLER_KEY) is None
        and iter_view3d_areas()
    ):
        try:
            namespace[PROGRESS_HANDLER_KEY] = bpy.types.SpaceView3D.draw_handler_add(
                _draw_proxy_deferred_progress_overlay,
                (),
                "WINDOW",
                "POST_PIXEL",
            )
        except Exception:
            namespace[PROGRESS_HANDLER_KEY] = None

    force_viewport_redraw()


def update_proxy_deferred_progress_overlay(current_step, total_steps=None, status_message=""):
    state = get_proxy_deferred_progress_state()
    if total_steps is not None:
        state["total_steps"] = max(int(total_steps), 1)
    state["current_step"] = max(0, int(current_step))
    if status_message:
        state["status_message"] = str(status_message)

    window_manager = getattr(bpy.context, "window_manager", None)
    if window_manager is not None:
        try:
            window_manager.progress_update(min(state["current_step"], state["total_steps"]))
        except Exception:
            pass

    force_viewport_redraw()


def call_progress_callback(progress_callback, current_step, total_steps, status_message=""):
    if progress_callback is None:
        return
    try:
        progress_callback(current_step, total_steps, status_message=status_message)
    except TypeError:
        try:
            progress_callback(current_step, total_steps, status_message)
        except TypeError:
            progress_callback(current_step, total_steps)

POINT_ATTR_SPECS = {
    "FLOAT": {"prop": "value", "components": 1, "dtype": np.float32},
    "FLOAT_VECTOR": {"prop": "vector", "components": 3, "dtype": np.float32},
    "FLOAT_COLOR": {"prop": "color", "components": 4, "dtype": np.float32},
}

_PROXY_BINDING_UTILS_MODULE = None
_PROXY_BINDING_UTILS_MODULE_PATH = None

LEGACY_RELIGHT_OBJECT_PROPS = (
    "proxy_deferred_relight_package_path",
    "proxy_deferred_relight_original_saved",
    "proxy_deferred_relight_object_uuid",
    "proxy_deferred_relight_layers_present",
    "proxy_deferred_relight_layers_version",
    "proxy_deferred_relight_composite_present",
    "proxy_deferred_relight_has_base_color_layer",
    "proxy_deferred_relight_has_direct_color_layer",
    "proxy_deferred_relight_has_indirect_color_layer",
    "proxy_deferred_relight_has_shadow_factor_layer",
    "proxy_deferred_relight_has_occlusion_factor_layer",
    "proxy_deferred_relight_has_light_tint_layer",
    "proxy_deferred_relight_has_final_color_layer",
    "proxy_deferred_relight_stage_written",
    "proxy_deferred_relight_stage_saved_at",
    "proxy_deferred_relight_stage_baked_at",
    "proxy_deferred_relight_stage_written_at",
    "proxy_deferred_relight_last_export_mode",
    "proxy_deferred_relight_has_gn_layer_mixer",
    "proxy_deferred_relight_gn_layer_mixer_version",
    "proxy_deferred_relight_gn_layer_mixer_modifier",
    "proxy_deferred_relight_gn_layer_mixer_group",
    "proxy_deferred_relight_has_gn_bakematch_mixer",
    "proxy_deferred_relight_gn_bakematch_mixer_version",
    "proxy_deferred_relight_gn_bakematch_modifier",
    "proxy_deferred_relight_gn_bakematch_group",
)


class ProxySurfaceRelightError(RuntimeError):
    pass


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_name(name):
    sanitized = "".join(
        character if character.isalnum() or character in ("-", "_") else "_"
        for character in str(name)
    )
    sanitized = sanitized.strip("_")
    return sanitized or "object"


def load_proxy_binding_utils(proxy_binding_utils_path=""):
    global _PROXY_BINDING_UTILS_MODULE
    global _PROXY_BINDING_UTILS_MODULE_PATH

    requested_path = str(proxy_binding_utils_path).strip() or DEFAULT_PROXY_BINDING_UTILS_PATH
    requested_path = os.path.normpath(requested_path)

    if (
        _PROXY_BINDING_UTILS_MODULE is not None
        and _PROXY_BINDING_UTILS_MODULE_PATH == requested_path
    ):
        return _PROXY_BINDING_UTILS_MODULE

    if not os.path.isfile(requested_path):
        raise ProxySurfaceRelightError(
            f"proxy_binding_utils.py was not found at '{requested_path}'."
        )

    spec = importlib.util.spec_from_file_location(
        "proxy_surface_relight_proxy_binding_utils_runtime",
        requested_path,
    )
    if spec is None or spec.loader is None:
        raise ProxySurfaceRelightError(
            f"Could not load proxy_binding_utils.py from '{requested_path}'."
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _PROXY_BINDING_UTILS_MODULE = module
    _PROXY_BINDING_UTILS_MODULE_PATH = requested_path
    return module


def resolve_target_mesh_object(
    target_mode="Active",
    target_obj=None,
    proxy_binding_utils_path="",
):
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    mode = str(target_mode).strip().lower().replace("_", " ")
    if mode in ("", "active"):
        return proxy_utils.get_active_3dgs_mesh_object(require_bound=False)
    if mode in ("input object", "input", "object", "target object"):
        return proxy_utils.get_input_3dgs_mesh_object(target_obj, require_bound=False)
    raise ProxySurfaceRelightError(
        f"Unsupported target_mode '{target_mode}'. Use Active or Input Object."
    )


def resolve_proxy_mesh_object(
    mesh_obj,
    proxy_obj=None,
    proxy_binding_utils_path="",
):
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    if proxy_obj is not None:
        if isinstance(proxy_obj, str):
            proxy_name = proxy_obj.strip()
            if not proxy_name:
                raise ProxySurfaceRelightError(
                    "proxy_obj cannot be blank when provided as a string."
                )
            resolved_obj = bpy.data.objects.get(proxy_name)
            if resolved_obj is None:
                raise ProxySurfaceRelightError(f"Proxy mesh '{proxy_name}' was not found.")
        else:
            resolved_obj = proxy_obj
        if getattr(resolved_obj, "type", None) != "MESH":
            raise ProxySurfaceRelightError("proxy_obj must point to a mesh object.")
        return resolved_obj

    package_path = str(mesh_obj.get(proxy_utils.PROXY_BINDING_PATH_PROP, "")).strip()
    if not package_path:
        raise ProxySurfaceRelightError(
            f"'{mesh_obj.name}' is not proxy-bound, so proxy_obj must be provided explicitly."
        )

    _, metadata, _, _ = proxy_utils.load_binding_package(mesh_obj)
    return proxy_utils.get_bound_proxy_object(metadata)


def get_relight_cache_base_dir(relight_cache_root=""):
    root = str(relight_cache_root).strip()
    if root:
        if os.path.splitext(root)[1].lower() == ".py":
            root = os.path.dirname(root)
    else:
        blend_path = bpy.data.filepath
        if blend_path:
            root = os.path.dirname(blend_path)
        else:
            root = tempfile.gettempdir()
    return os.path.join(root, "_3dgs_proxy_deferred_relighting")


def clear_legacy_relight_properties(mesh_obj):
    for property_name in LEGACY_RELIGHT_OBJECT_PROPS:
        if property_name in mesh_obj:
            del mesh_obj[property_name]


def find_matching_relight_package_dirs(mesh_obj, relight_cache_root=""):
    base_dir = get_relight_cache_base_dir(relight_cache_root)
    if not os.path.isdir(base_dir):
        return []

    object_name = str(mesh_obj.name)
    sanitized_prefix = f"{sanitize_name(object_name)}_"
    matches = []
    for entry_name in os.listdir(base_dir):
        package_dir = os.path.join(base_dir, entry_name)
        if not os.path.isdir(package_dir):
            continue
        if not entry_name.startswith(sanitized_prefix):
            continue

        metadata_path = os.path.join(package_dir, PROXY_RELIGHT_METADATA_FILENAME)
        bake_metadata_path = os.path.join(package_dir, PROXY_RELIGHT_BAKE_METADATA_FILENAME)
        if os.path.isfile(metadata_path):
            candidate_metadata_path = metadata_path
        elif os.path.isfile(bake_metadata_path):
            candidate_metadata_path = bake_metadata_path
        else:
            continue

        try:
            metadata = read_json_file(candidate_metadata_path)
        except Exception:
            continue

        if str(metadata.get("object_name", "")).strip() != object_name:
            continue

        saved_at = str(metadata.get("saved_at_utc", metadata.get("baked_at_utc", ""))).strip()
        try:
            sort_time = datetime.strptime(saved_at, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            ).timestamp()
        except Exception:
            sort_time = float(os.path.getmtime(candidate_metadata_path))
        matches.append((sort_time, package_dir))

    matches.sort(key=lambda item: item[0], reverse=True)
    return [package_dir for _, package_dir in matches]


def get_relight_package_dir(mesh_obj, relight_cache_root="", create=False):
    matches = find_matching_relight_package_dirs(mesh_obj, relight_cache_root=relight_cache_root)
    if matches:
        package_dir = matches[0]
        if create:
            os.makedirs(package_dir, exist_ok=True)
        return package_dir

    if not create:
        return ""

    base_dir = get_relight_cache_base_dir(relight_cache_root)
    package_name = f"{sanitize_name(mesh_obj.name)}_{uuid.uuid4()}"
    package_dir = os.path.join(base_dir, package_name)
    if create:
        os.makedirs(package_dir, exist_ok=True)
    return package_dir


def get_relight_file_paths(mesh_obj, relight_cache_root="", create=False):
    package_dir = get_relight_package_dir(
        mesh_obj,
        relight_cache_root=relight_cache_root,
        create=create,
    )
    if not package_dir:
        package_dir = os.path.join(
            get_relight_cache_base_dir(relight_cache_root),
            f"{sanitize_name(mesh_obj.name)}_unresolved",
        )
    return {
        "package_dir": package_dir,
        "metadata_path": os.path.join(package_dir, PROXY_RELIGHT_METADATA_FILENAME),
        "state_path": os.path.join(package_dir, PROXY_RELIGHT_STATE_FILENAME),
        "bake_metadata_path": os.path.join(package_dir, PROXY_RELIGHT_BAKE_METADATA_FILENAME),
        "bake_state_path": os.path.join(package_dir, PROXY_RELIGHT_BAKE_STATE_FILENAME),
    }


def write_json_file(json_path, data):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)


def read_json_file(json_path):
    with open(json_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_saved_color_state(mesh_obj, relight_cache_root=""):
    paths = get_relight_file_paths(mesh_obj, relight_cache_root=relight_cache_root, create=False)
    if not os.path.exists(paths["metadata_path"]):
        raise ProxySurfaceRelightError(f"Proxy relight metadata is missing for '{mesh_obj.name}'.")
    if not os.path.exists(paths["state_path"]):
        raise ProxySurfaceRelightError(
            f"Original proxy relight color state is missing for '{mesh_obj.name}'."
        )

    metadata = read_json_file(paths["metadata_path"])
    with np.load(paths["state_path"]) as state_npz:
        state = {
            "sh_coeffs": state_npz["sh_coeffs"].astype(np.float64),
            "logical_count": int(state_npz["logical_count"][0]),
            "sh_degree": int(state_npz["sh_degree"][0]),
        }
    return paths, metadata, state


def load_baked_lighting_cache(mesh_obj, relight_cache_root=""):
    paths = get_relight_file_paths(mesh_obj, relight_cache_root=relight_cache_root, create=False)
    if not os.path.exists(paths["bake_metadata_path"]):
        raise ProxySurfaceRelightError(
            f"Baked proxy deferred relight metadata is missing for '{mesh_obj.name}'."
        )
    if not os.path.exists(paths["bake_state_path"]):
        raise ProxySurfaceRelightError(
            f"Baked proxy deferred relight cache is missing for '{mesh_obj.name}'."
        )

    metadata = read_json_file(paths["bake_metadata_path"])
    with np.load(paths["bake_state_path"]) as bake_npz:
        cache = {
            "base_color": np.asarray(bake_npz["base_color"], dtype=np.float64),
            "indirect_color": np.asarray(bake_npz["indirect_color"], dtype=np.float64),
            "direct_color": np.asarray(bake_npz["direct_color"], dtype=np.float64),
            "occlusion_factor": np.asarray(bake_npz["occlusion_factor"], dtype=np.float64),
            "shadow_factor": np.asarray(bake_npz["shadow_factor"], dtype=np.float64),
            "logical_count": int(bake_npz["logical_count"][0]),
        }
    return paths, metadata, cache


def save_baked_lighting_cache(mesh_obj, cache, metadata, relight_cache_root=""):
    paths = get_relight_file_paths(mesh_obj, relight_cache_root=relight_cache_root, create=True)
    os.makedirs(paths["package_dir"], exist_ok=True)
    np.savez(
        paths["bake_state_path"],
        base_color=np.asarray(cache["base_color"], dtype=np.float32),
        indirect_color=np.asarray(cache["indirect_color"], dtype=np.float32),
        direct_color=np.asarray(cache["direct_color"], dtype=np.float32),
        occlusion_factor=np.asarray(cache["occlusion_factor"], dtype=np.float32),
        shadow_factor=np.asarray(cache["shadow_factor"], dtype=np.float32),
        logical_count=np.asarray([int(cache["logical_count"])], dtype=np.int32),
    )
    write_json_file(paths["bake_metadata_path"], metadata)
    sync_stage_state_properties(mesh_obj, relight_cache_root=relight_cache_root)
    return paths


def clear_saved_color_state(mesh_obj, relight_cache_root="", keep_package_path=False):
    package_dir = get_relight_package_dir(
        mesh_obj,
        relight_cache_root=relight_cache_root,
        create=False,
    )
    removed_files = []
    if package_dir and os.path.isdir(package_dir):
        for file_name in (PROXY_RELIGHT_METADATA_FILENAME, PROXY_RELIGHT_STATE_FILENAME):
            file_path = os.path.join(package_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                removed_files.append(file_path)
        try:
            if os.path.isdir(package_dir) and not os.listdir(package_dir):
                os.rmdir(package_dir)
        except Exception:
            pass

    sync_stage_state_properties(mesh_obj, relight_cache_root=relight_cache_root)
    clear_legacy_relight_properties(mesh_obj)
    return removed_files


def get_point_attr_spec(data_type):
    if data_type not in POINT_ATTR_SPECS:
        raise ProxySurfaceRelightError(f"Unsupported point attribute type '{data_type}'.")
    return POINT_ATTR_SPECS[data_type]


def ensure_point_attribute(mesh_data, attr_name, data_type):
    if attr_name in mesh_data.attributes:
        attr = mesh_data.attributes[attr_name]
        if attr.domain != "POINT":
            raise ProxySurfaceRelightError(
                f"Attribute '{attr_name}' must be on the POINT domain."
            )
        if attr.data_type != data_type:
            mesh_data.attributes.remove(attr)
        else:
            return attr
    return mesh_data.attributes.new(attr_name, data_type, "POINT")


def remove_point_attribute(mesh_data, attr_name):
    if attr_name in mesh_data.attributes:
        mesh_data.attributes.remove(mesh_data.attributes[attr_name])
        return True
    return False


def clear_temp_attributes(mesh_obj, attr_names=None):
    attr_names = attr_names or [
        DEFAULT_BASE_COLOR_ATTR,
        DEFAULT_DIRECT_COLOR_ATTR,
        DEFAULT_INDIRECT_COLOR_ATTR,
        DEFAULT_SHADOW_FACTOR_ATTR,
        DEFAULT_OCCLUSION_FACTOR_ATTR,
        DEFAULT_LIGHT_TINT_ATTR,
        DEFAULT_LIGHT_FACTOR_ATTR,
        DEFAULT_RELIT_COLOR_ATTR,
    ]
    removed = []
    for attr_name in attr_names:
        if remove_point_attribute(mesh_obj.data, attr_name):
            removed.append(attr_name)
    if removed:
        mesh_obj.data.update()
    return removed


def set_layer_state_properties(
    mesh_obj,
    **_kwargs,
):
    clear_legacy_relight_properties(mesh_obj)


def set_stage_state_properties(
    mesh_obj,
    *,
    saved=None,
    baked=None,
):
    if saved is not None:
        mesh_obj[PROXY_RELIGHT_STAGE_SAVED_PROP] = bool(saved)

    if baked is not None:
        mesh_obj[PROXY_RELIGHT_STAGE_BAKED_PROP] = bool(baked)

    clear_legacy_relight_properties(mesh_obj)


def sync_stage_state_properties(mesh_obj, relight_cache_root=""):
    paths = get_relight_file_paths(mesh_obj, relight_cache_root=relight_cache_root, create=False)
    saved_present = os.path.exists(paths["metadata_path"]) and os.path.exists(paths["state_path"])
    baked_present = os.path.exists(paths["bake_metadata_path"]) and os.path.exists(paths["bake_state_path"])
    set_stage_state_properties(mesh_obj, saved=saved_present, baked=baked_present)


def clear_stage_state_properties(mesh_obj):
    for property_name in (
        PROXY_RELIGHT_STAGE_SAVED_PROP,
        PROXY_RELIGHT_STAGE_BAKED_PROP,
    ):
        if property_name in mesh_obj:
            del mesh_obj[property_name]
    clear_legacy_relight_properties(mesh_obj)


def clear_layer_state_properties(mesh_obj):
    clear_legacy_relight_properties(mesh_obj)


def write_logical_point_attribute(
    mesh_obj,
    attr_name,
    logical_values,
    data_type="FLOAT_COLOR",
    proxy_binding_utils_path="",
):
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    mesh_data = mesh_obj.data
    splat_vertex_groups, _ = proxy_utils.get_splat_vertex_groups(mesh_data)
    num_vertices = len(mesh_data.vertices)
    spec = get_point_attr_spec(data_type)

    logical_values = np.asarray(logical_values, dtype=np.float32)
    if spec["components"] == 1:
        logical_values = logical_values.reshape(-1, 1)
    elif data_type == "FLOAT_VECTOR":
        logical_values = logical_values.reshape(-1, 3)
    elif data_type == "FLOAT_COLOR":
        logical_values = logical_values.reshape(len(logical_values), -1)
        if logical_values.shape[1] == 3:
            alpha = np.ones((len(logical_values), 1), dtype=np.float32)
            logical_values = np.concatenate([logical_values, alpha], axis=1)
        elif logical_values.shape[1] != 4:
            raise ProxySurfaceRelightError(
                f"Attribute '{attr_name}' expects 3 or 4 color components."
            )

    if logical_values.shape[0] != len(splat_vertex_groups):
        raise ProxySurfaceRelightError(
            f"Attribute '{attr_name}' has {logical_values.shape[0]} logical values, expected {len(splat_vertex_groups)}."
        )

    vertex_values = proxy_utils.scatter_logical_to_vertices(
        logical_values,
        splat_vertex_groups,
        num_vertices,
    ).astype(spec["dtype"], copy=False)

    attr = ensure_point_attribute(mesh_data, attr_name, data_type)
    attr.data.foreach_set(spec["prop"], vertex_values.reshape(-1))
    mesh_data.update()


def read_logical_point_attribute(mesh_obj, attr_name, proxy_binding_utils_path=""):
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    mesh_data = mesh_obj.data
    if attr_name not in mesh_data.attributes:
        raise ProxySurfaceRelightError(
            f"Attribute '{attr_name}' was not found on '{mesh_obj.name}'."
        )

    attr = mesh_data.attributes[attr_name]
    if attr.domain != "POINT":
        raise ProxySurfaceRelightError(
            f"Attribute '{attr_name}' must be a POINT attribute."
        )

    spec = get_point_attr_spec(attr.data_type)
    raw = np.empty(len(attr.data) * spec["components"], dtype=np.float32)
    attr.data.foreach_get(spec["prop"], raw)
    if spec["components"] > 1:
        raw = raw.reshape(-1, spec["components"])

    splat_vertex_groups, _ = proxy_utils.get_splat_vertex_groups(mesh_data)
    logical = raw[splat_vertex_groups].mean(axis=1)

    if attr.data_type == "FLOAT":
        return logical[:, 0].astype(np.float64)
    if attr.data_type == "FLOAT_COLOR":
        return logical[:, :3].astype(np.float64)
    return logical.astype(np.float64)


def normalize_vectors(vectors, fallback=(0.0, 0.0, 1.0)):
    vectors = np.asarray(vectors, dtype=np.float64)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    valid = norms[:, 0] > 1.0e-12
    result = np.zeros_like(vectors, dtype=np.float64)
    if np.any(valid):
        result[valid] = vectors[valid] / norms[valid]
    if np.any(~valid):
        result[~valid] = np.asarray(fallback, dtype=np.float64)
    return result


def compute_color_luminance(colors):
    colors = np.asarray(colors, dtype=np.float64)
    if colors.ndim != 2 or colors.shape[1] < 3:
        raise ProxySurfaceRelightError("compute_color_luminance expects an Nx3 or wider color array.")
    return (
        (0.2126 * colors[:, 0])
        + (0.7152 * colors[:, 1])
        + (0.0722 * colors[:, 2])
    ).reshape(-1, 1)


def compute_array_stats(values):
    values = np.asarray(values, dtype=np.float64)
    return {
        "min": np.min(values, axis=0).tolist(),
        "mean": np.mean(values, axis=0).tolist(),
        "max": np.max(values, axis=0).tolist(),
        "std": np.std(values, axis=0).tolist(),
        "p05": np.percentile(values, 5.0, axis=0).tolist(),
        "p50": np.percentile(values, 50.0, axis=0).tolist(),
        "p95": np.percentile(values, 95.0, axis=0).tolist(),
    }


def parse_debug_sample_indices(sample_indices, count, default=None):
    default = default or (0, 1, 2, 10, 100, -1)
    if count <= 0:
        return []
    if sample_indices is None:
        raw_indices = list(default)
    elif isinstance(sample_indices, str):
        raw_indices = []
        for item in sample_indices.split(","):
            item = item.strip()
            if not item:
                continue
            try:
                raw_indices.append(int(item))
            except ValueError:
                continue
        if not raw_indices:
            raw_indices = list(default)
    else:
        raw_indices = list(default)

    resolved = []
    for index in raw_indices:
        if index < 0:
            index = count + index
        if 0 <= index < count and index not in resolved:
            resolved.append(index)
    return resolved


def debug_print_array_stats(label, values, value_kind="generic", sample_indices=None):
    values = np.asarray(values, dtype=np.float64)
    if values.ndim == 1:
        values_2d = values.reshape(-1, 1)
    else:
        values_2d = values.reshape(values.shape[0], -1)

    stats = compute_array_stats(values_2d)
    channel_count = values_2d.shape[1]
    print(f"[PROXY RELIGHT DEBUG] {label}: count={len(values_2d)}, channels={channel_count}")
    for channel_index in range(channel_count):
        print(
            f"[PROXY RELIGHT DEBUG] {label}[{channel_index}] "
            f"min={stats['min'][channel_index]:.6f} "
            f"mean={stats['mean'][channel_index]:.6f} "
            f"max={stats['max'][channel_index]:.6f} "
            f"std={stats['std'][channel_index]:.6f} "
            f"p05={stats['p05'][channel_index]:.6f} "
            f"p50={stats['p50'][channel_index]:.6f} "
            f"p95={stats['p95'][channel_index]:.6f}"
        )

    if value_kind == "color":
        luminance = compute_color_luminance(values_2d[:, :3])
        luminance_stats = compute_array_stats(luminance)
        below_zero = float(np.mean(values_2d[:, :3] < 0.0) * 100.0)
        above_one = float(np.mean(values_2d[:, :3] > 1.0) * 100.0)
        print(
            f"[PROXY RELIGHT DEBUG] {label}.luminance "
            f"min={luminance_stats['min'][0]:.6f} "
            f"mean={luminance_stats['mean'][0]:.6f} "
            f"max={luminance_stats['max'][0]:.6f} "
            f"std={luminance_stats['std'][0]:.6f} "
            f"p05={luminance_stats['p05'][0]:.6f} "
            f"p50={luminance_stats['p50'][0]:.6f} "
            f"p95={luminance_stats['p95'][0]:.6f}"
        )
        print(
            f"[PROXY RELIGHT DEBUG] {label}.out_of_range "
            f"below_zero={below_zero:.3f}% above_one={above_one:.3f}%"
        )

    resolved_samples = parse_debug_sample_indices(sample_indices, len(values_2d))
    for sample_index in resolved_samples:
        sample_value = values_2d[sample_index]
        formatted = ", ".join(f"{component:.6f}" for component in sample_value.tolist())
        print(f"[PROXY RELIGHT DEBUG] {label}[sample {sample_index}] = ({formatted})")


def get_logical_positions_world(mesh_obj, state, proxy_utils):
    linear, translation = proxy_utils.matrix_to_row_affine(mesh_obj.matrix_world)
    return proxy_utils.transform_points_row(state["logical_positions_local"], linear, translation)


def collect_surface_geometry_world(mesh_obj, use_evaluated=True, proxy_binding_utils_path=""):
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)

    if use_evaluated:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        mesh_eval_obj = mesh_obj.evaluated_get(depsgraph)
        mesh_data = mesh_eval_obj.to_mesh()
        matrix_world = mesh_eval_obj.matrix_world.copy()
    else:
        mesh_eval_obj = None
        mesh_data = mesh_obj.data
        matrix_world = mesh_obj.matrix_world.copy()

    try:
        vertex_positions_local = proxy_utils.read_vertex_positions_local(mesh_data)
        vertex_normals_local = np.array(
            [vertex.normal[:] for vertex in mesh_data.vertices],
            dtype=np.float64,
        )
        linear = np.asarray(matrix_world.to_3x3(), dtype=np.float64)
        translation = np.asarray(matrix_world.translation[:], dtype=np.float64)
        normal_linear = np.linalg.inv(linear).T
        vertex_positions_world = proxy_utils.transform_points_row(
            vertex_positions_local,
            linear,
            translation,
        )
        vertex_normals_world = normalize_vectors(
            vertex_normals_local @ normal_linear.T,
            fallback=(0.0, 0.0, 1.0),
        )
        mesh_data.calc_loop_triangles()
        if not mesh_data.loop_triangles:
            raise ProxySurfaceRelightError(
                f"Mesh '{mesh_obj.name}' needs polygons for proxy relighting."
            )
        triangle_vertex_indices = np.array(
            [triangle.vertices[:] for triangle in mesh_data.loop_triangles],
            dtype=np.int32,
        )
        return vertex_positions_world, triangle_vertex_indices, vertex_normals_world
    finally:
        if mesh_eval_obj is not None:
            mesh_eval_obj.to_mesh_clear()


def compute_triangle_normals_world(proxy_vertices_world, surface_triangle_indices):
    triangle_vertices = np.asarray(proxy_vertices_world, dtype=np.float64)[
        np.asarray(surface_triangle_indices, dtype=np.int32)
    ]
    normals = np.cross(
        triangle_vertices[:, 1, :] - triangle_vertices[:, 0, :],
        triangle_vertices[:, 2, :] - triangle_vertices[:, 0, :],
    )
    return normalize_vectors(normals)


def compute_barycentric_coordinates(points_world, triangle_vertices_world):
    points_world = np.asarray(points_world, dtype=np.float64)
    triangle_vertices_world = np.asarray(triangle_vertices_world, dtype=np.float64)
    a = triangle_vertices_world[:, 0, :]
    b = triangle_vertices_world[:, 1, :]
    c = triangle_vertices_world[:, 2, :]

    v0 = b - a
    v1 = c - a
    v2 = points_world - a

    d00 = np.sum(v0 * v0, axis=1)
    d01 = np.sum(v0 * v1, axis=1)
    d11 = np.sum(v1 * v1, axis=1)
    d20 = np.sum(v2 * v0, axis=1)
    d21 = np.sum(v2 * v1, axis=1)

    denom = np.maximum((d00 * d11) - (d01 * d01), EPSILON)
    v = ((d11 * d20) - (d01 * d21)) / denom
    w = ((d00 * d21) - (d01 * d20)) / denom
    u = 1.0 - v - w
    barycentric = np.column_stack([u, v, w])
    return np.clip(barycentric, 0.0, 1.0)


def build_proxy_surface_binding(
    mesh_obj,
    proxy_obj,
    use_evaluated_proxy=True,
    proxy_binding_utils_path="",
):
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    state = proxy_utils.read_logical_gaussian_state(mesh_obj)
    logical_positions_world = get_logical_positions_world(mesh_obj, state, proxy_utils)
    proxy_vertices_world, triangle_vertex_indices, proxy_vertex_normals_world = collect_surface_geometry_world(
        proxy_obj,
        use_evaluated=use_evaluated_proxy,
        proxy_binding_utils_path=proxy_binding_utils_path,
    )
    proxy_bvh = build_proxy_bvh(proxy_vertices_world, triangle_vertex_indices)

    triangle_ids = np.zeros(len(logical_positions_world), dtype=np.int32)
    nearest_points_world = np.zeros_like(logical_positions_world, dtype=np.float64)
    for point_index, point in enumerate(logical_positions_world):
        nearest = proxy_bvh.find_nearest(Vector(point.tolist()))
        if nearest is None or nearest[2] is None:
            raise ProxySurfaceRelightError(
                f"Failed to find a nearest proxy surface triangle for '{mesh_obj.name}'."
            )
        nearest_points_world[point_index] = np.asarray(nearest[0][:], dtype=np.float64)
        triangle_ids[point_index] = int(nearest[2])

    bound_triangle_indices = np.asarray(triangle_vertex_indices, dtype=np.int32)[triangle_ids]
    bound_triangle_vertices_world = np.asarray(proxy_vertices_world, dtype=np.float64)[bound_triangle_indices]
    bound_triangle_vertex_normals_world = np.asarray(proxy_vertex_normals_world, dtype=np.float64)[bound_triangle_indices]
    barycentric = compute_barycentric_coordinates(nearest_points_world, bound_triangle_vertices_world)
    bound_triangle_normals_world = normalize_vectors(
        np.sum(bound_triangle_vertex_normals_world * barycentric[:, :, None], axis=1),
        fallback=(0.0, 0.0, 1.0),
    )

    return {
        "logical_positions_world": logical_positions_world,
        "bound_triangle_normals_world": bound_triangle_normals_world,
        "bound_triangle_centroids_world": nearest_points_world,
        "bound_triangle_barycentric": barycentric.astype(np.float64),
        "surface_distances": np.linalg.norm(logical_positions_world - nearest_points_world, axis=1).astype(np.float64),
        "proxy_name": proxy_obj.name,
        "proxy_vertices_world": np.asarray(proxy_vertices_world, dtype=np.float64),
        "proxy_vertex_normals_world": np.asarray(proxy_vertex_normals_world, dtype=np.float64),
        "triangle_vertex_indices": np.asarray(triangle_vertex_indices, dtype=np.int32),
        "bound_triangle_vertex_indices": bound_triangle_indices.astype(np.int32),
        "bound_triangle_ids": triangle_ids.astype(np.int32),
        "nearest_points_world": nearest_points_world.astype(np.float64),
    }


def build_bidirectional_vertex_edges(triangle_vertex_indices):
    triangle_vertex_indices = np.asarray(triangle_vertex_indices, dtype=np.int32)
    if triangle_vertex_indices.size == 0:
        return np.zeros((0, 2), dtype=np.int32)

    undirected_edges = np.concatenate(
        [
            triangle_vertex_indices[:, [0, 1]],
            triangle_vertex_indices[:, [1, 2]],
            triangle_vertex_indices[:, [2, 0]],
        ],
        axis=0,
    )
    valid = undirected_edges[:, 0] != undirected_edges[:, 1]
    undirected_edges = undirected_edges[valid]
    if len(undirected_edges) == 0:
        return np.zeros((0, 2), dtype=np.int32)

    reversed_edges = undirected_edges[:, ::-1]
    return np.concatenate([undirected_edges, reversed_edges], axis=0).astype(np.int32)


def build_bidirectional_triangle_edges(triangle_vertex_indices):
    triangle_vertex_indices = np.asarray(triangle_vertex_indices, dtype=np.int32)
    if triangle_vertex_indices.size == 0:
        return np.zeros((0, 2), dtype=np.int32)

    edge_to_triangles = {}
    for triangle_index, triangle in enumerate(triangle_vertex_indices):
        for a, b in ((0, 1), (1, 2), (2, 0)):
            edge_key = tuple(sorted((int(triangle[a]), int(triangle[b]))))
            edge_to_triangles.setdefault(edge_key, []).append(triangle_index)

    triangle_pairs = []
    for triangle_indices in edge_to_triangles.values():
        if len(triangle_indices) < 2:
            continue
        for source_index in range(len(triangle_indices)):
            for target_index in range(source_index + 1, len(triangle_indices)):
                triangle_a = int(triangle_indices[source_index])
                triangle_b = int(triangle_indices[target_index])
                if triangle_a == triangle_b:
                    continue
                triangle_pairs.append((triangle_a, triangle_b))
                triangle_pairs.append((triangle_b, triangle_a))

    if not triangle_pairs:
        return np.zeros((0, 2), dtype=np.int32)
    return np.asarray(triangle_pairs, dtype=np.int32)


def smooth_values_over_edges(values, edges, strength=0.0, pass_count=3, normalize_result=False):
    current = np.asarray(values, dtype=np.float64)
    if current.ndim == 1:
        current = current.reshape(-1, 1)
        squeeze_result = True
    else:
        squeeze_result = False

    edges = np.asarray(edges, dtype=np.int32)
    strength = float(np.clip(strength, 0.0, 1.0))
    if strength <= EPSILON or current.size == 0 or len(edges) == 0:
        result = current
    else:
        pass_count = max(int(pass_count), 1)
        per_pass_blend = strength / float(pass_count)
        result = current.copy()
        source_indices = edges[:, 0]
        target_indices = edges[:, 1]

        for _ in range(pass_count):
            accumulated = result.copy()
            counts = np.ones((len(result), 1), dtype=np.float64)
            np.add.at(accumulated, target_indices, result[source_indices])
            np.add.at(counts[:, 0], target_indices, 1.0)
            averaged = accumulated / np.maximum(counts, EPSILON)
            result = ((1.0 - per_pass_blend) * result) + (per_pass_blend * averaged)
            if normalize_result:
                result = normalize_vectors(result, fallback=(0.0, 0.0, 1.0))

    if squeeze_result:
        return result[:, 0]
    return result


def resolve_transfer_style_parameters(transfer_style="Accurate", transfer_smoothness=0.5):
    style_key = str(transfer_style).strip().lower().replace("_", " ")
    smoothness = float(np.clip(transfer_smoothness, 0.0, 1.0))
    if style_key in ("", "accurate", "exact"):
        return "Accurate", 0.0
    if style_key in ("balanced", "medium"):
        return "Balanced", min(1.0, 0.15 + (0.50 * smoothness))
    if style_key in ("smooth", "soft"):
        return "Smooth", min(1.0, 0.55 + (0.35 * smoothness))
    raise ProxySurfaceRelightError(
        f"Unsupported transfer_style '{transfer_style}'. Use Accurate, Balanced, or Smooth."
    )


def interpolate_triangle_vertex_values_with_style(
    vertex_values,
    triangle_vertex_indices,
    barycentric,
    transfer_style="Accurate",
    transfer_smoothness=0.5,
):
    barycentric_values = interpolate_triangle_vertex_values(
        vertex_values,
        triangle_vertex_indices,
        barycentric,
    )
    resolved_style, blend = resolve_transfer_style_parameters(
        transfer_style=transfer_style,
        transfer_smoothness=transfer_smoothness,
    )
    if blend <= EPSILON:
        return barycentric_values, resolved_style, 0.0

    triangle_values = np.asarray(vertex_values, dtype=np.float64)[
        np.asarray(triangle_vertex_indices, dtype=np.int32)
    ]
    triangle_mean_values = np.mean(triangle_values, axis=1)
    blended_values = ((1.0 - blend) * barycentric_values) + (blend * triangle_mean_values)
    return blended_values, resolved_style, blend


def build_triangle_value_fallback(vertex_values, triangle_vertex_indices):
    triangle_values = np.asarray(vertex_values, dtype=np.float64)[
        np.asarray(triangle_vertex_indices, dtype=np.int32)
    ]
    return np.mean(triangle_values, axis=1)


def smooth_transferred_values_by_triangle(
    sample_values,
    bound_triangle_ids,
    triangle_vertex_indices,
    triangle_edges,
    strength=0.0,
    triangle_fallback_values=None,
):
    sample_values_array = np.asarray(sample_values, dtype=np.float64)
    if sample_values_array.ndim == 1:
        sample_values_2d = sample_values_array.reshape(-1, 1)
        squeeze_result = True
    else:
        sample_values_2d = sample_values_array
        squeeze_result = False

    strength = float(np.clip(strength, 0.0, 1.0))
    if strength <= EPSILON or len(sample_values_2d) == 0:
        result = sample_values_2d
    else:
        triangle_count = int(len(np.asarray(triangle_vertex_indices, dtype=np.int32)))
        triangle_ids = np.asarray(bound_triangle_ids, dtype=np.int32)

        if triangle_fallback_values is None:
            fallback_values = np.zeros((triangle_count, sample_values_2d.shape[1]), dtype=np.float64)
        else:
            fallback_values = np.asarray(triangle_fallback_values, dtype=np.float64)
            if fallback_values.ndim == 1:
                fallback_values = fallback_values.reshape(-1, 1)

        triangle_values = fallback_values.copy()
        counts = np.zeros(triangle_count, dtype=np.float64)
        np.add.at(triangle_values, triangle_ids, sample_values_2d)
        np.add.at(counts, triangle_ids, 1.0)
        valid = counts > 0.0
        if np.any(valid):
            triangle_values[valid] /= counts[valid, None]

        smoothed_triangle_values = smooth_values_over_edges(
            triangle_values,
            triangle_edges,
            strength=strength,
            pass_count=3,
            normalize_result=False,
        )
        result = ((1.0 - strength) * sample_values_2d) + (
            strength * smoothed_triangle_values[triangle_ids]
        )

    if squeeze_result:
        return result[:, 0]
    return result


def interpolate_triangle_vertex_values(vertex_values, triangle_vertex_indices, barycentric):
    vertex_values = np.asarray(vertex_values, dtype=np.float64)
    triangle_vertex_indices = np.asarray(triangle_vertex_indices, dtype=np.int32)
    barycentric = np.asarray(barycentric, dtype=np.float64)

    triangle_values = vertex_values[triangle_vertex_indices]
    if triangle_values.ndim == 2:
        return np.sum(triangle_values * barycentric, axis=1)
    return np.sum(triangle_values * barycentric[:, :, None], axis=1)


def clamp_rgb(colors, low=0.0, high=1.0):
    return np.clip(np.asarray(colors, dtype=np.float64), float(low), float(high))


def resolve_max_color_tint_mode(mode):
    key = "".join(ch for ch in str(mode).strip().lower().replace("_", " ") if ch.isalnum())
    if key in ("", "perceivedbrightness", "brightness", "legacy", "clip", "clamp"):
        return "Perceived Brightness"
    if key in ("preserveluminance", "luminancepreserving", "keepluminance", "coloronly"):
        return "Preserve Luminance"
    raise ProxySurfaceRelightError(
        f"Unsupported max_color_tint_mode '{mode}'. Use Perceived Brightness or Preserve Luminance."
    )


def build_unit_luminance_tint(
    colors,
    tint_strength=1.0,
    max_tint=2.0,
    max_tint_mode="Perceived Brightness",
):
    colors = np.asarray(colors, dtype=np.float64)
    luminance = compute_color_luminance(colors).reshape(-1, 1)
    tint = np.ones_like(colors, dtype=np.float64)
    valid = luminance[:, 0] > EPSILON
    if np.any(valid):
        tint[valid] = colors[valid] / luminance[valid]
    resolved_mode = resolve_max_color_tint_mode(max_tint_mode)
    if resolved_mode == "Perceived Brightness":
        max_tint_value = max(float(max_tint), 0.0)
        tint = np.clip(tint, 0.0, max_tint_value)
    else:
        max_tint_value = max(float(max_tint), 1.0)
        # Keep unit luminance by reducing extreme color casts toward neutral white
        # instead of clipping individual RGB channels and changing brightness.
        over_limit = tint > max_tint_value
        if np.any(over_limit):
            denom = np.maximum(tint - 1.0, EPSILON)
            allowed_mix = (max_tint_value - 1.0) / denom
            allowed_mix = np.where(over_limit, allowed_mix, 1.0)
            per_point_mix = np.clip(np.min(allowed_mix, axis=1), 0.0, 1.0)
            tint = 1.0 + (per_point_mix[:, None] * (tint - 1.0))
        tint = np.maximum(tint, 0.0)
    mix = float(np.clip(tint_strength, 0.0, 1.0))
    return ((1.0 - mix) * np.ones_like(tint)) + (mix * tint)


def rgb_to_hsv_array(colors):
    colors = np.asarray(colors, dtype=np.float64)
    if colors.ndim < 2 or colors.shape[-1] < 3:
        raise ProxySurfaceRelightError("rgb_to_hsv_array expects an array ending in three color channels.")

    rgb = colors[..., :3]
    r = rgb[..., 0]
    g = rgb[..., 1]
    b = rgb[..., 2]

    maxc = np.max(rgb, axis=-1)
    minc = np.min(rgb, axis=-1)
    delta = maxc - minc

    hue = np.zeros_like(maxc, dtype=np.float64)
    saturation = np.zeros_like(maxc, dtype=np.float64)
    value = maxc.copy()

    nonzero_value = maxc > EPSILON
    saturation[nonzero_value] = delta[nonzero_value] / maxc[nonzero_value]

    valid = delta > EPSILON
    r_is_max = valid & (r >= g) & (r >= b)
    g_is_max = valid & (g > r) & (g >= b)
    b_is_max = valid & (b > r) & (b > g)

    hue[r_is_max] = ((g[r_is_max] - b[r_is_max]) / delta[r_is_max]) % 6.0
    hue[g_is_max] = ((b[g_is_max] - r[g_is_max]) / delta[g_is_max]) + 2.0
    hue[b_is_max] = ((r[b_is_max] - g[b_is_max]) / delta[b_is_max]) + 4.0
    hue = (hue / 6.0) % 1.0

    return np.stack([hue, saturation, value], axis=-1)


def hsv_to_rgb_array(colors):
    colors = np.asarray(colors, dtype=np.float64)
    if colors.ndim < 2 or colors.shape[-1] < 3:
        raise ProxySurfaceRelightError("hsv_to_rgb_array expects an array ending in three color channels.")

    hsv = colors[..., :3]
    hue = hsv[..., 0] % 1.0
    saturation = np.clip(hsv[..., 1], 0.0, None)
    value = np.clip(hsv[..., 2], 0.0, None)

    scaled_h = hue * 6.0
    sector = np.floor(scaled_h).astype(np.int32) % 6
    fraction = scaled_h - np.floor(scaled_h)

    p = value * (1.0 - saturation)
    q = value * (1.0 - fraction * saturation)
    t = value * (1.0 - (1.0 - fraction) * saturation)

    red = np.empty_like(value)
    green = np.empty_like(value)
    blue = np.empty_like(value)

    for sector_index in range(6):
        mask = sector == sector_index
        if not np.any(mask):
            continue
        if sector_index == 0:
            red[mask], green[mask], blue[mask] = value[mask], t[mask], p[mask]
        elif sector_index == 1:
            red[mask], green[mask], blue[mask] = q[mask], value[mask], p[mask]
        elif sector_index == 2:
            red[mask], green[mask], blue[mask] = p[mask], value[mask], t[mask]
        elif sector_index == 3:
            red[mask], green[mask], blue[mask] = p[mask], q[mask], value[mask]
        elif sector_index == 4:
            red[mask], green[mask], blue[mask] = t[mask], p[mask], value[mask]
        else:
            red[mask], green[mask], blue[mask] = value[mask], p[mask], q[mask]

    return np.stack([red, green, blue], axis=-1)


def apply_gamma_node(colors, node):
    gamma_value = max(float(node.inputs["Gamma"].default_value), EPSILON)
    return np.power(np.clip(colors, 0.0, None), gamma_value)


def apply_hue_sat_node(colors, node):
    factor = float(node.inputs["Fac"].default_value)
    hue_shift = float(node.inputs["Hue"].default_value) - 0.5
    saturation_scale = float(node.inputs["Saturation"].default_value)
    value_scale = float(node.inputs["Value"].default_value)

    hsv = rgb_to_hsv_array(np.clip(colors, 0.0, None))
    hsv[..., 0] = (hsv[..., 0] + hue_shift) % 1.0
    hsv[..., 1] = np.clip(hsv[..., 1] * saturation_scale, 0.0, None)
    hsv[..., 2] = np.clip(hsv[..., 2] * value_scale, 0.0, None)
    adjusted = hsv_to_rgb_array(hsv)
    return ((1.0 - factor) * colors) + (factor * adjusted)


def apply_invert_node(colors, node):
    factor = float(node.inputs["Fac"].default_value)
    return ((1.0 - factor) * colors) + (factor * (1.0 - colors))


def apply_bright_contrast_node(colors, node):
    bright = float(node.inputs["Bright"].default_value)
    contrast = float(node.inputs["Contrast"].default_value)
    slope = 1.0 + contrast
    intercept = bright + (0.5 * (1.0 - slope))
    return colors * slope + intercept


def apply_color_node_to_pixels(colors, node):
    node_type = str(getattr(node, "type", "")).upper()
    if node_type == "GAMMA":
        return apply_gamma_node(colors, node), True
    if node_type in ("HUE_SAT", "HUE_SAT_VAL"):
        return apply_hue_sat_node(colors, node), True
    if node_type == "INVERT":
        return apply_invert_node(colors, node), True
    if node_type == "BRIGHTCONTRAST":
        return apply_bright_contrast_node(colors, node), True
    return colors, False


def find_environment_path_from_input(input_socket, visited=None):
    visited = visited or set()
    node = trace_linked_node(input_socket)
    if node is None:
        return None

    node_key = id(node)
    if node_key in visited:
        return None
    visited = set(visited)
    visited.add(node_key)

    if node.type == "TEX_ENVIRONMENT" and getattr(node, "image", None) is not None:
        return {"environment_node": node, "color_nodes": []}

    for socket in getattr(node, "inputs", []):
        if socket.is_linked:
            found = find_environment_path_from_input(socket, visited=visited)
            if found is not None:
                found["color_nodes"].append(node)
                return found
    return None


def collect_vector_transform_nodes(node_input, visited=None):
    visited = visited or set()
    node = trace_linked_node(node_input)
    if node is None:
        return {"nodes": [], "unsupported": []}

    node_key = id(node)
    if node_key in visited:
        return {"nodes": [], "unsupported": []}
    visited = set(visited)
    visited.add(node_key)

    if node.type == "MAPPING":
        upstream = collect_vector_transform_nodes(get_node_input(node, "Vector"), visited=visited)
        upstream["nodes"].append(node)
        return upstream

    if node.type in ("TEX_COORD", "NEW_GEOMETRY", "ATTRIBUTE", "UV_MAP"):
        return {"nodes": [], "unsupported": []}

    unsupported = [node.type]
    for socket in getattr(node, "inputs", []):
        if socket.is_linked:
            upstream = collect_vector_transform_nodes(socket, visited=visited)
            return {
                "nodes": upstream["nodes"],
                "unsupported": unsupported + upstream["unsupported"],
            }
    return {"nodes": [], "unsupported": unsupported}


def apply_euler_rotation_xyz(vectors, rotation_radians):
    vectors = np.asarray(vectors, dtype=np.float64)
    rx, ry, rz = np.asarray(rotation_radians, dtype=np.float64).tolist()

    if abs(rx) > 1.0e-12:
        cos_x = math.cos(rx)
        sin_x = math.sin(rx)
        y = vectors[:, 1] * cos_x - vectors[:, 2] * sin_x
        z = vectors[:, 1] * sin_x + vectors[:, 2] * cos_x
        vectors = np.column_stack([vectors[:, 0], y, z])

    if abs(ry) > 1.0e-12:
        cos_y = math.cos(ry)
        sin_y = math.sin(ry)
        x = vectors[:, 0] * cos_y + vectors[:, 2] * sin_y
        z = -vectors[:, 0] * sin_y + vectors[:, 2] * cos_y
        vectors = np.column_stack([x, vectors[:, 1], z])

    if abs(rz) > 1.0e-12:
        cos_z = math.cos(rz)
        sin_z = math.sin(rz)
        x = vectors[:, 0] * cos_z - vectors[:, 1] * sin_z
        y = vectors[:, 0] * sin_z + vectors[:, 1] * cos_z
        vectors = np.column_stack([x, y, vectors[:, 2]])

    return vectors


def apply_mapping_node_to_directions(directions, mapping_node):
    directions = np.asarray(directions, dtype=np.float64)
    location = np.asarray(mapping_node.inputs["Location"].default_value[:3], dtype=np.float64)
    rotation = np.asarray(mapping_node.inputs["Rotation"].default_value[:3], dtype=np.float64)
    scale = np.asarray(mapping_node.inputs["Scale"].default_value[:3], dtype=np.float64)
    safe_scale = np.where(np.abs(scale) <= EPSILON, 1.0, scale)

    vector_type = str(getattr(mapping_node, "vector_type", "POINT")).upper()
    transformed = directions.copy()

    if vector_type == "TEXTURE":
        transformed = transformed - location[None, :]
        transformed = apply_euler_rotation_xyz(transformed, -rotation)
        transformed = transformed / safe_scale[None, :]
    elif vector_type == "VECTOR":
        transformed = transformed * safe_scale[None, :]
        transformed = apply_euler_rotation_xyz(transformed, rotation)
    elif vector_type == "NORMAL":
        transformed = transformed / safe_scale[None, :]
        transformed = apply_euler_rotation_xyz(transformed, rotation)
        transformed = normalize_vectors(transformed)
    else:
        transformed = transformed * safe_scale[None, :]
        transformed = apply_euler_rotation_xyz(transformed, rotation)
        transformed = transformed + location[None, :]

    return transformed


def apply_vector_nodes_to_directions(directions, vector_nodes):
    transformed = np.asarray(directions, dtype=np.float64)
    for node in vector_nodes:
        if getattr(node, "type", "") == "MAPPING":
            transformed = apply_mapping_node_to_directions(transformed, node)
    return normalize_vectors(transformed)


def build_proxy_bvh(proxy_vertices_world, triangle_vertex_indices):
    vertices = [tuple(vertex.tolist()) for vertex in np.asarray(proxy_vertices_world, dtype=np.float64)]
    triangles = [tuple(triangle.tolist()) for triangle in np.asarray(triangle_vertex_indices, dtype=np.int32)]
    return BVHTree.FromPolygons(vertices, triangles, all_triangles=True)


def ray_is_unoccluded(
    proxy_bvh,
    origin,
    direction,
    max_distance=0.0,
    source_triangle_id=-1,
    self_hit_epsilon=1.0e-4,
):
    direction = np.asarray(direction, dtype=np.float64)
    distance = float(max_distance)
    if distance <= 0.0:
        distance = 1.0e20

    hit_location, _, hit_triangle_index, hit_distance = proxy_bvh.ray_cast(
        Vector(origin.tolist()),
        Vector(direction.tolist()),
        distance,
    )
    if hit_location is None:
        return True
    if hit_triangle_index == int(source_triangle_id) and float(hit_distance or 0.0) <= float(self_hit_epsilon):
        return True
    return False


def build_orthonormal_basis(normals):
    normals = normalize_vectors(normals)
    up = np.tile(np.array([[0.0, 0.0, 1.0]], dtype=np.float64), (len(normals), 1))
    replace_mask = np.abs(normals[:, 2]) > 0.95
    if np.any(replace_mask):
        up[replace_mask] = np.array([1.0, 0.0, 0.0], dtype=np.float64)

    tangents = normalize_vectors(np.cross(up, normals), fallback=(1.0, 0.0, 0.0))
    bitangents = normalize_vectors(np.cross(normals, tangents), fallback=(0.0, 1.0, 0.0))
    return tangents, bitangents


def generate_cosine_hemisphere_samples(sample_count):
    sample_count = max(int(sample_count), 1)
    index = np.arange(sample_count, dtype=np.float64)
    u = (index + 0.5) / float(sample_count)
    v = (index * 0.6180339887498949) % 1.0
    radius = np.sqrt(u)
    theta = 2.0 * math.pi * v
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.sqrt(np.clip(1.0 - u, 0.0, 1.0))
    return np.column_stack([x, y, z]).astype(np.float64)


def compute_surface_occlusion_factors(
    sample_positions_world,
    sample_normals_world,
    proxy_bvh,
    sample_count=6,
    bias=0.002,
    max_distance=0.0,
    source_triangle_ids=None,
):
    sample_count = max(int(sample_count), 1)
    normals = np.asarray(sample_normals_world, dtype=np.float64)
    centroids = np.asarray(sample_positions_world, dtype=np.float64)
    if source_triangle_ids is None:
        triangle_ids = np.full(len(centroids), -1, dtype=np.int32)
    else:
        triangle_ids = np.asarray(source_triangle_ids, dtype=np.int32)
    origins = centroids + normals * float(bias)

    tangents, bitangents = build_orthonormal_basis(normals)
    local_samples = generate_cosine_hemisphere_samples(sample_count)
    visibility = np.ones((len(centroids), sample_count), dtype=np.float64)

    for sample_index, local_direction in enumerate(local_samples):
        ray_directions = (
            tangents * local_direction[0]
            + bitangents * local_direction[1]
            + normals * local_direction[2]
        )
        ray_directions = normalize_vectors(ray_directions)
        for point_index in range(len(centroids)):
            visible = ray_is_unoccluded(
                proxy_bvh,
                origins[point_index],
                ray_directions[point_index],
                max_distance=max_distance,
                source_triangle_id=triangle_ids[point_index],
                self_hit_epsilon=max(float(bias) * 4.0, 1.0e-4),
            )
            visibility[point_index, sample_index] = 1.0 if visible else 0.0

    return np.mean(visibility, axis=1).astype(np.float64)


def compute_proxy_occlusion_factors(
    surface_info,
    proxy_bvh,
    sample_count=6,
    bias=0.002,
    max_distance=0.0,
):
    return compute_surface_occlusion_factors(
        surface_info["bound_triangle_centroids_world"],
        surface_info["bound_triangle_normals_world"],
        proxy_bvh,
        sample_count=sample_count,
        bias=bias,
        max_distance=max_distance,
        source_triangle_ids=surface_info["bound_triangle_ids"],
    )


def collect_scene_lights(include_hidden_lights=False):
    lights = []
    for obj in bpy.context.scene.objects:
        if obj.type != "LIGHT":
            continue
        if not include_hidden_lights and (obj.hide_get() or obj.hide_render):
            continue

        light_data = obj.data
        if light_data is None:
            continue

        position = np.asarray(obj.matrix_world.translation[:], dtype=np.float64)
        forward = np.asarray((obj.matrix_world.to_3x3() @ Vector((0.0, 0.0, -1.0)))[:], dtype=np.float64)
        forward = normalize_vectors(forward.reshape(1, 3))[0]

        area_size_y = float(getattr(light_data, "size_y", getattr(light_data, "size", 1.0)))
        lights.append(
            {
                "name": obj.name,
                "type": str(light_data.type).upper(),
                "energy": float(light_data.energy),
                "color": np.asarray(light_data.color[:3], dtype=np.float64),
                "position": position,
                "forward": forward,
                "spot_size": float(getattr(light_data, "spot_size", math.pi)),
                "spot_blend": float(getattr(light_data, "spot_blend", 0.0)),
                "area_size_x": float(getattr(light_data, "size", 1.0)),
                "area_size_y": area_size_y,
            }
        )
    return lights


def evaluate_scene_lights_on_samples(
    sample_positions_world,
    sample_normals_world,
    proxy_bvh,
    scene_light_gain=1.0,
    use_light_shadows=True,
    direct_shadow_strength=1.0,
    shadow_bias=0.002,
    include_hidden_lights=False,
    source_triangle_ids=None,
):
    lights = collect_scene_lights(include_hidden_lights=include_hidden_lights)
    normals = np.asarray(sample_normals_world, dtype=np.float64)
    centroids = np.asarray(sample_positions_world, dtype=np.float64)
    if source_triangle_ids is None:
        triangle_ids = np.full(len(centroids), -1, dtype=np.int32)
    else:
        triangle_ids = np.asarray(source_triangle_ids, dtype=np.int32)
    origins = centroids + normals * float(shadow_bias)

    total_rgb = np.zeros((len(centroids), 3), dtype=np.float64)
    per_light_stats = []

    for light in lights:
        light_type = light["type"]
        light_color = light["color"] * float(light["energy"])

        if light_type == "SUN":
            to_light = np.tile((-light["forward"]).reshape(1, 3), (len(centroids), 1))
            distance = np.full(len(centroids), 1.0e20, dtype=np.float64)
            attenuation = np.ones(len(centroids), dtype=np.float64)
            cone_factor = np.ones(len(centroids), dtype=np.float64)
        else:
            light_vectors = light["position"][None, :] - centroids
            distance = np.linalg.norm(light_vectors, axis=1)
            safe_distance = np.maximum(distance, 1.0e-4)
            to_light = light_vectors / safe_distance[:, None]
            attenuation = 1.0 / np.maximum(safe_distance * safe_distance, 1.0e-4)
            cone_factor = np.ones(len(centroids), dtype=np.float64)

            if light_type == "SPOT":
                spot_cos = np.sum((-to_light) * light["forward"][None, :], axis=1)
                outer_angle = max(float(light["spot_size"]) * 0.5, 1.0e-4)
                inner_angle = max(outer_angle * (1.0 - float(light["spot_blend"])), 1.0e-4)
                outer_cos = math.cos(outer_angle)
                inner_cos = math.cos(inner_angle)
                denom = max(inner_cos - outer_cos, EPSILON)
                cone_factor = np.clip((spot_cos - outer_cos) / denom, 0.0, 1.0)
            elif light_type == "AREA":
                area_facing = np.clip(np.sum((-to_light) * light["forward"][None, :], axis=1), 0.0, None)
                cone_factor = area_facing

        ndotl = np.clip(np.sum(normals * to_light, axis=1), 0.0, None)
        active_mask = (ndotl > 0.0) & (cone_factor > 0.0)
        visibility = np.zeros(len(centroids), dtype=np.float64)

        if np.any(active_mask):
            if use_light_shadows:
                active_indices = np.nonzero(active_mask)[0]
                for point_index in active_indices:
                    ray_distance = 0.0 if light_type == "SUN" else max(float(distance[point_index] - shadow_bias), 0.0)
                    visible = ray_is_unoccluded(
                        proxy_bvh,
                        origins[point_index],
                        to_light[point_index],
                        max_distance=ray_distance,
                        source_triangle_id=triangle_ids[point_index],
                        self_hit_epsilon=max(float(shadow_bias) * 4.0, 1.0e-4),
                    )
                    visibility[point_index] = 1.0 if visible else 0.0
            else:
                visibility[active_mask] = 1.0

        shadow_mix = float(np.clip(direct_shadow_strength, 0.0, 1.0))
        visibility = ((1.0 - shadow_mix) + (shadow_mix * visibility)) * active_mask.astype(np.float64)

        light_rgb = (
            light_color[None, :]
            * ndotl[:, None]
            * attenuation[:, None]
            * cone_factor[:, None]
            * visibility[:, None]
        )
        total_rgb += light_rgb

        per_light_stats.append(
            {
                "name": light["name"],
                "type": light_type,
                "mean_luminance": float(np.mean(compute_color_luminance(light_rgb)[:, 0])) if len(light_rgb) else 0.0,
                "lit_fraction": float(np.mean(active_mask.astype(np.float64))) if len(active_mask) else 0.0,
                "visible_fraction": float(np.mean(visibility)) if len(visibility) else 0.0,
            }
        )

    total_rgb *= float(scene_light_gain)
    return {
        "lights": lights,
        "light_rgb": total_rgb.astype(np.float64),
        "light_count": len(lights),
        "per_light_stats": per_light_stats,
    }


def evaluate_scene_lights_on_proxy(
    surface_info,
    proxy_bvh,
    scene_light_gain=1.0,
    use_light_shadows=True,
    direct_shadow_strength=1.0,
    shadow_bias=0.002,
    include_hidden_lights=False,
):
    return evaluate_scene_lights_on_samples(
        surface_info["bound_triangle_centroids_world"],
        surface_info["bound_triangle_normals_world"],
        proxy_bvh,
        scene_light_gain=scene_light_gain,
        use_light_shadows=use_light_shadows,
        direct_shadow_strength=direct_shadow_strength,
        shadow_bias=shadow_bias,
        include_hidden_lights=include_hidden_lights,
        source_triangle_ids=surface_info["bound_triangle_ids"],
    )


def evaluate_base_color_from_f_dc(
    mesh_obj,
    clamp_base_color=True,
    source_mode="Current f_dc",
    relight_cache_root="",
    proxy_binding_utils_path="",
):
    source_mode_normalized = str(source_mode).strip().lower().replace("_", " ")
    if source_mode_normalized in ("", "current", "current f dc", "current f_dc", "f dc", "f_dc"):
        proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
        state = proxy_utils.read_logical_gaussian_state(mesh_obj)
        raw_color = state["sh_coeffs"][:, :, 0] * SH_C0 + 0.5
        f_dc_coeffs = np.asarray(state["sh_coeffs"][:, :, 0], dtype=np.float64)
        resolved_mode = "Current f_dc Clamped" if clamp_base_color else "Current f_dc Raw"
    elif source_mode_normalized in ("saved original", "saved", "original", "saved original f dc", "saved original f_dc"):
        _, _, saved_state = load_saved_color_state(
            mesh_obj,
            relight_cache_root=relight_cache_root,
        )
        raw_color = saved_state["sh_coeffs"][:, :, 0] * SH_C0 + 0.5
        f_dc_coeffs = np.asarray(saved_state["sh_coeffs"][:, :, 0], dtype=np.float64)
        resolved_mode = "Saved Original f_dc Clamped" if clamp_base_color else "Saved Original f_dc Raw"
    else:
        raise ProxySurfaceRelightError(
            f"Unsupported source_mode '{source_mode}'. Use Current f_dc or Saved Original."
        )

    logical_color = clamp_rgb(raw_color) if bool(clamp_base_color) else raw_color
    return {
        "logical_color": np.asarray(logical_color, dtype=np.float64),
        "source_color": np.asarray(raw_color, dtype=np.float64),
        "f_dc_coeffs": f_dc_coeffs,
        "logical_splat_count": int(len(logical_color)),
        "mode": resolved_mode,
    }


def build_base_color_from_f_dc(
    mesh_obj,
    base_color_attr_name=DEFAULT_BASE_COLOR_ATTR,
    clamp_base_color=True,
    source_mode="Current f_dc",
    relight_cache_root="",
    proxy_binding_utils_path="",
):
    result = evaluate_base_color_from_f_dc(
        mesh_obj,
        clamp_base_color=clamp_base_color,
        source_mode=source_mode,
        relight_cache_root=relight_cache_root,
        proxy_binding_utils_path=proxy_binding_utils_path,
    )
    logical_color = result["logical_color"]
    write_logical_point_attribute(
        mesh_obj,
        base_color_attr_name,
        logical_color,
        data_type="FLOAT_COLOR",
        proxy_binding_utils_path=proxy_binding_utils_path,
    )
    clear_legacy_relight_properties(mesh_obj)
    return result


def trace_linked_node(input_socket, visited=None):
    visited = visited or set()
    if input_socket is None or not input_socket.is_linked:
        return None
    link = input_socket.links[0]
    node = link.from_node
    if node is None:
        return None
    node_key = id(node)
    if node_key in visited:
        return None
    visited.add(node_key)

    if node.type == "REROUTE":
        if node.inputs:
            return trace_linked_node(node.inputs[0], visited=visited)
        return None
    return node


def get_node_input(node, socket_name):
    try:
        return node.inputs[socket_name]
    except Exception:
        return None


def socket_collection_index(socket_collection, target_socket):
    for index, socket in enumerate(socket_collection):
        if socket == target_socket:
            return index
    return -1


def find_active_group_output_node(node_tree):
    if node_tree is None:
        return None
    output_nodes = [node for node in node_tree.nodes if node.type == "GROUP_OUTPUT"]
    for node in output_nodes:
        if getattr(node, "is_active_output", False):
            return node
    return output_nodes[0] if output_nodes else None


def find_group_internal_output_socket(group_node, external_output_socket):
    if group_node is None or group_node.node_tree is None:
        return None
    output_index = socket_collection_index(group_node.outputs, external_output_socket)
    if output_index < 0:
        return None
    group_output = find_active_group_output_node(group_node.node_tree)
    if group_output is None or output_index >= len(group_output.inputs):
        return None
    return group_output.inputs[output_index]


def find_parent_group_input_socket(parent_group_node, group_input_output_socket):
    if parent_group_node is None:
        return None
    input_index = socket_collection_index(group_input_output_socket.node.outputs, group_input_output_socket)
    if input_index < 0 or input_index >= len(parent_group_node.inputs):
        return None
    return parent_group_node.inputs[input_index]


def default_color_from_socket(socket, count):
    if socket is None:
        return np.zeros((count, 3), dtype=np.float64)
    try:
        default_value = socket.default_value
    except Exception:
        return np.zeros((count, 3), dtype=np.float64)
    if hasattr(default_value, "__len__"):
        values = list(default_value)
        if len(values) >= 3:
            return np.tile(np.asarray(values[:3], dtype=np.float64), (count, 1))
        if len(values) == 1:
            return np.tile(np.asarray([values[0], values[0], values[0]], dtype=np.float64), (count, 1))
    try:
        scalar = float(default_value)
    except Exception:
        scalar = 0.0
    return np.tile(np.asarray([scalar, scalar, scalar], dtype=np.float64), (count, 1))


def default_scalar_from_socket(socket, count):
    if socket is None:
        return np.zeros(count, dtype=np.float64)
    try:
        default_value = socket.default_value
    except Exception:
        return np.zeros(count, dtype=np.float64)
    if hasattr(default_value, "__len__"):
        values = list(default_value)
        if values:
            return np.full(count, float(values[0]), dtype=np.float64)
    try:
        scalar = float(default_value)
    except Exception:
        scalar = 0.0
    return np.full(count, scalar, dtype=np.float64)


def default_vector_from_socket(socket, count, fallback_vectors=None):
    if fallback_vectors is not None and socket is not None and not socket.is_linked:
        try:
            default_value = socket.default_value
        except Exception:
            return np.asarray(fallback_vectors, dtype=np.float64)
        if hasattr(default_value, "__len__"):
            values = list(default_value)
            if len(values) >= 3 and np.linalg.norm(values[:3]) > EPSILON:
                return np.tile(np.asarray(values[:3], dtype=np.float64), (count, 1))
        return np.asarray(fallback_vectors, dtype=np.float64)

    if socket is None:
        return np.zeros((count, 3), dtype=np.float64)
    try:
        default_value = socket.default_value
    except Exception:
        return np.zeros((count, 3), dtype=np.float64)
    if hasattr(default_value, "__len__"):
        values = list(default_value)
        if len(values) >= 3:
            return np.tile(np.asarray(values[:3], dtype=np.float64), (count, 1))
    try:
        scalar = float(default_value)
    except Exception:
        scalar = 0.0
    return np.tile(np.asarray([scalar, scalar, scalar], dtype=np.float64), (count, 1))


def blend_color_arrays(color_a, color_b, factor, blend_type="MIX"):
    color_a = np.asarray(color_a, dtype=np.float64)
    color_b = np.asarray(color_b, dtype=np.float64)
    factor = np.clip(np.asarray(factor, dtype=np.float64).reshape(-1, 1), 0.0, 1.0)
    blend_mode = str(blend_type).upper()

    if blend_mode in ("MIX", "BLEND"):
        mixed = color_b
    elif blend_mode == "ADD":
        mixed = color_a + color_b
    elif blend_mode == "MULTIPLY":
        mixed = color_a * color_b
    elif blend_mode == "SCREEN":
        mixed = 1.0 - ((1.0 - color_a) * (1.0 - color_b))
    elif blend_mode == "SUBTRACT":
        mixed = color_a - color_b
    else:
        mixed = color_b

    return ((1.0 - factor) * color_a) + (factor * mixed)


def get_first_matching_socket(node, socket_names, prefer_outputs=False):
    sockets = node.outputs if prefer_outputs else node.inputs
    for socket_name in socket_names:
        for socket in sockets:
            if socket.name == socket_name:
                return socket
    return None


def register_trace_node(trace, category, node_type):
    if trace is None:
        return
    trace.setdefault(category, set()).add(str(node_type))


def register_trace_image(trace, image_name):
    if trace is None:
        return
    trace.setdefault("image_names", set()).add(str(image_name))


def evaluate_scalar_socket(socket, directions, parent_group_node=None, trace=None, visited=None):
    directions = np.asarray(directions, dtype=np.float64)
    count = len(directions)
    visited = visited or set()
    socket_key = ("SCALAR", id(socket), id(parent_group_node) if parent_group_node is not None else 0)
    if socket_key in visited:
        return default_scalar_from_socket(socket, count)
    visited = set(visited)
    visited.add(socket_key)

    if socket is None or not socket.is_linked:
        return default_scalar_from_socket(socket, count)

    link = socket.links[0]
    node = link.from_node
    output_socket = link.from_socket
    if node is None:
        return default_scalar_from_socket(socket, count)

    register_trace_node(trace, "scalar_node_types", node.type)

    if node.type == "REROUTE" and node.inputs:
        return evaluate_scalar_socket(node.inputs[0], directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
    if node.type == "VALUE":
        return default_scalar_from_socket(output_socket, count)
    if node.type == "GROUP_INPUT":
        parent_socket = find_parent_group_input_socket(parent_group_node, output_socket)
        return evaluate_scalar_socket(parent_socket, directions, parent_group_node=None, trace=trace, visited=visited)
    if node.type == "GROUP":
        internal_socket = find_group_internal_output_socket(node, output_socket)
        return evaluate_scalar_socket(internal_socket, directions, parent_group_node=node, trace=trace, visited=visited)
    if node.type == "MATH":
        operation = str(getattr(node, "operation", "ADD")).upper()
        value_a = evaluate_scalar_socket(node.inputs[0], directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        value_b = evaluate_scalar_socket(node.inputs[1], directions, parent_group_node=parent_group_node, trace=trace, visited=visited) if len(node.inputs) > 1 else np.zeros(count, dtype=np.float64)
        if operation == "ADD":
            return value_a + value_b
        if operation == "SUBTRACT":
            return value_a - value_b
        if operation == "MULTIPLY":
            return value_a * value_b
        if operation == "DIVIDE":
            return value_a / np.maximum(value_b, EPSILON)
        if operation == "POWER":
            return np.power(np.maximum(value_a, 0.0), value_b)
        if operation == "MINIMUM":
            return np.minimum(value_a, value_b)
        if operation == "MAXIMUM":
            return np.maximum(value_a, value_b)
        if operation == "ABSOLUTE":
            return np.abs(value_a)
        if operation == "CLAMP":
            min_value = evaluate_scalar_socket(node.inputs[1], directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
            max_value = evaluate_scalar_socket(node.inputs[2], directions, parent_group_node=parent_group_node, trace=trace, visited=visited) if len(node.inputs) > 2 else np.ones(count, dtype=np.float64)
            return np.clip(value_a, min_value, max_value)
        register_trace_node(trace, "unsupported_scalar_nodes", node.type)
        return value_a
    if node.type in ("SEPXYZ", "SEPARATE_XYZ", "SEP_COLOR", "SEPARATE_COLOR"):
        vector_value = evaluate_vector_socket(
            node.inputs[0],
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
        )
        output_index = socket_collection_index(node.outputs, output_socket)
        output_index = max(0, min(output_index, vector_value.shape[1] - 1))
        return vector_value[:, output_index]

    register_trace_node(trace, "unsupported_scalar_nodes", node.type)
    return default_scalar_from_socket(socket, count)


def evaluate_vector_socket(socket, directions, parent_group_node=None, trace=None, visited=None, fallback_vectors=None):
    directions = np.asarray(directions, dtype=np.float64)
    count = len(directions)
    visited = visited or set()
    socket_key = ("VECTOR", id(socket), id(parent_group_node) if parent_group_node is not None else 0)
    if socket_key in visited:
        return default_vector_from_socket(socket, count, fallback_vectors=fallback_vectors)
    visited = set(visited)
    visited.add(socket_key)

    if socket is None or not socket.is_linked:
        return default_vector_from_socket(socket, count, fallback_vectors=fallback_vectors)

    link = socket.links[0]
    node = link.from_node
    output_socket = link.from_socket
    if node is None:
        return default_vector_from_socket(socket, count, fallback_vectors=fallback_vectors)

    register_trace_node(trace, "vector_node_types", node.type)

    if node.type == "REROUTE" and node.inputs:
        return evaluate_vector_socket(node.inputs[0], directions, parent_group_node=parent_group_node, trace=trace, visited=visited, fallback_vectors=fallback_vectors)
    if node.type in ("TEX_COORD", "NEW_GEOMETRY", "ATTRIBUTE", "UV_MAP"):
        return np.asarray(fallback_vectors if fallback_vectors is not None else directions, dtype=np.float64)
    if node.type == "GROUP_INPUT":
        parent_socket = find_parent_group_input_socket(parent_group_node, output_socket)
        return evaluate_vector_socket(parent_socket, directions, parent_group_node=None, trace=trace, visited=visited, fallback_vectors=fallback_vectors)
    if node.type == "GROUP":
        internal_socket = find_group_internal_output_socket(node, output_socket)
        return evaluate_vector_socket(internal_socket, directions, parent_group_node=node, trace=trace, visited=visited, fallback_vectors=fallback_vectors)
    if node.type == "MAPPING":
        source_vectors = evaluate_vector_socket(
            get_node_input(node, "Vector"),
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
            fallback_vectors=fallback_vectors,
        )
        return apply_mapping_node_to_directions(source_vectors, node)
    if node.type in ("COMBXYZ", "COMBINE_XYZ"):
        x_value = evaluate_scalar_socket(node.inputs[0], directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        y_value = evaluate_scalar_socket(node.inputs[1], directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        z_value = evaluate_scalar_socket(node.inputs[2], directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        return np.column_stack([x_value, y_value, z_value])
    if node.type == "VECTOR_MATH":
        operation = str(getattr(node, "operation", "ADD")).upper()
        vector_a = evaluate_vector_socket(node.inputs[0], directions, parent_group_node=parent_group_node, trace=trace, visited=visited, fallback_vectors=fallback_vectors)
        vector_b = evaluate_vector_socket(node.inputs[1], directions, parent_group_node=parent_group_node, trace=trace, visited=visited, fallback_vectors=fallback_vectors) if len(node.inputs) > 1 else np.zeros_like(vector_a)
        if operation == "ADD":
            return vector_a + vector_b
        if operation == "SUBTRACT":
            return vector_a - vector_b
        if operation == "MULTIPLY":
            return vector_a * vector_b
        if operation == "SCALE":
            scale_value = evaluate_scalar_socket(node.inputs[3], directions, parent_group_node=parent_group_node, trace=trace, visited=visited) if len(node.inputs) > 3 else np.ones(count, dtype=np.float64)
            return vector_a * scale_value[:, None]
        if operation == "NORMALIZE":
            return normalize_vectors(vector_a, fallback=(0.0, 0.0, 1.0))
        register_trace_node(trace, "unsupported_vector_nodes", node.type)
        return vector_a

    register_trace_node(trace, "unsupported_vector_nodes", node.type)
    return default_vector_from_socket(socket, count, fallback_vectors=fallback_vectors)


def evaluate_color_socket(socket, directions, parent_group_node=None, trace=None, visited=None):
    directions = np.asarray(directions, dtype=np.float64)
    count = len(directions)
    visited = visited or set()
    socket_key = ("COLOR", id(socket), id(parent_group_node) if parent_group_node is not None else 0)
    if socket_key in visited:
        return default_color_from_socket(socket, count)
    visited = set(visited)
    visited.add(socket_key)

    if socket is None or not socket.is_linked:
        return default_color_from_socket(socket, count)

    link = socket.links[0]
    node = link.from_node
    output_socket = link.from_socket
    if node is None:
        return default_color_from_socket(socket, count)

    register_trace_node(trace, "color_node_types", node.type)

    if node.type == "REROUTE" and node.inputs:
        return evaluate_color_socket(node.inputs[0], directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
    if node.type == "GROUP_INPUT":
        parent_socket = find_parent_group_input_socket(parent_group_node, output_socket)
        return evaluate_color_socket(parent_socket, directions, parent_group_node=None, trace=trace, visited=visited)
    if node.type == "GROUP":
        internal_socket = find_group_internal_output_socket(node, output_socket)
        return evaluate_color_socket(internal_socket, directions, parent_group_node=node, trace=trace, visited=visited)
    if node.type == "RGB":
        return default_color_from_socket(output_socket, count)
    if node.type == "VALUE":
        scalar = default_scalar_from_socket(output_socket, count)
        return np.repeat(scalar[:, None], 3, axis=1)
    if node.type == "TEX_ENVIRONMENT":
        vector_input = get_node_input(node, "Vector")
        sample_directions = evaluate_vector_socket(
            vector_input,
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
            fallback_vectors=directions,
        ) if vector_input is not None and vector_input.is_linked else directions
        if getattr(node, "image", None) is None:
            return np.zeros((count, 3), dtype=np.float64)
        register_trace_image(trace, node.image.name)
        image_pixels = read_image_rgb_pixels(node.image)
        return sample_equirect_rgb(image_pixels["rgb_pixels"], sample_directions)
    if node.type == "GAMMA":
        source = evaluate_color_socket(get_node_input(node, "Color"), directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        return apply_gamma_node(source, node)
    if node.type in ("HUE_SAT", "HUE_SAT_VAL"):
        source = evaluate_color_socket(get_node_input(node, "Color"), directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        return apply_hue_sat_node(source, node)
    if node.type == "INVERT":
        source = evaluate_color_socket(get_node_input(node, "Color"), directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        return apply_invert_node(source, node)
    if node.type == "BRIGHTCONTRAST":
        source = evaluate_color_socket(get_node_input(node, "Color"), directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        return apply_bright_contrast_node(source, node)
    if node.type in ("MIX_RGB", "MIX"):
        factor_socket = get_first_matching_socket(node, ("Factor", "Fac"))
        color_a_socket = get_first_matching_socket(node, ("A", "Color1", "Color"))
        color_b_socket = get_first_matching_socket(node, ("B", "Color2", "Color"))
        color_a = evaluate_color_socket(color_a_socket, directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        color_b = evaluate_color_socket(color_b_socket, directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        factor = evaluate_scalar_socket(factor_socket, directions, parent_group_node=parent_group_node, trace=trace, visited=visited)
        blend_type = getattr(node, "blend_type", "MIX")
        return blend_color_arrays(color_a, color_b, factor, blend_type=blend_type)

    register_trace_node(trace, "unsupported_color_nodes", node.type)
    return default_color_from_socket(socket, count)


def evaluate_shader_socket(socket, directions, parent_group_node=None, trace=None, visited=None):
    directions = np.asarray(directions, dtype=np.float64)
    count = len(directions)
    visited = visited or set()
    socket_key = ("SHADER", id(socket), id(parent_group_node) if parent_group_node is not None else 0)
    if socket_key in visited:
        return np.zeros((count, 3), dtype=np.float64)
    visited = set(visited)
    visited.add(socket_key)

    if socket is None or not socket.is_linked:
        return np.zeros((count, 3), dtype=np.float64)

    link = socket.links[0]
    node = link.from_node
    output_socket = link.from_socket
    if node is None:
        return np.zeros((count, 3), dtype=np.float64)

    register_trace_node(trace, "shader_node_types", node.type)

    if node.type == "REROUTE" and node.inputs:
        return evaluate_shader_socket(
            node.inputs[0],
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
        )
    if node.type == "GROUP_INPUT":
        parent_socket = find_parent_group_input_socket(parent_group_node, output_socket)
        return evaluate_shader_socket(
            parent_socket,
            directions,
            parent_group_node=None,
            trace=trace,
            visited=visited,
        )
    if node.type == "GROUP":
        internal_socket = find_group_internal_output_socket(node, output_socket)
        return evaluate_shader_socket(
            internal_socket,
            directions,
            parent_group_node=node,
            trace=trace,
            visited=visited,
        )
    if node.type in ("BACKGROUND", "EMISSION"):
        color = evaluate_color_socket(
            get_node_input(node, "Color"),
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
        )
        strength_socket = get_node_input(node, "Strength")
        if strength_socket is None:
            strength = np.ones(count, dtype=np.float64)
        else:
            strength = evaluate_scalar_socket(
                strength_socket,
                directions,
                parent_group_node=parent_group_node,
                trace=trace,
                visited=visited,
            )
        return color * strength[:, None]
    if node.type == "ADD_SHADER":
        shader_a = evaluate_shader_socket(
            node.inputs[0],
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
        )
        shader_b = evaluate_shader_socket(
            node.inputs[1],
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
        )
        return shader_a + shader_b
    if node.type == "MIX_SHADER":
        factor = evaluate_scalar_socket(
            node.inputs[0],
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
        )
        shader_a = evaluate_shader_socket(
            node.inputs[1],
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
        )
        shader_b = evaluate_shader_socket(
            node.inputs[2],
            directions,
            parent_group_node=parent_group_node,
            trace=trace,
            visited=visited,
        )
        return ((1.0 - factor)[:, None] * shader_a) + (factor[:, None] * shader_b)
    if node.type in ("HOLDOUT", "BSDF_TRANSPARENT"):
        return np.zeros((count, 3), dtype=np.float64)

    register_trace_node(trace, "unsupported_shader_nodes", node.type)
    return np.zeros((count, 3), dtype=np.float64)


def find_world_background_context(world):
    if world is None or world.node_tree is None:
        return None

    def recurse_surface_input(surface_input, parent_group_node=None, visited=None):
        visited = visited or set()
        if surface_input is None or not surface_input.is_linked:
            return None
        link = surface_input.links[0]
        node = link.from_node
        output_socket = link.from_socket
        if node is None:
            return None
        node_key = (id(node), id(parent_group_node) if parent_group_node is not None else 0)
        if node_key in visited:
            return None
        visited = set(visited)
        visited.add(node_key)

        if node.type == "REROUTE" and node.inputs:
            return recurse_surface_input(node.inputs[0], parent_group_node=parent_group_node, visited=visited)
        if node.type == "BACKGROUND":
            return {"background_node": node, "parent_group_node": parent_group_node}
        if node.type == "GROUP" and node.node_tree is not None:
            internal_socket = find_group_internal_output_socket(node, output_socket)
            if internal_socket is not None:
                found = recurse_surface_input(internal_socket, parent_group_node=node, visited=visited)
                if found is not None:
                    return found
        for input_socket in getattr(node, "inputs", []):
            if input_socket.is_linked:
                found = recurse_surface_input(input_socket, parent_group_node=parent_group_node, visited=visited)
                if found is not None:
                    return found
        return None

    output_nodes = [node for node in world.node_tree.nodes if node.type == "OUTPUT_WORLD"]
    for output_node in output_nodes:
        found = recurse_surface_input(get_node_input(output_node, "Surface"))
        if found is not None:
            return found
    return None


def evaluate_active_world_environment(sample_height=64, extra_rotation_degrees=0.0):
    scene = bpy.context.scene
    world = scene.world
    if world is None or world.node_tree is None:
        raise ProxySurfaceRelightError("The current scene has no world environment to sample.")
    output_nodes = [node for node in world.node_tree.nodes if node.type == "OUTPUT_WORLD"]
    active_output = next((node for node in output_nodes if getattr(node, "is_active_output", False)), None)
    world_output = active_output or (output_nodes[0] if output_nodes else None)
    if world_output is None:
        raise ProxySurfaceRelightError("Could not find an active World Output node.")

    sample_height = max(int(sample_height), 4)
    sample_width = max(sample_height * 2, 8)
    directions = build_equirect_sample_grid(sample_width, sample_height)
    if abs(float(extra_rotation_degrees)) > 1.0e-12:
        directions = rotate_directions_z(directions, float(extra_rotation_degrees))

    trace = {
        "image_names": set(),
        "color_node_types": set(),
        "vector_node_types": set(),
        "scalar_node_types": set(),
        "shader_node_types": set(),
        "unsupported_color_nodes": set(),
        "unsupported_vector_nodes": set(),
        "unsupported_scalar_nodes": set(),
        "unsupported_shader_nodes": set(),
    }
    rgb_pixels = evaluate_shader_socket(
        get_node_input(world_output, "Surface"),
        directions,
        trace=trace,
    ).reshape(sample_height, sample_width, 3)

    return {
        "image": None,
        "rgb_pixels": rgb_pixels.astype(np.float32),
        "width": int(sample_width),
        "height": int(sample_height),
        "strength": 1.0,
        "tint": np.array([1.0, 1.0, 1.0], dtype=np.float64),
        "rotation_z_degrees": 0.0,
        "vector_nodes": [],
        "color_nodes": [],
        "vector_node_types": sorted(trace["vector_node_types"]),
        "color_node_types": sorted(trace["color_node_types"] | trace["shader_node_types"]),
        "unsupported_vector_nodes": sorted(trace["unsupported_vector_nodes"]),
        "unsupported_color_nodes": sorted(
            trace["unsupported_color_nodes"]
            | trace["unsupported_scalar_nodes"]
            | trace["unsupported_shader_nodes"]
        ),
        "world_name": world.name,
        "image_color_space": "World Graph",
        "is_float": True,
        "image_name": ", ".join(sorted(trace["image_names"])) if trace["image_names"] else world.name,
        "applied_color_nodes": sorted(trace["color_node_types"] | trace["shader_node_types"]),
        "skipped_color_nodes": sorted(
            trace["unsupported_color_nodes"]
            | trace["unsupported_scalar_nodes"]
            | trace["unsupported_shader_nodes"]
        ),
    }


def find_world_background_node(world):
    if world is None or world.node_tree is None:
        return None
    output_nodes = [node for node in world.node_tree.nodes if node.type == "OUTPUT_WORLD"]
    for output_node in output_nodes:
        background_node = trace_linked_node(get_node_input(output_node, "Surface"))
        if background_node is not None and background_node.type == "BACKGROUND":
            return background_node
    return None


def find_upstream_environment_node(node_input):
    node = trace_linked_node(node_input)
    if node is None:
        return None
    if node.type == "TEX_ENVIRONMENT":
        return node
    for input_socket in getattr(node, "inputs", []):
        found = find_upstream_environment_node(input_socket)
        if found is not None:
            return found
    return None


def resolve_active_world_environment():
    scene = bpy.context.scene
    world = scene.world
    if world is None or world.node_tree is None:
        raise ProxySurfaceRelightError("The current scene has no world environment to sample.")

    background_node = find_world_background_node(world)
    if background_node is None:
        raise ProxySurfaceRelightError(
            "Could not find an active Background node connected to the World Output."
        )

    color_input = get_node_input(background_node, "Color")
    environment_path = find_environment_path_from_input(color_input)
    if environment_path is None:
        raise ProxySurfaceRelightError(
            "Could not find an Environment Texture feeding the active world background."
        )
    environment_node = environment_path["environment_node"]

    strength = 1.0
    tint = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    vector_nodes_info = collect_vector_transform_nodes(get_node_input(environment_node, "Vector"))
    vector_nodes = vector_nodes_info["nodes"]
    vector_node_types = [node.type for node in vector_nodes]
    unsupported_vector_nodes = vector_nodes_info["unsupported"]
    color_node_types = [node.type for node in environment_path["color_nodes"]]
    unsupported_color_nodes = []

    try:
        strength = float(background_node.inputs["Strength"].default_value)
    except Exception:
        strength = 1.0
    if color_input is not None and color_input.is_linked:
        tint = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    else:
        try:
            tint = np.array(background_node.inputs["Color"].default_value[:3], dtype=np.float64)
        except Exception:
            tint = np.array([1.0, 1.0, 1.0], dtype=np.float64)

    rotation_z_degrees = 0.0
    for node in vector_nodes:
        if node.type == "MAPPING":
            try:
                rotation_z_degrees += math.degrees(float(node.inputs["Rotation"].default_value[2]))
            except Exception:
                pass

    return {
        "image": environment_node.image,
        "strength": strength,
        "tint": tint,
        "rotation_z_degrees": rotation_z_degrees,
        "vector_nodes": vector_nodes,
        "vector_node_types": vector_node_types,
        "unsupported_vector_nodes": unsupported_vector_nodes,
        "color_nodes": environment_path["color_nodes"],
        "color_node_types": color_node_types,
        "unsupported_color_nodes": unsupported_color_nodes,
        "world_name": world.name,
    }


def load_environment_image(hdri_image_path=""):
    image_ref = str(hdri_image_path).strip()
    strength = 1.0
    tint = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    rotation_z_degrees = 0.0
    vector_nodes = []
    color_nodes = []
    vector_node_types = []
    color_node_types = []
    unsupported_vector_nodes = []
    unsupported_color_nodes = []
    world_name = ""

    if image_ref:
        image = bpy.data.images.get(image_ref)
        if image is None:
            normalized_path = bpy.path.abspath(image_ref)
            if not os.path.isfile(normalized_path):
                raise ProxySurfaceRelightError(
                    f"HDRI image '{hdri_image_path}' was not found as a Blender image name or file path."
                )
            image = bpy.data.images.load(normalized_path, check_existing=True)
    else:
        world_setup = resolve_active_world_environment()
        image = world_setup["image"]
        strength = float(world_setup["strength"])
        tint = np.asarray(world_setup["tint"], dtype=np.float64)
        rotation_z_degrees = float(world_setup["rotation_z_degrees"])
        vector_nodes = list(world_setup["vector_nodes"])
        color_nodes = list(world_setup["color_nodes"])
        vector_node_types = list(world_setup["vector_node_types"])
        color_node_types = list(world_setup["color_node_types"])
        unsupported_vector_nodes = list(world_setup["unsupported_vector_nodes"])
        unsupported_color_nodes = list(world_setup["unsupported_color_nodes"])
        world_name = str(world_setup["world_name"])

    image_pixels = read_image_rgb_pixels(image)
    return {
        "image": image,
        "rgb_pixels": image_pixels["rgb_pixels"],
        "width": int(image_pixels["width"]),
        "height": int(image_pixels["height"]),
        "strength": strength,
        "tint": tint,
        "rotation_z_degrees": rotation_z_degrees,
        "vector_nodes": vector_nodes,
        "color_nodes": color_nodes,
        "vector_node_types": vector_node_types,
        "color_node_types": color_node_types,
        "unsupported_vector_nodes": unsupported_vector_nodes,
        "unsupported_color_nodes": unsupported_color_nodes,
        "world_name": world_name,
        "image_color_space": str(image_pixels["color_space"]),
        "is_float": bool(image_pixels["is_float"]),
        "image_name": str(image.name),
        "applied_color_nodes": [],
        "skipped_color_nodes": unsupported_color_nodes,
    }


def clamp_environment_luminance(image_rgb, luminance_clamp=0.0):
    image_rgb = np.asarray(image_rgb, dtype=np.float64)
    luminance_clamp = float(luminance_clamp)
    if luminance_clamp <= 0.0:
        return image_rgb.copy()
    luminance = compute_color_luminance(image_rgb.reshape(-1, 3)).reshape(
        image_rgb.shape[0],
        image_rgb.shape[1],
        1,
    )
    scale = np.minimum(1.0, luminance_clamp / np.maximum(luminance, EPSILON))
    return image_rgb * scale


def read_image_rgb_pixels(image):
    if image is None:
        raise ProxySurfaceRelightError("Image reference is None.")

    width = int(image.size[0])
    height = int(image.size[1])
    if width > 0 and height > 0 and len(image.pixels) > 0:
        pixel_array = np.array(image.pixels[:], dtype=np.float32)
        component_count = len(pixel_array) // max(width * height, 1)
        if component_count < 3:
            raise ProxySurfaceRelightError(
                f"Image '{image.name}' does not contain RGB pixel data."
            )
        pixel_array = pixel_array.reshape(height, width, component_count)
        return {
            "rgb_pixels": pixel_array[:, :, :3].astype(np.float32),
            "width": width,
            "height": height,
            "color_space": str(getattr(image.colorspace_settings, "name", "Unknown")),
            "is_float": bool(getattr(image, "is_float", False)),
        }

    try:
        image.reload()
    except Exception:
        pass

    width = int(image.size[0])
    height = int(image.size[1])
    if width > 0 and height > 0 and len(image.pixels) > 0:
        pixel_array = np.array(image.pixels[:], dtype=np.float32)
        component_count = len(pixel_array) // max(width * height, 1)
        if component_count < 3:
            raise ProxySurfaceRelightError(
                f"Image '{image.name}' does not contain RGB pixel data after reload."
            )
        pixel_array = pixel_array.reshape(height, width, component_count)
        return {
            "rgb_pixels": pixel_array[:, :, :3].astype(np.float32),
            "width": width,
            "height": height,
            "color_space": str(getattr(image.colorspace_settings, "name", "Unknown")),
            "is_float": bool(getattr(image, "is_float", False)),
        }

    candidate_paths = []
    for raw_path in (
        getattr(image, "filepath_raw", ""),
        getattr(image, "filepath", ""),
    ):
        resolved = bpy.path.abspath(raw_path) if raw_path else ""
        if resolved and resolved not in candidate_paths:
            candidate_paths.append(resolved)
    try:
        user_path = image.filepath_from_user()
        resolved_user_path = bpy.path.abspath(user_path) if user_path else ""
        if resolved_user_path and resolved_user_path not in candidate_paths:
            candidate_paths.append(resolved_user_path)
    except Exception:
        pass

    image_path = next((path for path in candidate_paths if os.path.isfile(path)), "")
    if not image_path:
        raise ProxySurfaceRelightError(
            f"Image '{image.name}' has no loaded pixel buffer and its file path could not be resolved. "
            f"Tried: {candidate_paths}"
        )

    temp_image = bpy.data.images.load(image_path, check_existing=False)
    try:
        width = int(temp_image.size[0])
        height = int(temp_image.size[1])
        if width <= 0 or height <= 0 or len(temp_image.pixels) == 0:
            raise ProxySurfaceRelightError(
                f"Image '{image.name}' could not be loaded from '{image_path}'."
            )
        pixel_array = np.array(temp_image.pixels[:], dtype=np.float32)
        component_count = len(pixel_array) // max(width * height, 1)
        if component_count < 3:
            raise ProxySurfaceRelightError(
                f"Image '{image.name}' loaded from '{image_path}' does not contain RGB pixel data."
            )
        pixel_array = pixel_array.reshape(height, width, component_count)
        return {
            "rgb_pixels": pixel_array[:, :, :3].astype(np.float32),
            "width": width,
            "height": height,
            "color_space": str(getattr(temp_image.colorspace_settings, "name", "Unknown")),
            "is_float": bool(getattr(temp_image, "is_float", False)),
        }
    finally:
        bpy.data.images.remove(temp_image)


def rotate_directions_z(directions, degrees):
    directions = np.asarray(directions, dtype=np.float64)
    angle = math.radians(float(degrees))
    if abs(angle) <= 1.0e-12:
        return directions.copy()
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    rotated = directions.copy()
    rotated[:, 0] = cos_angle * directions[:, 0] - sin_angle * directions[:, 1]
    rotated[:, 1] = sin_angle * directions[:, 0] + cos_angle * directions[:, 1]
    return rotated


def sample_equirect_rgb(image_rgb, directions):
    directions = normalize_vectors(directions)
    width = image_rgb.shape[1]
    height = image_rgb.shape[0]

    longitude = np.arctan2(directions[:, 0], directions[:, 1])
    latitude = np.arcsin(np.clip(directions[:, 2], -1.0, 1.0))

    u = (longitude / (2.0 * math.pi) + 0.5) % 1.0
    v = np.clip(0.5 - latitude / math.pi, 0.0, 1.0)

    x = u * (width - 1)
    y = v * (height - 1)

    x0 = np.floor(x).astype(np.int32)
    y0 = np.floor(y).astype(np.int32)
    x1 = (x0 + 1) % width
    y1 = np.clip(y0 + 1, 0, height - 1)

    xw = (x - x0).astype(np.float32)
    yw = (y - y0).astype(np.float32)

    top_left = image_rgb[y0, x0]
    top_right = image_rgb[y0, x1]
    bottom_left = image_rgb[y1, x0]
    bottom_right = image_rgb[y1, x1]

    top = top_left * (1.0 - xw[:, None]) + top_right * xw[:, None]
    bottom = bottom_left * (1.0 - xw[:, None]) + bottom_right * xw[:, None]
    return top * (1.0 - yw[:, None]) + bottom * yw[:, None]


def build_equirect_sample_grid(width, height):
    width = max(int(width), 1)
    height = max(int(height), 1)
    u = (np.arange(width, dtype=np.float64) + 0.5) / float(width)
    v = (np.arange(height, dtype=np.float64) + 0.5) / float(height)
    uu, vv = np.meshgrid(u, v)
    longitude = (uu - 0.5) * (2.0 * math.pi)
    latitude = (0.5 - vv) * math.pi
    cos_lat = np.cos(latitude)
    x = np.sin(longitude) * cos_lat
    y = np.cos(longitude) * cos_lat
    z = np.sin(latitude)
    return np.stack([x, y, z], axis=-1).reshape(-1, 3)


def resize_equirect_image(image_rgb, target_width, target_height):
    target_width = max(int(target_width), 1)
    target_height = max(int(target_height), 1)
    sample_dirs = build_equirect_sample_grid(target_width, target_height)
    sampled = sample_equirect_rgb(np.asarray(image_rgb, dtype=np.float64), sample_dirs)
    return sampled.reshape(target_height, target_width, 3)


def blur_equirect_image(image_rgb, blur_strength):
    iterations = max(int(round(float(blur_strength))), 0)
    blurred = np.asarray(image_rgb, dtype=np.float64).copy()
    for _ in range(iterations):
        left = np.roll(blurred, 1, axis=1)
        right = np.roll(blurred, -1, axis=1)
        up = np.vstack([blurred[0:1], blurred[:-1]])
        down = np.vstack([blurred[1:], blurred[-1:]])
        blurred = (blurred + left + right + up + down) / 5.0
    return blurred


def build_irradiance_map(
    image_rgb,
    resolution=32,
    blur_strength=6,
    luminance_clamp=20.0,
    color_nodes=None,
):
    filtered = clamp_environment_luminance(image_rgb, luminance_clamp=luminance_clamp)
    target_height = max(int(round(float(resolution))), 4)
    target_width = max(target_height * 2, 8)
    low_frequency = resize_equirect_image(filtered, target_width, target_height)
    applied_color_nodes = []
    skipped_color_nodes = []
    if color_nodes:
        processed = np.asarray(low_frequency, dtype=np.float64)
        for node in color_nodes:
            processed, supported = apply_color_node_to_pixels(processed, node)
            if supported:
                applied_color_nodes.append(node.type)
            else:
                skipped_color_nodes.append(node.type)
        low_frequency = processed
    irradiance_map = blur_equirect_image(low_frequency, blur_strength)
    return {
        "rgb_pixels": irradiance_map.astype(np.float32),
        "width": int(target_width),
        "height": int(target_height),
        "luminance_clamp": float(luminance_clamp),
        "applied_color_nodes": applied_color_nodes,
        "skipped_color_nodes": skipped_color_nodes,
    }


def build_proxy_lighting_cache(
    mesh_obj,
    proxy_obj=None,
    hdri_image_path="",
    base_color_source_mode="Saved Original",
    clamp_base_color=True,
    use_evaluated_proxy=True,
    normal_smoothing=0.0,
    pre_light_smoothing=0.0,
    post_light_smoothing=0.0,
    transfer_style="Accurate",
    transfer_smoothness=0.5,
    include_world_environment=True,
    include_scene_lights=True,
    scene_light_gain=1.0,
    use_light_shadows=True,
    include_hidden_lights=False,
    use_proxy_occlusion=True,
    occlusion_sample_count=6,
    occlusion_bias=0.002,
    occlusion_max_distance=0.0,
    light_shadow_bias=0.002,
    environment_rotation_degrees=0.0,
    irradiance_resolution=32,
    irradiance_blur_strength=8,
    irradiance_luminance_clamp=10.0,
    relight_cache_root="",
    proxy_binding_utils_path="",
    progress_callback=None,
):
    progress_total = 13
    call_progress_callback(progress_callback, 1, progress_total, "Resolving proxy settings...")
    proxy_obj = resolve_proxy_mesh_object(
        mesh_obj,
        proxy_obj=proxy_obj,
        proxy_binding_utils_path=proxy_binding_utils_path,
    )
    call_progress_callback(progress_callback, 2, progress_total, "Binding splats to the proxy surface...")
    surface_info = build_proxy_surface_binding(
        mesh_obj,
        proxy_obj,
        use_evaluated_proxy=use_evaluated_proxy,
        proxy_binding_utils_path=proxy_binding_utils_path,
    )
    call_progress_callback(progress_callback, 3, progress_total, "Reading base color from f_dc...")
    base_color_result = evaluate_base_color_from_f_dc(
        mesh_obj,
        clamp_base_color=clamp_base_color,
        source_mode=base_color_source_mode,
        relight_cache_root=relight_cache_root,
        proxy_binding_utils_path=proxy_binding_utils_path,
    )
    base_color = np.asarray(base_color_result["logical_color"], dtype=np.float64)

    use_world_environment = bool(include_world_environment or str(hdri_image_path).strip())
    if use_world_environment:
        call_progress_callback(progress_callback, 4, progress_total, "Loading and evaluating World / HDRI lighting...")
        if str(hdri_image_path).strip():
            image_info = load_environment_image(hdri_image_path)
            call_progress_callback(progress_callback, 5, progress_total, "Building blurred HDRI irradiance map...")
            irradiance_info = build_irradiance_map(
                image_info["rgb_pixels"],
                resolution=irradiance_resolution,
                blur_strength=irradiance_blur_strength,
                luminance_clamp=irradiance_luminance_clamp,
                color_nodes=image_info["color_nodes"],
            )
        else:
            world_sample_resolution = max(int(irradiance_resolution) * 4, 32)
            image_info = evaluate_active_world_environment(
                sample_height=world_sample_resolution,
                extra_rotation_degrees=environment_rotation_degrees,
            )
            call_progress_callback(progress_callback, 5, progress_total, "Building blurred World irradiance map...")
            irradiance_info = build_irradiance_map(
                image_info["rgb_pixels"],
                resolution=irradiance_resolution,
                blur_strength=irradiance_blur_strength,
                luminance_clamp=irradiance_luminance_clamp,
                color_nodes=None,
            )
    else:
        image_info = {
            "image": None,
            "rgb_pixels": None,
            "width": 0,
            "height": 0,
            "strength": 1.0,
            "tint": np.array([1.0, 1.0, 1.0], dtype=np.float64),
            "rotation_z_degrees": 0.0,
            "vector_nodes": [],
            "color_nodes": [],
            "vector_node_types": [],
            "color_node_types": [],
            "unsupported_vector_nodes": [],
            "unsupported_color_nodes": [],
            "world_name": "",
            "image_color_space": "Unknown",
            "is_float": False,
            "image_name": "",
            "applied_color_nodes": [],
            "skipped_color_nodes": [],
        }
        irradiance_info = {
            "rgb_pixels": np.zeros((max(int(irradiance_resolution), 4), max(int(irradiance_resolution) * 2, 8), 3), dtype=np.float32),
            "width": max(int(irradiance_resolution) * 2, 8),
            "height": max(int(irradiance_resolution), 4),
            "luminance_clamp": float(irradiance_luminance_clamp),
            "applied_color_nodes": [],
            "skipped_color_nodes": [],
        }

    call_progress_callback(progress_callback, 6, progress_total, "Preparing proxy BVH, normals, and smoothing graph...")
    proxy_bvh = build_proxy_bvh(
        surface_info["proxy_vertices_world"],
        surface_info["triangle_vertex_indices"],
    )
    proxy_vertex_positions = np.asarray(surface_info["proxy_vertices_world"], dtype=np.float64)
    proxy_vertex_normals = np.asarray(surface_info["proxy_vertex_normals_world"], dtype=np.float64)
    triangle_vertex_indices = np.asarray(surface_info["triangle_vertex_indices"], dtype=np.int32)
    bound_triangle_vertex_indices = np.asarray(surface_info["bound_triangle_vertex_indices"], dtype=np.int32)
    bound_triangle_barycentric = np.asarray(surface_info["bound_triangle_barycentric"], dtype=np.float64)
    bound_triangle_ids = np.asarray(surface_info["bound_triangle_ids"], dtype=np.int32)
    vertex_edges = build_bidirectional_vertex_edges(triangle_vertex_indices)
    triangle_edges = build_bidirectional_triangle_edges(triangle_vertex_indices)

    normal_smoothing = float(np.clip(normal_smoothing, 0.0, 1.0))
    pre_light_smoothing = float(np.clip(pre_light_smoothing, 0.0, 1.0))
    post_light_smoothing = float(np.clip(post_light_smoothing, 0.0, 1.0))
    transfer_smoothness = float(np.clip(transfer_smoothness, 0.0, 1.0))

    proxy_vertex_normals_for_lighting = proxy_vertex_normals.copy()
    if normal_smoothing > EPSILON:
        proxy_vertex_normals_for_lighting = smooth_values_over_edges(
            proxy_vertex_normals_for_lighting,
            vertex_edges,
            strength=normal_smoothing,
            pass_count=3,
            normalize_result=True,
        )

    vector_nodes = list(image_info["vector_nodes"])
    total_rotation = float(image_info["rotation_z_degrees"]) + (
        float(environment_rotation_degrees) if str(hdri_image_path).strip() else 0.0
    )
    world_directions = proxy_vertex_normals_for_lighting.copy()
    if abs(float(environment_rotation_degrees)) > 1.0e-12:
        world_directions = rotate_directions_z(world_directions, float(environment_rotation_degrees))
    world_directions = apply_vector_nodes_to_directions(world_directions, vector_nodes)

    call_progress_callback(progress_callback, 7, progress_total, "Sampling indirect HDRI light on the proxy...")
    environment_rgb_vertices = np.zeros((len(proxy_vertex_positions), 3), dtype=np.float64)
    occlusion_vertices = np.ones(len(proxy_vertex_positions), dtype=np.float64)
    if use_world_environment and include_world_environment:
        environment_rgb_vertices = sample_equirect_rgb(irradiance_info["rgb_pixels"], world_directions)
        environment_rgb_vertices = (
            environment_rgb_vertices
            * image_info["tint"][None, :]
            * float(image_info["strength"])
        )
        if use_proxy_occlusion:
            call_progress_callback(progress_callback, 8, progress_total, "Ray-casting proxy occlusion for HDRI shadowing...")
            occlusion_vertices = compute_surface_occlusion_factors(
                proxy_vertex_positions,
                proxy_vertex_normals,
                proxy_bvh,
                sample_count=occlusion_sample_count,
                bias=occlusion_bias,
                max_distance=occlusion_max_distance,
                source_triangle_ids=None,
            )

    direct_unshadowed_eval = {
        "lights": [],
        "light_rgb": np.zeros((len(proxy_vertex_positions), 3), dtype=np.float64),
        "light_count": 0,
        "per_light_stats": [],
    }
    direct_shadowed_eval = {
        "lights": [],
        "light_rgb": np.zeros((len(proxy_vertex_positions), 3), dtype=np.float64),
        "light_count": 0,
        "per_light_stats": [],
    }
    if include_scene_lights:
        call_progress_callback(progress_callback, 9, progress_total, "Evaluating Blender scene lights and direct shadows...")
        direct_unshadowed_eval = evaluate_scene_lights_on_samples(
            proxy_vertex_positions,
            proxy_vertex_normals_for_lighting,
            proxy_bvh,
            scene_light_gain=scene_light_gain,
            use_light_shadows=False,
            direct_shadow_strength=1.0,
            shadow_bias=light_shadow_bias,
            include_hidden_lights=include_hidden_lights,
            source_triangle_ids=None,
        )
        direct_shadowed_eval = evaluate_scene_lights_on_samples(
            proxy_vertex_positions,
            proxy_vertex_normals_for_lighting,
            proxy_bvh,
            scene_light_gain=scene_light_gain,
            use_light_shadows=use_light_shadows,
            direct_shadow_strength=1.0,
            shadow_bias=light_shadow_bias,
            include_hidden_lights=include_hidden_lights,
            source_triangle_ids=None,
        )

    direct_unshadowed_vertices = np.asarray(direct_unshadowed_eval["light_rgb"], dtype=np.float64)
    direct_shadowed_vertices = np.asarray(direct_shadowed_eval["light_rgb"], dtype=np.float64)
    if pre_light_smoothing > EPSILON:
        call_progress_callback(progress_callback, 10, progress_total, "Smoothing proxy lighting before transfer...")
        environment_rgb_vertices = smooth_values_over_edges(
            environment_rgb_vertices,
            vertex_edges,
            strength=pre_light_smoothing,
            pass_count=3,
            normalize_result=False,
        )
        direct_unshadowed_vertices = smooth_values_over_edges(
            direct_unshadowed_vertices,
            vertex_edges,
            strength=pre_light_smoothing,
            pass_count=3,
            normalize_result=False,
        )
        direct_shadowed_vertices = smooth_values_over_edges(
            direct_shadowed_vertices,
            vertex_edges,
            strength=pre_light_smoothing,
            pass_count=3,
            normalize_result=False,
        )

    call_progress_callback(progress_callback, 11, progress_total, "Transferring proxy lighting layers to splats...")
    indirect_color, resolved_transfer_style, resolved_transfer_blend = interpolate_triangle_vertex_values_with_style(
        environment_rgb_vertices,
        bound_triangle_vertex_indices,
        bound_triangle_barycentric,
        transfer_style=transfer_style,
        transfer_smoothness=transfer_smoothness,
    )
    occlusion_factor, _, _ = interpolate_triangle_vertex_values_with_style(
        occlusion_vertices,
        bound_triangle_vertex_indices,
        bound_triangle_barycentric,
        transfer_style=transfer_style,
        transfer_smoothness=transfer_smoothness,
    )
    direct_color, _, _ = interpolate_triangle_vertex_values_with_style(
        direct_unshadowed_vertices,
        bound_triangle_vertex_indices,
        bound_triangle_barycentric,
        transfer_style=transfer_style,
        transfer_smoothness=transfer_smoothness,
    )
    direct_shadowed_color, _, _ = interpolate_triangle_vertex_values_with_style(
        direct_shadowed_vertices,
        bound_triangle_vertex_indices,
        bound_triangle_barycentric,
        transfer_style=transfer_style,
        transfer_smoothness=transfer_smoothness,
    )

    if post_light_smoothing > EPSILON:
        call_progress_callback(progress_callback, 12, progress_total, "Smoothing transferred splat lighting and shadows...")
        indirect_color = smooth_transferred_values_by_triangle(
            indirect_color,
            bound_triangle_ids,
            triangle_vertex_indices,
            triangle_edges,
            strength=post_light_smoothing,
            triangle_fallback_values=build_triangle_value_fallback(
                environment_rgb_vertices,
                triangle_vertex_indices,
            ),
        )
        direct_color = smooth_transferred_values_by_triangle(
            direct_color,
            bound_triangle_ids,
            triangle_vertex_indices,
            triangle_edges,
            strength=post_light_smoothing,
            triangle_fallback_values=build_triangle_value_fallback(
                direct_unshadowed_vertices,
                triangle_vertex_indices,
            ),
        )
        direct_shadowed_color = smooth_transferred_values_by_triangle(
            direct_shadowed_color,
            bound_triangle_ids,
            triangle_vertex_indices,
            triangle_edges,
            strength=post_light_smoothing,
            triangle_fallback_values=build_triangle_value_fallback(
                direct_shadowed_vertices,
                triangle_vertex_indices,
            ),
        )
        occlusion_factor = smooth_transferred_values_by_triangle(
            occlusion_factor,
            bound_triangle_ids,
            triangle_vertex_indices,
            triangle_edges,
            strength=post_light_smoothing,
            triangle_fallback_values=build_triangle_value_fallback(
                occlusion_vertices,
                triangle_vertex_indices,
            ),
        )

    direct_luminance_raw = compute_color_luminance(direct_color).reshape(-1)
    direct_luminance_shadowed = compute_color_luminance(direct_shadowed_color).reshape(-1)
    shadow_factor = np.ones(len(direct_color), dtype=np.float64)
    active_direct = direct_luminance_raw > EPSILON
    if np.any(active_direct):
        shadow_factor[active_direct] = np.clip(
            direct_luminance_shadowed[active_direct]
            / np.maximum(direct_luminance_raw[active_direct], EPSILON),
            0.0,
            1.0,
        )
    if post_light_smoothing > EPSILON:
        triangle_direct_luminance_raw = compute_color_luminance(
            build_triangle_value_fallback(direct_unshadowed_vertices, triangle_vertex_indices)
        ).reshape(-1)
        triangle_direct_luminance_shadowed = compute_color_luminance(
            build_triangle_value_fallback(direct_shadowed_vertices, triangle_vertex_indices)
        ).reshape(-1)
        triangle_shadow_fallback = np.ones(len(triangle_direct_luminance_raw), dtype=np.float64)
        active_triangle_direct = triangle_direct_luminance_raw > EPSILON
        if np.any(active_triangle_direct):
            triangle_shadow_fallback[active_triangle_direct] = np.clip(
                triangle_direct_luminance_shadowed[active_triangle_direct]
                / np.maximum(triangle_direct_luminance_raw[active_triangle_direct], EPSILON),
                0.0,
                1.0,
            )
        shadow_factor = smooth_transferred_values_by_triangle(
            shadow_factor,
            bound_triangle_ids,
            triangle_vertex_indices,
            triangle_edges,
            strength=post_light_smoothing,
            triangle_fallback_values=triangle_shadow_fallback,
        )

    cache = {
        "base_color": base_color,
        "indirect_color": indirect_color.astype(np.float64),
        "direct_color": direct_color.astype(np.float64),
        "occlusion_factor": occlusion_factor.astype(np.float64),
        "shadow_factor": shadow_factor.astype(np.float64),
        "logical_count": int(len(base_color)),
    }
    call_progress_callback(progress_callback, 13, progress_total, "Saving baked lighting cache...")
    bake_metadata = {
        "object_name": mesh_obj.name,
        "baked_at_utc": utc_now_iso(),
        "logical_splat_count": int(len(base_color)),
        "proxy_name": surface_info["proxy_name"],
        "image_name": str(image_info.get("image_name", image_info["image"].name if image_info["image"] is not None else "")),
        "image_size": [int(image_info["width"]), int(image_info["height"])],
        "image_strength": float(image_info["strength"]),
        "image_tint": [float(value) for value in image_info["tint"]],
        "image_color_space": str(image_info["image_color_space"]),
        "image_is_float": bool(image_info["is_float"]),
        "world_name": str(image_info["world_name"]),
        "world_rotation_degrees": float(image_info["rotation_z_degrees"]),
        "total_rotation_degrees": total_rotation,
        "scene_light_count": int(direct_shadowed_eval["light_count"]),
        "vector_node_types": list(image_info["vector_node_types"]),
        "unsupported_vector_nodes": list(image_info["unsupported_vector_nodes"]),
        "color_node_types": list(image_info["color_node_types"]),
        "unsupported_color_nodes": list(image_info["unsupported_color_nodes"]),
        "base_color_source_mode": str(base_color_result["mode"]),
        "normal_smoothing": float(normal_smoothing),
        "pre_light_smoothing": float(pre_light_smoothing),
        "post_light_smoothing": float(post_light_smoothing),
        "transfer_style": str(resolved_transfer_style),
        "transfer_smoothness": float(transfer_smoothness),
        "transfer_smoothness_blend": float(resolved_transfer_blend),
        "proxy_interpolation_mode": f"Vertex Lighting + {resolved_transfer_style} Transfer",
    }
    paths = save_baked_lighting_cache(
        mesh_obj,
        cache,
        bake_metadata,
        relight_cache_root=relight_cache_root,
    )
    clear_temp_attributes(mesh_obj)
    clear_legacy_relight_properties(mesh_obj)
    sync_stage_state_properties(mesh_obj, relight_cache_root=relight_cache_root)

    return {
        "logical_splat_count": int(len(base_color)),
        "proxy_name": surface_info["proxy_name"],
        "base_color": base_color.astype(np.float64),
        "base_color_source_color": np.asarray(base_color_result["source_color"], dtype=np.float64),
        "base_color_source_mode": str(base_color_result["mode"]),
        "base_color_f_dc_coeffs": np.asarray(base_color_result["f_dc_coeffs"], dtype=np.float64),
        "environment_rgb": indirect_color.astype(np.float64),
        "environment_rgb_vertices": environment_rgb_vertices.astype(np.float64),
        "indirect_color": indirect_color.astype(np.float64),
        "direct_color": direct_color.astype(np.float64),
        "direct_shadowed_color": direct_shadowed_color.astype(np.float64),
        "image_name": str(image_info.get("image_name", image_info["image"].name if image_info["image"] is not None else "")),
        "image_size": (int(image_info["width"]), int(image_info["height"])),
        "image_strength": float(image_info["strength"]),
        "image_tint": np.asarray(image_info["tint"], dtype=np.float64),
        "image_color_space": str(image_info["image_color_space"]),
        "image_is_float": bool(image_info["is_float"]),
        "world_name": str(image_info["world_name"]),
        "world_rotation_degrees": float(image_info["rotation_z_degrees"]),
        "total_rotation_degrees": total_rotation,
        "irradiance_image_size": (
            int(irradiance_info["width"]),
            int(irradiance_info["height"]),
        ),
        "irradiance_map": np.asarray(irradiance_info["rgb_pixels"], dtype=np.float64),
        "applied_color_nodes": list(image_info.get("applied_color_nodes", irradiance_info["applied_color_nodes"])),
        "skipped_color_nodes": list(image_info.get("skipped_color_nodes", irradiance_info["skipped_color_nodes"])),
        "vector_node_types": list(image_info["vector_node_types"]),
        "unsupported_vector_nodes": list(image_info["unsupported_vector_nodes"]),
        "color_node_types": list(image_info["color_node_types"]),
        "unsupported_color_nodes": list(image_info["unsupported_color_nodes"]),
        "occlusion": occlusion_factor.astype(np.float64),
        "occlusion_factor": occlusion_factor.astype(np.float64),
        "occlusion_vertices": occlusion_vertices.astype(np.float64),
        "scene_light_rgb": direct_shadowed_color.astype(np.float64),
        "scene_light_rgb_vertices": direct_shadowed_vertices.astype(np.float64),
        "scene_light_count": int(direct_shadowed_eval["light_count"]),
        "scene_light_stats": list(direct_shadowed_eval["per_light_stats"]),
        "shadow_factor": shadow_factor.astype(np.float64),
        "surface_distances": surface_info["surface_distances"].astype(np.float64),
        "bound_triangle_normals_world": surface_info["bound_triangle_normals_world"].astype(np.float64),
        "proxy_vertex_normals_world": proxy_vertex_normals.astype(np.float64),
        "proxy_vertex_normals_for_lighting": proxy_vertex_normals_for_lighting.astype(np.float64),
        "normal_smoothing": float(normal_smoothing),
        "pre_light_smoothing": float(pre_light_smoothing),
        "post_light_smoothing": float(post_light_smoothing),
        "transfer_style": str(resolved_transfer_style),
        "transfer_smoothness": float(transfer_smoothness),
        "transfer_smoothness_blend": float(resolved_transfer_blend),
        "proxy_interpolation_mode": f"Vertex Lighting + {resolved_transfer_style} Transfer",
        "cache_package_dir": paths["package_dir"],
        "cache_state_path": paths["bake_state_path"],
        "cache_metadata_path": paths["bake_metadata_path"],
    }


def build_proxy_hdri_relight(*args, **kwargs):
    return build_proxy_lighting_cache(*args, **kwargs)


def build_proxy_lighting_layers(*args, **kwargs):
    return build_proxy_lighting_cache(*args, **kwargs)


def save_original_color_state(
    mesh_obj,
    relight_cache_root="",
    overwrite_saved_state=False,
    proxy_binding_utils_path="",
):
    clear_legacy_relight_properties(mesh_obj)
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    state = proxy_utils.read_logical_gaussian_state(mesh_obj)
    logical_count = int(state["sh_coeffs"].shape[0])
    sh_degree = int(state["sh_coeffs"].shape[2] - 1)

    paths = get_relight_file_paths(mesh_obj, relight_cache_root=relight_cache_root, create=False)
    already_saved = os.path.exists(paths["metadata_path"]) and os.path.exists(paths["state_path"])
    if already_saved and not overwrite_saved_state:
        sync_stage_state_properties(mesh_obj, relight_cache_root=relight_cache_root)
        clear_legacy_relight_properties(mesh_obj)
        return {
            "already_saved": True,
            "paths": paths,
            "logical_splat_count": logical_count,
            "sh_degree": sh_degree,
        }

    paths = get_relight_file_paths(mesh_obj, relight_cache_root=relight_cache_root, create=True)
    os.makedirs(paths["package_dir"], exist_ok=True)
    np.savez(
        paths["state_path"],
        sh_coeffs=state["sh_coeffs"].astype(np.float32),
        logical_count=np.asarray([logical_count], dtype=np.int32),
        sh_degree=np.asarray([sh_degree], dtype=np.int32),
    )
    metadata = {
        "object_name": mesh_obj.name,
        "saved_at_utc": utc_now_iso(),
        "logical_splat_count": logical_count,
        "sh_degree": sh_degree,
        "note": "Saved by proxy_deferred_layers_utils.py",
    }
    write_json_file(paths["metadata_path"], metadata)
    sync_stage_state_properties(mesh_obj, relight_cache_root=relight_cache_root)
    clear_legacy_relight_properties(mesh_obj)
    return {
        "already_saved": False,
        "paths": paths,
        "logical_splat_count": logical_count,
        "sh_degree": sh_degree,
    }


def compose_proxy_deferred_relight_from_cache(
    cache,
    *,
    indirect_strength=1.0,
    direct_strength=1.0,
    occlusion_strength=0.7,
    shadow_strength=1.0,
    lighting_factor_mode="Tinted Luminance",
    factor_curve_mode="Reinhard",
    colorize_mix=0.2,
    max_color_tint=2.0,
    max_color_tint_mode="Perceived Brightness",
    ambient_floor=0.08,
    light_gain=0.85,
    light_power=0.75,
    max_light_factor=1.75,
):
    base_color = np.asarray(cache["base_color"], dtype=np.float64)
    indirect_color = np.asarray(cache["indirect_color"], dtype=np.float64)
    direct_color = np.asarray(cache["direct_color"], dtype=np.float64)
    occlusion_factor = np.asarray(cache["occlusion_factor"], dtype=np.float64).reshape(-1)
    shadow_factor = np.asarray(cache["shadow_factor"], dtype=np.float64).reshape(-1)

    occlusion_mix = np.clip(float(occlusion_strength), 0.0, 1.0)
    shadow_mix = np.clip(float(shadow_strength), 0.0, 1.0)
    indirect_scale = float(indirect_strength)
    direct_scale = float(direct_strength)

    occlusion_multiplier = (1.0 - occlusion_mix) + (occlusion_mix * occlusion_factor)
    shadow_multiplier = (1.0 - shadow_mix) + (shadow_mix * shadow_factor)

    indirect_base = indirect_color * occlusion_multiplier[:, None]
    direct_base = direct_color * shadow_multiplier[:, None]

    shaded_indirect = indirect_scale * indirect_base
    shaded_direct = direct_scale * direct_base
    diffuse_rgb = shaded_indirect + shaded_direct

    indirect_base_luminance = compute_color_luminance(indirect_base).reshape(-1)
    direct_base_luminance = compute_color_luminance(direct_base).reshape(-1)
    indirect_base_mean_luminance = max(float(np.mean(indirect_base_luminance)), EPSILON)
    direct_base_mean_luminance = max(float(np.mean(direct_base_luminance)), EPSILON)

    indirect_normalized_luminance = indirect_base_luminance / indirect_base_mean_luminance
    direct_normalized_luminance = direct_base_luminance / direct_base_mean_luminance
    source_strength_sum = max(abs(indirect_scale) + abs(direct_scale), 1.0)
    normalized_luminance = (
        (indirect_scale * indirect_normalized_luminance)
        + (direct_scale * direct_normalized_luminance)
    ) / source_strength_sum

    indirect_rgb_factor = indirect_base / indirect_base_mean_luminance
    direct_rgb_factor = direct_base / direct_base_mean_luminance
    normalized_rgb_factor = (
        (indirect_scale * indirect_rgb_factor)
        + (direct_scale * direct_rgb_factor)
    ) / source_strength_sum

    # This is a debug/reference baseline, while the actual brightness response
    # above is source-normalized so weaker cached sources remain artistically usable.
    reference_diffuse_rgb = indirect_base + direct_base
    reference_diffuse_luminance = compute_color_luminance(reference_diffuse_rgb).reshape(-1)
    reference_mean_luminance = max(float(np.mean(reference_diffuse_luminance)), EPSILON)
    diffuse_luminance = compute_color_luminance(diffuse_rgb).reshape(-1)
    mean_luminance = max(float(np.mean(diffuse_luminance)), EPSILON)
    powered_luminance = np.power(np.maximum(normalized_luminance, 0.0), float(light_power))

    curve_mode = str(factor_curve_mode).strip().lower().replace("_", " ")
    if curve_mode in ("", "reinhard", "soft", "soft clip"):
        curved_luminance = (2.0 * powered_luminance) / (1.0 + powered_luminance)
        resolved_curve_mode = "Reinhard"
    elif curve_mode in ("linear", "none"):
        curved_luminance = powered_luminance
        resolved_curve_mode = "Linear"
    else:
        raise ProxySurfaceRelightError(
            f"Unsupported factor_curve_mode '{factor_curve_mode}'. Use Reinhard or Linear."
        )

    scalar_factor = float(ambient_floor) + float(light_gain) * curved_luminance
    scalar_factor = np.clip(scalar_factor, 0.0, float(max_light_factor))

    raw_light_tint_color = build_unit_luminance_tint(
        diffuse_rgb,
        tint_strength=1.0,
        max_tint=max_color_tint,
        max_tint_mode=max_color_tint_mode,
    )
    resolved_max_color_tint_mode = resolve_max_color_tint_mode(max_color_tint_mode)

    mode = str(lighting_factor_mode).strip().lower().replace("_", " ")
    if mode in ("", "luminance", "luminance factor"):
        light_factor_rgb = np.repeat(scalar_factor[:, None], 3, axis=1)
        resolved_mode = "Luminance"
    elif mode in ("tinted luminance", "tint", "tinted", "chroma"):
        tint_mix = float(np.clip(colorize_mix, 0.0, 1.0))
        tint_mix_rgb = ((1.0 - tint_mix) * np.ones_like(raw_light_tint_color)) + (
            tint_mix * raw_light_tint_color
        )
        light_factor_rgb = scalar_factor[:, None] * tint_mix_rgb
        resolved_mode = "Tinted Luminance"
    elif mode in ("rgb", "rgb factor", "color"):
        rgb_factor = normalized_rgb_factor
        rgb_factor = np.power(np.maximum(rgb_factor, 0.0), float(light_power))
        rgb_factor = float(ambient_floor) + float(light_gain) * rgb_factor
        rgb_factor = np.clip(rgb_factor, 0.0, float(max_light_factor))
        mix = float(np.clip(colorize_mix, 0.0, 1.0))
        light_factor_rgb = ((1.0 - mix) * scalar_factor[:, None]) + (mix * rgb_factor)
        resolved_mode = "RGB"
    else:
        raise ProxySurfaceRelightError(
            f"Unsupported lighting_factor_mode '{lighting_factor_mode}'. Use Luminance, Tinted Luminance, or RGB."
        )

    relit_color = base_color * light_factor_rgb
    return {
        "base_color": base_color.astype(np.float64),
        "indirect_color_raw": indirect_color.astype(np.float64),
        "direct_color_raw": direct_color.astype(np.float64),
        "occlusion_factor": occlusion_factor.astype(np.float64),
        "shadow_factor": shadow_factor.astype(np.float64),
        "effective_occlusion_multiplier": occlusion_multiplier.astype(np.float64),
        "effective_shadow_multiplier": shadow_multiplier.astype(np.float64),
        "indirect_color_after_occlusion": indirect_base.astype(np.float64),
        "direct_color_after_shadow": direct_base.astype(np.float64),
        "shaded_indirect": shaded_indirect.astype(np.float64),
        "shaded_direct": shaded_direct.astype(np.float64),
        "indirect_base_luminance": indirect_base_luminance.astype(np.float64),
        "direct_base_luminance": direct_base_luminance.astype(np.float64),
        "indirect_base_mean_luminance": indirect_base_mean_luminance,
        "direct_base_mean_luminance": direct_base_mean_luminance,
        "indirect_normalized_luminance": indirect_normalized_luminance.astype(np.float64),
        "direct_normalized_luminance": direct_normalized_luminance.astype(np.float64),
        "source_strength_sum": source_strength_sum,
        "normalized_rgb_factor": normalized_rgb_factor.astype(np.float64),
        "reference_diffuse_rgb": reference_diffuse_rgb.astype(np.float64),
        "reference_diffuse_luminance": reference_diffuse_luminance.astype(np.float64),
        "reference_mean_luminance": reference_mean_luminance,
        "diffuse_rgb": diffuse_rgb.astype(np.float64),
        "diffuse_luminance": diffuse_luminance.astype(np.float64),
        "normalized_luminance": normalized_luminance.astype(np.float64),
        "powered_luminance": powered_luminance.astype(np.float64),
        "curved_luminance": curved_luminance.astype(np.float64),
        "mean_luminance": mean_luminance,
        "light_tint_color": raw_light_tint_color.astype(np.float64),
        "light_factor_scalar": scalar_factor.astype(np.float64),
        "light_factor_rgb": light_factor_rgb.astype(np.float64),
        "relit_color": relit_color.astype(np.float64),
        "resolved_factor_mode": resolved_mode,
        "resolved_curve_mode": resolved_curve_mode,
        "resolved_max_color_tint_mode": resolved_max_color_tint_mode,
    }


def commit_proxy_relight_color(
    mesh_obj,
    relit_color_attr_name=DEFAULT_RELIT_COLOR_ATTR,
    zero_rest_sh=True,
    clamp_relight_color=True,
    proxy_binding_utils_path="",
):
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    state = proxy_utils.read_logical_gaussian_state(mesh_obj)
    relit_color = read_logical_point_attribute(
        mesh_obj,
        relit_color_attr_name,
        proxy_binding_utils_path=proxy_binding_utils_path,
    )

    relit_color_before_clamp = np.asarray(relit_color, dtype=np.float64)
    clipped_low_pct = float(np.mean(relit_color_before_clamp < 0.0) * 100.0)
    clipped_high_pct = float(np.mean(relit_color_before_clamp > 1.0) * 100.0)
    if clamp_relight_color:
        relit_color = clamp_rgb(relit_color_before_clamp)
    else:
        relit_color = relit_color_before_clamp.copy()

    state["sh_coeffs"][:, :, 0] = (relit_color - 0.5) / SH_C0
    if zero_rest_sh and state["sh_coeffs"].shape[2] > 1:
        state["sh_coeffs"][:, :, 1:] = 0.0

    proxy_utils.write_logical_gaussian_state(mesh_obj, state)
    return {
        "logical_splat_count": int(len(relit_color)),
        "zero_rest_sh": bool(zero_rest_sh),
        "clamped": bool(clamp_relight_color),
        "clipped_low_pct": clipped_low_pct,
        "clipped_high_pct": clipped_high_pct,
        "relit_color_before_clamp": relit_color_before_clamp.astype(np.float64),
        "relit_color_after_clamp": relit_color.astype(np.float64),
        "new_dc_coeffs": state["sh_coeffs"][:, :, 0].astype(np.float64),
    }


def commit_composed_color_to_3dgs(
    mesh_obj,
    indirect_strength=1.0,
    direct_strength=1.0,
    occlusion_strength=0.7,
    shadow_strength=1.0,
    lighting_factor_mode="Tinted Luminance",
    factor_curve_mode="Reinhard",
    colorize_mix=0.2,
    max_color_tint=2.0,
    max_color_tint_mode="Perceived Brightness",
    ambient_floor=0.08,
    light_gain=0.85,
    light_power=0.75,
    max_light_factor=1.75,
    export_mode="Compatible",
    directionality_strength=0.25,
    clamp_relight_color=True,
    relight_cache_root="",
    proxy_binding_utils_path="",
):
    clear_legacy_relight_properties(mesh_obj)
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    state = proxy_utils.read_logical_gaussian_state(mesh_obj)
    bake_paths, bake_metadata, cache = load_baked_lighting_cache(
        mesh_obj,
        relight_cache_root=relight_cache_root,
    )
    composed = compose_proxy_deferred_relight_from_cache(
        cache,
        indirect_strength=indirect_strength,
        direct_strength=direct_strength,
        occlusion_strength=occlusion_strength,
        shadow_strength=shadow_strength,
        lighting_factor_mode=lighting_factor_mode,
        factor_curve_mode=factor_curve_mode,
        colorize_mix=colorize_mix,
        max_color_tint=max_color_tint,
        max_color_tint_mode=max_color_tint_mode,
        ambient_floor=ambient_floor,
        light_gain=light_gain,
        light_power=light_power,
        max_light_factor=max_light_factor,
    )

    relit_color_before_clamp = np.asarray(composed["relit_color"], dtype=np.float64)
    clipped_low_pct = float(np.mean(relit_color_before_clamp < 0.0) * 100.0)
    clipped_high_pct = float(np.mean(relit_color_before_clamp > 1.0) * 100.0)
    if clamp_relight_color:
        relit_color = clamp_rgb(relit_color_before_clamp)
    else:
        relit_color = relit_color_before_clamp.copy()

    state["sh_coeffs"][:, :, 0] = (relit_color - 0.5) / SH_C0

    mode = str(export_mode).strip().lower().replace("_", " ")
    mode_compact = "".join(ch for ch in mode if ch.isalnum())
    resolved_mode = "Flatten SH"
    applied_directionality_strength = 0.0
    if state["sh_coeffs"].shape[2] > 1:
        if mode in ("", "compatible", "fdc only", "f_dc only", "flat") or mode_compact in (
            "flatten",
            "flattensh",
            "zerosh",
            "zerofrest",
            "zerofrestsh",
            "fdconly",
            "fdconlyzerofrest",
            "fdconlyzerofrestsh",
        ):
            state["sh_coeffs"][:, :, 1:] = 0.0
            resolved_mode = "Flatten SH"
            applied_directionality_strength = 0.0
        elif mode in ("keep current directionality", "preserve current directionality", "keep current f rest", "keep current f_rest") or mode_compact in (
            "fdckeepcurrentfrest",
            "fdckeepcurrentfrestsh",
            "keepcurrentfrest",
            "keepcurrentfrestsh",
        ):
            resolved_mode = "Keep Current SH"
            applied_directionality_strength = 1.0
        elif mode_compact in (
            "preserveoriginalsh",
            "restoreoriginalsh",
            "useoriginalsh",
            "originalsh",
            "preservesavedsh",
            "restoresavedsh",
        ):
            _, _, saved_state = load_saved_color_state(
                mesh_obj,
                relight_cache_root=relight_cache_root,
            )
            if saved_state["sh_coeffs"].shape != state["sh_coeffs"].shape:
                raise ProxySurfaceRelightError(
                    f"Saved original state for '{mesh_obj.name}' does not match the current SH layout."
                )
            state["sh_coeffs"][:, :, 1:] = np.asarray(
                saved_state["sh_coeffs"][:, :, 1:],
                dtype=np.float64,
            )
            resolved_mode = "Preserve Original SH"
            applied_directionality_strength = 1.0
        elif mode in ("dampen saved original directionality", "saved original directionality", "damped original", "enhanced") or mode_compact in (
            "dampenoriginalsh",
            "dampensavedsh",
            "dampensavedoriginalsh",
            "fdcsavedoriginalfrestdamped",
            "fdcsavedoriginalfrestshdamped",
            "savedoriginalfrestdamped",
            "savedoriginalfrestshdamped",
        ):
            _, _, saved_state = load_saved_color_state(
                mesh_obj,
                relight_cache_root=relight_cache_root,
            )
            if saved_state["sh_coeffs"].shape != state["sh_coeffs"].shape:
                raise ProxySurfaceRelightError(
                    f"Saved original state for '{mesh_obj.name}' does not match the current SH layout."
                )
            strength = float(np.clip(directionality_strength, 0.0, 1.0))
            state["sh_coeffs"][:, :, 1:] = (
                np.asarray(saved_state["sh_coeffs"][:, :, 1:], dtype=np.float64) * strength
            )
            resolved_mode = "Dampen Original SH"
            applied_directionality_strength = strength
        else:
            raise ProxySurfaceRelightError(
                f"Unsupported export_mode '{export_mode}'. "
                f"Use Flatten SH, Preserve Original SH, or Dampen Original SH."
            )

    proxy_utils.write_logical_gaussian_state(mesh_obj, state)
    sync_stage_state_properties(mesh_obj, relight_cache_root=relight_cache_root)
    return {
        "logical_splat_count": int(len(relit_color)),
        "clamped": bool(clamp_relight_color),
        "clipped_low_pct": clipped_low_pct,
        "clipped_high_pct": clipped_high_pct,
        "relit_color_before_clamp": relit_color_before_clamp.astype(np.float64),
        "relit_color_after_clamp": relit_color.astype(np.float64),
        "new_dc_coeffs": state["sh_coeffs"][:, :, 0].astype(np.float64),
        "new_rest_coeffs": state["sh_coeffs"][:, :, 1:].astype(np.float64) if state["sh_coeffs"].shape[2] > 1 else np.zeros((len(relit_color), 3, 0), dtype=np.float64),
        "resolved_export_mode": resolved_mode,
        "directionality_strength": float(applied_directionality_strength),
        "indirect_strength": float(indirect_strength),
        "direct_strength": float(direct_strength),
        "occlusion_strength": float(np.clip(occlusion_strength, 0.0, 1.0)),
        "shadow_strength": float(np.clip(shadow_strength, 0.0, 1.0)),
        "factor_mode": str(composed["resolved_factor_mode"]),
        "factor_curve_mode": str(composed["resolved_curve_mode"]),
        "max_color_tint_mode": str(composed["resolved_max_color_tint_mode"]),
        "base_color": composed["base_color"],
        "indirect_color_raw": composed["indirect_color_raw"],
        "direct_color_raw": composed["direct_color_raw"],
        "occlusion_factor": composed["occlusion_factor"],
        "shadow_factor": composed["shadow_factor"],
        "effective_occlusion_multiplier": composed["effective_occlusion_multiplier"],
        "effective_shadow_multiplier": composed["effective_shadow_multiplier"],
        "indirect_color_after_occlusion": composed["indirect_color_after_occlusion"],
        "direct_color_after_shadow": composed["direct_color_after_shadow"],
        "shaded_indirect": composed["shaded_indirect"],
        "shaded_direct": composed["shaded_direct"],
        "indirect_base_luminance": composed["indirect_base_luminance"],
        "direct_base_luminance": composed["direct_base_luminance"],
        "indirect_base_mean_luminance": float(composed["indirect_base_mean_luminance"]),
        "direct_base_mean_luminance": float(composed["direct_base_mean_luminance"]),
        "indirect_normalized_luminance": composed["indirect_normalized_luminance"],
        "direct_normalized_luminance": composed["direct_normalized_luminance"],
        "source_strength_sum": float(composed["source_strength_sum"]),
        "normalized_rgb_factor": composed["normalized_rgb_factor"],
        "diffuse_rgb": composed["diffuse_rgb"],
        "diffuse_luminance": composed["diffuse_luminance"],
        "normalized_luminance": composed["normalized_luminance"],
        "powered_luminance": composed["powered_luminance"],
        "curved_luminance": composed["curved_luminance"],
        "mean_luminance": float(composed["mean_luminance"]),
        "reference_diffuse_rgb": composed["reference_diffuse_rgb"],
        "reference_diffuse_luminance": composed["reference_diffuse_luminance"],
        "reference_mean_luminance": float(composed["reference_mean_luminance"]),
        "light_tint_color": composed["light_tint_color"],
        "light_factor_scalar": composed["light_factor_scalar"],
        "light_factor_rgb": composed["light_factor_rgb"],
        "bake_package_dir": bake_paths["package_dir"],
        "bake_metadata": dict(bake_metadata),
    }


def restore_original_color_state(
    mesh_obj,
    relight_cache_root="",
    clear_temp_attributes=True,
    base_color_attr_name=DEFAULT_BASE_COLOR_ATTR,
    light_factor_attr_name=DEFAULT_LIGHT_FACTOR_ATTR,
    relit_color_attr_name=DEFAULT_RELIT_COLOR_ATTR,
    clear_saved_state=False,
    proxy_binding_utils_path="",
):
    clear_legacy_relight_properties(mesh_obj)
    proxy_utils = load_proxy_binding_utils(proxy_binding_utils_path)
    _, _, saved_state = load_saved_color_state(mesh_obj, relight_cache_root=relight_cache_root)
    current_state = proxy_utils.read_logical_gaussian_state(mesh_obj)
    if current_state["sh_coeffs"].shape != saved_state["sh_coeffs"].shape:
        raise ProxySurfaceRelightError(
            f"Saved proxy relight color state for '{mesh_obj.name}' no longer matches the current mesh."
        )

    current_state["sh_coeffs"] = saved_state["sh_coeffs"].astype(np.float64)
    proxy_utils.write_logical_gaussian_state(mesh_obj, current_state)

    removed_attributes = []
    if clear_temp_attributes:
        removed_attributes = clear_temp_attributes_fn(
            mesh_obj,
            attr_names=[
                base_color_attr_name,
                DEFAULT_DIRECT_COLOR_ATTR,
                DEFAULT_INDIRECT_COLOR_ATTR,
                DEFAULT_SHADOW_FACTOR_ATTR,
                DEFAULT_OCCLUSION_FACTOR_ATTR,
                DEFAULT_LIGHT_TINT_ATTR,
                light_factor_attr_name,
                relit_color_attr_name,
            ],
        )
        clear_layer_state_properties(mesh_obj)

    removed_files = []
    if clear_saved_state:
        removed_files = clear_saved_color_state(
            mesh_obj,
            relight_cache_root=relight_cache_root,
            keep_package_path=False,
        )

    sync_stage_state_properties(mesh_obj, relight_cache_root=relight_cache_root)
    clear_legacy_relight_properties(mesh_obj)

    return {
        "logical_splat_count": int(saved_state["logical_count"]),
        "sh_degree": int(saved_state["sh_degree"]),
        "removed_attributes": removed_attributes,
        "removed_files": removed_files,
    }


def clear_temp_attributes_fn(mesh_obj, attr_names=None):
    return clear_temp_attributes(mesh_obj, attr_names=attr_names)
