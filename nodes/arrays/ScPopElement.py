import bpy
import math

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScPopElement(Node, ScNode):
    bl_idname = "ScPopElement"
    bl_label = "Pop Element"
    bl_icon = 'MOD_ARRAY'

    in_index: IntProperty(default=-1, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketNumber", "Index").init("in_index")
        self.outputs.new("ScNodeSocketArray", "New Array")
        self.outputs.new("ScNodeSocketUniversal", "Element")

    def post_execute(self):
        out = super().post_execute()
        arr = eval(self.inputs["Array"].default_value)
        try:
            elem = arr.pop(int(self.inputs["Index"].default_value))
        except:
            elem = None
        out["New Array"] = repr(arr)
        out["Element"] = repr(elem)
        return out