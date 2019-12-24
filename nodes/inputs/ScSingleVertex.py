import bpy

from bpy.types import Node
from .._base.node_input import ScInputNode


class ScSingleVertex(Node, ScInputNode):
    bl_idname = "ScSingleVertex"
    bl_label = "Single Vertex"

    def functionality(self):
        name = self.inputs["Name"].default_value
        me = bpy.data.meshes.new(name + "_mesh")
        obj = bpy.data.objects.new(name, me)
        obj.location = bpy.context.scene.cursor.location
        me.from_pydata([(0,0,0)], [], [])
        # obj.show_name = True
        me.update()
        # Link object to the active collection
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj




