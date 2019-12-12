import bpy
import mathutils

from bpy.props import FloatVectorProperty, FloatProperty, IntProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScMultiFractal(Node, ScNode):
    bl_idname = "ScMultiFractal"
    bl_label = "Multi-Fractal"

    in_position: FloatVectorProperty(update=ScNode.update_value)
    in_h: FloatProperty(update=ScNode.update_value)
    in_lacunarity: FloatProperty(update=ScNode.update_value)
    in_octaves: IntProperty(update=ScNode.update_value)
    in_noise_basis: EnumProperty(items=[('BLENDER', 'Blender', ''), ('PERLIN_ORIGINAL', 'Perlin (Original)', ''), ('PERLIN_NEW', 'Perlin (New)', ''), ('VORONOI_F1', 'Voronoi (F1)', ''), ('VORONOI_F2', 'Voronoi (F2)', ''), ('VORONOI_F3', 'Voronoi (F3)', ''), ('VORONOI_F4', 'Voronoi (F4)', ''), ('VORONOI_F2F1', 'Voronoi (F2F1)', ''), ('VORONOI_CRACKLE', 'Voronoi (Crackle)', ''), ('CELLNOISE', 'Cellnoise', '')], default='PERLIN_ORIGINAL', update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Position").init("in_position", True)
        self.inputs.new("ScNodeSocketNumber", "H").init("in_h")
        self.inputs.new("ScNodeSocketNumber", "Lacunarity").init("in_lacunarity")
        self.inputs.new("ScNodeSocketNumber", "Octaves").init("in_octaves")
        self.inputs.new("ScNodeSocketString", "Noise Basis").init("in_noise_basis", True)
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Noise Basis"].default_value in ['BLENDER', 'PERLIN_ORIGINAL', 'PERLIN_NEW', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2F1', 'VORONOI_CRACKLE', 'CELLNOISE'])
        )
    
    def post_execute(self):
        out = {}
        out["Value"] = mathutils.noise.multi_fractal(
            self.inputs["Position"].default_value,
            self.inputs["H"].default_value,
            self.inputs["Lacunarity"].default_value,
            int(self.inputs["Octaves"].default_value),
            noise_basis = self.inputs["Noise Basis"].default_value
        )
        return out