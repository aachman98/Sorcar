import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScOrigin(Node, ScObjectOperatorNode):
    bl_idname = "ScOrigin"
    bl_label = "Origin"
    bl_icon = 'OBJECT_ORIGIN'
    
    in_type: EnumProperty(items=[("GEOMETRY_ORIGIN", "Geometry to Origin", ""), ("ORIGIN_GEOMETRY", "Origin to Geometry", ""), ("ORIGIN_CURSOR", "Origin to 3D Cursor", ""), ("ORIGIN_CENTER_OF_MASS", "Origin to Center of Mass (Surface)", ""), ("ORIGIN_CENTER_OF_VOLUME", "Origin to Center of Mass (Volume)", "")], default="GEOMETRY_ORIGIN", update=ScNode.update_value)
    in_center: EnumProperty(items=[("MEDIAN", "Median", ""), ("BOUNDS", "Bounds", "")], default="MEDIAN", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketString", "Center").init("in_center")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['GEOMETRY_ORIGIN', 'ORIGIN_GEOMETRY', 'ORIGIN_CURSOR', 'ORIGIN_CENTER_OF_MASS', 'ORIGIN_CENTER_OF_VOLUME'])
            or (not self.inputs["Center"].default_value in ['MEDIAN', 'BOUNDS'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.origin_set(
            type = self.inputs["Type"].default_value,
            center = self.inputs["Center"].default_value
        )