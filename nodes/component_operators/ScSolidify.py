import bpy

from bpy.props import FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScSolidify(Node, ScEditOperatorNode):
    bl_idname = "ScSolidify"
    bl_label = "Solidify"
    
    in_thickness: FloatProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Thickness").init("in_thickness", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Thickness"].default_value < -10000.0 or self.inputs["Thickness"].default_value > 10000.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.solidify(
            thickness = self.inputs["Thickness"].default_value
        )