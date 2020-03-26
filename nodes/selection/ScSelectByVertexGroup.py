import bpy

from bpy.props import StringProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode
from ...helper import print_log

class ScSelectByVertexGroup(Node, ScSelectionNode):
    bl_idname = "ScSelectByVertexGroup"
    bl_label = "Select by Vertex Group"
    
    prop_vg: StringProperty(name="Vertex Group", update=ScNode.update_value)
    in_extend: BoolProperty(update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vg", self.inputs["Object"].default_value, "vertex_groups")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.prop_vg == ""
            or self.inputs["Object"].default_value.vertex_groups.get(self.prop_vg) == None
        )
    
    def pre_execute(self):
        super().pre_execute()
        if (not self.inputs["Extend"].default_value):
            if (self.inputs["Deselect"].default_value):
                bpy.ops.mesh.select_all(action="SELECT")
            else:
                bpy.ops.mesh.select_all(action="DESELECT")
    
    def functionality(self):
        self.inputs["Object"].default_value.vertex_groups.active_index = self.inputs["Object"].default_value.vertex_groups[self.prop_vg].index
        if (self.inputs["Deselect"].default_value):
            bpy.ops.object.vertex_group_deselect()
        else:
            bpy.ops.object.vertex_group_select()