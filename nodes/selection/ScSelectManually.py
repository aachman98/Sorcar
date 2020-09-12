import bpy

from bpy.props import StringProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode
from ...debug import log

class ScSelectManually(Node, ScSelectionNode):
    bl_idname = "ScSelectManually"
    bl_label = "Select Manually"
    
    prop_vert: StringProperty(default="[]")
    prop_edge: StringProperty(default="[]")
    prop_face: StringProperty(default="[]")
    prop_active: IntProperty()

    def save_selection(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        vert = [i.index for i in self.inputs["Object"].default_value.data.vertices if i.select]
        edge = [i.index for i in self.inputs["Object"].default_value.data.edges if i.select]
        face = [i.index for i in self.inputs["Object"].default_value.data.polygons if i.select]
        log(self.id_data.name, self.name, "save_selection", "Vertices="+str(len(vert))+", Edges="+str(len(edge))+", Faces="+str(len(face)), 3)
        self.prop_vert = repr(vert)
        self.prop_edge = repr(edge)
        self.prop_face = repr(face)
        self.prop_active = self.inputs["Object"].default_value.data.polygons.active
        bpy.ops.object.mode_set(mode="EDIT")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (self.node_executable):
            if (self == context.space_data.edit_tree.nodes.active):
                if (self == context.space_data.edit_tree.nodes.get(str(context.space_data.edit_tree.node))):
                    layout.operator("sorcar.save_selection")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        for i in eval(self.prop_vert):
            self.inputs["Object"].default_value.data.vertices[i].select = True
        for i in eval(self.prop_edge):
            self.inputs["Object"].default_value.data.edges[i].select = True
        for i in eval(self.prop_face):
            self.inputs["Object"].default_value.data.polygons[i].select = True
            self.inputs["Object"].default_value.data.polygons.active = self.prop_active
        bpy.ops.object.mode_set(mode="EDIT")