import bpy
from .important import *

class SNA_OT_Dgs_Render_Apply_Convert_To_Rough_Mesh_Modifier_9F4B2(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_convert_to_rough_mesh_modifier_9f4b2"
    bl_label = "3DGS Render: Apply Convert To Rough Mesh Modifier"
    bl_description = "Applies the named modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        object_name = bpy.context.view_layer.objects.active.name
        modifier_name = 'KIRI_3DGS_Convert_To_Rough_Mesh_GN'
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        bpy.context.view_layer.objects.active.update_tag(refresh={'OBJECT'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
