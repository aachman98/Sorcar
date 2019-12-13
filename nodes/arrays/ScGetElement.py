import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScGetElement(Node, ScNode):
    bl_idname = "ScGetElement"
    bl_label = "Get Element"
    
    in_index: IntProperty(min=0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketNumber", "Index").init("in_index", True)
        self.outputs.new("ScNodeSocketUniversal", "Element")
    
    def error_condition(self):
        return (
            (int(self.inputs["Index"].default_value) < 0 or int(self.inputs["Index"].default_value) >= len(eval(self.inputs["Array"].default_value)))
        )
    
    def post_execute(self):
        return {"Element": repr(eval(self.inputs["Array"].default_value)[int(self.inputs["Index"].default_value)])}