import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScWaveMod(Node, ScModifierNode):
    bl_idname = "ScWaveMod"
    bl_label = "Wave Modifier"
    bl_icon = 'MOD_WAVE'
    
    in_offset: FloatProperty(min=0.0, max=1048570.0, update=ScNode.update_value)
    in_speed: FloatProperty(default=0.25, soft_min=0.0, soft_max=1.0, update=ScNode.update_value)
    in_height: FloatProperty(default=0.5, soft_min=-2.0, soft_max=2.0, update=ScNode.update_value)
    in_width: FloatProperty(default=1.5, min=0.0, soft_max=5.0, update=ScNode.update_value)
    in_narrowness: FloatProperty(default=1.5, min=0.0, soft_max=10.0, update=ScNode.update_value)
    in_motion_x: BoolProperty(default=True, update=ScNode.update_value)
    in_motion_y: BoolProperty(default=True, update=ScNode.update_value)
    in_motion_cyclic: BoolProperty(default=True, update=ScNode.update_value)
    in_normals: BoolProperty(update=ScNode.update_value)
    in_normals_x: BoolProperty(default=True, update=ScNode.update_value)
    in_normals_y: BoolProperty(default=True, update=ScNode.update_value)
    in_normals_z: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "WAVE"
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketNumber", "Speed").init("in_speed")
        self.inputs.new("ScNodeSocketNumber", "Height").init("in_height")
        self.inputs.new("ScNodeSocketNumber", "Width").init("in_width")
        self.inputs.new("ScNodeSocketNumber", "Narrowness").init("in_narrowness")
        self.inputs.new("ScNodeSocketBool", "Motion X").init("in_motion_x")
        self.inputs.new("ScNodeSocketBool", "Motion Y").init("in_motion_y")
        self.inputs.new("ScNodeSocketBool", "Motion Cyclic").init("in_motion_cyclic")
        self.inputs.new("ScNodeSocketBool", "Normals").init("in_normals")
        self.inputs.new("ScNodeSocketBool", "Normals X").init("in_normals_x")
        self.inputs.new("ScNodeSocketBool", "Normals Y").init("in_normals_y")
        self.inputs.new("ScNodeSocketBool", "Normals Z").init("in_normals_z")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Offset"].default_value < 0.0 or self.inputs["Offset"].default_value > 1048570.0)
            or self.inputs["Width"].default_value < 0.0
            or self.inputs["Narrowness"].default_value < 0.0
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].time_offset = bpy.context.scene.frame_current - self.inputs["Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].speed = self.inputs["Speed"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].height = self.inputs["Height"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].width = self.inputs["Width"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].narrowness = self.inputs["Narrowness"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_x = self.inputs["Motion X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_y = self.inputs["Motion Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_cyclic = self.inputs["Motion Cyclic"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_normal = self.inputs["Normals"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_normal_x = self.inputs["Normals X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_normal_y = self.inputs["Normals Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_normal_z = self.inputs["Normals Z"].default_value