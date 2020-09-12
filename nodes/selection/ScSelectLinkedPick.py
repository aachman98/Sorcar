import bpy

from bpy.props import EnumProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectLinkedPick(Node, ScSelectionNode):
    bl_idname = "ScSelectLinkedPick"
    bl_label = "Select Linked Pick"
    
    prop_delimit: EnumProperty(items=[("NORMAL", "Normal", "", 2), ("MATERIAL", "Material", "", 4), ("SEAM", "Seam", "", 8), ("SHARP", "Sharp", "", 16), ("UV", "UV", "", 32)], default={"SEAM"}, options={"ENUM_FLAG"}, update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)
    in_index: IntProperty(default=-1, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")
        self.inputs.new("ScNodeSocketNumber", "Index").init("in_index", True)
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_delimit", expand=True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or len(self.prop_delimit) == 0
            or int(self.inputs["Index"].default_value < 0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_linked_pick(
            deselect = self.inputs["Deselect"].default_value,
            delimit = self.prop_delimit,
            index = self.inputs["Index"].default_value
        )