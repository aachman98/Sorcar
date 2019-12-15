import bpy

from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBeginForEachComponentLoop(Node, ScNode):
    bl_idname = "ScBeginForEachComponentLoop"
    bl_label = "Begin For-Each Component Loop"

    prop_locked: BoolProperty()
    prop_components: StringProperty()
    out_index: IntProperty()

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "In")
        self.outputs.new("ScNodeSocketInfo", "End For-Each Component Loop")
        self.outputs.new("ScNodeSocketObject", "Out")
        self.outputs.new("ScNodeSocketNumber", "Index")
    
    def execute(self, forced=False):
        if (self.prop_locked):
            self.outputs["Index"].default_value = self.out_index
            self.set_color()
            return True
        else:
            self.prop_locked = True
            self.out_index = 0
            return super().execute(forced)
    
    def pre_execute(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        self.prop_components = repr([i.index for i in self.inputs["In"].default_value.data.polygons if i.select])
        bpy.ops.object.mode_set(mode="EDIT")
    
    def post_execute(self):
        out = {}
        out["Out"] = self.inputs["In"].default_value
        out["Index"] = self.out_index
        return out