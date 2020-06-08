import bpy

from bpy.types import Operator
from ..helper import sc_poll_op

class ScClearPreview(Operator):
    """Clear the preview node"""
    bl_idname = "sorcar.clear_preview"
    bl_label = "Clear Preview"

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)

    def execute(self, context):
        curr_tree = context.space_data.edit_tree
        curr_tree.node = None
        curr_tree.execute_node()
        return {"FINISHED"}