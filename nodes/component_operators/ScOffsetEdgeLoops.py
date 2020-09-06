import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import get_override

class ScOffsetEdgeLoops(Node, ScEditOperatorNode):
    bl_idname = "ScOffsetEdgeLoops"
    bl_label = "Offset Edge Loops"
    
    in_factor: FloatProperty(default=0.523187, min=-1.0, max=1.0, update=ScNode.update_value)
    in_cap: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_factor", True)
        self.inputs.new("ScNodeSocketBool", "Cap Endpoint").init("in_cap")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Factor"].default_value < -1.0 or self.inputs["Factor"].default_value > 1.0)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.offset_edge_loops_slide(
            get_override(self.inputs["Object"].default_value, True),
            MESH_OT_offset_edge_loops = {
                "use_cap_endpoint": self.inputs["Cap Endpoint"].default_value
            },
            TRANSFORM_OT_edge_slide = {
                "value": self.inputs["Factor"].default_value
            }
        )