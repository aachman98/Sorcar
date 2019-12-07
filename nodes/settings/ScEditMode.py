import bpy

from bpy.props import EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScEditMode(Node, ScNode):
    bl_idname = "ScEditMode"
    bl_label = "Edit Mode"

    prop_mode: EnumProperty(name="Mode", items=[("VERT", "Vertices", "", "VERTEXSEL", 1), ("EDGE", "Edges", "", "EDGESEL", 2), ("FACE", "Faces", "", "FACESEL", 4)], default={"VERT", "EDGE", "FACE"}, options={"ENUM_FLAG"}, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = False
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_mode")
    
    def error_condition(self):
        return (
            self.inputs["Object"].default_value == None
            or len(self.prop_mode) == 0
        )
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value, True)
    
    def functionality(self):
        bpy.context.tool_settings.mesh_select_mode = ["VERT" in self.prop_mode, "EDGE" in self.prop_mode, "FACE" in self.prop_mode]
    
    def post_execute(self):
        return {"Object": self.inputs["Object"].default_value}