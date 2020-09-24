import bpy

from bpy.props import BoolProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScDrawMode(Node, ScObjectOperatorNode):
    bl_idname = "ScDrawMode"
    bl_label = "Draw Mode"
    bl_icon = 'MATSHADERBALL'
    
    in_name: BoolProperty(update=ScNode.update_value)
    in_axis: BoolProperty(update=ScNode.update_value)
    in_wire: BoolProperty(update=ScNode.update_value)
    in_all_edges: BoolProperty(update=ScNode.update_value)
    in_front: BoolProperty(update=ScNode.update_value)
    in_shadow: BoolProperty(default=True, update=ScNode.update_value)
    in_display_type: EnumProperty(items=[("SOLID", "Solid", ""), ("WIRE", "Wire", ""), ("BOUNDS", "Bounds", "")], default="SOLID", update=ScNode.update_value)
    in_bounds: BoolProperty(update=ScNode.update_value)
    in_bounds_shape: EnumProperty(items=[("BOX", "Box", ""), ("SPHERE", "Sphere", ""), ("CYLINDER", "Cylinder", ""), ("CONE", "Cone", ""), ("CAPSULE", "Capsule", "")], default="BOX", update=ScNode.update_value)
    in_visibility_viewport: BoolProperty(default=True, update=ScNode.update_value)
    in_visibility_render: BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Name").init("in_name")
        self.inputs.new("ScNodeSocketBool", "Axis").init("in_axis")
        self.inputs.new("ScNodeSocketBool", "Wireframe").init("in_wire")
        self.inputs.new("ScNodeSocketBool", "All Edges").init("in_all_edges")
        self.inputs.new("ScNodeSocketBool", "In Front").init("in_front")
        self.inputs.new("ScNodeSocketBool", "Shadow").init("in_shadow")
        self.inputs.new("ScNodeSocketString", "Display As").init("in_display_type", True)
        self.inputs.new("ScNodeSocketBool", "Bounds").init("in_bounds")
        self.inputs.new("ScNodeSocketString", "Bounds Shape").init("in_bounds_shape")
        self.inputs.new("ScNodeSocketBool", "Viewport").init("in_visibility_viewport")
        self.inputs.new("ScNodeSocketBool", "Render").init("in_visibility_render")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Display As"].default_value in ['SOLID', 'WIRE', 'BOUNDS'])
            or (not self.inputs["Bounds Shape"].default_value in ['BOX', 'SPHERE', 'CYLINDER', 'CONE', 'CAPSULE'])
        )
    
    def functionality(self):
        super().functionality()
        self.inputs["Object"].default_value.show_name = self.inputs["Name"].default_value
        self.inputs["Object"].default_value.show_axis = self.inputs["Axis"].default_value
        self.inputs["Object"].default_value.show_wire = self.inputs["Wireframe"].default_value
        self.inputs["Object"].default_value.show_all_edges = self.inputs["All Edges"].default_value
        self.inputs["Object"].default_value.show_in_front = self.inputs["In Front"].default_value
        self.inputs["Object"].default_value.display.show_shadows = self.inputs["Shadow"].default_value
        self.inputs["Object"].default_value.display_type = self.inputs["Display As"].default_value
        self.inputs["Object"].default_value.show_bounds = self.inputs["Bounds"].default_value
        self.inputs["Object"].default_value.display_bounds_type = self.inputs["Bounds Shape"].default_value
        self.inputs["Object"].default_value.hide_viewport = not self.inputs["Viewport"].default_value
        self.inputs["Object"].default_value.hide_render = not self.inputs["Render"].default_value