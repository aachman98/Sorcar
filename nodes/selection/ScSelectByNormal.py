import bpy

from bpy.props import EnumProperty, FloatVectorProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectByNormal(Node, ScSelectionNode):
    bl_idname = "ScSelectByNormal"
    bl_label = "Select by Normal"
    
    in_min: FloatVectorProperty(default=(-1.0, -1.0, -1.0), min=-1.0, max=1.0, update=ScNode.update_value)
    in_max: FloatVectorProperty(default=(1.0, 1.0, 1.0), min=-1.0, max=1.0, update=ScNode.update_value)
    in_extend: BoolProperty(update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Minimum").init("in_min", True)
        self.inputs.new("ScNodeSocketVector", "Maximum").init("in_max", True)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")
    
    def error_condition(self):
        return(
            super().error_condition()
            or (self.inputs["Minimum"].default_value[0] < -1 or self.inputs["Minimum"].default_value[1] < -1 or self.inputs["Minimum"].default_value[2] < -1)
            or (self.inputs["Minimum"].default_value[0] > 1 or self.inputs["Minimum"].default_value[1] > 1 or self.inputs["Minimum"].default_value[2] > 1)
            or (self.inputs["Maximum"].default_value[0] < -1 or self.inputs["Maximum"].default_value[1] < -1 or self.inputs["Maximum"].default_value[2] < -1)
            or (self.inputs["Maximum"].default_value[0] > 1 or self.inputs["Maximum"].default_value[1] > 1 or self.inputs["Maximum"].default_value[2] > 1)
        )
    
    def functionality(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        if (not (self.inputs["Deselect"].default_value or self.inputs["Extend"].default_value)):
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.mode_set(mode="OBJECT")

        if (bpy.context.tool_settings.mesh_select_mode[0]):
            for vertex in self.inputs["Object"].default_value.data.vertices:
                if (((vertex.normal[0]>=self.inputs["Minimum"].default_value[0] and vertex.normal[1]>=self.inputs["Minimum"].default_value[1] and vertex.normal[2]>=self.inputs["Minimum"].default_value[2]) and (vertex.normal[0]<=self.inputs["Maximum"].default_value[0] and vertex.normal[1]<=self.inputs["Maximum"].default_value[1] and vertex.normal[2]<=self.inputs["Maximum"].default_value[2]))):
                    vertex.select = not self.inputs["Deselect"].default_value
        if (bpy.context.tool_settings.mesh_select_mode[1]):
            for edge in self.inputs["Object"].default_value.data.edges:
                normal = (self.inputs["Object"].default_value.data.vertices[edge.vertices[0]].normal + self.inputs["Object"].default_value.data.vertices[edge.vertices[1]].normal)/2
                if (((normal[0]>=self.inputs["Minimum"].default_value[0] and normal[1]>=self.inputs["Minimum"].default_value[1] and normal[2]>=self.inputs["Minimum"].default_value[2]) and (normal[0]<=self.inputs["Maximum"].default_value[0] and normal[1]<=self.inputs["Maximum"].default_value[1] and normal[2]<=self.inputs["Maximum"].default_value[2]))):
                    edge.select = not self.inputs["Deselect"].default_value
        if (bpy.context.tool_settings.mesh_select_mode[2]):
            for face in self.inputs["Object"].default_value.data.polygons:
                if (((face.normal[0]>=self.inputs["Minimum"].default_value[0] and face.normal[1]>=self.inputs["Minimum"].default_value[1] and face.normal[2]>=self.inputs["Minimum"].default_value[2]) and (face.normal[0]<=self.inputs["Maximum"].default_value[0] and face.normal[1]<=self.inputs["Maximum"].default_value[1] and face.normal[2]<=self.inputs["Maximum"].default_value[2]))):
                    face.select = not self.inputs["Deselect"].default_value
        bpy.ops.object.mode_set(mode="EDIT")