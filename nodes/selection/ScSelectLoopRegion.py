import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectLoopRegion(Node, ScSelectionNode):
    bl_idname = "ScSelectLoopRegion"
    bl_label = "Select Loop Region"
    
    in_bigger: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Select Bigger").init("in_bigger", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.loop_to_region(
            select_bigger = self.inputs["Select Bigger"].default_value
        )