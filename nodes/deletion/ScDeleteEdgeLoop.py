import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDeleteEdgeLoop(Node, ScDeletionNode):
    bl_idname = "ScDeleteEdgeLoop"
    bl_label = "Delete Edge Loop"
    
    in_split: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Face Split").init("in_split")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.delete_edgeloop(
            use_face_split = self.inputs["Face Split"].default_value
        )