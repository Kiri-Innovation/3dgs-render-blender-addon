import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

import bpy
import bpy.utils.previews
import webbrowser
import os
import math
from bpy_extras.io_utils import ImportHelper, ExportHelper
import importlib.util
import types
import subprocess
import sys
import platform
import gpu.state
import numpy as np
import time
import gpu.types
import uuid
from mathutils import Matrix
import re
from mathutils import Vector
from bpy.app.handlers import persistent
from typing import Optional

from .. import load_preview_icon

__package__ = __package__.rsplit('.', 1)[0]


def _kiri_geometry_nodes_input(modifier, key):
    """Return a Geometry Nodes interface input on Blender 5.2+."""
    inputs = getattr(getattr(modifier, "properties", None), "inputs", None)
    if inputs is None:
        raise KeyError(key)
    try:
        return getattr(inputs, key)
    except AttributeError as exc:
        raise KeyError(key) from exc


def _kiri_geometry_nodes_getitem(modifier, key):
    socket = _kiri_geometry_nodes_input(modifier, key)
    value = socket.value
    prop = socket.bl_rna.properties.get("value")
    if prop is not None and prop.type == "ENUM":
        for item in prop.enum_items:
            if item.identifier == value:
                return item.value
    return value


def _kiri_geometry_nodes_setitem(modifier, key, value):
    socket = _kiri_geometry_nodes_input(modifier, key)
    prop = socket.bl_rna.properties.get("value")
    if prop is not None and prop.type == "ENUM" and isinstance(value, int):
        for item in prop.enum_items:
            if item.value == value:
                value = item.identifier
                break
    socket.value = value


def install_geometry_nodes_52_compat():
    """Preserve the generated pre-5.2 ``modifier['Socket_*']`` API.

    Blender 5.2 exposes Geometry Nodes inputs through
    ``modifier.properties.inputs.Socket_*.value``. The add-on contains many
    generated legacy get/set sites, so one narrowly scoped compatibility shim
    keeps them working without changing behavior on Blender 5.1.
    """
    if bpy.app.version < (5, 2, 0):
        return
    modifier_type = bpy.types.NodesModifier
    if not getattr(modifier_type, "_kiri_52_compat_installed", False):
        modifier_type.__getitem__ = _kiri_geometry_nodes_getitem
        modifier_type.__setitem__ = _kiri_geometry_nodes_setitem
        modifier_type._kiri_52_compat_installed = True


install_geometry_nodes_52_compat()


def set_modifier_socket(modifier, key, value):
    """Set a Geometry Nodes input using the API for the active Blender version."""
    if bpy.app.version >= (5, 2, 0):
        _kiri_geometry_nodes_setitem(modifier, key, value)
    else:
        modifier[key] = value


def get_modifier_socket(modifier, key):
    """Read a Geometry Nodes input using the API for the active Blender version."""
    if bpy.app.version >= (5, 2, 0):
        return _kiri_geometry_nodes_getitem(modifier, key)
    return modifier[key]


def kiri_gaussian_viewport_visible(obj, context=None):
    """Return Blender's effective viewport visibility for a Gaussian proxy.

    This includes the Outliner eye and monitor controls, hidden collections,
    excluded view-layer collections and local-view isolation.
    """
    if obj is None:
        return False
    context = context or bpy.context
    scene = getattr(context, "scene", None)
    view_layer = getattr(context, "view_layer", None)
    if scene is not None and obj.name not in scene.objects:
        return False
    if view_layer is not None and obj.name not in view_layer.objects:
        return False
    viewport = getattr(context, "space_data", None)
    if not isinstance(viewport, bpy.types.SpaceView3D):
        viewport = None
    try:
        return bool(obj.visible_get(view_layer=view_layer, viewport=viewport))
    except (TypeError, RuntimeError):
        try:
            return bool(obj.visible_get())
        except RuntimeError:
            return not bool(obj.hide_viewport or obj.hide_get())


def _kiri_collection_has_render_path(root, target):
    """Return whether target has a non-hidden collection path from root."""
    if getattr(root, "hide_render", False):
        return False
    if root == target:
        return True
    return any(_kiri_collection_has_render_path(child, target) for child in root.children)


