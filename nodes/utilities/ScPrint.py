import bpy

from bpy.props import StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import print_log

class ScPrint(Node, ScNode):
    bl_idname = "ScPrint"
    bl_label = "Print"

    in_str: StringProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.node_executable = True
        self.inputs.new("ScNodeSocketString", "String").init("in_str", True)
        self.outputs.new("ScNodeSocketString", "Value")
    
    def functionality(self):
        print_log(self.name, msg=self.inputs["String"].default_value)
    
    def post_execute(self):
        return {"Value": self.inputs["String"].default_value}