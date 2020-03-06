import bpy

from bpy.props import PointerProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScParent(Node, ScObjectOperatorNode):
    bl_idname = "ScParent"
    bl_label = "Parent"

    prop_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_ops_type: EnumProperty(items=[('OBJECT', 'Object', ''), ('WITHOUT_INVERSE', 'Object(Without Inverse)', '')], default='OBJECT', update=ScNode.update_value)
    in_keep_transform: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Parent").init("prop_obj", True)
        self.inputs.new("ScNodeSocketString", "Type").init("in_ops_type")
        self.inputs.new("ScNodeSocketBool", "Keep Transform").init(
            "in_keep_transform")

    def error_condition(self):
        return (
            super().error_condition()
            or self.inputs["Parent"].default_value == None
            or (not self.inputs["Type"].default_value in ['OBJECT', 'WITHOUT_INVERSE'])
        )

    def functionality(self):
        parent = self.inputs["Parent"].default_value
        parent.select_set(state=True)
        bpy.context.view_layer.objects.active = parent

        if self.inputs["Type"].default_value == "WITHOUT_INVERSE":
            bpy.ops.object.parent_no_inverse_set()
        else:
            bpy.ops.object.parent_set(
                type = 'OBJECT',
                keep_transform = self.inputs["Keep Transform"].default_value
            )
