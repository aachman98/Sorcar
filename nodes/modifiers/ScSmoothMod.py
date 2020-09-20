import bpy

from bpy.props import FloatProperty, IntProperty, BoolProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScSmoothMod(Node, ScModifierNode):
    bl_idname = "ScSmoothMod"
    bl_label = "Smooth Modifier"
    bl_icon = 'MOD_SMOOTH'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    in_factor: FloatProperty(default=0.5, update=ScNode.update_value)
    in_iterations: IntProperty(default=1, min=0, max=32767, soft_max=30, update=ScNode.update_value)
    in_use_x: BoolProperty(default=True, update=ScNode.update_value)
    in_use_y: BoolProperty(default=True, update=ScNode.update_value)
    in_use_z: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "SMOOTH"
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_factor", True)
        self.inputs.new("ScNodeSocketNumber", "Repeat").init("in_iterations", True)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_use_x")
        self.inputs.new("ScNodeSocketNumber", "Y").init("in_use_y")
        self.inputs.new("ScNodeSocketNumber", "Z").init("in_use_z")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Repeat"].default_value < 0 or self.inputs["Repeat"].default_value > 32767)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].factor = self.inputs["Factor"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].iterations = self.inputs["Repeat"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_x = self.inputs["X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_y = self.inputs["Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_z = self.inputs["Z"].default_value