import bpy

from bpy.types import Node
from .._base.node_base import ScNode

class ScSettingNode(ScNode):
    def init(self, context):
        self.node_executable = False
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def error_condition(self):
        return (
            self.inputs["In"].default_value == None
        )
    
    def post_execute(self):
        return {"Out": self.inputs["In"].default_value}