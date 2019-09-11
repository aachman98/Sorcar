import bpy

from bpy.types import Node
from .._base.node_base import ScNode

class ScSceneInfo(Node, ScNode):
    bl_idname = "ScSceneInfo"
    bl_label = "Scene Info"

    def init(self, context):
        super().init(context)
        self.outputs.new("ScNodeSocketNumber", "Start Frame")
        self.outputs.new("ScNodeSocketNumber", "Current Frame")
        self.outputs.new("ScNodeSocketNumber", "End Frame")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self.id_data, "prop_realtime")
    
    def post_execute(self):
        out = {}
        out["Start Frame"] = bpy.context.scene.frame_start
        out["Current Frame"] = bpy.context.scene.frame_current
        out["End Frame"] = bpy.context.scene.frame_end
        return out