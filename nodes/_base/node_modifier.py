import bpy

from bpy.props import StringProperty
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScModifierNode(ScNode):
    prop_mod_type: StringProperty()
    prop_mod_name: StringProperty()

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            self.inputs["Object"].default_value == None
        )
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value)
        bpy.ops.object.modifier_add(type=self.prop_mod_type)
        self.prop_mod_name = bpy.context.object.modifiers[-1].name
    
    def post_execute(self):
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=self.prop_mod_name)
        return {"Object": self.inputs["Object"].default_value}