import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScEndForEachLoop(Node, ScNode):
    bl_idname = "ScEndForEachLoop"
    bl_label = "End For-Each Loop"

    prop_counter: IntProperty()

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketInfo", "Begin For-Each Loop")
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketArray", "Array")
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def init_in(self, forced):
        return self.inputs["Array"].execute(forced)
    
    def error_condition(self):
        return (
            not self.inputs["Begin For-Each Loop"].is_linked
        )
    
    def pre_execute(self):
        self.prop_counter = -1
    
    def functionality(self):
        for i in eval(self.inputs["Array"].default_value):
            self.prop_counter += 1
            self.inputs["Begin For-Each Loop"].links[0].from_node.out_element = repr(i)
            self.inputs["Begin For-Each Loop"].links[0].from_node.out_index = self.prop_counter
            self.inputs["In"].execute(True)
    
    def post_execute(self):
        self.inputs["Begin For-Each Loop"].links[0].from_node.prop_locked = False
        return {"Out": self.inputs["In"].default_value}