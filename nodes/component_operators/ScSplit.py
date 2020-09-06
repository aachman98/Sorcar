import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScSplit(Node, ScEditOperatorNode):
    bl_idname = "ScSplit"
    bl_label = "Split"
    
    in_type: EnumProperty(items=[('REGION', 'Region', ''), ('INDIVIDUAL', 'Individual', ''), ('EDGE', 'Loose Edges', ''), ('NORMAL', 'Normals', '')], default='REGION', update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['REGION', 'INDIVIDUAL', 'EDGE', 'NORMAL'])
        )

    def functionality(self):
        super().functionality()
        if (self.inputs["Type"].default_value == 'REGION'):
            bpy.ops.mesh.split()
        elif (self.inputs["Type"].default_value == 'INDIVIDUAL'):
            bpy.ops.mesh.edge_split()
        elif (self.inputs["Type"].default_value == 'EDGE'):
            bpy.ops.mesh.face_split_by_edges()
        elif (self.inputs["Type"].default_value == 'NORMAL'):
            bpy.ops.mesh.split_normals()