def kiri_gaussian_render_visible(obj, context=None):
    """Return offline-render visibility for a Gaussian proxy.

    The Outliner camera control (``hide_render``), render-disabled collections
    and view-layer exclusion are respected. Viewport-only eye controls are
    deliberately ignored, matching normal Blender render behaviour.
    """
    if obj is None:
        return False
    context = context or bpy.context
    scene = getattr(context, "scene", None)
    view_layer = getattr(context, "view_layer", None)
    if scene is not None and obj.name not in scene.objects:
        return False
    if view_layer is not None and obj.name not in view_layer.objects:
        return False
    if bool(obj.hide_render):
        return False
    if scene is not None and obj.users_collection:
        if not any(_kiri_collection_has_render_path(scene.collection, collection) for collection in obj.users_collection):
            return False
    return True


def kiri_gaussian_is_instance(obj):
    """Return whether a Gaussian proxy is an independently placed duplicate."""
    return bool(obj and obj.get("kiri_gaussian_instance", False))


def _kiri_gaussian_source_key(obj):
    """Return a stable key used to find another proxy with the same splat data."""
    source_uuid = str(obj.get("source_mesh_uuid", "")).strip()
    if source_uuid:
        return ("MESH", source_uuid)
    ply_filepath = str(obj.get("ply_filepath", "")).strip()
    if ply_filepath:
        try:
            ply_filepath = os.path.normcase(os.path.abspath(bpy.path.abspath(ply_filepath)))
        except Exception:
            ply_filepath = os.path.normcase(ply_filepath)
        return ("PLY", ply_filepath)
    return None


def _kiri_valid_gaussian_array(value, gaussian_count):
    """Return a (count, 59) float32 view, or None for incomplete/corrupt data."""
    try:
        gaussian_count = int(gaussian_count)
        if gaussian_count <= 0 or value is None:
            return None
        if isinstance(value, np.ndarray):
            if value.dtype == np.float32 and value.shape == (gaussian_count, 59):
                return value
            gaussian_data = np.asarray(value, dtype=np.float32)
        elif isinstance(value, (bytes, bytearray, memoryview)):
            gaussian_data = np.frombuffer(value, dtype=np.float32)
        else:
            gaussian_data = np.asarray(value, dtype=np.float32)
        if gaussian_data.size != gaussian_count * 59:
            return None
        return gaussian_data.reshape(gaussian_count, 59)
    except (TypeError, ValueError, BufferError):
        return None


def _kiri_cache_signature(cache):
    signature = []
    for obj_name, entry in cache.items():
        obj = entry.get("object")
        try:
            pointer = obj.as_pointer() if obj is not None else 0
        except ReferenceError:
            pointer = 0
        signature.append((obj_name, pointer, int(entry.get("gaussian_count", 0)), id(entry.get("gaussian_data"))))
    return tuple(signature)


