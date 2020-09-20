import bpy

from bpy.props import FloatProperty, PointerProperty, StringProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScDisplaceMod(Node, ScModifierNode):
    bl_idname = "ScDisplaceMod"
    bl_label = "Displace Modifier"
    bl_icon = 'MOD_DISPLACE'
    
    prop_texture: PointerProperty(type=bpy.types.Texture)
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    prop_uv_layer: StringProperty(update=ScNode.update_value)
    in_direction: EnumProperty(items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""), ("NORMAL", "Normal", ""), ("CUSTOM_NORMAL", "Custom Normal", ""), ("RGB_TO_XYZ", "RGB to XYZ", "")], default="NORMAL", update=ScNode.update_value)
    in_space: EnumProperty(items=[("LOCAL", "Local", ""), ("GLOBAL", "Global", "")], default="LOCAL", update=ScNode.update_value)
    in_texture_coords: EnumProperty(items=[("LOCAL", "Local", ""), ("GLOBAL", "Global", ""), ("OBJECT", "Object", ""), ("UV", "UV", "")], default="LOCAL", update=ScNode.update_value)
    in_texture_coords_object: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_mid_level: FloatProperty(default=0.5, soft_min=0.0, soft_max=1.0, update=ScNode.update_value)
    in_strength: FloatProperty(default=1.0, soft_min=-100.0, soft_max=100.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "DISPLACE"
        self.inputs.new("ScNodeSocketString", "Direction").init("in_direction", True)
        self.inputs.new("ScNodeSocketString", "Space").init("in_space")
        self.inputs.new("ScNodeSocketString", "Texture Coordinates").init("in_texture_coords")
        self.inputs.new("ScNodeSocketObject", "Secondary Object").init("in_texture_coords_object")
        self.inputs.new("ScNodeSocketNumber", "Midlevel").init("in_mid_level")
        self.inputs.new("ScNodeSocketNumber", "Strength").init("in_strength", True)
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_texture", text="")
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
            if (self.inputs["Texture Coordinates"].default_value == 'UV'):
                layout.prop_search(self, "prop_uv_layer", self.mesh.data, "uv_textures", text="")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Direction"].default_value in ['X', 'Y', 'Z', 'NORMAL', 'CUSTOM_NORMAL', 'RGB_TO_XYZ'])
            or (not self.inputs["Space"].default_value in ['LOCAL', 'GLOBAL'])
            or (not self.inputs["Texture Coordinates"].default_value in ['LOCAL', 'GLOBAL', 'OBJECT', 'UV'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].texture = self.prop_texture
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].uv_layer = self.prop_uv_layer
        bpy.context.object.modifiers[self.prop_mod_name].direction = self.inputs["Direction"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].space = self.inputs["Space"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].texture_coords = self.inputs["Texture Coordinates"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].texture_coords_object = self.inputs["Secondary Object"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].mid_level = self.inputs["Midlevel"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].strength = self.inputs["Strength"].default_value