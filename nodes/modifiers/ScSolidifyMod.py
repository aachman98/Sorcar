import bpy

from bpy.props import FloatProperty, StringProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScSolidifyMod(Node, ScModifierNode):
    bl_idname = "ScSolidifyMod"
    bl_label = "Solidify Modifier"
    bl_icon = 'MOD_SOLIDIFY'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    prop_invert_vertex_group: BoolProperty(update=ScNode.update_value)
    in_thickness: FloatProperty(default=0.01, update=ScNode.update_value)
    in_thickness_clamp: FloatProperty(default=0.0, min=0.0, max=100.0, update=ScNode.update_value)
    in_thickness_vertex_group: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_edge_crease_inner: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_edge_crease_outer: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_edge_crease_rim: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_offset: FloatProperty(default=-1.0, update=ScNode.update_value)
    in_use_flip_normals: BoolProperty(update=ScNode.update_value)
    in_use_even_offset: BoolProperty(update=ScNode.update_value)
    in_use_quality_normals: BoolProperty(update=ScNode.update_value)
    in_use_rim: BoolProperty(default=True, update=ScNode.update_value)
    in_use_rim_only: BoolProperty(update=ScNode.update_value)
    in_material_offset: IntProperty(default=0, min=-32768, max=32767, update=ScNode.update_value)
    in_material_offset_rim: IntProperty(default=0, min=-32768, max=32767, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "SOLIDIFY"
        self.inputs.new("ScNodeSocketNumber", "Thickness").init("in_thickness", True)
        self.inputs.new("ScNodeSocketNumber", "Clamp").init("in_thickness_clamp")
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_thickness_vertex_group")
        self.inputs.new("ScNodeSocketNumber", "Inner").init("in_edge_crease_inner")
        self.inputs.new("ScNodeSocketNumber", "Outer").init("in_edge_crease_outer")
        self.inputs.new("ScNodeSocketNumber", "Rim").init("in_edge_crease_rim")
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketBool", "Flip Normals").init("in_use_flip_normals", True)
        self.inputs.new("ScNodeSocketBool", "Even Thickness").init("in_use_even_offset")
        self.inputs.new("ScNodeSocketBool", "High Quality Normals").init("in_use_quality_normals")
        self.inputs.new("ScNodeSocketBool", "Fill Rim").init("in_use_rim")
        self.inputs.new("ScNodeSocketBool", "Only Rim").init("in_use_rim_only")
        self.inputs.new("ScNodeSocketNumber", "Material Offset").init("in_material_offset")
        self.inputs.new("ScNodeSocketNumber", "Material Offset Rim").init("in_material_offset_rim")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            row = layout.row(align=True)
            row.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
            row.prop(self, "prop_invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Clamp"].default_value < 0 or self.inputs["Clamp"].default_value > 100)
            or (self.inputs["Factor"].default_value < 0 or self.inputs["Factor"].default_value > 1)
            or (self.inputs["Inner"].default_value < 0 or self.inputs["Inner"].default_value > 1)
            or (self.inputs["Outer"].default_value < 0 or self.inputs["Outer"].default_value > 1)
            or (self.inputs["Rim"].default_value < 0 or self.inputs["Rim"].default_value > 1)
            or (int(self.inputs["Material Offset"].default_value) < -32768 or int(self.inputs["Material Offset"].default_value) > 32767)
            or (int(self.inputs["Material Offset Rim"].default_value) < -32768 or int(self.inputs["Material Offset Rim"].default_value) > 32767)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].thickness = self.inputs["Thickness"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].thickness_clamp = self.inputs["Clamp"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].thickness_vertex_group = self.inputs["Factor"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].edge_crease_inner = self.inputs["Inner"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].edge_crease_outer = self.inputs["Outer"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].edge_crease_rim = self.inputs["Rim"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset = self.inputs["Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_flip_normals = self.inputs["Flip Normals"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_even_offset = self.inputs["Even Thickness"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_quality_normals = self.inputs["High Quality Normals"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_rim = self.inputs["Fill Rim"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_rim_only = self.inputs["Only Rim"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].material_offset = int(self.inputs["Material Offset"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].material_offset_rim = int(self.inputs["Material Offset Rim"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].invert_vertex_group = self.prop_invert_vertex_group