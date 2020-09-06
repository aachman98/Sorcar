import bpy

from bpy.types import Operator
from ..helper import sc_poll_op
from ..debug import log

class ScExecuteNode(Operator):
    """Execute the selected node (re-evaluates the nodetree)"""
    bl_idname = "sorcar.execute_node"
    bl_label = "Execute Node"

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)

    def execute(self, context):
        curr_tree = context.space_data.edit_tree
        node = curr_tree.nodes.active
        if (node):
            log("OPERATOR", curr_tree.name, self.bl_idname, "Node=\""+str(node.name)+"\"", 1)
            curr_tree.node = node.name
            curr_tree.execute_node()
            return {'FINISHED'}
        else:
            log("OPERATOR", curr_tree.name, self.bl_idname, "No active node, operation cancelled", 1)
        return {'CANCELLED'}