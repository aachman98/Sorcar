import bpy

from bpy.props import FloatProperty, IntProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScSubdivideEdgeRing(Node, ScEditOperatorNode):
    bl_idname = "ScSubdivideEdgeRing"
    bl_label = "Subdivide Edge Ring"
    
    in_number_cuts: IntProperty(default=10, min=0, max=1000, update=ScNode.update_value)
    in_interpolation: EnumProperty(items=[("PATH", "Path", ""), ("LINEAR", "Linear", ""), ("SURFACE", "Surface", "")], default="PATH", update=ScNode.update_value)
    in_smoothness: FloatProperty(default=1.0, min=0.0, max=1000.0, update=ScNode.update_value)
    in_profile_shape: EnumProperty(items=[('SMOOTH', 'Smooth', ''), ('SPHERE', 'Sphere', ''), ('ROOT', 'Root', ''), ('INVERSE_SQUARE', 'Inverse_square', ''), ('SHARP', 'Sharp', ''), ('LINEAR', 'Linear', '')], default='SMOOTH', update=ScNode.update_value)
    in_profile_shape_factor: FloatProperty(min=-1000.0, max=1000.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Number of Cuts").init("in_number_cuts", True)
        self.inputs.new("ScNodeSocketString", "Interpolation").init("in_interpolation")
        self.inputs.new("ScNodeSocketNumber", "Smoothness").init("in_smoothness", True)
        self.inputs.new("ScNodeSocketString", "Profile Shape").init("in_profile_shape")
        self.inputs.new("ScNodeSocketNumber", "Profile Factor").init("in_profile_shape_factor")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Number of Cuts"].default_value) < 0 or int(self.inputs["Number of Cuts"].default_value) > 1000)
            or (not self.inputs["Interpolation"].default_value in ['LINEAR', 'PATH', 'SURFACE'])
            or (self.inputs["Smoothness"].default_value < 0.0 or self.inputs["Smoothness"].default_value > 1000.0)
            or (not self.inputs["Profile Shape"].default_value in ['SMOOTH', 'SPHERE', 'ROOT', 'INVERSE_SQUARE', 'SHARP', 'LINEAR'])
            or (self.inputs["Profile Factor"].default_value < -1000.0 or self.inputs["Profile Factor"].default_value > 1000.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.subdivide_edgering(
            number_cuts = int(self.inputs["Number of Cuts"].default_value),
            interpolation = self.inputs["Interpolation"].default_value,
            smoothness = self.inputs["Smoothness"].default_value,
            profile_shape_factor = self.inputs["Profile Factor"].default_value,
            profile_shape = self.inputs["Profile Shape"].default_value
        )