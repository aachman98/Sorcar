import bpy

from bpy.props import StringProperty, FloatProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object, remove_object

class ScText(Node, ScNode):
    bl_idname = "ScText"
    bl_label = "Text"
    
    in_name: StringProperty(default="Curve", update=ScNode.update_value)
    in_text: StringProperty(default="Text", update=ScNode.update_value)
    in_radius: FloatProperty(default=1.0, min=0.0, update=ScNode.update_value)
    out_curve: PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Name").init("in_name")
        self.inputs.new("ScNodeSocketString", "Text").init("in_text", True)
        self.inputs.new("ScNodeSocketNumber", "Radius").init("in_radius", True)
        self.outputs.new("ScNodeSocketCurve", "Curve")
    
    def error_condition(self):
        return (
            self.inputs["Name"].default_value == ""
            or self.inputs["Text"].default_value == ""
            or self.inputs["Radius"].default_value <= 0
        )
    
    def pre_execute(self):
        if (self.out_curve):
            remove_object(self.out_curve)
    
    def functionality(self):
        bpy.ops.object.text_add(
            radius = self.inputs["Radius"].default_value,
            align = 'CURSOR'
        )
    
    def post_execute(self):
        self.out_curve = bpy.context.active_object
        self.out_curve.name = self.inputs["Name"].default_value
        if (self.out_curve.data):
            self.out_curve.data.name = self.out_curve.name
            self.out_curve.data.body = self.inputs["Text"].default_value
        return {"Curve": self.out_curve}