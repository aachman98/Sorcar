import bpy

from bpy.props import PointerProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectByMaterial(Node, ScSelectionNode):
    bl_idname = "ScSelectByMaterial"
    bl_label = "Select by Material"
    
    prop_mat: PointerProperty(name="Material", type=bpy.types.Material, update=ScNode.update_value)
    in_extend: BoolProperty(update=ScNode.update_value)
    in_deselect: BoolProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Extend").init("in_extend")
        self.inputs.new("ScNodeSocketBool", "Deselect").init("in_deselect")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_mat")
    
    def error_condition(self):
        return (
            super().error_condition()
            or self.prop_mat == None
            or self.inputs["Object"].default_value.material_slots.find(self.prop_mat.name) == -1
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
        self.inputs["Object"].default_value.active_material_index = self.inputs["Object"].default_value.material_slots.find(self.prop_mat.name)
        if (self.inputs["Deselect"].default_value):
            bpy.ops.object.material_slot_deselect()
        else:
            bpy.ops.object.material_slot_select()