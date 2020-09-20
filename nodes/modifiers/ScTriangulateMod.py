import bpy

from bpy.props import EnumProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScTriangulateMod(Node, ScModifierNode):
    bl_idname = "ScTriangulateMod"
    bl_label = "Triangulate Modifier"
    bl_icon = 'MOD_TRIANGULATE'
    
    in_quad_method: EnumProperty(items=[("BEAUTY", "Beauty", ""), ("FIXED", "Fixed", ""), ("FIXED_ALTERNATE", "Fixed Alternate", ""), ("SHORTEST_DIAGONAL", "Shortest Diagonal", "")], default="SHORTEST_DIAGONAL", update=ScNode.update_value)
    in_ngon_method: EnumProperty(items=[("BEAUTY", "Beauty", ""), ("CLIP", "Clip", "")], default="BEAUTY", update=ScNode.update_value)
    in_keep_custom_normals: BoolProperty(update=ScNode.update_value)
    in_min_vertices: IntProperty(default=4, min=4, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "TRIANGULATE"
        self.inputs.new("ScNodeSocketString", "Quad Method").init("in_quad_method", True)
        self.inputs.new("ScNodeSocketString", "Ngon Method").init("in_ngon_method", True)
        self.inputs.new("ScNodeSocketBool", "Keep Normals").init("in_keep_custom_normals")
        self.inputs.new("ScNodeSocketNumber", "Minimum Vertices").init("in_min_vertices")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Quad Method"].default_value in ['BEAUTY', 'FIXED', 'FIXED_ALTERNATE', 'SHORTEST_DIAGONAL'])
            or (not self.inputs["Ngon Method"].default_value in ['BEAUTY', 'CLIP'])
            or int(self.inputs["Minimum Vertices"].default_value) < 4
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].quad_method = self.inputs["Quad Method"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].ngon_method = self.inputs["Ngon Method"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].keep_custom_normals = self.inputs["Keep Normals"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].min_vertices = int(self.inputs["Minimum Vertices"].default_value)