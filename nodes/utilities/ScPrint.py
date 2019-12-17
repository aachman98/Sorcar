import bpy

from bpy.props import StringProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import print_log

class ScPrint(Node, ScNode):
    bl_idname = "ScPrint"
    bl_label = "Print"

    prop_force: BoolProperty(name="Force Re-evaluate", update=ScNode.update_value)
    in_str: StringProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.node_executable = True
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketString", "String").init("in_str", True)
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_force")
    
    def execute(self, forced=False):
        forced = forced or self.prop_force
        return super().execute(forced=forced)
    
    def functionality(self):
        print_log(self.name, msg=self.inputs["String"].default_value)
    
    def post_execute(self):
        return {"Out": self.inputs["In"].default_value}