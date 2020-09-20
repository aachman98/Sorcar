import bpy

from bpy.props import EnumProperty, PointerProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode
from ...helper import focus_on_object
from ...helper import sc_poll_mesh

class ScBooleanMod(Node, ScModifierNode):
    bl_idname = "ScBooleanMod"
    bl_label = "Boolean Modifier"
    bl_icon = 'MOD_BOOLEAN'
    
    in_op: EnumProperty(items=[("DIFFERENCE", "Difference", ""), ("UNION", "Union", ""), ("INTERSECT", "Intersect", "")], default="INTERSECT", update=ScNode.update_value)
    in_obj: PointerProperty(type=bpy.types.Object, poll=sc_poll_mesh, update=ScNode.update_value)
    in_overlap: FloatProperty(default=0.000001, min=0.0, max=1.0, precision=6, update=ScNode.update_value)
    in_draw_mode: EnumProperty(items=[("SOLID", "Solid", ""), ("WIRE", "Wire", ""), ("BOUNDS", "Bounds", "")], default="WIRE", update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "BOOLEAN"
        self.inputs.new("ScNodeSocketString", "Operation").init("in_op", True)
        self.inputs.new("ScNodeSocketObject", "Boolean Object").init("in_obj", True)
        self.inputs.new("ScNodeSocketNumber", "Overlap Threshold").init("in_overlap")
        self.inputs.new("ScNodeSocketString", "Draw Mode").init("in_draw_mode")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Operation"].default_value in ['DIFFERENCE', 'UNION', 'INTERSECT'])
            or self.inputs["Boolean Object"].default_value == None
            or (self.inputs["Overlap Threshold"].default_value < 0 or self.inputs["Overlap Threshold"].default_value > 1)
            or (not self.inputs["Draw Mode"].default_value in ['SOLID', 'WIRE', 'BOUNDS'])
        )
    
    def functionality(self):
        bpy.context.object.modifiers[self.prop_mod_name].operation = self.inputs["Operation"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].object = self.inputs["Boolean Object"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].double_threshold = self.inputs["Overlap Threshold"].default_value
        self.inputs["Boolean Object"].default_value.display_type = self.inputs["Draw Mode"].default_value