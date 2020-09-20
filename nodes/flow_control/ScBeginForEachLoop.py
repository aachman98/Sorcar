import bpy

from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...debug import log

class ScBeginForEachLoop(Node, ScNode):
    bl_idname = "ScBeginForEachLoop"
    bl_label = "Begin For-Each Loop"
    bl_icon = 'TRACKING_FORWARDS'

    prop_locked: BoolProperty()
    out_element: StringProperty()
    out_index: IntProperty()

    def reset(self, execute):
        if (execute):
            self.prop_locked = False
        super().reset(execute)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.outputs.new("ScNodeSocketInfo", "End For-Each Loop")
        self.outputs.new("ScNodeSocketUniversal", "Out")
        self.outputs.new("ScNodeSocketUniversal", "Element")
        self.outputs.new("ScNodeSocketNumber", "Index")
    
    def execute(self, forced=False):
        if (self.prop_locked):
            log(self.id_data.name, self.name, "execute", "Locked=True, Index="+str(self.out_index)+", Element="+self.out_element, 2)
            self.outputs["Element"].default_value = self.out_element
            self.outputs["Index"].default_value = self.out_index
            self.set_color()
            return True
        else:
            log(self.id_data.name, self.name, "execute", "Locked=False, Index=0, Element="+self.out_element, 2)
            self.prop_locked = True
            self.out_index = 0
            return super().execute(forced)
    
    def post_execute(self):
        out = super().post_execute()
        out["Out"] = self.inputs["In"].default_value
        out["Index"] = self.out_index
        return out