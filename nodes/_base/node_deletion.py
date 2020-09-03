import bpy

from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScDeletionNode(ScNode):
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