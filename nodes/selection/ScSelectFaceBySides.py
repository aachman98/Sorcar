import bpy

from bpy.props import EnumProperty, IntProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectFaceBySides(Node, ScSelectionNode):
    bl_idname = "ScSelectFaceBySides"
    bl_label = "Select Face by Sides"
    
    in_number: IntProperty(default=4, min=3, update=ScNode.update_value)
    in_type: EnumProperty(items=[("LESS", "Less", ""), ("EQUAL", "Equal", ""), ("GREATER", "Greater", ""), ("NOTEQUAL", "Not Equal", "")], default="EQUAL", update=ScNode.update_value)
    in_extend: BoolProperty(default=True, update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Number").init("in_number", True)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type")
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
    
    def error_condition(self):
        return (
            super().error_condition()
            or int(self.inputs["Number"].default_value) < 3
            or (not self.inputs["Type"].default_value in ['LESS', 'EQUAL', 'GREATER', 'NOTEQUAL'])
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.select_face_by_sides(
            number = int(self.inputs["Number"].default_value),
            type = self.inputs["Type"].default_value,
            extend = self.inputs["Extend"].default_value
        )