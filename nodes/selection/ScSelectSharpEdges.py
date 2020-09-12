import bpy

from bpy.props import FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectSharpEdges(Node, ScSelectionNode):
    bl_idname = "ScSelectSharpEdges"
    bl_label = "Select Sharp Edges"
    
    in_sharpness: FloatProperty(default=0.523599, min=0.000174533, max=3.14159, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Sharpness").init("in_sharpness", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Sharpness"].default_value < 0.000174533 or self.inputs["Sharpness"].default_value > 3.14159)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.edges_select_sharp(
            sharpness = self.inputs["Sharpness"].default_value
        )