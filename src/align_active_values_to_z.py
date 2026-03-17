import bpy

def sna_align_active_values_to_z_7B9ED():
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_2'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_3'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_4'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_5'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_6'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_7'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_8'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_9'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_10'] = 8.470330482284962e-22
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_11'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_12'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_13'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_14'] = -0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_15'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_16'] = -15.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_17'] = 1.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_34'] = 1920.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_35'] = 971.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_18'] = 1.0323200225830078
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_19'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_20'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_21'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_22'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_23'] = 2.041260004043579
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_24'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_25'] = 0.0
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_26'] = 0.06471700221300125
    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_27'] = 0.07061599940061569
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
