import bpy
import mathutils

from bpy.props import FloatVectorProperty, FloatProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode

class ScVariableLacunarity(Node, ScNode):
    bl_idname = "ScVariableLacunarity"
    bl_label = "Variable Lacunarity"

    in_position: FloatVectorProperty(update=ScNode.update_value)
    in_distortion: FloatProperty(update=ScNode.update_value)
    in_noise_type1: EnumProperty(items=[('BLENDER', 'Blender', ''), ('PERLIN_ORIGINAL', 'Perlin (Original)', ''), ('PERLIN_NEW', 'Perlin (New)', ''), ('VORONOI_F1', 'Voronoi (F1)', ''), ('VORONOI_F2', 'Voronoi (F2)', ''), ('VORONOI_F3', 'Voronoi (F3)', ''), ('VORONOI_F4', 'Voronoi (F4)', ''), ('VORONOI_F2F1', 'Voronoi (F2F1)', ''), ('VORONOI_CRACKLE', 'Voronoi (Crackle)', ''), ('CELLNOISE', 'Cellnoise', '')], default='PERLIN_ORIGINAL', update=ScNode.update_value)
    in_noise_type2: EnumProperty(items=[('BLENDER', 'Blender', ''), ('PERLIN_ORIGINAL', 'Perlin (Original)', ''), ('PERLIN_NEW', 'Perlin (New)', ''), ('VORONOI_F1', 'Voronoi (F1)', ''), ('VORONOI_F2', 'Voronoi (F2)', ''), ('VORONOI_F3', 'Voronoi (F3)', ''), ('VORONOI_F4', 'Voronoi (F4)', ''), ('VORONOI_F2F1', 'Voronoi (F2F1)', ''), ('VORONOI_CRACKLE', 'Voronoi (Crackle)', ''), ('CELLNOISE', 'Cellnoise', '')], default='PERLIN_ORIGINAL', update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketVector", "Position").init("in_position", True)
        self.inputs.new("ScNodeSocketNumber", "Distortion").init("in_distortion", True)
        self.inputs.new("ScNodeSocketString", "Noise Type 1").init("in_noise_type1")
        self.inputs.new("ScNodeSocketString", "Noise Type 2").init("in_noise_type2")
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Noise Type 1"].default_value in ['BLENDER', 'PERLIN_ORIGINAL', 'PERLIN_NEW', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2F1', 'VORONOI_CRACKLE', 'CELLNOISE'])
            or (not self.inputs["Noise Type 2"].default_value in ['BLENDER', 'PERLIN_ORIGINAL', 'PERLIN_NEW', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2F1', 'VORONOI_CRACKLE', 'CELLNOISE'])
        )
    
    def post_execute(self):
        out = super().post_execute()
        out["Value"] = mathutils.noise.variable_lacunarity(
            self.inputs["Position"].default_value,
            self.inputs["Distortion"].default_value,
            noise_type1 = self.inputs["Noise Type 2"].default_value,
            noise_type2 = self.inputs["Noise Type 2"].default_value
        )
        return out