from bpy_extras.io_utils import ImportHelper, ExportHelper
from .important import *
import bpy
import webbrowser

class SNA_OT_Dgs_Render_Open_Tutorial_Video_0684A(bpy.types.Operator):
    bl_idname = "sna.dgs_render_open_tutorial_video_0684a"
    bl_label = "3DGS Render: Open Tutorial Video"
    bl_description = "Launches a browser with the addon documentation video"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.youtube.com/@BlenderAddon-fromKIRI'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
