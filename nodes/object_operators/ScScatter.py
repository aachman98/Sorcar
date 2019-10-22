import bpy

from mathutils import Vector
from bpy.props import PointerProperty, StringProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import focus_on_object, remove_object, print_log

class ScScatter(Node, ScObjectOperatorNode):
    bl_idname = "ScScatter"
    bl_label = "Scatter"

    in_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_component: EnumProperty(items=[("FACE", "Faces", ""), ("VERT", "Vertices", ""), ("EDGE", "Edges", "")], default="FACE", update=ScNode.update_value)
    in_align: BoolProperty(default=True, update=ScNode.update_value)
    in_random: BoolProperty(update=ScNode.update_value)
    prop_obj_array: StringProperty(default="[]")

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Scatter Object").init("in_obj", True)
        self.inputs.new("ScNodeSocketString", "Component").init("in_component", True)
        self.inputs.new("ScNodeSocketBool", "Align to Normal").init("in_align")
        self.inputs.new("ScNodeSocketBool", "Random").init("in_random")
        self.outputs.new("ScNodeSocketArray", "Scattered Objects")
    
    def error_condition(self):
        return(
            super().error_condition()
            or self.inputs["Scatter Object"].default_value == None
            or (not self.inputs["Component"].default_value in ['FACE', 'VERT', 'EDGE'])
        )
    
    def pre_execute(self):
        super().pre_execute()
        for obj in self.prop_obj_array[1:-1].split(', '):
            try:
                remove_object(eval(obj))
            except:
                print_log(self.name, None, "pre_execute", "Invalid object: " + obj)
        self.prop_obj_array = "[]"
    
    def functionality(self):
        if (self.inputs["Component"].default_value == 'FACE'):
            loc = [i.center for i in self.inputs["Object"].default_value.data.polygons]
            rot = [i.normal for i in self.inputs["Object"].default_value.data.polygons]
        elif (self.inputs["Component"].default_value == 'VERT'):
            loc = [i.co for i in self.inputs["Object"].default_value.data.vertices]
            rot = [i.normal for i in self.inputs["Object"].default_value.data.vertices]
        else:
            loc = [(Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[0]].co) + Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[1]].co))/2 for i in self.inputs["Object"].default_value.data.edges]
            rot = [(Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[0]].normal) + Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[1]].normal))/2 for i in self.inputs["Object"].default_value.data.edges]
        for i in range(0, len(loc)):
            if (self.inputs["Random"].default_value):
                self.inputs["Scatter Object"].execute(True)
            else:
                focus_on_object(self.inputs["Scatter Object"].default_value)
            bpy.ops.object.duplicate()
            bpy.context.active_object.location = loc[i]
            if (self.inputs["Align to Normal"].default_value):
                bpy.context.active_object.rotation_euler = Vector((0.0, 0.0, 1.0)).rotation_difference(rot[i]).to_euler()
            temp = eval(self.prop_obj_array)
            temp.append(bpy.context.active_object)
            self.prop_obj_array = repr(temp)
    
    def post_execute(self):
        out = super().post_execute()
        out["Scattered Objects"] = self.prop_obj_array
        return out