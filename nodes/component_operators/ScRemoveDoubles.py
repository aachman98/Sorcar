import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScRemoveDoubles(Node, ScEditOperatorNode):
    bl_idname = "ScRemoveDoubles"
    bl_label = "Remove Doubles"
    
    in_threshold: FloatProperty(default=0.0001, min=0.000001, max=50.0, update=ScNode.update_value)
    in_unselected: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold", True)
        self.inputs.new("ScNodeSocketBool", "Unselected").init("in_unselected")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Threshold"].default_value < 0.000001 or self.inputs["Threshold"].default_value > 50)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.remove_doubles(
            threshold = self.inputs["Threshold"].default_value,
            use_unselected = self.inputs["Unselected"].default_value
        )