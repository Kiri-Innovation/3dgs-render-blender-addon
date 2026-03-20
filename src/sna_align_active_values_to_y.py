import bpy

def sna_align_active_values_to_y_E5E9E():
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_2'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_3'] = -7.642740166592926e-15
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_4'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_5'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_6'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_7'] = -4.3711398944878965e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_8'] = -1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_9'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_10'] = 8.470330482284962e-22
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_11'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_12'] = -4.3711398944878965e-08
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_13'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_14'] = -0.2445569932460785
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_15'] = -3.571039915084839
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_16'] = -9.365139961242676
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_17'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_34'] = 411.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_35'] = 853.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_18'] = 1.4878499507904053
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_19'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_20'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_21'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_22'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_23'] = 0.7168909907341003
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_24'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_25'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_26'] = -0.050099000334739685
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_27'] = 0.01845400035381317
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_28'] = -1.0002000331878662
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_30'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_31'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_29'] = -1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_32'] = -0.20002000033855438
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_33'] = 0.0
    bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()
