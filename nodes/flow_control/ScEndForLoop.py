import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...debug import log

class ScEndForLoop(Node, ScNode):
    bl_idname = "ScEndForLoop"
    bl_label = "End For Loop"
    bl_icon = 'TRACKING_REFINE_BACKWARDS'

    in_iterations: IntProperty(default=5, min=1, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketInfo", "Begin For Loop")
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketNumber", "Iterations").init("in_iterations", True)
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def init_in(self, forced): # Should be a behaviour of socket
        log(self.id_data.name, self.name, "init_in", "Forced="+str(forced), 3)
        if (self.inputs["Begin For Loop"].is_linked):
            if (self.inputs["Begin For Loop"].links[0].from_node.execute(forced)):
                if (self.inputs["Iterations"].execute(forced)):
                    return True
                else:
                    log(self.id_data.name, self.name, "init_in", "Execution failed for input \"Iterations\"", 3)
            else:
                log(self.id_data.name, self.name, "init_in", "Execution failed for node \"Begin For Loop\"", 3)
        else:
            log(self.id_data.name, self.name, "init_in", "Info input \"Begin For Loop\" not linked", 3)
        return False
    
    def error_condition(self):
        return (
            super().error_condition()
            or int(self.inputs["Iterations"].default_value) < 1
        )
    
    def functionality(self):
        super().functionality()
        for i in range (0, int(self.inputs["Iterations"].default_value)):
            log(self.id_data.name, self.name, "functionality", "Iteration="+str(i+1), 3)
            self.inputs["Begin For Loop"].links[0].from_node.out_counter += 1
            self.inputs["In"].execute(True)
        self.inputs["Begin For Loop"].links[0].from_node.prop_locked = False
    
    def post_execute(self):
        out = super().post_execute()
        out["Out"] = self.inputs["In"].default_value
        return out