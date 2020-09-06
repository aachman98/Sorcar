import bpy

from bpy.types import Operator
from ..helper import sc_poll_op
from ..debug import log

class ScSaveSelection(Operator):
    """Save the components of the mesh currently selected"""
    bl_idname = "sorcar.save_selection"
    bl_label = "Save Selection"

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)

    def execute(self, context):
        curr_tree = context.space_data.edit_tree
        node = curr_tree.nodes.active
        if (node):
            if (hasattr(node, "save_selection")):
                log("OPERATOR", curr_tree.name, self.bl_idname, "Node=\""+node.name+"\"", 1)
                node.save_selection()
                return {'FINISHED'}
            else:
                log("OPERATOR", curr_tree.name, self.bl_idname, "\""+str(node.name)+"\" does not support saving, operation cancelled", 1)
        else:
            log("OPERATOR", curr_tree.name, self.bl_idname, "No active node, operation cancelled", 1)
        return {'CANCELLED'}