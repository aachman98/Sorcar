import bpy

from bpy.props import BoolProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScMapRange(Node, ScNode):
    bl_idname = "ScMapRange"
    bl_label = "Map Range"
    bl_icon = 'MOD_HUE_SATURATION'

    in_x: FloatProperty(update=ScNode.update_value)
    in_min_in: FloatProperty(update=ScNode.update_value)
    in_max_in: FloatProperty(default=1, update=ScNode.update_value)
    in_min_out: FloatProperty(update=ScNode.update_value)
    in_max_out: FloatProperty(default=1, update=ScNode.update_value)
    in_clamp: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketNumber", "In Min").init("in_min_in", True)
        self.inputs.new("ScNodeSocketNumber", "In Max").init("in_max_in", True)
        self.inputs.new("ScNodeSocketNumber", "Out Min").init("in_min_out", True)
        self.inputs.new("ScNodeSocketNumber", "Out Max").init("in_max_out", True)
        self.inputs.new("ScNodeSocketBool", "Clamp").init("in_clamp")
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Out Min"].default_value == self.inputs["Out Max"].default_value
        )
    
    def post_execute(self):
        out = super().post_execute()
        x = self.inputs["X"].default_value
        x_min = self.inputs["In Min"].default_value
        x_max = self.inputs["In Max"].default_value
        y_min = self.inputs["Out Min"].default_value
        y_max = self.inputs["Out Max"].default_value
        if (self.inputs["Clamp"].default_value):
            x = max(min(x, x_max), x_min)
        out["Value"] = (((x-x_min) * (y_max-y_min)) / (x_max-x_min)) + y_min
        return out