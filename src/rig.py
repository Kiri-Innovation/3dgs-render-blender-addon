import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .bind_and_misc_tools import sna_bind_and_misc_tools_C36C1
from .rig_cache_frames import sna_rig_cache_frames_993DF
from .rig_update_settings import sna_rig_update_settings_88DF0

__package__ = __package__.rsplit('.', 1)[0]


def sna_rig_891FC(layout_function, ):
    if (bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory == ''):
        box_B8623 = layout_function.box()
        box_B8623.alert = False
        box_B8623.enabled = True
        box_B8623.active = True
        box_B8623.use_property_split = False
        box_B8623.use_property_decorate = False
        box_B8623.alignment = 'Expand'.upper()
        box_B8623.scale_x = 1.0
        box_B8623.scale_y = 1.0
        if not True: box_B8623.operator_context = "EXEC_DEFAULT"
        box_B8623.label(text='Cache directory is empty.', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_B8623.label(text='Set it in Preferences', icon_value=0)
    col_939A0 = layout_function.column(heading='', align=True)
    col_939A0.alert = False
    col_939A0.enabled = (bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory != '')
    col_939A0.active = True
    col_939A0.use_property_split = False
    col_939A0.use_property_decorate = False
    col_939A0.scale_x = 1.0
    col_939A0.scale_y = 1.0
    col_939A0.alignment = 'Expand'.upper()
    col_939A0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_939A0.label(text='Binding Data', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    if (bpy.context.view_layer.objects.active == None):
        box_D50A3 = col_939A0.box()
        box_D50A3.alert = False
        box_D50A3.enabled = True
        box_D50A3.active = True
        box_D50A3.use_property_split = False
        box_D50A3.use_property_decorate = False
        box_D50A3.alignment = 'Expand'.upper()
        box_D50A3.scale_x = 1.0
        box_D50A3.scale_y = 2.0
        if not True: box_D50A3.operator_context = "EXEC_DEFAULT"
        box_D50A3.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    else:
        if bpy.context.view_layer.objects.active.type == 'ARMATURE':
            box_C4E6D = col_939A0.box()
            box_C4E6D.alert = False
            box_C4E6D.enabled = True
            box_C4E6D.active = True
            box_C4E6D.use_property_split = False
            box_C4E6D.use_property_decorate = False
            box_C4E6D.alignment = 'Expand'.upper()
            box_C4E6D.scale_x = 1.0
            box_C4E6D.scale_y = 1.0
            if not True: box_C4E6D.operator_context = "EXEC_DEFAULT"
            box_C4E6D.label(text='Armature Tools', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            box_C4E6D.prop(bpy.context.view_layer.objects.active.data, 'pose_position', text=bpy.context.view_layer.objects.active.data.pose_position, icon_value=0, emboss=True, expand=True)
            op = box_C4E6D.operator('sna.dgs_render_apply_armature_pose_as_rest_pose_a8c68', text='Apply pose as Rest Pose', icon_value=0, emboss=True, depress=False)
        else:
            if '3DGS_Mesh_Type' in bpy.context.view_layer.objects.active:
                if (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'face'):
                    box_A082B = col_939A0.box()
                    box_A082B.alert = False
                    box_A082B.enabled = True
                    box_A082B.active = True
                    box_A082B.use_property_split = False
                    box_A082B.use_property_decorate = False
                    box_A082B.alignment = 'Expand'.upper()
                    box_A082B.scale_x = 1.0
                    box_A082B.scale_y = 1.0
                    if not True: box_A082B.operator_context = "EXEC_DEFAULT"
                    box_A082B.label(text='Rigging is only available for Vert based', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    box_A082B.label(text='3DGS objects. You can convert this object', icon_value=0)
                    box_A082B.label(text='from the Ctrl+A menu', icon_value=0)
                else:
                    col_29EE2 = col_939A0.column(heading='', align=False)
                    col_29EE2.alert = False
                    col_29EE2.enabled = True
                    col_29EE2.active = True
                    col_29EE2.use_property_split = False
                    col_29EE2.use_property_decorate = False
                    col_29EE2.scale_x = 1.0
                    col_29EE2.scale_y = 1.0
                    col_29EE2.alignment = 'Expand'.upper()
                    col_29EE2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    if 'proxy_binding_active' in bpy.context.view_layer.objects.active:
                        if bpy.context.view_layer.objects.active['proxy_binding_active']:
                            box_B68AA = col_29EE2.box()
                            box_B68AA.alert = True
                            box_B68AA.enabled = True
                            box_B68AA.active = True
                            box_B68AA.use_property_split = False
                            box_B68AA.use_property_decorate = False
                            box_B68AA.alignment = 'Expand'.upper()
                            box_B68AA.scale_x = 1.0
                            box_B68AA.scale_y = 1.0
                            if not True: box_B68AA.operator_context = "EXEC_DEFAULT"
                            op = box_B68AA.operator('sna.dgs_render_unbind_from_proxy_mesh_7648d', text='Unbind', icon_value=0, emboss=True, depress=False)
                        else:
                            box_485E0 = col_29EE2.box()
                            box_485E0.alert = False
                            box_485E0.enabled = True
                            box_485E0.active = True
                            box_485E0.use_property_split = False
                            box_485E0.use_property_decorate = False
                            box_485E0.alignment = 'Expand'.upper()
                            box_485E0.scale_x = 1.0
                            box_485E0.scale_y = 1.0
                            if not True: box_485E0.operator_context = "EXEC_DEFAULT"
                            op = box_485E0.operator('sna.dgs_render_unbind_from_proxy_mesh_7648d', text='Unbind / Refresh', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'refresh.svg')), emboss=True, depress=False)
                    box_B63D8 = col_29EE2.box()
                    box_B63D8.alert = False
                    box_B63D8.enabled = True
                    box_B63D8.active = True
                    box_B63D8.use_property_split = False
                    box_B63D8.use_property_decorate = False
                    box_B63D8.alignment = 'Expand'.upper()
                    box_B63D8.scale_x = 1.0
                    box_B63D8.scale_y = 1.0
                    if not True: box_B63D8.operator_context = "EXEC_DEFAULT"
                    box_B63D8.label(text='Proxy Mesh', icon_value=0)
                    row_6ADB2 = box_B63D8.row(heading='', align=True)
                    row_6ADB2.alert = False
                    row_6ADB2.enabled = True
                    row_6ADB2.active = True
                    row_6ADB2.use_property_split = False
                    row_6ADB2.use_property_decorate = False
                    row_6ADB2.scale_x = 1.0
                    row_6ADB2.scale_y = 1.0
                    row_6ADB2.alignment = 'Expand'.upper()
                    row_6ADB2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    row_6ADB2.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'rig_proxy_mesh', text='', icon_value=0, emboss=True)
                    if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh == None):
                        pass
                    else:
                        row_E7B4F = row_6ADB2.row(heading='', align=True)
                        row_E7B4F.alert = False
                        row_E7B4F.enabled = True
                        row_E7B4F.active = True
                        row_E7B4F.use_property_split = False
                        row_E7B4F.use_property_decorate = False
                        row_E7B4F.scale_x = 1.0
                        row_E7B4F.scale_y = 1.0
                        row_E7B4F.alignment = 'Expand'.upper()
                        row_E7B4F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                        op = row_E7B4F.operator('sna.dgs_render_select_object_b1f49', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'mouse-pointer.svg')), emboss=True, depress=False)
                        op.sna_object_name = bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh.name
                        row_E7B4F.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh, 'hide_viewport', text='', icon_value=0, emboss=True)
                        row_E7B4F.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh, 'hide_render', text='', icon_value=0, emboss=True)
                    if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh == None):
                        pass
                    else:
                        col_29EE2.separator(factor=3.0)
                        if 'proxy_binding_active' in bpy.context.view_layer.objects.active:
                            if bpy.context.view_layer.objects.active['proxy_binding_active']:
                                col_73DBB = col_29EE2.column(heading='', align=False)
                                col_73DBB.alert = False
                                col_73DBB.enabled = True
                                col_73DBB.active = True
                                col_73DBB.use_property_split = False
                                col_73DBB.use_property_decorate = False
                                col_73DBB.scale_x = 1.0
                                col_73DBB.scale_y = 1.0
                                col_73DBB.alignment = 'Expand'.upper()
                                col_73DBB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                box_21FC2 = col_73DBB.box()
                                box_21FC2.alert = False
                                box_21FC2.enabled = True
                                box_21FC2.active = True
                                box_21FC2.use_property_split = False
                                box_21FC2.use_property_decorate = False
                                box_21FC2.alignment = 'Expand'.upper()
                                box_21FC2.scale_x = 1.0
                                box_21FC2.scale_y = 1.0
                                if not True: box_21FC2.operator_context = "EXEC_DEFAULT"
                                box_21FC2.label(text='Update Settings', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
                                col_4847A = box_21FC2.column(heading='', align=True)
                                col_4847A.alert = False
                                col_4847A.enabled = True
                                col_4847A.active = True
                                col_4847A.use_property_split = False
                                col_4847A.use_property_decorate = False
                                col_4847A.scale_x = 1.0
                                col_4847A.scale_y = 1.0
                                col_4847A.alignment = 'Expand'.upper()
                                col_4847A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                col_4847A.label(text='Update Mode', icon_value=0)
                                row_88338 = col_4847A.row(heading='', align=False)
                                row_88338.alert = False
                                row_88338.enabled = True
                                row_88338.active = True
                                row_88338.use_property_split = False
                                row_88338.use_property_decorate = False
                                row_88338.scale_x = 1.0
                                row_88338.scale_y = 1.0
                                row_88338.alignment = 'Expand'.upper()
                                row_88338.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                row_88338.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_update_mode', text=bpy.context.scene.sna_dgs_scene_properties.rig_update_mode, icon_value=0, emboss=True, expand=True)
                                if bpy.context.scene.sna_dgs_scene_properties.rig_update_mode == "Single":
                                    col_2CAD4 = box_21FC2.column(heading='', align=False)
                                    col_2CAD4.alert = False
                                    col_2CAD4.enabled = True
                                    col_2CAD4.active = True
                                    col_2CAD4.use_property_split = False
                                    col_2CAD4.use_property_decorate = False
                                    col_2CAD4.scale_x = 1.0
                                    col_2CAD4.scale_y = 1.0
                                    col_2CAD4.alignment = 'Expand'.upper()
                                    col_2CAD4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                    if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
                                        if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                                            layout_function = col_2CAD4
                                            sna_rig_update_settings_88DF0(layout_function, False, False)
                                        else:
                                            layout_function = col_2CAD4
                                            sna_rig_update_settings_88DF0(layout_function, False, True)
                                    else:
                                        layout_function = col_2CAD4
                                        sna_rig_update_settings_88DF0(layout_function, False, True)
                                    col_2CAD4.separator(factor=1.0)
                                    col_DF573 = col_2CAD4.column(heading='', align=False)
                                    col_DF573.alert = False
                                    col_DF573.enabled = True
                                    col_DF573.active = True
                                    col_DF573.use_property_split = False
                                    col_DF573.use_property_decorate = False
                                    col_DF573.scale_x = 1.0
                                    col_DF573.scale_y = 2.0
                                    col_DF573.alignment = 'Expand'.upper()
                                    col_DF573.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                    op = col_DF573.operator('sna.dgs_render_update_bound_3dgs_from_proxy_mesh_951a0', text='Update Single', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg')), emboss=True, depress=False)
                                elif bpy.context.scene.sna_dgs_scene_properties.rig_update_mode == "Interval":
                                    col_6A648 = box_21FC2.column(heading='', align=False)
                                    col_6A648.alert = False
                                    col_6A648.enabled = True
                                    col_6A648.active = True
                                    col_6A648.use_property_split = False
                                    col_6A648.use_property_decorate = False
                                    col_6A648.scale_x = 1.0
                                    col_6A648.scale_y = 1.0
                                    col_6A648.alignment = 'Expand'.upper()
                                    col_6A648.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                    if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
                                        if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                                            layout_function = col_6A648
                                            sna_rig_update_settings_88DF0(layout_function, False, False)
                                        else:
                                            layout_function = col_6A648
                                            sna_rig_update_settings_88DF0(layout_function, False, True)
                                    else:
                                        layout_function = col_6A648
                                        sna_rig_update_settings_88DF0(layout_function, False, True)
                                    col_6A648.separator(factor=1.0)
                                    box_3F9E9 = col_6A648.box()
                                    box_3F9E9.alert = False
                                    box_3F9E9.enabled = True
                                    box_3F9E9.active = True
                                    box_3F9E9.use_property_split = False
                                    box_3F9E9.use_property_decorate = False
                                    box_3F9E9.alignment = 'Expand'.upper()
                                    box_3F9E9.scale_x = 1.0
                                    box_3F9E9.scale_y = 1.0
                                    if not True: box_3F9E9.operator_context = "EXEC_DEFAULT"
                                    if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
                                        if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                                            layout_function = box_3F9E9
                                            sna_rig_cache_frames_993DF(layout_function, False)
                                        else:
                                            layout_function = box_3F9E9
                                            sna_rig_cache_frames_993DF(layout_function, True)
                                    else:
                                        layout_function = box_3F9E9
                                        sna_rig_cache_frames_993DF(layout_function, True)
                                    if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
                                        if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                                            pass
                                        else:
                                            col_55551 = box_3F9E9.column(heading='', align=False)
                                            col_55551.alert = False
                                            col_55551.enabled = True
                                            col_55551.active = True
                                            col_55551.use_property_split = False
                                            col_55551.use_property_decorate = False
                                            col_55551.scale_x = 1.0
                                            col_55551.scale_y = 2.0
                                            col_55551.alignment = 'Expand'.upper()
                                            col_55551.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                            op = col_55551.operator('sna.dgs_render_bake_frames_to_cache_90885', text='Bake Frames to Cache', icon_value=0, emboss=True, depress=False)
                                    else:
                                        col_A92B7 = box_3F9E9.column(heading='', align=False)
                                        col_A92B7.alert = False
                                        col_A92B7.enabled = True
                                        col_A92B7.active = True
                                        col_A92B7.use_property_split = False
                                        col_A92B7.use_property_decorate = False
                                        col_A92B7.scale_x = 1.0
                                        col_A92B7.scale_y = 2.0
                                        col_A92B7.alignment = 'Expand'.upper()
                                        col_A92B7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                        op = col_A92B7.operator('sna.dgs_render_bake_frames_to_cache_90885', text='Bake Frames to Cache', icon_value=0, emboss=True, depress=False)
                                    if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
                                        if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                                            box_0905C = col_6A648.box()
                                            box_0905C.alert = False
                                            box_0905C.enabled = True
                                            box_0905C.active = True
                                            box_0905C.use_property_split = False
                                            box_0905C.use_property_decorate = False
                                            box_0905C.alignment = 'Expand'.upper()
                                            box_0905C.scale_x = 1.0
                                            box_0905C.scale_y = 1.0
                                            if not True: box_0905C.operator_context = "EXEC_DEFAULT"
                                            col_935FA = box_0905C.column(heading='', align=True)
                                            col_935FA.alert = False
                                            col_935FA.enabled = True
                                            col_935FA.active = True
                                            col_935FA.use_property_split = False
                                            col_935FA.use_property_decorate = False
                                            col_935FA.scale_x = 1.0
                                            col_935FA.scale_y = 1.0
                                            col_935FA.alignment = 'Expand'.upper()
                                            col_935FA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                            col_935FA.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_update_interval', text='Update Interval', icon_value=0, emboss=True)
                                            col_16CA7 = col_935FA.column(heading='', align=False)
                                            col_16CA7.alert = False
                                            col_16CA7.enabled = True
                                            col_16CA7.active = True
                                            col_16CA7.use_property_split = False
                                            col_16CA7.use_property_decorate = False
                                            col_16CA7.scale_x = 1.0
                                            col_16CA7.scale_y = 2.0
                                            col_16CA7.alignment = 'Expand'.upper()
                                            col_16CA7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                            if bpy.context.scene.sna_dgs_scene_properties.rig_interval_stop:
                                                op = col_16CA7.operator('sna.dgs_render_update_bound_3dgs_from_cache_385ec', text='Update from cache', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'play.svg')), emboss=True, depress=False)
                                            else:
                                                col_BE41C = col_16CA7.column(heading='', align=False)
                                                col_BE41C.alert = True
                                                col_BE41C.enabled = True
                                                col_BE41C.active = True
                                                col_BE41C.use_property_split = False
                                                col_BE41C.use_property_decorate = False
                                                col_BE41C.scale_x = 1.0
                                                col_BE41C.scale_y = 1.0
                                                col_BE41C.alignment = 'Expand'.upper()
                                                col_BE41C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                                                op = col_BE41C.operator('sna.dgs_render_end_proxy_rig_updates_60c6a', text='Stop', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'stop.svg')), emboss=True, depress=False)
                                else:
                                    pass
                                col_73DBB.separator(factor=1.0)
                                if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
                                    if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                                        if 'rig_baked_render_enabled' in bpy.context.view_layer.objects.active:
                                            box_0F4AD = col_73DBB.box()
                                            box_0F4AD.alert = False
                                            box_0F4AD.enabled = True
                                            box_0F4AD.active = True
                                            box_0F4AD.use_property_split = False
                                            box_0F4AD.use_property_decorate = False
                                            box_0F4AD.alignment = 'Expand'.upper()
                                            box_0F4AD.scale_x = 1.0
                                            box_0F4AD.scale_y = 1.0
                                            if not True: box_0F4AD.operator_context = "EXEC_DEFAULT"
                                            box_0F4AD.label(text='Rig Render Settings', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
                                            attr_003BE = '["' + str('rig_baked_render_enabled' + '"]') 
                                            box_0F4AD.prop(*kiri_geometry_nodes_ui_target(bpy.context.view_layer.objects.active, attr_003BE), text='Enable rig updates in renders', icon_value=0, emboss=True)
                                else:
                                    layout_function = col_73DBB
                                    sna_rig_cache_frames_993DF(layout_function, True)
                            else:
                                layout_function = col_29EE2
                                sna_bind_and_misc_tools_C36C1(layout_function, )
                        else:
                            layout_function = col_29EE2
                            sna_bind_and_misc_tools_C36C1(layout_function, )
            else:
                box_958E5 = col_939A0.box()
                box_958E5.alert = False
                box_958E5.enabled = True
                box_958E5.active = True
                box_958E5.use_property_split = False
                box_958E5.use_property_decorate = False
                box_958E5.alignment = 'Expand'.upper()
                box_958E5.scale_x = 1.0
                box_958E5.scale_y = 2.0
                if not True: box_958E5.operator_context = "EXEC_DEFAULT"
                box_958E5.label(text='The Active Object is not a 3DGS Mesh', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
