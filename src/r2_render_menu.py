import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_r2_render_menu_7AD0F(layout_function, ):
    box_3D205 = layout_function.box()
    box_3D205.alert = False
    box_3D205.enabled = True
    box_3D205.active = True
    box_3D205.use_property_split = False
    box_3D205.use_property_decorate = False
    box_3D205.alignment = 'Expand'.upper()
    box_3D205.scale_x = 1.0
    box_3D205.scale_y = 1.0
    if not True: box_3D205.operator_context = "EXEC_DEFAULT"
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_sh_degree', text='SH Degrees', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_animation', text='Render Animation', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_color', text='Export Color Pass', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_depth', text='Export Depth Pass', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_comp', text='Combine With Native Render', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_delete_temp_files', text='Delete Temp Files', icon_value=0, emboss=True)
    relight_box = box_3D205.box()
    relight_box.label(text='Realtime Relighting')
    relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight', text='Use Blender Lights')
    if bpy.context.scene.sna_dgs_scene_properties.r2_relight:
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_mode', text='Appearance')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_response', text='Light Response')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_strength', text='Direct Strength')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_ambient', text='Ambient')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_ambient_strength', text='Ambient Strength')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadows', text='Cached Mesh Shadows')
        if bpy.context.scene.sna_dgs_scene_properties.r2_shadows:
            relight_box.prop_search(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_light', bpy.data, 'objects', text='Shadow Light')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_light_limit', text='Shadow Lights')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_update_mode', text='Animation Update')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_resolution', text='Resolution')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_bias', text='Bias')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_normal_bias', text='Normal Bias')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_filter_radius', text='Filter Radius')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_density', text='Shadow Density')
            relight_box.operator('sna.dgs_render_refresh_shadows_16f2b')
            shadow_status = getattr(bpy, 'dgs_shadow_cache_status', None)
            if shadow_status:
                relight_box.label(text=f"Cached: {shadow_status['total']} lights, rebuilt {shadow_status['rebuilt']} at frame {shadow_status['frame']}")
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_proxy', text='Eevee Shadow Proxies')
        if bpy.context.scene.sna_dgs_scene_properties.r2_shadow_proxy:
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_proxy_limit', text='Max Cards')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_proxy_cutoff', text='Alpha Cutoff')
            relight_box.operator('sna.dgs_render_build_shadow_proxies_5b787')
    split_A5CFC = box_3D205.split(factor=0.5, align=False)
    split_A5CFC.alert = False
    split_A5CFC.enabled = True
    split_A5CFC.active = True
    split_A5CFC.use_property_split = False
    split_A5CFC.use_property_decorate = False
    split_A5CFC.scale_x = 1.0
    split_A5CFC.scale_y = 1.0
    split_A5CFC.alignment = 'Expand'.upper()
    if not True: split_A5CFC.operator_context = "EXEC_DEFAULT"
    split_A5CFC.label(text='Rig Behaviour', icon_value=0)
    split_A5CFC.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_render_rig_cache_mode', text='', icon_value=0, emboss=True)
    col_A8B0F = box_3D205.column(heading='', align=False)
    col_A8B0F.alert = False
    col_A8B0F.enabled = ((bpy.context.scene.camera != None) and (bpy.context.scene.render.filepath != '') and (bpy.context.scene.render.image_settings.media_type == 'IMAGE') and (bpy.context.scene.sna_dgs_scene_properties.r2_color or bpy.context.scene.sna_dgs_scene_properties.r2_depth))
    col_A8B0F.active = True
    col_A8B0F.use_property_split = False
    col_A8B0F.use_property_decorate = False
    col_A8B0F.scale_x = 1.0
    col_A8B0F.scale_y = 2.0
    col_A8B0F.alignment = 'Expand'.upper()
    col_A8B0F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_A8B0F.operator('sna.dgs_render_advanced_render_147af', text='Render', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera.svg')), emboss=True, depress=False)
    op = box_3D205.operator('sna.dgs_render_open_output_folder_82000', text='Open Output Folder', icon_value=0, emboss=True, depress=False)
    op.sna_path = os.path.dirname(bpy.context.scene.render.filepath)
    if (bpy.context.scene.camera == None):
        box_3CB16 = box_3D205.box()
        box_3CB16.alert = False
        box_3CB16.enabled = True
        box_3CB16.active = True
        box_3CB16.use_property_split = False
        box_3CB16.use_property_decorate = False
        box_3CB16.alignment = 'Expand'.upper()
        box_3CB16.scale_x = 1.0
        box_3CB16.scale_y = 1.0
        if not True: box_3CB16.operator_context = "EXEC_DEFAULT"
        box_3CB16.label(text='No Active Camera found in Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    if (bpy.context.scene.render.filepath == ''):
        box_A1F25 = box_3D205.box()
        box_A1F25.alert = False
        box_A1F25.enabled = True
        box_A1F25.active = True
        box_A1F25.use_property_split = False
        box_A1F25.use_property_decorate = False
        box_A1F25.alignment = 'Expand'.upper()
        box_A1F25.scale_x = 1.0
        box_A1F25.scale_y = 1.0
        if not True: box_A1F25.operator_context = "EXEC_DEFAULT"
        box_A1F25.label(text='Output path is empty', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    if (bpy.context.scene.render.image_settings.media_type == 'IMAGE'):
        pass
    else:
        box_7936D = box_3D205.box()
        box_7936D.alert = False
        box_7936D.enabled = True
        box_7936D.active = True
        box_7936D.use_property_split = False
        box_7936D.use_property_decorate = False
        box_7936D.alignment = 'Expand'.upper()
        box_7936D.scale_x = 1.0
        box_7936D.scale_y = 1.0
        if not True: box_7936D.operator_context = "EXEC_DEFAULT"
        box_7936D.label(text='Set the output Media Type to Image', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    if (bpy.context.scene.sna_dgs_scene_properties.r2_color or bpy.context.scene.sna_dgs_scene_properties.r2_depth):
        pass
    else:
        box_3B948 = box_3D205.box()
        box_3B948.alert = False
        box_3B948.enabled = True
        box_3B948.active = True
        box_3B948.use_property_split = False
        box_3B948.use_property_decorate = False
        box_3B948.alignment = 'Expand'.upper()
        box_3B948.scale_x = 1.0
        box_3B948.scale_y = 1.0
        if not True: box_3B948.operator_context = "EXEC_DEFAULT"
        box_3B948.label(text='No passes enabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
