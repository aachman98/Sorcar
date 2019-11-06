import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScBranch(Node, ScNode):
    bl_idname = "ScBranch"
    bl_label = "Branch (If-Else)"

    in_condition: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "True")
        self.inputs.new("ScNodeSocketUniversal", "False")
        self.inputs.new("ScNodeSocketBool", "Condition").init("in_condition", True)
        self.outputs.new("ScNodeSocketUniversal", "Value")
    
    def init_in(self, forced):
        if (self.inputs["Condition"].execute(forced)):
            if (self.inputs["Condition"].default_value):
                return self.inputs["True"].execute(forced)
            else:
                return self.inputs["False"].execute(forced)
        return False
    
    def post_execute(self):
        if (self.inputs["Condition"].default_value):
            return {"Value": self.inputs["True"].default_value}
        else:
            return {"Value": self.inputs["False"].default_value}