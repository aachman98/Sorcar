import bpy
import mathutils

from bpy.props import BoolProperty, IntProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBool(Node, ScNode):
    bl_idname = "ScBool"
    bl_label = "Bool"

    prop_bool: BoolProperty(name="Bool", update=ScNode.update_value)
    in_random: BoolProperty(update=ScNode.update_value)
    in_seed: IntProperty(update=ScNode.update_value)
    in_weight: FloatProperty(default=0.5, min=0.0, max=1.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Random").init("in_random", True)
        self.inputs.new("ScNodeSocketNumber", "Seed").init("in_seed")
        self.inputs.new("ScNodeSocketNumber", "Weight").init("in_weight")
        self.outputs.new("ScNodeSocketBool", "Value")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Random"].default_value):
            layout.prop(self, "prop_bool")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Weight"].default_value < 0.0 or self.inputs["Weight"].default_value > 1.0)
        )
    
    def post_execute(self):
        out = {}
        if (self.inputs["Random"].default_value):
            if (not int(self.inputs["Seed"].default_value) == 0):
                if (self.first_time):
                    mathutils.noise.seed_set(int(self.inputs["Seed"].default_value))
            out["Value"] = mathutils.noise.random() < self.inputs["Weight"].default_value
        else:
            out["Value"] = self.prop_bool
        return out