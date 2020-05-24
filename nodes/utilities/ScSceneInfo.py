import bpy
import time

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
        self.outputs.new("ScNodeSocketVector", "Cursor Location")
        self.outputs.new("ScNodeSocketVector", "Cursor Rotation")
        self.outputs.new("ScNodeSocketArray", "Objects")
        self.outputs.new("ScNodeSocketNumber", "Unit Scale")
        self.outputs.new("ScNodeSocketNumber", "System Time")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self.id_data, "prop_realtime")
    
    def post_execute(self):
        scene = bpy.context.scene
        out = {}
        out["Start Frame"] = scene.frame_start
        out["Current Frame"] = scene.frame_current
        out["End Frame"] = scene.frame_end
        out["Cursor Location"] = scene.cursor.location
        out["Cursor Rotation"] = scene.cursor.rotation_euler
        out["Objects"] = repr(list(scene.objects))
        out["Unit Scale"] = scene.unit_settings.scale_length
        out["System Time"] = time.time()
        return out