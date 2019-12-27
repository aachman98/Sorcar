import bpy

from bpy.props import PointerProperty, EnumProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScMaterialParameter(Node, ScNode):
    bl_idname = "ScMaterialParameter"
    bl_label = "Material Parameter"

    prop_mat: PointerProperty(name="Material", type=bpy.types.Material, update=ScNode.update_value)
    in_node: StringProperty(default="RGB", update=ScNode.update_value)
    in_type: EnumProperty(items=[('INPUT', 'Input', ''), ('OUTPUT', 'Output', '')], default='OUTPUT', update=ScNode.update_value)
    in_parameter: StringProperty(default="Color", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketString", "Node").init("in_node", True)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketString", "Parameter").init("in_parameter", True)
        self.inputs.new("ScNodeSocketUniversal", "Value")
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_mat")
    
    def error_condition(self):
        return (
            self.prop_mat == None
            or self.inputs["Node"].default_value == ""
            or self.inputs["Type"].default_value == ""
            or self.inputs["Parameter"].default_value == ""
        )
    
    def functionality(self):
        nodes = self.prop_mat.node_tree.nodes
        node = nodes.get(self.inputs["Node"].default_value)
        if (node):
            if (self.inputs["Type"].default_value == "INPUT"):
                param = node.inputs.get(self.inputs["Parameter"].default_value)
            else:
                param = node.outputs.get(self.inputs["Parameter"].default_value)
            if (param):
                param.default_value = eval(self.inputs["Value"].default_value)
    
    def post_execute(self):
        out = {}
        out["Out"] = self.inputs["In"].default_value
        return out