import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .relight2_0_save_original_3dgs_color import sna_relight2_0_save_original_3dgs_color_76EB6

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Store_Original_Lighting_99939(bpy.types.Operator):
    bl_idname = "sna.dgs_render_store_original_lighting_99939"
    bl_label = "3DGS Render: Store Original Lighting"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        sna_relight2_0_save_original_3dgs_color_76EB6()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_44ADA = layout.box()
        box_44ADA.label(text='Any existing stored base light data will be overwritten', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_44ADA.label(text='The current state will be set as the new base light state', icon_value=0)
        box_44ADA.label(text="This action will not respond to 'undo' commands", icon_value=0)
        box_44ADA.separator(factor=1.0)
        box_44ADA.label(text='Adding, deleting or merging points will corrupt stored data.', icon_value=0)
        box_44ADA.label(text='Edit your mesh before Light Baking, or to edit later;', icon_value=0)
        box_44ADA.label(text='restore lighting, edit mesh, store and re-bake lights', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
