import bpy

from bpy.types import Operator

class ScExecuteNode(Operator):
    bl_idname = "sc.execute_node"
    bl_label = "Execute Node"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "ScNodeTree"

    def execute(Self, context):
        context.space_data.edit_tree.node = context.space_data.edit_tree.nodes.active.name
        context.space_data.edit_tree.execute_node()
        return {"FINISHED"}