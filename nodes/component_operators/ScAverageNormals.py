import bpy

from bpy.props import FloatProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScAverageNormals(Node, ScEditOperatorNode):
    bl_idname = "ScAverageNormals"
    bl_label = "Average Normals"
    
    in_average_type: EnumProperty(items=[('CUSTOM_NORMAL', 'Custom Normal', ''), ('FACE_AREA', 'Face Area', ''), ('CORNER_ANGLE', 'Corner Angle', '')], default='CUSTOM_NORMAL', update=ScNode.update_value)
    in_weight: FloatProperty(default=50.0, min=1.0, max=100.0, update=ScNode.update_value)
    in_threshold: FloatProperty(default=0.01, min=0.0, max=10.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_average_type", True)
        self.inputs.new("ScNodeSocketNumber", "Weight").init("in_weight")
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['CUSTOM_NORMAL', 'FACE_AREA', 'CORNER_ANGLE'])
            or (self.inputs["Weight"].default_value < 1.0 or self.inputs["Weight"].default_value > 100.0)
            or (self.inputs["Threshold"].default_value < 0.0 or self.inputs["Threshold"].default_value > 10.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.average_normals(
            average_type = self.inputs["Type"].default_value,
            weight = self.inputs["Weight"].default_value,
            threshold = self.inputs["Threshold"].default_value
        )