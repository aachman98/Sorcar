import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScMakeNormalsConsistent(Node, ScEditOperatorNode):
    bl_idname = "ScMakeNormalsConsistent"
    bl_label = "Make Normals Consistent"
    
    in_inside: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Inside").init("in_inside", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.normals_make_consistent(
            inside = self.inputs["Inside"].default_value
        )