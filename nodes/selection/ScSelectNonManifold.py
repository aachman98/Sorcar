import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectNonManifold(Node, ScSelectionNode):
    bl_idname = "ScSelectNonManifold"
    bl_label = "Select Non-Manifold"
    
    in_extend: BoolProperty(default=True, update=ScNode.update_value)
    in_wire: BoolProperty(default=True, update=ScNode.update_value)
    in_boundary: BoolProperty(default=True, update=ScNode.update_value)
    in_multi_face: BoolProperty(default=True, update=ScNode.update_value)
    in_non_contiguous: BoolProperty(default=True, update=ScNode.update_value)
    in_verts: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend", True)
        self.inputs.new("ScNodeSocketBool", "Wire").init("in_wire")
        self.inputs.new("ScNodeSocketBool", "Boundaries").init("in_boundary")
        self.inputs.new("ScNodeSocketBool", "Multiple Face").init("in_multi_face")
        self.inputs.new("ScNodeSocketBool", "Non-Contiguous").init("in_non_contiguous")
        self.inputs.new("ScNodeSocketBool", "Vertices").init("in_verts")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_non_manifold(
            extend = self.inputs["Extend"].default_value,
            use_wire = self.inputs["Wire"].default_value,
            use_boundary = self.inputs["Boundaries"].default_value,
            use_multi_face = self.inputs["Multiple Face"].default_value,
            use_non_contiguous = self.inputs["Non-Contiguous"].default_value,
            use_verts = self.inputs["Vertices"].default_value
        )