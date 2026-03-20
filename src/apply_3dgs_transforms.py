import bpy

class SNA_OT_Dgs_Render_Apply_3Dgs_Tranforms_5B665(bpy.types.Operator):
    bl_idname = "sna.dgs_render_apply_3dgs_tranforms_5b665"
    bl_label = "3DGS Render: Apply 3DGS Tranforms"
    bl_description = "Applies the 3DGS Render modifier if present, makes colour edits permanent and updates 3DGS rotation and scale values"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Render_GN' in bpy.context.view_layer.objects.active.modifiers):
            modifier_name = 'KIRI_3DGS_Render_GN'
            object_name = bpy.context.view_layer.objects.active.name
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
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_3DGS_Adjust_Colour_And_Material' in bpy.context.view_layer.objects.active.modifiers):
            modifier_name = 'KIRI_3DGS_Adjust_Colour_And_Material'
            object_name = bpy.context.view_layer.objects.active.name
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
        APPLY_SCALE = True
        APPLY_ROTATION = True
        TRANSFORM_ORDER = 'ROTATION_FIRST'
        import numpy as np
        from mathutils import Quaternion, Matrix, Euler
        #------ INPUT VARIABLES (modify these) ------#
        # The attributes to update
        SCALE_ATTRIBUTES = ["scale_0", "scale_1", "scale_2"]
        ROTATION_ATTRIBUTES = ["rot_0", "rot_1", "rot_2", "rot_3"]
        # Whether to apply transformations after updating attributes
        #APPLY_SCALE = True
        #APPLY_ROTATION = True
        # The order of operations: either "SCALE_FIRST" or "ROTATION_FIRST"
        # 3DGS typically uses SCALE_FIRST (scale, then rotate)
        #TRANSFORM_ORDER = "SCALE_FIRST"
        # Whether to print debug information
        VERBOSE = True
        # Whether to normalize quaternions after transformation (PostShot does this)
        NORMALIZE_QUATERNIONS = True
        #------------------------------------------#

        def quaternion_multiply(q1, q2):
            """
            Multiply two quaternions (compose rotations)
            q1 and q2 are in form [w, x, y, z]
            """
            w1, x1, y1, z1 = q1
            w2, x2, y2, z2 = q2
            w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
            x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
            y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
            z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
            return [w, x, y, z]

        def normalize_quaternion(q):
            """
            Normalize a quaternion to unit length
            q is in form [w, x, y, z]
            """
            magnitude = math.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)
            if magnitude > 0.00001:  # Avoid division by near-zero
                return [q[0]/magnitude, q[1]/magnitude, q[2]/magnitude, q[3]/magnitude]
            else:
                return [1.0, 0.0, 0.0, 0.0]  # Default to identity quaternion

        def update_scale_attributes(obj, scale_attributes, log_scale_factors, verbose=False):
            """
            Update the scale attributes with logarithmic scale factors
            """
            success = True
            for attr_idx, attr_name in enumerate(scale_attributes):
                if attr_name not in obj.data.attributes:
                    print(f"Attribute '{attr_name}' not found on object.")
                    success = False
                    continue
                attr = obj.data.attributes[attr_name]
                if verbose:
                    print(f"\nUpdating attribute: {attr_name}")
                    print(f"Data type: {attr.data_type}")
                    print(f"Domain: {attr.domain}")
                    print(f"Length: {len(attr.data)}")
                # Determine which scale factor to use based on attribute name
                if attr_name == "scale_0":
                    log_scale = log_scale_factors[0]
                elif attr_name == "scale_1":
                    log_scale = log_scale_factors[1]
                elif attr_name == "scale_2":
                    log_scale = log_scale_factors[2]
                else:
                    # For custom-named attributes, use the index in the scale_attributes list
                    log_scale = log_scale_factors[min(attr_idx, 2)]
                if verbose:
                    print(f"Using log scale factor: {log_scale}")
                # Update the attribute values
                if attr.data_type == 'FLOAT':
                    # Sample a few values before and after for verification
                    sample_size = min(5, len(attr.data))
                    before_values = []
                    for i in range(sample_size):
                        before_values.append(attr.data[i].value)
                    # Update all values
                    for i in range(len(attr.data)):
                        # In 3DGS, adding the log of the scale factor to the log-space scale value
                        attr.data[i].value += log_scale
                    # Print sample values after update
                    if verbose:
                        print("Sample values before and after update:")
                        for i in range(sample_size):
                            print(f"  [{i}]: {before_values[i]} -> {attr.data[i].value}")
                else:
                    print(f"Attribute '{attr_name}' is not of type FLOAT (found {attr.data_type}). Skipping.")
                    success = False
            return success

        def update_rotation_attributes(obj, rotation_attributes, blender_quat, verbose=False, normalize=True):
            """
            Update the rotation attributes with the object's rotation quaternion
            """
            # First, gather all data to avoid processing incomplete sets
            attribute_data = {}
            valid_attributes = True
            for attr_name in rotation_attributes:
                if attr_name not in obj.data.attributes:
                    print(f"Attribute '{attr_name}' not found on object.")
                    valid_attributes = False
                    break
                attr = obj.data.attributes[attr_name]
                if attr.data_type != 'FLOAT':
                    print(f"Attribute '{attr_name}' is not of type FLOAT (found {attr.data_type}). Skipping.")
                    valid_attributes = False
                    break
                # Store the attribute for processing
                attribute_data[attr_name] = attr
            if not valid_attributes:
                print("Unable to process rotation due to missing or invalid attributes.")
                return False
            # Sample a few values before the update for verification
            sample_size = min(5, len(attribute_data[rotation_attributes[0]].data))
            before_values = {attr_name: [] for attr_name in rotation_attributes}
            for attr_name in rotation_attributes:
                for i in range(sample_size):
                    before_values[attr_name].append(attribute_data[attr_name].data[i].value)
            # Process all points
            num_points = len(attribute_data[rotation_attributes[0]].data)
            print(f"Processing {num_points} points...")
            for i in range(num_points):
                # Get current quaternion values [w, x, y, z]
                point_quat = [
                    attribute_data[rotation_attributes[0]].data[i].value,  # w
                    attribute_data[rotation_attributes[1]].data[i].value,  # x
                    attribute_data[rotation_attributes[2]].data[i].value,  # y
                    attribute_data[rotation_attributes[3]].data[i].value   # z
                ]
                # Apply rotation by multiplying quaternions
                # The order matters: PostShot appears to use the object_rotation * point_quat
                # format (rotating the local frame)
                new_quat = quaternion_multiply(blender_quat, point_quat)
                # Normalize the quaternion if requested (PostShot does this)
                if normalize:
                    new_quat = normalize_quaternion(new_quat)
                # Enforce positive w component to match PostShot's convention
                # Since q and -q represent the same rotation, we can flip all signs if w is negative
                if new_quat[0] < 0:
                    new_quat = [-q for q in new_quat]
                # Update attribute values
                attribute_data[rotation_attributes[0]].data[i].value = new_quat[0]  # w
                attribute_data[rotation_attributes[1]].data[i].value = new_quat[1]  # x
                attribute_data[rotation_attributes[2]].data[i].value = new_quat[2]  # y
                attribute_data[rotation_attributes[3]].data[i].value = new_quat[3]  # z
            # Print sample values after update for verification
            if verbose:
                print("\nSample values before and after update:")
                for i in range(sample_size):
                    print(f"Point [{i}]:")
                    for j, attr_name in enumerate(rotation_attributes):
                        print(f"  {attr_name}: {before_values[attr_name][i]} -> {attribute_data[attr_name].data[i].value}")
            return True

        def apply_transformations(obj, apply_rotation=False, apply_scale=False):
            """
            Apply the transformations to the object
            """
            if not (apply_rotation or apply_scale):
                return
            # Store current context
            original_mode = obj.mode
            # Switch to object mode if needed
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            # Apply transformations
            bpy.ops.object.transform_apply(
                location=False, 
                rotation=apply_rotation, 
                scale=apply_scale
            )
            # Restore original mode
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=original_mode)
            transformations = []
            if apply_rotation:
                transformations.append("rotation")
            if apply_scale:
                transformations.append("scale")
            print(f"Object {', '.join(transformations)} applied.")
        # MAIN SCRIPT EXECUTION
        # Get the active object
        obj = bpy.context.active_object
        if not obj:
            print("No active object found.")
        else:
            print(f"Processing 3DGS transformations for object: {obj.name}")
            # Get current object rotation (ensuring quaternion is updated)
            original_rotation_mode = obj.rotation_mode
            # If not already in quaternion mode, ensure the quaternion gets updated
            if original_rotation_mode != 'QUATERNION':
                # Switch to quaternion mode to ensure quaternion is updated
                obj.rotation_mode = 'QUATERNION'
                # Switch back to original mode
                obj.rotation_mode = original_rotation_mode
            # Get the quaternion values
            obj_rotation_quat = obj.rotation_quaternion.copy()
            # Convert to w, x, y, z format (from Blender's x, y, z, w)
            blender_quat = [obj_rotation_quat.w, obj_rotation_quat.x, 
                          obj_rotation_quat.y, obj_rotation_quat.z]
            if VERBOSE:
                print(f"Current object rotation quaternion [w,x,y,z]: {blender_quat}")
            # Get current object scale
            scale_x, scale_y, scale_z = obj.scale
            if VERBOSE:
                print(f"Current object scale: X={scale_x}, Y={scale_y}, Z={scale_z}")
            # Calculate the logarithm of scale factors
            log_scale_x = math.log(scale_x) if scale_x > 0 else 0
            log_scale_y = math.log(scale_y) if scale_y > 0 else 0
            log_scale_z = math.log(scale_z) if scale_z > 0 else 0
            log_scale_factors = [log_scale_x, log_scale_y, log_scale_z]
            if VERBOSE:
                print(f"Log scale factors: X={log_scale_x}, Y={log_scale_y}, Z={log_scale_z}")
            # Check if the object has attribute data
            if not hasattr(obj.data, "attributes"):
                print("Object does not have attribute data.")
            else:
                # Perform transformations in the specified order
                if TRANSFORM_ORDER == "SCALE_FIRST":
                    # First update scale attributes
                    scale_success = update_scale_attributes(obj, SCALE_ATTRIBUTES, log_scale_factors, VERBOSE)
                    print("Scale attributes update", "succeeded" if scale_success else "failed")
                    # Then update rotation attributes
                    rotation_success = update_rotation_attributes(obj, ROTATION_ATTRIBUTES, blender_quat, VERBOSE, NORMALIZE_QUATERNIONS)
                    print("Rotation attributes update", "succeeded" if rotation_success else "failed")
                else:  # ROTATION_FIRST
                    # First update rotation attributes
                    rotation_success = update_rotation_attributes(obj, ROTATION_ATTRIBUTES, blender_quat, VERBOSE, NORMALIZE_QUATERNIONS)
                    print("Rotation attributes update", "succeeded" if rotation_success else "failed")
                    # Then update scale attributes
                    scale_success = update_scale_attributes(obj, SCALE_ATTRIBUTES, log_scale_factors, VERBOSE)
                    print("Scale attributes update", "succeeded" if scale_success else "failed")
                # Apply transformations to reset object transforms
                apply_transformations(obj, APPLY_ROTATION, APPLY_SCALE)
                print("\nTransformation operations completed.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
