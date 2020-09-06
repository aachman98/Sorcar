import bpy

from bpy.props import FloatProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScUvProject(Node, ScEditOperatorNode):
    bl_idname = "ScUvProject"
    bl_label = "UV Project"
    
    in_type: EnumProperty(items=[('CUBE', 'Cube', ''), ('CYLINDER', 'Cylinder', ''), ('SPHERE', 'Sphere', '')], default='CUBE', update=ScNode.update_value)
    in_value: FloatProperty(default=1.0, min=0.0, update=ScNode.update_value)
    in_aspect: BoolProperty(default=True, update=ScNode.update_value)
    in_clip: BoolProperty(update=ScNode.update_value)
    in_scale: BoolProperty(update=ScNode.update_value)
    in_dir: EnumProperty(items=[('VIEW_ON_EQUATOR', 'View on Equator', ''), ('VIEW_ON_POLES', 'View on Poles', ''), ('ALIGN_TO_OBJECT', 'Align to Object', '')], default='VIEW_ON_EQUATOR', update=ScNode.update_value)
    in_align: EnumProperty(items=[('POLAR_ZX', 'Polar ZX', ''), ('POLAR_ZY', 'Polar ZY', '')], default='POLAR_ZX', update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketNumber", "Value").init("in_value", True)
        self.inputs.new("ScNodeSocketBool", "Correct Aspect").init("in_aspect")
        self.inputs.new("ScNodeSocketBool", "Clip to Bounds").init("in_clip")
        self.inputs.new("ScNodeSocketBool", "Scale to Bounds").init("in_scale")
        self.inputs.new("ScNodeSocketString", "Direction").init("in_dir")
        self.inputs.new("ScNodeSocketString", "Align").init("in_align")
    
    def error_condition(self):
        return(
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['CUBE', 'CYLINDER', 'SPHERE'])
            or self.inputs["Value"].default_value < 0.0
            or (not self.inputs["Direction"].default_value in ['VIEW_ON_EQUATOR', 'VIEW_ON_POLES', 'ALIGN_TO_OBJECT'])
            or (not self.inputs["Align"].default_value in ['POLAR_ZX', 'POLAR_ZY'])
        )
    
    def functionality(self):
        super().functionality()
        if (self.inputs["Type"].default_value == 'CUBE'):
            bpy.ops.uv.cube_project(
                cube_size = self.inputs["Value"].default_value,
                correct_aspect = self.inputs["Correct Aspect"].default_value,
                clip_to_bounds = self.inputs["Clip to Bounds"].default_value,
                scale_to_bounds = self.inputs["Scale to Bounds"].default_value
            )
        elif (self.inputs["Type"].default_value == 'CYLINDER'):
            bpy.ops.uv.cylinder_project(
                direction = self.inputs["Direction"].default_value,
                align = self.inputs["Align"].default_value,
                radius = self.inputs["Value"].default_value,
                correct_aspect = self.inputs["Correct Aspect"].default_value,
                clip_to_bounds = self.inputs["Clip to Bounds"].default_value,
                scale_to_bounds = self.inputs["Scale to Bounds"].default_value
            )
        elif (self.inputs["Type"].default_value == 'SPHERE'):
            bpy.ops.uv.cylinder_project(
                direction = self.inputs["Direction"].default_value,
                align = self.inputs["Align"].default_value,
                correct_aspect = self.inputs["Correct Aspect"].default_value,
                clip_to_bounds = self.inputs["Clip to Bounds"].default_value,
                scale_to_bounds = self.inputs["Scale to Bounds"].default_value
            )