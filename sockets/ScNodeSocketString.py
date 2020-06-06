import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket
from ..nodes._base.node_base import ScNode

class ScNodeSocketString(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketString"
    bl_label = "String"
    color = (1.0, 0.0, 1.0, 1.0)
    
    default_value: StringProperty()
    default_value_update: StringProperty(update=ScNode.update_value)
    default_type: StringProperty(default="STRING")