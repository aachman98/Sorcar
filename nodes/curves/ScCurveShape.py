import bpy

from bpy.props import EnumProperty, IntProperty, BoolProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScCurveOperatorNode

class ScCurveShape(Node, ScCurveOperatorNode):
    bl_idname = "ScCurveShape"
    bl_label = "Curve Shape Properties"
    
    in_dimensions: EnumProperty(name="Dimensions", items=[("2D", "2D", ""), ("3D", "3D", "")], default="3D", update=ScNode.update_value)
    in_resolution: IntProperty(default=12, min=1, max=1024, soft_max=64, update=ScNode.update_value)
    in_render_resolution: IntProperty(min=0, max=1024, soft_max=64, update=ScNode.update_value)
    in_twist: EnumProperty(name="Twist Method", items=[("Z_UP", "Z-Up", ""), ("MINIMUM", "Minimum", ""), ("TANGENT", "Tangent", "")], default="MINIMUM", update=ScNode.update_value)
    in_smooth: FloatProperty(update=ScNode.update_value)
    in_fill_mode: EnumProperty(name="Fill Mode (3D)", items=[("FULL", "Full", ""), ("BACK", "Back", ""), ("FRONT", "Front", ""), ("HALF", "Half", "")], default="HALF", update=ScNode.update_value)
    in_fill_mode_2d: EnumProperty(name="Fill Mode (2D)", items=[("NONE", "None", ""), ("BACK", "Back", ""), ("FRONT", "Front", ""), ("BOTH", "Both", "")], default="NONE", update=ScNode.update_value)
    in_fill: BoolProperty(default=True, update=ScNode.update_value)
    in_radius: BoolProperty(default=True, update=ScNode.update_value)
    in_stretch: BoolProperty(update=ScNode.update_value)
    in_clamp: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Dimensions").init("in_dimensions", True)
        self.inputs.new("ScNodeSocketNumber", "Resolution Preview").init("in_resolution", True)
        self.inputs.new("ScNodeSocketNumber", "Resolution Render").init("in_render_resolution")
        self.inputs.new("ScNodeSocketString", "Twist Method").init("in_twist", True)
        self.inputs.new("ScNodeSocketNumber", "Smooth").init("in_smooth", True)
        self.inputs.new("ScNodeSocketString", "Fill Mode (3D)").init("in_fill_mode")
        self.inputs.new("ScNodeSocketString", "Fill Mode (2D)").init("in_fill_mode_2d")
        self.inputs.new("ScNodeSocketBool", "Fill Deformed").init("in_fill")
        self.inputs.new("ScNodeSocketBool", "Radius").init("in_radius", True)
        self.inputs.new("ScNodeSocketBool", "Stretch").init("in_stretch")
        self.inputs.new("ScNodeSocketBool", "Bounds Clamp").init("in_clamp")
    
    def error_condition(self):
        return(
            super().error_condition()
            or (not self.inputs["Dimensions"].default_value in ['2D', '3D'])
            or (int(self.inputs["Resolution Preview"].default_value) < 1 or int(self.inputs["Resolution Preview"].default_value) > 1024)
            or (int(self.inputs["Resolution Render"].default_value) < 0 or int(self.inputs["Resolution Render"].default_value) > 1024)
            or (not self.inputs["Twist Method"].default_value in ['Z_UP', 'MINIMUM', 'TANGENT'])
            or (not self.inputs["Fill Mode (3D)"].default_value in ['FULL', 'BACK', 'FRONT', 'HALF'])
            or (not self.inputs["Fill Mode (2D)"].default_value in ['NONE', 'BACK', 'FRONT', 'BOTH'])
        )
    
    def functionality(self):
        self.inputs["Curve"].default_value.data.dimensions = self.inputs["Dimensions"].default_value
        if (self.inputs["Dimensions"].default_value == "3D"):
            self.inputs["Curve"].default_value.data.fill_mode = self.inputs["Fill Mode (3D)"].default_value
        else:
            self.inputs["Curve"].default_value.data.fill_mode = self.inputs["Fill Mode (2D)"].default_value
        self.inputs["Curve"].default_value.data.resolution_u = int(self.inputs["Resolution Preview"].default_value)
        self.inputs["Curve"].default_value.data.render_resolution_u = int(self.inputs["Resolution Render"].default_value)
        self.inputs["Curve"].default_value.data.twist_mode = self.inputs["Twist Method"].default_value
        self.inputs["Curve"].default_value.data.twist_smooth = self.inputs["Smooth"].default_value
        self.inputs["Curve"].default_value.data.use_fill_deform = self.inputs["Fill Deformed"].default_value
        self.inputs["Curve"].default_value.data.use_radius = self.inputs["Radius"].default_value
        self.inputs["Curve"].default_value.data.use_stretch = self.inputs["Stretch"].default_value
        self.inputs["Curve"].default_value.data.use_deform_bounds = self.inputs["Bounds Clamp"].default_value