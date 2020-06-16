import bpy
import os

from bpy.props import StringProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import remove_object

class ScImportSvg(Node, ScNode):
    bl_idname = "ScImportSvg"
    bl_label = "Import SVG"

    prop_collections: StringProperty(default="[]")
    in_name: StringProperty(default="Object", update=ScNode.update_value)
    in_file: StringProperty(subtype='FILE_PATH', update=ScNode.update_value)
    out_curve: PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Name").init("in_name")
        self.outputs.new("ScNodeSocketCurve", "Curve")
        self.inputs.new("ScNodeSocketString", "File").init("in_file", True)
    
    def error_condition(self):
        return (
            self.inputs["Name"].default_value == ""
            or self.inputs["File"].default_value == ""
        )
    
    def pre_execute(self):
        self.prop_collections = repr(list(bpy.data.collections))
    
    def functionality(self):
        bpy.ops.import_curve.svg(
            filepath = bpy.path.abspath(self.inputs["File"].default_value)
        )
    
    def post_execute(self):
        out = {}
        collection = [c for c in bpy.data.collections if c not in eval(self.prop_collections)][0]
        bpy.context.view_layer.objects.active = collection.objects[0]
        self.out_curve = bpy.context.active_object
        self.id_data.register_object(self.out_curve)
        self.out_curve.select_set(True)
        self.out_curve.name = self.inputs["Name"].default_value
        if (self.out_curve.data):
            self.out_curve.data.name = self.out_curve.name
        bpy.ops.object.move_to_collection(collection_index=0)
        bpy.data.collections.remove(collection)
        out["Curve"] = self.out_curve
        return out
    
    def free(self):
        self.id_data.unregister_object(self.out_curve)