import bpy
from .important import *
from bpy_extras.io_utils import ImportHelper, ExportHelper
import webbrowser

class SNA_OT_Dgs_Render_Open_Documentation_3A04F(bpy.types.Operator):
    bl_idname = "sna.dgs_render_open_documentation_3a04f"
    bl_label = "3DGS Render: Open Documentation"
    bl_description = "Launches a browser with the addon documentation"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.app/blender-addon/3dgs-render'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
