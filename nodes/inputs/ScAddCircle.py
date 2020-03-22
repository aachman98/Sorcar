import bpy

from bpy.props import EnumProperty, IntProperty, FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScAddCircle(Node, ScEditOperatorNode):
    bl_idname = "ScAddCircle"
    bl_label = "Add Circle"

    in_uv: BoolProperty(default=True, update=ScNode.update_value)
    in_type: EnumProperty(items=[("NOTHING", "Nothing", ""), ("NGON", "Ngon", ""), ("TRIFAN", "Triangle Fan", "")], default="NOTHING", update=ScNode.update_value)
    in_vertices: IntProperty(default=32, min=3, max=10000000, update=ScNode.update_value)
    in_radius: FloatProperty(default=1.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Generate UVs").init("in_uv")
        self.inputs.new("ScNodeSocketString", "Fill Type").init("in_type")
        self.inputs.new("ScNodeSocketNumber", "Vertices").init("in_vertices", True)
        self.inputs.new("ScNodeSocketNumber", "Radius").init("in_radius", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Fill Type"].default_value in ['NOTHING', 'NGON', 'TRIFAN'])
            or self.inputs["Vertices"].default_value < 3
            or self.inputs["Radius"].default_value < 0
        )
    
    def functionality(self):
        bpy.ops.mesh.primitive_circle_add(
            vertices = int(self.inputs["Vertices"].default_value),
            radius = self.inputs["Radius"].default_value,
            fill_type = self.inputs["Fill Type"].default_value,
            calc_uvs = self.inputs["Generate UVs"].default_value
        )