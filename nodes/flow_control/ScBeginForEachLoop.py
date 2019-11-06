import bpy

from bpy.props import IntProperty, BoolProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBeginForEachLoop(Node, ScNode):
    bl_idname = "ScBeginForEachLoop"
    bl_label = "Begin For-Each Loop"

    prop_locked: BoolProperty()
    out_element: StringProperty()
    out_index: IntProperty()

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.outputs.new("ScNodeSocketInfo", "End For-Each Loop")
        self.outputs.new("ScNodeSocketUniversal", "Out")
        self.outputs.new("ScNodeSocketUniversal", "Element")
        self.outputs.new("ScNodeSocketNumber", "Index")
    
    def error_condition(self):
        return (
            not self.outputs["End For-Each Loop"].is_linked
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
        out["Element"] = self.out_element
        out["Index"] = self.out_index
        return out