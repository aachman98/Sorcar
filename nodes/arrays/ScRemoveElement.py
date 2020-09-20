import bpy
import math

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScRemoveElement(Node, ScNode):
    bl_idname = "ScRemoveElement"
    bl_label = "Remove Element"
    bl_icon = 'X'

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketUniversal", "Element")
        self.outputs.new("ScNodeSocketArray", "New Array")

    def post_execute(self):
        out = super().post_execute()
        arr = eval(self.inputs["Array"].default_value)
        try:
            arr.remove(self.inputs["Element"].default_value)
        except:
            pass
        out["New Array"] = repr(arr)
        return out