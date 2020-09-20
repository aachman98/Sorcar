import bpy

from bpy.props import FloatProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScBuildMod(Node, ScModifierNode):
    bl_idname = "ScBuildMod"
    bl_label = "Build Modifier"
    bl_icon = 'MOD_BUILD'
    
    in_percent: FloatProperty(default=50.0, min=0.0, max=100.0, update=ScNode.update_value)
    in_reverse: BoolProperty(update=ScNode.update_value)
    in_random: BoolProperty(update=ScNode.update_value)
    in_seed: IntProperty(default=1, min=1, max=1048574, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "BUILD"
        self.inputs.new("ScNodeSocketNumber", "Percent").init("in_percent", True)
        self.inputs.new("ScNodeSocketBool", "Reverse").init("in_reverse", True)
        self.inputs.new("ScNodeSocketBool", "Randomize").init("in_random")
        self.inputs.new("ScNodeSocketNumber", "Seed").init("in_seed")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Percent"].default_value < 0.0 or self.inputs["Percent"].default_value > 100.0)
            or (int(self.inputs["Seed"].default_value) < 1 or int(self.inputs["Seed"].default_value > 1048574))
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].frame_start = bpy.context.scene.frame_current_final - self.inputs["Percent"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].frame_duration = 100.0
        bpy.context.object.modifiers[self.prop_mod_name].use_reverse = self.inputs["Reverse"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_random_order = self.inputs["Randomize"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].seed = int(self.inputs["Seed"].default_value)