import bpy

from bpy.types import Node
from bpy.props import StringProperty, PointerProperty, BoolProperty
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import focus_on_object

class ScSendToSverchok(Node, ScObjectOperatorNode):
    bl_idname = "ScSendToSverchok"
    bl_label = "Send To Sverchok"

    def sv_poll(self, object):
        return object.bl_idname == "SverchCustomTreeType"
    prop_tree: PointerProperty(name="Tree", type=bpy.types.NodeTree, poll=sv_poll)
    prop_node: StringProperty(update=ScNode.update_value)
    in_hide: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Hide").init("in_hide")

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_tree")
        if (not self.prop_tree == None):
            layout.prop_search(self, "prop_node", self.prop_tree, "nodes", text="Node")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.prop_tree == None
            or (not self.prop_tree.nodes[self.prop_node].bl_idname == "ReceiveFromSorcarNode")
        )
    
    def pre_execute(self):
        if (self.inputs["Hide"].default_value):
            self.inputs["Object"].default_value.hide_set(True)
        super().pre_execute()
    
    def functionality(self):
        obj = self.inputs["Object"].default_value
        v = [[list(i.co) for i in obj.data.vertices]]
        e = [[list(i) for i in obj.data.edge_keys]]
        f = [[list(i.vertices) for i in obj.data.polygons]]
        self.prop_tree.nodes[self.prop_node].verts = repr(v)
        self.prop_tree.nodes[self.prop_node].edges = repr(e)
        self.prop_tree.nodes[self.prop_node].faces = repr(f)