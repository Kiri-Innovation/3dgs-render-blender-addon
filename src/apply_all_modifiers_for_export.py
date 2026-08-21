import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_apply_all_modifiers_for_export_B90C0(Target_Object):
    if (property_exists("bpy.data.objects[Target_Object].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.data.objects[Target_Object].modifiers):
        set_modifier_socket(bpy.data.objects[Target_Object].modifiers['KIRI_3DGS_Render_GN'], 'Socket_50', 1)
    if (property_exists("bpy.data.objects[Target_Object].modifiers", globals(), locals()) and 'KIRI_3DGS_Animate_GN' in bpy.data.objects[Target_Object].modifiers):
        if bpy.data.objects[Target_Object].modifiers['KIRI_3DGS_Animate_GN'].show_viewport:
            if ((bpy.data.objects[Target_Object].modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 1) or (bpy.data.objects[Target_Object].modifiers['KIRI_3DGS_Animate_GN']['Socket_26'] == 2)):
                set_modifier_socket(bpy.data.objects[Target_Object].modifiers['KIRI_3DGS_Animate_GN'], 'Socket_26', 0)
    bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()
    object_name = Target_Object
    # Replace this with your Serpens input or variable
    # object_name = "Cube"
    obj = bpy.data.objects.get(object_name)
    if obj:
        # 1. Store the NAMES as plain strings, not the RNA structs
        modifier_names = [m.name for m in obj.modifiers] 
        for mod_name in modifier_names: 
            # 2. Fetch a fresh, live reference to the modifier on each iteration
            modifier = obj.modifiers.get(mod_name)
            # Failsafe in case a modifier was destroyed by a previous operation
            if not modifier:
                continue 
            if not modifier.show_viewport:
                # Safely remove hidden modifiers via data operation
                obj.modifiers.remove(modifier)
                print(f"Removed hidden modifier: {mod_name}")
            else:
                # Apply visible modifiers using an isolated context override
                try:
                    with bpy.context.temp_override(object=obj, active_object=obj):
                        bpy.ops.object.modifier_apply(modifier=mod_name)
                    print(f"Applied visible modifier: {mod_name}")
                except Exception as e:
                    print(f"Failed to apply modifier '{mod_name}'. Error: {e}")
    else:
        print(f"Object '{object_name}' not found.")
