import bpy

from bpy.props import FloatProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_setting import ScSettingNode

class ScProportionalEditing(Node, ScSettingNode):
    bl_idname = "ScProportionalEditing"
    bl_label = "Proportional Editing"

    in_falloff: EnumProperty(items=[('SMOOTH', 'Smooth', ''), ('SPHERE', 'Sphere', ''), ('ROOT', 'Root', ''), ('INVERSE_SQUARE', 'Inverse Square', ''), ('SHARP', 'Sharp', ''), ('LINEAR', 'Linear', ''), ('CONSTANT', 'Constant', ''), ('RANDOM', 'Random', '')], update=ScNode.update_value)
    in_size: FloatProperty(default=1.0, min=0.00001, max=5000, update=ScNode.update_value)
    in_connected: BoolProperty(update=ScNode.update_value)
    in_edit: BoolProperty(update=ScNode.update_value)
    in_object: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Falloff").init("in_falloff", True)
        self.inputs.new("ScNodeSocketNumber", "Size").init("in_size", True)
        self.inputs.new("ScNodeSocketBool", "Edit Mode").init("in_edit", True)
        self.inputs.new("ScNodeSocketBool", "Object Mode").init("in_object")
        self.inputs.new("ScNodeSocketBool", "Connected Only").init("in_connected")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Falloff"].default_value in ['SMOOTH', 'SPHERE', 'ROOT', 'INVERSE_SQUARE', 'SHARP', 'LINEAR', 'CONSTANT', 'RANDOM'])
            or (self.inputs["Size"].default_value < 0.00001 or self.inputs["Size"].default_value > 5000)
        )
    
    def functionality(self):
        bpy.context.scene.tool_settings.proportional_edit_falloff = self.inputs["Falloff"].default_value
        bpy.context.scene.tool_settings.proportional_size = self.inputs["Size"].default_value
        bpy.context.scene.tool_settings.use_proportional_connected = self.inputs["Connected Only"].default_value
        bpy.context.scene.tool_settings.use_proportional_edit = self.inputs["Edit Mode"].default_value
        bpy.context.scene.tool_settings.use_proportional_edit_objects = self.inputs["Object Mode"].default_value