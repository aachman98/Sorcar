import bpy

from bpy.props import FloatProperty, IntProperty, BoolProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScLaplacianSmoothMod(Node, ScModifierNode):
    bl_idname = "ScLaplacianSmoothMod"
    bl_label = "Laplacian Smooth Modifier"
    bl_icon = 'MOD_SMOOTH'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    in_iterations: IntProperty(name="Repeat", default=1, min=-32768, max=32767, soft_min=0, soft_max=200, update=ScNode.update_value)
    in_use_x: BoolProperty(name="X", default=True, update=ScNode.update_value)
    in_use_y: BoolProperty(name="Y", default=True, update=ScNode.update_value)
    in_use_z: BoolProperty(name="Z", default=True, update=ScNode.update_value)
    in_lambda_factor: FloatProperty(default=0.01, soft_min=-1000.0, soft_max=1000.0, update=ScNode.update_value)
    in_lambda_border: FloatProperty(default=0.01, soft_min=-1000.0, soft_max=1000.0, update=ScNode.update_value)
    in_use_volume_preserve: BoolProperty(name="Preserve Volume", default=True, update=ScNode.update_value)
    in_use_normalized: BoolProperty(name="Normalized", default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "LAPLACIANSMOOTH"
        self.inputs.new("ScNodeSocketNumber", "Repeat").init("in_iterations", True)
        self.inputs.new("ScNodeSocketNumber", "X").init("in_use_x")
        self.inputs.new("ScNodeSocketNumber", "Y").init("in_use_y")
        self.inputs.new("ScNodeSocketNumber", "Z").init("in_use_z")
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_lambda_factor", True)
        self.inputs.new("ScNodeSocketNumber", "Border").init("in_lambda_border")
        self.inputs.new("ScNodeSocketNumber", "Preserve Volume").init("in_use_volume_preserve")
        self.inputs.new("ScNodeSocketNumber", "Normalized").init("in_use_normalized")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Repeat"].default_value < -32768 or self.inputs["Repeat"].default_value > 32767)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].iterations = self.inputs["Repeat"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_x = self.inputs["X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_y = self.inputs["Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_z = self.inputs["Z"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].lambda_factor = self.inputs["Factor"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].lambda_border = self.inputs["Border"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_volume_preserve = self.inputs["Preserve Volume"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_normalized = self.inputs["Normalized"].default_value