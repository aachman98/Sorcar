import bpy
import mathutils

from bpy.props import PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScOverlap(Node, ScObjectOperatorNode):
    bl_idname = "ScOverlap"
    bl_label = "Overlap"
    bl_icon = 'SELECT_INTERSECT'

    in_object: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Secondary Object").init("in_object", True)
        self.outputs.new("ScNodeSocketArray", "Primary Indices")
        self.outputs.new("ScNodeSocketArray", "Secondary Indices")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Secondary Object"].default_value == None
        )
    
    def post_execute(self):
        out = super().post_execute()
        ret = mathutils.bvhtree.BVHTree().FromObject(self.inputs["Object"].default_value, bpy.context.evaluated_depsgraph_get()).overlap(mathutils.bvhtree.BVHTree().FromObject(self.inputs["Secondary Object"].default_value, bpy.context.evaluated_depsgraph_get()))
        out["Primary Indices"] = repr([i[0] for i in ret])
        out["Secondary Indices"] = repr([i[1] for i in ret])
        return out