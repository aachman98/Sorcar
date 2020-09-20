import bpy

from bpy.props import FloatProperty, EnumProperty, PointerProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScScrewMod(Node, ScModifierNode):
    bl_idname = "ScScrewMod"
    bl_label = "Screw Modifier"
    bl_icon = 'MOD_SCREW'
    
    in_axis: EnumProperty(items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="Z", update=ScNode.update_value)
    in_object: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_angle: FloatProperty(default=6.283185, unit="ROTATION", update=ScNode.update_value)
    in_steps: IntProperty(default=16, min=2, max=10000, soft_max=512, update=ScNode.update_value)
    in_render_steps: IntProperty(default=16, min=2, max=10000, soft_max=512, update=ScNode.update_value)
    in_use_smooth_shade: BoolProperty(default=True, update=ScNode.update_value)
    in_use_merge_vertices: BoolProperty(update=ScNode.update_value)
    in_merge_threshold: FloatProperty(default=0.01, min=0, update=ScNode.update_value)
    in_screw_offset: FloatProperty(update=ScNode.update_value)
    in_use_object_screw_offset: BoolProperty(update=ScNode.update_value)
    in_use_normal_calculate: BoolProperty(update=ScNode.update_value)
    in_use_normal_flip: BoolProperty(update=ScNode.update_value)
    in_iterations: IntProperty(default=1, min=1, max=10000, update=ScNode.update_value)
    in_use_stretch_u: BoolProperty(update=ScNode.update_value)
    in_use_stretch_v: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "SCREW"
        self.inputs.new("ScNodeSocketString", "Axis").init("in_axis", True)
        self.inputs.new("ScNodeSocketObject", "Axis Object").init("in_object")
        self.inputs.new("ScNodeSocketNumber", "Angle").init("in_angle", True)
        self.inputs.new("ScNodeSocketNumber", "Steps").init("in_steps", True)
        self.inputs.new("ScNodeSocketNumber", "Render Steps").init("in_render_steps")
        self.inputs.new("ScNodeSocketBool", "Smooth Shading").init("in_use_smooth_shade")
        self.inputs.new("ScNodeSocketBool", "Merge Vertices").init("in_use_merge_vertices")
        self.inputs.new("ScNodeSocketNumber", "Merge Distance").init("in_merge_threshold")
        self.inputs.new("ScNodeSocketNumber", "Screw").init("in_screw_offset", True)
        self.inputs.new("ScNodeSocketBool", "Object Screw").init("in_use_object_screw_offset")
        self.inputs.new("ScNodeSocketBool", "Calc Order").init("in_use_normal_calculate")
        self.inputs.new("ScNodeSocketBool", "Flip").init("in_use_normal_flip")
        self.inputs.new("ScNodeSocketNumber", "Iterations").init("in_iterations")
        self.inputs.new("ScNodeSocketBool", "Stretch U").init("in_use_stretch_u")
        self.inputs.new("ScNodeSocketBool", "Stretch V").init("in_use_stretch_v")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Axis"].default_value in ['X', 'Y', 'Z'])
            or (int(self.inputs["Steps"].default_value) < 2 or int(self.inputs["Steps"].default_value) > 10000)
            or (int(self.inputs["Render Steps"].default_value) < 2 or int(self.inputs["Render Steps"].default_value) > 10000)
            or self.inputs["Merge Distance"].default_value < 0
            or (int(self.inputs["Iterations"].default_value) < 1 or int(self.inputs["Render Steps"].default_value) > 10000)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].axis = self.inputs["Axis"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].object = self.inputs["Axis Object"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].angle = self.inputs["Angle"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].steps = int(self.inputs["Steps"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].render_steps = int(self.inputs["Render Steps"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].use_smooth_shade = self.inputs["Smooth Shading"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_merge_vertices = self.inputs["Merge Vertices"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].merge_threshold = self.inputs["Merge Distance"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].screw_offset = self.inputs["Screw"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_object_screw_offset = self.inputs["Object Screw"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_normal_calculate = self.inputs["Calc Order"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_normal_flip = self.inputs["Flip"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].iterations = int(self.inputs["Iterations"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].use_stretch_u = self.inputs["Stretch U"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_stretch_v = self.inputs["Stretch V"].default_value