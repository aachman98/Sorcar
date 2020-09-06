import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScUnhideComponents(Node, ScEditOperatorNode):
    bl_idname = "ScUnhideComponents"
    bl_label = "Unhide Components"
    
    in_select: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Select").init("in_select")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.reveal(
            select = self.inputs["Select"].default_value
        )
