import bpy
import mathutils

from bpy.props import FloatVectorProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScRaycastScene(Node, ScNode):
    bl_idname = "ScRaycastScene"
    bl_label = "Raycast (Scene)"
    bl_icon = 'OUTLINER_OB_LIGHTPROBE'
    
    in_origin: FloatVectorProperty(update=ScNode.update_value)
    in_direction: FloatVectorProperty(update=ScNode.update_value)
    in_distance: FloatProperty(default=100.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Origin").init("in_origin", True)
        self.inputs.new("ScNodeSocketVector", "Direction").init("in_direction", True)
        self.inputs.new("ScNodeSocketNumber", "Distance").init("in_distance")
        self.outputs.new("ScNodeSocketBool", "Result")
        self.outputs.new("ScNodeSocketVector", "Location")
        self.outputs.new("ScNodeSocketVector", "Normal")
        self.outputs.new("ScNodeSocketNumber", "Index")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Distance"].default_value < 0.0
        )
    
    def post_execute(self):
        out = super().post_execute()
        ret = bpy.context.scene.ray_cast(
            bpy.context.view_layer,
            self.inputs["Origin"].default_value,
            self.inputs["Direction"].default_value,
            distance = self.inputs["Distance"].default_value
        )
        out["Result"] = ret[0]
        out["Location"] = ret[1]
        out["Normal"] = ret[2]
        out["Index"] = ret[3]
        out["Object"] = ret[4]
        return out