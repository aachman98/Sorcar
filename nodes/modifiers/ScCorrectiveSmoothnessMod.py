import bpy

from bpy.props import StringProperty, FloatProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScCorrectiveSmoothnessMod(Node, ScModifierNode):
    bl_idname = "ScCorrectiveSmoothnessMod"
    bl_label = "Corrective Smoothness Modifier"
    bl_icon = 'MOD_SMOOTH'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    prop_invert_vertex_group: BoolProperty(update=ScNode.update_value)
    in_factor: FloatProperty(default=0.5, soft_min=0.0, soft_max=1.0, update=ScNode.update_value)
    in_iterations: IntProperty(default=5, min=-32768, max=32767, soft_min=0, soft_max=200, update=ScNode.update_value)
    in_smooth_type: EnumProperty(items=[("SIMPLE", "Simple", ""), ("LENGTH_WEIGHTED", "Length Weight", "")], default="SIMPLE", update=ScNode.update_value)
    in_use_only_smooth: BoolProperty(update=ScNode.update_value)
    in_use_pin_boundary: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "CORRECTIVE_SMOOTH"
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_factor", True)
        self.inputs.new("ScNodeSocketNumber", "Repeat").init("in_iterations", True)
        self.inputs.new("ScNodeSocketString", "Smooth Type").init("in_smooth_type")
        self.inputs.new("ScNodeSocketBool", "Only Smooth").init("in_use_only_smooth")
        self.inputs.new("ScNodeSocketBool", "Pin Boundaries").init("in_use_pin_boundary")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            row = layout.row(align=True)
            row.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
            row.prop(self, "prop_invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Repeat"].default_value) < -32768 or int(self.inputs["Repeat"].default_value) > 32767)
            or (not self.inputs["Smooth Type"].default_value in ['SIMPLE', 'LENGTH_WEIGHTED'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].factor = self.inputs["Factor"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].iterations = int(self.inputs["Repeat"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].smooth_type = self.inputs["Smooth Type"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_only_smooth = self.inputs["Only Smooth"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_pin_boundary = self.inputs["Pin Boundaries"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].invert_vertex_group = self.prop_invert_vertex_group