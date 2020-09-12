import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectRegionBoundary(Node, ScSelectionNode):
    bl_idname = "ScSelectRegionBoundary"
    bl_label = "Select Region Boundary"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.region_to_loop()