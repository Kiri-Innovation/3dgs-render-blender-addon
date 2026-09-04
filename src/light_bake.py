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
        box_923B8.label(text='Cache directory is empty.', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_923B8.label(text='Set it in Preferences', icon_value=0)
    col_3F618 = layout_function.column(heading='', align=True)
    col_3F618.enabled = (bpy.context.preferences.addons[__package__].preferences.sna_cache_file_directory != '')
    if (bpy.context.view_layer.objects.active == None):
        box_C7AE0 = col_3F618.box()
        box_C7AE0.scale_y = 2.0
        box_C7AE0.label(text='No Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    else:
        if '3DGS_Mesh_Type' in bpy.context.view_layer.objects.active:
            col_9A00F = col_3F618.column(heading='', align=False)
            box_18E8E = col_9A00F.box()
            box_18E8E.label(text='Proxy Mesh', icon_value=0)
            row_33E8E = box_18E8E.row(heading='', align=True)
            row_33E8E.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties, 'rig_proxy_mesh', text='', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh == None):
                pass
            else:
                row_BD7EE = row_33E8E.row(heading='', align=True)
                op = row_BD7EE.operator('sna.dgs_render_select_object_b1f49', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'mouse-pointer.svg')), emboss=True, depress=False)
                op.sna_object_name = bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh.name
                row_BD7EE.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh, 'hide_viewport', text='', icon_value=0, emboss=True)
                row_BD7EE.prop(bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh, 'hide_render', text='', icon_value=0, emboss=True)
            if (bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh == None):
                pass
            else:
                col_9A00F.separator(factor=3.0)
                col_DA035 = col_9A00F.column(heading='', align=False)
                row_18A3E = col_DA035.row(heading='', align=False)
                row_18A3E.scale_y = 2.0
                row_18A3E.prop(bpy.context.scene.sna_dgs_scene_properties, 'light_bake_active_menu', text=bpy.context.scene.sna_dgs_scene_properties.light_bake_active_menu, icon_value=0, emboss=True, expand=True)
                if bpy.context.scene.sna_dgs_scene_properties.light_bake_active_menu == "1. Store Light":
                    col_56E5A = col_DA035.column(heading='', align=False)
                    col_56E5A.alert = True
                    if 'proxy_deferred_relight_stage_saved' in bpy.context.view_layer.objects.active:
                        if bpy.context.view_layer.objects.active['proxy_deferred_relight_stage_saved']:
                            box_D56BA = col_56E5A.box()
                            box_D56BA.label(text='Light data has previously been saved', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
                    col_305D8 = col_56E5A.column(heading='', align=False)
                    col_305D8.scale_y = 2.0
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
                col_9B44F = box_82787.column(heading='', align=False)
                col_9B44F.alert = True
                op = col_9B44F.operator('sna.dgs_render_restore_original_light_9a7fe', text='Restore Lighting', icon_value=0, emboss=True, depress=False)
        else:
            box_B787A = col_3F618.box()
            box_B787A.scale_y = 2.0
            box_B787A.label(text='The Active Object is not a 3DGS Mesh', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
