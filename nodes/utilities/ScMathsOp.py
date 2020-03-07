import bpy
import math

from bpy.props import EnumProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

op_items = [
    # (identifier, name, description)
    ("ADD", "X + Y", "Addition"),
    ("SUB", "X - Y", "Subtraction"),
    ("MULT", "X * Y", "Multiplication"),
    ("DIV", "X / Y", "Division"),
    None,
    ("POW", "X ^ Y", "Exponent (Power)"),
    ("LOG", "Log(X) to base Y", "Logarithm"),
    ("SQRT", "√X", "Square Root"),
    ("FACT", "!X", "X Factorial"),
    ("ABS", "|X|", "Absolute"),
    None,
    ("MIN", "Min(X, Y)", "Minimum"),
    ("MAX", "Max(X, Y)", "Maximum"),
    None,
    ("ROUND", "Round(X)", "Round"),
    ("FLOOR", "Floor(X)", "Floor of X"),
    ("CEIL", "Ceil(X)", "Ceiling of X"),
    ("FRACT", "Fraction", "Fractional Part of X"),
    ("MOD", "X % Y", "Modulo (Remainder)"),
]

class ScMathsOp(Node, ScNode):
    bl_idname = "ScMathsOp"
    bl_label = "Maths Operation"

    in_x: FloatProperty(update=ScNode.update_value)
    in_y: FloatProperty(update=ScNode.update_value)
    in_op: EnumProperty(name="Operation", items=op_items, default="ADD", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketNumber", "Y").init("in_y", True)
        self.inputs.new("ScNodeSocketString", "Operation").init("in_op", True)
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def error_condition(self):
        op = self.inputs["Operation"].default_value
        return (
            (not op in [i[0] for i in op_items if i])
            or (op in ['DIV', 'MOD'] and self.inputs["Y"].default_value == 0)
            or (op == "POW" and self.inputs["X"].default_value == 0 and self.inputs["Y"].default_value == 0)
            or (op == "LOG" and (self.inputs["X"].default_value <= 0 or self.inputs["Y"].default_value < 0 or self.inputs["Y"].default_value == 1))
            or (op == "FACT" and int(self.inputs["X"].default_value) < 0)
        )

    def post_execute(self):
        out = {}
        op = self.inputs["Operation"].default_value
        x = self.inputs["X"].default_value
        y = self.inputs["Y"].default_value
        if (op == 'ADD'):
            out["Value"] = x + y
        elif (op == 'SUB'):
            out["Value"] = x - y
        elif (op == 'MULT'):
            out["Value"] = x * y
        elif (op == 'DIV'):
            out["Value"] = x / y
        elif (op == 'POW'):
            out["Value"] = pow(x, y)
        elif (op == 'LOG'):
            out["Value"] = math.log(x, y)
        elif (op == 'SQRT'):
            out["Value"] = math.sqrt(x)
        elif (op == 'FACT'):
            out["Value"] = math.factorial(int(x))
        elif (op == 'ABS'):
            out["Value"] = abs(x)
        elif (op == 'MIN'):
            out["Value"] = min(x, y)
        elif (op == 'MAX'):
            out["Value"] = max(x, y)
        elif (op == 'ROUND'):
            out["Value"] = round(x)
        elif (op == 'FLOOR'):
            out["Value"] = math.floor(x)
        elif (op == 'CEIL'):
            out["Value"] = math.ceil(x)
        elif (op == 'FRACT'):
            out["Value"] = x - math.floor(x)
        elif (op == 'MOD'):
            out["Value"] = x % y
        return out