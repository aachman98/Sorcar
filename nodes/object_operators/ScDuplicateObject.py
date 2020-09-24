import bpy

from bpy.props import BoolProperty, PointerProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import remove_object

class ScDuplicateObject(Node, ScObjectOperatorNode):
    bl_idname = "ScDuplicateObject"
    bl_label = "Duplicate Object"
    bl_icon = 'DUPLICATE'

    in_linked: BoolProperty(update=ScNode.update_value)
    out_mesh: PointerProperty(type=bpy.types.Object)
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Linked").init("in_linked")
        self.outputs.new("ScNodeSocketObject", "Duplicate Object")
    
    def functionality(self):
        super().functionality()
        bpy.ops.object.duplicate(
            linked = self.inputs["Linked"].default_value
        )
    
    def post_execute(self):
        out = super().post_execute()
        self.out_mesh = bpy.context.active_object
        out["Duplicate Object"] = self.out_mesh
        self.id_data.register_object(self.out_mesh)
        return out
    
    def free(self):
        super().free()
        self.id_data.unregister_object(self.out_mesh)