import bpy

from bpy.props import FloatVectorProperty, StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket

class ScNodeSocketVector(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketVector"
    bl_label = "Vector"
    color = (1.0, 1.0, 0.0, 1.0)

    default_value: FloatVectorProperty()
    default_type: StringProperty(default="VECTOR")

    def get_label(self):
        return str(round(self.default_value[0], 1)) + ", " + str(round(self.default_value[1], 1)) + ", " + str(round(self.default_value[2], 1))