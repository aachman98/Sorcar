import bpy

from bpy.props import FloatProperty, EnumProperty, IntProperty, PointerProperty, BoolProperty, FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode
from ...helper import sc_poll_curve, sc_poll_mesh

class ScArrayMod(Node, ScModifierNode):
    bl_idname = "ScArrayMod"
    bl_label = "Array Modifier"
    bl_icon = 'MOD_ARRAY'
    
    in_fit_type: EnumProperty(items=[("FIXED_COUNT", "Fixed Count", ""), ("FIT_LENGTH", "Fit Length", ""), ("FIT_CURVE", "Fit Curve", "")], default="FIXED_COUNT", update=ScNode.update_value)
    in_count: IntProperty(default=2, min=1, max=1000, update=ScNode.update_value)
    in_fit_length: FloatProperty(default=0.0, min=0.0, update=ScNode.update_value)
    in_curve: PointerProperty(type=bpy.types.Object, poll=sc_poll_curve, update=ScNode.update_value)
    in_use_constant_offset: BoolProperty(update=ScNode.update_value)
    in_constant_offset_displace: FloatVectorProperty(update=ScNode.update_value)
    in_use_merge_vertices: BoolProperty(name="Merge", update=ScNode.update_value)
    in_use_merge_vertices_cap: BoolProperty(update=ScNode.update_value)
    in_merge_threshold: FloatProperty(default=0.01, min=0.0, max=1.0, update=ScNode.update_value)
    in_use_relative_offset: BoolProperty(default=True, update=ScNode.update_value)
    in_relative_offset_displace: FloatVectorProperty(default=(1.0, 0.0, 0.0), update=ScNode.update_value)
    in_use_object_offset: BoolProperty(update=ScNode.update_value)
    in_offset_object: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_offset_u: FloatProperty(default=0.0, min=-1, max=1, update=ScNode.update_value)
    in_offset_v: FloatProperty(default=0.0, min=-1, max=1, update=ScNode.update_value)
    in_start_cap: PointerProperty(type=bpy.types.Object, poll=sc_poll_mesh, update=ScNode.update_value)
    in_end_cap: PointerProperty(type=bpy.types.Object, poll=sc_poll_mesh, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "ARRAY"
        self.inputs.new("ScNodeSocketString", "Fit Type").init("in_fit_type", True)
        self.inputs.new("ScNodeSocketNumber", "Count").init("in_count", True)
        self.inputs.new("ScNodeSocketNumber", "Length").init("in_fit_length", True)
        self.inputs.new("ScNodeSocketCurve", "Curve").init("in_curve")
        self.inputs.new("ScNodeSocketBool", "Use Constant Offset").init("in_use_constant_offset")
        self.inputs.new("ScNodeSocketVector", "Constant Offset").init("in_constant_offset_displace")
        self.inputs.new("ScNodeSocketBool", "Use Relative Offset").init("in_use_relative_offset")
        self.inputs.new("ScNodeSocketVector", "Relative Offset").init("in_relative_offset_displace", True)
        self.inputs.new("ScNodeSocketBool", "Use Object Offset").init("in_use_object_offset")
        self.inputs.new("ScNodeSocketObject", "Object Offset").init("in_offset_object")
        self.inputs.new("ScNodeSocketBool", "Merge").init("in_use_merge_vertices")
        self.inputs.new("ScNodeSocketBool", "First Last").init("in_use_merge_vertices_cap")
        self.inputs.new("ScNodeSocketNumber", "Distance").init("in_merge_threshold")
        self.inputs.new("ScNodeSocketNumber", "U Offset").init("in_offset_u")
        self.inputs.new("ScNodeSocketNumber", "V Offset").init("in_offset_v")
        self.inputs.new("ScNodeSocketObject", "End Cap").init("in_start_cap")
        self.inputs.new("ScNodeSocketObject", "Start Cap").init("in_end_cap")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Fit Type"].default_value in ["FIXED_COUNT", "FIT_LENGTH", "FIT_CURVE"])
            or (int(self.inputs["Count"].default_value) < 1 or int(self.inputs["Count"].default_value) > 1000)
            or self.inputs["Length"].default_value < 0.0
            or (self.inputs["Distance"].default_value < 0.0 or self.inputs["Distance"].default_value > 1.0)
            or (self.inputs["U Offset"].default_value < -1.0 or self.inputs["U Offset"].default_value > 1.0)
            or (self.inputs["V Offset"].default_value < -1.0 or self.inputs["V Offset"].default_value > 1.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].fit_type = self.inputs["Fit Type"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].count = int(self.inputs["Count"].default_value)
        bpy.context.object.modifiers[self.prop_mod_name].fit_length = self.inputs["Length"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].curve = self.inputs["Curve"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_constant_offset = self.inputs["Use Constant Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].constant_offset_displace = self.inputs["Constant Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_merge_vertices = self.inputs["Merge"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_merge_vertices_cap = self.inputs["First Last"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].merge_threshold = self.inputs["Distance"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_relative_offset = self.inputs["Use Relative Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].relative_offset_displace = self.inputs["Relative Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].use_object_offset = self.inputs["Use Object Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset_object = self.inputs["Object Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset_u = self.inputs["U Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].offset_v = self.inputs["V Offset"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].start_cap = self.inputs["End Cap"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].end_cap = self.inputs["Start Cap"].default_value