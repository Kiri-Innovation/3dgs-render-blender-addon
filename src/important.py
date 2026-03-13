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

# _icons = None
#
# def load_preview_icon(path):
#     global _icons
#     if not path in _icons:
#         if os.path.exists(path):
#             _icons.load(path, path, "IMAGE")
#         else:
#             return 0
#     return _icons[path].icon_id

def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False
