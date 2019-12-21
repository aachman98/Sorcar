import bpy
import bmesh
from bpy.props import IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode


class ScSelectVertexByConnections(Node, ScSelectionNode):
    bl_idname = "ScSelectVertexByConnections"
    bl_label = "Select Vertex By Connections"

    in_connections: IntProperty(default=1, min=0, update=ScNode.update_value)
    in_extend: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Connections").init("in_connections", True)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        # work in vertex mode:
        # With this it is not necessary to manually force the mode to vertices mode:
        self.in_selection_type = {'VERT'}
        self.in_extend = False

    def error_condition(self):
        return (
                super().error_condition()
                or int(self.inputs["Connections"].default_value) < 0
                # prevent other modes:
                or self.in_selection_type != {'VERT'}
        )

    def functionality(self):
        print(self)
        connections = int(self.inputs["Connections"].default_value)
        obj = self.inputs["Object"].default_value

        mode = bpy.context.mode
        if mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        ## Force to use vertex mode:
        ## save selection mode:
        # sel_mode = bpy.context.tool_settings.mesh_select_mode
        ## set selection mode to vertext:
        # if not bpy.context.tool_settings.mesh_select_mode[0]:
        #    bpy.context.tool_settings.mesh_select_mode = [True, False, False]

        bm = bmesh.from_edit_mesh(obj.data)
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
                    if len(bm.verts[i].link_edges) == connections:
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

        ## Restore selection mode forced previously:
        ## restore selection mode:
        # bpy.context.tool_settings.mesh_select_mode = sel_mode
