import bpy

from bpy.props import EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectMirror(Node, ScSelectionNode):
    bl_idname = "ScSelectMirror"
    bl_label = "Select Mirror "
    
    prop_axis: EnumProperty(items=[("X", "X", "", 2), ("Y", "Y", "", 4), ("Z", "Z", "", 8)], default={"X"}, options={"ENUM_FLAG"}, update=ScNode.update_value)
    in_extend: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_axis", expand=True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or len(self.prop_axis) == 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_mirror(
            axis = self.prop_axis,
            extend = self.inputs["Extend"].default_value
        )