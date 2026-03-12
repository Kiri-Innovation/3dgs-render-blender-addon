import bpy

class SNA_OT_Dgs_Render_Start_Vertex_Painting_A36E0(bpy.types.Operator):
    bl_idname = "sna.dgs_render_start_vertex_painting_a36e0"
    bl_label = "3DGS Render: Start Vertex Painting"
    bl_description = "Enters vertex paint mode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.data.color_attributes.active_color = bpy.context.view_layer.objects.active.data.color_attributes['KIRI_3DGS_Paint']
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='VERTEX_PAINT')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
