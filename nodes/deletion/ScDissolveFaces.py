import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDissolveFaces(Node, ScDeletionNode):
    bl_idname = "ScDissolveFaces"
    bl_label = "Dissolve Faces"
    
    in_verts: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Dissolve Vertices").init("in_verts", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.dissolve_faces(
            use_verts = self.inputs["Dissolve Vertices"].default_value,
        )