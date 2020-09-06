import bpy

from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScPointNormals(Node, ScEditOperatorNode):
    bl_idname = "ScPointNormals"
    bl_label = "Point Normals"
    
    in_target_location: FloatVectorProperty(update=ScNode.update_value)
    in_invert: BoolProperty(update=ScNode.update_value)
    in_align: BoolProperty(update=ScNode.update_value)
    in_spherize: BoolProperty(update=ScNode.update_value)
    in_spherize_strength: FloatProperty(default=0.1, min=0.0, max=1.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Target").init("in_target_location", True)
        self.inputs.new("ScNodeSocketBool", "Invert").init("in_invert", True)
        self.inputs.new("ScNodeSocketBool", "Align").init("in_align")
        self.inputs.new("ScNodeSocketBool", "Spherize").init("in_spherize")
        self.inputs.new("ScNodeSocketNumber", "Spherize Strength").init("in_spherize_strength")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Spherize Strength"].default_value < 0.0 or self.inputs["Spherize Strength"].default_value > 1.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.point_normals(
            target_location = self.inputs["Target"].default_value,
            invert = self.inputs["Invert"].default_value,
            align = self.inputs["Align"].default_value,
            spherize = self.inputs["Spherize"].default_value,
            spherize_strength = self.inputs["Spherize Strength"].default_value
        )