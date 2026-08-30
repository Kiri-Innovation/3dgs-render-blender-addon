import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_and_add_geo_nodes_function_execute import sna_append_and_add_geo_nodes_function_execute_6BCD7
from .duplicate_object import sna_duplicate_object_ED1F0
from .move_modifier_index import sna_move_modifier_index_23126

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Append_Rough_Mesh_Modifier_65Da3(bpy.types.Operator):
    bl_idname = "sna.dgs_render_append_rough_mesh_modifier_65da3"
    bl_label = "3DGS Render: Append Rough Mesh Modifier"
    bl_description = "Adds a Rough Mesh modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}
    sna_create_duplicate: bpy.props.BoolProperty(name='Create Duplicate', description='', options={'HIDDEN'}, default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        if (bpy.context.view_layer.objects.active.type == 'MESH' or bpy.context.view_layer.objects.active.type == 'CURVE'):
            if self.sna_create_duplicate:
                new_object_name_0_e557e = sna_duplicate_object_ED1F0(bpy.context.view_layer.objects.active.name)
                if (property_exists("bpy.data.objects[new_object_name_0_e557e].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.data.objects[new_object_name_0_e557e].modifiers):
                    set_modifier_socket(bpy.data.objects[new_object_name_0_e557e].modifiers['KIRI_3DGS_Render_GN'], 'Socket_50', 1)
                    bpy.data.objects[new_object_name_0_e557e].update_tag(refresh={'DATA'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
                    object_name = new_object_name_0_e557e
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
                    created_modifier_0_827c5 = sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Convert_To_Rough_Mesh_GN', 'KIRI_3DGS_Convert_To_Rough_Mesh_GN', bpy.data.objects[new_object_name_0_e557e])
                    if '3DGS_Mesh_Type' in bpy.data.objects[new_object_name_0_e557e]:
                        object_name = new_object_name_0_e557e
                        property_name = '3DGS_Mesh_Type'
                        # Replace these with your object and property names
                        #object_name = "Cube"
                        #property_name = "my_custom_prop"
                        # Get the object
                        obj = bpy.data.objects.get(object_name)
                        if obj is None:
                            print(f"Error: Object '{object_name}' not found in the scene")
                        else:
                            if property_name in obj:
                                del obj[property_name]
                                print(f"Removed property '{property_name}' from object '{object_name}'")
                            else:
                                print(f"Property '{property_name}' not found on object '{object_name}'")
                    if 'gaussian_source_uuid' in bpy.data.objects[new_object_name_0_e557e]:
                        object_name = new_object_name_0_e557e
                        property_name = 'gaussian_source_uuid'
                        # Replace these with your object and property names
                        #object_name = "Cube"
                        #property_name = "my_custom_prop"
                        # Get the object
                        obj = bpy.data.objects.get(object_name)
                        if obj is None:
                            print(f"Error: Object '{object_name}' not found in the scene")
                        else:
                            if property_name in obj:
                                del obj[property_name]
                                print(f"Removed property '{property_name}' from object '{object_name}'")
                            else:
                                print(f"Property '{property_name}' not found on object '{object_name}'")
                    if 'proxy_binding_proxy_uuid' in bpy.data.objects[new_object_name_0_e557e]:
                        object_name = new_object_name_0_e557e
                        property_name = 'proxy_binding_proxy_uuid'
                        # Replace these with your object and property names
                        #object_name = "Cube"
                        #property_name = "my_custom_prop"
                        # Get the object
                        obj = bpy.data.objects.get(object_name)
                        if obj is None:
                            print(f"Error: Object '{object_name}' not found in the scene")
                        else:
                            if property_name in obj:
                                del obj[property_name]
                                print(f"Removed property '{property_name}' from object '{object_name}'")
                            else:
                                print(f"Property '{property_name}' not found on object '{object_name}'")
                    bpy.data.objects[new_object_name_0_e557e].update_tag(refresh={'DATA'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
            else:
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                    set_modifier_socket(bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN'], 'Socket_50', 1)
                    bpy.context.view_layer.objects.active.sna_dgs_object_properties.update_mode = 'Disable Camera Updates'
                created_modifier_0_174bb = sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Convert_To_Rough_Mesh_GN', 'KIRI_3DGS_Convert_To_Rough_Mesh_GN', bpy.context.view_layer.objects.active)
                sna_move_modifier_index_23126(bpy.context.view_layer.objects.active, 'KIRI_3DGS_Convert_To_Rough_Mesh_GN', 0)
        else:
            self.report({'INFO'}, message='The Active Object is not a mesh or curve object.')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_48B99 = layout.box()
        box_48B99.label(text='Objects imported as Verts will produce smoother meshes', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_F6B46 = layout.box()
        box_F6B46.prop(self, 'sna_create_duplicate', text='Create a duplicate object', icon_value=0, emboss=True)
        if self.sna_create_duplicate:
            pass
        else:
            box_F6B46.label(text='The 3DGS Render modifier will have Camera Updates disabled', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
