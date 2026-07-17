import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .light_bake_apply import sna_light_bake_apply_A5653
from .light_bake_build import sna_light_bake_build_8B9DD

__package__ = __package__.rsplit('.', 1)[0]


def sna_light_bake_8F346(layout_function, ):
    if (bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory == ''):
        box_923B8 = layout_function.box()
        box_923B8.alert = False
        box_923B8.enabled = True
        box_923B8.active = True
        box_923B8.use_property_split = False
        box_923B8.use_property_decorate = False
        box_923B8.alignment = 'Expand'.upper()
        box_923B8.scale_x = 1.0
        box_923B8.scale_y = 1.0
        if not True: box_923B8.operator_context = "EXEC_DEFAULT"
        box_923B8.label(text='Cache directory is empty.', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_923B8.label(text='Set it in Preferences', icon_value=0)
    col_3F618 = layout_function.column(heading='', align=True)
    col_3F618.alert = False
    col_3F618.enabled = (bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory != '')
    col_3F618.active = True
    col_3F618.use_property_split = False
    col_3F618.use_property_decorate = False
    col_3F618.scale_x = 1.0
    col_3F618.scale_y = 1.0
    col_3F618.alignment = 'Expand'.upper()
    col_3F618.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if (bpy.context.view_layer.objects.active == None):
        box_C7AE0 = col_3F618.box()
        box_C7AE0.alert = False
        box_C7AE0.enabled = True
        box_C7AE0.active = True
        box_C7AE0.use_property_split = False
        box_C7AE0.use_property_decorate = False
        box_C7AE0.alignment = 'Expand'.upper()
        box_C7AE0.scale_x = 1.0
        box_C7AE0.scale_y = 2.0
        if not True: box_C7AE0.operator_context = "EXEC_DEFAULT"
        box_C7AE0.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    else:
        if '3DGS_Mesh_Type' in bpy.context.view_layer.objects.active:
            col_9A00F = col_3F618.column(heading='', align=False)
            col_9A00F.alert = False
            col_9A00F.enabled = True
            col_9A00F.active = True
            col_9A00F.use_property_split = False
            col_9A00F.use_property_decorate = False
            col_9A00F.scale_x = 1.0
            col_9A00F.scale_y = 1.0
            col_9A00F.alignment = 'Expand'.upper()
            col_9A00F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_18E8E = col_9A00F.box()
            box_18E8E.alert = False
            box_18E8E.enabled = True
            box_18E8E.active = True
            box_18E8E.use_property_split = False
            box_18E8E.use_property_decorate = False
            box_18E8E.alignment = 'Expand'.upper()
            box_18E8E.scale_x = 1.0
            box_18E8E.scale_y = 1.0
            if not True: box_18E8E.operator_context = "EXEC_DEFAULT"
            box_18E8E.label(text='Proxy Mesh', icon_value=0)
            row_33E8E = box_18E8E.row(heading='', align=True)
            row_33E8E.alert = False
            row_33E8E.enabled = True
            row_33E8E.active = True
            row_33E8E.use_property_split = False
            row_33E8E.use_property_decorate = False
            row_33E8E.scale_x = 1.0
            row_33E8E.scale_y = 1.0
            row_33E8E.alignment = 'Expand'.upper()
            row_33E8E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_33E8E.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'rig_proxy_mesh', text='', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh == None):
                pass
            else:
                row_BD7EE = row_33E8E.row(heading='', align=True)
                row_BD7EE.alert = False
                row_BD7EE.enabled = True
                row_BD7EE.active = True
                row_BD7EE.use_property_split = False
                row_BD7EE.use_property_decorate = False
                row_BD7EE.scale_x = 1.0
                row_BD7EE.scale_y = 1.0
                row_BD7EE.alignment = 'Expand'.upper()
                row_BD7EE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = row_BD7EE.operator('sna.dgs_render_select_object_b1f49', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'mouse-pointer.svg')), emboss=True, depress=False)
                op.sna_object_name = bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh.name
                row_BD7EE.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh, 'hide_viewport', text='', icon_value=0, emboss=True)
                row_BD7EE.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh, 'hide_render', text='', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh == None):
                pass
            else:
                col_9A00F.separator(factor=3.0)
                col_DA035 = col_9A00F.column(heading='', align=False)
                col_DA035.alert = False
                col_DA035.enabled = True
                col_DA035.active = True
                col_DA035.use_property_split = False
                col_DA035.use_property_decorate = False
                col_DA035.scale_x = 1.0
                col_DA035.scale_y = 1.0
                col_DA035.alignment = 'Expand'.upper()
                col_DA035.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_18A3E = col_DA035.row(heading='', align=False)
                row_18A3E.alert = False
                row_18A3E.enabled = True
                row_18A3E.active = True
                row_18A3E.use_property_split = False
                row_18A3E.use_property_decorate = False
                row_18A3E.scale_x = 1.0
                row_18A3E.scale_y = 2.0
                row_18A3E.alignment = 'Expand'.upper()
                row_18A3E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_18A3E.prop(bpy.context.scene.sna_dgs_scene_properties, 'light_bake_active_menu', text=bpy.context.scene.sna_dgs_scene_properties.light_bake_active_menu, icon_value=0, emboss=True, expand=True)
                if bpy.context.scene.sna_dgs_scene_properties.light_bake_active_menu == "1. Store Light":
                    col_56E5A = col_DA035.column(heading='', align=False)
                    col_56E5A.alert = True
                    col_56E5A.enabled = True
                    col_56E5A.active = True
                    col_56E5A.use_property_split = False
                    col_56E5A.use_property_decorate = False
                    col_56E5A.scale_x = 1.0
                    col_56E5A.scale_y = 1.0
                    col_56E5A.alignment = 'Expand'.upper()
                    col_56E5A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    if 'proxy_deferred_relight_stage_saved' in bpy.context.view_layer.objects.active:
                        if bpy.context.view_layer.objects.active['proxy_deferred_relight_stage_saved']:
                            box_D56BA = col_56E5A.box()
                            box_D56BA.alert = False
                            box_D56BA.enabled = True
                            box_D56BA.active = True
                            box_D56BA.use_property_split = False
                            box_D56BA.use_property_decorate = False
                            box_D56BA.alignment = 'Expand'.upper()
                            box_D56BA.scale_x = 1.0
                            box_D56BA.scale_y = 1.0
                            if not True: box_D56BA.operator_context = "EXEC_DEFAULT"
                            box_D56BA.label(text='Light data has previously been saved', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    col_305D8 = col_56E5A.column(heading='', align=False)
                    col_305D8.alert = False
                    col_305D8.enabled = True
                    col_305D8.active = True
                    col_305D8.use_property_split = False
                    col_305D8.use_property_decorate = False
                    col_305D8.scale_x = 1.0
                    col_305D8.scale_y = 2.0
                    col_305D8.alignment = 'Expand'.upper()
                    col_305D8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    op = col_305D8.operator('sna.dgs_render_store_original_lighting_99939', text='Store Original Lighting', icon_value=0, emboss=True, depress=False)
                elif bpy.context.scene.sna_dgs_scene_properties.light_bake_active_menu == "2. Bake Light":
                    layout_function = col_DA035
                    sna_light_bake_build_8B9DD(layout_function, )
                elif bpy.context.scene.sna_dgs_scene_properties.light_bake_active_menu == "3. Apply Light":
                    layout_function = col_DA035
                    sna_light_bake_apply_A5653(layout_function, )
                else:
                    pass
                box_82787 = col_DA035.box()
                box_82787.alert = False
                box_82787.enabled = True
                box_82787.active = True
                box_82787.use_property_split = False
                box_82787.use_property_decorate = False
                box_82787.alignment = 'Expand'.upper()
                box_82787.scale_x = 1.0
                box_82787.scale_y = 1.0
                if not True: box_82787.operator_context = "EXEC_DEFAULT"
                col_9B44F = box_82787.column(heading='', align=False)
                col_9B44F.alert = True
                col_9B44F.enabled = True
                col_9B44F.active = True
                col_9B44F.use_property_split = False
                col_9B44F.use_property_decorate = False
                col_9B44F.scale_x = 1.0
                col_9B44F.scale_y = 1.0
                col_9B44F.alignment = 'Expand'.upper()
                col_9B44F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = col_9B44F.operator('sna.dgs_render_restore_original_light_9a7fe', text='Restore Lighting', icon_value=0, emboss=True, depress=False)
        else:
            box_B787A = col_3F618.box()
            box_B787A.alert = False
            box_B787A.enabled = True
            box_B787A.active = True
            box_B787A.use_property_split = False
            box_B787A.use_property_decorate = False
            box_B787A.alignment = 'Expand'.upper()
            box_B787A.scale_x = 1.0
            box_B787A.scale_y = 2.0
            if not True: box_B787A.operator_context = "EXEC_DEFAULT"
            box_B787A.label(text='The Active Object is not a 3DGS Mesh', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
