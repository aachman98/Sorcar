import bpy
import mathutils

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBool(Node, ScNode):
    bl_idname = "ScBool"
    bl_label = "Bool"
    bl_icon = 'CON_ACTION'

    prop_bool: BoolProperty(name="Bool", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.outputs.new("ScNodeSocketBool", "Value")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_bool")
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = self.prop_bool
        return out