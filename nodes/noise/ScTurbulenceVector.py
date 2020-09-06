import bpy
import mathutils

from bpy.props import FloatVectorProperty, FloatProperty, IntProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScTurbulenceVector(Node, ScNode):
    bl_idname = "ScTurbulenceVector"
    bl_label = "Turbulence (Vector)"

    in_position: FloatVectorProperty(update=ScNode.update_value)
    in_octaves: IntProperty(update=ScNode.update_value)
    in_hard: BoolProperty(update=ScNode.update_value)
    in_noise_basis: EnumProperty(items=[('BLENDER', 'Blender', ''), ('PERLIN_ORIGINAL', 'Perlin (Original)', ''), ('PERLIN_NEW', 'Perlin (New)', ''), ('VORONOI_F1', 'Voronoi (F1)', ''), ('VORONOI_F2', 'Voronoi (F2)', ''), ('VORONOI_F3', 'Voronoi (F3)', ''), ('VORONOI_F4', 'Voronoi (F4)', ''), ('VORONOI_F2F1', 'Voronoi (F2F1)', ''), ('VORONOI_CRACKLE', 'Voronoi (Crackle)', ''), ('CELLNOISE', 'Cellnoise', '')], default='PERLIN_ORIGINAL', update=ScNode.update_value)
    in_amplitude: FloatProperty(default=0.5, update=ScNode.update_value)
    in_frequency: FloatProperty(default=2.0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Position").init("in_position", True)
        self.inputs.new("ScNodeSocketNumber", "Octaves").init("in_octaves")
        self.inputs.new("ScNodeSocketBool", "Hard").init("in_hard")
        self.inputs.new("ScNodeSocketString", "Noise Basis").init("in_noise_basis", True)
        self.inputs.new("ScNodeSocketNumber", "Amplitude Scale").init("in_amplitude")
        self.inputs.new("ScNodeSocketNumber", "Frequency Scale").init("in_frequency")
        self.outputs.new("ScNodeSocketVector", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Noise Basis"].default_value in ['BLENDER', 'PERLIN_ORIGINAL', 'PERLIN_NEW', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2F1', 'VORONOI_CRACKLE', 'CELLNOISE'])
        )
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = mathutils.noise.turbulence_vector(
            self.inputs["Position"].default_value,
            int(self.inputs["Octaves"].default_value),
            self.inputs["Hard"].default_value,
            noise_basis = self.inputs["Noise Basis"].default_value,
            amplitude_scale = self.inputs["Amplitude Scale"].default_value,
            frequency_scale = self.inputs["Frequency Scale"].default_value
        )
        return out