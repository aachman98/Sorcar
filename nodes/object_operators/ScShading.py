import bpy

from bpy.props import FloatProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScShading(Node, ScObjectOperatorNode):
    bl_idname = "ScShading"
    bl_label = "Shading"
    bl_icon = 'SHADING_RENDERED'
        
    in_shading: EnumProperty(items=[("SMOOTH", "Smooth", ""), ("FLAT", "Flat", "")], default="FLAT", update=ScNode.update_value)
    in_auto: BoolProperty(update=ScNode.update_value)
    in_angle: FloatProperty(default=0.523599, min=0.0, max=3.14159, unit="ROTATION", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Shading").init("in_shading", True)
        self.inputs.new("ScNodeSocketBool", "Auto Smooth").init("in_auto")
        self.inputs.new("ScNodeSocketNumber", "Angle").init("in_angle")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Shading"].default_value in ['SMOOTH', 'FLAT'])
            or (self.inputs["Angle"].default_value < 0.0 or self.inputs["Angle"].default_value > 3.14159)
        )
    
    def functionality(self):
        super().functionality()
        if (self.inputs["Shading"].default_value == "FLAT"):
            bpy.ops.object.shade_flat()
        else:
            bpy.ops.object.shade_smooth()
        self.inputs["Object"].default_value.data.use_auto_smooth = self.inputs["Auto Smooth"].default_value
        self.inputs["Object"].default_value.data.auto_smooth_angle = self.inputs["Angle"].default_value