import bpy

from bpy.props import BoolProperty, FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectByLocation(Node, ScSelectionNode):
    bl_idname = "ScSelectByLocation"
    bl_label = "Select by Location"
    
    in_min: FloatVectorProperty(default=(-1.0, -1.0, -1.0), update=ScNode.update_value)
    in_max: FloatVectorProperty(default=(1.0, 1.0, 1.0), update=ScNode.update_value)
    in_extend: BoolProperty(update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Minimum").init("in_min", True)
        self.inputs.new("ScNodeSocketVector", "Maximum").init("in_max", True)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")

    def functionality(self):
        super().functionality()
        bpy.ops.object.mode_set(mode="OBJECT")
        if (not (self.inputs["Deselect"].default_value or self.inputs["Extend"].default_value)):
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.mode_set(mode="OBJECT")
        if (bpy.context.tool_settings.mesh_select_mode[0]):
            for vertex in self.inputs["Object"].default_value.data.vertices:
                if (((vertex.co[0]>=self.inputs["Minimum"].default_value[0] and vertex.co[1]>=self.inputs["Minimum"].default_value[1] and vertex.co[2]>=self.inputs["Minimum"].default_value[2]) and (vertex.co[0]<=self.inputs["Maximum"].default_value[0] and vertex.co[1]<=self.inputs["Maximum"].default_value[1] and vertex.co[2]<=self.inputs["Maximum"].default_value[2]))):
                    vertex.select = not self.inputs["Deselect"].default_value
        if (bpy.context.tool_settings.mesh_select_mode[1]):
            for edge in self.inputs["Object"].default_value.data.edges:
                co = (self.inputs["Object"].default_value.data.vertices[edge.vertices[0]].co + self.inputs["Object"].default_value.data.vertices[edge.vertices[1]].co)/2
                if (((co[0]>=self.inputs["Minimum"].default_value[0] and co[1]>=self.inputs["Minimum"].default_value[1] and co[2]>=self.inputs["Minimum"].default_value[2]) and (co[0]<=self.inputs["Maximum"].default_value[0] and co[1]<=self.inputs["Maximum"].default_value[1] and co[2]<=self.inputs["Maximum"].default_value[2]))):
                    edge.select = not self.inputs["Deselect"].default_value
        if (bpy.context.tool_settings.mesh_select_mode[2]):
            for face in self.inputs["Object"].default_value.data.polygons:
                if (((face.center[0]>=self.inputs["Minimum"].default_value[0] and face.center[1]>=self.inputs["Minimum"].default_value[1] and face.center[2]>=self.inputs["Minimum"].default_value[2]) and (face.center[0]<=self.inputs["Maximum"].default_value[0] and face.center[1]<=self.inputs["Maximum"].default_value[1] and face.center[2]<=self.inputs["Maximum"].default_value[2]))):
                    face.select = not self.inputs["Deselect"].default_value
        bpy.ops.object.mode_set(mode="EDIT")