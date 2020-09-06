import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScMergeNormals(Node, ScEditOperatorNode):
    bl_idname = "ScMergeNormals"
    bl_label = "Merge Normals"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.merge_normals()