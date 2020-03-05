import bpy

from bpy.props import StringProperty
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
        m = bpy.data.meshes.new(self.inputs["Name"].default_value)
        m.from_pydata(eval(self.inputs["Vertices"].default_value), eval(self.inputs["Edges"].default_value), eval(self.inputs["Faces"].default_value))
        o = bpy.data.objects.new(self.inputs["Name"].default_value, m)
        bpy.ops.object.add_named(
            linked = True,
            name = self.inputs["Name"].default_value
        )