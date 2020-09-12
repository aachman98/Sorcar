import bpy

from bpy.props import EnumProperty, BoolProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectShortestPath(Node, ScSelectionNode):
    bl_idname = "ScSelectShortestPath"
    bl_label = "Select Shortest Path"
    
    in_mode: EnumProperty(items=[('SELECT', 'Select', ""), ('SEAM', 'Seam', ""), ('SHARP', 'Sharp', ""), ('CREASE', 'Crease', ""), ('BEVEL', 'Bevel', ""), ('FREESTYLE', 'Freestyle', "")], default="SELECT", update=ScNode.update_value)
    in_step: BoolProperty(update=ScNode.update_value)
    in_distance: BoolProperty(update=ScNode.update_value)
    in_fill: BoolProperty(update=ScNode.update_value)
    in_nth: IntProperty(default=1, min=1, update=ScNode.update_value)
    in_skip: IntProperty(min=0, update=ScNode.update_value)
    in_offset: IntProperty(update=ScNode.update_value)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Edge Tag").init("in_mode")
        self.inputs.new("ScNodeSocketBool", "Face Stepping").init("in_step")
        self.inputs.new("ScNodeSocketBool", "Topology Distance").init("in_distance")
        self.inputs.new("ScNodeSocketBool", "Fill Region").init("in_fill")
        self.inputs.new("ScNodeSocketNumber", "Nth Selection").init("in_nth")
        self.inputs.new("ScNodeSocketNumber", "Skip").init("in_skip")
        self.inputs.new("ScNodeSocketNumber", "Offset").init("in_offset")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Edge Tag"].default_value in ['SELECT', 'SEAM', 'SHARP', 'CREASE', 'BEVEL', 'FREESTYLE'])
            or int(self.inputs["Nth Selection"].default_value) < 1
            or int(self.inputs["Skip"].default_value) < 0
        )
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.shortest_path_select(
            edge_mode = self.inputs["Edge Tag"].default_value,
            use_face_step = self.inputs["Face Stepping"].default_value,
            use_topology_distance = self.inputs["Topology Distance"].default_value,
            use_fill = self.inputs["Fill Region"].default_value,
            nth = int(self.inputs["Nth Selection"].default_value),
            skip = int(self.inputs["Skip"].default_value),
            offset = int(self.inputs["Offset"].default_value)
        )
