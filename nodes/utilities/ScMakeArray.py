import bpy
import math

from bpy.props import EnumProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScMakeArray(Node, ScNode):
    bl_idname = "ScMakeArray"
    bl_label = "Make Array"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArrayPlaceholder", "...")
        self.outputs.new("ScNodeSocketArray", "Array")
    
    def init_in(self, forced):
        for i in self.inputs:
            if (not i.bl_rna.name == "ScNodeSocketArrayPlaceholder"):
                if (i.is_linked):
                    if (not i.execute(forced)):
                        return False
                else:
                    self.inputs.remove(i)
        return True

    def post_execute(self):
        arr = []
        for i in self.inputs:
            if (not i.bl_rna.name == "ScNodeSocketArrayPlaceholder"):
                if (i.bl_rna.name == "ScNodeSocketVector"):
                    arr.append(list(i.default_value))
                else:
                    arr.append(i.default_value)
        return {"Array": repr(arr)}