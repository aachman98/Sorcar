import bpy

from bpy.props import EnumProperty, IntProperty, BoolProperty, FloatProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScCurveOperatorNode

class ScCurveGeometry(Node, ScCurveOperatorNode):
    bl_idname = "ScCurveGeometry"
    bl_label = "Curve Geometry Properties"
    
    in_depth: FloatProperty(soft_min=0.0, update=ScNode.update_value)
    in_offset: FloatProperty(update=ScNode.update_value)
    in_extrude: FloatProperty(min=0.0, update=ScNode.update_value)
    in_resolution: IntProperty(default=4, min=0, max=32, update=ScNode.update_value)
    in_bevel_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_taper_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_bevel_mapping_start: EnumProperty(name="Start Mapping Type", items=[("RESOLUTION", "Resolution", ""), ("SEGMENTS", "Segments", ""), ("SPLINE", "Spline", "")], default="RESOLUTION", update=ScNode.update_value)
    in_bevel_mapping_end: EnumProperty(name="End Mapping Type", items=[("RESOLUTION", "Resolution", ""), ("SEGMENTS", "Segments", ""), ("SPLINE", "Spline", "")], default="RESOLUTION", update=ScNode.update_value)
    in_bevel_start: FloatProperty(min=0.0, max=1.0, update=ScNode.update_value)
    in_bevel_end: FloatProperty(default=1.0, min=0.0, max=1.0, update=ScNode.update_value)
    in_taper: BoolProperty(update=ScNode.update_value)
    in_fill: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset")
        self.inputs.new("ScNodeSocketNumber", "Extrude").init("in_extrude", True)
        self.inputs.new("ScNodeSocketObject", "Taper Object").init("in_taper_obj")
        self.inputs.new("ScNodeSocketBool", "Map Taper").init("in_taper")
        self.inputs.new("ScNodeSocketNumber", "Depth").init("in_depth", True)
        self.inputs.new("ScNodeSocketNumber", "Resolution").init("in_resolution")
        self.inputs.new("ScNodeSocketObject", "Bevel Object").init("in_bevel_obj")
        self.inputs.new("ScNodeSocketBool", "Fill Caps").init("in_fill", True)
        self.inputs.new("ScNodeSocketNumber", "Bevel Start").init("in_bevel_start")
        self.inputs.new("ScNodeSocketNumber", "Bevel End").init("in_bevel_end")
        self.inputs.new("ScNodeSocketString", "Bevel Mapping Start").init("in_bevel_mapping_start")
        self.inputs.new("ScNodeSocketString", "Bevel Mapping End").init("in_bevel_mapping_end")
    
    def error_condition(self):
        return(
            super().error_condition()
            or self.inputs["Extrude"].default_value < 0
            or (int(self.inputs["Resolution"].default_value) < 0 or int(self.inputs["Resolution"].default_value) > 32)
            or (not self.inputs["Bevel Mapping Start"].default_value in ['RESOLUTION', 'SEGMENTS', 'SPLINE'])
            or (not self.inputs["Bevel Mapping End"].default_value in ['RESOLUTION', 'SEGMENTS', 'SPLINE'])
            or (self.inputs["Bevel Start"].default_value < 0.0 or self.inputs["Bevel Start"].default_value > 1.0)
            or (self.inputs["Bevel End"].default_value < 0.0 or self.inputs["Bevel End"].default_value > 1.0)
        )
    
    def functionality(self):
        self.inputs["Curve"].default_value.data.offset = self.inputs["Offset"].default_value
        self.inputs["Curve"].default_value.data.extrude = self.inputs["Extrude"].default_value
        self.inputs["Curve"].default_value.data.taper_object = self.inputs["Taper Object"].default_value
        self.inputs["Curve"].default_value.data.use_map_taper = self.inputs["Map Taper"].default_value
        self.inputs["Curve"].default_value.data.bevel_depth = self.inputs["Depth"].default_value
        self.inputs["Curve"].default_value.data.bevel_resolution = int(self.inputs["Resolution"].default_value)
        self.inputs["Curve"].default_value.data.bevel_object = self.inputs["Bevel Object"].default_value
        self.inputs["Curve"].default_value.data.use_fill_caps = self.inputs["Fill Caps"].default_value
        self.inputs["Curve"].default_value.data.bevel_factor_start = self.inputs["Bevel Start"].default_value
        self.inputs["Curve"].default_value.data.bevel_factor_end = self.inputs["Bevel End"].default_value
        self.inputs["Curve"].default_value.data.bevel_factor_mapping_start = self.inputs["Bevel Mapping Start"].default_value
        self.inputs["Curve"].default_value.data.bevel_factor_mapping_end = self.inputs["Bevel Mapping End"].default_value