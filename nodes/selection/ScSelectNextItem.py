import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectNextItem(Node, ScSelectionNode):
    bl_idname = "ScSelectNextItem"
    bl_label = "Select Next Item"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_next_item()