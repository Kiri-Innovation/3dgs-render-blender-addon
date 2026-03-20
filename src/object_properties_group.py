# import bpy
# from .update_camera_single_time import sna_update_camera_single_time_9EF18
#
# class SNA_GROUP_sna_dgs_object_properties_group(bpy.types.PropertyGroup):
#     update_mode: bpy.props.EnumProperty(name='Update_Mode', description='', items=[('Disable Camera Updates', 'Disable Camera Updates', '', 0, 0), ('Enable Camera Updates', 'Enable Camera Updates', '', 0, 1), ('Show As Point Cloud', 'Show As Point Cloud', '', 0, 2)], update=sna_update_update_mode_868D4)
#     cam_update: bpy.props.BoolProperty(name='Cam_Update', description='', default=False, update=sna_update_cam_update_DE26E)
#
# def sna_update_update_mode_868D4(self, context):
#     sna_updated_prop = self.update_mode
#     bpy.context.view_layer.objects.active['update_rot_to_cam'] = (sna_updated_prop == 'Enable Camera Updates')
#     bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = (2 if (sna_updated_prop == 'Show As Point Cloud') else (1 if (sna_updated_prop != 'Enable Camera Updates') else 0))
#     bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'].show_viewport = (True if (sna_updated_prop != 'Disable Camera Updates') else False)
#     bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
#     if bpy.context and bpy.context.screen:
#         for a in bpy.context.screen.areas:
#             a.tag_redraw()
#
# def sna_update_cam_update_DE26E(self, context):
#     sna_updated_prop = self.cam_update
#     if sna_updated_prop:
#         bpy.context.area.spaces.active.region_3d.view_perspective = 'CAMERA'
#         bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop
#
#         def delayed_214CF():
#             sna_update_camera_single_time_9EF18()
#         bpy.app.timers.register(delayed_214CF, first_interval=0.10000000149011612)
#     else:
#         bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_54'] = sna_updated_prop
