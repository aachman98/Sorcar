import bpy

from bpy.props import EnumProperty
from bpy.types import NodeSocketInterface
from ._base.interface_base import ScNodeSocketInterface

class ScNodeSocketInterfaceSelectionType(NodeSocketInterface, ScNodeSocketInterface):
    bl_idname = "ScNodeSocketInterfaceSelectionType"
    bl_label = "Selection Type"
    bl_socket_idname = "ScNodeSocketSelectionType"

    color = (0.3, 0.6, 0.9, 1.0)
    default_value: EnumProperty(name="Default Mode", items=[("VERT", "Vertices", "", "VERTEXSEL", 1), ("EDGE", "Edges", "", "EDGESEL", 2), ("FACE", "Faces", "", "FACESEL", 4)], options={"ENUM_FLAG"})