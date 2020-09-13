import bpy

from bpy.props import IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectAlternateFaces(Node, ScSelectionNode):
    bl_idname = "ScSelectAlternateFaces"
    bl_label = "Select Alternate Faces"
    
    in_nth: IntProperty(name="Every Nth", default=2, min=1, update=ScNode.update_value)
    in_offset: IntProperty(name="Offset", min=0, update=ScNode.update_value)
    in_extend: BoolProperty(update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Every Nth").init("in_nth", True)
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset", True)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")
    
    def error_condition(self):
        return (
            super().error_condition()
            or int(self.inputs["Every Nth"].default_value) < 1
            or int(self.inputs["Offset"].default_value) < 0
        )
    
    def pre_execute(self):
        super().pre_execute()
        if (not self.inputs["Extend"].default_value):
            if (self.inputs["Deselect"].default_value):
                bpy.ops.mesh.select_all(action="SELECT")
            else:
                bpy.ops.mesh.select_all(action="DESELECT")
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.mode_set(mode="OBJECT")
        for i in range(int(self.inputs["Offset"].default_value), len(self.inputs["Object"].default_value.data.polygons), int(self.inputs["Every Nth"].default_value)):
            self.inputs["Object"].default_value.data.polygons[i].select = not self.inputs["Deselect"].default_value
        bpy.ops.object.mode_set(mode="EDIT")