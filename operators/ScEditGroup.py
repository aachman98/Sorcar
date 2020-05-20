import bpy

from bpy.types import Operator
from ..helper import sc_poll_op

class ScEditGroup(Operator):
    bl_idname = "sc.edit_group"
    bl_label = "Edit Group"

    @classmethod
    def poll(cls, context):
        return (
            sc_poll_op(context)
            and context.space_data.node_tree.nodes.active.node_tree
        )

    def execute(self, context):
        space = context.space_data
        node = space.node_tree.nodes.active
        space.path.append(node.node_tree)
        return {"FINISHED"}