import bpy

from bpy.props import FloatProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode

class ScConvexHull(Node, ScEditOperatorNode):
    bl_idname = "ScConvexHull"
    bl_label = "Convex Hull"
    
    in_delete_unused: BoolProperty(default=True, update=ScNode.update_value)
    in_use_existing_faces: BoolProperty(default=True, update=ScNode.update_value)
    in_make_holes: BoolProperty(name="Make Holes", update=ScNode.update_value)
    in_join_triangles: BoolProperty(default=True, update=ScNode.update_value)
    in_face_threshold: FloatProperty(default=0.698132, min=0.0, max=3.14159, unit="ROTATION", update=ScNode.update_value)
    in_shape_threshold: FloatProperty(default=0.698132, min=0.0, max=3.14159, unit="ROTATION", update=ScNode.update_value)
    in_uvs: BoolProperty(update=ScNode.update_value)
    in_vcols: BoolProperty(update=ScNode.update_value)
    in_seam: BoolProperty(update=ScNode.update_value)
    in_sharp: BoolProperty(update=ScNode.update_value)
    in_materials: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Delete Unused").init("in_delete_unused")
        self.inputs.new("ScNodeSocketBool", "Use Existing Faces").init("in_use_existing_faces")
        self.inputs.new("ScNodeSocketBool", "Make Holes").init("in_make_holes")
        self.inputs.new("ScNodeSocketBool", "Join Triangles").init("in_join_triangles")
        self.inputs.new("ScNodeSocketNumber", "Max Face Angle").init("in_face_threshold", True)
        self.inputs.new("ScNodeSocketNumber", "Max Shape Angle").init("in_shape_threshold")
        self.inputs.new("ScNodeSocketBool", "Compare UVs").init("in_uvs")
        self.inputs.new("ScNodeSocketBool", "Compare VCols").init("in_vcols")
        self.inputs.new("ScNodeSocketBool", "Compare Seam").init("in_seam")
        self.inputs.new("ScNodeSocketBool", "Compare Sharp").init("in_sharp")
        self.inputs.new("ScNodeSocketBool", "Compare Materials").init("in_materials")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (self.inputs["Max Face Angle"].default_value < 0.0 or self.inputs["Max Face Angle"].default_value > 3.14159)
            or (self.inputs["Max Shape Angle"].default_value < 0.0 or self.inputs["Max Shape Angle"].default_value > 3.14159)
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.convex_hull(
            delete_unused = self.inputs["Delete Unused"].default_value,
            use_existing_faces = self.inputs["Use Existing Faces"].default_value,
            make_holes = self.inputs["Make Holes"].default_value,
            join_triangles = self.inputs["Join Triangles"].default_value,
            face_threshold = self.inputs["Max Face Angle"].default_value,
            shape_threshold = self.inputs["Max Shape Angle"].default_value,
            uvs = self.inputs["Compare UVs"].default_value,
            vcols = self.inputs["Compare VCols"].default_value,
            seam = self.inputs["Compare Seam"].default_value,
            sharp = self.inputs["Compare Sharp"].default_value,
            materials = self.inputs["Compare Materials"].default_value
        )