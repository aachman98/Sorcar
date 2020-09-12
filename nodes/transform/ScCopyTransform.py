import bpy

from bpy.props import BoolProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScCopyTransform(Node, ScObjectOperatorNode):
    bl_idname = "ScCopyTransform"
    bl_label = "Copy Transform"

    in_location: BoolProperty(default=True, update=ScNode.update_value)
    in_rotation: BoolProperty(default=True, update=ScNode.update_value)
    in_scale: BoolProperty(default=True, update=ScNode.update_value)
    in_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Secondary Object").init("in_obj", True)
        self.inputs.new("ScNodeSocketBool", "Location").init("in_location", True)
        self.inputs.new("ScNodeSocketBool", "Rotation").init("in_rotation", True)
        self.inputs.new("ScNodeSocketBool", "Scale").init("in_scale", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Secondary Object"].default_value == None
        )
    
    def functionality(self):
        super().functionality()
        if self.inputs["Location"].default_value:
            self.inputs["Object"].default_value.location = self.inputs["Secondary Object"].default_value.location
        if self.inputs["Rotation"].default_value:
            self.inputs["Object"].default_value.rotation_euler = self.inputs["Secondary Object"].default_value.rotation_euler
        if self.inputs["Scale"].default_value:
            self.inputs["Object"].default_value.scale = self.inputs["Secondary Object"].default_value.scale