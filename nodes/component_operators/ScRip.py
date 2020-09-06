import bpy

from bpy.props import BoolProperty, FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import get_override

class ScRip(Node, ScEditOperatorNode):
    bl_idname = "ScRip"
    bl_label = "Rip"
    
    in_value: FloatVectorProperty(update=ScNode.update_value)
    in_mirror: BoolProperty(update=ScNode.update_value)
    in_fill: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Value").init("in_value", True)
        self.inputs.new("ScNodeSocketBool", "Mirror Editing").init("in_mirror")
        self.inputs.new("ScNodeSocketBool", "Fill").init("in_fill")
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.rip_move(
            get_override(self.inputs["Object"].default_value, True),
            MESH_OT_rip = {
                "mirror": self.inputs["Mirror Editing"].default_value,
                "use_fill": self.inputs["Fill"].default_value
            },
            TRANSFORM_OT_translate = {
                "value": self.inputs["Value"].default_value
            }
        )