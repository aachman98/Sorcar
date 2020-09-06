import bpy

from bpy.props import FloatProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScSymmetrize(Node, ScEditOperatorNode):
    bl_idname = "ScSymmetrize"
    bl_label = "Symmetrize"
    
    in_direction: EnumProperty(items=[("NEGATIVE_X", "-X to +X", ""), ("POSITIVE_X", "+X to -X", ""), ("NEGATIVE_Y", "-Y to +Y", ""), ("POSITIVE_Y", "+Y to -Y", ""), ("NEGATIVE_Z", "-Z to +Z", ""), ("POSITIVE_Z", "+Z to -Z", "")], default="NEGATIVE_X", update=ScNode.update_value)
    in_threshold: FloatProperty(default=0.0001, min=0.0, max=10.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Direction").init("in_direction", True)
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Direction"].default_value in ['NEGATIVE_X', 'POSITIVE_X', 'NEGATIVE_Y', 'POSITIVE_Y', 'NEGATIVE_Z', 'POSITIVE_Z'])
            or (self.inputs["Threshold"].default_value < 0.0 or self.inputs["Threshold"].default_value > 10.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.symmetrize(
            direction = self.inputs["Direction"].default_value,
            threshold = self.inputs["Threshold"].default_value
        )