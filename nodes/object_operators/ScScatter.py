import bpy

from mathutils import Vector
from bpy.props import PointerProperty, StringProperty, EnumProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode
from ...helper import focus_on_object, remove_object, print_log

class ScScatter(Node, ScObjectOperatorNode):
    bl_idname = "ScScatter"
    bl_label = "Scatter"

    prop_loc: EnumProperty(items=[('X', 'X', '', 2), ('Y', 'Y', '', 4), ('Z', 'Z', '', 8)], default={'X', 'Y', 'Z'}, options={'ENUM_FLAG'}, update=ScNode.update_value)
    prop_rot: EnumProperty(items=[('X', 'X', '', 2), ('Y', 'Y', '', 4), ('Z', 'Z', '', 8)], default={'X', 'Y', 'Z'}, options={'ENUM_FLAG'}, update=ScNode.update_value)
    in_obj: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    in_type: EnumProperty(items=[('INST', 'Instanced', ''), ('MAN', 'Manual', ''), ('RAND', 'Random', '')], default='INST', update=ScNode.update_value)
    in_component: EnumProperty(items=[("FACES", "Faces", ""), ("VERTS", "Vertices", ""), ("EDGES", "Edges", "")], default="FACES", update=ScNode.update_value)
    prop_obj_array: StringProperty(default="[]")

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Scatter Object").init("in_obj", True)
        self.inputs.new("ScNodeSocketString", "Type").init("in_type", True)
        self.inputs.new("ScNodeSocketString", "Component").init("in_component", True)
        self.outputs.new("ScNodeSocketArray", "Scattered Objects")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Type"].default_value == 'INST'):
            layout.label(text="Location:")
            layout.prop(self, "prop_loc", expand=True)
            layout.label(text="Rotation:")
            layout.prop(self, "prop_rot", expand=True)
    
    def error_condition(self):
        return(
            super().error_condition()
            or self.inputs["Scatter Object"].default_value == None
            or (not self.inputs["Component"].default_value in ['FACES', 'VERTS', 'EDGES'])
            or (not self.inputs["Type"].default_value in ['INST', 'MAN', 'RAND'])
            or (self.inputs["Type"].default_value == 'INST' and self.inputs["Component"].default_value == 'EDGES')
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
        if (self.inputs["Type"].default_value == 'INST'):
            o = self.inputs["Object"].default_value
            so = self.inputs["Scatter Object"].default_value
            o.instance_type = self.inputs["Component"].default_value
            so.parent = o
            focus_on_object(o)
            bpy.ops.object.duplicates_make_real(use_base_parent=True)
            so.parent = None
            arr_inst = o.children
            self.prop_obj_array = repr(arr_inst)
            bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
            for i in arr_inst:
                i.parent = None
            o.instance_type = 'NONE'
        else:
            if (self.inputs["Component"].default_value == 'FACES'):
                loc = [i.center for i in self.inputs["Object"].default_value.data.polygons if i.select]
                rot = [i.normal for i in self.inputs["Object"].default_value.data.polygons if i.select]
            elif (self.inputs["Component"].default_value == 'VERTS'):
                loc = [i.co for i in self.inputs["Object"].default_value.data.vertices if i.select]
                rot = [i.normal for i in self.inputs["Object"].default_value.data.vertices if i.select]
            else:
                loc = [(Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[0]].co) + Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[1]].co))/2 for i in self.inputs["Object"].default_value.data.edges if i.select]
                rot = [(Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[0]].normal) + Vector(self.inputs["Object"].default_value.data.vertices[i.vertices[1]].normal))/2 for i in self.inputs["Object"].default_value.data.edges if i.select]
            for i in range(0, len(loc)):
                focus_on_object(self.inputs["Scatter Object"].default_value)
                bpy.ops.object.duplicate()
                if ('X' in self.prop_loc):
                    bpy.context.active_object.location[0] = loc[i][0]
                if ('Y' in self.prop_loc):
                    bpy.context.active_object.location[1] = loc[i][1]
                if ('Z' in self.prop_loc):
                    bpy.context.active_object.location[2] = loc[i][2]
                rot_diff = Vector((0.0, 0.0, 1.0)).rotation_difference(rot[i]).to_euler()
                if ('X' in self.prop_rot):
                    bpy.context.active_object.rotation_euler[0] = rot_diff[0]
                if ('Y' in self.prop_rot):
                    bpy.context.active_object.rotation_euler[1] = rot_diff[1]
                if ('Z' in self.prop_rot):
                    bpy.context.active_object.rotation_euler[2] = rot_diff[2]
                temp = eval(self.prop_obj_array)
                temp.append(bpy.context.active_object)
                self.prop_obj_array = repr(temp)
                if (self.inputs["Type"].default_value == 'RAND'):
                    self.inputs["Scatter Object"].execute(True)
    
    def post_execute(self):
        out = super().post_execute()
        out["Scattered Objects"] = self.prop_obj_array
        return out