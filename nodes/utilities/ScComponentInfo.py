import bpy

from mathutils import Vector
from bpy.props import EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScComponentInfo(Node, ScNode):
    bl_idname = "ScComponentInfo"
    bl_label = "Component Info"

    in_component: EnumProperty(name="Component", items=[("FACE", "Face", ""), ("VERT", "Vertex", ""), ("EDGE", "Edge", "")], default="FACE", update=ScNode.update_value)
    in_average: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.inputs.new("ScNodeSocketString", "Component").init("in_component", True)
        self.inputs.new("ScNodeSocketBool", "Average").init("in_average")
        self.outputs.new("ScNodeSocketVector", "Location")
        self.outputs.new("ScNodeSocketVector", "Normal")
        self.outputs.new("ScNodeSocketNumber", "Area (Only Faces)")
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value)
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Object"].default_value == None
            or (not self.inputs["Component"].default_value in ['FACE', 'VERT', 'EDGE'])
        )
    
    def post_execute(self):
        out = {}
        if (self.inputs["Component"].default_value == 'FACE'):
            loc = [i.center for i in self.inputs["Object"].default_value.data.polygons if i.select]
            rot = [i.normal for i in self.inputs["Object"].default_value.data.polygons if i.select]
            area = [i.area for i in self.inputs["Object"].default_value.data.polygons if i.select]
        elif (self.inputs["Component"].default_value == 'VERT'):
            loc = [i.co for i in self.inputs["Object"].default_value.data.vertices if i.select]
            rot = [i.normal for i in self.inputs["Object"].default_value.data.vertices if i.select]
            area = [0 for i in self.inputs["Object"].default_value.data.vertices if i.select]
        elif (self.inputs["Component"].default_value == 'EDGE'):
            loc = [(Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[0]].co) + Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[1]].co))/2 for i in self.inputs["Object"].default_value.data.edges if i.select]
            rot = [(Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[0]].normal) + Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[1]].normal))/2 for i in self.inputs["Object"].default_value.data.edges if i.select]
            area = [0 for i in self.inputs["Object"].default_value.data.edges if i.select]
        l = Vector((0, 0, 0))
        r = Vector((0, 0, 0))
        a = 0
        if (self.inputs["Average"].default_value):
            for i in range (0, len(loc)):
                l += loc[i]/len(loc)
                r += rot[i]/len(rot)
                a += area[i]/len(area)
            out["Location"] = l
            out["Normal"] = r
            out["Area (Only Faces)"] = a
        else:
            if (len(loc) == 0):
                out["Location"] = l
                out["Normal"] = r
                out["Area (Only Faces)"] = a
            else:
                out["Location"] = loc[0]
                out["Normal"] = rot[0]
                out["Area (Only Faces)"] = area[0]
        bpy.ops.object.mode_set(mode="EDIT")
        return out