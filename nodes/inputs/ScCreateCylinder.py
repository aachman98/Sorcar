import bpy

from bpy.props import EnumProperty, IntProperty, FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_input import ScInputNode

class ScCreateCylinder(Node, ScInputNode):
    bl_idname = "ScCreateCylinder"
    bl_label = "Create Cylinder"

    in_uv: BoolProperty(default=True, update=ScNode.update_value)
    in_type: EnumProperty(items=[("NOTHING", "Nothing", ""), ("NGON", "Ngon", ""), ("TRIFAN", "Triangle Fan", "")], default="NGON", update=ScNode.update_value)
    in_vertices: IntProperty(default=32, min=3, max=10000000, update=ScNode.update_value)
    in_radius: FloatProperty(default=1.0, min=0.0, update=ScNode.update_value)
    in_depth: FloatProperty(default=2.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Generate UVs").init("in_uv")
        self.inputs.new("ScNodeSocketString", "Cap Fill Type").init("in_type")
        self.inputs.new("ScNodeSocketNumber", "Vertices").init("in_vertices", True)
        self.inputs.new("ScNodeSocketNumber", "Radius").init("in_radius", True)
        self.inputs.new("ScNodeSocketNumber", "Depth").init("in_depth", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Cap Fill Type"].default_value in ['NOTHING', 'NGON', 'TRIFAN'])
            or (self.inputs["Vertices"].default_value < 3 or self.inputs["Vertices"].default_value > 10000000)
            or self.inputs["Radius"].default_value < 0
            or self.inputs["Depth"].default_value < 0
        )
    
    def functionality(self):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices = int(self.inputs["Vertices"].default_value),
            radius = self.inputs["Radius"].default_value,
            depth = self.inputs["Depth"].default_value,
            end_fill_type = self.inputs["Cap Fill Type"].default_value,
            calc_uvs = self.inputs["Generate UVs"].default_value
        )