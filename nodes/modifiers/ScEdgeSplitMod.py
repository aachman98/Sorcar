import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScEdgeSplitMod(Node, ScModifierNode):
    bl_idname = "ScEdgeSplitMod"
    bl_label = "Edge Split Modifier"
    bl_icon = 'MOD_EDGESPLIT'
    
    in_split_angle: FloatProperty(default=0.523599, min=0.0, max=3.14159, unit="ROTATION", update=ScNode.update_value)
    in_use_edge_angle: BoolProperty(default=True, update=ScNode.update_value)
    in_use_edge_sharp: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "EDGE_SPLIT"
        self.inputs.new("ScNodeSocketNumber", "Split Angle").init("in_split_angle", True)
        self.inputs.new("ScNodeSocketNumber", "Edge Angle").init("in_use_edge_angle")
        self.inputs.new("ScNodeSocketNumber", "Sharp Edges").init("in_use_edge_sharp")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Split Angle"].default_value < 0 or self.inputs["Split Angle"].default_value > 3.14159)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].split_angle = self.inputs["Split Angle"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_edge_angle = self.inputs["Edge Angle"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_edge_sharp = self.inputs["Sharp Edges"].default_value