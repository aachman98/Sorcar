import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectAll(Node, ScSelectionNode):
    bl_idname = "ScSelectAll"
    bl_label = "Select All"

    in_action: EnumProperty(items=[("TOGGLE", "Toggle", ""), ("SELECT", "Select", ""), ("DESELECT", "Deselect", ""), ("INVERT", "Invert", "")], default="TOGGLE", update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Action").init("in_action", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Action"].default_value in ["TOGGLE", "SELECT", "DESELECT", "INVERT"])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_all(
            action = self.inputs["Action"].default_value
        )