import bpy
import mathutils

from bpy.props import EnumProperty, FloatProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScNumber(Node, ScNode):
    bl_idname = "ScNumber"
    bl_label = "Number"

    prop_type: EnumProperty(name="Type", items=[("FLOAT", "Float", ""), ("INT", "Integer", ""), ("ANGLE", "Angle", "")], default="FLOAT", update=ScNode.update_value)
    prop_float: FloatProperty(name="Float", update=ScNode.update_value)
    prop_int: IntProperty(name="Integer", update=ScNode.update_value)
    prop_angle: FloatProperty(name="Angle", unit="ROTATION", update=ScNode.update_value)
    in_random: BoolProperty(update=ScNode.update_value)
    in_seed: IntProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Random").init("in_random", True)
        self.inputs.new("ScNodeSocketNumber", "Seed").init("in_seed")
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Random"].default_value):
            layout.prop(self, "prop_type", expand=True)
            if (self.prop_type == "FLOAT"):
                layout.prop(self, "prop_float")
            elif (self.prop_type == "INT"):
                layout.prop(self, "prop_int")
            elif (self.prop_type == "ANGLE"):
                layout.prop(self, "prop_angle")
    
    def post_execute(self):
        out = {}
        if (self.inputs["Random"].default_value):
            if (not int(self.inputs["Seed"].default_value) == 0):
                if (self.first_time):
                    mathutils.noise.seed_set(int(self.inputs["Seed"].default_value))
            out["Value"] = mathutils.noise.random()
        else:
            if (self.prop_type == "FLOAT"):
                out["Value"] = self.prop_float
            elif (self.prop_type == "INT"):
                out["Value"] = self.prop_int
            elif (self.prop_type == "ANGLE"):
                out["Value"] = self.prop_angle
        return out