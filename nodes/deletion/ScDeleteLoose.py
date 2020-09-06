import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDeleteLoose(Node, ScDeletionNode):
    bl_idname = "ScDeleteLoose"
    bl_label = "Delete Loose"
    
    in_vert: BoolProperty(default=True, update=ScNode.update_value)
    in_edge: BoolProperty(default=True, update=ScNode.update_value)
    in_face: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Vertices").init("in_vert")
        self.inputs.new("ScNodeSocketBool", "Edges").init("in_edge")
        self.inputs.new("ScNodeSocketBool", "Faces").init("in_face")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.delete_loose(
            use_verts = self.inputs["Vertices"].default_value,
            use_edges = self.inputs["Edges"].default_value,
            use_faces = self.inputs["Faces"].default_value
        )