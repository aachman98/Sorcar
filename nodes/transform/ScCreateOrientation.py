import bpy

from bpy.props import StringProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_transform import ScTransformNode
from ...helper import get_override

class ScCreateOrientation(Node, ScTransformNode):
    bl_idname = "ScCreateOrientation"
    bl_label = "Create Orientation"

    in_name: StringProperty(default="My Orientation", update=ScNode.update_value)
    in_use: BoolProperty(default=True, update=ScNode.update_value)
    in_overwrite: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Name").init("in_name", True)
        self.inputs.new("ScNodeSocketBool", "Use").init("in_use")
        self.inputs.new("ScNodeSocketBool", "Overwrite").init("in_overwrite")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Name"].default_value == None or self.inputs["Name"].default_value == "")
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.transform.create_orientation(
            get_override(self.inputs["Object"].default_value, self.inputs["Edit Mode"].default_value),
            name = self.inputs["Name"].default_value,
            use = self.inputs["Use"].default_value,
            overwrite = self.inputs["Overwrite"].default_value
        )