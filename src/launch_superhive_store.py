import bpy
from .important import *
from bpy_extras.io_utils import ImportHelper, ExportHelper
import webbrowser

class SNA_OT_Dgs_Render_Launch_Superhive_Store_08F23(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_superhive_store_08f23"
    bl_label = "3DGS Render: Launch SuperHive Store"
    bl_description = "Launches a browser for the KIRI Engine SuperHive store"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://blendermarket.com/creators/blender-addon-from-kiri-engine'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
