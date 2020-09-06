import bpy

from bpy.props import EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScMergeComponents(Node, ScEditOperatorNode):
    bl_idname = "ScMergeComponents"
    bl_label = "Merge Components"
    
    in_type: EnumProperty(items=[('FIRST', 'First', ''), ('LAST', 'Last', ''), ('CENTER', 'Center', ''), ('CURSOR', 'Cursor', ''), ('COLLAPSE', 'Collapse', '')], default='CENTER', update=ScNode.update_value)
    in_uvs: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketBool", "UVs").init("in_uvs")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['FIRST', 'LAST', 'CENTER', 'CURSOR', 'COLLAPSE'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.merge(
            type = self.inputs["Type"].default_value,
            uvs = self.inputs["UVs"].default_value
        )