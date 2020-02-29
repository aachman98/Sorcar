import bpy

from bpy.props import FloatProperty, BoolProperty, IntProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScQuadriFlowRemesh(Node, ScObjectOperatorNode):
    bl_idname = "ScQuadriFlowRemesh"
    bl_label = "QuadriFlow Remesh (Blender 2.81+)"

    in_paint_symmetry: BoolProperty(default=True, update=ScNode.update_value)
    in_preserve_sharp: BoolProperty(update=ScNode.update_value)
    in_preserve_boundary: BoolProperty(update=ScNode.update_value)
    in_mesh_curvature: BoolProperty(update=ScNode.update_value)
    in_preserve_paint_mask: BoolProperty(update=ScNode.update_value)
    in_smooth_normals: BoolProperty(update=ScNode.update_value)
    in_mode: EnumProperty(name="Mode", items=[('RATIO', 'Ratio', ''), ('EDGE', 'Edge Length', ''), ('FACES', 'Faces', '')], update=ScNode.update_value)
    in_target_ratio: FloatProperty(default=1.0, min=0.0, update=ScNode.update_value)
    in_target_edge_length: FloatProperty(default=0.1, min=0.0000001, update=ScNode.update_value)
    in_target_faces: IntProperty(default=4000, min=1, update=ScNode.update_value)
    in_mesh_area: FloatProperty(default=-1.0, update=ScNode.update_value)
    in_seed: IntProperty(min=0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Mode").init("in_mode", True)
        self.inputs.new("ScNodeSocketNumber", "Ratio").init("in_target_ratio", True)
        self.inputs.new("ScNodeSocketNumber", "Edge Length").init("in_target_edge_length")
        self.inputs.new("ScNodeSocketNumber", "Number of Faces").init("in_target_faces")
        self.inputs.new("ScNodeSocketNumber", "Old Object Face Area").init("in_mesh_area")
        self.inputs.new("ScNodeSocketNumber", "Seed").init("in_seed", True)
        self.inputs.new("ScNodeSocketBool", "Use Paint Symmetry").init("in_paint_symmetry")
        self.inputs.new("ScNodeSocketBool", "Preserve Sharp").init("in_preserve_sharp")
        self.inputs.new("ScNodeSocketBool", "Preserve Mesh Boundary").init("in_preserve_boundary")
        self.inputs.new("ScNodeSocketBool", "Use Mesh Curvature").init("in_mesh_curvature")
        self.inputs.new("ScNodeSocketBool", "Preserve Paint Mask").init("in_preserve_paint_mask")
        self.inputs.new("ScNodeSocketBool", "Smooth Normals").init("in_smooth_normals", True)
    
    def error_condition(self):
        return(
            super().error_condition()
            or bpy.app.version[1] < 81
            or (not self.inputs["Mode"].default_value in ['RATIO', 'EDGE', 'FACES'])
            or self.inputs["Ratio"].default_value < 0.0
            or self.inputs["Edge Length"].default_value < 0.1
            or int(self.inputs["Number of Faces"].default_value) < 1
            or int(self.inputs["Seed"].default_value) < 0
        )

    def functionality(self):
        bpy.ops.object.quadriflow_remesh(
            use_paint_symmetry = self.inputs["Use Paint Symmetry"].default_value,
            use_preserve_sharp = self.inputs["Preserve Sharp"].default_value,
            use_preserve_boundary = self.inputs["Preserve Mesh Boundary"].default_value,
            use_mesh_curvature = self.inputs["Use Mesh Curvature"].default_value,
            preserve_paint_mask = self.inputs["Preserve Paint Mask"].default_value,
            smooth_normals = self.inputs["Smooth Normals"].default_value,
            mode = self.inputs["Mode"].default_value,
            target_ratio = self.inputs["Ratio"].default_value,
            target_edge_length = self.inputs["Edge Length"].default_value,
            target_faces = int(self.inputs["Number of Faces"].default_value),
            mesh_area = self.inputs["Old Object Face Area"].default_value,
            seed = int(self.inputs["Seed"].default_value)
        )
