import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper

class SNA_OT_Dgs_Render_Append_Geometry_Node_Modifier_C2492(bpy.types.Operator):
    bl_idname = "sna.dgs_render_append_geometry_node_modifier_c2492"
    bl_label = "3DGS Render: Append Geometry Node Modifier"
    bl_description = "Adds a geometry node modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}
    sna_node_group_name: bpy.props.StringProperty(name='Node Group Name', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)
    sna_modifier_name: bpy.props.StringProperty(name='Modifier Name', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.view_layer.objects.active.type == 'MESH' or bpy.context.view_layer.objects.active.type == 'CURVE'):
            created_modifier_0_7a9a7 = sna_append_and_add_geo_nodes_function_execute_6BCD7(self.sna_node_group_name, self.sna_node_group_name, bpy.context.view_layer.objects.active)
            for i_1A879 in range(len(bpy.context.view_layer.objects.active.modifiers)):
                if (bpy.context.view_layer.objects.active.modifiers[i_1A879] == created_modifier_0_7a9a7):
                    bpy.context.view_layer.objects.active.modifiers.move(from_index=i_1A879, to_index=0, )
        else:
            self.report({'INFO'}, message='The Active Object is not a mesh or curve object.')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
