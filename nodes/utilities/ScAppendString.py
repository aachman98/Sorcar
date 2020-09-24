import bpy

from bpy.props import StringProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScAppendString(Node, ScNode):
    bl_idname = "ScAppendString"
    bl_label = "Append String"
    bl_icon = 'LINENUMBERS_OFF'

    in_a: StringProperty(update=ScNode.update_value)
    in_b: StringProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "A").init("in_a", True)
        self.inputs.new("ScNodeSocketString", "B").init("in_b", True)
        self.outputs.new("ScNodeSocketString", "Value")
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = self.inputs["A"].default_value + self.inputs["B"].default_value
        return out