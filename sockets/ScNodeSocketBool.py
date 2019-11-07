import bpy

from bpy.props import BoolProperty, StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket

class ScNodeSocketBool(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketBool"
    bl_label = "Bool"
    color = (1.0, 0.0, 0.0, 1.0)

    default_value: BoolProperty()
    default_type: StringProperty(default="BOOL")