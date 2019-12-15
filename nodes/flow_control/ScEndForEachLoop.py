import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScEndForEachLoop(Node, ScNode):
    bl_idname = "ScEndForEachLoop"
    bl_label = "End For-Each Loop"

    in_iterations: IntProperty(default=5, min=1, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketInfo", "Begin For-Each Loop")
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketArray", "Array")
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def init_in(self, forced):
        return (
            self.inputs["Begin For-Each Loop"].is_linked
            and self.inputs["Begin For-Each Loop"].links[0].from_node.execute(forced)
            and self.inputs["Array"].execute(forced)
        )
    
    def error_condition(self):
        return (
            len(eval(self.inputs["Array"].default_value)) == 0
        )
    
    def functionality(self):
        for i in eval(self.inputs["Array"].default_value):
            self.inputs["Begin For-Each Loop"].links[0].from_node.out_index += 1
            self.inputs["Begin For-Each Loop"].links[0].from_node.out_element = repr(i)
            self.inputs["In"].execute(True)
        self.inputs["Begin For-Each Loop"].links[0].from_node.prop_locked = False
    
    def post_execute(self):
        out = {}
        out["Out"] = self.inputs["In"].default_value
        return out