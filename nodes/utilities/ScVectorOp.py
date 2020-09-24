import bpy
from mathutils import Vector

from bpy.props import EnumProperty, FloatVectorProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScVectorOp(Node, ScNode):
    bl_idname = "ScVectorOp"
    bl_label = "Vector Operation"
    bl_icon = 'CON_LOCLIMIT'

    in_x: FloatVectorProperty(update=ScNode.update_value)
    in_y: FloatVectorProperty(update=ScNode.update_value)
    in_k: FloatProperty(update=ScNode.update_value)
    in_op: EnumProperty(name="Operation", items=[("ADD", "X + Y", "Addition"), ("SUB", "X - Y", "Subtraction"), ("MULT", "K * X", "Multiplication by Scalar"), ("CROSS", "X * Y", "Cross Product"), ("DOT", "X . Y", "Dot Product"), ("ANGLE", "Angle", ""), ("PROJ", "Project", ""), ("REFL", "Reflect", "Mirror"), ("ROT", "Rotation Difference", "Rotation Difference"), ("NORM", "Normalise X", "Unit Vector"), ("ORTHO", "Orthogonal X", "Perpendicular"), ("LERP", "Lerp", "Linear Interpolate"), ("SLERP", "S-Lerp", "Spherical Interpolate")], default="ADD", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketVector", "Y").init("in_y", True)
        self.inputs.new("ScNodeSocketNumber", "K").init("in_k")
        self.inputs.new("ScNodeSocketString", "Operation").init("in_op", True)
        self.outputs.new("ScNodeSocketVector", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Operation"].default_value in ["ADD", "SUB", "MULT", "CROSS", "DOT", "ANGLE", "PROJ", "REFL", "ROT", "NORM", "ORTHO", "LERP", "SLERP"])
            or (self.inputs["Operation"].default_value == "LERP" and (self.inputs["K"].default_value < 0 or self.inputs["K"].default_value > 1))
        )

    def post_execute(self):
        out = super().post_execute()
        if (self.inputs["Operation"].default_value == 'ADD'):
            out["Value"] = Vector(self.inputs["X"].default_value) + Vector(self.inputs["Y"].default_value)
        elif (self.inputs["Operation"].default_value == 'SUB'):
            out["Value"] = Vector(self.inputs["X"].default_value) - Vector(self.inputs["Y"].default_value)
        elif (self.inputs["Operation"].default_value == 'MULT'):
            out["Value"] = Vector(self.inputs["X"].default_value) * self.inputs["K"].default_value
        elif (self.inputs["Operation"].default_value == 'CROSS'):
            out["Value"] = Vector(self.inputs["X"].default_value).cross(Vector(self.inputs["Y"].default_value))
        elif (self.inputs["Operation"].default_value == 'DOT'):
            out["Value"] = Vector.Fill(3, Vector(self.inputs["X"].default_value).dot(Vector(self.inputs["Y"].default_value)))
        elif (self.inputs["Operation"].default_value == 'ANGLE'):
            out["Value"] = Vector.Fill(3, Vector(self.inputs["X"].default_value).angle(Vector(self.inputs["Y"].default_value)))
        elif (self.inputs["Operation"].default_value == 'PROJ'):
            out["Value"] = Vector(self.inputs["X"].default_value).project(Vector(self.inputs["Y"].default_value))
        elif (self.inputs["Operation"].default_value == 'REFL'):
            out["Value"] = Vector(self.inputs["X"].default_value).reflect(Vector(self.inputs["Y"].default_value))
        elif (self.inputs["Operation"].default_value == 'ROT'):
            out["Value"] = Vector(self.inputs["X"].default_value).rotation_difference(Vector(self.inputs["Y"].default_value)).to_euler()
        elif (self.inputs["Operation"].default_value == 'NORM'):
            out["Value"] = Vector(self.inputs["X"].default_value).normalized()
        elif (self.inputs["Operation"].default_value == 'ORTHO'):
            out["Value"] = Vector(self.inputs["X"].default_value).orthogonal()
        elif (self.inputs["Operation"].default_value == 'LERP'):
            out["Value"] = Vector(self.inputs["X"].default_value).lerp(Vector(self.inputs["Y"].default_value), self.inputs["K"].default_value)
        elif (self.inputs["Operation"].default_value == 'SLERP'):
            out["Value"] = Vector(self.inputs["X"].default_value).slerp(Vector(self.inputs["Y"].default_value), self.inputs["K"].default_value)
        return out