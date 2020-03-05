import bpy

from bpy.props import PointerProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import remove_object, focus_on_object

class ScCustomCurve(Node, ScNode):
    bl_idname = "ScCustomCurve"
    bl_label = "Custom Curve"

    def curve_poll(self, object):
        return object.type == "CURVE"
    in_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value, poll=curve_poll)
    in_hide: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        self.node_executable = True
        self.use_custom_color = True
        self.set_color()
        self.inputs.new("ScNodeSocketCurve", "Curve").init("in_obj", True)
        self.inputs.new("ScNodeSocketBool", "Hide Original").init("in_hide")
        self.outputs.new("ScNodeSocketCurve", "Curve")
    
    def error_condition(self):
        return (
            self.inputs["Curve"].default_value == None
        )
    
    def pre_execute(self):
        remove_object(self.outputs["Curve"].default_value)
        self.inputs["Curve"].default_value.hide_set(False)
        focus_on_object(self.inputs["Curve"].default_value)
    
    def functionality(self):
        bpy.ops.object.duplicate()
    
    def post_execute(self):
        if (self.inputs["Hide Original"].default_value):
            self.inputs["Curve"].default_value.hide_set(True)
        return {"Curve": bpy.context.active_object}