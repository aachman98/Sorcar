import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket

class ScNodeSocketArrayPlaceholder(NodeSocket):
    bl_idname = "ScNodeSocketArrayPlaceholder"
    bl_label = "Array Placeholder"
    
    def draw_color(self, context, node):
        return (0.0, 0.0, 0.0, 0.0)

    def draw(self, context, layout, node, text):
        layout.label(text="---")