import bpy

from bpy.props import FloatProperty, StringProperty, BoolProperty, PointerProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScSimpleDeformMod(Node, ScModifierNode):
    bl_idname = "ScSimpleDeformMod"
    bl_label = "Simple Deform Modifier"
    bl_icon = 'MOD_SIMPLEDEFORM'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    prop_invert_vertex_group: BoolProperty(update=ScNode.update_value)
    in_deform_method: EnumProperty(items=[("TWIST", "Twist", ""), ("BEND", "Bend", ""), ("TAPER", "Taper", ""), ("STRETCH", "Stretch", "")], default="TWIST", update=ScNode.update_value)
    in_deform_axis: EnumProperty(items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X", update=ScNode.update_value)
    in_origin: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_lock_x: BoolProperty(update=ScNode.update_value)
    in_lock_y: BoolProperty(update=ScNode.update_value)
    in_lock_z: BoolProperty(update=ScNode.update_value)
    in_factor: FloatProperty(default=0.785398, update=ScNode.update_value)
    in_angle: FloatProperty(default=0.785398, unit="ROTATION", update=ScNode.update_value)
    in_lower_limit: FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_upper_limit: FloatProperty(default=1.0, min=0.0, max=1.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "SIMPLE_DEFORM"
        self.inputs.new("ScNodeSocketString", "Deform Method").init("in_deform_method", True)
        self.inputs.new("ScNodeSocketString", "Deform Axis").init("in_deform_axis", True)
        self.inputs.new("ScNodeSocketObject", "Origin").init("in_origin")
        self.inputs.new("ScNodeSocketBool", "Lock X Axis").init("in_lock_x")
        self.inputs.new("ScNodeSocketBool", "Lock Y Axis").init("in_lock_y")
        self.inputs.new("ScNodeSocketBool", "Lock Z Axis").init("in_lock_z")
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_factor", True)
        self.inputs.new("ScNodeSocketNumber", "Angle").init("in_angle", True)
        self.inputs.new("ScNodeSocketNumber", "Lower Limit").init("in_lower_limit")
        self.inputs.new("ScNodeSocketNumber", "Upper Limit").init("in_upper_limit")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            row = layout.row(align=True)
            row.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
            row.prop(self, "prop_invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Deform Method"].default_value in ['TWIST', 'BEND', 'TAPER', 'STRETCH'])
            or (not self.inputs["Deform Axis"].default_value in ['X', 'Y', 'Z'])
            or (self.inputs["Lower Limit"].default_value < 0 or self.inputs["Lower Limit"].default_value > 1)
            or (self.inputs["Upper Limit"].default_value < 0 or self.inputs["Upper Limit"].default_value > 1)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].deform_method = self.inputs["Deform Method"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].deform_axis = self.inputs["Deform Axis"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].origin = self.inputs["Origin"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].lock_x = self.inputs["Lock X Axis"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].lock_y = self.inputs["Lock Y Axis"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].lock_y = self.inputs["Lock Z Axis"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].factor = self.inputs["Factor"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].angle = self.inputs["Angle"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].limits = (self.inputs["Lower Limit"].default_value, self.inputs["Upper Limit"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].invert_vertex_group = self.prop_invert_vertex_group