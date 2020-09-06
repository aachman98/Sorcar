import bpy

from bpy.props import FloatProperty, EnumProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScBevel(Node, ScEditOperatorNode):
    bl_idname = "ScBevel"
    bl_label = "Bevel"

    in_offset_type: EnumProperty(items=[("OFFSET", "Offset", ""), ("WIDTH", "Width", ""), ("PERCENT", "Percent", ""), ("DEPTH", "Depth", "")], default="OFFSET", update=ScNode.update_value)
    in_offset: FloatProperty(min=0.0, max=1000000.0, update=ScNode.update_value)
    in_segments: IntProperty(default=1, min=1, max=1000, update=ScNode.update_value)
    in_profile: FloatProperty(default=0.5, min=0.15, max=1.0, update=ScNode.update_value)
    in_vertex_only: BoolProperty(update=ScNode.update_value)
    in_clamp_overlap: BoolProperty(update=ScNode.update_value)
    in_loop_slide: BoolProperty(default=True, update=ScNode.update_value)
    in_mark_seam: BoolProperty(update=ScNode.update_value)
    in_mark_sharp: BoolProperty(update=ScNode.update_value)
    in_material: IntProperty(default=-1, min=-1, update=ScNode.update_value)
    in_harden_normals: BoolProperty(update=ScNode.update_value)
    in_face_strength_mode: EnumProperty(items=[('NONE', 'None', ''), ('NEW', 'New', ''), ('AFFECTED', 'Affected', ''), ('ALL', 'All', '')], default="NONE", update=ScNode.update_value)
    in_miter_outer: EnumProperty(items=[("SHARP", "Sharp", ""), ("PATCH", "Patch", ""), ("ARC", "Arc", "")], default="SHARP", update=ScNode.update_value)
    in_miter_inner: EnumProperty(items=[("SHARP", "Sharp", ""), ("ARC", "Arc", "")], default="SHARP", update=ScNode.update_value)
    in_spread: FloatProperty(default=0.1, min=0.0, max=1000000.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Offset Type").init("in_offset_type")
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketNumber", "Segments").init("in_segments", True)
        self.inputs.new("ScNodeSocketNumber", "Profile").init("in_profile")
        self.inputs.new("ScNodeSocketBool", "Vertex Only").init("in_vertex_only", True)
        self.inputs.new("ScNodeSocketBool", "Clamp Overlap").init("in_clamp_overlap")
        self.inputs.new("ScNodeSocketBool", "Loop Slide").init("in_loop_slide")
        self.inputs.new("ScNodeSocketBool", "Mark Seams").init("in_mark_seam")
        self.inputs.new("ScNodeSocketBool", "Mark Sharp").init("in_mark_sharp")
        self.inputs.new("ScNodeSocketNumber", "Material").init("in_material")
        self.inputs.new("ScNodeSocketBool", "Harden Normals").init("in_harden_normals")
        self.inputs.new("ScNodeSocketString", "Face Strength Mode").init("in_face_strength_mode")
        self.inputs.new("ScNodeSocketString", "Outer Miter").init("in_miter_outer")
        self.inputs.new("ScNodeSocketString", "Inner Miter").init("in_miter_inner")
        self.inputs.new("ScNodeSocketNumber", "Spread").init("in_spread")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Offset Type"].default_value in ['OFFSET', 'WIDTH', 'DEPTH', 'PERCENT'])
            or (self.inputs["Offset Type"].default_value == 'PERCENT' and (self.inputs["Offset"].default_value < 0.0 or self.inputs["Offset"].default_value > 100.0))
            or (self.inputs["Offset"].default_value < 0.0 or self.inputs["Offset"].default_value > 1000000.0)
            or (int(self.inputs["Segments"].default_value) < 1 or int(self.inputs["Segments"].default_value) > 1000)
            or (self.inputs["Profile"].default_value < 0.15 or self.inputs["Profile"].default_value > 1)
            or int(self.inputs["Material"].default_value) < -1
            or (not self.inputs["Face Strength Mode"].default_value in ['NONE', 'NEW', 'AFFECTED', 'ALL'])
            or (not self.inputs["Outer Miter"].default_value in ['SHARP', 'PATCH', 'ARC'])
            or (not self.inputs["Inner Miter"].default_value in ['SHARP', 'ARC'])
            or (self.inputs["Spread"].default_value < 0.0 or self.inputs["Spread"].default_value > 1000000.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.bevel(
            offset_type = self.inputs["Offset Type"].default_value,
            offset = self.inputs["Offset"].default_value,
            offset_pct = self.inputs["Offset"].default_value,
            segments = int(self.inputs["Segments"].default_value),
            profile = self.inputs["Profile"].default_value,
            vertex_only = self.inputs["Vertex Only"].default_value,
            clamp_overlap = self.inputs["Clamp Overlap"].default_value,
            loop_slide = self.inputs["Loop Slide"].default_value,
            mark_seam = self.inputs["Mark Seams"].default_value,
            mark_sharp = self.inputs["Mark Sharp"].default_value,
            material = int(self.inputs["Material"].default_value),
            harden_normals = self.inputs["Harden Normals"].default_value,
            face_strength_mode = self.inputs["Face Strength Mode"].default_value,
            miter_outer = self.inputs["Outer Miter"].default_value,
            miter_inner = self.inputs["Inner Miter"].default_value,
            spread = self.inputs["Spread"].default_value
        )