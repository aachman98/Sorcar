import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectMore(Node, ScSelectionNode):
    bl_idname = "ScSelectMore"
    bl_label = "Select More"
    
    in_step: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Face Step").init("in_step", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_more(
            use_face_step = self.inputs["Face Step"].default_value
        )