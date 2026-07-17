import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Disable_Hq_Overlap_34678(bpy.types.Operator):
    bl_idname = "sna.dgs_render_disable_hq_overlap_34678"
    bl_label = "3DGS Render: Disable HQ Overlap"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.data.objects.remove(object=bpy.data.objects['KIRI_HQ_Merged_Object'], do_unlink=True, do_id_user=True, do_ui_user=True, )
        if property_exists("bpy.data.collections['3DGS_HQ_Object']", globals(), locals()):
            bpy.data.collections.remove(collection=bpy.data.collections['3DGS_HQ_Object'], do_unlink=True, do_id_user=True, do_ui_user=True, )
        if property_exists("bpy.data.collections['3DGS_LQ_Objects']", globals(), locals()):
            for i_EF373 in range(len(bpy.data.collections['3DGS_LQ_Objects'].all_objects)):
                bpy.data.collections['3DGS_LQ_Objects'].all_objects[i_EF373].hide_viewport = False
                bpy.data.collections['3DGS_LQ_Objects'].all_objects[i_EF373].hide_render = False
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_2D485 = layout.box()
        box_2D485.alert = False
        box_2D485.enabled = True
        box_2D485.active = True
        box_2D485.use_property_split = False
        box_2D485.use_property_decorate = False
        box_2D485.alignment = 'Expand'.upper()
        box_2D485.scale_x = 1.0
        box_2D485.scale_y = 1.0
        if not True: box_2D485.operator_context = "EXEC_DEFAULT"
        box_2D485.label(text='HQ Object Found In Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_2D485.label(text='        Remove It?', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
