import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_move_modifier_index_23126(object, modifier_to_move, to_index):
    for i_64655 in range(len(object.modifiers)):
        if (object.modifiers[i_64655] == object.modifiers[modifier_to_move]):
            bpy.context.view_layer.objects.active.modifiers.move(from_index=i_64655, to_index=to_index, )
            bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
            if bpy.context and bpy.context.screen:
                for a in bpy.context.screen.areas:
                    a.tag_redraw()
