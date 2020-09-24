import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScVoxelRemesh(Node, ScObjectOperatorNode):
    bl_idname = "ScVoxelRemesh"
    bl_label = "Voxel Remesh"
    bl_icon = 'FILE_VOLUME'

    in_remesh_voxel_size: FloatProperty(default=0.1, min=0.0001, update=ScNode.update_value)
    in_remesh_voxel_adaptivity: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_use_remesh_fix_poles: BoolProperty(default=False, update=ScNode.update_value)
    in_use_remesh_smooth_normals: BoolProperty(default=False, update=ScNode.update_value)
    in_use_remesh_preserve_volume: BoolProperty(default=False, update=ScNode.update_value)
    in_use_remesh_preserve_paint_mask: BoolProperty(default=False, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Voxel Size").init("in_remesh_voxel_size", True)
        self.inputs.new("ScNodeSocketNumber", "Adaptivity").init("in_remesh_voxel_adaptivity")
        self.inputs.new("ScNodeSocketBool", "Fix Poles").init("in_use_remesh_fix_poles")
        self.inputs.new("ScNodeSocketBool", "Smooth Normals").init("in_use_remesh_smooth_normals")
        self.inputs.new("ScNodeSocketBool", "Preserve Volume").init("in_use_remesh_preserve_volume")
        self.inputs.new("ScNodeSocketBool", "Preserve Paint Mask").init("in_use_remesh_preserve_paint_mask")
    
    def error_condition(self):
        return (
            super().error_condition()
            or bpy.app.version[1] < 81
            or self.inputs["Voxel Size"].default_value < 0.0
            or (self.inputs["Adaptivity"].default_value < 0.0 or self.inputs["Adaptivity"].default_value > 1.0)
        )

    def functionality(self):
        super().functionality()
        self.inputs["Object"].default_value.data.remesh_voxel_size = self.inputs["Voxel Size"].default_value
        self.inputs["Object"].default_value.data.remesh_voxel_adaptivity = self.inputs["Adaptivity"].default_value
        self.inputs["Object"].default_value.data.use_remesh_fix_poles = self.inputs["Fix Poles"].default_value
        self.inputs["Object"].default_value.data.use_remesh_smooth_normals = self.inputs["Smooth Normals"].default_value
        self.inputs["Object"].default_value.data.use_remesh_preserve_volume = self.inputs["Preserve Volume"].default_value
        self.inputs["Object"].default_value.data.use_remesh_preserve_paint_mask = self.inputs["Preserve Paint Mask"].default_value
        bpy.ops.object.voxel_remesh()
