import bpy
import math

from bpy.props import EnumProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScMathsOp(Node, ScNode):
    bl_idname = "ScMathsOp"
    bl_label = "Maths Operation"

    in_x: FloatProperty(update=ScNode.update_value)
    in_y: FloatProperty(update=ScNode.update_value)
    in_op: EnumProperty(name="Operation", items=[("ADD", "X + Y", "Addition"), ("SUB", "X - Y", "Subtraction"), ("MULT", "X * Y", "Multiplication"), ("DIV", "X / Y", "Division"), ("MOD", "X % Y", "Modulo (Remainder)"), ("POW", "X ^ Y", "Exponent (Power)"), ("LOG", "Log(X) to base Y", "Logarithm"), ("FACT", "!X", "X Factorial")], default="ADD", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketNumber", "Y").init("in_y", True)
        self.inputs.new("ScNodeSocketString", "Operation").init("in_op", True)
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def error_condition(self):
        return (
            (not self.inputs["Operation"].default_value in ["ADD", "SUB", "MULT", "DIV", "MOD", "POW", "LOG", "FACT"])
            or (self.inputs["Operation"].default_value in ['DIV', 'MOD'] and self.inputs["Y"].default_value == 0)
            or (self.inputs["Operation"].default_value == "POW" and self.inputs["X"].default_value == 0 and self.inputs["Y"].default_value == 0)
            or (self.inputs["Operation"].default_value == "LOG" and (self.inputs["X"].default_value <= 0 or self.inputs["Y"].default_value < 0 or self.inputs["Y"].default_value == 1))
            or (self.inputs["Operation"].default_value == "FACT" and int(self.inputs["X"].default_value) < 0)
        )

    def post_execute(self):
        out = {}
        if (self.inputs["Operation"].default_value == 'ADD'):
            out["Value"] = self.inputs["X"].default_value + self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == 'SUB'):
            out["Value"] = self.inputs["X"].default_value - self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == 'MULT'):
            out["Value"] = self.inputs["X"].default_value * self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == 'DIV'):
            out["Value"] = self.inputs["X"].default_value / self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == 'MOD'):
            out["Value"] = int(self.inputs["X"].default_value) % int(self.inputs["Y"].default_value)
        elif (self.inputs["Operation"].default_value == 'POW'):
            out["Value"] = pow(self.inputs["X"].default_value, self.inputs["Y"].default_value)
        elif (self.inputs["Operation"].default_value == 'LOG'):
            out["Value"] = math.log(self.inputs["X"].default_value, self.inputs["Y"].default_value)
        elif (self.inputs["Operation"].default_value == 'FACT'):
            out["Value"] = math.factorial(int(self.inputs["X"].default_value))
        return out