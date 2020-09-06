import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDissolve(Node, ScDeletionNode):
    bl_idname = "ScDissolve"
    bl_label = "Dissolve"
    
    in_split: BoolProperty(update=ScNode.update_value)
    in_boundary: BoolProperty(update=ScNode.update_value)
    in_verts: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Dissolve Vertices").init("in_verts")
        self.inputs.new("ScNodeSocketBool", "Face Split").init("in_split")
        self.inputs.new("ScNodeSocketBool", "Tear Boundary").init("in_boundary")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.dissolve_mode(
            use_verts = self.inputs["Dissolve Vertices"].default_value,
            use_face_split = self.inputs["Face Split"].default_value,
            use_boundary_tear = self.inputs["Tear Boundary"].default_value
        )