def kiri_sync_gaussian_object_cache(context=None):
    """Reconcile Blender Gaussian proxies with the renderer's runtime cache.

    Blender duplicates object custom properties but the add-on's cache is a
    separate Python dictionary keyed by object name. This function discovers
    new duplicates, renamed proxies and deletions while preserving shared CPU
    data where possible. Duplicates receive their own cache/metadata entry and
    therefore their own Blender transform in viewport and offline renders.

    Returns True only when GPU textures/metadata need to be rebuilt.
    """
    context = context or bpy.context
    scene = getattr(context, "scene", None)
    object_source = scene.objects if scene is not None else bpy.data.objects
    gaussian_objects = [obj for obj in object_source if obj.get("is_gaussian_splat", False)]

    existing_cache = getattr(bpy, "gaussian_object_cache", None)
    if not isinstance(existing_cache, dict):
        existing_cache = {}

    existing_by_pointer = {}
    for entry in existing_cache.values():
        obj = entry.get("object")
        try:
            if obj is not None:
                existing_by_pointer[obj.as_pointer()] = entry
        except ReferenceError:
            pass

    # Process already-cached objects first so a copied proxy UUID always keeps
    # the original proxy as its owner.
    identity_order = sorted(
        gaussian_objects,
        key=lambda obj: 0 if obj.as_pointer() in existing_by_pointer else 1,
    )
    proxy_id_owner = {}
    source_owner = {}
    identity_changed = False
    for obj in identity_order:
        proxy_uuid = str(obj.get("kiri_gaussian_proxy_uuid", "")).strip()
        duplicate_of = None
        if proxy_uuid and proxy_uuid in proxy_id_owner and proxy_id_owner[proxy_uuid] != obj:
            duplicate_of = proxy_id_owner[proxy_uuid]
        elif not proxy_uuid:
            source_key = _kiri_gaussian_source_key(obj)
            if source_key and source_key in source_owner:
                duplicate_of = source_owner[source_key]
            proxy_uuid = str(uuid.uuid4())
            try:
                obj["kiri_gaussian_proxy_uuid"] = proxy_uuid
            except (TypeError, RuntimeError):
                pass

        if duplicate_of is not None:
            original_uuid = str(duplicate_of.get("kiri_gaussian_proxy_uuid", "")).strip()
            new_uuid = str(uuid.uuid4())
            try:
                obj["kiri_gaussian_proxy_uuid"] = new_uuid
                obj["kiri_gaussian_instance"] = True
                if original_uuid:
                    obj["kiri_gaussian_instance_source_uuid"] = original_uuid
                proxy_uuid = new_uuid
                identity_changed = True
            except (TypeError, RuntimeError):
                pass

        if proxy_uuid:
            proxy_id_owner[proxy_uuid] = obj
        source_key = _kiri_gaussian_source_key(obj)
        if source_key and source_key not in source_owner:
            source_owner[source_key] = obj

    new_cache = {}
    data_by_proxy_uuid = {}
    data_by_source = {}

    # Seed fallbacks with healthy runtime entries. This is important after a
    # saved .blend truncates a large byte ID property: a duplicate can still
    # share the source proxy's already-recovered NumPy data.
    for entry in existing_cache.values():
        obj = entry.get("object")
        if obj is None:
            continue
        try:
            gaussian_count = int(entry.get("gaussian_count", obj.get("gaussian_count", 0)))
        except ReferenceError:
            continue
        gaussian_data = _kiri_valid_gaussian_array(entry.get("gaussian_data"), gaussian_count)
        if gaussian_data is None:
            continue
        try:
            proxy_uuid = str(obj.get("kiri_gaussian_proxy_uuid", "")).strip()
        except ReferenceError:
            continue
        if proxy_uuid:
            data_by_proxy_uuid[(proxy_uuid, gaussian_count)] = gaussian_data
        source_key = _kiri_gaussian_source_key(obj)
        if source_key:
            data_by_source[(source_key, gaussian_count)] = gaussian_data

    for obj in gaussian_objects:
        try:
            existing_entry = existing_by_pointer.get(obj.as_pointer())
        except ReferenceError:
            existing_entry = None
        gaussian_count = int(obj.get("gaussian_count", 0))
        if gaussian_count <= 0 and existing_entry is not None:
            gaussian_count = int(existing_entry.get("gaussian_count", 0))
        if gaussian_count <= 0:
            continue
        gaussian_data = None
        if existing_entry is not None:
            gaussian_data = _kiri_valid_gaussian_array(existing_entry.get("gaussian_data"), gaussian_count)
        if gaussian_data is None:
            gaussian_data = _kiri_valid_gaussian_array(obj.get("gaussian_data"), gaussian_count)
        if gaussian_data is None:
            instance_source_uuid = str(obj.get("kiri_gaussian_instance_source_uuid", "")).strip()
            if instance_source_uuid:
                gaussian_data = data_by_proxy_uuid.get((instance_source_uuid, gaussian_count))
        if gaussian_data is None:
            source_key = _kiri_gaussian_source_key(obj)
            if source_key:
                gaussian_data = data_by_source.get((source_key, gaussian_count))
        if gaussian_data is None:
            print(f"KIRI 3DGS: Could not add '{obj.name}' to the render cache (Gaussian data unavailable)")
            continue

        ply_filepath = obj.get("ply_filepath", "")
        source_info = ""
        if obj.get("source_mesh_uuid"):
            source_info = f"Mesh:{obj.get('source_mesh_name', 'Unknown')}"
        elif ply_filepath:
            source_info = f"PLY:{os.path.basename(str(ply_filepath))}"
        entry = {
            "gaussian_data": gaussian_data,
            "gaussian_count": gaussian_count,
            "sh_degree": int(obj.get("sh_degree", 48)),
            "object": obj,
            "ply_filepath": ply_filepath,
            "source_info": source_info,
        }
        if obj.get("source_mesh_uuid"):
            entry["source_mesh_uuid"] = obj.get("source_mesh_uuid")
            entry["source_mesh_name"] = obj.get("source_mesh_name", "")
        new_cache[obj.name] = entry

        proxy_uuid = str(obj.get("kiri_gaussian_proxy_uuid", "")).strip()
        if proxy_uuid:
            data_by_proxy_uuid[(proxy_uuid, gaussian_count)] = gaussian_data
        source_key = _kiri_gaussian_source_key(obj)
        if source_key:
            data_by_source[(source_key, gaussian_count)] = gaussian_data

    changed = identity_changed or _kiri_cache_signature(existing_cache) != _kiri_cache_signature(new_cache)
    if changed or not hasattr(bpy, "gaussian_object_cache"):
        bpy.gaussian_object_cache = new_cache
    if changed:
        bpy.gaussian_global_needs_update = True
        bpy.gaussian_needs_depth_sort = True
        print(
            f"KIRI 3DGS: Synced render cache to {len(new_cache)} proxy object(s), "
            f"{sum(entry['gaussian_count'] for entry in new_cache.values()):,} rendered splats"
        )
    return changed


