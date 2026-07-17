import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_append_and_add_geo_nodes_function_execute_6BCD7(Node_Group_Name, Modifier_Name, Object):
    if property_exists("bpy.data.node_groups[Node_Group_Name]", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', '3DGS Render APPEND V5.blend') + r'\NodeTree', filename=Node_Group_Name, link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_65345 = None if not new_data else new_data[0]
    modifier_6D624 = Object.modifiers.new(name=Modifier_Name, type='NODES', )
    modifier_6D624.node_group = bpy.data.node_groups[Node_Group_Name]
    return modifier_6D624
