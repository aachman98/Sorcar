import bpy

from bpy.types import Node
from mathutils import Vector
from .._base.node_base import ScNode

class ScEvaluateAs(Node, ScNode):
    bl_idname = "ScEvaluateAs"
    bl_label = "Evaluate As"

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
        return (self.inputs["Element"].default_value == None)
    
    def post_execute(self):
        out = {}
        try:
            print("debug: Array")
            out["As Array"] = repr(list(eval(self.inputs["Element"].default_value)))
        except:
            out["As Array"] = "[]"
        try:
            print("debug: Bool")
            out["As Bool"] = bool(eval(self.inputs["Element"].default_value))
        except:
            out["As Bool"] = False
        try:
            print("debug: Curve")
            out["As Curve"] = bpy.data.objects.get(eval(self.inputs["Element"].default_value).name)
        except:
            out["As Curve"] = None
        try:
            print("debug: Float")
            out["As Float"] = float(eval(self.inputs["Element"].default_value))
        except:
            out["As Float"] = 0.0
        try:
            print("debug: Int")
            out["As Int"] = int(eval(self.inputs["Element"].default_value))
        except:
            out["As Int"] = 0
        try:
            print("debug: Object")
            out["As Object"] = bpy.data.objects.get(eval(self.inputs["Element"].default_value).name)
        except:
            out["As Object"] = None
        try:
            print("debug: String")
            out["As String"] = str(eval(self.inputs["Element"].default_value))
        except:
            out["As String"] = ""
        try:
            print("debug: Vector")
            out["As Vector"] = Vector(eval(self.inputs["Element"].default_value)).to_tuple()
        except:
            out["As Vector"] = (0, 0, 0)
        return out