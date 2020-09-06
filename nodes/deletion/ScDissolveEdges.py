import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDissolveEdges(Node, ScDeletionNode):
    bl_idname = "ScDissolveEdges"
    bl_label = "Dissolve Edges"
    
    in_verts: BoolProperty(default=True, update=ScNode.update_value)
    in_split: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Dissolve Vertices").init("in_verts", True)
        self.inputs.new("ScNodeSocketBool", "Face Split").init("in_split")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.dissolve_edges(
            use_verts = self.inputs["Dissolve Vertices"].default_value,
            use_face_split = self.inputs["Face Split"].default_value
        )