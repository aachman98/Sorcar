import bpy

from bpy.props import FloatProperty, PointerProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScLatticeMod(Node, ScModifierNode):
    bl_idname = "ScLatticeMod"
    bl_label = "Lattice Modifier"
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    in_strength: FloatProperty(default=1.0, soft_min=0.0, soft_max=1.0, update=ScNode.update_value)
    in_lattice: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "LATTICE"
        self.inputs.new("ScNodeSocketObject", "Lattice").init("in_lattice", True)
        self.inputs.new("ScNodeSocketNumber", "Strength").init("in_strength")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Lattice"].default_value == None
        )
    
    def functionality(self):
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].object = self.inputs["Lattice"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].strength = self.inputs["Strength"].default_value