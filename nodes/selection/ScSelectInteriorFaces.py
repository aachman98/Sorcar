import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectInteriorFaces(Node, ScSelectionNode):
    bl_idname = "ScSelectInteriorFaces"
    bl_label = "Select Interior Faces"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_interior_faces()