import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Apply_Animate_Modifier_3938E(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_animate_modifier_3938e"
    bl_label = "3DGS Render: Apply Animate Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Animate_GN']['Socket_35'] = True
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Animate_GN'
        #import bpy
        # --- VARIABLES ---
        # Replace these with your Serpens inputs or variables
        #object_name = "Cube"      # The name of the object you want to affect
        #modifier_name = "Bevel"   # The name of the modifier to apply/remove
        # --- SCRIPT START ---
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Case 1: Modifier is hidden in viewport -> Remove it directly
                    # This works because .remove() is a data operation, not an operator.
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from '{object_name}'.")
                else:
                    # Case 2: Modifier is visible -> Apply it using an Operator
                    # CONTEXT OVERRIDE EXPLANATION:
                    # bpy.ops usually runs on whatever is selected in the 3D View.
                    # 'temp_override' creates a temporary, isolated environment where 
                    # Blender believes 'obj' is the Active Object, regardless of what 
                    # you actually have selected. 
                    try:
                        # We force the 'object' and 'active_object' context members to be our specific obj
                        with bpy.context.temp_override(object=obj, active_object=obj):
                            # Inside this block, the operator thinks 'obj' is the active selection
                            bpy.ops.object.modifier_apply(modifier=modifier_name)
                        print(f"Applied visible modifier '{modifier_name}' to '{object_name}'.")
                    except Exception as e:
                        print(f"Could not apply modifier. Error: {e}")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
