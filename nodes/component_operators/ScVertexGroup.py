import bpy

from bpy.props import StringProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScVertexGroup(Node, ScEditOperatorNode):
    bl_idname = "ScVertexGroup"
    bl_label = "Vertex Group"
    
    in_vg: StringProperty(default="Group", update=ScNode.update_value)
    in_assign: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Name").init("in_vg", True)
        self.inputs.new("ScNodeSocketBool", "Assign").init("in_assign")
    
    def error_condition(self):
        return(
            super().error_condition()
            or self.inputs["Name"].default_value == ""
        )
    
    def pre_execute(self):
        super().pre_execute()
        name = self.inputs["Name"].default_value
        slot = self.inputs["Object"].default_value.vertex_groups.find(name)
        if (slot == -1):
            bpy.ops.object.vertex_group_add()
            self.inputs["Object"].default_value.vertex_groups.active.name = name
        else:
            self.inputs["Object"].default_value.vertex_groups.active_index = slot
    
    def functionality(self):
        if (self.inputs["Assign"].default_value):
            bpy.ops.object.vertex_group_assign()
        else:
            bpy.ops.object.vertex_group_remove_from()