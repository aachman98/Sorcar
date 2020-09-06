import bpy

from bpy.props import BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScFillGrid(Node, ScEditOperatorNode):
    bl_idname = "ScFillGrid"
    bl_label = "Fill Grid"
    
    in_span: IntProperty(default=1, min=1, max=1000, update=ScNode.update_value)
    in_offset: IntProperty(default=0, min=-1000, max=1000, update=ScNode.update_value)
    in_interp: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Span").init("in_span", True)
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketBool", "Simple Blending").init("in_interp")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (int(self.inputs["Span"].default_value) < 1 or int(self.inputs["Span"].default_value) > 1000)
            or (int(self.inputs["Offset"].default_value) < -1000 or int(self.inputs["Offset"].default_value) > 1000)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.fill_grid(
            span = int(self.inputs["Span"].default_value),
            offset = int(self.inputs["Offset"].default_value),
            use_interp_simple = self.inputs["Simple Blending"].default_value
        )