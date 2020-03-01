import bpy

from bpy.props import BoolProperty, FloatProperty, IntProperty, StringProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScWeightedNormalMod(Node, ScModifierNode):
    bl_idname = "ScWeightedNormalMod"
    bl_label = "Weighted Normal Modifier"
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    prop_invert_vertex_group: BoolProperty(update=ScNode.update_value)
    in_mode: EnumProperty(name="Weighting Mode", items=[('FACE_AREA', 'Face Area', ''), ('CORNER_ANGLE', 'Corner Angle', ''), ('FACE_AREA_WITH_ANGLE', 'Face Area and Angle', '')], update=ScNode.update_value)
    in_weight: IntProperty(default=50, min=1, max=100, update=ScNode.update_value)
    in_threshold: FloatProperty(default=0.01, min=0.0, max=10.0, update=ScNode.update_value)
    in_sharp: BoolProperty(update=ScNode.update_value)
    in_face: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "WEIGHTED_NORMAL"
        self.inputs.new("ScNodeSocketString", "Weighting Mode").init("in_mode", True)
        self.inputs.new("ScNodeSocketNumber", "Weight").init("in_weight", True)
        self.inputs.new("ScNodeSocketNumber", "Threshold").init("in_threshold")
        self.inputs.new("ScNodeSocketBool", "Keep Sharp").init("in_sharp", True)
        self.inputs.new("ScNodeSocketBool", "Face Influence").init("in_face")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            row = layout.row(align=True)
            row.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
            row.prop(self, "prop_invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Weighting Mode"].default_value in ['FACE_AREA', 'CORNER_ANGLE', 'FACE_AREA_WITH_ANGLE'])
            or (int(self.inputs["Weight"].default_value) < 1 or int(self.inputs["Weight"].default_value) > 100)
            or (self.inputs["Threshold"].default_value < 0.0 or self.inputs["Threshold"].default_value > 10.0)
        )
    
    def functionality(self):
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].invert_vertex_group = self.prop_invert_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].mode = self.inputs["Weighting Mode"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].weight = int(self.inputs["Weight"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].thresh = self.inputs["Threshold"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].keep_sharp = self.inputs["Keep Sharp"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].face_influence = self.inputs["Face Influence"].default_value