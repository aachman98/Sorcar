import bpy

from bpy.types import NodeCustomGroup
from .._base.node_base import ScNode

class ScNodeGroup(ScNode, NodeCustomGroup):
    bl_idname = "ScNodeGroup"
    bl_label = "Node Group"

    def init(self, context):
        self.node_executable = True
        super().init(context)

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (self == self.id_data.nodes.active):
            row = layout.row(align=True)
            row.prop(self, "node_tree", text="")
            row.operator("sc.edit_group", text="", icon='NODETREE', emboss=True)
    
    def error_condition(self):
        return (
            self.node_tree == None
            or self.node_tree.nodes.get('Group Input') == None
            or self.node_tree.nodes.get('Group Output') == None
        )
    
    def pre_execute(self):
        for i in range(0, len(self.inputs)):
            self.node_tree.nodes['Group Input'].outputs[i].default_value = self.inputs[i].default_value
    
    def functionality(self):
        for i in range(0, len(self.outputs)):
            self.node_tree.nodes['Group Output'].inputs[i].execute(True)

    def post_execute(self):
        out = {}
        for i in range(0, len(self.outputs)):
            out[self.outputs[i].name] = self.node_tree.nodes['Group Output'].inputs[i].default_value
        return out