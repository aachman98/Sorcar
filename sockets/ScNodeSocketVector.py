import bpy

from bpy.props import FloatVectorProperty, StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket
from ..nodes._base.node_base import ScNode

class ScNodeSocketVector(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketVector"
    bl_label = "Vector"
    color = (1.0, 1.0, 0.0, 1.0)

    default_value: FloatVectorProperty()
    default_value_update: FloatVectorProperty(update=ScNode.update_value)
    default_type: StringProperty(default="VECTOR")

    def get_label(self):
        return str(round(self.default_value[0], 1)) + ", " + str(round(self.default_value[1], 1)) + ", " + str(round(self.default_value[2], 1))
    
    def draw_layout(self, context, layout, node, prop, text):
        layout.column().prop(node, prop, text=text)