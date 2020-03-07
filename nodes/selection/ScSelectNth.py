import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectNth(Node, ScSelectionNode):
    bl_idname = "ScSelectNth"
    bl_label = "Select Nth (Checker Deselect)"
    
    in_nth: IntProperty(default=1, min=1, update=ScNode.update_value)
    in_skip: IntProperty(default=1, min=1, update=ScNode.update_value)
    in_offset: IntProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Nth Element").init("in_nth", True)
        self.inputs.new("ScNodeSocketNumber", "Skip Number").init("in_skip")
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset")
    
    def error_condition(self):
        return(
            super().error_condition()
            or int(self.inputs["Nth Element"].default_value) < 1
            or int(self.inputs["Skip Number"].default_value) < 1
        )
    
    def functionality(self):
        bpy.ops.mesh.select_nth(
            nth = int(self.inputs["Nth Element"].default_value),
            skip = int(self.inputs["Skip Number"].default_value),
            offset = int(self.inputs["Offset"].default_value)
        )