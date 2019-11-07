import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScAddEdgeFace(Node, ScEditOperatorNode):
    bl_idname = "ScAddEdgeFace"
    bl_label = "Add Edge/Face"
    
    def functionality(self):
        bpy.ops.mesh.edge_face_add()