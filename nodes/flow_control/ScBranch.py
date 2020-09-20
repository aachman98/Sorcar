import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...debug import log

class ScBranch(Node, ScNode):
    bl_idname = "ScBranch"
    bl_label = "Branch (If-Else)"
    bl_icon = 'QUESTION'

    in_condition: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "True")
        self.inputs.new("ScNodeSocketUniversal", "False")
        self.inputs.new("ScNodeSocketBool", "Condition").init("in_condition", True)
        self.outputs.new("ScNodeSocketUniversal", "Value")
    
    def init_in(self, forced):
        log(self.id_data.name, self.name, "init_in", "Forced="+str(forced), 3)
        if (self.inputs["Condition"].execute(forced)):
            log(self.id_data.name, self.name, "init_in", "Condition="+self.inputs["Condition"].default_value, 3)
            if (self.inputs["Condition"].default_value):
                if (self.inputs["True"].execute(forced)):
                    return True
                else:
                    log(self.id_data.name, self.name, "init_in", "Execution failed for input \"True\"", 3)
            else:
                if (self.inputs["False"].execute(forced)):
                    return True
                else:
                    log(self.id_data.name, self.name, "init_in", "Execution failed for input \"False\"", 3)
        else:
            log(self.id_data.name, self.name, "init_in", "Execution failed for input \"Condition\"", 3)
        return False
    
    def execute(self, forced):
        log(self.id_data.name, self.name, "execute", "Condition="+str(self.inputs["Condition"].default_value), 2)
        return super().execute(forced)
    
    def post_execute(self):
        out = super().post_execute()
        if (self.inputs["Condition"].default_value):
            out["Value"] = self.inputs["True"].default_value
        else:
            out["Value"] = self.inputs["False"].default_value
        return out