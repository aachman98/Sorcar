import bpy

from bpy.props import BoolProperty, IntProperty, StringProperty
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
    
    def execute(self, forced=False):
        if (self.prop_locked):
            self.outputs["Element"].default_value = self.out_element
            self.outputs["Index"].default_value = self.out_index
            self.set_color()
            return True
        else:
            self.prop_locked = True
            self.out_index = 0
            return super().execute(forced)
    
    def post_execute(self):
        out = {}
        out["Out"] = self.inputs["In"].default_value
        out["Index"] = self.out_index
        return out