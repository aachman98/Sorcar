import bpy

from bpy.props import FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScSetDimensions(Node, ScObjectOperatorNode):
    bl_idname = "ScSetDimensions"
    bl_label = "Set Dimensions"
    
    in_dimensions: FloatVectorProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Dimensions").init("in_dimensions", True)
    
    def functionality(self):
        self.inputs["Object"].default_value.dimensions = self.inputs["Dimensions"].default_value