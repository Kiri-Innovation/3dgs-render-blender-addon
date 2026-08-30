import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_hq_mode_function_interface_17C41(layout_function, ):
    if (bpy.context.scene.render.engine == 'BLENDER_EEVEE'):
        pass
    else:
        box_5B434 = layout_function.box()
        box_5B434.label(text='Eevee is not enabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    if (bpy.context.scene.camera == None):
        box_9AC8C = layout_function.box()
        box_9AC8C.label(text='No Active Camera', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_9AC8C.label(text='         HQ Materials Require An Active Camera', icon_value=0)
    col_249D2 = layout_function.column(heading='', align=False)
    if bpy.context.preferences.addons[__package__].preferences.sna_show_tips:
        box_AEE3F = col_249D2.box()
        box_AEE3F.label(text='LQ Mode requires high samples', icon_value=0)
        box_AEE3F.label(text='Samples can be set to 1 in HQ Mode', icon_value=0)
        box_AEE3F.label(text="if 'Shadeless' materials are used", icon_value=0)
    if bpy.context.scene.eevee.use_taa_reprojection:
        box_06ADA = col_249D2.box()
        box_06ADA.label(text='Temporal Reprojection is enabled ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_06ADA.label(text='This can cause flickering', icon_value=0)
    box_0F8BF = col_249D2.box()
    col_E83D4 = box_0F8BF.column(heading='', align=True)
    col_E83D4.prop(bpy.context.scene.eevee, 'taa_samples', text='Eevee Viewport Samples', icon_value=0, emboss=True)
    col_E83D4.prop(bpy.context.scene.eevee, 'taa_render_samples', text='Eevee Render Samples', icon_value=0, emboss=True)
    if bpy.context.scene.eevee.use_taa_reprojection:
        box_6EA64 = col_249D2.box()
        box_6EA64.prop(bpy.context.scene.eevee, 'use_taa_reprojection', text='Temporal Reprojection', icon_value=0, emboss=True)
    col_249D2.separator(factor=1.0)
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        for i_E3C27 in range(len(bpy.context.view_layer.objects.active.material_slots)):
            if (bpy.context.view_layer.objects.active.material_slots[i_E3C27].material == None):
                pass
            else:
                box_2E343 = col_249D2.box()
                row_19BC2 = box_2E343.row(heading='', align=False)
                row_19BC2.label(text=str(bpy.context.view_layer.objects.active.material_slots[i_E3C27].material.name), icon_value=0)
                box_2E343.prop(bpy.context.view_layer.objects.active.material_slots[i_E3C27].material.sna_dgs_material_properties, 'lq_hq', text='', icon_value=0, emboss=True)
    col_249D2.separator(factor=1.0)
    box_D2847 = col_249D2.box()
    box_D2847.prop(bpy.context.scene.sna_dgs_scene_properties, 'hq_overlap', text='HQ Objects Overlap', icon_value=0, emboss=True, toggle=False)
    if bpy.context.scene.sna_dgs_scene_properties.hq_overlap:
        box_0826A = col_249D2.box()
        if (property_exists("bpy.context.scene.objects", globals(), locals()) and 'KIRI_HQ_Merged_Object' in bpy.context.scene.objects):
            box_BEFDD = box_0826A.box()
            box_BEFDD.label(text='HQ Object Already Exists', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            op = box_BEFDD.operator('sna.dgs_render_generate_hq_object_55455', text='Generate HQ Object', icon_value=0, emboss=True, depress=False)
        else:
            op = box_0826A.operator('sna.dgs_render_generate_hq_object_55455', text='Generate HQ Object', icon_value=0, emboss=True, depress=False)
