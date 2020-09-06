import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScTriangulate(Node, ScEditOperatorNode):
    bl_idname = "ScTriangulate"
    bl_label = "Triangulate"
    
    in_quad: EnumProperty(items=[("BEAUTY", "Beauty", ""), ("FIXED", "Fixed", ""), ("FIXED_ALTERNATE", "Fixed Alternate", ""), ("SHORTEST_DIAGONAL", "Shortest Diagonal", "")], default="BEAUTY", update=ScNode.update_value)
    in_ngon: EnumProperty(items=[("BEAUTY", "Beauty", ""), ("CLIP", "Clip", "")], default="BEAUTY", update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Quad Method").init("in_quad", True)
        self.inputs.new("ScNodeSocketString", "Polygon Method").init("in_ngon", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Quad Method"].default_value in ['BEAUTY', 'FIXED', 'FIXED_ALTERNATE', 'SHORTEST_DIAGONAL'])
            or (not self.inputs["Polygon Method"].default_value in ['BEAUTY', 'CLIP'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.quads_convert_to_tris(
            quad_method = self.inputs["Quad Method"].default_value,
            ngon_method = self.inputs["Polygon Method"].default_value
        )