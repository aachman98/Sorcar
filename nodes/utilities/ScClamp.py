import bpy

from bpy.props import FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScClamp(Node, ScNode):
    bl_idname = "ScClamp"
    bl_label = "Clamp"
    bl_icon = 'SNAP_PEEL_OBJECT'

    in_x: FloatProperty(update=ScNode.update_value)
    in_min: FloatProperty(update=ScNode.update_value)
    in_max: FloatProperty(default=1, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketNumber", "Min").init("in_min", True)
        self.inputs.new("ScNodeSocketNumber", "Max").init("in_max", True)
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Max"].default_value < self.inputs["Min"].default_value
        )
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = max(min(self.inputs["Max"].default_value, self.inputs["X"].default_value), self.inputs["Min"].default_value)
        return out