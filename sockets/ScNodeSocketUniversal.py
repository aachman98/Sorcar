import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket

class ScNodeSocketUniversal(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketUniversal"
    bl_label = "Universal"
    color = (0.0, 0.0, 0.0, 0.0)

    default_value: StringProperty()
    default_type: StringProperty(default="STRING")