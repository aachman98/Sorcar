import bpy

from bpy.props import PointerProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceCurve(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceCurve"
    bl_label = "Curve"
    bl_socket_idname = "ScNodeSocketCurve"

    color = (0.0, 0.0, 1.0, 1.0)
    default_value: PointerProperty(name="Default Curve", type=bpy.types.Object)