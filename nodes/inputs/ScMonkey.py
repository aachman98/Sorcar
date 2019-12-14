import bpy

from bpy.props import FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_input import ScInputNode

class ScMonkey(Node, ScInputNode):
    bl_idname = "ScMonkey"
    bl_label = "Monkey (Suzanne)"

    in_size: FloatProperty(default=2.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Size").init("in_size", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Size"].default_value <= 0
        )
    
    def functionality(self):
        bpy.ops.mesh.primitive_monkey_add(
            size = self.inputs["Size"].default_value,
            calc_uvs = self.inputs["Generate UVs"].default_value
        )