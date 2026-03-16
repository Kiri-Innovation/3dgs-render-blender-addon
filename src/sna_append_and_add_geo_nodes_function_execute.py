# from .important import *
#
# def sna_append_and_add_geo_nodes_function_execute_6BCD7(Node_Group_Name, Modifier_Name, Object):
#     import bpy
#     import os
#
#     if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
#         pass
#     else:
#         before_data = list(bpy.data.node_groups)
#         bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V4.blend') + r'\NodeTree', filename=Node_Group_Name, link=False)
#         new_data = list(filter(lambda d: d not in before_data, list(bpy.data.node_groups)))
#         appended_65345 = None if not new_data else new_data[0]
#     modifier_6D624 = Object.modifiers.new(name=Modifier_Name, type='NODES', )
#     modifier_6D624.node_group = bpy.data.node_groups[Node_Group_Name]
#     return modifier_6D624
