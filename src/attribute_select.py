import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


class SNA_OT_Dgs_Render_Attribute_Select_51C86(bpy.types.Operator):
    bl_idname = "sna.dgs_render_attribute_select_51c86"
    bl_label = "3DGS Render: Attribute Select"
    bl_description = "Select points based on native 3DGS attributes"
    bl_options = {"REGISTER", "UNDO"}

    def sna_scale_target_attr_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_scale_target_attr: bpy.props.EnumProperty(name='SCALE_TARGET_ATTR', description='', items=[('scale_combined', 'scale_combined', '', 0, 0), ('scale_0', 'scale_0', '', 0, 1), ('scale_1', 'scale_1', '', 0, 2), ('scale_2', 'scale_2', '', 0, 3)])
    sna_scale_factor: bpy.props.FloatProperty(name='SCALE_FACTOR', description='', default=0.5, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2)

    def sna_scale_compare_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_scale_compare: bpy.props.EnumProperty(name='SCALE_COMPARE', description='', items=[('GREATER', 'GREATER', '', 0, 0), ('LESS', 'LESS', '', 0, 1)])
    sna_rot_target_euler: bpy.props.FloatVectorProperty(name='ROT_TARGET_EULER', description='', size=3, default=(0.0, 0.0, 0.0), subtype='EULER', unit='NONE', step=3, precision=6)
    sna_rot_tolerance_deg: bpy.props.FloatProperty(name='ROT_TOLERANCE_DEG', description='', default=5.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2)

    def sna_rot_compare_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_rot_compare: bpy.props.EnumProperty(name='ROT_COMPARE', description='', items=[('EQUAL', 'EQUAL', '', 0, 0), ('NOT_EQUAL', 'NOT_EQUAL', '', 0, 1)])

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set('')
        return True

    def execute(self, context):
        TARGET_OBJ = bpy.context.view_layer.objects.active
        SELECTION_MODE = bpy.context.scene.sna_dgs_scene_properties.select_attribute_type
        SCALE_TARGET_ATTR = self.sna_scale_target_attr
        SCALE_FACTOR = self.sna_scale_factor
        SCALE_COMPARE = self.sna_scale_compare
        ROT_TARGET_EULER = self.sna_rot_target_euler
        ROT_TOLERANCE_DEG = self.sna_rot_tolerance_deg
        ROT_COMPARE = self.sna_rot_compare
        COL_TARGET_RGB = None
        COL_COMPARE_MODE = None
        COL_TOLERANCE = None
        STRETCH_FACTOR = self.sna_scale_factor
        STRETCH_COMPARE = self.sna_scale_compare
        CLEAR_PREVIOUS = True
        import bmesh
        import mathutils
        # =========================================================================
        # INPUT VARIABLES (Serpens Sockets)
        # =========================================================================
        # TARGET_OBJ = None                  # Input: Pointer property / Object
        # CLEAR_PREVIOUS = True              # Input: Boolean
        # SELECTION_MODE = 'SCALE'           # Input: 'SCALE', 'ROT', or 'STRETCH'
        # --- SCALE SETTINGS ---
        # SCALE_TARGET_ATTR = 'scale_0'      # Input: 'scale_0', 'scale_1', 'scale_2', or 'scale_combined'
        # SCALE_FACTOR = 0.5                 # Input: Float 0.0 to 1.0
        # SCALE_COMPARE = 'GREATER'          # Input: 'GREATER' or 'LESS'
        # --- STRETCH SETTINGS ---
        # STRETCH_FACTOR = 0.5               # Input: Float 0.0 to 1.0 (0 = least stretched, 1 = most stretched)
        # STRETCH_COMPARE = 'GREATER'        # Input: 'GREATER' or 'LESS'
        # --- ROTATION SETTINGS ---
        # ROT_TARGET_EULER = (0.0, 0.0, 0.0) # Input: Vector/Tuple in degrees
        # ROT_TOLERANCE_DEG = 5.0            # Input: Float (Degrees of leeway)
        # ROT_COMPARE = 'EQUAL'              # Input: 'EQUAL' or 'NOT_EQUAL'
        # =========================================================================
        # OUTPUT VARIABLES
        # =========================================================================
        SCRIPT_SUCCESS = False
        SELECTED_COUNT = 0
        ERROR_MSG = ""
        # =========================================================================
        # FIREWALL FUNCTIONS (Strips Serpens Wrappers/Lists/Strings into Floats)
        # =========================================================================

        def parse_float(val, default=0.0):
            try:
                if isinstance(val, (int, float)): return float(val)
                if isinstance(val, (list, tuple)) and len(val) > 0: return float(val)
                nums = [float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", str(val))]
                return nums if nums else float(default)
            except:
                return float(default)

        def parse_vec3(val, default=(0.0, 0.0, 0.0)):
            try:
                if isinstance(val, (list, tuple)) and len(val) >= 3:
                    return float(val), float(val[1]), float(val[2])
                nums = [float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", str(val))]
                if len(nums) >= 3:
                    return nums, nums[1], nums[2]
                return default
            except:
                return default
        # =========================================================================
        # EXECUTION LOGIC 
        # =========================================================================
        try:
            if TARGET_OBJ and TARGET_OBJ.type == 'MESH':
                mesh = TARGET_OBJ.data
                attrs = mesh.attributes
                original_mode = 'OBJECT'
                if bpy.context.active_object:
                    original_mode = bpy.context.active_object.mode
                if bpy.context.mode != 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
                vert_selections = [False] * len(mesh.vertices)
                # 1. Sanitize all inputs through the firewall immediately
                safe_scale_factor = parse_float(SCALE_FACTOR, 0.5)
                safe_stretch_factor = parse_float(STRETCH_FACTOR, 0.5)
                safe_rot_tol = parse_float(ROT_TOLERANCE_DEG, 5.0)
                target_rx, target_ry, target_rz = parse_vec3(ROT_TARGET_EULER, (0.0, 0.0, 0.0))
                # -------------------------------------------------------------
                # SCALE SELECTION
                # -------------------------------------------------------------
                if SELECTION_MODE == 'SCALE':
                    if SCALE_TARGET_ATTR == 'scale_combined':
                        required_scales = ['scale_0', 'scale_1', 'scale_2']
                        if not all(a in attrs for a in required_scales):
                            raise ValueError("Missing one or more scale attributes.")
                        s0, s1, s2 = [attrs[a].data for a in required_scales]
                        raw_scales = [(float(s0[i].value) + float(s1[i].value) + float(s2[i].value)) for i in range(len(mesh.vertices))]
                    else:
                        if SCALE_TARGET_ATTR not in attrs:
                            raise ValueError(f"Attribute {SCALE_TARGET_ATTR} not found.")
                        s_data = attrs[SCALE_TARGET_ATTR].data
                        raw_scales = [float(item.value) for item in s_data]
                    min_s = min(raw_scales)
                    max_s = max(raw_scales)
                    range_s = max_s - min_s if max_s != min_s else 1.0
                    for i, val in enumerate(raw_scales):
                        normalized_factor = (val - min_s) / range_s
                        if SCALE_COMPARE == 'GREATER' and normalized_factor > safe_scale_factor:
                            vert_selections[i] = True
                        elif SCALE_COMPARE == 'LESS' and normalized_factor < safe_scale_factor:
                            vert_selections[i] = True
                # -------------------------------------------------------------
                # STRETCH SELECTION
                # -------------------------------------------------------------
                elif SELECTION_MODE == 'STRETCH':
                    required_scales = ['scale_0', 'scale_1', 'scale_2']
                    if not all(a in attrs for a in required_scales):
                        raise ValueError("Missing scale attributes for stretch mode.")
                    s0, s1, s2 = [attrs[a].data for a in required_scales]
                    raw_ratios = []
                    for i in range(len(mesh.vertices)):
                        v0, v1, v2 = float(s0[i].value), float(s1[i].value), float(s2[i].value)
                        ratio = math.exp(max(v0, v1, v2) - min(v0, v1, v2))
                        raw_ratios.append(ratio)
                    min_r = min(raw_ratios)
                    max_r = max(raw_ratios)
                    range_r = max_r - min_r if max_r != min_r else 1.0
                    for i, ratio in enumerate(raw_ratios):
                        normalized_factor = (ratio - min_r) / range_r
                        if STRETCH_COMPARE == 'GREATER' and normalized_factor > safe_stretch_factor:
                            vert_selections[i] = True
                        elif STRETCH_COMPARE == 'LESS' and normalized_factor < safe_stretch_factor:
                            vert_selections[i] = True
                # -------------------------------------------------------------
                # ROTATION SELECTION
                # -------------------------------------------------------------
                elif SELECTION_MODE == 'ROT':
                    required_attrs = ['rot_0', 'rot_1', 'rot_2', 'rot_3']
                    if not all(a in attrs for a in required_attrs):
                        raise ValueError("Missing rot_0/1/2/3 attributes.")
                    r0, r1, r2, r3 = [attrs[a].data for a in required_attrs]
                    rad_eul = [math.radians(target_rx), math.radians(target_ry), math.radians(target_rz)]
                    target_quat = mathutils.Euler(rad_eul, 'XYZ').to_quaternion()
                    target_quat.normalize()
                    for i in range(len(mesh.vertices)):
                        vert_quat = mathutils.Quaternion((float(r0[i].value), float(r1[i].value), float(r2[i].value), float(r3[i].value)))
                        if vert_quat.magnitude > 0.0001:
                            vert_quat.normalize()
                            angle_diff = target_quat.rotation_difference(vert_quat).angle
                            angle_deg = math.degrees(angle_diff)
                            is_match = angle_deg <= safe_rot_tol
                            if ROT_COMPARE == 'EQUAL' and is_match:
                                vert_selections[i] = True
                            elif ROT_COMPARE == 'NOT_EQUAL' and not is_match:
                                vert_selections[i] = True
                # -------------------------------------------------------------
                # APPLY SELECTION
                # -------------------------------------------------------------
                bm = bmesh.new()
                bm.from_mesh(mesh)
                bm.verts.ensure_lookup_table()
                count = 0
                for i, vert in enumerate(bm.verts):
                    if CLEAR_PREVIOUS and not vert_selections[i]:
                        vert.select = False
                    if vert_selections[i]:
                        vert.select = True
                        count += 1
                bm.to_mesh(mesh)
                bm.free()
                mesh.update()
                if bpy.context.active_object and bpy.context.active_object.mode != original_mode:
                    bpy.ops.object.mode_set(mode=original_mode)
                SCRIPT_SUCCESS = True
                SELECTED_COUNT = count
            else:
                ERROR_MSG = "Invalid or missing target object."
                SCRIPT_SUCCESS = False
        except Exception as exc:
            SCRIPT_SUCCESS = False
            SELECTED_COUNT = 0
            ERROR_MSG = str(exc)
            print(f"3DGS Attribute Selection Error: {exc}")
            if 'original_mode' in locals() and bpy.context.active_object:
                if bpy.context.active_object.mode != original_mode:
                    bpy.ops.object.mode_set(mode=original_mode)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        if bpy.context.scene.sna_dgs_scene_properties.select_attribute_type == "SCALE":
            col_94F1A = layout.column(heading='', align=False)
            col_94F1A.prop(self, 'sna_scale_target_attr', text=self.sna_scale_target_attr, icon_value=0, emboss=True, expand=True)
            col_94F1A.prop(self, 'sna_scale_factor', text='Factor', icon_value=0, emboss=True, expand=False)
            row_0FEBA = col_94F1A.row(heading='', align=False)
            row_0FEBA.prop(self, 'sna_scale_compare', text=self.sna_scale_compare, icon_value=0, emboss=True, expand=True)
        elif bpy.context.scene.sna_dgs_scene_properties.select_attribute_type == "ROT":
            col_50BE3 = layout.column(heading='', align=False)
            col_50BE3.prop(self, 'sna_rot_target_euler', text='Target Rotation', icon_value=0, emboss=True)
            col_50BE3.prop(self, 'sna_rot_tolerance_deg', text='Tolerance', icon_value=0, emboss=True, expand=False)
            row_9826B = col_50BE3.row(heading='', align=False)
            row_9826B.prop(self, 'sna_rot_compare', text=self.sna_rot_compare, icon_value=0, emboss=True, expand=True)
        elif bpy.context.scene.sna_dgs_scene_properties.select_attribute_type == "STRETCH":
            col_0EDB7 = layout.column(heading='', align=False)
            col_0EDB7.prop(self, 'sna_scale_factor', text='Factor', icon_value=0, emboss=True, expand=False)
            row_1AE6E = col_0EDB7.row(heading='', align=False)
            row_1AE6E.prop(self, 'sna_scale_compare', text=self.sna_scale_compare, icon_value=0, emboss=True, expand=True)
        else:
            pass

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
