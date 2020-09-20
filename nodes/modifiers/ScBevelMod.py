import bpy

from bpy.props import FloatProperty, IntProperty, EnumProperty, BoolProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode

class ScBevelMod(Node, ScModifierNode):
    bl_idname = "ScBevelMod"
    bl_label = "Bevel Modifier"
    bl_icon = 'MOD_BEVEL'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    in_width: FloatProperty(name="Width", default=0.1, min=0.0, update=ScNode.update_value)
    in_segments: IntProperty(name="Segments", default=1, min=0, max=100, update=ScNode.update_value)
    in_profile: FloatProperty(name="Profile", default=0.5, min=0.0, max=1.0, update=ScNode.update_value)
    in_material: IntProperty(name="Material", default=-1, min=0, max=32767, update=ScNode.update_value)
    in_use_only_vertices: BoolProperty(name="Only Vertices", update=ScNode.update_value)
    in_use_clamp_overlap: BoolProperty(name="Clamp Overlap", default=True, update=ScNode.update_value)
    in_loop_slide: BoolProperty(name="Loop Slide", default=True, update=ScNode.update_value)
    in_mark_seam: BoolProperty(name="Mark Seams", update=ScNode.update_value)
    in_mark_sharp: BoolProperty(name="Mark Sharp", update=ScNode.update_value)
    in_harden_normals: BoolProperty(name="Harden Normals", update=ScNode.update_value)
    in_limit_method: EnumProperty(name="Limit Method", items=[("NONE", "None", ""), ("ANGLE", "Angle", ""), ("WEIGHT", "Weight", ""), ("VGROUP", "Vertex Group", "")], default="NONE", update=ScNode.update_value)
    in_angle_limit: FloatProperty(name="Angle", default=0.523599, min=0.0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    in_offset_type: EnumProperty(name="Width Method", items=[("OFFSET", "Offset", ""), ("WIDTH", "Width", ""), ("DEPTH", "Depth", ""), ("PERCENT", "Percent", "")], default="OFFSET", update=ScNode.update_value)
    in_face_strength_mode: EnumProperty(name="Face Strength Mode", items=[("FSTR_NONE", "None", ""), ("FSTR_NEW", "New", ""), ("FSTR_AFFECTED", "Affected", ""), ("FSTR_ALL", "All", "")], default="FSTR_NONE", update=ScNode.update_value)
    in_miter_outer: EnumProperty(name="Outer Miter", items=[("MITER_SHARP", "Sharp", ""), ("MITER_PATCH", "Patch", ""), ("MITER_ARC", "Arc", "")], default="MITER_SHARP", update=ScNode.update_value)
    in_miter_inner: EnumProperty(name="Inner Miter", items=[("MITER_SHARP", "Sharp", ""), ("MITER_PATCH", "Patch", ""), ("MITER_ARC", "Arc", "")], default="MITER_SHARP", update=ScNode.update_value)
    in_spread: FloatProperty(name="Spread", default=0.1, min=0.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "BEVEL"
        self.inputs.new("ScNodeSocketNumber", "Width").init("in_width", True)
        self.inputs.new("ScNodeSocketNumber", "Segments").init("in_segments", True)
        self.inputs.new("ScNodeSocketNumber", "Profile").init("in_profile", True)
        self.inputs.new("ScNodeSocketNumber", "Material").init("in_material")
        self.inputs.new("ScNodeSocketBool", "Only Vertices").init("in_use_only_vertices", True)
        self.inputs.new("ScNodeSocketBool", "Clamp Overlap").init("in_use_clamp_overlap")
        self.inputs.new("ScNodeSocketBool", "Loop Slide").init("in_loop_slide")
        self.inputs.new("ScNodeSocketBool", "Mark Seams").init("in_mark_seam")
        self.inputs.new("ScNodeSocketBool", "Mark Sharp").init("in_mark_sharp")
        self.inputs.new("ScNodeSocketBool", "Harden Normals").init("in_harden_normals")
        self.inputs.new("ScNodeSocketString", "Limit Method").init("in_limit_method")
        self.inputs.new("ScNodeSocketNumber", "Angle").init("in_angle_limit")
        self.inputs.new("ScNodeSocketString", "Width Method").init("in_offset_type")
        self.inputs.new("ScNodeSocketString", "Face Strength Mode").init("in_face_strength_mode")
        self.inputs.new("ScNodeSocketString", "Outer Miter").init("in_miter_outer")
        self.inputs.new("ScNodeSocketString", "Inner Miter").init("in_miter_inner")
        self.inputs.new("ScNodeSocketNumber", "Spread").init("in_spread")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if ((not self.inputs["Object"].default_value == None) and self.inputs["Limit Method"].default_value == "VGROUP"):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Width"].default_value < 0
            or (int(self.inputs["Segments"].default_value) < 0 or int(self.inputs["Segments"].default_value) > 100)
            or (self.inputs["Profile"].default_value < 0 or self.inputs["Profile"].default_value > 1)
            or (int(self.inputs["Material"].default_value) < -1 or int(self.inputs["Material"].default_value) > 32767)
            or (not self.inputs["Limit Method"].default_value in ["NONE", "ANGLE", "WEIGHT", "VGROUP"])
            or (self.inputs["Angle"].default_value < 0 or self.inputs["Angle"].default_value > 3.14159)
            or (not self.inputs["Width Method"].default_value in ["OFFSET", "WIDTH", "DEPTH", "PERCENT"])
            or (not self.inputs["Face Strength Mode"].default_value in ["FSTR_NONE", "FSTR_NEW", "FSTR_AFFECTED", "FSTR_ALL"])
            or (not self.inputs["Outer Miter"].default_value in ["MITER_SHARP", "MITER_PATCH", "MITER_ARC"])
            or (not self.inputs["Inner Miter"].default_value in ["MITER_SHARP", "MITER_PATCH", "MITER_ARC"])
            or self.inputs["Spread"].default_value < 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group
        bpy.context.object.modifiers[self.prop_mod_name].width = self.inputs["Width"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].width_pct = self.inputs["Width"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].segments = int(self.inputs["Segments"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].profile = self.inputs["Profile"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].material = int(self.inputs["Material"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].use_only_vertices = self.inputs["Only Vertices"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_clamp_overlap = self.inputs["Clamp Overlap"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].loop_slide = self.inputs["Loop Slide"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].mark_seam = self.inputs["Mark Seams"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].mark_sharp = self.inputs["Mark Sharp"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].harden_normals = self.inputs["Harden Normals"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].limit_method = self.inputs["Limit Method"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].angle_limit = self.inputs["Angle"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset_type = self.inputs["Width Method"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].face_strength_mode = self.inputs["Face Strength Mode"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].miter_outer = self.inputs["Outer Miter"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].miter_inner = self.inputs["Inner Miter"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].spread = self.inputs["Spread"].default_value