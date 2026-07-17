import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


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

    def execute(self, context):
        if 'EDIT_MESH'==bpy.context.mode:
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        before_data = list(bpy.data.objects)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V5.blend') + r'\Object', filename='Wire Sphere', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_69F39 = None if not new_data else new_data[0]
        appended_69F39.location = bpy.context.scene.cursor.location
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
