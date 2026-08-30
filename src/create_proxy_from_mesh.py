import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .b2_load_from_blender_object import sna_b2_load_from_blender_object_F0CCB
from .shader_system import sna_shader_system_A4AED
from .texture_creation import sna_texture_creation_FD1B2
from .viewport_render import sna_viewport_render_A3941

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Create_Proxy_From_Mesh_Eafbb(bpy.types.Operator):
    bl_idname = "sna.dgs_render_create_proxy_from_mesh_eafbb"
    bl_label = "3DGS Render: Create Proxy From Mesh"
    bl_description = "Create a Proxy Empty from the active 3DGS mesh. The mesh must not be hidden."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        exec('import os')
        sna_b2_load_from_blender_object_F0CCB(bpy.context.view_layer.objects.active.name + 'Splat_Proxy')
        sna_shader_system_A4AED()
        sna_texture_creation_FD1B2()
        sna_viewport_render_A3941(bpy.context.scene.sna_dgs_scene_properties.r2_sh_degree, bpy.context.scene.sna_dgs_scene_properties.r2_sort_threshold, bpy.context.scene.sna_dgs_scene_properties.rt_rotation_sort_threshold)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
