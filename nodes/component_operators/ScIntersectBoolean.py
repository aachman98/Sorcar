import bpy

from bpy.props import FloatProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScIntersectBoolean(Node, ScEditOperatorNode):
    bl_idname = "ScIntersectBoolean"
    bl_label = "Intersect Boolean"

    in_operation: EnumProperty(items=[('INTERSECT', 'Intersect', ''), ('UNION', 'Union', ''), ('DIFFERENCE', 'Difference', '')], default='DIFFERENCE', update=ScNode.update_value)
    in_use_swap: BoolProperty(update=ScNode.update_value)
    in_threshold: FloatProperty(default=0.000001, min=0.0, max=0.01, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Operation").init("in_operation", True)
        self.inputs.new("ScNodeSocketBool", "Swap").init("in_use_swap")
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Operation"].default_value in ['INTERSECT', 'UNION', 'DIFFERENCE'])
            or (self.inputs["Threshold"].default_value < 0.0 or self.inputs["Threshold"].default_value > 0.01)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.intersect_boolean(
            operation = self.inputs["Operation"].default_value,
            use_swap = self.inputs["Swap"].default_value,
            threshold = self.inputs["Threshold"].default_value
        )