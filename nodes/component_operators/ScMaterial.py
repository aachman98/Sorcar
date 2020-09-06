import bpy

from bpy.props import PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import get_override

class ScMaterial(Node, ScEditOperatorNode):
    bl_idname = "ScMaterial"
    bl_label = "Material"
    
    prop_mat: PointerProperty(name="Material", type=bpy.types.Material, update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_mat")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.prop_mat == None
        )
    
    def pre_execute(self):
        super().pre_execute()
        slot = self.inputs["Object"].default_value.material_slots.find(self.prop_mat.name)
        if (slot == -1):
            bpy.ops.object.material_slot_add()
            self.inputs["Object"].default_value.active_material = self.prop_mat
        else:
            self.inputs["Object"].default_value.active_material_index = slot
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.material_slot_assign()