import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScUnsubdivide(Node, ScEditOperatorNode):
    bl_idname = "ScUnsubdivide"
    bl_label = "Unsubdivide"
    
    in_iterations: IntProperty(default=2, min=1, max=1000, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Iterations").init("in_iterations", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Iterations"].default_value) < 1 or int(self.inputs["Iterations"].default_value) > 1000)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.unsubdivide(
            iterations = int(self.inputs["Iterations"].default_value)
        )