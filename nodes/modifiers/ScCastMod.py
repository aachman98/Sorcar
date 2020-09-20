import bpy

from bpy.props import EnumProperty, BoolProperty, FloatProperty, StringProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScCastMod(Node, ScModifierNode):
    bl_idname = "ScCastMod"
    bl_label = "Cast Modifier"
    bl_icon = 'MOD_CAST'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    in_cast_type: EnumProperty(items=[("SPHERE", "Sphere", ""), ("CYLINDER", "Cylinder", ""), ("CUBOID", "Cuboid", "")], update=ScNode.update_value)
    in_use_x: BoolProperty(default=True, update=ScNode.update_value)
    in_use_y: BoolProperty(default=True, update=ScNode.update_value)
    in_use_z: BoolProperty(default=True, update=ScNode.update_value)
    in_factor: FloatProperty(default=0.5, update=ScNode.update_value)
    in_radius: FloatProperty(default=0.0, min=0.0, update=ScNode.update_value)
    in_size: FloatProperty(default=0.0, min=0.0, update=ScNode.update_value)
    in_use_radius_as_size: BoolProperty(default=True, update=ScNode.update_value)
    in_control_object: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_use_transform: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "CAST"
        self.inputs.new("ScNodeSocketString", "Cast Type").init("in_cast_type", True)
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_factor", True)
        self.inputs.new("ScNodeSocketNumber", "Radius").init("in_radius", True)
        self.inputs.new("ScNodeSocketNumber", "Size").init("in_size", True)
        self.inputs.new("ScNodeSocketBool", "From Radius").init("in_use_radius_as_size")
        self.inputs.new("ScNodeSocketBool", "X").init("in_use_x")
        self.inputs.new("ScNodeSocketBool", "Y").init("in_use_y")
        self.inputs.new("ScNodeSocketBool", "Z").init("in_use_z")
        self.inputs.new("ScNodeSocketObject", "Control Object").init("in_control_object")
        self.inputs.new("ScNodeSocketBool", "Use Transform").init("in_use_transform")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Cast Type"].default_value in ['SPHERE', 'CYLINDER', 'CUBOID'])
            or self.inputs["Radius"].default_value < 0
            or self.inputs["Size"].default_value < 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].cast_type = self.inputs["Cast Type"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_x = self.inputs["X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_y = self.inputs["Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_z = self.inputs["Z"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].factor = self.inputs["Factor"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].radius = self.inputs["Radius"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].size = self.inputs["Size"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_radius_as_size = self.inputs["From Radius"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].object = self.inputs["Control Object"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_transform = self.inputs["Use Transform"].default_value