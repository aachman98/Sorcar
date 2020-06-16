import bpy

from bpy.props import EnumProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...helper import remove_object

class ScSeparate(Node, ScEditOperatorNode):
    bl_idname = "ScSeparate"
    bl_label = "Separate"
    
    in_type: EnumProperty(items=[('SELECTED', 'Selected', ''), ('MATERIAL', 'Material', ''), ('LOOSE', 'Loose', '')], default='SELECTED', update=ScNode.update_value)
    out_mesh: PointerProperty(type=bpy.types.Object)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.outputs.new("ScNodeSocketObject", "Separated Object")
    
    def error_condition(self):
        return(
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['SELECTED', 'MATERIAL', 'LOOSE'])
        )
    
    def functionality(self):
        bpy.ops.mesh.separate(
            type = self.inputs["Type"].default_value
        )
    
    def post_execute(self):
        ret = super().post_execute()
        if (len(bpy.context.selected_objects) < 2):
            self.out_mesh = None
        else:
            self.out_mesh = bpy.context.selected_objects[1]
            self.id_data.register_object(self.out_mesh)
        ret["Separated Object"] = self.out_mesh
        return ret
    
    def free(self):
        self.id_data.unregister_object(self.out_mesh)