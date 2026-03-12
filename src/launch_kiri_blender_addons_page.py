import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
import webbrowser

class SNA_OT_Dgs_Render_Launch_Kiri_Blender_Addons_Page_9D58C(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_kiri_blender_addons_page_9d58c"
    bl_label = "3DGS Render: Launch KIRI Blender Addons page"
    bl_description = "Launches a browser for the KIRI Engine Blender Market store"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.app/blender-addon'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
