import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Select_Proxy_Mesh_E76B7(bpy.types.Operator):
    bl_idname = "sna.dgs_render_select_proxy_mesh_e76b7"
    bl_label = "3DGS Render: Select Proxy Mesh"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        input_object = bpy.context.view_layer.objects.active.sna_dgs_object_properties.rig_proxy_mesh
        # --- Input Variables (For testing or Serpens integration) ---
        #input_object = bpy.context.object  # The target object
        deselect_all_first = True          # Clear selection before starting?
        make_active = True                 # NEW: Toggle between just selecting or selecting + activating
        # --- Output Variables ---
        success = False
        error_message = ""

        def safe_deselect_all():
            try:
                view_layer = bpy.context.view_layer
                for obj in bpy.context.selected_objects[:]:
                    if obj.name in view_layer.objects:
                        obj.select_set(False)
                # Only clear active if we actually want to reset everything
                if view_layer.objects.active:
                    view_layer.objects.active = None
                return True, ""
            except Exception as e:
                return False, f"Deselect error: {str(e)}"

        def select_object_logic(obj, should_activate):
            if not obj:
                return False, "No object provided"
            try:
                view_layer = bpy.context.view_layer
                if obj.name not in view_layer.objects:
                    return False, f"Object '{obj.name}' not in current view layer"
                # 1. Unhide Object
                if obj.hide_viewport:
                    obj.hide_viewport = False
                view_layer_obj = view_layer.objects[obj.name]
                if view_layer_obj.hide_get():
                    view_layer_obj.hide_set(False)
                # 2. Unhide Direct Parent Collections
                for col in obj.users_collection:
                    if col.hide_viewport:
                        col.hide_viewport = False
                # 3. Select 
                view_layer_obj.select_set(True)
                # 4. Conditionally Activate
                if should_activate:
                    view_layer.objects.active = view_layer_obj
                    msg = f"Selected and activated {obj.name}"
                else:
                    msg = f"Selected {obj.name} (Active object remains {view_layer.objects.active})"
                return True, msg
            except Exception as e:
                return False, f"Selection error: {str(e)}"
        # --- Execution Logic ---
        # 1. Handle Deselection
        if deselect_all_first:
            success, error_message = safe_deselect_all()
        else:
            success = True # Skip deselect, proceed to selection
        # 2. Handle Selection
        if success:
            if input_object:
                success, error_message = select_object_logic(input_object, make_active)
            else:
                success = False
                error_message = "No input object provided"
        print(f"Result -> Success: {success}, Message: {error_message}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
