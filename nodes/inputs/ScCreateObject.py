import bpy

from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_input import ScInputNode

class ScCreateObject(Node, ScInputNode):
    bl_idname = "ScCreateObject"
    bl_label = "Create Object"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Vertices")
        self.inputs.new("ScNodeSocketArray", "Edges")
        self.inputs.new("ScNodeSocketArray", "Faces")
    
    def functionality(self):
        bpy.ops.object.add(
            type = "MESH",
            align = "CURSOR"
        )
        bpy.context.active_object.data.from_pydata(eval(self.inputs["Vertices"].default_value), eval(self.inputs["Edges"].default_value), eval(self.inputs["Faces"].default_value))