import bpy
import os

from bpy.props import PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScConvertToMesh(Node, ScNode):
    bl_idname = "ScConvertToMesh"
    bl_label = "Convert To Mesh"

    prop_curve: PointerProperty(type=bpy.types.Curve)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketCurve", "Curve")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def pre_execute(self):
        focus_on_object(self.inputs["Curve"].default_value)
        self.prop_curve = self.inputs["Curve"].default_value.data
    
    def functionality(self):
        bpy.ops.object.convert(
            target = "MESH",
            keep_original = False
        )
    
    def post_execute(self):
        bpy.context.active_object.data.name = bpy.context.active_object.name
        bpy.data.curves.remove(self.prop_curve)
        return {"Object": bpy.context.active_object}