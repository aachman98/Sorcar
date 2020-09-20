import bpy

from bpy.props import FloatProperty, BoolProperty, PointerProperty, StringProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScHookMod(Node, ScModifierNode):
    bl_idname = "ScHookMod"
    bl_label = "Hook Modifier"
    bl_icon = 'HOOK'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    in_object: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_falloff_radius: FloatProperty(min=0.0, update=ScNode.update_value)
    in_strength: FloatProperty(default=1.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_falloff_type: EnumProperty(items=[('NONE', 'No Falloff', ''), ('SMOOTH', 'Smooth', ''), ('SPHERE', 'Sphere', ''), ('ROOT', 'Root', ''), ('INVERSE_SQUARE', 'Inverse Square', ''), ('SHARP', 'Sharp', ''), ('LINEAR', 'Linear', ''), ('CONSTANT', 'Constant', '')], default='SMOOTH', update=ScNode.update_value)
    in_use_falloff_uniform: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "HOOK"
        self.inputs.new("ScNodeSocketObject", "Hook Object").init("in_object", True)
        self.inputs.new("ScNodeSocketNumber", "Radius").init("in_falloff_radius", True)
        self.inputs.new("ScNodeSocketNumber", "Strength").init("in_strength", True)
        self.inputs.new("ScNodeSocketString", "Falloff Type").init("in_falloff_type")
        self.inputs.new("ScNodeSocketBool", "Uniform Faloff").init("in_use_falloff_uniform")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Hook Object"].default_value == None
            or self.inputs["Radius"].default_value < 0
            or (self.inputs["Strength"].default_value < 0 or self.inputs["Strength"].default_value > 1)
            or (not self.inputs["Falloff Type"].default_value in ['NONE', 'SMOOTH', 'SPHERE', 'ROOT', 'INVERSE_SQUARE', 'SHARP', 'LINEAR', 'CONSTANT'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].object = self.inputs["Hook Object"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].falloff_radius = self.inputs["Radius"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].strength = self.inputs["Strength"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].falloff_type = self.inputs["Falloff Type"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_falloff_uniform = self.inputs["Uniform Faloff"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group