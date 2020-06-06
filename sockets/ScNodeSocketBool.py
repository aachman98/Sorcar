import bpy

from bpy.props import BoolProperty, StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket
from ..nodes._base.node_base import ScNode

class ScNodeSocketBool(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketBool"
    bl_label = "Bool"
    color = (1.0, 0.0, 0.0, 1.0)

    default_value: BoolProperty()
    default_value_update: BoolProperty(update=ScNode.update_value)
    default_type: StringProperty(default="BOOL")