import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectUngrouped(Node, ScSelectionNode):
    bl_idname = "ScSelectUngrouped"
    bl_label = "Select Ungrouped"
    
    in_extend: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend", True)
    
    def functionality(self):
        bpy.ops.mesh.select_ungrouped(
            extend = self.inputs["Extend"].default_value
        )