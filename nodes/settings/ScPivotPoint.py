import bpy

from bpy.props import EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_setting import ScSettingNode

class ScPivotPoint(Node, ScSettingNode):
    bl_idname = "ScPivotPoint"
    bl_label = "Pivot Point"
    bl_icon = 'PIVOT_MEDIAN'

    in_pivot: EnumProperty(items=[("BOUNDING_BOX_CENTER", "Bound Box Center", ""), ("CURSOR", "Cursor", ""), ("INDIVIDUAL_ORIGINS", "Individual Origins", ""), ("MEDIAN_POINT", "Median Point", ""), ("ACTIVE_ELEMENT", "Active Element", "")], default="MEDIAN_POINT", update=ScNode.update_value)
    in_origin: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Pivot Point").init("in_pivot", True)
        self.inputs.new("ScNodeSocketBool", "Only Origins").init("in_origin")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Pivot Point"].default_value in ['BOUNDING_BOX_CENTER', 'CURSOR', 'INDIVIDUAL_ORIGINS', 'MEDIAN_POINT', 'ACTIVE_ELEMENT'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.scene.tool_settings.transform_pivot_point = self.inputs["Pivot Point"].default_value
        bpy.context.scene.tool_settings.use_transform_pivot_point_align = self.inputs["Only Origins"].default_value