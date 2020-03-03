import bpy

from bpy.types import Operator

class ScExecuteNode(Operator):
    bl_idname = "sc.execute_node"
    bl_label = "Execute Node"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "ScNodeTree"

    def execute(self, context):
        if (context.space_data.edit_tree.bl_idname == "ScNodeTree" and context.space_data.edit_tree.nodes.active):
            context.space_data.edit_tree.node = context.space_data.edit_tree.nodes.active.name
            context.space_data.edit_tree.execute_node()
            return {"FINISHED"}
        return {"CANCELLED"}