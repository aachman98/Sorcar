import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectPrevItem(Node, ScSelectionNode):
    bl_idname = "ScSelectPrevItem"
    bl_label = "Select Previous Item"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_next_item()