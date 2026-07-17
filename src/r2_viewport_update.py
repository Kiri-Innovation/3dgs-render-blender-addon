import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .c2_refresh_all import sna_c2_refresh_all_4D367
from .clean_up_scene_5f1f1 import sna_clean_up_scene_5F1F1
from .rig_5_apply_baked_cache import sna_rig_5_apply_baked_cache_5656F
from .shader_system import sna_shader_system_A4AED
from .texture_creation import sna_texture_creation_FD1B2
from .viewport_render import sna_viewport_render_A3941

__package__ = __package__.rsplit('.', 1)[0]


def sna_r2_viewport_update_BA246():
    if bpy.context.scene.sna_dgs_scene_properties.r2_render_rig_cache_mode == "Enabled Baked":
        sna_rig_5_apply_baked_cache_5656F('All Bound', None)
        sna_clean_up_scene_5F1F1(False)
        sna_shader_system_A4AED()
        sna_texture_creation_FD1B2()
        sna_viewport_render_A3941(bpy.context.scene.sna_dgs_scene_properties.r2_sh_degree, bpy.context.scene.sna_dgs_scene_properties.r2_sort_threshold)
    else:
        pass
    sna_c2_refresh_all_4D367((not bpy.context.scene.sna_dgs_scene_properties.r2_selected), bpy.context.scene.sna_dgs_scene_properties.r2_transforms, True)
    sna_shader_system_A4AED()
    sna_texture_creation_FD1B2()
    sna_viewport_render_A3941(bpy.context.scene.sna_dgs_scene_properties.r2_sh_degree, bpy.context.scene.sna_dgs_scene_properties.r2_sort_threshold)
