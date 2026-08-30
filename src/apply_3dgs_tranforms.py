import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_3dgs_tranforms_5b665"
    bl_label = "3DGS Render: Apply 3DGS Tranforms"
    bl_description = "Applies rotation and scale transforms and updates 3DGS Attributes"
    bl_options = {"REGISTER", "UNDO"}
    sna_apply_location: bpy.props.BoolProperty(name='Apply location', description='', options={'HIDDEN'}, default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        target_obj_name = bpy.context.view_layer.objects.active.name
        load_export_transform_utils().apply_transforms_to_object(target_obj_name)
        bpy.ops.object.transform_apply('INVOKE_DEFAULT', location=self.sna_apply_location)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_84D03 = layout.box()
        box_84D03.prop(self, 'sna_apply_location', text='Apply Location', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
