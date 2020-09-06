import bpy

from bpy.props import FloatProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import get_override

class ScLoopCut(Node, ScEditOperatorNode):
    bl_idname = "ScLoopCut"
    bl_label = "Loop Cut"
    
    in_cuts: IntProperty(default=1, min=1, soft_max=100, update=ScNode.update_value)
    in_smoothness: FloatProperty(soft_min=-4.0, soft_max=4.0, update=ScNode.update_value)
    in_use_selected_edge: BoolProperty(default=True, update=ScNode.update_value)
    in_index: IntProperty(default=0, min=0, update=ScNode.update_value)
    in_factor: FloatProperty(default=0.0, min=-1.0, max=1.0, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Number of Cuts").init("in_cuts", True)
        self.inputs.new("ScNodeSocketNumber", "Smoothness").init("in_smoothness", True)
        self.inputs.new("ScNodeSocketBool", "Use selected edge").init("in_use_selected_edge", True)
        self.inputs.new("ScNodeSocketNumber", "Edge Index").init("in_index", True)
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_factor", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or int(self.inputs["Number of Cuts"].default_value) < 1
            or int(self.inputs["Edge Index"].default_value) < 0
            or (self.inputs["Factor"].default_value < -1.0 or self.inputs["Factor"].default_value > 1.0)
        )
    
    def functionality(self):
        super().functionality()
        index = int(self.inputs["Edge Index"].default_value)
        if (self.inputs["Use selected edge"].default_value):
            bpy.ops.object.mode_set(mode="OBJECT")
            index = [i.index for i in self.inputs["Object"].default_value.data.edges if i.select][0]
            bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.loopcut_slide(
            get_override(self.inputs["Object"].default_value, True),
            MESH_OT_loopcut = {
                "number_cuts": int(self.inputs["Number of Cuts"].default_value),
                "smoothness": self.inputs["Smoothness"].default_value,
                "object_index": 0,
                "edge_index": index
            },
            TRANSFORM_OT_edge_slide = {
                "value": self.inputs["Factor"].default_value
            }
        )