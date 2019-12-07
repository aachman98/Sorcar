import bpy

from bpy.props import FloatVectorProperty, StringProperty, BoolVectorProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket
from ..helper import selection_type_to_string

class ScNodeSocketSelectionType(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketSelectionType"
    bl_label = "Selection Type"
    color = (0.3, 0.6, 0.9, 1.0)

    default_value: BoolVectorProperty(default=(True, False, False))
    default_type: StringProperty(default="SELECTION_TYPE")

    def get_label(self):
        return selection_type_to_string(self.default_value)