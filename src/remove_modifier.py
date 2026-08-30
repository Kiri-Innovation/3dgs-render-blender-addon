import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Remove_Modifier_9Cf0D(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_modifier_9cf0d"
    bl_label = "3DGS Render: Remove Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}
    sna_target_object: bpy.props.StringProperty(name='Target Object', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)
    sna_target_modifier: bpy.props.StringProperty(name='Target Modifier', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        bpy.data.objects[self.sna_target_object].modifiers.remove(modifier=bpy.data.objects[self.sna_target_object].modifiers[self.sna_target_modifier], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
