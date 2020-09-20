import bpy

from bpy.props import PointerProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_input import ScInputNode
from ...helper import focus_on_object, remove_object, sc_poll_mesh, apply_all_modifiers

class ScCustomObject(Node, ScInputNode):
    bl_idname = "ScCustomObject"
    bl_label = "Custom Object"
    bl_icon = 'EYEDROPPER'

    in_obj: PointerProperty(type=bpy.types.Object, poll=sc_poll_mesh, update=ScNode.update_value)
    in_hide: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object").init("in_obj", True)
        self.inputs.new("ScNodeSocketBool", "Hide Original").init("in_hide")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Object"].default_value == None
        )
    
    def pre_execute(self):
        super().pre_execute()
        self.inputs["Object"].default_value.hide_set(False)
        focus_on_object(self.inputs["Object"].default_value)
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.duplicate()
    
    def post_execute(self):
        out = super().post_execute()
        apply_all_modifiers(self.out_mesh)
        self.inputs["Object"].default_value.hide_set(self.inputs["Hide Original"].default_value)
        return out
    
    def free(self):
        super().free()
        if (self.inputs["Object"].default_value):
            self.inputs["Object"].default_value.hide_set(False)