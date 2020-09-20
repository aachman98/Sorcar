import bpy

from bpy.props import EnumProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScSubsurfMod(Node, ScModifierNode):
    bl_idname = "ScSubsurfMod"
    bl_label = "Subdivision Surface Modifier"
    bl_icon = 'MOD_SUBSURF'
    
    in_subdivision_type: EnumProperty(items=[("CATMULL_CLARK", "Catmull-Clark", ""), ("SIMPLE", "Simple", "")], default="CATMULL_CLARK", update=ScNode.update_value)
    in_render_levels: IntProperty(default=2, min=0, max=11, soft_max=6, update=ScNode.update_value)
    in_levels: IntProperty(default=1, min=0, max=11, soft_max=6, update=ScNode.update_value)
    in_quality: IntProperty(default=3, min=1, max=10, soft_max=6, update=ScNode.update_value)
    in_uv_smooth: EnumProperty(name="Options", items=[("NONE", "Sharp", ""), ("PRESERVE_CORNERS", "Smooth, keep corners", "")], default="PRESERVE_CORNERS", update=ScNode.update_value)
    in_show_only_control_edges: BoolProperty(name="Optimal Display", update=ScNode.update_value)
    in_use_creases: BoolProperty(name="Use Creases", default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "SUBSURF"
        self.inputs.new("ScNodeSocketString", "Type").init("in_subdivision_type", True)
        self.inputs.new("ScNodeSocketNumber", "Render").init("in_render_levels")
        self.inputs.new("ScNodeSocketNumber", "Viewport").init("in_levels", True)
        self.inputs.new("ScNodeSocketNumber", "Quality").init("in_quality")
        self.inputs.new("ScNodeSocketString", "Options").init("in_uv_smooth")
        self.inputs.new("ScNodeSocketBool", "Optimal Display").init("in_show_only_control_edges")
        self.inputs.new("ScNodeSocketBool", "Use Creases").init("in_use_creases")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ["CATMULL_CLARK", "SIMPLE"])
            or (int(self.inputs["Render"].default_value) < 0 or int(self.inputs["Render"].default_value) > 11)
            or (int(self.inputs["Viewport"].default_value) <= 0 or int(self.inputs["Viewport"].default_value) > 11)
            or (int(self.inputs["Quality"].default_value) < 1 or int(self.inputs["Quality"].default_value) > 10)
            or (not self.inputs["Options"].default_value in ["NONE", "PRESERVE_CORNERS"])
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].subdivision_type = self.inputs["Type"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].render_levels = self.inputs["Render"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].levels = self.inputs["Viewport"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].quality = self.inputs["Quality"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].uv_smooth = self.inputs["Options"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].show_only_control_edges = self.inputs["Optimal Display"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_creases = self.inputs["Use Creases"].default_value