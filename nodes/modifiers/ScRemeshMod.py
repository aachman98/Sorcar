import bpy

from bpy.props import EnumProperty, FloatProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScRemeshMod(Node, ScModifierNode):
    bl_idname = "ScRemeshMod"
    bl_label = "Remesh Modifier"
    bl_icon = 'MOD_REMESH'

    in_mode: EnumProperty(items=[("BLOCKS", "Blocks", ""), ("SMOOTH", "Smooth", ""), ("SHARP", "Sharp", "")], default="SHARP", update=ScNode.update_value)
    in_octree_depth: IntProperty(default=4, min=1, max=12, update=ScNode.update_value)
    in_scale: FloatProperty(default=0.9, min=0.0, max=0.99, update=ScNode.update_value)
    in_sharpness: FloatProperty(default=1.0, update=ScNode.update_value)
    in_use_smooth_shade: BoolProperty(update=ScNode.update_value)
    in_use_remove_disconnected: BoolProperty(default=True, update=ScNode.update_value)
    in_threshold: FloatProperty(default=1.0, min=0.0, max=1.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "REMESH"
        self.inputs.new("ScNodeSocketString", "Mode").init("in_mode", True)
        self.inputs.new("ScNodeSocketNumber", "Octree Depth").init("in_octree_depth", True)
        self.inputs.new("ScNodeSocketNumber", "Scale").init("in_scale", True)
        self.inputs.new("ScNodeSocketNumber", "Sharpness").init("in_sharpness")
        self.inputs.new("ScNodeSocketBool", "Smooth Shading").init("in_use_smooth_shade")
        self.inputs.new("ScNodeSocketBool", "Remove Disconnected Pieces").init("in_use_remove_disconnected")
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Mode"].default_value in ['BLOCKS', 'SMOOTH', 'SHARP'])
            or (int(self.inputs["Octree Depth"].default_value < 1) or int(self.inputs["Octree Depth"].default_value > 12))
            or (self.inputs["Scale"].default_value < 0 or self.inputs["Scale"].default_value > 0.99)
            or (self.inputs["Threshold"].default_value < 0 or self.inputs["Threshold"].default_value > 1)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].mode = self.inputs["Mode"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].octree_depth = int(self.inputs["Octree Depth"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].scale = self.inputs["Scale"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].sharpness = self.inputs["Sharpness"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_smooth_shade = self.inputs["Smooth Shading"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_remove_disconnected = self.inputs["Remove Disconnected Pieces"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].threshold = self.inputs["Threshold"].default_value