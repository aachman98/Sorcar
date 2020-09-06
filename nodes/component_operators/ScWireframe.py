import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScWireframe(Node, ScEditOperatorNode):
    bl_idname = "ScWireframe"
    bl_label = "Wireframe"
    
    in_thickness: FloatProperty(default=0.01, min=0.0, max=10000.0, update=ScNode.update_value)
    in_offset: FloatProperty(default=0.01, min=0.0, max=10000.0, update=ScNode.update_value)
    in_use_crease: BoolProperty(update=ScNode.update_value)
    in_crease_weight: FloatProperty(default=0.01, min=0.0, max=1000.0, update=ScNode.update_value)
    in_use_even_offset: BoolProperty(default=True, update=ScNode.update_value)
    in_use_relative_offset: BoolProperty(update=ScNode.update_value)
    in_use_boundary: BoolProperty(update=ScNode.update_value)
    in_use_replace: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Thickness").init("in_thickness", True)
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketBool", "Crease Edges").init("in_use_crease")
        self.inputs.new("ScNodeSocketNumber", "Crease Weight").init("in_crease_weight")
        self.inputs.new("ScNodeSocketBool", "Even Thickness").init("in_use_even_offset")
        self.inputs.new("ScNodeSocketBool", "Relative Thickness").init("in_use_relative_offset")
        self.inputs.new("ScNodeSocketBool", "Boundary").init("in_use_boundary")
        self.inputs.new("ScNodeSocketBool", "Replace Original").init("in_use_replace", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Thickness"].default_value < 0.0 or self.inputs["Thickness"].default_value > 10000.0)
            or (self.inputs["Offset"].default_value < 0.0 or self.inputs["Offset"].default_value > 10000.0)
            or (self.inputs["Crease Weight"].default_value < 0.0 or self.inputs["Crease Weight"].default_value > 1000.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.wireframe(
            thickness = self.inputs["Thickness"].default_value,
            offset = self.inputs["Offset"].default_value,
            use_crease = self.inputs["Crease Edges"].default_value,
            crease_weight = self.inputs["Crease Weight"].default_value,
            use_even_offset = self.inputs["Even Thickness"].default_value,
            use_relative_offset = self.inputs["Relative Thickness"].default_value,
            use_boundary = self.inputs["Boundary"].default_value,
            use_replace = self.inputs["Replace Original"].default_value
        )