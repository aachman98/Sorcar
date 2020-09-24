import bpy

from bpy.props import FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBreakVector(Node, ScNode):
    bl_idname = "ScBreakVector"
    bl_label = "Break Vector"
    bl_icon = 'CENTER_ONLY'

    in_vector: FloatVectorProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Vector").init("in_vector", True)
        self.outputs.new("ScNodeSocketNumber", "X")
        self.outputs.new("ScNodeSocketNumber", "Y")
        self.outputs.new("ScNodeSocketNumber", "Z")
    
    def post_execute(self):
        out = super().post_execute()
        out["X"] = self.inputs["Vector"].default_value[0]
        out["Y"] = self.inputs["Vector"].default_value[1]
        out["Z"] = self.inputs["Vector"].default_value[2]
        return out