import bpy

from bpy.props import PointerProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import remove_object

class ScCustomObject(Node, ScObjectOperatorNode):
    bl_idname = "ScCustomObject"
    bl_label = "Custom Object"

    in_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_hide: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        self.node_executable = True
        self.use_custom_color = True
        self.set_color()
        self.inputs.new("ScNodeSocketObject", "Object").init("in_obj", True)
        self.inputs.new("ScNodeSocketBool", "Hide Original").init("in_hide")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def pre_execute(self):
        remove_object(self.outputs["Object"].default_value)
        self.inputs["Object"].default_value.hide_set(False)
        super().pre_execute()
    
    def functionality(self):
        bpy.ops.object.duplicate()
    
    def post_execute(self):
        if (self.inputs["Hide Original"].default_value):
            self.inputs["Object"].default_value.hide_set(True)
        return {"Object": bpy.context.active_object}