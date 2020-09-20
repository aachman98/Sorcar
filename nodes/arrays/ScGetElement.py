import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScGetElement(Node, ScNode):
    bl_idname = "ScGetElement"
    bl_label = "Get Element"
    bl_icon = 'SHORTDISPLAY'
    
    in_index: IntProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketNumber", "Index").init("in_index", True)
        self.outputs.new("ScNodeSocketUniversal", "Element")
    
    def post_execute(self):
        out = super().post_execute()
        try:
            out["Element"] = repr(eval(self.inputs["Array"].default_value)[int(self.inputs["Index"].default_value)])
        except:
            out["Element"] = None
        return out