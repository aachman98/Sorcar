import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceUniversal(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceUniversal"
    bl_label = "Universal"
    bl_socket_idname = "ScNodeSocketUniversal"

    color = (0.0, 0.0, 0.0, 0.0)
    default_value: StringProperty(name="Default Universal")