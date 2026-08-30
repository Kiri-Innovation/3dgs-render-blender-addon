import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *
from .append_and_add_geo_nodes_function_execute import sna_append_and_add_geo_nodes_function_execute_6BCD7
from .move_object_to_collection_create_if_missingfunction_execute import sna_move_object_to_collection_create_if_missingfunction_execute_AB682
from .update_camera_single_time import sna_update_camera_single_time_9EF18
from .. import dgs_render__hq_mode

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Generate_Hq_Object_55455(bpy.types.Operator):
    bl_idname = "sna.dgs_render_generate_hq_object_55455"
    bl_label = "3DGS Render: Generate HQ Object"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        dgs_render__hq_mode['sna_lq_object_list'] = []
        for i_3F5D0 in range(len(bpy.data.objects)):
            if (property_exists("bpy.data.objects[i_3F5D0].modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.data.objects[i_3F5D0].modifiers):
                bpy.data.objects[i_3F5D0].sna_dgs_object_properties.cam_update = True
                set_modifier_socket(bpy.data.objects[i_3F5D0].modifiers['KIRI_3DGS_Render_GN'], 'Socket_54', True)

        def delayed_CB67D():
            sna_update_camera_single_time_9EF18()

            def delayed_013E4():
                bpy.data.objects[i_3F5D0].update_tag(refresh={'DATA'}, )
                if bpy.context and bpy.context.screen:
                    for a in bpy.context.screen.areas:
                        a.tag_redraw()
                for i_294E7 in range(len(bpy.context.scene.objects)):
                    if (bpy.context.scene.objects[i_294E7] == None):
                        pass
                    else:
                        if (property_exists("bpy.context.scene.objects[i_294E7].modifiers", globals(), locals()) and 'KIRI_3DGS_Sorter_GN' in bpy.context.scene.objects[i_294E7].modifiers):
                            dgs_render__hq_mode['sna_lq_object_list'].append(bpy.context.scene.objects[i_294E7].name)
                for i_6C743 in range(len(dgs_render__hq_mode['sna_lq_object_list'])):
                    bpy.data.objects[dgs_render__hq_mode['sna_lq_object_list'][i_6C743]].hide_viewport = True
                    bpy.data.objects[dgs_render__hq_mode['sna_lq_object_list'][i_6C743]].hide_render = True
                    sna_move_object_to_collection_create_if_missingfunction_execute_AB682(dgs_render__hq_mode['sna_lq_object_list'][i_6C743], '3DGS_LQ_Objects', 'COLOR_06')
                before_data = list(bpy.data.objects)
                bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V5.blend') + r'\Object', filename='KIRI_HQ_Merged_Object', link=False)
                new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
                appended_D9EAC = None if not new_data else new_data[0]
                sna_move_object_to_collection_create_if_missingfunction_execute_AB682('KIRI_HQ_Merged_Object', '3DGS_HQ_Object', 'COLOR_05')
                sna_append_and_add_geo_nodes_function_execute_6BCD7('KIRI_3DGS_Instance_HQ', 'KIRI_3DGS_Instance_HQ', bpy.data.objects['KIRI_HQ_Merged_Object'])
                set_modifier_socket(bpy.data.objects['KIRI_HQ_Merged_Object'].modifiers['KIRI_3DGS_Instance_HQ'], 'Socket_2', bpy.data.collections['3DGS_LQ_Objects'])
                if property_exists("bpy.data.materials['KIRI_3DGS_Render_Material']", globals(), locals()):
                    pass
                else:
                    before_data = list(bpy.data.materials)
                    bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V5.blend') + r'\Material', filename='KIRI_3DGS_Render_Material', link=False)
                    new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
                    appended_061FB = None if not new_data else new_data[0]
                input_object = bpy.data.objects['KIRI_HQ_Merged_Object']
                material_name = 'KIRI_3DGS_Render_Material'
                # Input Variable Names
                #input_object = None  # Should be set to a bpy.types.Object pointer before running
                #material_name = "KIRI_3DGS_Render_Material"  # Name of the material to assign
                # Check if the input object is provided and is valid
                if not input_object or input_object.type != 'MESH':
                    print("Error: No valid mesh object provided as input.")
                else:
                    # Get the object and its mesh data
                    obj = input_object
                    mesh = obj.data
                    try:
                        # Remove all existing material slots
                        while len(obj.material_slots) > 0:
                            bpy.context.object.active_material_index = 0  # Set to the first slot to remove
                            bpy.ops.object.material_slot_remove()
                        # Check if the material exists; create it if it doesn’t
                        if material_name not in bpy.data.materials:
                            new_material = bpy.data.materials.new(name=material_name)
                            new_material.use_nodes = True  # Enable node-based shading (optional, matching your original script)
                        else:
                            new_material = bpy.data.materials[material_name]
                        # Add the material to the object as a new slot
                        obj.data.materials.append(new_material)
                        print(f"Assigned material '{material_name}' to {obj.name} and removed existing material slots.")
                    except Exception as e:
                        print(f"Error assigning material to {obj.name}: {e}")
                bpy.data.materials['KIRI_3DGS_Render_Material'].surface_render_method = 'BLENDED'
                bpy.data.objects['KIRI_HQ_Merged_Object'].update_tag(refresh={'OBJECT'}, )
                if bpy.context and bpy.context.screen:
                    for a in bpy.context.screen.areas:
                        a.tag_redraw()
            bpy.app.timers.register(delayed_013E4, first_interval=0.10000000149011612)
        bpy.app.timers.register(delayed_CB67D, first_interval=0.10000000149011612)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_B5524 = layout.box()
        box_B5524.label(text="All original 'LQ' objects will be moved into '3DGS_LQ_Objects' collection", icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'warning.svg')))
        box_B5524.label(text="        A new object -'KIRI_HQ_Merged_Object' - will be created", icon_value=0)
        box_B5524.label(text='        Use the LQ / HQ drop down to toggle between original and HQ object visibilities', icon_value=0)
        box_B5524.label(text='        Do not rename the created collections', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)
