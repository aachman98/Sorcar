import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScApplyTransform(Node, ScObjectOperatorNode):
    bl_idname = "ScApplyTransform"
    bl_label = "Apply Transform"

    in_location: BoolProperty(default=True, update=ScNode.update_value)
    in_rotation: BoolProperty(default=True, update=ScNode.update_value)
    in_scale: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Location").init("in_location", True)
        self.inputs.new("ScNodeSocketBool", "Rotation").init("in_rotation", True)
        self.inputs.new("ScNodeSocketBool", "Scale").init("in_scale", True)
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.transform_apply(
            location = self.inputs["Location"].default_value,
            rotation = self.inputs["Rotation"].default_value,
            scale = self.inputs["Scale"].default_value
        )