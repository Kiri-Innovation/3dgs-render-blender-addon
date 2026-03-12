import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper

class SNA_OT_Dgs_Render_Import_Image_Overlay_4A457(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.dgs_render_import_image_overlay_4a457"
    bl_label = "3DGS Render: Import Image Overlay"
    bl_description = "Import an image an assign it as the image overlay."
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.png;*.jpg;*.exr', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        image_AB939 = bpy.data.images.load(filepath=self.filepath, check_existing=True, )
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Adjust_Colour_And_Material']['Socket_60'] = image_AB939
        bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}
