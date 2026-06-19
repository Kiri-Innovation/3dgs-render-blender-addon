import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_duplicate_object_ED1F0(source_obj_name):
    source_obj_name = source_obj_name
    new_object_name = None
    # Input variables
    #source_obj_name = "Cube"  # Change this to your object's name
    offset_x = 0.0  # Input float variable for X offset
    # Get the source object
    source_obj = bpy.data.objects.get(source_obj_name)
    # Check if the object exists
    if source_obj:
        # Create a copy of the object
        new_obj = source_obj.copy()
        new_obj.data = source_obj.data.copy()
        # Link the new object to the scene
        bpy.context.scene.collection.objects.link(new_obj)
        # Apply the offset if any
        new_obj.location.x += offset_x
        # Clear current selection
        bpy.ops.object.select_all(action='DESELECT')
        # Select and activate the new object
        new_obj.select_set(True)
        bpy.context.view_layer.objects.active = new_obj
        # Store the new object's name in a variable
        new_object_name = new_obj.name
        # Output the new object for Serpens (return the actual object)
        output_object = new_obj
    else:
        new_object_name = "ERROR: Source object not found"
        output_object = None
    # Output the new object's name (this will be captured by Serpens)
    print(new_object_name)
    return new_object_name
