import bpy

from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode
from ...helper import get_override

class ScSkinMod(Node, ScModifierNode):
    bl_idname = "ScSkinMod"
    bl_label = "Skin Modifier"
    
    in_branch_smoothing: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_resize: FloatVectorProperty(default=(1.0, 1.0, 1.0), update=ScNode.update_value)
    in_use_smooth_shade: BoolProperty(update=ScNode.update_value)
    in_use_x_symmetry: BoolProperty(default=True, update=ScNode.update_value)
    in_use_y_symmetry: BoolProperty(update=ScNode.update_value)
    in_use_z_symmetry: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "SKIN"
        self.inputs.new("ScNodeSocketNumber", "Branch Smoothing").init("in_branch_smoothing", True)
        self.inputs.new("ScNodeSocketVector", "Skin Resize").init("in_resize", True)
        self.inputs.new("ScNodeSocketNumber", "Smooth Shading").init("in_use_smooth_shade")
        self.inputs.new("ScNodeSocketNumber", "X").init("in_use_x_symmetry")
        self.inputs.new("ScNodeSocketNumber", "Y").init("in_use_y_symmetry")
        self.inputs.new("ScNodeSocketNumber", "Z").init("in_use_z_symmetry")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Branch Smoothing"].default_value < 0 or self.inputs["Branch Smoothing"].default_value > 1)
        )
    
    def functionality(self):
        bpy.context.object.modifiers[self.prop_mod_name].branch_smoothing = self.inputs["Branch Smoothing"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_smooth_shade = self.inputs["Smooth Shading"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_x_symmetry = self.inputs["X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_y_symmetry = self.inputs["Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_z_symmetry = self.inputs["Z"].default_value
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.transform.skin_resize(
            get_override(self.inputs["Object"].default_value, True),
            value = self.inputs["Skin Resize"].default_value
        )
        bpy.ops.object.mode_set(mode="OBJECT")
