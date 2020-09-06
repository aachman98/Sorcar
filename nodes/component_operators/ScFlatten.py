import bpy

from bpy.props import FloatProperty, BoolProperty, IntProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScFlatten(Node, ScEditOperatorNode):
    bl_idname = "ScFlatten"
    bl_label = "Flatten"
    
    in_mode: EnumProperty(items=[("FACES", "Faces", ""), ("VERTICES", "Vertices", "")], default="FACES", update=ScNode.update_value)
    in_factor: FloatProperty(default=0.5, min=-10.0, max=10.0, update=ScNode.update_value)
    in_repeat: IntProperty(default=1, min=0, max=1000, update=ScNode.update_value)
    in_x: BoolProperty(default=True, update=ScNode.update_value)
    in_y: BoolProperty(default=True, update=ScNode.update_value)
    in_z: BoolProperty(default=True, update=ScNode.update_value)
    in_laplacian: BoolProperty(update=ScNode.update_value)
    in_lambda_factor: FloatProperty(default=0.5, min=0.0000001, max=1000.0, update=ScNode.update_value)
    in_lambda_border: FloatProperty(default=0.5, min=0.0000001, max=1000.0, update=ScNode.update_value)
    in_preserve_volume: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Mode").init("in_mode", True)
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_factor", True)
        self.inputs.new("ScNodeSocketNumber", "Repeat").init("in_repeat")
        self.inputs.new("ScNodeSocketBool", "X").init("in_x")
        self.inputs.new("ScNodeSocketBool", "Y").init("in_y")
        self.inputs.new("ScNodeSocketBool", "Z").init("in_z")
        self.inputs.new("ScNodeSocketBool", "Laplacian").init("in_laplacian")
        self.inputs.new("ScNodeSocketNumber", "Lambda Factor").init("in_lambda_factor")
        self.inputs.new("ScNodeSocketNumber", "Lambda Border").init("in_lambda_border")
        self.inputs.new("ScNodeSocketBool", "Preserve Volume").init("in_preserve_volume")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Mode"].default_value in ['FACES', 'VERTICES'])
            or (self.inputs["Factor"].default_value < -10.0 or self.inputs["Factor"].default_value > 10.0)
            or (int(self.inputs["Repeat"].default_value) < 0 or int(self.inputs["Repeat"].default_value) > 1000)
            or (self.inputs["Lambda Factor"].default_value < 0.0000001 or self.inputs["Lambda Factor"].default_value > 1000.0)
            or (self.inputs["Lambda Border"].default_value < 0.0000001 or self.inputs["Lambda Border"].default_value > 1000.0)
        )

    def functionality(self):
        super().functionality()
        if (self.inputs["Mode"].default_value == "VERTICES"):
            if (self.inputs["Laplacian"].default_value):
                bpy.ops.mesh.vertices_smooth_laplacian(
                    repeat = int(self.inputs["Repeat"].default_value),
                    lambda_factor = self.inputs["Lambda Factor"].default_value,
                    lambda_border = self.inputs["Lambda Border"].default_value,
                    use_x = self.inputs["X"].default_value,
                    use_y = self.inputs["Y"].default_value,
                    use_z = self.inputs["Z"].default_value,
                    preserve_volume = self.inputs["Preserve Volume"].default_value
                )
            else:
                bpy.ops.mesh.vertices_smooth(
                    factor = self.inputs["Factor"].default_value,
                    repeat = int(self.inputs["Repeat"].default_value),
                    xaxis = self.inputs["X"].default_value,
                    yaxis = self.inputs["Y"].default_value,
                    zaxis = self.inputs["Z"].default_value
                )
        else:
            bpy.ops.mesh.face_make_planar(
                factor = self.inputs["Factor"].default_value,
                repeat = int(self.inputs["Repeat"].default_value)
            )