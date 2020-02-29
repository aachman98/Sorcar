import bpy

from bpy.props import FloatProperty, IntProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScWeldMod(Node, ScModifierNode):
    bl_idname = "ScWeldMod"
    bl_label = "Weld Modifier"
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    in_distance: FloatProperty(default=0.001, min=0.0, soft_max=1.0, update=ScNode.update_value)
    in_limit: IntProperty(default=1, min=0, soft_max=10000, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "WELD"
        self.inputs.new("ScNodeSocketNumber", "Distance").init("in_distance", True)
        self.inputs.new("ScNodeSocketNumber", "Duplicate Limit").init("in_limit", True)
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Distance"].default_value < 0.0
            or int(self.inputs["Duplicate Limit"].default_value) < 0
        )
    
    def functionality(self):
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].merge_threshold = self.inputs["Distance"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].max_interactions = int(self.inputs["Duplicate Limit"].default_value)