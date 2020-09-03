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
            super().error_condition()
            or self.inputs["Name"].default_value == ""
        )
    
    def pre_execute(self):
        super().pre_execute()
        if (bpy.ops.object.mode_set.poll()):
            bpy.ops.object.mode_set(mode="OBJECT")
    
    def post_execute(self):
        out = super().post_execute()
        self.out_mesh = bpy.context.active_object
        self.out_mesh.name = self.inputs["Name"].default_value
        if (self.out_mesh.data):
            self.out_mesh.data.name = self.out_mesh.name
        out["Object"] = self.out_mesh
        self.id_data.register_object(self.out_mesh)
        return out
    
    def free(self):
        self.id_data.unregister_object(self.out_mesh)
        super().free()