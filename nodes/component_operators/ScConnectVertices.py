import bpy

from bpy.props import FloatProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScConnectVertices(Node, ScEditOperatorNode):
    bl_idname = "ScConnectVertices"
    bl_label = "Connect Vertices"
    
    in_type: EnumProperty(items=[('SIMPLE', 'Simple', ''), ('CONCAVE', 'Concave', ''), ('NONPLANAR', 'Non-Planar', '')], default='SIMPLE', update=ScNode.update_value)
    in_angle_limit: FloatProperty(default=0.0872665, min=0.0, max=3.14159, unit="ROTATION", update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketNumber", "Angle Limit").init("in_angle_limit")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['SIMPLE', 'CONCAVE', 'NONPLANAR'])
            or (self.inputs["Angle Limit"].default_value < 0.0 or self.inputs["Angle Limit"].default_value > 3.14159)
        )
    
    def functionality(self):
        super().functionality()
        if (self.inputs["Type"].default_value == 'SIMPLE'):
            bpy.ops.mesh.vert_connect()
        elif (self.inputs["Type"].default_value == 'CONCAVE'):
            bpy.ops.mesh.vert_connect_concave()
        else:
            bpy.ops.mesh.vert_connect_nonplanar(
                angle_limit = self.inputs["Angle Limit"].default_value
            )