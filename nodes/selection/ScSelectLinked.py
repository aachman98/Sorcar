import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectLinked(Node, ScSelectionNode):
    bl_idname = "ScSelectLinked"
    bl_label = "Select Linked"
    
    prop_delimit: EnumProperty(items=[("NORMAL", "Normal", "", 2), ("MATERIAL", "Material", "", 4), ("SEAM", "Seam", "", 8), ("SHARP", "Sharp", "", 16), ("UV", "UV", "", 32)], default={"SEAM"}, options={"ENUM_FLAG"}, update=ScNode.update_value)
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_delimit", expand=True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or len(self.prop_delimit) == 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_linked(
            delimit = self.prop_delimit
        )