import bpy
import math

from bpy.props import EnumProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScTrigoOp(Node, ScNode):
    bl_idname = "ScTrigoOp"
    bl_label = "Trigonometric Operation"
    bl_icon = 'FORCE_HARMONIC'

    in_x: FloatProperty(update=ScNode.update_value)
    in_op1: EnumProperty(name="Opertion", items=[("SIN","Sin",""), ("COS","Cos",""), ("TAN","Tan","")], default="SIN", update=ScNode.update_value)
    in_op2: EnumProperty(name="Opertion 2", items=[("NONE","None",""), ("HB","Hyperbolic",""), ("INV","Inverse","")], default="NONE", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketString", "Operation 1").init("in_op1", True)
        self.inputs.new("ScNodeSocketString", "Operation 2").init("in_op2")
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Operation 1"].default_value in ["SIN", "COS", "TAN"])
            or (not self.inputs["Operation 2"].default_value in ["NONE", "HB", "INV"])
        )
    
    def post_execute(self):
        out = super().post_execute()
        if (self.inputs["Operation 1"].default_value == "SIN"):
            if (self.inputs["Operation 2"].default_value == "NONE"):
                out["Value"] = math.sin(self.inputs["X"].default_value)
            elif (self.inputs["Operation 2"].default_value == "HB"):
                out["Value"] = math.sinh(self.inputs["X"].default_value)
            elif (self.inputs["Operation 2"].default_value == "INV"):
                out["Value"] = math.asin(max(min(self.inputs["X"].default_value, 1), -1))
        elif (self.inputs["Operation 1"].default_value == "COS"):
            if (self.inputs["Operation 2"].default_value == "NONE"):
                out["Value"] = math.cos(self.inputs["X"].default_value)
            elif (self.inputs["Operation 2"].default_value == "HB"):
                out["Value"] = math.cosh(self.inputs["X"].default_value)
            elif (self.inputs["Operation 2"].default_value == "INV"):
                out["Value"] = math.acos(max(min(self.inputs["X"].default_value, 1), -1))
        elif (self.inputs["Operation 1"].default_value == "TAN"):
            if (self.inputs["Operation 2"].default_value == "NONE"):
                out["Value"] = math.tan(self.inputs["X"].default_value)
            elif (self.inputs["Operation 2"].default_value == "HB"):
                out["Value"] = math.tanh(self.inputs["X"].default_value)
            elif (self.inputs["Operation 2"].default_value == "INV"):
                out["Value"] = math.atan(self.inputs["X"].default_value)
        return out