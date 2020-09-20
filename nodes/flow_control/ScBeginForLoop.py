import bpy

from bpy.props import BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...debug import log

class ScBeginForLoop(Node, ScNode):
    bl_idname = "ScBeginForLoop"
    bl_label = "Begin For Loop"
    bl_icon = 'TRACKING_REFINE_FORWARDS'

    prop_locked: BoolProperty()
    out_counter: IntProperty()

    def reset(self, execute):
        if (execute):
            self.prop_locked = False
        super().reset(execute)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.outputs.new("ScNodeSocketInfo", "End For Loop")
        self.outputs.new("ScNodeSocketUniversal", "Out")
        self.outputs.new("ScNodeSocketNumber", "Counter")
    
    def execute(self, forced=False):
        if (self.prop_locked):
            log(self.id_data.name, self.name, "execute", "Locked=True, Counter="+str(self.out_counter), 2)
            self.outputs["Counter"].default_value = self.out_counter
            self.set_color()
            return True
        else:
            log(self.id_data.name, self.name, "execute", "Locked=False, Counter=0", 2)
            self.prop_locked = True
            self.out_counter = 0
            return super().execute(forced)
    
    def post_execute(self):
        out = super().post_execute()
        out["Out"] = self.inputs["In"].default_value
        out["Counter"] = self.out_counter
        return out