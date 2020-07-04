import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceString(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceString"
    bl_label = "String"
    bl_socket_idname = "ScNodeSocketString"

    color = (1.0, 0.0, 1.0, 1.0)
    default_value: StringProperty(name="Default String")