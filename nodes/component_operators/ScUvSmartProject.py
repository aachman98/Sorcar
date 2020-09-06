import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScUvSmartProject(Node, ScEditOperatorNode):
    bl_idname = "ScUvSmartProject"
    bl_label = "UV Smart Project"
    
    in_limit: FloatProperty(default=66.0, min=1.0, max=89.0, update=ScNode.update_value)
    in_margin: FloatProperty(min=0.0, max=1.0, update=ScNode.update_value)
    in_weight: FloatProperty(min=0.0, max=1.0, update=ScNode.update_value)
    in_aspect: BoolProperty(default=True, update=ScNode.update_value)
    in_stretch: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Angle Limit").init("in_limit", True)
        self.inputs.new("ScNodeSocketNumber", "Island Margin").init("in_margin")
        self.inputs.new("ScNodeSocketNumber", "Area Weight").init("in_weight")
        self.inputs.new("ScNodeSocketBool", "Correct Aspect").init("in_aspect")
        self.inputs.new("ScNodeSocketBool", "Stretch to UV Bounds").init("in_stretch", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Angle Limit"].default_value < 1.0 or self.inputs["Angle Limit"].default_value > 89.0)
            or (self.inputs["Island Margin"].default_value < 0.0 or self.inputs["Island Margin"].default_value > 1.0)
            or (self.inputs["Area Weight"].default_value < 0.0 or self.inputs["Area Weight"].default_value > 1.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.uv.smart_project(
            angle_limit = self.inputs["Angle Limit"].default_value,
            island_margin = self.inputs["Island Margin"].default_value,
            user_area_weight = self.inputs["Area Weight"].default_value,
            use_aspect = self.inputs["Correct Aspect"].default_value,
            stretch_to_bounds = self.inputs["Stretch to UV Bounds"].default_value
        )