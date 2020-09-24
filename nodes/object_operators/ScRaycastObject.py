import bpy
import mathutils

from bpy.props import FloatVectorProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScRaycastObject(Node, ScObjectOperatorNode):
    bl_idname = "ScRaycastObject"
    bl_label = "Raycast (Object)"
    bl_icon = 'OUTLINER_DATA_LIGHTPROBE'
    
    in_origin: FloatVectorProperty(update=ScNode.update_value)
    in_direction: FloatVectorProperty(update=ScNode.update_value)
    in_distance: FloatProperty(default=100.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Origin").init("in_origin", True)
        self.inputs.new("ScNodeSocketVector", "Direction").init("in_direction", True)
        self.inputs.new("ScNodeSocketNumber", "Distance").init("in_distance")
        self.outputs.new("ScNodeSocketVector", "Location")
        self.outputs.new("ScNodeSocketVector", "Normal")
        self.outputs.new("ScNodeSocketNumber", "Index")
        self.outputs.new("ScNodeSocketNumber", "Distance")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Distance"].default_value < 0.0
        )
    
    def post_execute(self):
        out = super().post_execute()
        ret = mathutils.bvhtree.BVHTree().FromObject(self.inputs["Object"].default_value, bpy.context.evaluated_depsgraph_get()).ray_cast(self.inputs["Origin"].default_value, self.inputs["Direction"].default_value, self.inputs["Distance"].default_value)
        out["Location"] = ret[0]
        out["Normal"] = ret[1]
        out["Index"] = ret[2]
        out["Distance"] = ret[3]
        return out