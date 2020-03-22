import bpy

from bpy.types import Operator
from ..helper import sc_poll

class ScExecuteNode(Operator):
    bl_idname = "sc.execute_node"
    bl_label = "Execute Node"

    @classmethod
    def poll(cls, context):
        return sc_poll(context)

    def execute(self, context):
        curr_tree = context.space_data.edit_tree
        if (curr_tree.bl_idname == "ScNodeTree" and curr_tree.nodes.active):
            curr_tree.node = curr_tree.nodes.active.name
            curr_tree.execute_node()
            return {"FINISHED"}
        return {"CANCELLED"}