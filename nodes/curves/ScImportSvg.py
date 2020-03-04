import bpy
import os

from bpy.props import StringProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import remove_object

class ScImportSvg(Node, ScNode):
    bl_idname = "ScImportSvg"
    bl_label = "Import SVG"

    prop_collection: PointerProperty(type=bpy.types.Collection)
    in_name: StringProperty(default="Object", update=ScNode.update_value)
    in_filepath: StringProperty(default="/path/to/dir/")
    in_filename: StringProperty(default="untitled")
    out_curve: PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Name").init("in_name")
        self.outputs.new("ScNodeSocketCurve", "Curve")
        self.inputs.new("ScNodeSocketString", "File Path").init("in_filepath", True)
        self.inputs.new("ScNodeSocketString", "File Name").init("in_filename", True)
    
    def error_condition(self):
        return (
            self.inputs["Name"].default_value == ""
            or self.inputs["File Path"].default_value == ""
            or self.inputs["File Name"].default_value == ""
        )
    
    def pre_execute(self):
        if (self.out_curve):
            remove_object(self.out_curve)
        if (self.prop_collection):
            bpy.data.collections.remove(self.prop_collection)
    
    def functionality(self):
        bpy.ops.import_curve.svg(
            filepath = os.path.join(self.inputs["File Path"].default_value, self.inputs["File Name"].default_value + ".svg")
        )
    
    def post_execute(self):
        out = {}
        self.prop_collection = bpy.data.collections.get(self.inputs["File Name"].default_value+".svg")
        bpy.context.view_layer.objects.active = self.prop_collection.objects[0]
        self.out_curve = bpy.context.active_object
        self.out_curve.select_set(True)
        self.out_curve.name = self.inputs["Name"].default_value
        if (self.out_curve.data):
            self.out_curve.data.name = self.out_curve.name
        out["Curve"] = self.out_curve
        return out