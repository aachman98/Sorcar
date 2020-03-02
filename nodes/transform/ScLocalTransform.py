import bpy

from bpy.props import EnumProperty, FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_transform import ScTransformNode
from ...helper import get_override

class ScLocalTransform(Node, ScTransformNode):
    bl_idname = "ScLocalTransform"
    bl_label = "Local Transform"

    in_mode: EnumProperty(items=[('TRANSLATION', 'Translate', ''), ('ROTATION', 'Rotate', ''), ('RESIZE', 'Scale', ''), ('SHEAR', 'Shear', ''), ('BEND', 'Bend', ''), ('SHRINKFATTEN', 'Shrink-Fatten', ''), ('TILT', 'Tilt', ''), ('PUSHPULL', 'Push-Pull', ''), ('SKIN_RESIZE', 'Skin Resize', ''), ('CREASE', 'Crease', ''), ('MIRROR', 'Mirror', ''), ('ALIGN', 'Align', ''), ('EDGESLIDE', 'Edge Slide', '')], update=ScNode.update_value)
    in_x: FloatProperty(update=ScNode.update_value)
    in_y: FloatProperty(update=ScNode.update_value)
    in_z: FloatProperty(update=ScNode.update_value)
    in_w: FloatProperty(update=ScNode.update_value)
    in_axis: EnumProperty(items=[('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', '')], update=ScNode.update_value)
    in_mirror: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Mode").init("in_mode", True)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_x", True)
        self.inputs.new("ScNodeSocketNumber", "Y").init("in_y", True)
        self.inputs.new("ScNodeSocketNumber", "Z").init("in_z", True)
        self.inputs.new("ScNodeSocketNumber", "W").init("in_w")
        self.inputs.new("ScNodeSocketString", "Axis").init("in_axis")
        self.inputs.new("ScNodeSocketBool", "Mirror").init("in_mirror")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Mode"].default_value in ['TRANSLATION', 'ROTATION', 'RESIZE', 'SHEAR', 'BEND', 'SHRINKFATTEN', 'TILT', 'PUSHPULL', 'SKIN_RESIZE', 'CREASE', 'MIRROR', 'ALIGN', 'EDGESLIDE'])
            or (not self.inputs["Axis"].default_value in ['X', 'Y', 'Z'])
            or (self.inputs["Mode"].default_value in ['CREASE', 'SKIN_RESIZE', 'EDGESLIDE'] and not self.inputs["Edit Mode"].default_value)
        )
    
    def functionality(self):
        bpy.ops.transform.transform(
            get_override(self.inputs["Object"].default_value, self.inputs["Edit Mode"].default_value),
            mode = self.inputs["Mode"].default_value,
            value = (self.inputs["X"].default_value, self.inputs["Y"].default_value, self.inputs["Z"].default_value, self.inputs["W"].default_value),
            orient_axis = self.inputs["Axis"].default_value,
            orient_type = bpy.context.scene.transform_orientation_slots[0].type,
            mirror = self.inputs["Mirror"].default_value,
            use_proportional_edit = bpy.context.scene.tool_settings.use_proportional_edit,
            proportional_edit_falloff = bpy.context.scene.tool_settings.proportional_edit_falloff,
            proportional_size = bpy.context.scene.tool_settings.proportional_size,
            use_proportional_connected = bpy.context.scene.tool_settings.use_proportional_connected,
            # use_proportional_projected = bpy.context.scene.tool_settings.use_proportional_projected,
            snap = bpy.context.scene.tool_settings.use_snap,
            snap_target = bpy.context.scene.tool_settings.snap_target,
            # snap_point = (0, 0, 0),
            snap_align = bpy.context.scene.tool_settings.use_snap_align_rotation,
            # snap_normal = bpy.context.scene.tool_settings.use_snap_align_rotation,
        )