import bpy

from bpy.props import FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDissolveDegenerate(Node, ScDeletionNode):
    bl_idname = "ScDissolveDegenerate"
    bl_label = "Dissolve Degenerate"

    in_threshold: FloatProperty(default=0.0001, min=0.000001, max=50.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.dissolve_degenerate(
            threshold = self.inputs["Threshold"].default_value
        )