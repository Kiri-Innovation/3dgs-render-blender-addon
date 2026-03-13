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


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False
