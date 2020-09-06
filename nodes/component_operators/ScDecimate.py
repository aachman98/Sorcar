import bpy

from bpy.props import FloatProperty, BoolProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScDecimate(Node, ScEditOperatorNode):
    bl_idname = "ScDecimate"
    bl_label = "Decimate"

    in_ratio: FloatProperty(default=1.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_use_vertex_group: BoolProperty(update=ScNode.update_value)
    in_vertex_group_factor: FloatProperty(default=1.0, min=0.0, max=1000.0, update=ScNode.update_value)
    in_invert_vertex_group: BoolProperty(update=ScNode.update_value)
    in_use_symmetry: BoolProperty(update=ScNode.update_value)
    in_symmetry_axis: EnumProperty(items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="Y", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Ratio").init("in_ratio", True)
        self.inputs.new("ScNodeSocketBool", "Vertex Group").init("in_use_vertex_group")
        self.inputs.new("ScNodeSocketNumber", "Weight").init("in_vertex_group_factor")
        self.inputs.new("ScNodeSocketBool", "Invert").init("in_invert_vertex_group")
        self.inputs.new("ScNodeSocketBool", "Symmetry").init("in_use_symmetry")
        self.inputs.new("ScNodeSocketString", "Symmetry Axis").init("in_symmetry_axis", True)

    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Ratio"].default_value < 0.0 or self.inputs["Ratio"].default_value > 1.0)
            or (self.inputs["Weight"].default_value < 0.0 or self.inputs["Weight"].default_value > 1000.0)
            or (not self.inputs["Symmetry Axis"].default_value in ['X', 'Y', 'Z'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.decimate(
            ratio = self.inputs["Ratio"].default_value,
            use_vertex_group = self.inputs["Vertex Group"].default_value,
            vertex_group_factor = self.inputs["Weight"].default_value,
            invert_vertex_group = self.inputs["Invert"].default_value,
            use_symmetry = self.inputs["Symmetry"].default_value,
            symmetry_axis = self.inputs["Symmetry Axis"].default_value
        )
    