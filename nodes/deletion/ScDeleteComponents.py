import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDeleteComponents(Node, ScDeletionNode):
    bl_idname = "ScDeleteComponents"
    bl_label = "Delete Components"
    
    in_type: EnumProperty(items=[("VERT", "Vertices", ""), ("EDGE", "Edges", ""), ("FACE", "Faces", ""), ("EDGE_FACE", "Edges And Faces", ""), ("ONLY_FACE", "Only Faces", "")], default="VERT", update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['VERT', 'EDGE', 'FACE', 'EDGE_FACE', 'ONLY_FACE'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.delete(
            type = self.inputs["Type"].default_value
        )