import bpy

from bpy.props import PointerProperty, StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket
from ..nodes._base.node_base import ScNode

class ScNodeSocketObject(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketObject"
    bl_label = "Object"
    color = (1.0, 1.0, 1.0, 1.0)

    default_value: PointerProperty(type=bpy.types.Object)
    default_value_update: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    default_type: StringProperty(default="OBJECT")

    def get_label(self):
        if (self.default_value):
            return self.default_value.name
        else:
            return "-"