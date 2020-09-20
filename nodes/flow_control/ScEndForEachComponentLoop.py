import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...debug import log

class ScEndForEachComponentLoop(Node, ScNode):
    bl_idname = "ScEndForEachComponentLoop"
    bl_label = "End For-Each Component Loop"
    bl_icon = 'TRACKING_BACKWARDS_SINGLE'

    in_iterations: IntProperty(default=5, min=1, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketInfo", "Begin For-Each Component Loop")
        self.inputs.new("ScNodeSocketObject", "In")
        self.outputs.new("ScNodeSocketObject", "Out")
    
    def init_in(self, forced):
        log(self.id_data.name, self.name, "init_in", "Forced="+str(forced), 3)
        if (self.inputs["Begin For-Each Component Loop"].is_linked):
            if (self.inputs["Begin For-Each Component Loop"].links[0].from_node.execute(forced)):
                return True
            else:
                log(self.id_data.name, self.name, "init_in", "Execution failed for node \"Begin For-Each Component Loop\"", 3)
        else:
            log(self.id_data.name, self.name, "init_in", "Info input \"Begin For-Each Component Loop\" not linked", 3)
        return False
    
    def functionality(self):
        super().functionality()
        for i in eval(self.inputs["Begin For-Each Component Loop"].links[0].from_node.prop_components):
            log(self.id_data.name, self.name, "functionality", "Index="+str(i), 3)
            self.inputs["Begin For-Each Component Loop"].links[0].from_node.out_index = i
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.mode_set(mode="OBJECT")
            if (self.inputs["Begin For-Each Component Loop"].links[0].from_node.inputs["Type"].default_value == 'VERT'):
                self.inputs["Begin For-Each Component Loop"].links[0].from_node.outputs["Out"].default_value.data.vertices[i].select = True
            elif (self.inputs["Begin For-Each Component Loop"].links[0].from_node.inputs["Type"].default_value == 'EDGE'):
                self.inputs["Begin For-Each Component Loop"].links[0].from_node.outputs["Out"].default_value.data.edges[i].select = True
            elif (self.inputs["Begin For-Each Component Loop"].links[0].from_node.inputs["Type"].default_value == 'FACE'):
                self.inputs["Begin For-Each Component Loop"].links[0].from_node.outputs["Out"].default_value.data.polygons[i].select = True
            bpy.ops.object.mode_set(mode="EDIT")
            self.inputs["In"].execute(True)
        self.inputs["Begin For-Each Component Loop"].links[0].from_node.prop_locked = False
    
    def post_execute(self):
        out = super().post_execute()
        out["Out"] = self.inputs["In"].default_value
        return out