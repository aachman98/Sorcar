import bpy

from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScBridgeEdgeLoops(Node, ScEditOperatorNode):
    bl_idname = "ScBridgeEdgeLoops"
    bl_label = "Bridge Edge Loops"
    
    in_type: EnumProperty(items=[("SINGLE", "Single", ""), ("CLOSED", "Closed", ""), ("PAIRS", "Pairs", "")], default="SINGLE", update=ScNode.update_value)
    in_use_merge: BoolProperty(update=ScNode.update_value)
    in_merge_factor: FloatProperty(default=0.5, min=0.0, max=1.0, update=ScNode.update_value)
    in_twist_offset: IntProperty(default=0, min=-1000, max=1000, update=ScNode.update_value)
    in_number_cuts: IntProperty(default=0, min=0, max=1000, update=ScNode.update_value)
    in_interpolation: EnumProperty(items=[("LINEAR", "Linear", ""), ("PATH", "Path", ""), ("SURFACE", "Surface", "")], default="PATH", update=ScNode.update_value)
    in_smoothness: FloatProperty(default=1.0, min=0.0, max=1000.0, update=ScNode.update_value)
    in_profile_shape_factor: FloatProperty(default=0.0, min=-1000.0, max=1000.0, update=ScNode.update_value)
    in_profile_shape: EnumProperty(items=[("SMOOTH", "Smooth", ""), ("SPHERE", "Sphere", ""), ("ROOT", "Root", ""), ("INVERSE_SQUARE", "Inverse Square", ""), ("SHARP", "Sharp", ""), ("LINEAR", "Linear", "")], default="SMOOTH", update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Connect Loops").init("in_type")
        self.inputs.new("ScNodeSocketBool", "Merge").init("in_use_merge")
        self.inputs.new("ScNodeSocketNumber", "Merge Factor").init("in_merge_factor")
        self.inputs.new("ScNodeSocketNumber", "Twist").init("in_twist_offset", True)
        self.inputs.new("ScNodeSocketNumber", "Number of Cuts").init("in_number_cuts", True)
        self.inputs.new("ScNodeSocketString", "Interpolation").init("in_interpolation")
        self.inputs.new("ScNodeSocketNumber", "Smoothness").init("in_smoothness")
        self.inputs.new("ScNodeSocketNumber", "Profile Factor").init("in_profile_shape_factor")
        self.inputs.new("ScNodeSocketString", "Profile Shape").init("in_profile_shape")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Connect Loops"].default_value in ['SINGLE', 'CLOSED', 'PAIRS'])
            or (self.inputs["Merge Factor"].default_value < 0.0 or self.inputs["Merge Factor"].default_value > 1.0)
            or (int(self.inputs["Twist"].default_value) < -1000 or int(self.inputs["Twist"].default_value) > 1000)
            or (int(self.inputs["Number of Cuts"].default_value) < 0 or int(self.inputs["Number of Cuts"].default_value) > 1000)
            or (not self.inputs["Interpolation"].default_value in ['LINEAR', 'PATH', 'SURFACE'])
            or (self.inputs["Smoothness"].default_value < 0.0 or self.inputs["Smoothness"].default_value > 1000.0)
            or (self.inputs["Profile Factor"].default_value < -1000.0 or self.inputs["Smoothness"].default_value > 1000.0)
            or (not self.inputs["Profile Shape"].default_value in ['SMOOTH', 'SPHERE', 'ROOT', 'INVERSE_SQUARE', 'SHARP', 'LINEAR'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.bridge_edge_loops(
            type = self.inputs["Connect Loops"].default_value,
            use_merge = self.inputs["Merge"].default_value,
            merge_factor = self.inputs["Merge Factor"].default_value,
            twist_offset = int(self.inputs["Twist"].default_value),
            number_cuts = int(self.inputs["Number of Cuts"].default_value),
            interpolation = self.inputs["Interpolation"].default_value,
            smoothness = self.inputs["Smoothness"].default_value,
            profile_shape_factor = self.inputs["Profile Factor"].default_value,
            profile_shape = self.inputs["Profile Shape"].default_value
        )