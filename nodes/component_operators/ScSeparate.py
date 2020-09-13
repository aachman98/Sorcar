import bpy

from bpy.props import EnumProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScEditOperatorNode
from ...debug import log

class ScSeparate(Node, ScEditOperatorNode):
    bl_idname = "ScSeparate"
    bl_label = "Separate"
    
    in_type: EnumProperty(items=[('SELECTED', 'Selected', ''), ('MATERIAL', 'Material', ''), ('LOOSE', 'Loose', '')], default='SELECTED', update=ScNode.update_value)
    prop_obj_array: StringProperty(default="[]")
    
    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.outputs.new("ScNodeSocketArray", "Separated Objects")
    
    def error_condition(self):
        return (
            super().error_condition()
            or (not self.inputs["Type"].default_value in ['SELECTED', 'MATERIAL', 'LOOSE'])
        )
    
    def pre_execute(self):
        super().pre_execute()
        self.prop_obj_array = "[]"
    
    def functionality(self):
        super().functionality()
        bpy.ops.mesh.separate(
            type = self.inputs["Type"].default_value
        )
    
    def post_execute(self):
        ret = super().post_execute()
        if (len(bpy.context.selected_objects) < 2):
            self.prop_obj_array = "[]"
        else:
            self.prop_obj_array = repr(list(bpy.context.selected_objects))
            for object in bpy.context.selected_objects:
                self.id_data.register_object(object)
        ret["Separated Objects"] = self.prop_obj_array
        return ret
    
    def free(self):
        super().free()
        for object in self.prop_obj_array[1:-1].split(', '):
            try:
                obj = eval(object)
            except:
                log(self.id_data.name, self.name, "free", "Invalid object: " + object, 2)
                continue
            self.id_data.unregister_object(obj)