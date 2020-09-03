import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScEditOperatorNode(ScNode):
    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Object"].default_value == None
        )
    
    def pre_execute(self):
        super().pre_execute()
        focus_on_object(self.inputs["Object"].default_value, True)
    
    def post_execute(self):
        out = super().post_execute()
        out["Object"] = self.inputs["Object"].default_value
        return out

class ScObjectOperatorNode(ScNode):
    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Object"].default_value == None
        )
    
    def pre_execute(self):
        super().pre_execute()
        focus_on_object(self.inputs["Object"].default_value)
    
    def post_execute(self):
        out = super().post_execute()
        out["Object"] = self.inputs["Object"].default_value
        return out

class ScCurveOperatorNode(ScNode):
    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketCurve", "Curve")
        self.outputs.new("ScNodeSocketCurve", "Curve")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Curve"].default_value == None
        )
    
    def pre_execute(self):
        super().pre_execute()
        focus_on_object(self.inputs["Curve"].default_value)
    
    def post_execute(self):
        out = super().post_execute()
        out["Curve"] = self.inputs["Curve"].default_value
        return out