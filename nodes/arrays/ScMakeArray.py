import bpy
import math

from bpy.types import Node
from .._base.node_base import ScNode
from ...debug import log

class ScMakeArray(Node, ScNode):
    bl_idname = "ScMakeArray"
    bl_label = "Make Array"
    bl_icon = 'LONGDISPLAY'

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArrayPlaceholder", "...")
        self.outputs.new("ScNodeSocketArray", "Array")
    
    def init_in(self, forced): # Should be a behaviour of socket
        log(self.id_data.name, self.name, "init_in", "Forced="+str(forced), 3)
        for i in self.inputs:
            if (not i.bl_rna.name == "ScNodeSocketArrayPlaceholder"):
                if (i.is_linked):
                    if (not i.execute(forced)):
                        return False
                else:
                    self.inputs.remove(i)
        return True

    def post_execute(self):
        out = super().post_execute()
        arr = []
        for i in self.inputs:
            if (not i.bl_rna.name == "ScNodeSocketArrayPlaceholder"):
                if (i.bl_rna.name == "ScNodeSocketVector"):
                    arr.append(list(i.default_value))
                else:
                    arr.append(i.default_value)
        out["Array"] = repr(arr)
        return out