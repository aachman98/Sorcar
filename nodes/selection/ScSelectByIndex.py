import bpy

from bpy.props import EnumProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectByIndex(Node, ScSelectionNode):
    bl_idname = "ScSelectByIndex"
    bl_label = "Select by Index"
    
    in_index: IntProperty(min=0, update=ScNode.update_value)
    in_extend: BoolProperty(update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Index").init("in_index", True)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")
    
    def error_condition(self):
        return (
            super().error_condition()
            or int(self.inputs["Index"].default_value) < 0
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
        for i in data:
            index = max(0, min(int(self.inputs["Index"].default_value), len(i)-1))
            i[index].select = not self.inputs["Deselect"].default_value
        bpy.ops.object.mode_set(mode="EDIT")