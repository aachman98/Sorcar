import bpy
import mathutils

from bpy.props import FloatVectorProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScNoiseVector(Node, ScNode):
    bl_idname = "ScNoiseVector"
    bl_label = "Noise (Vector)"

    in_position: FloatVectorProperty(update=ScNode.update_value)
    in_noise_basis: EnumProperty(items=[('BLENDER', 'Blender', ''), ('PERLIN_ORIGINAL', 'Perlin (Original)', ''), ('PERLIN_NEW', 'Perlin (New)', ''), ('VORONOI_F1', 'Voronoi (F1)', ''), ('VORONOI_F2', 'Voronoi (F2)', ''), ('VORONOI_F3', 'Voronoi (F3)', ''), ('VORONOI_F4', 'Voronoi (F4)', ''), ('VORONOI_F2F1', 'Voronoi (F2F1)', ''), ('VORONOI_CRACKLE', 'Voronoi (Crackle)', ''), ('CELLNOISE', 'Cellnoise', '')], default='PERLIN_ORIGINAL', update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Position").init("in_position", True)
        self.inputs.new("ScNodeSocketString", "Noise Basis").init("in_noise_basis", True)
        self.outputs.new("ScNodeSocketVector", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Noise Basis"].default_value in ['BLENDER', 'PERLIN_ORIGINAL', 'PERLIN_NEW', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2F1', 'VORONOI_CRACKLE', 'CELLNOISE'])
        )
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = mathutils.noise.noise_vector(
            self.inputs["Position"].default_value,
            noise_basis = self.inputs["Noise Basis"].default_value
        )
        return out