import bpy
import math

from bpy.props import BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScSearchElement(Node, ScNode):
    bl_idname = "ScSearchElement"
    bl_label = "Search Element"
    bl_icon = 'ZOOM_ALL'

    in_range: BoolProperty(update=ScNode.update_value)
    in_start: IntProperty(update=ScNode.update_value)
    in_end: IntProperty(default=10, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketUniversal", "Element")
        self.inputs.new("ScNodeSocketBool", "Use Range").init("in_range")
        self.inputs.new("ScNodeSocketNumber", "Start Index").init("in_start")
        self.inputs.new("ScNodeSocketNumber", "End Index").init("in_end")
        self.outputs.new("ScNodeSocketNumber", "Index")

    def post_execute(self):
        out = super().post_execute()
        try:
            if (self.inputs["Use Range"].default_value):
                index = eval(self.inputs["Array"].default_value).index(self.inputs["Element"].default_value, int(self.inputs["Start Index"].default_value), int(self.inputs["End Index"].default_value))
            else:
                index = eval(self.inputs["Array"].default_value).index(self.inputs["Element"].default_value)
        except:
            index = -1
        out["Index"] = index
        return out