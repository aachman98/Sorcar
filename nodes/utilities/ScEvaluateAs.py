import bpy

from bpy.types import Node
from mathutils import Vector
from .._base.node_base import ScNode
from ...debug import log

class ScEvaluateAs(Node, ScNode):
    bl_idname = "ScEvaluateAs"
    bl_label = "Evaluate As"
    bl_icon = 'CON_TRANSFORM_CACHE'

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "Element")
        self.outputs.new("ScNodeSocketArray", "As Array")
        self.outputs.new("ScNodeSocketBool", "As Bool")
        self.outputs.new("ScNodeSocketCurve", "As Curve")
        self.outputs.new("ScNodeSocketNumber", "As Float")
        self.outputs.new("ScNodeSocketNumber", "As Int")
        self.outputs.new("ScNodeSocketObject", "As Object")
        self.outputs.new("ScNodeSocketString", "As String")
        self.outputs.new("ScNodeSocketVector", "As Vector")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Element"].default_value == None
        )
    
    def post_execute(self):
        out = super().post_execute()
        try:
            out["As Array"] = repr(list(eval(self.inputs["Element"].default_value)))
            log(self.id_data.name, self.name, "post_execute", "Value successfully evaluated as Array", 3)
        except:
            out["As Array"] = "[]"
            log(self.id_data.name, self.name, "post_execute", "Value couldn't be evaluated as Array", 3)
        try:
            out["As Bool"] = bool(eval(self.inputs["Element"].default_value))
            log(self.id_data.name, self.name, "post_execute", "Value successfully evaluated as Bool", 3)
        except:
            out["As Bool"] = False
            log(self.id_data.name, self.name, "post_execute", "Value couldn't be evaluated as Bool", 3)
        try:
            out["As Curve"] = bpy.data.objects.get(eval(self.inputs["Element"].default_value).name)
            log(self.id_data.name, self.name, "post_execute", "Value successfully evaluated as Curve", 3)
        except:
            out["As Curve"] = None
            log(self.id_data.name, self.name, "post_execute", "Value couldn't be evaluated as Curve", 3)
        try:
            out["As Float"] = float(eval(self.inputs["Element"].default_value))
            log(self.id_data.name, self.name, "post_execute", "Value successfully evaluated as Float", 3)
        except:
            out["As Float"] = 0.0
            log(self.id_data.name, self.name, "post_execute", "Value couldn't be evaluated as Float", 3)
        try:
            out["As Int"] = int(eval(self.inputs["Element"].default_value))
            log(self.id_data.name, self.name, "post_execute", "Value successfully evaluated as Int", 3)
        except:
            out["As Int"] = 0
            log(self.id_data.name, self.name, "post_execute", "Value couldn't be evaluated as Int", 3)
        try:
            out["As Object"] = bpy.data.objects.get(eval(self.inputs["Element"].default_value).name)
            log(self.id_data.name, self.name, "post_execute", "Value successfully evaluated as Object", 3)
        except:
            out["As Object"] = None
            log(self.id_data.name, self.name, "post_execute", "Value couldn't be evaluated as Object", 3)
        try:
            out["As String"] = str(eval(self.inputs["Element"].default_value))
            log(self.id_data.name, self.name, "post_execute", "Value successfully evaluated as String", 3)
        except:
            out["As String"] = ""
            log(self.id_data.name, self.name, "post_execute", "Value couldn't be evaluated as String", 3)
        try:
            out["As Vector"] = Vector(eval(self.inputs["Element"].default_value)).to_tuple()
            log(self.id_data.name, self.name, "post_execute", "Value successfully evaluated as Vector", 3)
        except:
            out["As Vector"] = (0, 0, 0)
            log(self.id_data.name, self.name, "post_execute", "Value couldn't be evaluated as Vector", 3)
        return out