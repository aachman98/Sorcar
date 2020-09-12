import bpy

from bpy.props import EnumProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectSimilar(Node, ScSelectionNode):
    bl_idname = "ScSelectSimilar"
    bl_label = "Select Similar"
    
    in_type: EnumProperty(items=[('NORMAL', 'Normal', ""), ('FACE', 'Face', ""), ('VGROUP', 'Vertex Group', ""), ('EDGE', 'Edge', ""), ('LENGTH', 'Length', ""), ('DIR', 'Direction', ""), ('FACE', 'Face', ""), ('FACE_ANGLE', 'Face Angle', ""), ('CREASE', 'Crease', ""), ('BEVEL', 'Bevel', ""), ('SEAM', 'Seam', ""), ('SHARP', 'Sharp', ""), ('FREESTYLE_EDGE', 'Freestyle Edge', ""), ('MATERIAL', 'Material', ""), ('AREA', 'Area', ""), ('SIDES', 'Sides', ""), ('PERIMETER', 'Perimeter', ""), ('COPLANAR', 'Co-Planar', ""), ('SMOOTH', 'Smooth', ""), ('FACE_MAP', 'Face Map', ""), ('FREESTYLE_FACE', 'Freestyle Face', "")], default="NORMAL", update=ScNode.update_value)
    in_compare: EnumProperty(items=[("EQUAL", "Equal", ""), ("GREATER", "Greater", ""), ("LESS", "Less", "")], default="EQUAL", update=ScNode.update_value)
    in_threshold: FloatProperty(min=0.0, max=1.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketString", "Compare").init("in_compare")
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['NORMAL', 'FACE', 'VGROUP', 'EDGE', 'LENGTH', 'DIR', 'FACE', 'FACE_ANGLE', 'CREASE', 'BEVEL', 'SEAM', 'SHARP', 'FREESTYLE_EDGE', 'MATERIAL', 'AREA', 'SIDES', 'PERIMETER', 'COPLANAR', 'SMOOTH', 'FACE_MAP', 'FREESTYLE_FACE'])
            or (not self.inputs["Compare"].default_value in ['EQUAL', 'GREATER', 'LESS'])
            or (self.inputs["Threshold"].default_value < 0 or self.inputs["Threshold"].default_value > 1)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_similar(
            type = self.inputs["Type"].default_value,
            compare = self.inputs["Compare"].default_value,
            threshold = self.inputs["Threshold"].default_value
        )