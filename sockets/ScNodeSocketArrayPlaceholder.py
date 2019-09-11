import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket

class ScNodeSocketArrayPlaceholder(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketArrayPlaceholder"
    bl_label = "Array Placeholder"
    color = (0.0, 0.0, 0.0, 0.0)

    default_value: StringProperty()
    default_type: StringProperty(default="STRING")

    def draw(self, context, layout, node, text):
        if (self.is_linked):
            layout.label(text=self.get_label())
        else:
            layout.label(text=text)
    
    def execute(self, forced):
        # Execute node socket to get/set default_value
        if (self.is_linked):
            if (self.links[0].from_socket.execute(forced)):
                self.default_value = repr(self.links[0].from_socket.default_value)
                return True
        else:
            self.node.inputs.remove(self)
            return True
        return False