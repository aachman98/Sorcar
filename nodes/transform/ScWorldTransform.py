import bpy

from bpy.props import FloatVectorProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScWorldTransform(Node, ScObjectOperatorNode):
    bl_idname = "ScWorldTransform"
    bl_label = "World Transform"

    in_type: EnumProperty(items=[('LOCATION', 'Location', ''), ('ROTATION', 'Rotation', ''), ('SCALE', 'Scale', '')], update=ScNode.update_value)
    in_val: FloatVectorProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketVector", "Value").init("in_val", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['LOCATION', 'ROTATION', 'SCALE'])
        )
    
    def functionality(self):
        if (self.inputs["Type"].default_value == 'LOCATION'):
            self.inputs["Object"].default_value.location = self.inputs["Value"].default_value
        elif (self.inputs["Type"].default_value == 'ROTATION'):
            self.inputs["Object"].default_value.rotation_euler = self.inputs["Value"].default_value
        elif (self.inputs["Type"].default_value == 'SCALE'):
            self.inputs["Object"].default_value.scale = self.inputs["Value"].default_value