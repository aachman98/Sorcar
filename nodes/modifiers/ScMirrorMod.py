import bpy

from bpy.props import FloatProperty, BoolProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScMirrorMod(Node, ScModifierNode):
    bl_idname = "ScMirrorMod"
    bl_label = "Mirror Modifier"
    bl_icon = 'MOD_MIRROR'
    
    in_use_x: BoolProperty(default=True, update=ScNode.update_value)
    in_use_y: BoolProperty(update=ScNode.update_value)
    in_use_z: BoolProperty(update=ScNode.update_value)
    in_use_bisect_x: BoolProperty(default=True, update=ScNode.update_value)
    in_use_bisect_y: BoolProperty(update=ScNode.update_value)
    in_use_bisect_z: BoolProperty(update=ScNode.update_value)
    in_use_bisect_flip_x: BoolProperty(default=True, update=ScNode.update_value)
    in_use_bisect_flip_y: BoolProperty(update=ScNode.update_value)
    in_use_bisect_flip_z: BoolProperty(update=ScNode.update_value)
    in_mirror_object: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_use_mirror_merge: BoolProperty(default=True, update=ScNode.update_value)
    in_use_clip: BoolProperty(update=ScNode.update_value)
    in_use_mirror_vertex_groups: BoolProperty(default=True, update=ScNode.update_value)
    in_merge_threshold: FloatProperty(default=0.001, min=0, soft_max=1, update=ScNode.update_value)
    in_use_mirror_u: BoolProperty(update=ScNode.update_value)
    in_use_mirror_v: BoolProperty(update=ScNode.update_value)
    in_mirror_offset_u: FloatProperty(default=0.0, min=-1.0, max=1.0, update=ScNode.update_value)
    in_mirror_offset_v: FloatProperty(default=0.0, min=-1.0, max=1.0, update=ScNode.update_value)
    in_offset_u: FloatProperty(default=0.0, soft_min=-1, soft_max=1, min=-1000, max=1000, update=ScNode.update_value)
    in_offset_v: FloatProperty(default=0.0, soft_min=-1, soft_max=1, min=-1000, max=1000, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "MIRROR"
        self.inputs.new("ScNodeSocketBool", "Axis X").init("in_use_x", True)
        self.inputs.new("ScNodeSocketBool", "Axis Y").init("in_use_y", True)
        self.inputs.new("ScNodeSocketBool", "Axis Z").init("in_use_z", True)
        self.inputs.new("ScNodeSocketBool", "Bisect X").init("in_use_bisect_x")
        self.inputs.new("ScNodeSocketBool", "Bisect Y").init("in_use_bisect_y")
        self.inputs.new("ScNodeSocketBool", "Bisect Z").init("in_use_bisect_z")
        self.inputs.new("ScNodeSocketBool", "Flip X").init("in_use_bisect_flip_x")
        self.inputs.new("ScNodeSocketBool", "Flip Y").init("in_use_bisect_flip_y")
        self.inputs.new("ScNodeSocketBool", "Flip Z").init("in_use_bisect_flip_z")
        self.inputs.new("ScNodeSocketObject", "Mirror Object").init("in_mirror_object")
        self.inputs.new("ScNodeSocketBool", "Merge").init("in_use_mirror_merge")
        self.inputs.new("ScNodeSocketBool", "Clipping").init("in_use_clip")
        self.inputs.new("ScNodeSocketBool", "Vertex Groups").init("in_use_mirror_vertex_groups")
        self.inputs.new("ScNodeSocketNumber", "Merge Limit").init("in_merge_threshold")
        self.inputs.new("ScNodeSocketBool", "Flip U").init("in_use_mirror_u")
        self.inputs.new("ScNodeSocketBool", "Flip V").init("in_use_mirror_v")
        self.inputs.new("ScNodeSocketNumber", "Flip U Offset").init("in_mirror_offset_u")
        self.inputs.new("ScNodeSocketNumber", "Flip V Offset").init("in_mirror_offset_v")
        self.inputs.new("ScNodeSocketNumber", "U Offset").init("in_offset_u")
        self.inputs.new("ScNodeSocketNumber", "V Offset").init("in_offset_v")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Merge Limit"].default_value < 0
            or (self.inputs["Flip U"].default_value < -1 or self.inputs["Flip U"].default_value > 1)
            or (self.inputs["Flip V"].default_value < -1 or self.inputs["Flip V"].default_value > 1)
            or (self.inputs["U Offset"].default_value < -1000 or self.inputs["U Offset"].default_value > 1000)
            or (self.inputs["V Offset"].default_value < -1000 or self.inputs["V Offset"].default_value > 1000)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].use_axis[0] = self.inputs["Axis X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_axis[1] = self.inputs["Axis Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_axis[2] = self.inputs["Axis Z"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_bisect_axis[0] = self.inputs["Bisect X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_bisect_axis[1] = self.inputs["Bisect Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_bisect_axis[2] = self.inputs["Bisect Z"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_bisect_flip_axis[0] = self.inputs["Flip X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_bisect_flip_axis[1] = self.inputs["Flip Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_bisect_flip_axis[2] = self.inputs["Flip Z"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].mirror_object = self.inputs["Mirror Object"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_mirror_merge = self.inputs["Merge"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_clip = self.inputs["Clipping"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_mirror_vertex_groups = self.inputs["Vertex Groups"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].merge_threshold = self.inputs["Merge Limit"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_mirror_u = self.inputs["Flip U"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_mirror_v = self.inputs["Flip V"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].mirror_offset_u = self.inputs["Flip U Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].mirror_offset_v = self.inputs["Flip V Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset_u = self.inputs["U Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset_v = self.inputs["V Offset"].default_value