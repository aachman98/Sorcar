import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectLoop(Node, ScSelectionNode):
    bl_idname = "ScSelectLoop"
    bl_label = "Select Loop"
    
    in_extend: BoolProperty(update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)
    in_toggle: BoolProperty(update=ScNode.update_value)
    in_ring: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")
        self.inputs.new("ScNodeSocketBool", "Toggle Selection").init("in_toggle")
        self.inputs.new("ScNodeSocketBool", "Select Ring").init("in_ring", True)
    
    def functionality(self):
        bpy.ops.mesh.loop_select(
            extend = self.inputs["Extend"].default_value,
            deselect = self.inputs["Deselect"].default_value,
            toggle = self.inputs["Toggle Selection"].default_value,
            ring = self.inputs["Select Ring"].default_value
        )