import bpy

from bpy.props import FloatProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceNumber(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceNumber"
    bl_label = "Number"
    bl_socket_idname = "ScNodeSocketNumber"

    color = (0.0, 1.0, 0.0, 1.0)
    default_value: FloatProperty(name="Default Value")