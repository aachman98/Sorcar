import bpy
import bmesh

from bpy.props import IntProperty, BoolProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScSelectVerticesByConnections(Node, ScEditOperatorNode):
    bl_idname = "ScSelectVerticesByConnections"
    bl_label = "Select Vertices by Connections"

    in_connections: IntProperty(default=1, min=0, update=ScNode.update_value)
    in_extend: BoolProperty(default=False, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Connections").init("in_connections", True)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")

    def error_condition(self):
        return (
            super().error_condition()
            or int(self.inputs["Connections"].default_value) < 0
        )
    
    def pre_execute(self):
        super().pre_execute()
        bpy.context.tool_settings.mesh_select_mode = [True, False, False]

    def functionality(self):
        super().functionality()
        bm = bmesh.from_edit_mesh(self.inputs["Object"].default_value.data)
        index = -1
        if hasattr(bm.verts, "ensure_lookup_table"):
            bm.verts.ensure_lookup_table()
        if (self.inputs["Extend"].default_value):
            original_selection = [v.index for v in bm.verts if v.select]
        bpy.ops.mesh.select_all(action='DESELECT')
        for i in bm.verts:
            if (len(i.link_edges) == int(self.inputs["Connections"].default_value)):
                index = i.index
                break
        if (not index == -1):
            bm.verts[index].select_set(True)
            bpy.ops.mesh.select_similar(type='EDGE', threshold=0.01)
        bm.free()
        if (self.inputs["Extend"].default_value):
            bpy.ops.object.mode_set(mode='OBJECT')
            for i in original_selection:
                self.inputs["Object"].default_value.data.vertices[i].select = True
            bpy.ops.object.mode_set(mode='EDIT')