import bpy

from bpy.props import BoolProperty, FloatProperty, EnumProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScInstancing(Node, ScObjectOperatorNode):
    bl_idname = "ScInstancing"
    bl_label = "Instancing"
    bl_icon = 'OUTLINER_DATA_POINTCLOUD'

    # prop_collection: PointerProperty(type=bpy.types.Collection, update=ScNode.update_value)
    # in_type: EnumProperty(items=[('NONE', 'None', ''), ('VERTS', 'Vertices', ''), ('FACES', 'Faces', ''), ('COLLECTION', 'Collection', '')], default='NONE', update=ScNode.update_value)
    in_type: EnumProperty(items=[('NONE', 'None', ''), ('VERTS', 'Vertices', ''), ('FACES', 'Faces', '')], default='NONE', update=ScNode.update_value)
    in_display: BoolProperty(default=True, update=ScNode.update_value)
    in_render: BoolProperty(default=True, update=ScNode.update_value)
    in_scale: BoolProperty(update=ScNode.update_value)
    in_factor: FloatProperty(default=1.0, min=0.001, max=10000, update=ScNode.update_value)
    in_rotate: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketBool", "Display Instancer").init("in_display", True)
        self.inputs.new("ScNodeSocketBool", "Render Instancer").init("in_render")
        self.inputs.new("ScNodeSocketBool", "Scale by Face Size").init("in_scale", True)
        self.inputs.new("ScNodeSocketNumber", "Factor").init("in_factor")
        self.inputs.new("ScNodeSocketBool", "Rotate by Vertex Normal").init("in_rotate")
    
    # def draw_buttons(self, context, layout):
    #     super().draw_buttons(context, layout)
    #     if (self.inputs["Type"].default_value == 'COLLECTION'):
    #         layout.prop(self, "prop_collection")
    
    def error_condition(self):
        return (
            super().error_condition()
            # or (not self.inputs["Type"].default_value in ['NONE', 'VERTS', 'FACES', 'COLLECTION'])
            or (not self.inputs["Type"].default_value in ['NONE', 'VERTS', 'FACES'])
            # or (self.inputs["Type"].default_value == 'COLLECTION' and self.prop_collection == None)
            or (self.inputs["Factor"].default_value < 0.001 or self.inputs["Factor"].default_value > 10000)
        )
    
    def functionality(self):
        super().functionality()
        self.inputs["Object"].default_value.instance_type = self.inputs["Type"].default_value
        self.inputs["Object"].default_value.show_instancer_for_viewport = self.inputs["Display Instancer"].default_value
        self.inputs["Object"].default_value.show_instancer_for_render = self.inputs["Render Instancer"].default_value
        self.inputs["Object"].default_value.use_instance_faces_scale = self.inputs["Scale by Face Size"].default_value
        self.inputs["Object"].default_value.instance_faces_scale = self.inputs["Factor"].default_value
        self.inputs["Object"].default_value.use_instance_vertices_rotation = self.inputs["Rotate by Vertex Normal"].default_value
        # self.inputs["Object"].default_value.instance_collection = self.prop_collection