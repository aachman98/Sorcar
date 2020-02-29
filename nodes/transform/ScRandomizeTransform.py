import bpy

from mathutils import Vector
from bpy.props import IntProperty, FloatVectorProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScRandomizeTransform(Node, ScObjectOperatorNode):
    bl_idname = "ScRandomizeTransform"
    bl_label = "Randomize Transform"

    in_seed: IntProperty(min=0, max=10000, update=ScNode.update_value)
    in_delta: BoolProperty(update=ScNode.update_value)
    in_use_loc: BoolProperty(default=True, update=ScNode.update_value)
    in_loc: FloatVectorProperty(min=-100.0, max=100.0, update=ScNode.update_value)
    in_use_rot: BoolProperty(default=True, update=ScNode.update_value)
    in_rot: FloatVectorProperty(min=-3.14159, max=3.14159, unit='ROTATION', update=ScNode.update_value)
    in_use_scale: BoolProperty(default=True, update=ScNode.update_value)
    in_scale_even: BoolProperty(update=ScNode.update_value)
    in_scale: FloatVectorProperty(default=(1.0, 1.0, 1.0), min=-100.0, max=100.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Random Seed").init("in_seed", True)
        self.inputs.new("ScNodeSocketBool", "Transform Delta").init("in_delta")
        self.inputs.new("ScNodeSocketBool", "Randomize Location").init("in_use_loc", True)
        self.inputs.new("ScNodeSocketVector", "Location").init("in_loc", True)
        self.inputs.new("ScNodeSocketBool", "Randomize Rotation").init("in_use_rot")
        self.inputs.new("ScNodeSocketVector", "Rotation").init("in_rot")
        self.inputs.new("ScNodeSocketBool", "Randomize Scale").init("in_use_scale")
        self.inputs.new("ScNodeSocketBool", "Scale Even").init("in_scale_even")
        self.inputs.new("ScNodeSocketVector", "Scale").init("in_scale")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Random Seed"].default_value) < 0 or int(self.inputs["Random Seed"].default_value) > 10000)
            or (Vector(self.inputs["Location"].default_value).magnitude < -100.0 or Vector(self.inputs["Location"].default_value).magnitude > 100.0)
            or (Vector(self.inputs["Rotation"].default_value).magnitude < -3.14159 or Vector(self.inputs["Rotation"].default_value).magnitude > 3.14159)
            or (Vector(self.inputs["Scale"].default_value).magnitude < -100.0 or Vector(self.inputs["Scale"].default_value).magnitude > 100.0)
        )
    
    def functionality(self):
        bpy.ops.object.randomize_transform(
            random_seed = int(self.inputs["Random Seed"].default_value),
            use_delta = self.inputs["Transform Delta"].default_value,
            use_loc = self.inputs["Randomize Location"].default_value,
            loc = self.inputs["Location"].default_value,
            use_rot = self.inputs["Randomize Rotation"].default_value,
            rot = self.inputs["Rotation"].default_value,
            use_scale = self.inputs["Randomize Scale"].default_value,
            scale_even = self.inputs["Scale Even"].default_value,
            scale = self.inputs["Scale"].default_value
        )