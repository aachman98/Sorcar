import bpy

from bpy.props import EnumProperty, IntProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectRandom(Node, ScSelectionNode):
    bl_idname = "ScSelectRandom"
    bl_label = "Select Random"
    
    in_percent: FloatProperty(default=50.0, min=0.0, max=100.0, update=ScNode.update_value)
    in_seed: IntProperty(default=0, min=0, update=ScNode.update_value)
    in_action: EnumProperty(items=[("SELECT", "Select", ""), ("DESELECT", "Deselect", "")], default="SELECT", update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Percent").init("in_percent", True)
        self.inputs.new("ScNodeSocketNumber", "Seed").init("in_seed", True)
        self.inputs.new("ScNodeSocketString", "Action").init("in_action", True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Percent"].default_value < 0 or self.inputs["Percent"].default_value > 100)
            or self.inputs["Seed"].default_value < 0
            or (not self.inputs["Action"].default_value in ["SELECT", "DESELECT"])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_random(
            percent = self.inputs["Percent"].default_value,
            seed = int(self.inputs["Seed"].default_value),
            action = self.inputs["Action"].default_value
        )