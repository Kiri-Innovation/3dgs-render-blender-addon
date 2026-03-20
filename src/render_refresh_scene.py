import bpy
from .shader_system import *
from .refresh_create_paint_attribute import *
from .sna_texture_creation import *
from .sna_viewport_render import *

class SNA_OT_Dgs_Render_Refresh_Scene_C0B35(bpy.types.Operator):
    bl_idname = "sna.dgs_render_refresh_scene_c0b35"
    bl_label = "3DGS Render: Refresh Scene"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Single Time'):
            pass
        else:
            bpy.context.scene.frame_current = bpy.context.scene.frame_start
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop = (bpy.context.scene.sna_dgs_scene_properties.r2_update_type == 'Single Time')

        def delayed_09B50():
            for i_75739 in range(len(bpy.context.scene.objects)):
                if (property_exists("bpy.context.scene.objects[i_75739].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_75739].modifiers):
                    bpy.context.scene.objects[i_75739].hide_viewport = False
            sna_c2_refresh_all_4D367((not bpy.context.scene.sna_dgs_scene_properties.r2_selected), bpy.context.scene.sna_dgs_scene_properties.r2_transforms, True)
            sna_shader_system_A4AED()
            sna_texture_creation_FD1B2()
            sna_viewport_render_A3941()
            for i_07D59 in range(len(bpy.context.scene.objects)):
                if ((property_exists("bpy.context.scene.objects[i_07D59].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_07D59].modifiers) and '3DGS_Mesh_Type' in bpy.context.scene.objects[i_07D59]):
                    if (bpy.context.scene.objects[i_07D59]['3DGS_Mesh_Type'] == 'face'):
                        bpy.context.scene.objects[i_07D59].hide_viewport = True
            if bpy.context.scene.sna_dgs_scene_properties.r2_interval_stop:
                return None
            return bpy.context.scene.sna_dgs_scene_properties.r2_interval
        bpy.app.timers.register(delayed_09B50, first_interval=0.0)
        for i_BD2F9 in range(len(bpy.context.scene.objects)):
            if (property_exists("bpy.context.scene.objects[i_BD2F9].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_BD2F9].modifiers):
                bpy.context.scene.objects[i_BD2F9].hide_viewport = False
        sna_c2_refresh_all_4D367((not bpy.context.scene.sna_dgs_scene_properties.r2_selected), bpy.context.scene.sna_dgs_scene_properties.r2_transforms, True)
        sna_shader_system_A4AED()
        sna_texture_creation_FD1B2()
        sna_viewport_render_A3941()
        for i_D854A in range(len(bpy.context.scene.objects)):
            if ((property_exists("bpy.context.scene.objects[i_D854A].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_D854A].modifiers) and '3DGS_Mesh_Type' in bpy.context.scene.objects[i_D854A]):
                if (bpy.context.scene.objects[i_D854A]['3DGS_Mesh_Type'] == 'face'):
                    bpy.context.scene.objects[i_D854A].hide_viewport = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
