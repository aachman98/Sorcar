import bpy

from bpy.props import EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import remove_object

class ScSeparate(Node, ScEditOperatorNode):
    bl_idname = "ScSeparate"
    bl_label = "Separate"
    
    in_type: EnumProperty(items=[('SELECTED', 'Selected', ''), ('MATERIAL', 'Material', ''), ('LOOSE', 'Loose', '')], default='SELECTED', update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.outputs.new("ScNodeSocketObject", "Separated Object")
    
    def error_condition(self):
        return(
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['SELECTED', 'MATERIAL', 'LOOSE'])
        )
    
    def pre_execute(self):
        remove_object(self.outputs["Separated Object"].default_value)
        super().pre_execute()
    
    def functionality(self):
        bpy.ops.mesh.separate(
            type = self.inputs["Type"].default_value
        )
    
    def post_execute(self):
        ret = super().post_execute()
        if (len(bpy.context.selected_objects) < 2):
            ret["Separated Object"] = None
        else:
            ret["Separated Object"] = bpy.context.selected_objects[1]
        return ret