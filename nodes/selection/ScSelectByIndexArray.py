import bpy

from bpy.props import EnumProperty, StringProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectByIndexArray(Node, ScSelectionNode):
    bl_idname = "ScSelectByIndexArray"
    bl_label = "Select by Index Array"
    
    in_index_arr: StringProperty(default="[]", update=ScNode.update_value)
    in_extend: BoolProperty(update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Index Array").init("in_index_arr", True)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")
    
    def error_condition(self):
        return (
            super().error_condition()
            or len(eval(self.inputs["Index Array"].default_value)) < 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.mode_set(mode="OBJECT")
        data = []
        if (bpy.context.tool_settings.mesh_select_mode[0]):
            data.append(self.inputs["Object"].default_value.data.vertices)
        if (bpy.context.tool_settings.mesh_select_mode[1]):
            data.append(self.inputs["Object"].default_value.data.edges)
        if (bpy.context.tool_settings.mesh_select_mode[2]):
            data.append(self.inputs["Object"].default_value.data.polygons)
        if (not (self.inputs["Deselect"].default_value or self.inputs["Extend"].default_value)):
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.mode_set(mode="OBJECT")
        for d in data:
            for i in eval(self.inputs["Index Array"].default_value):
                index = max(0, min(i, len(d)-1))
                d[index].select = not self.inputs["Deselect"].default_value
        bpy.ops.object.mode_set(mode="EDIT")