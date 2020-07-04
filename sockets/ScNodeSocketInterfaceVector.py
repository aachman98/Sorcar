import bpy

from bpy.props import FloatVectorProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceVector(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceVector"
    bl_label = "Vector"
    bl_socket_idname = "ScNodeSocketVector"
    
    color = (1.0, 1.0, 0.0, 1.0)
    default_value: FloatVectorProperty(name="Default Vector")