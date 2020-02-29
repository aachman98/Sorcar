import bpy

from bpy.props import FloatProperty, FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScWarp(Node, ScEditOperatorNode):
    bl_idname = "ScWarp"
    bl_label = "Warp"

    in_warp_angle: FloatProperty(default=6.28319, update=ScNode.update_value)
    in_offset_angle: FloatProperty(update=ScNode.update_value)
    in_min: FloatProperty(default=-1.0, update=ScNode.update_value)
    in_max: FloatProperty(default=1.0, update=ScNode.update_value)
    in_center: FloatVectorProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Warp Angle").init("in_warp_angle", True)
        self.inputs.new("ScNodeSocketNumber", "Offset Angle").init("in_offset_angle", True)
        self.inputs.new("ScNodeSocketNumber", "Min").init("in_min")
        self.inputs.new("ScNodeSocketNumber", "Max").init("in_max")
        self.inputs.new("ScNodeSocketVector", "Center").init("in_center")
    
    def functionality(self):
        bpy.ops.transform.vertex_warp(
            warp_angle = self.inputs["Warp Angle"].default_value,
            offset_angle = self.inputs["Offset Angle"].default_value,
            min = self.inputs["Min"].default_value,
            max = self.inputs["Max"].default_value,
            center = self.inputs["Center"].default_value
        )