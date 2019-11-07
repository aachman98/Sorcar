import bpy

from bpy.props import FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import remove_object

class ScDuplicateObject(Node, ScObjectOperatorNode):
    bl_idname = "ScDuplicateObject"
    bl_label = "Duplicate Object"
    
    def init(self, context):
        super().init(context)
        self.outputs.new("ScNodeSocketObject", "Duplicate Object")
    
    def pre_execute(self):
        remove_object(self.outputs["Duplicate Object"].default_value)
        super().pre_execute()
    
    def functionality(self):
        bpy.ops.object.duplicate()
    
    def post_execute(self):
        out = super().post_execute()
        out["Duplicate Object"] = bpy.context.active_object
        return out