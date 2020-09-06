import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScHideComponents(Node, ScEditOperatorNode):
    bl_idname = "ScHideComponents"
    bl_label = "Hide Components"
    
    in_unselected: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Unselected").init("in_unselected")

    def functionality(self):
        super().functionality()
        bpy.ops.mesh.hide(
            unselected = self.inputs["Unselected"].default_value
        )
