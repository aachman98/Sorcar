import bpy

from bpy.props import PointerProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceObject(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceObject"
    bl_label = "Object"
    bl_socket_idname = "ScNodeSocketObject"

    color = (1.0, 1.0, 1.0, 1.0)
    default_value: PointerProperty(name="Default Object", type=bpy.types.Object)