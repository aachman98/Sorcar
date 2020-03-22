import bpy

from bpy.props import IntProperty, FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScAddUvSphere(Node, ScEditOperatorNode):
    bl_idname = "ScAddUvSphere"
    bl_label = "Add UV Sphere"

    in_uv: BoolProperty(default=True, update=ScNode.update_value)
    in_segment: IntProperty(default=32, min=3, max=10000000, update=ScNode.update_value)
    in_ring: IntProperty(default=16, min=3, max=10000000, update=ScNode.update_value)
    in_radius: FloatProperty(default=1.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Generate UVs").init("in_uv")
        self.inputs.new("ScNodeSocketNumber", "Segments").init("in_segment", True)
        self.inputs.new("ScNodeSocketNumber", "Rings").init("in_ring", True)
        self.inputs.new("ScNodeSocketNumber", "Radius").init("in_radius", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Segments"].default_value < 3 or self.inputs["Segments"].default_value > 10000000)
            or (self.inputs["Rings"].default_value < 3 or self.inputs["Rings"].default_value > 10000000)
            or self.inputs["Radius"].default_value < 0
        )
    
    def functionality(self):
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments = int(self.inputs["Segments"].default_value),
            ring_count = int(self.inputs["Rings"].default_value),
            radius = self.inputs["Radius"].default_value,
            calc_uvs = self.inputs["Generate UVs"].default_value
        )