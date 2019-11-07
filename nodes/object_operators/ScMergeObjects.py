import bpy

from bpy.props import FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import focus_on_object

class ScMergeObjects(Node, ScObjectOperatorNode):
    bl_idname = "ScMergeObjects"
    bl_label = "Merge Objects"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Mesh Array")
    
    def error_condition(self):
        return(
            super().error_condition()
            or len(eval(self.inputs["Mesh Array"].default_value)) == 0
        )
    
    def pre_execute(self):
        super().pre_execute()
        for obj in eval(self.inputs["Mesh Array"].default_value):
            obj.select_set(True, view_layer=bpy.context.view_layer)
    
    def functionality(self):
        bpy.ops.object.join()