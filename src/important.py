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