def kiri_build_gaussian_metadata(all_object_metadata, for_render=False, context=None):
    """Pack transforms and context-appropriate visibility for the GPU shader."""
    num_objects = len(all_object_metadata)
    floats_per_object = 15
    total_metadata_floats = num_objects * floats_per_object
    max_texture_dim = 16384
    metadata_width = min(max_texture_dim, total_metadata_floats)
    metadata_height = (total_metadata_floats + metadata_width - 1) // metadata_width
    expected_size = metadata_width * metadata_height
    metadata_data = np.zeros(expected_size, dtype=np.float32)
    visibility_function = kiri_gaussian_render_visible if for_render else kiri_gaussian_viewport_visible
    for obj_idx, obj_meta in enumerate(all_object_metadata):
        base_idx = obj_idx * floats_per_object
        uint32_start_idx = np.uint32(obj_meta['start_idx'])
        metadata_data[base_idx + 0] = uint32_start_idx.view(np.float32)
        metadata_data[base_idx + 1] = float(obj_meta['gaussian_count'])
        metadata_data[base_idx + 2] = 1.0 if visibility_function(obj_meta['object'], context) else 0.0
        transform = obj_meta['object'].matrix_world
        matrix_idx = 0
        for col in range(4):
            for row in range(3):
                metadata_data[base_idx + 3 + matrix_idx] = transform[row][col]
                matrix_idx += 1
    return metadata_data, metadata_width, metadata_height


def kiri_geometry_nodes_ui_target(owner, property_name):
    """Resolve generated legacy socket paths for Blender 5.2 UI drawing."""
    if bpy.app.version < (5, 2, 0) or not isinstance(owner, bpy.types.NodesModifier):
        return owner, property_name
    match = re.fullmatch(r'\["(Socket_\d+)"\]', property_name)
    if not match:
        return owner, property_name
    return _kiri_geometry_nodes_input(owner, match.group(1)), "value"


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


def load_export_transform_utils():
    cached = sys.modules.get("export_transform_utils")
    if cached is not None and getattr(cached, "__file__", None) and os.path.exists(cached.__file__):
        return cached
    module_path = os.path.join(os.path.dirname(__file__), "assets", "export_transform_utils.py")
    spec = importlib.util.spec_from_file_location("export_transform_utils", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules["export_transform_utils"] = module
    return module


def register_proxy_binding_gpu_module(proxy_utils_module):
    """Load proxy_binding_gpu.py from next to proxy_binding_utils.py and register it
    under sys.modules['proxy_binding_gpu'] so rotate_sh_coeffs can find it for the
    GPU fast path. Best-effort — silently no-op on any failure (CPU path still works)."""
    try:
        utils_file = getattr(proxy_utils_module, "__file__", None)
        if not utils_file:
            return None
        gpu_path = os.path.join(os.path.dirname(utils_file), "proxy_binding_gpu.py")
        if not os.path.exists(gpu_path):
            return None
        cached = sys.modules.get("proxy_binding_gpu")
        if cached is not None and getattr(cached, "__file__", None) == gpu_path:
            return cached
        spec = importlib.util.spec_from_file_location("proxy_binding_gpu", gpu_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules["proxy_binding_gpu"] = module
        return module
    except Exception:
        return None


def apply_gpu_sh_addon_pref():
    """Read the addon preference and update bpy._proxy_sh_gpu_state['enabled']
    so proxy_binding_utils.rotate_sh_coeffs honors the user toggle."""
    try:
        prefs = bpy.context.preferences.addons[__package__].preferences
        enabled = bool(getattr(prefs, "sna_use_gpu_sh_rotation", True))
    except Exception:
        return
    if not hasattr(bpy, "_proxy_sh_gpu_state"):
        bpy._proxy_sh_gpu_state = {"sticky_cpu": False, "enabled": True, "gpu_module": None}
    bpy._proxy_sh_gpu_state["enabled"] = enabled
