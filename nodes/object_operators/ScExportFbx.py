import bpy
import os

from bpy.props import StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScExportFbx(Node, ScObjectOperatorNode):
    bl_idname = "ScExportFbx"
    bl_label = "Export FBX"

    in_file: StringProperty(subtype='FILE_PATH', update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "File").init("in_file", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["File"].default_value == ""
        )
    
    def functionality(self):
        bpy.ops.export_scene.fbx(
            filepath = bpy.path.abspath(self.inputs["File"].default_value),
            use_selection = True,
            use_tspace = True
        )