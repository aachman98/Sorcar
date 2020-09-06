import bpy

from bpy.props import IntProperty, FloatVectorProperty
from bpy.types import Node
from mathutils import Vector
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScScrew(Node, ScEditOperatorNode):
    bl_idname = "ScScrew"
    bl_label = "Screw"
    
    in_steps: IntProperty(default=9, min=1, max=100000, update=ScNode.update_value)
    in_turns: IntProperty(default=1, min=1, max=100000, update=ScNode.update_value)
    in_center: FloatVectorProperty(update=ScNode.update_value)
    in_axis: FloatVectorProperty(default=(1.0, 0.0, 0.0), min=-1.0, max=1.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Steps").init("in_steps", True)
        self.inputs.new("ScNodeSocketNumber", "Turns").init("in_turns", True)
        self.inputs.new("ScNodeSocketVector", "Center").init("in_center", True)
        self.inputs.new("ScNodeSocketVector", "Axis").init("in_axis", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Steps"].default_value) < 1 or int(self.inputs["Steps"].default_value) > 100000)
            or (int(self.inputs["Turns"].default_value) < 1 or int(self.inputs["Turns"].default_value) > 100000)
            or Vector(self.inputs["Axis"].default_value).magnitude == 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.screw(
            steps = int(self.inputs["Steps"].default_value),
            turns = int(self.inputs["Turns"].default_value),
            center = self.inputs["Center"].default_value,
            axis = self.inputs["Axis"].default_value
        )