import bpy
from .important import *

class SNA_OT_Dgs_Render_Advanced_Render_Ba196(bpy.types.Operator):
    bl_idname = "sna.dgs_render_advanced_render_ba196"
    bl_label = "3DGS Render: Advanced Render"
    bl_description = "Renders the proxy Gaussian objects with current settings"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_dgs_scene_properties.r2_comp:
            temp_render_path_0_c714f = sna_render_temp_scene_913CD(bpy.context.scene.sna_dgs_scene_properties.r2_animation, bpy.context.scene.frame_step)
            bpy.context.scene.sna_dgs_scene_properties.r2_temp_path = temp_render_path_0_c714f
        sna_render_comp_0DAEE(bpy.context.scene.sna_dgs_scene_properties.r2_animation, bpy.context.scene.sna_dgs_scene_properties.r2_color, bpy.context.scene.sna_dgs_scene_properties.r2_depth, bpy.context.scene.sna_dgs_scene_properties.r2_comp, bpy.context.scene.sna_dgs_scene_properties.r2_transforms, True, bpy.context.scene.frame_step, bpy.context.scene.sna_dgs_scene_properties.r2_temp_path)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
