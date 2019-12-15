import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScEndForEachComponentLoop(Node, ScNode):
    bl_idname = "ScEndForEachComponentLoop"
    bl_label = "End For-Each Component Loop"

    in_iterations: IntProperty(default=5, min=1, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketInfo", "Begin For-Each Component Loop")
        self.inputs.new("ScNodeSocketObject", "In")
        self.outputs.new("ScNodeSocketObject", "Out")
    
    def init_in(self, forced):
        return (
            self.inputs["Begin For-Each Component Loop"].is_linked
            and self.inputs["Begin For-Each Component Loop"].links[0].from_node.execute(forced)
        )
    
    def functionality(self):
        for i in eval(self.inputs["Begin For-Each Component Loop"].links[0].from_node.prop_components):
            self.inputs["Begin For-Each Component Loop"].links[0].from_node.out_index = i
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.mode_set(mode="OBJECT")
            self.inputs["Begin For-Each Component Loop"].links[0].from_node.outputs["Out"].default_value.data.polygons[i].select = True
            bpy.ops.object.mode_set(mode="EDIT")
            self.inputs["In"].execute(True)
        self.inputs["Begin For-Each Component Loop"].links[0].from_node.prop_locked = False
    
    def post_execute(self):
        out = {}
        out["Out"] = self.inputs["In"].default_value
        return out