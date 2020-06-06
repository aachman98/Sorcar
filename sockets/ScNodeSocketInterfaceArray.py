import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceArray(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceArray"
    bl_socket_idname = "ScNodeSocketArray"
    color = (0.0, 0.0, 1.0, 1.0)

    default_value: StringProperty(name="Default Array", default="[]")