import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_add_to_view3d_mt_object_apply_4C860(self, context):
    if not (False):
        layout = self.layout
        if '3DGS_Mesh_Type' in bpy.context.view_layer.objects.active:
            col_B3C28 = layout.column(heading='', align=False)
            col_B3C28.alert = False
            col_B3C28.enabled = True
            col_B3C28.active = True
            col_B3C28.use_property_split = False
            col_B3C28.use_property_decorate = False
            col_B3C28.scale_x = 1.0
            col_B3C28.scale_y = 1.0
            col_B3C28.alignment = 'Expand'.upper()
            col_B3C28.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_B3C28.operator('sna.dgs_render_apply_3dgs_tranforms_5b665', text='Apply 3DGS Transforms', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')), emboss=True, depress=False)
            op.sna_apply_location = False
            if bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == "face":
                op = col_B3C28.operator('sna.dgs_render_convert_face_3dgs_to_vert_3dgs_fc49c', text='Convert Face 3DGS to Vert 3DGS', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')), emboss=True, depress=False)
            elif bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == "vert":
                op = col_B3C28.operator('sna.dgs_render_convert_vert_3dgs_to_face_3dgs_e6635', text='Convert Vert 3DGS to Face 3DGS', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')), emboss=True, depress=False)
            else:
                pass
