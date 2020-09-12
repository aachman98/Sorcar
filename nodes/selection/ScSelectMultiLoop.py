import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectMultiLoop(Node, ScSelectionNode):
    bl_idname = "ScSelectMultiLoop"
    bl_label = "Select Multi-Loop"
    
    in_ring: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Select Ring").init("in_ring", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.loop_multi_select(
            ring = self.inputs["Select Ring"].default_value
        )