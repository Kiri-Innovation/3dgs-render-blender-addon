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
from mathutils import Matrix
import re
from mathutils import Vector
from bpy.app.handlers import persistent
from typing import Optional

from .. import load_preview_icon

__package__ = __package__.rsplit('.', 1)[0]


def set_modifier_socket(modifier, key, value):
    """Set modifier[key] = value, swallowing the TypeError Blender 5.2 raises for
    Menu/Material/Image/Collection sockets (e.g. KIRI_3DGS_Render_GN's Socket_50,
    Socket_61). Works fine on 5.1.2 — silently no-ops on 5.2 so setup continues
    instead of aborting; the socket just keeps its node-group default."""
    try:
        modifier[key] = value
    except TypeError:
        pass


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
