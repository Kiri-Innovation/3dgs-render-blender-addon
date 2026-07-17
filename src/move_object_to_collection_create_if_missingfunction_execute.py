import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_move_object_to_collection_create_if_missingfunction_execute_AB682(Object_to_move, Target_Collection, Collection_Color_Tag):
    if (property_exists("bpy.data.collections", globals(), locals()) and Target_Collection in bpy.data.collections):
        pass
    else:
        collection_CF177 = bpy.data.collections.new(name=Target_Collection, )
        bpy.context.scene.collection.children.link(child=collection_CF177, )
        bpy.data.collections[Target_Collection].color_tag = Collection_Color_Tag
    if (property_exists("bpy.data.collections[Target_Collection].objects", globals(), locals()) and Object_to_move in bpy.data.collections[Target_Collection].objects):
        pass
    else:
        bpy.data.collections[Target_Collection].objects.link(object=bpy.data.objects[Object_to_move], )
    for i_7587C in range(len(bpy.context.scene.collection.children)):
        if (property_exists("bpy.context.scene.collection.children[i_7587C].objects", globals(), locals()) and Object_to_move in bpy.context.scene.collection.children[i_7587C].objects):
            if (bpy.context.scene.collection.children[i_7587C].name == Target_Collection):
                pass
            else:
                bpy.context.scene.collection.children[i_7587C].objects.unlink(object=bpy.data.objects[Object_to_move], )
    if (property_exists("bpy.context.scene.collection.objects", globals(), locals()) and Object_to_move in bpy.context.scene.collection.objects):
        bpy.context.scene.collection.objects.unlink(object=bpy.data.objects[Object_to_move], )
