import bpy
import os

class SNA_OT_Dgs_Render_Append_Rough_Mesh_Modifier_65Da3(bpy.types.Operator):
    bl_idname = "sna.dgs_render_append_rough_mesh_modifier_65da3"
    bl_label = "3DGS Render: Append Rough Mesh Modifier"
    bl_description = "Adds a Rough Mesh modifier to the active object."
    bl_options = {"REGISTER", "UNDO"}
    sna_create_duplicate_and_remove_other_modifiers: bpy.props.BoolProperty(name='Create duplicate and remove other modifiers', description='', options={'HIDDEN'}, default=True)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.view_layer.objects.active.type == 'MESH' or bpy.context.view_layer.objects.active.type == 'CURVE'):
            if self.sna_create_duplicate_and_remove_other_modifiers:
                source_obj_name = bpy.context.view_layer.objects.active.name
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
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
                    bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
                    object_name = bpy.context.view_layer.objects.active.name
                    # Replace this with your object's name
                    #object_name = "YourObjectName"
                    # Get the object
                    obj = bpy.data.objects.get(object_name)
                    if obj:
                        # Make sure the object is selected and active
                        bpy.context.view_layer.objects.active = obj
                        obj.select_set(True)
                        # Apply all modifiers
                        for modifier in obj.modifiers[:]:  # [:] creates a copy of the list to avoid modification issues
                            try:
                                bpy.ops.object.modifier_apply(modifier=modifier.name)
                                print(f"Applied modifier: {modifier.name}")
                            except Exception as e:
                                print(f"Failed to apply modifier {modifier.name}: {str(e)}")
                    else:
                        print(f"Object '{object_name}' not found")
            else:
                if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
                    bpy.context.view_layer.objects.active.modifiers['KIRI_3DGS_Render_GN']['Socket_50'] = 1
                    bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
            created_modifier_0_827c5 = sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Convert_To_Rough_Mesh_GN', 'KIRI_3DGS_Convert_To_Rough_Mesh_GN', bpy.context.view_layer.objects.active)
            for i_1EB8C in range(len(bpy.context.view_layer.objects.active.modifiers)):
                if (bpy.context.view_layer.objects.active.modifiers[i_1EB8C] == created_modifier_0_827c5):
                    bpy.context.view_layer.objects.active.modifiers.move(from_index=i_1EB8C, to_index=0, )
                    bpy.context.view_layer.objects.active.update_tag(refresh={'DATA'}, )
                    if bpy.context and bpy.context.screen:
                        for a in bpy.context.screen.areas:
                            a.tag_redraw()
        else:
            self.report({'INFO'}, message='The Active Object is not a mesh or curve object.')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_F6B46 = layout.box()
        box_F6B46.alert = False
        box_F6B46.enabled = True
        box_F6B46.active = True
        box_F6B46.use_property_split = False
        box_F6B46.use_property_decorate = False
        box_F6B46.alignment = 'Expand'.upper()
        box_F6B46.scale_x = 1.0
        box_F6B46.scale_y = 1.0
        if not True: box_F6B46.operator_context = "EXEC_DEFAULT"
        box_F6B46.prop(self, 'sna_create_duplicate_and_remove_other_modifiers', text='Create duplicate and remove other modifiers', icon_value=0, emboss=True)
        box_F6B46.label(text='The 3DGS Render modifier will have Camera Updates disabled', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'tips-one.svg')))

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
