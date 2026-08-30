import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_rig_cache_frames_993DF(layout_function, enabled):
    col_EF5B6 = layout_function.column(heading='', align=True)
    col_EF5B6.enabled = enabled
    col_EF5B6.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_bake_start_frame', text='Start Frame', icon_value=0, emboss=True)
    col_EF5B6.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_bake_end_frame', text='End Frame', icon_value=0, emboss=True)
    col_EF5B6.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_bake_frame_step', text='Frame Step', icon_value=0, emboss=True)
