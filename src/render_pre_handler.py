import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def render_pre_handler_77179(dummy):
    for i_55361 in range(len(bpy.context.scene.objects)):
        if (property_exists("bpy.context.scene.objects[i_55361].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.scene.objects[i_55361].modifiers):
            bpy.context.scene.objects[i_55361].modifiers['KIRI_3DGS_Render_GN']['Socket_34'] = bpy.context.scene.render.resolution_x
            bpy.context.scene.objects[i_55361].modifiers['KIRI_3DGS_Render_GN']['Socket_35'] = bpy.context.scene.render.resolution_y
            bpy.context.scene.objects[i_55361].update_tag(refresh={'OBJECT'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()
