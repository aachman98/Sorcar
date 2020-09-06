import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScInset(Node, ScEditOperatorNode):
    bl_idname = "ScInset"
    bl_label = "Inset"
    
    in_thickness: FloatProperty(default=0.01, min=0.0, update=ScNode.update_value)
    in_depth: FloatProperty(update=ScNode.update_value)
    in_boundary: BoolProperty(default=True, update=ScNode.update_value)
    in_even_offset: BoolProperty(default=True, update=ScNode.update_value)
    in_relative_offset: BoolProperty(update=ScNode.update_value)
    in_edge_rail: BoolProperty(update=ScNode.update_value)
    in_outset: BoolProperty(update=ScNode.update_value)
    in_select_inset: BoolProperty(update=ScNode.update_value)
    in_individual: BoolProperty(update=ScNode.update_value)
    in_interpolate: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Thickness").init("in_thickness", True)
        self.inputs.new("ScNodeSocketNumber", "Depth").init("in_depth", True)
        self.inputs.new("ScNodeSocketBool", "Individual").init("in_individual", True)
        self.inputs.new("ScNodeSocketBool", "Select Inset").init("in_select_inset")
        self.inputs.new("ScNodeSocketBool", "Boundary").init("in_boundary")
        self.inputs.new("ScNodeSocketBool", "Even Offset").init("in_even_offset")
        self.inputs.new("ScNodeSocketBool", "Edge Rail").init("in_edge_rail")
        self.inputs.new("ScNodeSocketBool", "Outset").init("in_outset")
        self.inputs.new("ScNodeSocketBool", "Relative Offset").init("in_relative_offset")
        self.inputs.new("ScNodeSocketBool", "Interpolate").init("in_interpolate")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Thickness"].default_value < 0.0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.inset(
            use_boundary = self.inputs["Boundary"].default_value,
            use_even_offset = self.inputs["Even Offset"].default_value,
            use_relative_offset = self.inputs["Relative Offset"].default_value,
            use_edge_rail = self.inputs["Edge Rail"].default_value,
            thickness = self.inputs["Thickness"].default_value,
            depth = self.inputs["Depth"].default_value,
            use_outset = self.inputs["Outset"].default_value,
            use_select_inset = self.inputs["Select Inset"].default_value,
            use_individual = self.inputs["Individual"].default_value,
            use_interpolate = self.inputs["Interpolate"].default_value
        )
