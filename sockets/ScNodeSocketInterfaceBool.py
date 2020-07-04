import bpy

from bpy.props import BoolProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceBool(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceBool"
    bl_label = "Bool"
    bl_socket_idname = "ScNodeSocketBool"

    color = (1.0, 0.0, 0.0, 1.0)
    default_value: BoolProperty(name="Default Value")