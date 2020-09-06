import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScRotateEdge(Node, ScEditOperatorNode):
    bl_idname = "ScRotateEdge"
    bl_label = "Rotate Edge"
    
    in_use_ccw: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Counter Clockwise").init("in_use_ccw", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.edge_rotate(
            use_ccw = self.inputs["Counter Clockwise"].default_value
        )