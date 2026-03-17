import bpy
from .shader_system import sna_shader_system_A4AED
from .sna_texture_creation import sna_texture_creation_FD1B2
from .sna_viewport_render import sna_viewport_render_A3941

class SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_D5B41(bpy.types.Operator):
    bl_idname = "sna.dgs_render_create_proxy_from_mesh_d5b41"
    bl_label = "3DGS Render: Create Proxy From Mesh"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_b2_load_from_blender_object_F0CCB(bpy.context.view_layer.objects.active.name + 'Splat_Proxy')
        sna_shader_system_A4AED()
        sna_texture_creation_FD1B2()
        sna_viewport_render_A3941()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
