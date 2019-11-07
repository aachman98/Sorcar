import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScEndForLoop(Node, ScNode):
    bl_idname = "ScEndForLoop"
    bl_label = "End For Loop"

    in_start: IntProperty(default=1, update=ScNode.update_value)
    in_finish: IntProperty(default=5, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketInfo", "Begin For Loop")
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketNumber", "Start").init("in_start", True)
        self.inputs.new("ScNodeSocketNumber", "Finish").init("in_finish", True)
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def init_in(self, forced):
        return self.inputs["Start"].execute(forced) and self.inputs["Finish"].execute(forced)
    
    def error_condition(self):
        return (
            (not self.inputs["Begin For Loop"].is_linked)
            or int(self.inputs["Start"].default_value) > int(self.inputs["Finish"].default_value)
        )
    
    def functionality(self):
        for i in range(int(self.inputs["Start"].default_value), int(self.inputs["Finish"].default_value)+1):
            self.inputs["Begin For Loop"].links[0].from_node.out_counter = i
            self.inputs["In"].execute(True)
    
    def post_execute(self):
        self.inputs["Begin For Loop"].links[0].from_node.prop_locked = False
        return {"Out": self.inputs["In"].default_value}