import bpy

from bpy.props import BoolProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScMarkComponent(Node, ScEditOperatorNode):
    bl_idname = "ScMarkComponent"
    bl_label = "Mark Component"
    
    in_type: EnumProperty(items=[('SHARP', 'Sharp', ''), ('SEAM', 'Seam', ''), ('FREESTYLE', 'Freestyle', '')], default='SHARP', update=ScNode.update_value)
    in_clear: BoolProperty(update=ScNode.update_value)
    in_vert: BoolProperty(update=ScNode.update_value)
    in_face: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketBool", "Unmark").init("in_clear", True)
        self.inputs.new("ScNodeSocketBool", "Sharp Vertices").init("in_vert")
        self.inputs.new("ScNodeSocketBool", "Freestyle Faces").init("in_face")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['SHARP', 'SEAM', 'FREESTYLE'])
        )
    
    def functionality(self):
        super().functionality()
        if (self.inputs["Type"].default_value == 'SHARP'):
            bpy.ops.mesh.mark_sharp(
                clear = self.inputs["Unmark"].default_value,
                use_verts = self.inputs["Sharp Vertices"].default_value
            )
        elif (self.inputs["Type"].default_value == 'SEAM'):
            bpy.ops.mesh.mark_seam(
                clear = self.inputs["Unmark"].default_value
            )
        elif (self.inputs["Type"].default_value == 'FREESTYLE'):
            if (self.inputs["Freestyle Faces"].default_value):
                bpy.ops.mesh.mark_freestyle_face(
                    clear = self.inputs["Unmark"].default_value
                )
            else:
                bpy.ops.mesh.mark_freestyle_edge(
                    clear = self.inputs["Unmark"].default_value
                )