import bpy

from bpy.props import IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBeginForLoop(Node, ScNode):
    bl_idname = "ScBeginForLoop"
    bl_label = "Begin For Loop"

    prop_locked: BoolProperty()
    out_counter: IntProperty()

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.outputs.new("ScNodeSocketInfo", "End For Loop")
        self.outputs.new("ScNodeSocketUniversal", "Out")
        self.outputs.new("ScNodeSocketNumber", "Counter")
    
    def error_condition(self):
        return (
            not self.outputs["End For Loop"].is_linked
        )
    
    def execute(self, forced=False):
        if (self.prop_locked):
            return self.init_out(self.post_execute())
        else:
            self.prop_locked = True
            return super().execute(forced)
    
    def post_execute(self):
        out = {}
        out["Out"] = self.inputs["In"].default_value
        out["Counter"] = self.out_counter
        return out