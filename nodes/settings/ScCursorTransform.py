import bpy

from bpy.props import FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_setting import ScSettingNode

class ScCursorTransform(Node, ScSettingNode):
    bl_idname = "ScCursorTransform"
    bl_label = "Cursor Transform"
    bl_icon = 'CURSOR'

    in_location: FloatVectorProperty(update=ScNode.update_value)
    in_rotation: FloatVectorProperty(unit="ROTATION", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Location").init("in_location", True)
        self.inputs.new("ScNodeSocketVector", "Rotation").init("in_rotation")
    
    def functionality(self):
        super().functionality()
        bpy.context.scene.cursor.location = self.inputs["Location"].default_value
        bpy.context.scene.cursor.rotation_euler = self.inputs["Rotation"].default_value