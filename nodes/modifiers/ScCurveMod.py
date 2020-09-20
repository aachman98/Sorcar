import bpy

from bpy.props import StringProperty, PointerProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_modifier import ScModifierNode
from ...helper import sc_poll_curve

class ScCurveMod(Node, ScModifierNode):
    bl_idname = "ScCurveMod"
    bl_label = "Curve Modifier"
    bl_icon = 'MOD_CURVE'
    
    prop_vertex_group: StringProperty(update=ScNode.update_value)
    in_object: PointerProperty(type=bpy.types.Object, poll=sc_poll_curve, update=ScNode.update_value)
    in_deform_axis: EnumProperty(items=[("POS_X", "X", ""), ("POS_Y", "Y", ""), ("POS_Z", "Z", ""), ("NEG_X", "-X", ""), ("NEG_Y", "-Y", ""), ("NEG_Z", "-Z", "")], default="POS_X", update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.prop_mod_type = "CURVE"
        self.inputs.new("ScNodeSocketCurve", "Curve").init("in_object", True)
        self.inputs.new("ScNodeSocketString", "Deformation Axis").init("in_deform_axis", True)
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Object"].default_value == None):
            layout.prop_search(self, "prop_vertex_group", self.inputs["Object"].default_value, "vertex_groups", text="Vertex Group")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Curve"].default_value == None
            or (not self.inputs["Deformation Axis"].default_value in ['POS_X', 'POS_Y', 'POS_Z', 'NEG_X', 'NEG_Y', 'NEG_Z'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.context.object.modifiers[self.prop_mod_name].object = self.inputs["Curve"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].deform_axis = self.inputs["Deformation Axis"].default_value
        bpy.context.object.modifiers[self.prop_mod_name].vertex_group = self.prop_vertex_group