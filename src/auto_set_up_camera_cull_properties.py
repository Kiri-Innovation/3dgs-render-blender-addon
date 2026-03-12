import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper

class SNA_OT_Dgs_Render_Auto_Set_Up_Camera_Cull_Properties_Aef48(bpy.types.Operator):
    bl_idname = "sna.dgs_render_auto_set_up_camera_cull_properties_aef48"
    bl_label = "3DGS Render: Auto Set Up Camera Cull Properties"
    bl_description = "Sets the Camera Cull properties to the current scene/camera settings"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN']['Socket_2'] = bpy.context.scene.render.resolution_x
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN']['Socket_3'] = bpy.context.scene.render.resolution_y
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN']['Socket_4'] = bpy.context.scene.camera.data.lens
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Camera_Cull_GN']['Socket_5'] = bpy.context.scene.camera.data.sensor_width
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
