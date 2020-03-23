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
            self.inputs["Object"].default_value == None
        )
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value, True)
    
    def post_execute(self):
        return {"Object": self.inputs["Object"].default_value}

class ScObjectOperatorNode(ScNode):
    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            self.inputs["Object"].default_value == None
        )
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value)
    
    def post_execute(self):
        return {"Object": self.inputs["Object"].default_value}

class ScCurveOperatorNode(ScNode):
    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketCurve", "Curve")
        self.outputs.new("ScNodeSocketCurve", "Curve")
    
    def error_condition(self):
        return (
            self.inputs["Curve"].default_value == None
        )
    
    def pre_execute(self):
        focus_on_object(self.inputs["Curve"].default_value)
    
    def post_execute(self):
        return {"Curve": self.inputs["Curve"].default_value}