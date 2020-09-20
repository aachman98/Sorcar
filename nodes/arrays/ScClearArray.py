import bpy
import math

from bpy.types import Node
from .._base.node_base import ScNode

class ScClearArray(Node, ScNode):
    bl_idname = "ScClearArray"
    bl_label = "Clear Array"
    bl_icon = 'CANCEL'

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.outputs.new("ScNodeSocketArray", "Empty Array")

    def post_execute(self):
        out = super().post_execute()
        arr = eval(self.inputs["Array"].default_value)
        arr.clear()
        out["Empty Array"] = repr(arr)
        return out