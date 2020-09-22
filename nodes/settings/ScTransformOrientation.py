import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_setting import ScSettingNode

class ScTransformOrientation(Node, ScSettingNode):
    bl_idname = "ScTransformOrientation"
    bl_label = "Transform Orientation"
    bl_icon = 'ORIENTATION_GLOBAL'

    in_orientation: EnumProperty(items=[("GLOBAL", "Global", ""), ("LOCAL", "Local", ""), ("NORMAL", "Normal", ""), ("GIMBAL", "Gimbal", ""), ("CURSOR", "Cursor", "")], default="GLOBAL", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Transform Orientation").init("in_orientation", True)
    
    def functionality(self):
        super().functionality()
        bpy.context.scene.transform_orientation_slots[0].type = self.inputs["Transform Orientation"].default_value