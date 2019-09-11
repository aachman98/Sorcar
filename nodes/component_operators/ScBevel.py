import bpy

from bpy.props import FloatProperty, EnumProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScBevel(Node, ScEditOperatorNode):
    bl_idname = "ScBevel"
    bl_label = "Bevel"

    in_offset_type: EnumProperty(name="Offset Type", items=[("OFFSET", "Offset", ""), ("WIDTH", "Width", ""), ("PERCENT", "Percent", ""), ("DEPTH", "Depth", "")], default="OFFSET", update=ScNode.update_value)
    in_offset: FloatProperty(name="Offset", default=0.0, min=-1000000.0, max=1000000.0, update=ScNode.update_value)
    in_segments: IntProperty(name="Segments", default=1, min=1, max=1000, update=ScNode.update_value)
    in_profile: FloatProperty(name="Profile", default=0.5, min=0.15, max=1.0, update=ScNode.update_value)
    in_vertex_only: BoolProperty(name="Vertex Only", update=ScNode.update_value)
    in_clamp_overlap: BoolProperty(name="Clamp Overlap", update=ScNode.update_value)
    in_loop_slide: BoolProperty(name="Loop Slide", default=True, update=ScNode.update_value)
    in_material: IntProperty(name="Material", default=0, min=-1, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Offset Type").init("in_offset_type")
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketNumber", "Segments").init("in_segments", True)
        self.inputs.new("ScNodeSocketNumber", "Profile").init("in_profile")
        self.inputs.new("ScNodeSocketBool", "Vertex Only").init("in_vertex_only", True)
        self.inputs.new("ScNodeSocketBool", "Clamp Overlap").init("in_clamp_overlap")
        self.inputs.new("ScNodeSocketBool", "Loop Slide").init("in_loop_slide")
        self.inputs.new("ScNodeSocketNumber", "Material").init("in_material")
    
    def error_condition(self):
        return(
            super().error_condition()
            or (not self.inputs["Offset Type"].default_value in ['OFFSET', 'WIDTH', 'DEPTH', 'PERCENT'])
            or (self.inputs["Offset"].default_value < -1000000 or self.inputs["Offset"].default_value > 1000000)
            or (int(self.inputs["Segments"].default_value) < 1 or int(self.inputs["Segments"].default_value) > 1000)
            or (self.inputs["Profile"].default_value < 0.15 or self.inputs["Profile"].default_value > 1)
            or int(self.inputs["Material"].default_value) < 0
        )
    
    def functionality(self):
        bpy.ops.mesh.bevel(
            offset_type = self.inputs["Offset Type"].default_value,
            offset = self.inputs["Offset"].default_value,
            segments = int(self.inputs["Segments"].default_value),
            profile = self.inputs["Profile"].default_value,
            vertex_only = self.inputs["Vertex Only"].default_value,
            clamp_overlap = self.inputs["Clamp Overlap"].default_value,
            loop_slide = self.inputs["Loop Slide"].default_value,
            material = int(self.inputs["Material"].default_value)
        )