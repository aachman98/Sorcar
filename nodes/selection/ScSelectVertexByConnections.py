import bpy
import bmesh
from bpy.props import IntProperty, BoolProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode


class ScSelectVertexByConnections(Node, ScSelectionNode):
    bl_idname = "ScSelectVertexByConnections"
    bl_label = "Select Vertex By Connections"

    in_connections: IntProperty(default=1, min=0, update=ScNode.update_value)
    in_extend: BoolProperty(default=False, update=ScNode.update_value)
    in_selection_type: EnumProperty(name="Mode", items=[("VERT", "Vertices", "", "VERTEXSEL", 1), ("EDGE", "Edges", "", "EDGESEL", 2), ("FACE", "Faces", "", "FACESEL", 4)], default=set({'VERT'}), options={"ENUM_FLAG"}, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Connections").init("in_connections", True)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")

    def error_condition(self):
        return (
                super().error_condition()
                or int(self.inputs["Connections"].default_value) < 0
                or (not 'VERT' in self.inputs["Selection Type"].default_value)
        )

    def functionality(self):

        bm = bmesh.from_edit_mesh(self.inputs["Object"].default_value.data)
        matched = False
        i = 0
        total_vertex = len(bm.verts)
        any_vertex_selected = False

        # get original selection if use extend:
        if self.in_extend:
            original_selection = [v for v in bm.verts if v.select]

        bpy.ops.mesh.select_all(action='DESELECT')

        if total_vertex != 0 and total_vertex >= 1:
            while not matched and i <= total_vertex:

                # for dont have problems with bmesh:
                if hasattr(bm.verts, "ensure_lookup_table"):
                    bm.verts.ensure_lookup_table()

                # prevent out of range:
                if i <= (total_vertex-1):
                    if len(bm.verts[i].link_edges) == int(self.inputs["Connections"].default_value):
                        v = bm.verts[i]
                        v.select = True
                        any_vertex_selected = True
                        matched = True
                i += 1

            # prevent if not have any vertex selected for select similar:
            if any_vertex_selected:
               bpy.ops.mesh.select_similar(type='EDGE', threshold=0.01)
        else:
            bpy.ops.mesh.select_all(action='DESELECT')

        if self.in_extend:
            for v in original_selection:
                v.select = True
