import bpy

from bpy.props import IntProperty, FloatVectorProperty, BoolProperty, FloatProperty
from bpy.types import Node
from mathutils import Vector
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScSpin(Node, ScEditOperatorNode):
    bl_idname = "ScSpin"
    bl_label = "Spin"
    
    in_steps: IntProperty(default=9, min=0, max=1000000, update=ScNode.update_value)
    in_dupli: BoolProperty(update=ScNode.update_value)
    in_angle: FloatProperty(default=1.5708, unit="ROTATION", update=ScNode.update_value)
    in_merge: BoolProperty(default=True, update=ScNode.update_value)
    in_flip: BoolProperty(update=ScNode.update_value)
    in_center: FloatVectorProperty(update=ScNode.update_value)
    in_axis: FloatVectorProperty(default=(1.0, 0.0, 0.0), min=-1.0, max=1.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Steps").init("in_steps", True)
        self.inputs.new("ScNodeSocketBool", "Duplicate").init("in_dupli")
        self.inputs.new("ScNodeSocketNumber", "Angle").init("in_angle", True)
        self.inputs.new("ScNodeSocketBool", "Auto Merge").init("in_merge")
        self.inputs.new("ScNodeSocketBool", "Flip Normals").init("in_flip")
        self.inputs.new("ScNodeSocketVector", "Center").init("in_center", True)
        self.inputs.new("ScNodeSocketVector", "Axis").init("in_axis", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Steps"].default_value) < 0 or int(self.inputs["Steps"].default_value) > 1000000)
            or Vector(self.inputs["Axis"].default_value).magnitude == 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.spin(
            steps = int(self.inputs["Steps"].default_value),
            dupli = self.inputs["Duplicate"].default_value,
            angle = self.inputs["Angle"].default_value,
            use_auto_merge = self.inputs["Auto Merge"].default_value,
            use_normal_flip = self.inputs["Flip Normals"].default_value,
            center = self.inputs["Center"].default_value,
            axis = self.inputs["Axis"].default_value
        )