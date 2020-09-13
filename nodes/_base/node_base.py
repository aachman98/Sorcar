import bpy

from bpy.props import BoolProperty
from ...debug import log

class ScNode:
    node_executable: BoolProperty()
    first_time: BoolProperty()
    node_error: BoolProperty()

    @classmethod
    def poll(cls, _ntree):
        return _ntree.bl_idname == "ScNodeTree"
    
    def update_value(self, context):
        if (hasattr(context.space_data, "edit_tree") and context.space_data.edit_tree.bl_idname == "ScNodeTree"):
            context.space_data.edit_tree.execute_node()
        else:
            log(self.id_data.name, self.name, "update_value", "Context is not Sorcar node-tree")
        return None
    
    def reset(self, execute):
        log(self.id_data.name, self.name, "reset", "Execute="+str(execute), 3)
        if (execute):
            self.first_time = True
        self.set_color()
    
    def set_color(self):
        log(self.id_data.name, self.name, "set_color", "Error="+str(self.node_error)+", Preview="+str(self == self.id_data.nodes.get(str(self.id_data.node))), 3)
        if (self.node_error and self == self.id_data.nodes.get(str(self.id_data.node))):
            self.color = (0.1, 0.1, 0.3)
        elif (self.node_error):
            self.color = (0.9, 0.1, 0.1)
        elif (self == self.id_data.nodes.get(str(self.id_data.node))):
            self.color = (0.1, 0.1, 0.9)
        else:
            self.color = (0.334, 0.334, 0.334)
    
    def init(self, context):
        log(self.id_data.name, self.name, "init", "Executable="+str(self.node_executable), 3)
        self.use_custom_color = True
        self.set_color()
    
    def draw_buttons(self, context, layout):
        if (self.node_executable):
            if (self == context.space_data.edit_tree.nodes.active):
                if (not self == context.space_data.edit_tree.nodes.get(str(context.space_data.edit_tree.node))):
                    layout.operator("sorcar.execute_node", text="Set Preview")
    
    def execute(self, forced=False):
        log(self.id_data.name, self.name, "execute", "FirstTime="+str(self.first_time)+", Forced="+str(forced), 2)
        if (self.first_time or forced):
            self.node_error = True
            if (self.init_in(forced)):
                if not (self.error_condition()):
                    self.pre_execute()
                    self.functionality()
                    self.node_error = not self.init_out(self.post_execute())
            self.first_time = False
        self.set_color()
        return not self.node_error
    
    def init_in(self, forced):
        log(self.id_data.name, self.name, "init_in", "Forced="+str(forced), 3)
        for i in self.inputs:
            if (not i.execute(forced)):
                log(self.id_data.name, self.name, "init_in", "Execution failed for input \""+i.name+"\"", 3)
                return False
        return True
    
    def error_condition(self):
        log(self.id_data.name, self.name, "error_condition", "Checking for invalid parameters", 3)
        return False
    
    def pre_execute(self):
        log(self.id_data.name, self.name, "pre_execute", "Setting up environment", 3)
    
    def functionality(self):
        log(self.id_data.name, self.name, "functionality", "Performing the actual operation", 3)
    
    def post_execute(self):
        log(self.id_data.name, self.name, "post_execute", "Preparing output sockets' data", 3)
        return {}
    
    def init_out(self, out):
        if (not out):
            log(self.id_data.name, self.name, "init_out", "No output", 3)
            return False
        log(self.id_data.name, self.name, "init_out", "Output="+repr(out), 3)
        for i in out:
            if not (self.outputs[i].set(out[i])):
                log(self.id_data.name, self.name, "init_out", "Cannot set output \""+self.outputs[i].name+"\"", 3)
                return False
        return True
    
    def free(self):
        log(self.id_data.name, self.name, "free", "Node removed", 3)