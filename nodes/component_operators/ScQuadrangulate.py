import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScQuadrangulate(Node, ScEditOperatorNode):
    bl_idname = "ScQuadrangulate"
    bl_label = "Quadrangulate"
    
    in_face_threshold: FloatProperty(default=0.698132, min=0.0, max=3.14159, unit="ROTATION", update=ScNode.update_value)
    in_shape_threshold: FloatProperty(default=0.698132, min=0.0, max=3.14159, unit="ROTATION", update=ScNode.update_value)
    in_uvs: BoolProperty(update=ScNode.update_value)
    in_vcols: BoolProperty(update=ScNode.update_value)
    in_seam: BoolProperty(update=ScNode.update_value)
    in_sharp: BoolProperty(update=ScNode.update_value)
    in_materials: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Max Face Angle").init("in_face_threshold", True)
        self.inputs.new("ScNodeSocketNumber", "Max Shape Angle").init("in_shape_threshold")
        self.inputs.new("ScNodeSocketBool", "Compare UVs").init("in_uvs")
        self.inputs.new("ScNodeSocketBool", "Compare VCols").init("in_vcols")
        self.inputs.new("ScNodeSocketBool", "Compare Seam").init("in_seam")
        self.inputs.new("ScNodeSocketBool", "Compare Sharp").init("in_sharp")
        self.inputs.new("ScNodeSocketBool", "Compare Materials").init("in_materials")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Max Face Angle"].default_value < 0.0 or self.inputs["Max Face Angle"].default_value > 3.14159)
            or (self.inputs["Max Shape Angle"].default_value < 0.0 or self.inputs["Max Shape Angle"].default_value > 3.14159)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.tris_convert_to_quads(
            face_threshold = self.inputs["Max Face Angle"].default_value,
            shape_threshold = self.inputs["Max Shape Angle"].default_value,
            uvs = self.inputs["Compare UVs"].default_value,
            vcols = self.inputs["Compare VCols"].default_value,
            seam = self.inputs["Compare Seam"].default_value,
            sharp = self.inputs["Compare Sharp"].default_value,
            materials = self.inputs["Compare Materials"].default_value
        )