import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Apply_Modifier_0F5F2(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_modifier_0f5f2"
    bl_label = "3DGS Render: Apply Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}
    sna_target_object: bpy.props.StringProperty(name='Target Object', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)
    sna_target_modifier: bpy.props.StringProperty(name='Target Modifier', description='', options={'HIDDEN'}, default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        object_name = self.sna_target_object
        modifier_name = self.sna_target_modifier
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
