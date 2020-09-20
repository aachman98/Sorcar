import bpy
import mathutils

from bpy.props import BoolVectorProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScSelectionType(Node, ScNode):
    bl_idname = "ScSelectionType"
    bl_label = "Selection Type"
    bl_icon = 'UV_VERTEXSEL'

    prop_type: EnumProperty(name="Mode", items=[("VERT", "Vertices", "", "VERTEXSEL", 1), ("EDGE", "Edges", "", "EDGESEL", 2), ("FACE", "Faces", "", "FACESEL", 4)], default={"VERT"}, options={"ENUM_FLAG"}, update=ScNode.update_value)
    def init(self, context):
        super().init(context)
        self.outputs.new("ScNodeSocketSelectionType", "Value")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.column().prop(self, "prop_type")
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = self.prop_type
        return out