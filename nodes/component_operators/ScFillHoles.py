import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScFillHoles(Node, ScEditOperatorNode):
    bl_idname = "ScFillHoles"
    bl_label = "Fill Holes (by Sides)"
    
    in_sides: IntProperty(default=4, min=0, max=1000, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Sides").init("in_sides", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Sides"].default_value) < 0 or int(self.inputs["Sides"].default_value) > 1000)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.fill_holes(
            sides = int(self.inputs["Sides"].default_value)
        )