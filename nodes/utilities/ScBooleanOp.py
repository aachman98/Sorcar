import bpy

from bpy.props import EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBooleanOp(Node, ScNode):
    bl_idname = "ScBooleanOp"
    bl_label = "Boolean Operation"
    bl_icon = 'SELECT_SUBTRACT'

    in_x: BoolProperty(name="X", update=ScNode.update_value)
    in_y: BoolProperty(name="Y", update=ScNode.update_value)
    in_op: EnumProperty(items=[("AND", "X and Y", "&&"), ("OR", "X or Y", "||"), ("EQUAL", "X equals Y", "=="), ("NOTEQUAL", "X not equals Y", "!="), ("NOTX", "not X", "!X"), ("NOTY", "not Y", "!Y")], default="OR", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketBool", "Y").init("in_y", True)
        self.inputs.new("ScNodeSocketString", "Operation").init("in_op", True)
        self.outputs.new("ScNodeSocketBool", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Operation"].default_value in ['AND', 'OR', 'EQUAL', 'NOTEQUAL', 'NOTX', 'NOTY'])
        )
    
    def post_execute(self):
        out = super().post_execute()
        if (self.inputs["Operation"].default_value == "AND"):
            out["Value"] = self.inputs["X"].default_value and self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "OR"):
            out["Value"] = self.inputs["X"].default_value or self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "EQUAL"):
            out["Value"] = self.inputs["X"].default_value == self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "NOTEQUAL"):
            out["Value"] = self.inputs["X"].default_value != self.inputs["Y"].default_value
        elif (self.inputs["Operation"].default_value == "NOTX"):
            out["Value"] = not self.inputs["X"].default_value
        elif (self.inputs["Operation"].default_value == "NOTY"):
            out["Value"] = not self.inputs["Y"].default_value
        return out