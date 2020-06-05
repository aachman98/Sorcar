import bpy
import bmesh
from math import sqrt
from mathutils import Vector

from bpy.props import FloatVectorProperty, EnumProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScFindNearest(Node, ScObjectOperatorNode):
    bl_idname = "ScFindNearest"
    bl_label = "Find Nearest"
    
    in_component: EnumProperty(items=[("VERTEX", "Vertex", ""), ("FACE", "Face", "")], default="FACE", update=ScNode.update_value)
    in_origin: FloatVectorProperty(update=ScNode.update_value)
    in_distance: FloatProperty(default=100.0, min=0.0, update=ScNode.update_value)
    
    info = {}

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Component").init("in_component", True)
        self.inputs.new("ScNodeSocketVector", "Origin").init("in_origin", True)
        self.inputs.new("ScNodeSocketNumber", "Distance").init("in_distance")
        self.outputs.new("ScNodeSocketVector", "Location")
        self.outputs.new("ScNodeSocketVector", "Normal")
        self.outputs.new("ScNodeSocketNumber", "Index")
        self.outputs.new("ScNodeSocketNumber", "Distance")
    
    def error_condition(self):
        return(
            super().error_condition()
            or self.inputs["Distance"].default_value < 0.0
        )

    def functionality(self):
        obj = self.inputs["Object"].default_value
        comp = self.inputs["Component"].default_value
        origin = self.inputs["Origin"].default_value
        max_dist = self.inputs["Distance"].default_value

        if comp == "VERTEX":            
            current_mode = bpy.context.object.mode
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(obj.data)
            set = bm.verts
            set.ensure_lookup_table()
            self.info["Distance"] = max_dist

            for item in set:
                dist = self.measure_distance(item.co, origin)
                if dist < self.info["Distance"]:
                    self.info["Distance"] = dist
                    self.info["Location"] = Vector(item.co)
                    self.info["Normal"] = Vector(item.normal)
                    self.info["Index"] = item.index
            
            bpy.ops.object.mode_set(mode=current_mode)
                    
        elif comp == "FACE":
            ret = self.inputs["Object"].default_value.closest_point_on_mesh(origin, distance=max_dist)
            self.info["Location"] = ret[1]
            self.info["Normal"] = ret[2]
            self.info["Index"] = ret[3]
            self.info["Distance"] = self.measure_distance(origin, self.info["Location"])

    def post_execute(self):
        out = super().post_execute()
        out["Location"] = self.info["Location"]
        out["Normal"] = self.info["Normal"]
        out["Index"] = self.info["Index"]
        out["Distance"] = self.info["Distance"]
        return out
    
    def measure_distance(self, first, second):
        locx = second[0] - first[0]
        locy = second[1] - first[1]
        locz = second[2] - first[2]
        return sqrt((locx)**2 + (locy)**2 + (locz)**2)
