import bpy

from bpy.props import EnumProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectAxis(Node, ScSelectionNode):
    bl_idname = "ScSelectAxis"
    bl_label = "Select Axis"
    
    in_sign: EnumProperty(items=[("POS", "Positive", ""), ("NEG", "Negative", ""), ("ALIGN", "Aligned", "")], default="POS", update=ScNode.update_value)
    in_axis: EnumProperty(items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X", update=ScNode.update_value)
    in_threshold: FloatProperty(default=0.0001, min=0.000001, max=50, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Sign").init("in_sign")
        self.inputs.new("ScNodeSocketString", "Axis").init("in_axis", True)
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Sign"].default_value in ['POS', 'NEG', 'ALIGN'])
            or (not self.inputs["Axis"].default_value in ['X', 'Y', 'Z'])
            or (self.inputs["Threshold"].default_value < 0.000001 or self.inputs["Threshold"].default_value > 50)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_axis(
            orientation = bpy.context.scene.transform_orientation_slots[0].type,
            sign = self.inputs["Sign"].default_value,
            axis = self.inputs["Axis"].default_value,
            threshold = self.inputs["Threshold"].default_value
        )