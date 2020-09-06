import bpy

from bpy.props import FloatProperty, BoolProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScPoke(Node, ScEditOperatorNode):
    bl_idname = "ScPoke"
    bl_label = "Poke"
    
    in_offset: FloatProperty(default=0.0, min=-1000.0, max=1000.0, update=ScNode.update_value)
    in_use_relative_offset: BoolProperty(update=ScNode.update_value)
    in_center_mode: EnumProperty(items=[("MEDIAN_WEIGHTED", "Median Weighted", ""), ("MEDIAN", "Median", ""), ("BOUNDS", "Bounds", "")], default="MEDIAN_WEIGHTED", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Poke Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketBool", "Relative Offset").init("in_use_relative_offset")
        self.inputs.new("ScNodeSocketString", "Poke Center").init("in_center_mode")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Poke Offset"].default_value < -1000 or self.inputs["Poke Offset"].default_value > 1000)
            or (not self.inputs["Poke Center"].default_value in ['MEDIAN_WEIGHTED', 'MEDIAN', 'BOUNDS'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.poke(
            offset = self.inputs["Poke Offset"].default_value,
            use_relative_offset = self.inputs["Relative Offset"].default_value,
            center_mode = self.inputs["Poke Center"].default_value
        )