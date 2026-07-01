import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_AddonPreferences_AB8B3(bpy.types.AddonPreferences):
    bl_idname = __package__
    sna_cache_file_directory: bpy.props.StringProperty(name='Cache File Directory', description='', default='', subtype='DIR_PATH', maxlen=0)
    sna_show_tips: bpy.props.BoolProperty(name='Show Tips', description='', default=True)
    sna_use_gpu_sh_rotation: bpy.props.BoolProperty(name='Use GPU for SH rotation during bake', description='Accelerates the spherical-harmonics rotation step of compute_bound_state via a Blender compute shader. Falls back to CPU automatically on failure', default=True)

    def draw(self, context):
        if not (False):
            layout = self.layout 
            box_D84AF = layout.box()
            box_D84AF.alert = False
            box_D84AF.enabled = True
            box_D84AF.active = True
            box_D84AF.use_property_split = False
            box_D84AF.use_property_decorate = False
            box_D84AF.alignment = 'Expand'.upper()
            box_D84AF.scale_x = 1.0
            box_D84AF.scale_y = 1.0
            if not True: box_D84AF.operator_context = "EXEC_DEFAULT"
            box_236E6 = box_D84AF.box()
            box_236E6.alert = False
            box_236E6.enabled = True
            box_236E6.active = True
            box_236E6.use_property_split = False
            box_236E6.use_property_decorate = False
            box_236E6.alignment = 'Expand'.upper()
            box_236E6.scale_x = 1.0
            box_236E6.scale_y = 1.0
            if not True: box_236E6.operator_context = "EXEC_DEFAULT"
            box_236E6.label(text='Cache', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            box_236E6.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_cache_file_directory', text='Cache directory', icon_value=0, emboss=True)
            box_F03E4 = box_236E6.box()
            box_F03E4.alert = False
            box_F03E4.enabled = True
            box_F03E4.active = True
            box_F03E4.use_property_split = False
            box_F03E4.use_property_decorate = False
            box_F03E4.alignment = 'Expand'.upper()
            box_F03E4.scale_x = 1.0
            box_F03E4.scale_y = 1.0
            if not True: box_F03E4.operator_context = "EXEC_DEFAULT"
            box_F03E4.label(text='If cache files are removed or disconnected, it may not be possible to restore the original state', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
            box_F03E4.label(text='of light baked or rig-deformed objects. Try to maintained a stable cache location.', icon_value=0)
            box_24429 = box_D84AF.box()
            box_24429.alert = False
            box_24429.enabled = True
            box_24429.active = True
            box_24429.use_property_split = False
            box_24429.use_property_decorate = False
            box_24429.alignment = 'Expand'.upper()
            box_24429.scale_x = 1.0
            box_24429.scale_y = 1.0
            if not True: box_24429.operator_context = "EXEC_DEFAULT"
            box_24429.label(text='Tips', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
            box_24429.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_show_tips', text='Show tips throughout the interface', icon_value=0, emboss=True)
