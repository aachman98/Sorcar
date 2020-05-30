import bpy

from bpy.types import Operator
from ..helper import sc_poll_op

class ScExecuteNode(Operator):
    """Execute the selected node (re-evaluates the nodetree)"""
    bl_idname = "sc.execute_node"
    bl_label = "Execute Node"

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)

    def execute(self, context):
        curr_tree = context.space_data.edit_tree
        if (curr_tree.bl_idname == "ScNodeTree" and curr_tree.nodes.active):
            curr_tree.node = curr_tree.nodes.active.name
            curr_tree.execute_node()
            return {"FINISHED"}
        return {"CANCELLED"}