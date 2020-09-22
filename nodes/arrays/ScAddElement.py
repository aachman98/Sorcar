import bpy
import math

from bpy.props import IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScAddElement(Node, ScNode):
    bl_idname = "ScAddElement"
    bl_label = "Add Element"
    bl_icon = 'ADD'

    in_use_index: BoolProperty(update=ScNode.update_value)
    in_index: IntProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketUniversal", "Element")
        self.inputs.new("ScNodeSocketBool", "Use Index").init("in_use_index")
        self.inputs.new("ScNodeSocketNumber", "Index").init("in_index")
        self.outputs.new("ScNodeSocketArray", "New Array")

    def post_execute(self):
        out = super().post_execute()
        arr = eval(self.inputs["Array"].default_value)
        if (self.inputs["Use Index"].default_value):
            arr.insert(int(self.inputs["Index"].default_value), self.inputs["Element"].default_value)
        else:
            arr.append(self.inputs["Element"].default_value)
        out["New Array"] = repr(arr)
        return out