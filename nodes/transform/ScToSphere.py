import bpy

from bpy.props import EnumProperty, FloatProperty, BoolProperty, FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_transform import ScTransformNode
from ...helper import get_override, focus_on_object

class ScToSphere(Node, ScNode):
    bl_idname = "ScToSphere"
    bl_label = "To Sphere"

    in_value: FloatProperty(default=0.5, min=0.0, max=1.0, update=ScNode.update_value)
    in_mirror: BoolProperty(update=ScNode.update_value)
    in_center: FloatVectorProperty(update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.inputs.new("ScNodeSocketNumber", "Value").init("in_value", True)
        self.inputs.new("ScNodeSocketBool", "Mirror").init("in_mirror")
        self.inputs.new("ScNodeSocketVector", "Center").init("in_center")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            self.inputs["Object"].default_value == None
            or (self.inputs["Value"].default_value < 0.0 or self.inputs["Value"].default_value > 1.0)
        )
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value, True)
    
    def functionality(self):
        bpy.ops.transform.tosphere(
            get_override(self.inputs["Object"].default_value, True),
            value = self.inputs["Value"].default_value,
            mirror = self.inputs["Mirror"].default_value,
            center_override = self.inputs["Center"].default_value,
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
    
    def post_execute(self):
        return {"Object": self.inputs["Object"].default_value}