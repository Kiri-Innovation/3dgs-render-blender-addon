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
        box_5B434.alert = False
        box_5B434.enabled = True
        box_5B434.active = True
        box_5B434.use_property_split = False
        box_5B434.use_property_decorate = False
        box_5B434.alignment = 'Expand'.upper()
        box_5B434.scale_x = 1.0
        box_5B434.scale_y = 1.0
        if not True: box_5B434.operator_context = "EXEC_DEFAULT"
        box_5B434.label(text='Eevee is not enabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    if (bpy.context.scene.camera == None):
        box_9AC8C = layout_function.box()
        box_9AC8C.alert = False
        box_9AC8C.enabled = True
        box_9AC8C.active = True
        box_9AC8C.use_property_split = False
        box_9AC8C.use_property_decorate = False
        box_9AC8C.alignment = 'Expand'.upper()
        box_9AC8C.scale_x = 1.0
        box_9AC8C.scale_y = 1.0
        if not True: box_9AC8C.operator_context = "EXEC_DEFAULT"
        box_9AC8C.label(text='No Active Camera', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_9AC8C.label(text='         HQ Materials Require An Active Camera', icon_value=0)
    col_249D2 = layout_function.column(heading='', align=False)
    col_249D2.alert = False
    col_249D2.enabled = True
    col_249D2.active = True
    col_249D2.use_property_split = False
    col_249D2.use_property_decorate = False
    col_249D2.scale_x = 1.0
    col_249D2.scale_y = 1.0
    col_249D2.alignment = 'Expand'.upper()
    col_249D2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if bpy.context.preferences.addons[__package__].preferences.sna_show_tips:
        box_AEE3F = col_249D2.box()
        box_AEE3F.alert = False
        box_AEE3F.enabled = True
        box_AEE3F.active = True
        box_AEE3F.use_property_split = False
        box_AEE3F.use_property_decorate = False
        box_AEE3F.alignment = 'Expand'.upper()
        box_AEE3F.scale_x = 1.0
        box_AEE3F.scale_y = 1.0
        if not True: box_AEE3F.operator_context = "EXEC_DEFAULT"
        box_AEE3F.label(text='LQ Mode requires high samples', icon_value=0)
        box_AEE3F.label(text='Samples can be set to 1 in HQ Mode', icon_value=0)
        box_AEE3F.label(text="if 'Shadeless' materials are used", icon_value=0)
    if bpy.context.scene.eevee.use_taa_reprojection:
        box_06ADA = col_249D2.box()
        box_06ADA.alert = False
        box_06ADA.enabled = True
        box_06ADA.active = True
        box_06ADA.use_property_split = False
        box_06ADA.use_property_decorate = False
        box_06ADA.alignment = 'Expand'.upper()
        box_06ADA.scale_x = 1.0
        box_06ADA.scale_y = 1.0
        if not True: box_06ADA.operator_context = "EXEC_DEFAULT"
        box_06ADA.label(text='Temporal Reprojection is enabled ', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_06ADA.label(text='This can cause flickering', icon_value=0)
    box_0F8BF = col_249D2.box()
    box_0F8BF.alert = False
    box_0F8BF.enabled = True
    box_0F8BF.active = True
    box_0F8BF.use_property_split = False
    box_0F8BF.use_property_decorate = False
    box_0F8BF.alignment = 'Expand'.upper()
    box_0F8BF.scale_x = 1.0
    box_0F8BF.scale_y = 1.0
    if not True: box_0F8BF.operator_context = "EXEC_DEFAULT"
    col_E83D4 = box_0F8BF.column(heading='', align=True)
    col_E83D4.alert = False
    col_E83D4.enabled = True
    col_E83D4.active = True
    col_E83D4.use_property_split = False
    col_E83D4.use_property_decorate = False
    col_E83D4.scale_x = 1.0
    col_E83D4.scale_y = 1.0
    col_E83D4.alignment = 'Expand'.upper()
    col_E83D4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_E83D4.prop(bpy.context.scene.eevee, 'taa_samples', text='Eevee Viewport Samples', icon_value=0, emboss=True)
    col_E83D4.prop(bpy.context.scene.eevee, 'taa_render_samples', text='Eevee Render Samples', icon_value=0, emboss=True)
    if bpy.context.scene.eevee.use_taa_reprojection:
        box_6EA64 = col_249D2.box()
        box_6EA64.alert = False
        box_6EA64.enabled = True
        box_6EA64.active = True
        box_6EA64.use_property_split = False
        box_6EA64.use_property_decorate = False
        box_6EA64.alignment = 'Expand'.upper()
        box_6EA64.scale_x = 1.0
        box_6EA64.scale_y = 1.0
        if not True: box_6EA64.operator_context = "EXEC_DEFAULT"
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
                box_2E343.alert = False
                box_2E343.enabled = True
                box_2E343.active = True
                box_2E343.use_property_split = False
                box_2E343.use_property_decorate = False
                box_2E343.alignment = 'Expand'.upper()
                box_2E343.scale_x = 1.0
                box_2E343.scale_y = 1.0
                if not True: box_2E343.operator_context = "EXEC_DEFAULT"
                row_19BC2 = box_2E343.row(heading='', align=False)
                row_19BC2.alert = False
                row_19BC2.enabled = True
                row_19BC2.active = True
                row_19BC2.use_property_split = False
                row_19BC2.use_property_decorate = False
                row_19BC2.scale_x = 1.0
                row_19BC2.scale_y = 1.0
                row_19BC2.alignment = 'Expand'.upper()
                row_19BC2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_19BC2.label(text=str(bpy.context.view_layer.objects.active.material_slots[i_E3C27].material.name), icon_value=0)
                box_2E343.prop(bpy.context.view_layer.objects.active.material_slots[i_E3C27].material.sna_dgs_material_properties, 'lq_hq', text='', icon_value=0, emboss=True)
    col_249D2.separator(factor=1.0)
    box_D2847 = col_249D2.box()
    box_D2847.alert = False
    box_D2847.enabled = True
    box_D2847.active = True
    box_D2847.use_property_split = False
    box_D2847.use_property_decorate = False
    box_D2847.alignment = 'Expand'.upper()
    box_D2847.scale_x = 1.0
    box_D2847.scale_y = 1.0
    if not True: box_D2847.operator_context = "EXEC_DEFAULT"
    box_D2847.prop(bpy.context.scene.sna_dgs_scene_properties, 'hq_overlap', text='HQ Objects Overlap', icon_value=0, emboss=True, toggle=False)
    if bpy.context.scene.sna_dgs_scene_properties.hq_overlap:
        box_0826A = col_249D2.box()
        box_0826A.alert = False
        box_0826A.enabled = True
        box_0826A.active = True
        box_0826A.use_property_split = False
        box_0826A.use_property_decorate = False
        box_0826A.alignment = 'Expand'.upper()
        box_0826A.scale_x = 1.0
        box_0826A.scale_y = 1.0
        if not True: box_0826A.operator_context = "EXEC_DEFAULT"
        if (property_exists("bpy.context.scene.objects", globals(), locals()) and 'KIRI_HQ_Merged_Object' in bpy.context.scene.objects):
            box_BEFDD = box_0826A.box()
            box_BEFDD.alert = False
            box_BEFDD.enabled = False
            box_BEFDD.active = True
            box_BEFDD.use_property_split = False
            box_BEFDD.use_property_decorate = False
            box_BEFDD.alignment = 'Expand'.upper()
            box_BEFDD.scale_x = 1.0
            box_BEFDD.scale_y = 1.0
            if not True: box_BEFDD.operator_context = "EXEC_DEFAULT"
            box_BEFDD.label(text='HQ Object Already Exists', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            op = box_BEFDD.operator('sna.dgs_render_generate_hq_object_55455', text='Generate HQ Object', icon_value=0, emboss=True, depress=False)
        else:
            op = box_0826A.operator('sna.dgs_render_generate_hq_object_55455', text='Generate HQ Object', icon_value=0, emboss=True, depress=False)
