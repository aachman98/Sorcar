import bpy
from mathutils import Vector

from bpy.props import EnumProperty, FloatVectorProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScClosestPointOnMesh(Node, ScNode):
    bl_idname = "ScClosestPointOnMesh"
    bl_label = "Closest Point on Mesh"

    in_x: FloatVectorProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Vector").init("in_x", True)
        self.outputs.new("ScNodeSocketVector", "Value")
    
    def error_condition(self):
        return False

    def post_execute(self):
        out = {}
        idx = bpy.context.object.closest_point_on_mesh(self.inputs["Vector"].default_value)
        out["Value"] = idx[1]
        return out
