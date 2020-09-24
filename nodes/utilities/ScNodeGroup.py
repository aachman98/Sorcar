import bpy

from bpy.types import NodeCustomGroup
from .._base.node_base import ScNode
from ...debug import log

class ScNodeGroup(ScNode, NodeCustomGroup):
    bl_idname = "ScNodeGroup"
    bl_label = "Node Group"
    bl_icon = 'NODETREE'

    def init(self, context):
        self.node_executable = True
        super().init(context)

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (self == self.id_data.nodes.active):
            row = layout.row(align=True)
            row.prop(self, "node_tree", text="")
            row.operator("sorcar.edit_group", text="", icon='NODETREE', emboss=True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.node_tree == None
            or self.node_tree.nodes.get('Group Input') == None
            or self.node_tree.nodes.get('Group Output') == None
        )
    
    def pre_execute(self):
        super().pre_execute()
        self.node_tree.reset_nodes(True)
        self.node_tree.objects = []
        for i in range(0, len(self.inputs)):
            self.node_tree.nodes['Group Input'].outputs[i].default_value = self.inputs[i].default_value
    
    def functionality(self):
        super().functionality()
        for i in range(0, len(self.outputs)):
            if (not self.node_tree.nodes['Group Output'].inputs[i].execute(False)):
                break
        self.id_data.objects.extend(self.node_tree.objects)
    
    def post_execute(self):
        super().post_execute()
        out = []
        for i in range(0, len(self.outputs)):
            inp = self.node_tree.nodes['Group Output'].inputs[i]
            if (inp.socket_error):
                return None
            out.append(inp.default_value)
        return out
    
    def init_out(self, out):
        if (not out):
            log(self.id_data.name, self.name, "init_out", "No output", 3)
            return False
        log(self.id_data.name, self.name, "init_out", "Output="+repr(out), 3)
        for i in range(0, len(out)):
            if not (self.outputs[i].set(out[i])):
                log(self.id_data.name, self.name, "init_out", "Cannot set output \""+self.outputs[i].name+"\"", 3)
                return False
        return True
    
    def free(self):
        super().free()
        self.node_tree.unregister_all_objects()