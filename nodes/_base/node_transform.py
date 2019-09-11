import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScTransformNode(ScNode):
    in_edit: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.inputs.new("ScNodeSocketBool", "Edit Mode").init("in_edit", True)
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            self.inputs["Object"].default_value == None
        )
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value, self.inputs["Edit Mode"].default_value)
    
    def post_execute(self):
        return {"Object": self.inputs["Object"].default_value}