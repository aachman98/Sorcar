import bpy

from bpy.props import StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScSetName(Node, ScObjectOperatorNode):
    bl_idname = "ScSetName"
    bl_label = "Set Name"
    
    in_name: StringProperty(default="Object", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Name").init("in_name", True)
    
    def error_condition(self):
        return(
            super().error_condition()
            or self.inputs["Name"].default_value == ""
        )
    
    def functionality(self):
        self.inputs["Object"].default_value.name = self.inputs["Name"].default_value
        if (self.inputs["Object"].default_value.data):
            self.inputs["Object"].default_value.data.name = self.inputs["Name"].default_value