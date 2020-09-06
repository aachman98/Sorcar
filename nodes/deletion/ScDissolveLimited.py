import bpy

from bpy.props import EnumProperty, BoolProperty, FloatProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_deletion import ScDeletionNode

class ScDissolveLimited(Node, ScDeletionNode):
    bl_idname = "ScDissolveLimited"
    bl_label = "Dissolve Limited"
    
    prop_delimit: EnumProperty(items=[('NORMAL', 'Normal', "", 2), ('MATERIAL', 'Material', "", 4), ('SEAM', 'Seam', "", 8), ('SHARP', 'Sharp', "", 16), ('UV', 'UV', "", 32)], default={'NORMAL'}, options={"ENUM_FLAG"}, update=ScNode.update_value)
    in_angle: FloatProperty(default=0.0872665, min=0, max=3.14159, unit="ROTATION", update=ScNode.update_value)
    in_boundary: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketNumber", "Max Angle").init("in_angle", True)
        self.inputs.new("ScNodeSocketBool", "All Boundaries").init("in_boundary")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_delimit")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Max Angle"].default_value < 0 or self.inputs["Max Angle"].default_value > 3.14159)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.dissolve_limited(
            angle_limit = self.inputs["Max Angle"].default_value,
            use_dissolve_boundaries = self.inputs["All Boundaries"].default_value,
            delimit = self.prop_delimit
        )