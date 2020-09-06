import bpy

from bpy.props import FloatVectorProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import get_override

class ScExtrudeVertices(Node, ScEditOperatorNode):
    bl_idname = "ScExtrudeVertices"
    bl_label = "Extrude Vertices (Individually)"
    
    in_value: FloatVectorProperty(update=ScNode.update_value)
    in_use_normal_flip: BoolProperty(update=ScNode.update_value)
    in_mirror: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Value").init("in_value", True)
        self.inputs.new("ScNodeSocketBool", "Mirror Editing").init("in_mirror")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.extrude_vertices_move(
            get_override(self.inputs["Object"].default_value, True),
            MESH_OT_extrude_verts_indiv = {
                "mirror": self.inputs["Mirror Editing"].default_value
            },
            TRANSFORM_OT_translate = {
                "value": self.inputs["Value"].default_value
            }
        )