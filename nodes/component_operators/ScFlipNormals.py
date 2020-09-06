import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScFlipNormals(Node, ScEditOperatorNode):
    bl_idname = "ScFlipNormals"
    bl_label = "Flip Normals"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.flip_normals()