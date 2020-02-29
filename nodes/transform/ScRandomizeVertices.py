import bpy

from bpy.props import IntProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScRandomizeVertices(Node, ScEditOperatorNode):
    bl_idname = "ScRandomizeVertices"
    bl_label = "Randomize Vertices"

    in_offset: FloatProperty(update=ScNode.update_value)
    in_uniform: FloatProperty(min=0.0, max=1.0, update=ScNode.update_value)
    in_normal: FloatProperty(min=0.0, max=1.0, update=ScNode.update_value)
    in_seed: IntProperty(min=0, max=10000, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Offset Amount").init("in_offset", True)
        self.inputs.new("ScNodeSocketNumber", "Uniform").init("in_uniform")
        self.inputs.new("ScNodeSocketNumber", "Normal").init("in_normal")
        self.inputs.new("ScNodeSocketNumber", "Random Seed").init("in_seed", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Uniform"].default_value < 0 or self.inputs["Uniform"].default_value > 1)
            or (self.inputs["Normal"].default_value < 0 or self.inputs["Normal"].default_value > 1)
            or (int(self.inputs["Random Seed"].default_value) < 0 or int(self.inputs["Random Seed"].default_value) > 10000)
        )
    
    def functionality(self):
        bpy.ops.transform.vertex_random(
            offset = self.inputs["Offset Amount"].default_value,
            uniform = self.inputs["Uniform"].default_value,
            normal = self.inputs["Normal"].default_value,
            seed = int(self.inputs["Random Seed"].default_value)
        )