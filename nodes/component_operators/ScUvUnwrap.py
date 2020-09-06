import bpy

from bpy.props import FloatProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScUvUnwrap(Node, ScEditOperatorNode):
    bl_idname = "ScUvUnwrap"
    bl_label = "UV Unwrap"
    
    in_method: EnumProperty(items=[('ANGLE_BASED', 'Angle Based', ''), ('CONFORMAL', 'Conformal', '')], default='ANGLE_BASED', update=ScNode.update_value)
    in_fill: BoolProperty(default=True, update=ScNode.update_value)
    in_aspect: BoolProperty(default=True, update=ScNode.update_value)
    in_subsurf: BoolProperty(update=ScNode.update_value)
    in_margin: FloatProperty(min=0.0, max=1.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Method").init("in_method", True)
        self.inputs.new("ScNodeSocketBool", "Fill Holes").init("in_fill")
        self.inputs.new("ScNodeSocketBool", "Correct Aspect").init("in_aspect")
        self.inputs.new("ScNodeSocketBool", "Use Subsurf Modifier").init("in_subsurf")
        self.inputs.new("ScNodeSocketNumber", "Margin").init("in_margin")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Method"].default_value in ['ANGLE_BASED', 'CONFORMAL'])
            or (self.inputs["Margin"].default_value < 0.0 or self.inputs["Margin"].default_value > 1.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.uv.unwrap(
            method = self.inputs["Method"].default_value,
            fill_holes = self.inputs["Fill Holes"].default_value,
            correct_aspect = self.inputs["Correct Aspect"].default_value,
            use_subsurf_data = self.inputs["Use Subsurf Modifier"].default_value,
            margin = self.inputs["Margin"].default_value
        )