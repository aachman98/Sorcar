import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScClearParent(Node, ScObjectOperatorNode):
    bl_idname = "ScClearParent"
    bl_label = "Clear Parent"

    ops_type: EnumProperty(items=[('CLEAR', 'Normal', ''), ('CLEAR_KEEP_TRANSFORM', 'Keep Transform', ''), ('CLEAR_INVERSE', 'Clear Inverse', '')], default='CLEAR', update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("ops_type", True)

    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['CLEAR', 'CLEAR_KEEP_TRANSFORM', 'CLEAR_INVERSE'])
        )

    def functionality(self):
        bpy.ops.object.parent_clear(
            type = self.inputs["Type"].default_value
        )
