import bpy

from bpy.props import FloatVectorProperty, StringProperty, BoolVectorProperty, EnumProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket
from ..helper import selection_type_to_string

class ScNodeSocketSelectionType(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketSelectionType"
    bl_label = "Selection Type"
    color = (0.3, 0.6, 0.9, 1.0)

    default_value: EnumProperty(name="Mode", items=[("VERT", "Vertices", "", "VERTEXSEL", 1), ("EDGE", "Edges", "", "EDGESEL", 2), ("FACE", "Faces", "", "FACESEL", 4)], options={"ENUM_FLAG"})
    default_type: StringProperty(default="SELECTION_TYPE")

    def get_label(self):
        return selection_type_to_string(self.default_value)