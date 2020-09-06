import bpy

from bpy.types import Operator
from ..helper import sc_poll_op
from ..debug import log

class ScClearPreview(Operator):
    """Clear the preview node"""
    bl_idname = "sorcar.clear_preview"
    bl_label = "Clear Preview"

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)

    def execute(self, context):
        curr_tree = context.space_data.edit_tree
        if (curr_tree.node):
            log("OPERATOR", curr_tree.name, self.bl_idname, "Node=\""+str(curr_tree.node)+"\"", 1)
            curr_tree.node = None
            curr_tree.execute_node()
            return {'FINISHED'}
        else:
            log("OPERATOR", curr_tree.name, self.bl_idname, "No preview node set, operation cancelled", 1)
        return {'CANCELLED'}