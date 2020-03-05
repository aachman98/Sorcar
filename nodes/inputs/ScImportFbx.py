import bpy
import os

from bpy.props import StringProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_input import ScInputNode

class ScImportFbx(Node, ScInputNode):
    bl_idname = "ScImportFbx"
    bl_label = "Import FBX"

    in_filepath: StringProperty(default="/path/to/dir/")
    in_filename: StringProperty(default="untitled")
    in_uv: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "File Path").init("in_filepath", True)
        self.inputs.new("ScNodeSocketString", "File Name").init("in_filename", True)
        self.inputs.new("ScNodeSocketBool", "Generate UVs").init("in_uv")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["File Path"].default_value == ""
            or self.inputs["File Name"].default_value == ""
        )
    
    def functionality(self):
        bpy.ops.import_scene.fbx(
            filepath = os.path.join(self.inputs["File Path"].default_value, self.inputs["File Name"].default_value + ".fbx"),
            use_custom_normals = self.inputs["Generate UVs"].default_value
        )
    
    def post_execute(self):
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        return super().post_execute()