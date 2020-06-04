import bpy
import bmesh
from math import sqrt
from mathutils import Vector

from bpy.props import FloatVectorProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScFindNearest(Node, ScObjectOperatorNode):
    bl_idname = "ScFindNearest"
    bl_label = "Find Nearest"
    
    in_origin: FloatVectorProperty(update=ScNode.update_value)
    in_distance: FloatProperty(default=100.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Origin").init("in_origin", True)
        self.inputs.new("ScNodeSocketNumber", "Distance").init("in_distance")
        self.outputs.new("ScNodeSocketVector", "Location")
        self.outputs.new("ScNodeSocketVector", "Normal")
        self.outputs.new("ScNodeSocketNumber", "Face Index")
        self.outputs.new("ScNodeSocketNumber", "Distance")
        self.outputs.new("ScNodeSocketVector", "Vertex Position")
        self.outputs.new("ScNodeSocketNumber", "Vertex Index")
    
    def error_condition(self):
        return(
            super().error_condition()
            or self.inputs["Distance"].default_value < 0.0
        )

    def post_execute(self):
        out = super().post_execute()
        ret = self.inputs["Object"].default_value.closest_point_on_mesh(self.inputs["Origin"].default_value, distance=self.inputs["Distance"].default_value)
        out["Location"] = ret[1]
        out["Normal"] = ret[2]
        out["Face Index"] = ret[3]
        out["Distance"] = self.measure_distance(self.inputs["Origin"].default_value, out["Location"])
        current_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(self.inputs["Object"].default_value.data)
        bm.faces.ensure_lookup_table()
        face = bm.faces[out["Face Index"]]
        closest_vertex = Vector((0,0,0))
        closest_index = -1
        closest_distance = 10 ** 10
        for v in face.verts:
            dist = self.measure_distance(v.co, out["Location"])
            if (dist < closest_distance):
                closest_vertex = Vector(v.co)
                closest_index = v.index
                closest_distance = dist
        bpy.ops.object.mode_set(mode=current_mode)
        out["Vertex Position"] = closest_vertex
        out["Vertex Index"] = closest_index
        return out
    
    def measure_distance(self, first, second):
        locx = second[0] - first[0]
        locy = second[1] - first[1]
        locz = second[2] - first[2]
        return sqrt((locx)**2 + (locy)**2 + (locz)**2)
