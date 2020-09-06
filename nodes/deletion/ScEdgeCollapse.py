import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScEdgeCollapse(Node, ScDeletionNode):
    bl_idname = "ScEdgeCollapse"
    bl_label = "Collapse Edge"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.edge_collapse()