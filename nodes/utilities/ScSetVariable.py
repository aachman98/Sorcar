import bpy

from bpy.props import PointerProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScSetVariable(Node, ScNode):
    bl_idname = "ScSetVariable"
    bl_label = "Set Variable"
    bl_icon = 'PMARKER_ACT'

    prop_nodetree: PointerProperty(name="NodeTree", type=bpy.types.NodeTree, update=ScNode.update_value)
    in_name: StringProperty(default="Var", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketString", "Name").init("in_name", True)
        self.inputs.new("ScNodeSocketUniversal", "Value")
        self.outputs.new("ScNodeSocketUniversal", "Out")
        self.outputs.new("ScNodeSocketUniversal", "Value")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_nodetree")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.prop_nodetree == None
            or self.inputs["Name"].default_value == ""
        )
    
    def pre_execute(self):
        super().pre_execute()
        if not hasattr(self.prop_nodetree, "variables"):
            self.prop_nodetree.variables = {}
    
    def functionality(self):
        super().functionality()
        self.prop_nodetree.variables[self.inputs["Name"].default_value] = self.inputs["Value"].default_value
    
    def post_execute(self):
        out = super().post_execute()
        out["Out"] = self.inputs["In"].default_value
        out["Value"] = self.inputs["Value"].default_value
        return out