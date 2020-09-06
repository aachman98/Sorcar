import bpy

from bpy.props import FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import get_override

class ScDuplicateComponent(Node, ScEditOperatorNode):
    bl_idname = "ScDuplicateComponent"
    bl_label = "Duplicate Component"
    
    in_move_offset: FloatVectorProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Move Offset").init("in_move_offset", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.duplicate_move(
            get_override(self.inputs["Object"].default_value, True),
            TRANSFORM_OT_translate = {
                "value": self.inputs["Move Offset"].default_value
            }
        )