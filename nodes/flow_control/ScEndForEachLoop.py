import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...debug import log

class ScEndForEachLoop(Node, ScNode):
    bl_idname = "ScEndForEachLoop"
    bl_label = "End For-Each Loop"
    bl_icon = 'TRACKING_BACKWARDS'

    in_iterations: IntProperty(default=5, min=1, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketInfo", "Begin For-Each Loop")
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketArray", "Array")
        self.outputs.new("ScNodeSocketUniversal", "Out")
    
    def init_in(self, forced):
        log(self.id_data.name, self.name, "init_in", "Forced="+str(forced), 3)
        if (self.inputs["Begin For-Each Loop"].is_linked):
            if (self.inputs["Begin For-Each Loop"].links[0].from_node.execute(forced)):
                if (self.inputs["Array"].execute(forced)):
                    return True
                else:
                    log(self.id_data.name, self.name, "init_in", "Execution failed for input \"Array\"", 3)
            else:
                log(self.id_data.name, self.name, "init_in", "Execution failed for node \"Begin For-Each Loop\"", 3)
        else:
            log(self.id_data.name, self.name, "init_in", "Info input \"Begin For-Each Loop\" not linked", 3)
        return False
    
    def error_condition(self):
        return (
            super().error_condition()
            or len(eval(self.inputs["Array"].default_value)) == 0
        )
    
    def functionality(self):
        super().functionality()
        for i in eval(self.inputs["Array"].default_value):
            log(self.id_data.name, self.name, "functionality", "Index="+str(self.inputs["Begin For-Each Loop"].links[0].from_node.out_index+1)+", Element="+repr(i), 3)
            self.inputs["Begin For-Each Loop"].links[0].from_node.out_index += 1
            self.inputs["Begin For-Each Loop"].links[0].from_node.out_element = repr(i)
            self.inputs["In"].execute(True)
        self.inputs["Begin For-Each Loop"].links[0].from_node.prop_locked = False
    
    def post_execute(self):
        out = super().post_execute()
        out["Out"] = self.inputs["In"].default_value
        return out