import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDissolveVertices(Node, ScDeletionNode):
    bl_idname = "ScDissolveVertices"
    bl_label = "Dissolve Vertices"
    
    in_split: BoolProperty(update=ScNode.update_value)
    in_boundary: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Face Split").init("in_split")
        self.inputs.new("ScNodeSocketBool", "Tear Boundary").init("in_boundary")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.dissolve_verts(
            use_face_split = self.inputs["Face Split"].default_value,
            use_boundary_tear = self.inputs["Tear Boundary"].default_value
        )