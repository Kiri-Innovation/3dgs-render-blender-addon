import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .realtime_relighting import world_lighting_requires_initial_analysis

__package__ = __package__.rsplit('.', 1)[0]


def sna_r2_render_menu_7AD0F(layout_function, ):
    box_3D205 = layout_function.box()
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_sh_degree', text='SH Degrees', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_animation', text='Render Animation', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_color', text='Export Color Pass', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_depth', text='Export Depth Pass', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_comp', text='Combine With Native Render', icon_value=0, emboss=True)
    box_3D205.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_delete_temp_files', text='Delete Temp Files', icon_value=0, emboss=True)
    relight_box = box_3D205.box()
    relight_box.label(text='Realtime Relighting')
    relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight', text='Use Blender Lights (Up to 16)')
    if bpy.context.scene.sna_dgs_scene_properties.r2_relight:
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_mode', text='Appearance')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_response', text='Light Response')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_strength', text='Direct Strength')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_ambient', text='Ambient')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_relight_ambient_strength', text='Ambient Strength')
        if bpy.context.scene.sna_dgs_scene_properties.r2_world_lighting:
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_world_lighting', text='Use World / HDRI (Diffuse)')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_world_strength', text='World Strength')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_world_response', text='World Shading')
        else:
            relight_box.operator(
                'sna.dgs_render_enable_world_lighting_94c2a',
                text='Use World / HDRI (Diffuse)',
                icon='CHECKBOX_DEHLT',
            )
            if world_lighting_requires_initial_analysis(bpy.context.scene):
                world_warning = relight_box.row()
                world_warning.label(text='First use of a new HDRI may take time to prepare', icon='INFO')
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadows', text='Cached Shadows (Mesh to GS)')
        if bpy.context.scene.sna_dgs_scene_properties.r2_shadows:
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_gaussian_self_shadows', text='GS Self-Shadows (Experimental)')
            relight_box.prop_search(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_light', bpy.data, 'objects', text='Shadow Light')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_light_limit', text='Shadow Lights')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_update_mode', text='Animation Update')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_resolution', text='Resolution per Face')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_bias', text='Bias')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_normal_bias', text='Normal Bias')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_filter_radius', text='Filter Radius')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_density', text='Shadow Density')
            relight_box.operator('sna.dgs_render_refresh_shadows_16f2b')
            shadow_status = getattr(bpy, 'dgs_shadow_cache_status', None)
            if shadow_status:
                relight_box.label(text=f"Cached: {shadow_status['total']} lights, rebuilt {shadow_status['rebuilt']} at frame {shadow_status['frame']}")
        relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_proxy', text='GS to Mesh Shadows (Eevee)')
        if bpy.context.scene.sna_dgs_scene_properties.r2_shadow_proxy or bpy.context.scene.sna_dgs_scene_properties.r2_gaussian_self_shadows:
            eevee_settings = getattr(bpy.context.scene, 'eevee', None)
            if bpy.context.scene.sna_dgs_scene_properties.r2_shadow_proxy and eevee_settings is not None and not eevee_settings.use_shadows:
                warning_row = relight_box.row()
                warning_row.alert = True
                warning_row.label(text='Eevee Shadows are disabled; rebuild to enable them', icon='ERROR')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_proxy_limit', text='Total Max Cards')
            relight_box.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_shadow_proxy_cutoff', text='Alpha Cutoff')
            relight_box.operator('sna.dgs_render_build_shadow_proxies_5b787', text='Rebuild Gaussian Shadow Proxies')
    split_A5CFC = box_3D205.split(factor=0.5, align=False)
    split_A5CFC.label(text='Rig Behaviour', icon_value=0)
    split_A5CFC.prop(bpy.context.scene.sna_dgs_scene_properties, 'r2_render_rig_cache_mode', text='', icon_value=0, emboss=True)
    col_A8B0F = box_3D205.column(heading='', align=False)
    col_A8B0F.enabled = ((bpy.context.scene.camera != None) and (bpy.context.scene.render.filepath != '') and (bpy.context.scene.render.image_settings.media_type == 'IMAGE') and (bpy.context.scene.sna_dgs_scene_properties.r2_color or bpy.context.scene.sna_dgs_scene_properties.r2_depth))
    col_A8B0F.scale_y = 2.0
    op = col_A8B0F.operator('sna.dgs_render_advanced_render_147af', text='Render', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'camera.svg')), emboss=True, depress=False)
    op = box_3D205.operator('sna.dgs_render_open_output_folder_82000', text='Open Output Folder', icon_value=0, emboss=True, depress=False)
    op.sna_path = os.path.dirname(bpy.context.scene.render.filepath)
    if (bpy.context.scene.camera == None):
        box_3CB16 = box_3D205.box()
        box_3CB16.label(text='No Active Camera found in Scene', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    if (bpy.context.scene.render.filepath == ''):
        box_A1F25 = box_3D205.box()
        box_A1F25.label(text='Output path is empty', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    if (bpy.context.scene.render.image_settings.media_type == 'IMAGE'):
        pass
    else:
        box_7936D = box_3D205.box()
        box_7936D.label(text='Set the output Media Type to Image', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
    if (bpy.context.scene.sna_dgs_scene_properties.r2_color or bpy.context.scene.sna_dgs_scene_properties.r2_depth):
        pass
    else:
        box_3B948 = box_3D205.box()
        box_3B948.label(text='No passes enabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
