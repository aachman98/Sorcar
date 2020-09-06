import bpy

from bpy.props import FloatProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScIntersect(Node, ScEditOperatorNode):
    bl_idname = "ScIntersect"
    bl_label = "Intersect"
    
    in_mode: EnumProperty(items=[('SELECT', 'Self Intersect', ''), ('SELECT_UNSELECT', 'Selected/Unselected', '')], default='SELECT_UNSELECT', update=ScNode.update_value)
    in_separate_mode: EnumProperty(items=[('ALL', 'All', ''), ('CUT', 'Cut', ''), ('NONE', 'Merge', '')], default='CUT', update=ScNode.update_value)
    in_threshold: FloatProperty(default=0.000001, min=0.0, max=0.01, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Source").init("in_mode", True)
        self.inputs.new("ScNodeSocketString", "Separate Mode").init("in_separate_mode", True)
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Source"].default_value in ['SELECT', 'SELECT_UNSELECT'])
            or (not self.inputs["Separate Mode"].default_value in ['ALL', 'CUT', 'NONE'])
            or (self.inputs["Threshold"].default_value < 0.0 or self.inputs["Threshold"].default_value > 0.01)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.intersect(
            mode = self.inputs["Source"].default_value,
            separate_mode = self.inputs["Separate Mode"].default_value,
            threshold = self.inputs["Threshold"].default_value
        )