import bpy

from bpy.props import EnumProperty, IntProperty, FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScAddCone(Node, ScEditOperatorNode):
    bl_idname = "ScAddCone"
    bl_label = "Add Cone"

    in_uv: BoolProperty(default=True, update=ScNode.update_value)
    in_type: EnumProperty(items=[("NOTHING", "Nothing", ""), ("NGON", "Ngon", ""), ("TRIFAN", "Triangle Fan", "")], default="NGON", update=ScNode.update_value)
    in_vertices: IntProperty(default=32, min=3, max=10000000, update=ScNode.update_value)
    in_radius1: FloatProperty(default=1.0, min=0.0, update=ScNode.update_value)
    in_radius2: FloatProperty(min=0.0, update=ScNode.update_value)
    in_depth: FloatProperty(default=2.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Generate UVs").init("in_uv")
        self.inputs.new("ScNodeSocketString", "Base Fill Type").init("in_type")
        self.inputs.new("ScNodeSocketNumber", "Vertices").init("in_vertices", True)
        self.inputs.new("ScNodeSocketNumber", "Radius 1").init("in_radius1", True)
        self.inputs.new("ScNodeSocketNumber", "Radius 2").init("in_radius2")
        self.inputs.new("ScNodeSocketNumber", "Depth").init("in_depth", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Base Fill Type"].default_value in ['NOTHING', 'NGON', 'TRIFAN'])
            or (self.inputs["Vertices"].default_value < 3 or self.inputs["Vertices"].default_value > 10000000)
            or self.inputs["Radius 1"].default_value < 0
            or self.inputs["Radius 2"].default_value < 0
            or self.inputs["Depth"].default_value < 0
        )
    
    def functionality(self):
        bpy.ops.mesh.primitive_cone_add(
            vertices = int(self.inputs["Vertices"].default_value),
            radius1 = self.inputs["Radius 1"].default_value,
            radius2 = self.inputs["Radius 2"].default_value,
            depth = self.inputs["Depth"].default_value,
            end_fill_type = self.inputs["Base Fill Type"].default_value,
            calc_uvs = self.inputs["Generate UVs"].default_value
        )