import bpy

from bpy.props import FloatProperty, StringProperty, EnumProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScDecimateMod(Node, ScModifierNode):
    bl_idname = "ScDecimateMod"
    bl_label = "Decimate Modifier"
    bl_icon = 'MOD_DECIM'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    prop_invert_vertex_group: BoolProperty(update=ScNode.update_value)
    prop_delimit: EnumProperty(items=[("NORMAL", "Normal", "", 2), ("MATERIAL", "Material", "", 4), ("SEAM", "Seam", "", 8), ("SHARP", "Sharp", "", 16), ("UV", "UVs", "", 32)], default={"NORMAL"}, options={'ENUM_FLAG'}, update=ScNode.update_value)
    in_decimate_type: EnumProperty(items=[("COLLAPSE", "Collapse", ""), ("UNSUBDIV", "Un-Subdivide", ""), ("DISSOLVE", "Planar", "")], default="COLLAPSE", update=ScNode.update_value)
    in_ratio: FloatProperty(default=1.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_iterations: IntProperty(default=0, min=0, max=32767, soft_max=100, update=ScNode.update_value)
    in_use_collapse_triangulate: BoolProperty(update=ScNode.update_value)
    in_use_symmetry: BoolProperty(update=ScNode.update_value)
    in_use_dissolve_boundaries: BoolProperty(update=ScNode.update_value)
    in_symmetry_axis: EnumProperty(items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X", update=ScNode.update_value)
    in_angle_limit: FloatProperty(default=0.087266, min=0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    in_vertex_group_factor: FloatProperty(default=1.0, min=0, max=1000, soft_max=10, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "DECIMATE"
        self.inputs.new("ScNodeSocketString", "Type").init("in_decimate_type", True)
        self.inputs.new("ScNodeSocketNumber", "Ratio").init("in_ratio", True)
        self.inputs.new("ScNodeSocketNumber", "Iterations").init("in_iterations", True)
        self.inputs.new("ScNodeSocketBool", "Triangulate").init("in_use_collapse_triangulate")
        self.inputs.new("ScNodeSocketBool", "Symmetry").init("in_use_symmetry")
        self.inputs.new("ScNodeSocketBool", "All Boundaries").init("in_use_dissolve_boundaries")
        self.inputs.new("ScNodeSocketString", "Symmetry Axis").init("in_symmetry_axis")
        self.inputs.new("ScNodeSocketNumber", "Angle Limit").init("in_angle_limit")
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_vertex_group_factor")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_delimit", expand=True)
        if (not self.inputs["Object"].default_value == None):
            row = layout.row(align=True)
            row.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
            row.prop(self, "prop_invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['COLLAPSE', 'UNSUBDIV', 'DISSOLVE'])
            or (self.inputs["Ratio"].default_value < 0 or self.inputs["Ratio"].default_value > 1)
            or (int(self.inputs["Iterations"].default_value) < 0 or int(self.inputs["Iterations"].default_value) > 32767)
            or (not self.inputs["Symmetry Axis"].default_value in ['X', 'Y', 'Z'])
            or (self.inputs["Angle Limit"].default_value < 0 or self.inputs["Angle Limit"].default_value > 3.14159)
            or (self.inputs["Factor"].default_value < 0 or self.inputs["Factor"].default_value > 1000)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].decimate_type = self.inputs["Type"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].ratio = self.inputs["Ratio"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].invert_vertex_group = self.prop_invert_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group_factor = self.inputs["Factor"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_collapse_triangulate = self.inputs["Triangulate"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_symmetry = self.inputs["Symmetry"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].symmetry_axis = self.inputs["Symmetry Axis"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].iterations = int(self.inputs["Iterations"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].angle_limit = self.inputs["Angle Limit"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_dissolve_boundaries = self.inputs["All Boundaries"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].delimit = self.prop_delimit