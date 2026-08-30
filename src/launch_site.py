import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Launch_Site_Bf973(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_site_bf973"
    bl_label = "3DGS Render: Launch Site"
    bl_description = "Launches a web browser"
    bl_options = {"REGISTER", "UNDO"}
    sna_site_address: bpy.props.StringProperty(name='Site Address', description='', default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        url = self.sna_site_address
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
