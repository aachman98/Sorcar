import bpy

from bpy.props import FloatProperty, IntProperty, BoolProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScSubdivide(Node, ScEditOperatorNode):
    bl_idname = "ScSubdivide"
    bl_label = "Subdivide"
    
    in_number_cuts: IntProperty(default=1, min=1, max=100, update=ScNode.update_value)
    in_smoothness: FloatProperty(min=0.0, max=1000.0, update=ScNode.update_value)
    in_ngon: BoolProperty(update=ScNode.update_value)
    in_quadcorner: EnumProperty(items=[("INNERVERT", "Inner Vertices", ""), ("PATH", "Path", ""), ("STRAIGHT_CUT", "Straight Cut", ""), ("FAN", "Fan", "")], default="STRAIGHT_CUT", update=ScNode.update_value)
    in_fractal: FloatProperty(min=0.0, max=1000000, update=ScNode.update_value)
    in_fractal_along_normal: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_seed: IntProperty(min=0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Number of Cuts").init("in_number_cuts", True)
        self.inputs.new("ScNodeSocketNumber", "Smoothness").init("in_smoothness", True)
        self.inputs.new("ScNodeSocketBool", "Create N-Gons").init("in_ngon")
        self.inputs.new("ScNodeSocketString", "Quad Corner Type").init("in_quadcorner")
        self.inputs.new("ScNodeSocketNumber", "Fractal").init("in_fractal", True)
        self.inputs.new("ScNodeSocketNumber", "Along Normal").init("in_fractal_along_normal")
        self.inputs.new("ScNodeSocketNumber", "Random Seed").init("in_seed")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Number of Cuts"].default_value) < 1 or int(self.inputs["Number of Cuts"].default_value) > 100)
            or (self.inputs["Smoothness"].default_value < 0.0 or self.inputs["Smoothness"].default_value > 1000.0)
            or (not self.inputs["Quad Corner Type"].default_value in ['INNERVERT', 'PATH', 'STRAIGHT_CUT', 'FAN'])
            or (self.inputs["Fractal"].default_value < 0.0 or self.inputs["Fractal"].default_value > 1000000.0)
            or (self.inputs["Along Normal"].default_value < 0.0 or self.inputs["Along Normal"].default_value > 1.0)
            or int(self.inputs["Random Seed"].default_value) < 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.subdivide(
            number_cuts = int(self.inputs["Number of Cuts"].default_value),
            smoothness = self.inputs["Smoothness"].default_value,
            ngon = self.inputs["Create N-Gons"].default_value,
            quadcorner = self.inputs["Quad Corner Type"].default_value,
            fractal = self.inputs["Fractal"].default_value,
            fractal_along_normal = self.inputs["Along Normal"].default_value,
            seed = int(self.inputs["Random Seed"].default_value)
        )