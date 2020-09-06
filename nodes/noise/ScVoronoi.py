import bpy
import mathutils

from bpy.props import FloatVectorProperty, FloatProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScVoronoi(Node, ScNode):
    bl_idname = "ScVoronoi"
    bl_label = "Voronoi"

    in_position: FloatVectorProperty(update=ScNode.update_value)
    in_distance_metric: EnumProperty(items=[('DISTANCE', 'Distance', ''), ('DISTANCE_SQUARED', 'Distance Squared', ''), ('MANHATTAN', 'Manhattan', ''), ('CHEBYCHEV', 'Chebychev', ''), ('MINKOVSKY', 'Minkovsky', ''), ('MINKOVSKY_HALF', 'Minkovsky (Half)', ''), ('MINKOVSKY_FOUR', 'Minkovsky (Four)', '')], default='DISTANCE', update=ScNode.update_value)
    in_exponent: FloatProperty(default=2.5, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Position").init("in_position", True)
        self.inputs.new("ScNodeSocketString", "Distance Metric").init("in_distance_metric", True)
        self.inputs.new("ScNodeSocketNumber", "Exponent").init("in_exponent")
        self.outputs.new("ScNodeSocketNumber", "Distance 1")
        self.outputs.new("ScNodeSocketNumber", "Distance 2")
        self.outputs.new("ScNodeSocketNumber", "Distance 3")
        self.outputs.new("ScNodeSocketNumber", "Distance 4")
        self.outputs.new("ScNodeSocketVector", "Location 1")
        self.outputs.new("ScNodeSocketVector", "Location 2")
        self.outputs.new("ScNodeSocketVector", "Location 3")
        self.outputs.new("ScNodeSocketVector", "Location 4")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Distance Metric"].default_value in ['DISTANCE', 'DISTANCE_SQUARED', 'MANHATTAN', 'CHEBYCHEV', 'MINKOVSKY', 'MINKOVSKY_HALF', 'MINKOVSKY_FOUR'])
        )
    
    def post_execute(self):
        out = super().post_execute()
        dist, loc = mathutils.noise.voronoi(
            self.inputs["Position"].default_value,
            distance_metric = self.inputs["Distance Metric"].default_value,
            exponent = self.inputs["Exponent"].default_value
        )
        out["Distance 1"] = dist[0]
        out["Distance 2"] = dist[1]
        out["Distance 3"] = dist[2]
        out["Distance 4"] = dist[3]
        out["Location 1"] = loc[0]
        out["Location 2"] = loc[1]
        out["Location 3"] = loc[2]
        out["Location 4"] = loc[3]
        return out