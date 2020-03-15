import bpy

from bpy.types import Node
from mathutils import Vector
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScObjectInfo(Node, ScNode):
    bl_idname = "ScObjectInfo"
    bl_label = "Object Info"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.outputs.new("ScNodeSocketString", "Name")
        self.outputs.new("ScNodeSocketVector", "Location")
        self.outputs.new("ScNodeSocketVector", "Rotation")
        self.outputs.new("ScNodeSocketVector", "Scale")
        self.outputs.new("ScNodeSocketVector", "Dimensions")
        self.outputs.new("ScNodeSocketArray", "Bounding Box")
        self.outputs.new("ScNodeSocketArray", "Selected Vertices")
        self.outputs.new("ScNodeSocketArray", "Selected Edges")
        self.outputs.new("ScNodeSocketArray", "Selected Faces")
        self.outputs.new("ScNodeSocketArray", "Unselected Vertices")
        self.outputs.new("ScNodeSocketArray", "Unselected Edges")
        self.outputs.new("ScNodeSocketArray", "Unselected Faces")
        self.outputs.new("ScNodeSocketArray", "Total Vertices")
        self.outputs.new("ScNodeSocketArray", "Total Edges")
        self.outputs.new("ScNodeSocketArray", "Total Faces")
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value, True)
        bpy.ops.object.mode_set(mode='OBJECT')
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Object"].default_value == None
        )
    
    def post_execute(self):
        out = {}
        out["Name"] = self.inputs["Object"].default_value.name
        out["Location"] = self.inputs["Object"].default_value.location
        out["Rotation"] = self.inputs["Object"].default_value.rotation_euler
        out["Scale"] = self.inputs["Object"].default_value.scale
        out["Dimensions"] = self.inputs["Object"].default_value.dimensions
        out["Bounding Box"] = repr([Vector(i).to_tuple() for i in self.inputs["Object"].default_value.bound_box])
        out["Selected Vertices"] = str([i.index for i in self.inputs["Object"].default_value.data.vertices if i.select])
        out["Selected Edges"] = str([i.index for i in self.inputs["Object"].default_value.data.edges if i.select])
        out["Selected Faces"] = str([i.index for i in self.inputs["Object"].default_value.data.polygons if i.select])
        out["Unselected Vertices"] = str([i.index for i in self.inputs["Object"].default_value.data.vertices if not i.select])
        out["Unselected Edges"] = str([i.index for i in self.inputs["Object"].default_value.data.edges if not i.select])
        out["Unselected Faces"] = str([i.index for i in self.inputs["Object"].default_value.data.polygons if not i.select])
        out["Total Vertices"] = str([i.index for i in self.inputs["Object"].default_value.data.vertices])
        out["Total Edges"] = str([i.index for i in self.inputs["Object"].default_value.data.edges])
        out["Total Faces"] = str([i.index for i in self.inputs["Object"].default_value.data.polygons])
        return out