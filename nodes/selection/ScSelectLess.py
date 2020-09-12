import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectLess(Node, ScSelectionNode):
    bl_idname = "ScSelectLess"
    bl_label = "Select Less"
    
    in_step: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Face Step").init("in_step", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_less(
            use_face_step = self.inputs["Face Step"].default_value
        )