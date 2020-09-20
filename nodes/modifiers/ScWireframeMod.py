import bpy

from bpy.props import FloatProperty, StringProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScWireframeMod(Node, ScModifierNode):
    bl_idname = "ScWireframeMod"
    bl_label = "Wireframe Modifier"
    bl_icon = 'MOD_WIREFRAME'

    prop_vertex_group: StringProperty(update=ScNode.update_value)
    prop_invert_vertex_group: BoolProperty(update=ScNode.update_value)
    in_thickness: FloatProperty(default=0.02, update=ScNode.update_value)
    in_thickness_vertex_group: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_use_crease: BoolProperty(update=ScNode.update_value)
    in_crease_weight: FloatProperty(update=ScNode.update_value)
    in_offset: FloatProperty(update=ScNode.update_value)
    in_use_even_offset: BoolProperty(default=True, update=ScNode.update_value)
    in_use_relative_offset: BoolProperty(update=ScNode.update_value)
    in_use_boundary: BoolProperty(update=ScNode.update_value)
    in_use_replace: BoolProperty(default=True, update=ScNode.update_value)
    in_material_offset: IntProperty(default=0, min=-32768, max=32767, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "WIREFRAME"
        self.inputs.new("ScNodeSocketNumber", "Thickness").init("in_thickness", True)
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_thickness_vertex_group")
        self.inputs.new("ScNodeSocketBool", "Crease Edges").init("in_use_crease")
        self.inputs.new("ScNodeSocketNumber", "Crease Weight").init("in_crease_weight")
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketBool", "Even Thickness").init("in_use_even_offset")
        self.inputs.new("ScNodeSocketBool", "Relative Thickness").init("in_use_relative_offset")
        self.inputs.new("ScNodeSocketBool", "Boundary").init("in_use_boundary")
        self.inputs.new("ScNodeSocketBool", "Replace Original").init("in_use_replace", True)
        self.inputs.new("ScNodeSocketNumber", "Material Offset").init("in_material_offset")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            row = layout.row(align=True)
            row.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
            row.prop(self, "prop_invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Factor"].default_value < 0 or self.inputs["Factor"].default_value > 1)
            or (int(self.inputs["Material Offset"].default_value) < -32768 or int(self.inputs["Material Offset"].default_value) > 32767)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].thickness = self.inputs["Thickness"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].invert_vertex_group = self.prop_invert_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].thickness_vertex_group = self.inputs["Factor"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_crease = self.inputs["Crease Edges"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].crease_weight = self.inputs["Crease Weight"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset = self.inputs["Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_even_offset = self.inputs["Even Thickness"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_relative_offset = self.inputs["Relative Thickness"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_boundary = self.inputs["Boundary"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_replace = self.inputs["Replace Original"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].material_offset = int(self.inputs["Material Offset"].default_value)