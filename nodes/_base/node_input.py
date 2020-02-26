import bpy

from bpy.props import PointerProperty, StringProperty, BoolProperty
from .._base.node_base import ScNode
from ...helper import focus_on_object, remove_object

class ScInputNode(ScNode):
    in_name: StringProperty(default="Object", update=ScNode.update_value)
    out_mesh: PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.node_executable = True
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Name").init("in_name")
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            self.inputs["Name"].default_value == ""
        )
    
    def pre_execute(self):
        focus_on_object(self.out_mesh)
        remove_object(self.out_mesh)
    
    def post_execute(self):
        out = {}
        self.out_mesh = bpy.context.active_object
        self.out_mesh.name = self.inputs["Name"].default_value
        if (self.out_mesh.data):
            self.out_mesh.data.name = self.out_mesh.name
        out["Object"] = self.out_mesh
        return out