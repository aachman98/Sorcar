import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScGetChildren(Node, ScNode):
    bl_idname = "ScGetChildren"
    bl_label = "Get Children"
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.outputs.new("ScNodeSocketArray", "Children")

    def error_condition(self):
        return (
            self.inputs["Object"].default_value == None
        )
    
    def post_execute(self):
        return {
            "Children": repr(list(self.inputs["Object"].default_value.children))
        }