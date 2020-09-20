import bpy

from bpy.props import FloatProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_input import ScInputNode

class ScEmpty(Node, ScInputNode):
    bl_idname = "ScEmpty"
    bl_label = "Empty"
    bl_icon = 'EMPTY_AXIS'
    
    in_type: EnumProperty(items=[('PLAIN_AXES', 'Plain Axes', ''), ('ARROWS', 'Arrows', ''), ('SINGLE_ARROW', 'Single Arrow', ''), ('CIRCLE', 'Circle', ''), ('CUBE', 'Cube', ''), ('SPHERE', 'Sphere', ''), ('CONE', 'Cone', ''), ('IMAGE', 'Image', '')], default='PLAIN_AXES', update=ScNode.update_value)
    in_radius: FloatProperty(default=1.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketNumber", "Radius").init("in_radius")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['PLAIN_AXES', 'ARROWS', 'SINGLE_ARROW', 'CIRCLE', 'CUBE', 'SPHERE', 'CONE', 'IMAGE'])
            or self.inputs["Radius"].default_value <= 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.empty_add(
            type = self.inputs["Type"].default_value,
            radius = self.inputs["Radius"].default_value
        )