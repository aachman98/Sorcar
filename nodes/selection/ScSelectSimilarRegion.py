import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectSimilarRegion(Node, ScSelectionNode):
    bl_idname = "ScSelectSimilarRegion"
    bl_label = "Select Similar Region"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_similar_region()