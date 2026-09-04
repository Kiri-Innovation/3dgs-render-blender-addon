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
        box_B8623.label(text='Cache directory is empty.', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_B8623.label(text='Set it in Preferences', icon_value=0)
    col_939A0 = layout_function.column(heading='', align=True)
    col_939A0.enabled = (bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory != '')
    col_939A0.label(text='Binding Data', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    if (bpy.context.view_layer.objects.active == None):
        box_D50A3 = col_939A0.box()
        box_D50A3.scale_y = 2.0
        box_D50A3.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    else:
        if bpy.context.view_layer.objects.active.type == 'ARMATURE':
            box_C4E6D = col_939A0.box()
            box_C4E6D.label(text='Armature Tools', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            box_C4E6D.prop(bpy.context.view_layer.objects.active.data, 'pose_position', text=bpy.context.view_layer.objects.active.data.pose_position, icon_value=0, emboss=True, expand=True)
            op = box_C4E6D.operator('sna.dgs_render_apply_armature_pose_as_rest_pose_a8c68', text='Apply pose as Rest Pose', icon_value=0, emboss=True, depress=False)
        else:
            if '3DGS_Mesh_Type' in bpy.context.view_layer.objects.active:
                if (bpy.context.view_layer.objects.active['3DGS_Mesh_Type'] == 'face'):
                    box_A082B = col_939A0.box()
                    box_A082B.label(text='Rigging is only available for Vert based', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    box_A082B.label(text='3DGS objects. You can convert this object', icon_value=0)
                    box_A082B.label(text='from the Ctrl+A menu', icon_value=0)
                else:
                    col_29EE2 = col_939A0.column(heading='', align=False)
                    if 'proxy_binding_active' in bpy.context.view_layer.objects.active:
                        if bpy.context.view_layer.objects.active['proxy_binding_active']:
                            box_B68AA = col_29EE2.box()
                            box_B68AA.alert = True
                            op = box_B68AA.operator('sna.dgs_render_unbind_from_proxy_mesh_7648d', text='Unbind', icon_value=0, emboss=True, depress=False)
                        else:
                            box_485E0 = col_29EE2.box()
                            op = box_485E0.operator('sna.dgs_render_unbind_from_proxy_mesh_7648d', text='Unbind / Refresh', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'refresh.svg')), emboss=True, depress=False)
                    box_B63D8 = col_29EE2.box()
                    box_B63D8.label(text='Proxy Mesh', icon_value=0)
                    row_6ADB2 = box_B63D8.row(heading='', align=True)
                    row_6ADB2.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'rig_proxy_mesh', text='', icon_value=0, emboss=True)
                    if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh == None):
                        pass
                    else:
                        row_E7B4F = row_6ADB2.row(heading='', align=True)
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
                                box_21FC2 = col_73DBB.box()
                                box_21FC2.label(text='Update Settings', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
                                col_4847A = box_21FC2.column(heading='', align=True)
                                col_4847A.label(text='Update Mode', icon_value=0)
                                row_88338 = col_4847A.row(heading='', align=False)
                                row_88338.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_update_mode', text=bpy.context.scene.sna_dgs_scene_properties.rig_update_mode, icon_value=0, emboss=True, expand=True)
                                if bpy.context.scene.sna_dgs_scene_properties.rig_update_mode == "Single":
                                    col_2CAD4 = box_21FC2.column(heading='', align=False)
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
                                    col_DF573.scale_y = 2.0
                                    op = col_DF573.operator('sna.dgs_render_update_bound_3dgs_from_proxy_mesh_951a0', text='Update Single', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg')), emboss=True, depress=False)
                                elif bpy.context.scene.sna_dgs_scene_properties.rig_update_mode == "Interval":
                                    col_6A648 = box_21FC2.column(heading='', align=False)
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
                                            col_55551.scale_y = 2.0
                                            op = col_55551.operator('sna.dgs_render_bake_frames_to_cache_90885', text='Bake Frames to Cache', icon_value=0, emboss=True, depress=False)
                                    else:
                                        col_A92B7 = box_3F9E9.column(heading='', align=False)
                                        col_A92B7.scale_y = 2.0
                                        op = col_A92B7.operator('sna.dgs_render_bake_frames_to_cache_90885', text='Bake Frames to Cache', icon_value=0, emboss=True, depress=False)
                                    if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
                                        if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                                            box_0905C = col_6A648.box()
                                            col_935FA = box_0905C.column(heading='', align=True)
                                            col_935FA.prop(bpy.context.scene.sna_dgs_scene_properties, 'rig_update_interval', text='Update Interval', icon_value=0, emboss=True)
                                            col_16CA7 = col_935FA.column(heading='', align=False)
                                            col_16CA7.scale_y = 2.0
                                            if bpy.context.scene.sna_dgs_scene_properties.rig_interval_stop:
                                                op = col_16CA7.operator('sna.dgs_render_update_bound_3dgs_from_cache_385ec', text='Update from cache', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'play.svg')), emboss=True, depress=False)
                                            else:
                                                col_BE41C = col_16CA7.column(heading='', align=False)
                                                col_BE41C.alert = True
                                                op = col_BE41C.operator('sna.dgs_render_end_proxy_rig_updates_60c6a', text='Stop', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'stop.svg')), emboss=True, depress=False)
                                else:
                                    pass
                                col_73DBB.separator(factor=1.0)
                                if 'proxy_sequence_binding' in bpy.context.view_layer.objects.active:
                                    if bpy.context.view_layer.objects.active['proxy_sequence_binding']:
                                        if 'rig_baked_render_enabled' in bpy.context.view_layer.objects.active:
                                            box_0F4AD = col_73DBB.box()
                                            box_0F4AD.label(text='Rig Render Settings', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
                                            attr_003BE = '["' + str('rig_baked_render_enabled' + '"]') 
                                            box_0F4AD.prop(bpy.context.view_layer.objects.active, attr_003BE, text='Enable rig updates in renders', icon_value=0, emboss=True)
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
                box_958E5.scale_y = 2.0
                box_958E5.label(text='The Active Object is not a 3DGS Mesh', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
