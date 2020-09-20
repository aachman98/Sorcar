import bpy
import os

from bpy.props import StringProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_input import ScInputNode

class ScImportFbx(Node, ScInputNode):
    bl_idname = "ScImportFbx"
    bl_label = "Import FBX"
    bl_icon = 'IMPORT'

    in_file: StringProperty(subtype='FILE_PATH', update=ScNode.update_value)
    in_uv: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "File").init("in_file", True)
        self.inputs.new("ScNodeSocketBool", "Generate UVs").init("in_uv")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["File"].default_value == ""
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.import_scene.fbx(
            filepath = bpy.path.abspath(self.inputs["File"].default_value),
            use_custom_normals = self.inputs["Generate UVs"].default_value
        )
    
    def post_execute(self):
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        return super().post_execute()