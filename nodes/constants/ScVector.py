import bpy
import mathutils

from bpy.props import EnumProperty, FloatProperty, IntProperty, BoolProperty
from bpy.types import Node
from mathutils import Vector
from .._base.node_base import ScNode

class ScVector(Node, ScNode):
    bl_idname = "ScVector"
    bl_label = "Vector"

    in_uniform: EnumProperty(items=[("NONE", "None", "-"), ("XY", "XY", "-"), ("YZ", "YZ", "-"), ("XZ", "XZ", "-"), ("XYZ", "XYZ", "-")], default="NONE", update=ScNode.update_value)
    in_x: FloatProperty(update=ScNode.update_value)
    in_y: FloatProperty(update=ScNode.update_value)
    in_z: FloatProperty(update=ScNode.update_value)
    in_random: BoolProperty(update=ScNode.update_value)
    in_seed: IntProperty(update=ScNode.update_value)
    in_unit: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Uniform").init("in_uniform")
        self.inputs.new("ScNodeSocketNumber", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketNumber", "Y").init("in_y", True)
        self.inputs.new("ScNodeSocketNumber", "Z").init("in_z", True)
        self.inputs.new("ScNodeSocketBool", "Random").init("in_random", True)
        self.inputs.new("ScNodeSocketNumber", "Seed").init("in_seed")
        self.inputs.new("ScNodeSocketBool", "Unit Vector").init("in_unit")
        self.outputs.new("ScNodeSocketVector", "Value")
    
    def error_condition(self):
        return (
            not self.inputs["Uniform"].default_value in ["NONE", "XY", "YZ", "XZ", "XYZ"]
        )
    
    def post_execute(self):
        out = {}
        if (self.inputs["Random"].default_value):
            if (not int(self.inputs["Seed"].default_value) == 0):
                if (self.first_time):
                    mathutils.noise.seed_set(int(self.inputs["Seed"].default_value))
            if (self.inputs["Unit Vector"].default_value):
                out["Value"] = mathutils.noise.random_unit_vector(size=3)
            else:
                out["Value"] = mathutils.noise.random_vector(size=3)
        else:
            if (self.inputs["Uniform"].default_value == "NONE"):
                out["Value"] = Vector((self.inputs["X"].default_value, self.inputs["Y"].default_value, self.inputs["Z"].default_value))
            elif (self.inputs["Uniform"].default_value == "XY"):
                out["Value"] = Vector((self.inputs["X"].default_value, self.inputs["X"].default_value, self.inputs["Z"].default_value))
            elif (self.inputs["Uniform"].default_value == "YZ"):
                out["Value"] = Vector((self.inputs["X"].default_value, self.inputs["Y"].default_value, self.inputs["Y"].default_value))
            elif (self.inputs["Uniform"].default_value == "XZ"):
                out["Value"] = Vector((self.inputs["X"].default_value, self.inputs["Y"].default_value, self.inputs["X"].default_value))
            elif (self.inputs["Uniform"].default_value == "XYZ"):
                out["Value"] = Vector((self.inputs["X"].default_value, self.inputs["X"].default_value, self.inputs["X"].default_value))
        return out