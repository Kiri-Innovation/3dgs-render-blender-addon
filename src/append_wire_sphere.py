import bpy
from .important import *
import os


class SNA_OT_Dgs_Render_Append_Wire_Sphere_2Bf63(bpy.types.Operator):
    bl_idname = "sna.dgs_render_append_wire_sphere_2bf63"
    bl_label = "3DGS Render: Append Wire Sphere"
    bl_description = "Appends an object for use as a modifier effector. The object will not render."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    # TODO: check of ospath here causes any issues
    def execute(self, context):
        before_data = list(bpy.data.objects)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V4.blend') + r'\Object', filename='Wire Sphere', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_69F39 = None if not new_data else new_data[0]
        appended_69F39.location = bpy.context.scene.cursor.location
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

