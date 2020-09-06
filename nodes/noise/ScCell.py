import bpy
import mathutils

from bpy.props import FloatVectorProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScCell(Node, ScNode):
    bl_idname = "ScCell"
    bl_label = "Cell"

    in_position: FloatVectorProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Position").init("in_position", True)
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = mathutils.noise.cell(self.inputs["Position"].default_value)
        return out