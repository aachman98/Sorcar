import bpy
import os

from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScConvertToMesh(Node, ScNode):
    bl_idname = "ScConvertToMesh"
    bl_label = "Convert To Mesh"

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketCurve", "Curve")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def pre_execute(self):
        focus_on_object(self.inputs["Curve"].default_value)
    
    def functionality(self):
        bpy.ops.object.convert(
            target = "MESH",
            keep_original = True
        )
    
    def post_execute(self):
        return {"Object": bpy.context.active_object}