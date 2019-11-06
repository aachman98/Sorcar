import bpy

from bpy.types import NodeSocket

class ScNodeSocketInfo(NodeSocket):
    bl_idname = "ScNodeSocketInfo"
    bl_label = "Info Socket"
    
    def draw_color(self, context, node):
        return (1.0, 0.5, 0.5, 1.0)
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)