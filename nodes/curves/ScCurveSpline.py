import bpy

from bpy.props import EnumProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScCurveOperatorNode

class ScCurveSpline(Node, ScCurveOperatorNode):
    bl_idname = "ScCurveSpline"
    bl_label = "Curve Spline Properties"
    
    in_tilt: EnumProperty(name="Tilt", items=[("LINEAR", "Linear", ""), ("CARDINAL", "Cardinal", ""), ("BSPLINE", "Bspline", ""), ("EASE", "Ease", "")], default="LINEAR", update=ScNode.update_value)
    in_radius: EnumProperty(name="Radius", items=[("LINEAR", "Linear", ""), ("CARDINAL", "Cardinal", ""), ("BSPLINE", "Bspline", ""), ("EASE", "Ease", "")], default="LINEAR", update=ScNode.update_value)
    in_resolution: IntProperty(default=1, min=1, max=1024, soft_max=64, update=ScNode.update_value)
    in_cyclic: BoolProperty(default=True, update=ScNode.update_value)
    in_smooth: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Tilt").init("in_tilt")
        self.inputs.new("ScNodeSocketString", "Radius").init("in_radius")
        self.inputs.new("ScNodeSocketNumber", "Resolution").init("in_resolution")
        self.inputs.new("ScNodeSocketBool", "Cyclic").init("in_cyclic", True)
        self.inputs.new("ScNodeSocketBool", "Smooth").init("in_smooth", True)
    
    def error_condition(self):
        return(
            super().error_condition()
            or (not self.inputs["Tilt"].default_value in ['LINEAR', 'CARDINAL', 'BSPLINE', 'EASE'])
            or (not self.inputs["Radius"].default_value in ['LINEAR', 'CARDINAL', 'BSPLINE', 'EASE'])
            or (int(self.inputs["Resolution"].default_value) < 1 or int(self.inputs["Resolution"].default_value) > 1024)
        )
    
    def functionality(self):
        self.inputs["Curve"].default_value.data.splines[0].tilt_interpolation = self.inputs["Tilt"].default_value
        self.inputs["Curve"].default_value.data.splines[0].radius_interpolation = self.inputs["Radius"].default_value
        self.inputs["Curve"].default_value.data.splines[0].resolution_u = int(self.inputs["Resolution"].default_value)
        self.inputs["Curve"].default_value.data.splines[0].use_cyclic_u = self.inputs["Cyclic"].default_value
        self.inputs["Curve"].default_value.data.splines[0].use_smooth = self.inputs["Smooth"].default_value