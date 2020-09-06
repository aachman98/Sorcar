import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScFillEdgeLoop(Node, ScEditOperatorNode):
    bl_idname = "ScFillEdgeLoop"
    bl_label = "Fill Edge Loop"
    
    in_use_beauty: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Beauty").init("in_use_beauty", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.fill(
            use_beauty = self.inputs["Beauty"].default_value
        )