import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_and_add_geo_nodes_function_execute import sna_append_and_add_geo_nodes_function_execute_6BCD7
from .move_modifier_index import sna_move_modifier_index_23126

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Add_Uv_Edit_Modifier_E8Ae6(bpy.types.Operator):
    bl_idname = "sna.dgs_render_add_uv_edit_modifier_e8ae6"
    bl_label = "3DGS Render: Add UV Edit Modifier"
    bl_description = "Adds a UV Edit modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        if (bpy.context.view_layer.objects.active.type == 'MESH' or bpy.context.view_layer.objects.active.type == 'CURVE'):
            created_modifier_0_06d8b = sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Render_UV_Edit_GN', 'KIRI_3DGS_Render_UV_Edit_GN', bpy.context.view_layer.objects.active)
            sna_move_modifier_index_23126(bpy.context.view_layer.objects.active, 'KIRI_3DGS_Render_UV_Edit_GN', int(len(bpy.context.view_layer.objects.active.modifiers) - 1.0))
        else:
            self.report({'INFO'}, message='The Active Object is not a mesh or curve object.')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
