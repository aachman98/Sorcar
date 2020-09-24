import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScMakeLinks(Node, ScObjectOperatorNode):
    bl_idname = "ScMakeLinks"
    bl_label = "Make Links"
    bl_icon = 'LINKED'
    
    in_type: EnumProperty(items=[("OBDATA", "Object Data", ""), ("MATERIAL", "Material", ""), ("ANIMATION", "Animation", ""), ("GROUPS", "Groups", ""), ("DUPLIGROUP", "Dupligroup", ""), ("MODIFIERS", "Modifiers", ""), ("FONTS", "Fonts", "")], default="OBDATA", update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketArray", "Objects")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['OBDATA', 'MATERIAL', 'ANIMATION', 'GROUPS', 'DUPLICOLLECTION', 'MODIFIERS', 'FONTS'])
        )
    
    def pre_execute(self):
        super().pre_execute()
        for obj in eval(self.inputs["Objects"].default_value):
            obj.select_set(True, view_layer=bpy.context.view_layer)
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.make_links_data(
            type = self.inputs["Type"].default_value
        )