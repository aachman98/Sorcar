import bpy

from bpy.props import FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScBeautifyFill(Node, ScEditOperatorNode):
    bl_idname = "ScBeautifyFill"
    bl_label = "Beautify Fill"
    
    in_angle_limit: FloatProperty(default=3.14159, min=0.0, max=3.14159, unit="ROTATION", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Angle Limit").init("in_angle_limit", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Angle Limit"].default_value < 0 or self.inputs["Angle Limit"].default_value > 3.14159)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.beautify_fill(
            angle_limit = self.inputs["Angle Limit"].default_value
        )