import bpy

from mathutils import Vector
from bpy.props import FloatProperty, FloatVectorProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScBisect(Node, ScEditOperatorNode):
    bl_idname = "ScBisect"
    bl_label = "Bisect"
    
    in_plane_co: FloatVectorProperty(update=ScNode.update_value)
    in_plane_no: FloatVectorProperty(default=(0.0, 0.0, 1.0), min=-1, max=1, update=ScNode.update_value)
    in_use_fill: BoolProperty(update=ScNode.update_value)
    in_clear_inner: BoolProperty(update=ScNode.update_value)
    in_clear_outer: BoolProperty(update=ScNode.update_value)
    in_threshold: FloatProperty(default=0.0001, min=0.0, max=1.0, update=ScNode.update_value)
    in_xstart: IntProperty(update=ScNode.update_value)
    in_xend: IntProperty(update=ScNode.update_value)
    in_ystart: IntProperty(update=ScNode.update_value)
    in_yend: IntProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Plane Point").init("in_plane_co", True)
        self.inputs.new("ScNodeSocketVector", "Plane Normal").init("in_plane_no", True)
        self.inputs.new("ScNodeSocketBool", "Fill").init("in_use_fill")
        self.inputs.new("ScNodeSocketBool", "Clear Inner").init("in_clear_inner")
        self.inputs.new("ScNodeSocketBool", "Clear Outer").init("in_clear_outer")
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
        self.inputs.new("ScNodeSocketNumber", "X Start").init("in_xstart")
        self.inputs.new("ScNodeSocketNumber", "X End").init("in_xend")
        self.inputs.new("ScNodeSocketNumber", "Y Start").init("in_ystart")
        self.inputs.new("ScNodeSocketNumber", "Y End").init("in_yend")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Threshold"].default_value < 0.0 or self.inputs["Threshold"].default_value > 10.0)
            or (Vector(self.inputs["Plane Normal"].default_value).magnitude == 0.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.bisect(
            plane_co = self.inputs["Plane Point"].default_value,
            plane_no = self.inputs["Plane Normal"].default_value,
            use_fill = self.inputs["Fill"].default_value,
            clear_inner = self.inputs["Clear Inner"].default_value,
            clear_outer = self.inputs["Clear Outer"].default_value,
            threshold = self.inputs["Threshold"].default_value,
            xstart = int(self.inputs["X Start"].default_value),
            xend = int(self.inputs["X End"].default_value),
            ystart = int(self.inputs["Y Start"].default_value),
            yend = int(self.inputs["Y End"].default_value)
        )