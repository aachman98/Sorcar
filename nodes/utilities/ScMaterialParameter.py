import bpy

from bpy.props import PointerProperty, EnumProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScMaterialParameter(Node, ScNode):
    bl_idname = "ScMaterialParameter"
    bl_label = "Material Parameter"
    bl_icon = 'MATERIAL'

    prop_mat: PointerProperty(name="Material", type=bpy.types.Material, update=ScNode.update_value)
    prop_node: StringProperty(name="Node", update=ScNode.update_value)
    prop_type: EnumProperty(name="Type", items=[('INPUT', 'Input', ''), ('OUTPUT', 'Output', '')], default='OUTPUT', update=ScNode.update_value)
    prop_socket: StringProperty(name="Socket", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketUniversal", "Value")
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_mat")
        if (not self.prop_mat == None):
            layout.prop_search(self, "prop_node", self.prop_mat.node_tree, "nodes")
            if (not self.prop_node == ""):
                layout.prop(self, "prop_type")
                if (self.prop_type == 'INPUT'):
                    layout.prop_search(self, "prop_socket", self.prop_mat.node_tree.nodes[self.prop_node], "inputs")
                else:
                    layout.prop_search(self, "prop_socket", self.prop_mat.node_tree.nodes[self.prop_node], "outputs")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.prop_mat == None
            or self.prop_node == ""
            or (not self.prop_type in ['INPUT', 'OUTPUT'])
            or self.prop_socket == ""
        )
    
    def functionality(self):
        super().functionality()
        if (self.prop_type == "INPUT"):
            self.prop_mat.node_tree.nodes[self.prop_node].inputs[self.prop_socket].default_value = eval(self.inputs["Value"].default_value)
        else:
            self.prop_mat.node_tree.nodes[self.prop_node].outputs[self.prop_socket].default_value = eval(self.inputs["Value"].default_value)
    
    def post_execute(self):
        out = super().post_execute()
        out["Out"] = self.inputs["In"].default_value
        return out