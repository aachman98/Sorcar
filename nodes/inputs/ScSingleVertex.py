import bpy

from bpy.props import BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_input import ScInputNode


class ScSingleVertex(Node, ScInputNode):
    bl_idname = "ScSingleVertex"
    bl_label = "Single Vertex"
    bl_icon = 'DOT'

    in_show_name: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Show Name").init("in_show_name", True)

    def functionality(self):
        super().functionality()
        m = bpy.data.meshes.new(self.inputs["Name"].default_value)
        obj = bpy.data.objects.new(self.inputs["Name"].default_value, m)
        obj.location = bpy.context.scene.cursor.location
        m.vertices.add(1)
        m.update()
        obj.show_name = self.inputs["Show Name"].default_value
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj




