import bpy
import mathutils

from bpy.props import BoolVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScSelectionType(Node, ScNode):
    bl_idname = "ScSelectionType"
    bl_label = "Selection Type"

    prop_type: BoolVectorProperty(default=(True, False, False), update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.outputs.new("ScNodeSocketSelectionType", "Value")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        row = layout.row(align = True)
        row.prop(self, "prop_type", index = 0, toggle = True, icon_only = True, icon = "VERTEXSEL")
        row.prop(self, "prop_type", index = 1, toggle = True, icon_only = True, icon = "EDGESEL")
        row.prop(self, "prop_type", index = 2, toggle = True, icon_only = True, icon = "FACESEL")
        row.alignment = "CENTER"
    
    def post_execute(self):
        return {"Value": self.prop_type}