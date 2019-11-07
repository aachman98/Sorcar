import bpy
import math

from bpy.props import IntProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import print_log

class ScCustomPythonScript(Node, ScNode):
    bl_idname = "ScCustomPythonScript"
    bl_label = "Custom Python Script"

    in_script: StringProperty(default="print('Hello')", update=ScNode.update_value)
    in_iteration: IntProperty(default=1, min=1, soft_max=50, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketString", "Script").init("in_script", True)
        self.inputs.new("ScNodeSocketNumber", "Repeat").init("in_iteration")
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def error_condition(self):
        return (
            int(self.inputs["Repeat"].default_value) < 1
        )
    
    def pre_execute(self):
        print_log(self.name, None, None, self.inputs["Script"].default_value)
    
    def functionality(self):
        for i in range(0, int(self.inputs["Repeat"].default_value)):
            exec(self.inputs["Script"].default_value)

    def post_execute(self):
        return {"Out": self.inputs["In"].default_value}