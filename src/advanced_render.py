import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .render_comp import sna_render_comp_0DAEE
from .render_temp_scene import sna_render_temp_scene_913CD

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Advanced_Render_147Af(bpy.types.Operator):
    bl_idname = "sna.dgs_render_advanced_render_147af"
    bl_label = "3DGS Render: Advanced Render"
    bl_description = "Renders the proxy Gaussian objects with current settings"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        exec('import os')
        if bpy.context.scene.sna_dgs_scene_properties.r2_comp:
            temp_render_path_0_03f89 = sna_render_temp_scene_913CD(bpy.context.scene.sna_dgs_scene_properties.r2_animation, bpy.context.scene.frame_step)
        sna_render_comp_0DAEE(bpy.context.scene.sna_dgs_scene_properties.r2_animation, bpy.context.scene.sna_dgs_scene_properties.r2_color, bpy.context.scene.sna_dgs_scene_properties.r2_depth, bpy.context.scene.sna_dgs_scene_properties.r2_comp, bpy.context.scene.sna_dgs_scene_properties.r2_transforms, True, bpy.context.scene.frame_step, bpy.context.scene.sna_dgs_scene_properties.r2_delete_temp_files, bpy.context.scene.sna_dgs_scene_properties.r2_render_rig_cache_mode, bpy.context.scene.sna_dgs_scene_properties.r2_sh_degree)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
