import bpy

from bpy.props import EnumProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScComparisonOp(Node, ScNode):
    bl_idname = "ScComparisonOp"
    bl_label = "Comparison Operation"
    bl_icon = 'CON_SAMEVOL'

    in_x: FloatProperty(name="X", update=ScNode.update_value)
    in_y: FloatProperty(name="Y", update=ScNode.update_value)
    in_op: EnumProperty(items=[("LT", "X < Y", "Less Than"), ("GT", "X > Y", "Greater Than"), ("LE", "X <= Y", "Less Than or Equal To"), ("GE", "X >= Y", "Greater Than or Equal To"), ("EQ", "X == Y", "Equal To"), ("NE", "X != Y", "Not Equal To")], default="EQ", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketNumber", "Y").init("in_y", True)
        self.inputs.new("ScNodeSocketString", "Operation").init("in_op", True)
        self.outputs.new("ScNodeSocketBool", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Operation"].default_value in ['LT', 'GT', 'LE', 'GE', 'EQ', 'NE'])
        )
    
    def post_execute(self):
        out = super().post_execute()
        if (self.inputs["Operation"].default_value == "LT"):
            out["Value"] = self.inputs["X"].default_value < self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "GT"):
            out["Value"] = self.inputs["X"].default_value > self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "LE"):
            out["Value"] = self.inputs["X"].default_value <= self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "GE"):
            out["Value"] = self.inputs["X"].default_value >= self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "EQ"):
            out["Value"] = self.inputs["X"].default_value == self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "NE"):
            out["Value"] = self.inputs["X"].default_value != self.inputs["Y"].default_value
        return out