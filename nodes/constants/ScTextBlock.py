import bpy

from bpy.props import PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScTextBlock(Node, ScNode):
    bl_idname = "ScTextBlock"
    bl_label = "Text Block"
    bl_icon = 'FILE_TEXT'

    prop_text: PointerProperty(name="Text", type=bpy.types.Text, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.outputs.new("ScNodeSocketString", "Value")
    
    def error_condition(self):
        return (
            super().error_condition
            or self.prop_text == None
        )
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_text")
        if (not self.prop_text == None):
            col = layout.column()
            for l in self.prop_text.lines:
                col.label(text=l.body)
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = self.prop_text.as_string()
        return out