import bpy
import os

from bpy.props import PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScConvertToCurve(Node, ScNode):
    bl_idname = "ScConvertToCurve"
    bl_label = "Convert To Curve"

    prop_mesh: PointerProperty(type=bpy.types.Mesh)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.outputs.new("ScNodeSocketCurve", "Curve")
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value)
        self.prop_mesh = self.inputs["Object"].default_value.data
    
    def functionality(self):
        bpy.ops.object.convert(
            target = "CURVE",
            keep_original = False
        )
    
    def post_execute(self):
        bpy.context.active_object.data.name = bpy.context.active_object.name
        bpy.data.meshes.remove(self.prop_mesh)
        return {"Curve": bpy.context.active_object}