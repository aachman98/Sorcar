import bpy
import time

from bpy.types import Node
from .._base.node_base import ScNode

class ScSceneInfo(Node, ScNode):
    bl_idname = "ScSceneInfo"
    bl_label = "Scene Info"
    bl_icon = 'SCENE_DATA'

    def init(self, context):
        super().init(context)
        self.outputs.new("ScNodeSocketNumber", "Start Frame")
        self.outputs.new("ScNodeSocketNumber", "Current Frame")
        self.outputs.new("ScNodeSocketNumber", "End Frame")
        self.outputs.new("ScNodeSocketVector", "Cursor Location")
        self.outputs.new("ScNodeSocketVector", "Cursor Rotation")
        self.outputs.new("ScNodeSocketObject", "Active Object")
        self.outputs.new("ScNodeSocketArray", "Selected Objects")
        self.outputs.new("ScNodeSocketArray", "All Objects")
        self.outputs.new("ScNodeSocketNumber", "Unit Scale")
        self.outputs.new("ScNodeSocketNumber", "System Time")
    
    def post_execute(self):
        c = bpy.context
        s = c.scene
        out = super().post_execute()
        out["Start Frame"] = s.frame_start
        out["Current Frame"] = s.frame_current
        out["End Frame"] = s.frame_end
        out["Cursor Location"] = s.cursor.location
        out["Cursor Rotation"] = s.cursor.rotation_euler
        out["Active Object"] = c.object
        out["Selected Objects"] = repr(list(c.selected_objects))
        out["All Objects"] = repr(list(s.objects))
        out["Unit Scale"] = s.unit_settings.scale_length
        out["System Time"] = time.time()
        return out