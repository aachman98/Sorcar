import bpy

from bpy.props import PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import remove_object

class ScCustomObject(Node, ScObjectOperatorNode):
    bl_idname = "ScCustomObject"
    bl_label = "Custom Object"

    in_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    
    def init(self, context):
        self.node_executable = True
        self.use_custom_color = True
        self.set_color()
        self.inputs.new("ScNodeSocketObject", "Object").init("in_obj", True)
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def pre_execute(self):
        remove_object(self.outputs["Object"].default_value)
        super().pre_execute()
    
    def functionality(self):
        bpy.ops.object.duplicate()
    
    def post_execute(self):
        out = super().post_execute()
        out["Object"] = bpy.context.active_object
        return out