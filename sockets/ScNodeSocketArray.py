import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket
from ..nodes._base.node_base import ScNode

class ScNodeSocketArray(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketArray"
    bl_label = "Array"
    color = (0.0, 0.0, 1.0, 1.0)

    default_value: StringProperty(default="[]")
    default_value_update: StringProperty(default="[]", update=ScNode.update_value)
    default_type: StringProperty(default="ARRAY")

    def get_label(self):
        arr = []
        arr_len = 0
        try:
            arr = eval(self.default_value)
            arr_len = len(arr)
        except:
            arr_len = self.default_value.count(',') + 1
        return str(arr_len)
    
    def draw(self, context, layout, node, text):
        if (self.is_output or self.is_linked):
            layout.label(text=text + " [" + self.get_label() + "]")
        else:
            layout.label(text=text)