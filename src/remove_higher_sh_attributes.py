import bpy
from .important import *

class SNA_OT_Dgs_Render_Remove_Higher_Sh_Attributes_Cb703(bpy.types.Operator):
    bl_idname = "sna.dgs_render_remove_higher_sh_attributes_cb703"
    bl_label = "3DGS Render: Remove Higher SH Attributes"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        TARGET_OBJECT_NAME = bpy.context.view_layer.objects.active.name
        import bmesh
        # ===== GLOBAL INPUT VARIABLES - EDIT THESE =====
        MODE = "remove_named"  # Options: "remove_active", "remove_selected", "remove_named", "list_attributes"
        #TARGET_OBJECT_NAME = ""  # Only used when MODE = "remove_named" - leave empty to use active object
        VERBOSE_OUTPUT = False    # Set to False for minimal console output
        # Additional f_rest patterns to search for (add your specific naming conventions here)
        CUSTOM_F_REST_PATTERNS = [
            # Add any custom patterns your 3DGS implementation uses
            # Examples: "custom_sh_rest", "features_rest", etc.
        ]
        # ===== SCRIPT FUNCTIONS =====

        def remove_f_rest_attributes(obj: Optional[bpy.types.Object] = None) -> dict:
            """
            Remove SH f_rest attributes from a 3DGS object while keeping other 3DGS attributes.
            Args:
                obj: Target object. If None, uses the active object.
            Returns:
                dict: Summary of removed attributes and operation status
            """
            # Get target object
            if obj is None:
                obj = bpy.context.active_object
            if obj is None:
                return {
                    "success": False,
                    "error": "No object provided and no active object found",
                    "removed_attributes": []
                }
            if obj.type != 'MESH':
                return {
                    "success": False,
                    "error": f"Object '{obj.name}' is not a mesh object",
                    "removed_attributes": []
                }
            mesh = obj.data
            removed_attributes = []
            # Common f_rest attribute naming patterns in 3DGS implementations
            f_rest_patterns = [
                "f_rest",           # Simple naming
                "f_rest_0",         # Indexed naming
                "f_rest_1", 
                "f_rest_2",
                "sh_rest",          # Alternative naming
                "sh_features_rest", # Another common pattern
                "spherical_harmonics_rest",
            ]
            # Add custom patterns from global variables
            f_rest_patterns.extend(CUSTOM_F_REST_PATTERNS)
            # Also check for numbered f_rest attributes (up to reasonable limit)
            for i in range(50):  # Adjust range based on your SH degree
                f_rest_patterns.extend([
                    f"f_rest_{i}",
                    f"sh_rest_{i}",
                    f"f_rest_{i:02d}",  # Zero-padded
                ])
            # Get list of attribute names to check
            attribute_names = list(mesh.attributes.keys())
            # Remove f_rest attributes
            for attr_name in attribute_names:
                # Check if attribute name matches f_rest patterns
                is_f_rest = False
                # Direct pattern matching
                if attr_name in f_rest_patterns:
                    is_f_rest = True
                # Pattern matching for variations
                attr_lower = attr_name.lower()
                if any(pattern in attr_lower for pattern in ["f_rest", "sh_rest", "spherical_harmonics_rest"]):
                    # Additional check to avoid false positives
                    if not any(keep_pattern in attr_lower for keep_pattern in ["f_dc", "position", "scale", "rotation", "opacity"]):
                        is_f_rest = True
                if is_f_rest:
                    try:
                        mesh.attributes.remove(mesh.attributes[attr_name])
                        removed_attributes.append(attr_name)
                        if VERBOSE_OUTPUT:
                            print(f"Removed attribute: {attr_name}")
                    except Exception as e:
                        print(f"Failed to remove attribute '{attr_name}': {e}")
            # Update the mesh
            mesh.update()
            return {
                "success": True,
                "object_name": obj.name,
                "removed_attributes": removed_attributes,
                "remaining_attributes": list(mesh.attributes.keys())
            }

        def remove_f_rest_from_selected() -> None:
            """Remove f_rest attributes from all selected mesh objects."""
            selected_meshes = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
            if not selected_meshes:
                print("No mesh objects selected")
                return
            total_removed = 0
            for obj in selected_meshes:
                result = remove_f_rest_attributes(obj)
                if result["success"]:
                    total_removed += len(result["removed_attributes"])
                    print(f"✓ Processed '{result['object_name']}': removed {len(result['removed_attributes'])} f_rest attributes")
                    if VERBOSE_OUTPUT and result["removed_attributes"]:
                        print(f"  Removed: {', '.join(result['removed_attributes'])}")
                else:
                    print(f"✗ Failed to process '{obj.name}': {result['error']}")
            print(f"\nTotal f_rest attributes removed across all objects: {total_removed}")

        def list_3dgs_attributes(obj: Optional[bpy.types.Object] = None) -> dict:
            """
            List all attributes on an object, categorizing them as 3DGS-related or other.
            Args:
                obj: Target object. If None, uses the active object.
            Returns:
                dict: Categorized attribute information
            """
            if obj is None:
                obj = bpy.context.active_object
            if obj is None or obj.type != 'MESH':
                return {"error": "No valid mesh object"}
            mesh = obj.data
            all_attributes = list(mesh.attributes.keys())
            # Categorize attributes
            f_dc_attrs = [name for name in all_attributes if "f_dc" in name.lower()]
            f_rest_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["f_rest", "sh_rest"])]
            position_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["position", "pos", "xyz"])]
            scale_attrs = [name for name in all_attributes if "scale" in name.lower()]
            rotation_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["rotation", "rot", "quaternion", "quat"])]
            opacity_attrs = [name for name in all_attributes if any(pattern in name.lower() for pattern in ["opacity", "alpha"])]
            known_3dgs = f_dc_attrs + f_rest_attrs + position_attrs + scale_attrs + rotation_attrs + opacity_attrs
            other_attrs = [name for name in all_attributes if name not in known_3dgs]
            return {
                "object_name": obj.name,
                "total_attributes": len(all_attributes),
                "f_dc": f_dc_attrs,
                "f_rest": f_rest_attrs,
                "position": position_attrs,
                "scale": scale_attrs,
                "rotation": rotation_attrs,
                "opacity": opacity_attrs,
                "other": other_attrs
            }
        # ===== MAIN EXECUTION =====
        print("=== 3DGS f_rest Attribute Removal Script ===")
        print(f"Mode: {MODE}")
        if MODE == "remove_active":
            print("Removing f_rest attributes from active object...")
            result = remove_f_rest_attributes()
            if result["success"]:
                print(f"✓ Successfully processed '{result['object_name']}'")
                print(f"Removed {len(result['removed_attributes'])} f_rest attributes")
                if VERBOSE_OUTPUT and result["removed_attributes"]:
                    print(f"Removed attributes: {', '.join(result['removed_attributes'])}")
                if VERBOSE_OUTPUT:
                    print(f"Remaining attributes: {', '.join(result['remaining_attributes'])}")
            else:
                print(f"✗ Error: {result['error']}")
        elif MODE == "remove_selected":
            print("Removing f_rest attributes from all selected objects...")
            remove_f_rest_from_selected()
        elif MODE == "remove_named":
            if not TARGET_OBJECT_NAME:
                print("✗ Error: TARGET_OBJECT_NAME must be specified when using 'remove_named' mode")
            else:
                target_obj = bpy.data.objects.get(TARGET_OBJECT_NAME)
                if target_obj is None:
                    print(f"✗ Error: Object '{TARGET_OBJECT_NAME}' not found")
                else:
                    print(f"Removing f_rest attributes from object '{TARGET_OBJECT_NAME}'...")
                    result = remove_f_rest_attributes(target_obj)
                    if result["success"]:
                        print(f"✓ Successfully processed '{result['object_name']}'")
                        print(f"Removed {len(result['removed_attributes'])} f_rest attributes")
                        if VERBOSE_OUTPUT and result["removed_attributes"]:
                            print(f"Removed attributes: {', '.join(result['removed_attributes'])}")
                        if VERBOSE_OUTPUT:
                            print(f"Remaining attributes: {', '.join(result['remaining_attributes'])}")
                    else:
                        print(f"✗ Error: {result['error']}")
        elif MODE == "list_attributes":
            target_obj = None
            if TARGET_OBJECT_NAME:
                target_obj = bpy.data.objects.get(TARGET_OBJECT_NAME)
                if target_obj is None:
                    print(f"Warning: Object '{TARGET_OBJECT_NAME}' not found, using active object instead")
            print("Listing 3DGS attributes...")
            attr_info = list_3dgs_attributes(target_obj)
            if "error" not in attr_info:
                print(f"\n=== Attribute Summary for '{attr_info['object_name']}' ===")
                print(f"Total attributes: {attr_info['total_attributes']}")
                print(f"f_dc attributes ({len(attr_info['f_dc'])}): {attr_info['f_dc']}")
                print(f"f_rest attributes ({len(attr_info['f_rest'])}): {attr_info['f_rest']}")
                print(f"Position attributes ({len(attr_info['position'])}): {attr_info['position']}")
                print(f"Scale attributes ({len(attr_info['scale'])}): {attr_info['scale']}")
                print(f"Rotation attributes ({len(attr_info['rotation'])}): {attr_info['rotation']}")
                print(f"Opacity attributes ({len(attr_info['opacity'])}): {attr_info['opacity']}")
                print(f"Other attributes ({len(attr_info['other'])}): {attr_info['other']}")
            else:
                print(f"✗ Error: {attr_info['error']}")
        else:
            print(f"✗ Error: Unknown mode '{MODE}'")
            print("Valid modes: 'remove_active', 'remove_selected', 'remove_named', 'list_attributes'")
        print("=== Script Complete ===")
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_DCA59 = layout.box()
        box_DCA59.alert = False
        box_DCA59.enabled = True
        box_DCA59.active = True
        box_DCA59.use_property_split = False
        box_DCA59.use_property_decorate = False
        box_DCA59.alignment = 'Expand'.upper()
        box_DCA59.scale_x = 1.0
        box_DCA59.scale_y = 1.0
        if not True: box_DCA59.operator_context = "EXEC_DEFAULT"
        box_DCA59.label(text='This action is destructive and not reversible', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_DCA59.label(text='Removing higher SH attributes can save memory and increase performance in some areas.', icon_value=0)
        box_DCA59.label(text='If you are unsure about what to do, try working on a duplicate.', icon_value=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)
