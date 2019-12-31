import bpy

from bpy.props import PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScParent(Node, ScObjectOperatorNode):
    bl_idname = "ScParent"
    bl_label = "Parent"

    prop_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Parent Object").init("prop_obj", True)
    
    def functionality(self):
        self.inputs["Object"].default_value.parent = self.inputs["Parent Object"].default_value