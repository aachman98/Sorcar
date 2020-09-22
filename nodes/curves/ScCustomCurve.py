import bpy

from bpy.props import PointerProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import remove_object, focus_on_object
from ...helper import sc_poll_curve_font

class ScCustomCurve(Node, ScNode):
    bl_idname = "ScCustomCurve"
    bl_label = "Custom Curve"
    bl_icon = 'EYEDROPPER'

    in_obj: PointerProperty(type=bpy.types.Object, poll=sc_poll_curve_font, update=ScNode.update_value)
    in_hide: BoolProperty(default=True, update=ScNode.update_value)
    out_curve: PointerProperty(type=bpy.types.Object, poll=sc_poll_curve_font)
    
    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketCurve", "Curve").init("in_obj", True)
        self.inputs.new("ScNodeSocketBool", "Hide Original").init("in_hide")
        self.outputs.new("ScNodeSocketCurve", "Curve")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Curve"].default_value == None
        )
    
    def pre_execute(self):
        super().pre_execute()
        self.inputs["Curve"].default_value.hide_set(False)
        focus_on_object(self.inputs["Curve"].default_value)
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.duplicate()
    
    def post_execute(self):
        out = super().post_execute()
        self.out_curve = bpy.context.active_object
        if (self.inputs["Hide Original"].default_value):
            self.inputs["Curve"].default_value.hide_set(True)
        out["Curve"] = self.out_curve
        self.id_data.register_object(self.out_curve)
        return out
    
    def free(self):
        super().free()
        self.id_data.unregister_object(self.out_curve)
        if (self.inputs["Curve"].default_value):
            self.inputs["Curve"].default_value.hide_set(False)