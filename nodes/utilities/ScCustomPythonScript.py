import bpy
import math

from bpy.props import IntProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...debug import log

class ScCustomPythonScript(Node, ScNode):
    bl_idname = "ScCustomPythonScript"
    bl_label = "Custom Python Script"
    bl_icon = 'FILE_SCRIPT'

    in_script: StringProperty(default="print('Hello World')", update=ScNode.update_value)
    in_iteration: IntProperty(default=1, min=1, soft_max=50, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketString", "Script").init("in_script", True)
        self.inputs.new("ScNodeSocketNumber", "Repeat").init("in_iteration")
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def error_condition(self):
        return (
            super().error_condition()
            or int(self.inputs["Repeat"].default_value) < 1
        )
    
    def pre_execute(self):
        log(self.id_data.name, self.name, "pre_execute", "Script:\n"+self.inputs["Script"].default_value, 2)
    
    def functionality(self):
        super().functionality()
        _C = bpy.context
        _D = bpy.data
        _O = bpy.ops
        _S = _C.scene
        _N = self
        _NT = self.id_data
        if not hasattr(_NT, "variables"):
            _NT.variables = {}
        _VAR = _NT.variables
        _IN = self.inputs["In"].default_value
        for i in range(0, int(self.inputs["Repeat"].default_value)):
            exec(self.inputs["Script"].default_value)

    def post_execute(self):
        out = super().post_execute()
        out["Out"] = self.inputs["In"].default_value
        return out