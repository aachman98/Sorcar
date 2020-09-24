import bpy

from bpy.types import Node
from bpy.props import StringProperty, PointerProperty, BoolProperty
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import focus_on_object

class ScSendToSverchok(Node, ScObjectOperatorNode):
    bl_idname = "ScSendToSverchok"
    bl_label = "Send to Sverchok"
    bl_icon = 'RNA_ADD'

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
            or (not self.prop_tree.nodes[self.prop_node].bl_idname == "SvReceiveFromSorcarNode")
        )
    
    def pre_execute(self):
        if (self.inputs["Hide"].default_value):
            self.inputs["Object"].default_value.hide_set(True)
        super().pre_execute()
    
    def functionality(self):
        super().functionality()
        obj = self.inputs["Object"].default_value
        self.prop_tree.nodes[self.prop_node].set_mesh(
            repr([[list(i.co) for i in obj.data.vertices]]),
            repr([[list(i) for i in obj.data.edge_keys]]),
            repr([[list(i.vertices) for i in obj.data.polygons]]),
            repr([[i.select for i in obj.data.vertices]]),
            repr([[i.select for i in obj.data.edges]]),
            repr([[i.select for i in obj.data.polygons]])
        )