import bpy

from bpy.types import Operator

class ScSaveSelection(Operator):
    bl_idname = "sc.save_selection"
    bl_label = "Save Selection"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "ScNodeTree"

    def execute(Self, context):
        context.space_data.edit_tree.nodes.active.save_selection()
        return {"FINISHED"}