import bpy

from bpy.props import BoolProperty

class ScNodeSocketInterface:
    show_prop: BoolProperty(name="Show Property", default=True)

    def draw(self, context, layout):
        if (not self.is_output):
            layout.prop(self, "show_prop")
            # layout.prop(self, "default_value")
    
    def draw_color(self, context):
        return self.color