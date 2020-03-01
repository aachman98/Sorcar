import bpy

from bpy.props import BoolProperty, FloatProperty, IntProperty, StringProperty, PointerProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScShrinkwrapMod(Node, ScModifierNode):
    bl_idname = "ScShrinkwrapMod"
    bl_label = "Shrinkwrap Modifier"
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    prop_invert_vertex_group: BoolProperty(update=ScNode.update_value)
    in_target: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_offset: FloatProperty(update=ScNode.update_value)
    in_mode: EnumProperty(name="Mode", items=[('NEAREST_SURFACEPOINT', 'Nearest Surface Point', ''), ('PROJECT', 'Project', ''), ('NEAREST_VERTEX', 'Nearest Vertex', ''), ('TARGET_PROJECT', 'Target Normal Project', '')], update=ScNode.update_value)
    in_snap_mode: EnumProperty(name="Snap Mode", items=[('ON_SURFACE', 'On Surface', ''), ('INSIDE', 'Inside', ''), ('OUTSIDE', 'Outside', ''), ('OUTSIDE_SURFACE', 'Outside Surface', ''), ('ABOVE_SURFACE', 'Above Surface', '')], update=ScNode.update_value)
    in_subsurf: IntProperty(min=0, max=6, update=ScNode.update_value)
    in_limit: FloatProperty(min=0.0, update=ScNode.update_value)
    in_x: BoolProperty(update=ScNode.update_value)
    in_y: BoolProperty(update=ScNode.update_value)
    in_z: BoolProperty(update=ScNode.update_value)
    in_neg: BoolProperty(update=ScNode.update_value)
    in_pos: BoolProperty(default=True, update=ScNode.update_value)
    in_inv: BoolProperty(update=ScNode.update_value)
    in_cull: EnumProperty(name="Cull Faces", items=[('OFF', 'Off', ''), ('FRONT', 'Front', ''), ('BACK', 'Back', '')], update=ScNode.update_value)
    in_aux_target: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "SHRINKWRAP"
        self.inputs.new("ScNodeSocketObject", "Target").init("in_target", True)
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketString", "Mode").init("in_mode", True)
        self.inputs.new("ScNodeSocketString", "Snap Mode").init("in_snap_mode", True)
        self.inputs.new("ScNodeSocketNumber", "Subsurf Levels").init("in_subsurf")
        self.inputs.new("ScNodeSocketNumber", "Limit").init("in_limit")
        self.inputs.new("ScNodeSocketBool", "X").init("in_x")
        self.inputs.new("ScNodeSocketBool", "Y").init("in_y")
        self.inputs.new("ScNodeSocketBool", "Z").init("in_z")
        self.inputs.new("ScNodeSocketBool", "Negative").init("in_neg")
        self.inputs.new("ScNodeSocketBool", "Positive").init("in_pos")
        self.inputs.new("ScNodeSocketBool", "Invert Cull").init("in_inv")
        self.inputs.new("ScNodeSocketString", "Cull Faces").init("in_cull")
        self.inputs.new("ScNodeSocketObject", "Auxiliary Target").init("in_aux_target")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            row = layout.row(align=True)
            row.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
            row.prop(self, "prop_invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Target"].default_value == None
            or (not self.inputs["Mode"].default_value in ['NEAREST_SURFACEPOINT', 'PROJECT', 'NEAREST_VERTEX', 'TARGET_PROJECT'])
            or (not self.inputs["Snap Mode"].default_value in ['ON_SURFACE', 'INSIDE', 'OUTSIDE', 'OUTSIDE_SURFACE', 'ABOVE_SURFACE'])
            or (int(self.inputs["Subsurf Levels"].default_value) < 0 or int(self.inputs["Subsurf Levels"].default_value) > 6)
            or self.inputs["Limit"].default_value < 0.0
            or (not self.inputs["Cull Faces"].default_value in ['OFF', 'FRONT', 'BACK'])
        )
    
    def functionality(self):
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].invert_vertex_group = self.prop_invert_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].target = self.inputs["Target"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset = self.inputs["Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].wrap_method = self.inputs["Mode"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].wrap_mode = self.inputs["Snap Mode"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].subsurf_levels = int(self.inputs["Subsurf Levels"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].project_limit = self.inputs["Limit"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_project_x = self.inputs["X"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_project_y = self.inputs["Y"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_project_z = self.inputs["Z"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_negative_direction = self.inputs["Negative"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_positive_direction = self.inputs["Positive"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_invert_cull = self.inputs["Invert Cull"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].cull_face = self.inputs["Cull Faces"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].auxiliary_target = self.inputs["Auxiliary Target"].default_value