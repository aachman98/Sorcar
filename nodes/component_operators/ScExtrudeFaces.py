import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import get_override

class ScExtrudeFaces(Node, ScEditOperatorNode):
    bl_idname = "ScExtrudeFaces"
    bl_label = "Extrude Faces (Individually)"
    
    in_value: FloatProperty(update=ScNode.update_value)
    in_use_normal_flip: BoolProperty(update=ScNode.update_value)
    in_mirror: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Value").init("in_value", True)
        self.inputs.new("ScNodeSocketBool", "Mirror Editing").init("in_mirror")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.extrude_faces_move(
            get_override(self.inputs["Object"].default_value, True),
            MESH_OT_extrude_faces_indiv = {
                "mirror": self.inputs["Mirror Editing"].default_value
            },
            TRANSFORM_OT_shrink_fatten = {
                "value": self.inputs["Value"].default_value
            }
        )