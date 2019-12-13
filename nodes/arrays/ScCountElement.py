import bpy
import math

from bpy.types import Node
from .._base.node_base import ScNode

class ScCountElement(Node, ScNode):
    bl_idname = "ScCountElement"
    bl_label = "Count Element"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketUniversal", "Element")
        self.outputs.new("ScNodeSocketNumber", "Value")

    def post_execute(self):
        out = {}
        out["Value"] = eval(self.inputs["Array"].default_value).count(self.inputs["Element"].default_value)
        return out