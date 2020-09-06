import bpy

from bpy.types import Operator
from ..helper import sc_poll_op
from ..debug import log

class ScEditGroup(Operator):
    """Edit the group referenced by the active node (or exit the current node-group)"""
    bl_idname = "sorcar.edit_group"
    bl_label = "Edit Group"

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)

    def execute(self, context):
        space = context.space_data
        path = space.path
        node_tree = path[-1].node_tree
        node = node_tree.nodes.active

        if (node):
            if hasattr(node, "node_tree"):
                if (node.node_tree):
                    log("OPERATOR", node_tree.name, self.bl_idname, "Node=\""+str(node.name)+"\", NodeTree="+"\""+node.node_tree.name+"\"", 1)
                    path.append(node.node_tree, node=node)
                    return {'FINISHED'}
                else:
                    log("OPERATOR", node_tree.name, self.bl_idname, "Node=\""+str(node.name)+"\", NodeTree not set", 1)
            elif len(path) > 1:
                path.pop()
                log("OPERATOR", node_tree.name, self.bl_idname, "Node=\""+str(node.name)+"\", NodeTree="+"\""+path[-1].node_tree.name+"\"", 1)
                return {'FINISHED'}
            else:
                log("OPERATOR", node_tree.name, self.bl_idname, "\""+str(node.name)+"\" not a group node, operation cancelled", 1)
        else:
            log("OPERATOR", node_tree.name, self.bl_idname, "No active node, operation cancelled", 1)
        return {'CANCELLED'}