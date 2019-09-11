import bpy

from bpy.props import EnumProperty, FloatProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScNumber(Node, ScNode):
    bl_idname = "ScNumber"
    bl_label = "Number"

    prop_type: EnumProperty(name="Type", items=[("FLOAT", "Float", ""), ("INT", "Integer", ""), ("ANGLE", "Angle", "")], default="FLOAT", update=ScNode.update_value)
    prop_float: FloatProperty(name="Float", update=ScNode.update_value)
    prop_int: IntProperty(name="Integer", update=ScNode.update_value)
    prop_angle: FloatProperty(name="Angle", unit="ROTATION", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_type", expand=True)
        if (self.prop_type == "FLOAT"):
            layout.prop(self, "prop_float")
        elif (self.prop_type == "INT"):
            layout.prop(self, "prop_int")
        elif (self.prop_type == "ANGLE"):
            layout.prop(self, "prop_angle")
    
    def post_execute(self):
        out = {}
        if (self.prop_type == "FLOAT"):
            out["Value"] = self.prop_float
        elif (self.prop_type == "INT"):
            out["Value"] = self.prop_int
        elif (self.prop_type == "ANGLE"):
            out["Value"] = self.prop_angle
        return out