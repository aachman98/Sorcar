import bpy
import math

from bpy.types import Node
from .._base.node_base import ScNode

class ScReverseArray(Node, ScNode):
    bl_idname = "ScReverseArray"
    bl_label = "Reverse Array"
    bl_icon = 'ARROW_LEFTRIGHT'

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.outputs.new("ScNodeSocketArray", "New Array")

    def post_execute(self):
        out = super().post_execute()
        arr = eval(self.inputs["Array"].default_value)
        arr.reverse()
        out["New Array"] = repr(arr)
        return out