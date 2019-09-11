import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket

class ScNodeSocketArray(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketArray"
    bl_label = "Array"
    color = (0.0, 0.0, 1.0, 1.0)

    default_value: StringProperty(default="[]")
    default_type: StringProperty(default="ARRAY")

    def get_label(self):
        return str(len(eval(self.default_value)))
    
    def draw(self, context, layout, node, text):
        if (self.is_output or self.is_linked):
            layout.label(text=text + " [" + self.get_label() + "]")
        else:
            layout.label(text=text)