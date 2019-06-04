print("______________________________________________________")
bl_info = {
    "name": "Sorcar",
    "author": "Punya Aachman",
    "version": (2, 0, 1),
    "blender": (2, 79, 0),
    "location": "Node Editor",
    "description": "Create procedural meshes using Node Editor",
    "category": "Node"}

import bpy
import bmesh
import nodeitems_utils
import random
import requests

from bpy.types import NodeTree, Node, NodeSocket, Operator
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty, StringProperty, FloatVectorProperty, PointerProperty, BoolVectorProperty
from nodeitems_utils import NodeCategory, NodeItem

######################### ADDON UPDATER ######################
class ScPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    prop_addon_location = StringProperty(name="Addon Location", default=bpy.utils.user_resource('SCRIPTS', "addons/") + __name__ + "/__init__.py") # Contributed by @kabu & @Poulpator

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prop_addon_location")
        layout.operator("sc.addon_updater")
class ScAddonUpdater(Operator):
    bl_idname = "sc.addon_updater"
    bl_label = "Update Sorcar"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        user_prefs = context.user_preferences
        addon_prefs = user_prefs.addons[__name__].preferences
        print("DEBUG: Sorcar: Fetching data...")
        r = requests.get("https://raw.githubusercontent.com/aachman98/Sorcar/master/__init__.py")
        print("DEBUG: Sorcar: Data Fetched! Writing data...")
        f = open(addon_prefs.prop_addon_location, 'w', encoding="utf8")
        f.write(r.text)
        print("DEBUG: Sorcar: Data Written! Addon successfully updated.")
        f.close()
        return {'FINISHED'}
##############################################################


########################## NODE-TREE #########################
class ScNodeTree(NodeTree):
    bl_idname = 'ScNodeTree'
    bl_label = 'Sorcar'
    bl_icon = 'MESH_CUBE'

    def update(self):
        for link in self.links:
            if not (link.from_socket.rna_type == link.to_socket.rna_type or link.from_socket.rna_type.name in link.to_socket.friends or link.to_socket.rna_type.name in link.from_socket.friends):
                self.links.remove(link)
class ScNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ScNodeTree'
##############################################################


########################### SOCKETS ##########################
# Socket base class
class ScNodeSocket:
    prop_prop = StringProperty(default="prop_dummy")
    color = (1.0, 1.0, 1.0, 1.0)
    mirror_prop = True
    friends = []
    def draw_color(self, context, node):
        return self.color
    def draw(self, context, layout, node, text):
        if (not self.is_output) and (not self.is_linked) and (self.mirror_prop):
            layout.prop(node, self.prop_prop, text=self.name)
        else:
            layout.label(self.name)
    def execute(self):
        if (self.is_output):
            return self.node.execute()
            # self.node.execute()
            # return eval("self.node." + self.prop_prop)
        elif (self.is_linked):
            return self.links[0].from_socket.execute()
        elif (self.mirror_prop):
            return eval("self.node." + self.prop_prop)
        else:
            return None
# Socket types
class ScMeshSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScMeshSocket"
    bl_label = "Mesh"
    color = (1.0, 1.0, 1.0, 1.0)
    mirror_prop = False
class ScMeshRefSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScMeshRefSocket"
    bl_label = "Mesh Reference"
    color = (1.0, 1.0, 1.0, 1.0)
    friends = ["ScMeshSocket"]
class ScComponentSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScComponentSocket"
    bl_label = "Component"
    color = (0.0, 0.0, 0.0, 1.0)
    mirror_prop = False
class ScObjectSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScObjectSocket"
    bl_label = "Object"
    color = (0.5, 0.5, 0.5, 1.0)
    mirror_prop = False
    friends = ["ScMeshSocket", "ScComponentSocket", "ScMeshRefSocket"]
class ScBoolSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScBoolSocket"
    bl_label = "Boolean"
    color = (1.0, 0.0, 0.0, 1.0)
class ScIntSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScIntSocket"
    bl_label = "Integer"
    color = (0.0, 0.7, 1.0, 1.0)
class ScFloatSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScFloatSocket"
    bl_label = "Float"
    color = (0.0, 1.0, 0.0, 1.0)
class ScFloatVectorSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScFloatVectorSocket"
    bl_label = "Float Vector"
    color = (1.0, 1.0, 0.0, 1.0)
class ScAngleSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScAngleSocket"
    bl_label = "Angle"
    color = (0.0, 0.0, 0.5, 1.0)
    friends = ["ScFloatSocket"]
class ScAngleVectorSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScAngleVectorSocket"
    bl_label = "Angle Vector"
    color = (0.3, 0.3, 1.0, 1.0)
    friends = ["ScFloatVectorSocket"]
class ScStringSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScStringSocket"
    bl_label = "String"
    color = (1.0, 0.0, 1.0, 1.0)
class ScUniversalSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScUniversalSocket"
    bl_label = "Universal"
    color = (1.0, 1.0, 1.0, 0.0)
    mirror_prop = False
    friends = ["ScMeshSocket", "ScComponentSocket", "ScObjectSocket", "ScBoolSocket", "ScIntSocket", "ScFloatSocket", "ScFloatVectorSocket", "ScAngleSocket", "ScAngleVectorSocket", "ScStringSocket"]
class ScInfoSocket(NodeSocket, ScNodeSocket):
    bl_idname = "ScInfoSocket"
    bl_label = "Info"
    color = (1.0, 0.5, 0.5, 1.0)
    mirror_prop = False
##############################################################


########################## CATEGORIES ########################
# Node base class
class ScNode:
    first_time = BoolProperty(default=True)
    node_color = (1, 1, 1)
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ScNodeTree'
    def update_value(self, context):
        bpy.ops.sc.execute_node_op()
        return None
    def init(self, context):
        self.hide = True
        self.use_custom_color = True
        self.color = self.node_color
    def override(self, mesh=False, edit=False):
        window = bpy.data.window_managers['WinMan'].windows[0]
        screen = window.screen
        area = [i for i in screen.areas if i.type == 'VIEW_3D'][0]
        space = area.spaces[0]
        scene = bpy.data.scenes[0]
        region = [i for i in area.regions if i.type == 'WINDOW'][0]
        ret = {'window':window, 'screen':screen, 'area': area, 'space':space, 'scene':scene, 'region':region, 'gpencil_data':bpy.context.gpencil_data}
        if (mesh):
            try:
                ret['active_object'] = self.mesh
                if (edit):
                    ret['edit_object'] = self.mesh
            except:
                print("DEBUG: " + self.name + ": Override: No mesh input")
        return ret
    def draw_buttons(self, context, layout):
        # Draw non-socket attributes
        pass
    def pre_execute(self):
        # Condition check, setting up environment, overrides, ...
        return True
    def post_execute(self):
        # Reset environment, change active object, ...
        pass
    def execute(self):
        if not self.pre_execute():
            return None
        self.functionality()
        ret_data = self.post_execute()
        if (self.first_time):
            self.first_time = False
        return ret_data
    def functionality(self):
        # Main functionality of the node using props_... & self.inputs["..."]
        pass
# Node categories
class ScInputNode(ScNode):
    node_color = (0.5, 0.0, 0.0)

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.outputs.new("ScMeshSocket", "Mesh")
        super().init(context)

    def pre_execute(self):
        if (not self.mesh == None):
            try:
                bpy.data.meshes.remove(bpy.data.meshes[self.mesh.name])
                bpy.data.objects.remove(self.mesh)
            except:
                print("DEBUG: " + self.name + ": Mesh object non-existant")
        if ((not bpy.context.active_object == None) and (not bpy.context.active_object.mode == "OBJECT")):
            bpy.ops.object.mode_set(mode="OBJECT")
        return True
    
    def post_execute(self):
        self.mesh = bpy.context.active_object
        return self.mesh
class ScTransformNode(ScNode):
    node_color = (0.0, 0.5, 0.0)

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScObjectSocket", "Object").prop_prop = "mesh"
        self.outputs.new("ScObjectSocket", "Object")
        self.inputs.move(len(self.inputs)-1, 0)
        super().init(context)

    def pre_execute(self):
        self.mesh = self.inputs["Object"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        bpy.context.scene.objects.active = self.mesh
        return True
    
    def post_execute(self):
        return self.mesh
class ScModifierNode(ScNode):
    node_color = (0.0, 0.0, 0.5)

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScMeshSocket", "Mesh").prop_prop = "mesh"
        self.outputs.new("ScMeshSocket", "Mesh")
        self.inputs.move(len(self.inputs)-1, 0)
        super().init(context)

    def pre_execute(self):
        self.mesh = self.inputs["Mesh"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        bpy.context.scene.objects.active = self.mesh
        return True
    
    def post_execute(self):
        bpy.ops.object.modifier_apply(modifier=self.mesh.modifiers[0].name)
        return self.mesh
class ScConversionNode(ScNode):
    node_color = (0.0, 0.5, 0.5)

    mesh = PointerProperty(type=bpy.types.Object)

    def pre_execute(self):
        self.mesh = self.inputs[0].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        bpy.context.scene.objects.active = self.mesh
        return True
    
    def post_execute(self):
        return self.mesh
class ScSelectionNode(ScNode):
    node_color = (0.5, 0.0, 0.5)

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScComponentSocket", "Component").prop_prop = "mesh"
        self.outputs.new("ScComponentSocket", "Component")
        self.inputs.move(len(self.inputs)-1, 0)
        super().init(context)
    
    def pre_execute(self):
        self.mesh = self.inputs["Component"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        return True
    
    def post_execute(self):
        return self.mesh
class ScDeletionNode(ScNode):
    node_color = (0.5, 0.5, 0.0)

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScComponentSocket", "Component").prop_prop = "mesh"
        self.outputs.new("ScComponentSocket", "Component")
        self.inputs.move(len(self.inputs)-1, 0)
        super().init(context)
    
    def pre_execute(self):
        self.mesh = self.inputs["Component"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        return True
    
    def post_execute(self):
        return self.mesh
class ScEditOperatorNode(ScNode):
    node_color = (0.5, 0.5, 0.5)

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScComponentSocket", "Component").prop_prop = "mesh"
        self.outputs.new("ScComponentSocket", "Component")
        self.inputs.move(len(self.inputs)-1, 0)
        super().init(context)
    
    def pre_execute(self):
        self.mesh = self.inputs["Component"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        return True
    
    def post_execute(self):
        return self.mesh
class ScObjectOperatorNode(ScNode):
    node_color = (0.3, 0.7, 0.0)

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScMeshSocket", "Mesh").prop_prop = "mesh"
        self.outputs.new("ScMeshSocket", "Mesh")
        self.inputs.move(len(self.inputs)-1, 0)
        super().init(context)
    
    def pre_execute(self):
        self.mesh = self.inputs["Mesh"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        return True
    
    def post_execute(self):
        return self.mesh
class ScConstantNode(ScNode):
    node_color = (0.3, 0.0, 0.7)

    def init(self, context):
        self.use_custom_color = True
        self.color = self.node_color
class ScUtilityNode(ScNode):
    node_color = (0.7, 0.3, 0.0)
class ScControlNode(ScNode):
    node_color = (0.0, 0.3, 0.7)
class ScSettingNode(ScNode):
    node_color = (0.7, 0.0, 0.3)

    def init(self, context):
        self.inputs.new("ScUniversalSocket", "")
        self.outputs.new("ScUniversalSocket", "")
        self.inputs.move(len(self.inputs)-1, 0)
        super().init(context)
    
    def post_execute(self):
        return self.inputs[0].execute()
class ScOutputNode(ScNode):
    node_color = (0.0, 0.7, 0.3)

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScMeshSocket", "Mesh")
        self.inputs.move(len(self.inputs)-1, 0)
        self.use_custom_color = True
        self.color = self.node_color

    def pre_execute(self):
        self.mesh = self.inputs["Mesh"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        return True
    
    def post_execute(self):
        return self.mesh
##############################################################


######################### HELPER OPS #########################
class ScRealtimeMeshOp(Operator):
    bl_idname = "sc.realtime_mesh_op"
    bl_label = "Realtime Mesh Update"
    bl_options = {"REGISTER", "UNDO"}

    node = None

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR"

    def execute(self, context):
        bpy.ops.sc.execute_node_op()
        return {'FINISHED'}

    def modal(self, context, event):
        if (event.type == "ESC"):
            print("DEBUG: ScRealtimeMeshOp: STOP")
            return {'FINISHED'}
        elif (event.type == "LEFTMOUSE"):
            try:
                node = context.active_node
            except:
                return {'PASS_THROUGH'}
            if (not node == self.node):
                print("DEBUG: ScRealtimeMeshOp: Active node changed")
                self.node = node
                self.execute(context)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        print("DEBUG: ScRealtimeMeshOp: START")
        return {'RUNNING_MODAL'}
class ScSaveSelectionOp(Operator):
    bl_idname = "sc.save_selection_op"
    bl_label = "Execute MeshNode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR"
    
    def execute(self, context):
        node = context.active_node
        if (node == None):
            print("DEBUG: ScSaveSelectionOp: No Active Node")
            return {'CANCELLED'}
        node.save_selection()
        return {'FINISHED'}
class ScExecuteNodeOp(Operator):
    bl_idname = "sc.execute_node_op"
    bl_label = "Execute Node"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR"

    def execute(self, context):
        node = context.active_node
        if (not node == None):
            print("--- EXECUTE NODE: " + node.name + " ---")
            for group in bpy.data.node_groups:
                for node in group.nodes:
                    try:
                        node.first_time = True
                        node.last_time = False
                    except:
                        print("DEBUG: " + node.name + ": Not a Loop node")
            node.execute()
            return {'FINISHED'}
        print("DEBUG: ScExecuteNodeOp: No active node")
        return {'CANCELLED'}
def toList(string):
        string = string.replace("[", "")
        string = string.replace("]", "")
        list_string = string.rsplit(", ")
        if (not list_string == [""]):
            return [int(i) for i in list_string]
        return []
##############################################################


########################### NODES ############################
# Inputs
class PlaneNode(Node, ScInputNode):
    bl_idname = "PlaneNode"
    bl_label = "Plane"
    
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0, update=ScNode.update_value)
    
    def init(self, context):
        self.inputs.new("ScFloatSocket", "Radius").prop_prop = "prop_radius"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.primitive_plane_add(radius=self.inputs["Radius"].execute())
class CubeNode(Node, ScInputNode):
    bl_idname = "CubeNode"
    bl_label = "Cube"
    
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Radius").prop_prop = "prop_radius"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.primitive_cube_add(radius=self.inputs["Radius"].execute())
class CircleNode(Node, ScInputNode):
    bl_idname = "CircleNode"
    bl_label = "Circle"
    
    prop_vertices = IntProperty(name="Vertices", default=32, min=3, max=1000000, update=ScNode.update_value)
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0, update=ScNode.update_value)
    prop_end = EnumProperty(name="Fill Type", items=[("NOTHING", "Nothing", "Don’t fill at all."), ("NGON", "Ngon", "Use ngons"), ("TRIFAN", "Triangle Fan", "Use triangle fans.")], default="NOTHING", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Vertices").prop_prop = "prop_vertices"
        self.inputs.new("ScFloatSocket", "Radius").prop_prop = "prop_radius"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_end")
    
    def functionality(self):
        bpy.ops.mesh.primitive_circle_add(vertices=self.inputs["Vertices"].execute(), radius=self.inputs["Radius"].execute(), fill_type=self.prop_end)
class UVSphereNode(Node, ScInputNode):
    bl_idname = "UVSphereNode"
    bl_label = "UV Sphere"
    
    prop_segments = IntProperty(name="Segments", default=32, min=3, max=10000, update=ScNode.update_value)
    prop_rings = IntProperty(name="Ring Count", default=16, min=3, max=10000, update=ScNode.update_value)
    prop_size = FloatProperty(name="Size", default=1.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Segments").prop_prop = "prop_segments"
        self.inputs.new("ScIntSocket", "Rings").prop_prop = "prop_rings"
        self.inputs.new("ScFloatSocket", "Size").prop_prop = "prop_size"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=self.inputs["Segments"].execute(), ring_count=self.inputs["Rings"].execute(), size=self.inputs["Size"].execute())
class IcoSphereNode(Node, ScInputNode):
    bl_idname = "IcoSphereNode"
    bl_label = "Ico Sphere"
    
    prop_subdivisions = IntProperty(name="Subdivisions", default=2, min=1, max=10, update=ScNode.update_value)
    prop_size = FloatProperty(name="Size", default=1.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Subdivisions").prop_prop = "prop_subdivisions"
        self.inputs.new("ScFloatSocket", "Size").prop_prop = "prop_size"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=self.inputs["Subdivisions"].execute(), size=self.inputs["Size"].execute())
class CylinderNode(Node, ScInputNode):
    bl_idname = "CylinderNode"
    bl_label = "Cylinder"
    
    prop_vertices = IntProperty(name="Vertices", default=32, min=3, max=1000000, update=ScNode.update_value)
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0, update=ScNode.update_value)
    prop_depth = FloatProperty(name="Depth", default=2.0, min=0, update=ScNode.update_value)
    prop_end = EnumProperty(name="End Fill Type", items=[("NOTHING", "Nothing", "Don’t fill at all."), ("NGON", "Ngon", "Use ngons"), ("TRIFAN", "Triangle Fan", "Use triangle fans.")], default="NGON", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Vertices").prop_prop = "prop_vertices"
        self.inputs.new("ScFloatSocket", "Radius").prop_prop = "prop_radius"
        self.inputs.new("ScFloatSocket", "Depth").prop_prop = "prop_depth"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_end")

    def functionality(self):
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.inputs["Vertices"].execute(), radius=self.inputs["Radius"].execute(), depth=self.inputs["Depth"].execute(), end_fill_type=self.prop_end)
class ConeNode(Node, ScInputNode):
    bl_idname = "ConeNode"
    bl_label = "Cone"
    
    prop_vertices = IntProperty(name="Vertices", default=32, min=3, max=1000000, update=ScNode.update_value)
    prop_radius1 = FloatProperty(name="Radius 1", default=1.0, min=0.0, update=ScNode.update_value)
    prop_radius2 = FloatProperty(name="Radius 2", default=0.0, min=0.0, update=ScNode.update_value)
    prop_depth = FloatProperty(name="Depth", default=2.0, min=0, update=ScNode.update_value)
    prop_end = EnumProperty(name="End Fill Type", items=[("NOTHING", "Nothing", "Don’t fill at all."), ("NGON", "Ngon", "Use ngons"), ("TRIFAN", "Triangle Fan", "Use triangle fans.")], default="NGON", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Vertices").prop_prop = "prop_vertices"
        self.inputs.new("ScFloatSocket", "Radius 1").prop_prop = "prop_radius1"
        self.inputs.new("ScFloatSocket", "Radius 2").prop_prop = "prop_radius2"
        self.inputs.new("ScFloatSocket", "Depth").prop_prop = "prop_depth"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_end")
    
    def functionality(self):
        bpy.ops.mesh.primitive_cone_add(vertices=self.inputs["Vertices"].execute(), radius1=self.inputs["Radius 1"].execute(), radius2=self.inputs["Radius 2"].execute(), depth=self.inputs["Depth"].execute(), end_fill_type=self.prop_end)
# class TorusNode(Node, ScInputNode):
#     bl_idname = "TorusNode"
#     bl_label = "Torus"
    
#     prop_major_segments = IntProperty(name="Major Segment", default=48, min=3, max=256, update=ScNode.update_value)
#     prop_minor_segments = IntProperty(name="Minor Segment", default=12, min=3, max=256, update=ScNode.update_value)
#     prop_mode = EnumProperty(name="Mode", items=[("MAJOR_MINOR", "Major/Minor", "Use the major/minor radii for torus dimensions."), ("EXT_INT", "Exterior/Interior", "Use the exterior/interior radii for torus dimensions.")], default="MAJOR_MINOR", update=ScNode.update_value)
#     prop_major_radius = FloatProperty(name="Major Radius", default=1.0, min=0.01, max=100, update=ScNode.update_value)
#     prop_minor_radius = FloatProperty(name="Minor Radius", default=0.25, min=0.01, max=100, update=ScNode.update_value)
#     prop_ext_radius = FloatProperty(name="Exterior Radius", default=1.25, min=0.01, max=100, update=ScNode.update_value)
#     prop_int_radius = FloatProperty(name="Interior Radius", default=0.75, min=0.01, max=100, update=ScNode.update_value)
    
#     def draw_buttons(self, context, layout):
#         layout.column().prop(self, "prop_major_segments")
#         layout.column().prop(self, "prop_minor_segments")
#         layout.column().prop(self, "prop_mode")
#         if (self.prop_mode == "MAJOR_MINOR"):
#             layout.column().prop(self, "prop_major_radius")
#             layout.column().prop(self, "prop_minor_radius")
#         else:
#             layout.column().prop(self, "prop_ext_radius")
#             layout.column().prop(self, "prop_int_radius")
    
#     def functionality(self, loc, rot):
#         bpy.ops.mesh.primitive_torus_add(major_segments=self.prop_major_segments, minor_segments=self.prop_minor_segments, mode=self.prop_mode, major_radius = self.prop_major_radius, minor_radius = self.prop_minor_radius, abso_major_rad = self.prop_ext_radius, abso_minor_rad = self.prop_int_radius, location=loc, rotation=rot)
class GridNode(Node, ScInputNode):
    bl_idname = "GridNode"
    bl_label = "Grid"
    
    prop_x = IntProperty(name="X Subdivisions", default=10, min=2, max=10000000, update=ScNode.update_value)
    prop_y = IntProperty(name="Y Subdivisions", default=10, min=2, max=10000000, update=ScNode.update_value)
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "X Subdivisions").prop_prop = "prop_x"
        self.inputs.new("ScIntSocket", "Y Subdivisions").prop_prop = "prop_y"
        self.inputs.new("ScFloatSocket", "Radius").prop_prop = "prop_radius"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=self.inputs["X Subdivisions"].execute(), y_subdivisions=self.inputs["Y Subdivisions"].execute(), radius=self.inputs["Radius"].execute())
class SuzanneNode(Node, ScInputNode):
    bl_idname = "SuzanneNode"
    bl_label = "Suzanne (Monkey)"
    
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Radius").prop_prop = "prop_radius"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.primitive_monkey_add(radius=self.inputs["Radius"].execute())
class CustomMeshNode(Node, ScInputNode):
    bl_idname = "CustomMeshNode"
    bl_label = "Custom Mesh"
    
    prop_mesh = PointerProperty(name="Mesh", type=bpy.types.Object, update=ScNode.update_value)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_mesh")
    
    def pre_execute(self):
        if (self.prop_mesh == None):
            print("DEBUG: " + self.name + ": No mesh selected")
            return False
        return super().pre_execute()
    
    def functionality(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = self.prop_mesh
        self.prop_mesh.select = True
        bpy.ops.object.duplicate()
# Transform
class LocationNode(Node, ScTransformNode):
    bl_idname = "LocationNode"
    bl_label = "Set Location"
    
    prop_location = FloatVectorProperty(name="Location", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatVectorSocket", "Location").prop_prop = "prop_location"
        super().init(context)
    
    def functionality(self):
        self.mesh.location = self.inputs["Location"].execute()
class RotationNode(Node, ScTransformNode):
    bl_idname = "RotationNode"
    bl_label = "Set Rotation"
    
    prop_rotation = FloatVectorProperty(name="Rotation", subtype="EULER", unit="ROTATION", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScAngleVectorSocket", "Rotation").prop_prop = "prop_rotation"
        super().init(context)
    
    def functionality(self):
        self.mesh.rotation_euler = self.inputs["Rotation"].execute()
class ScaleNode(Node, ScTransformNode):
    bl_idname = "ScaleNode"
    bl_label = "Set Scale"
    
    prop_scale = FloatVectorProperty(name="Scale", default=(1.0, 1.0, 1.0), update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatVectorSocket", "Scale").prop_prop = "prop_scale"
        super().init(context)
    
    def functionality(self):
        self.mesh.scale = self.inputs["Scale"].execute()
class TranslateNode(Node, ScTransformNode):
    bl_idname = "TranslateNode"
    bl_label = "Translate"

    prop_value = FloatVectorProperty(name="Value", update=ScNode.update_value)
    prop_constraint_axis = BoolVectorProperty(name="Constraint Axis", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatVectorSocket", "Value").prop_prop = "prop_value"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_constraint_axis")

    def functionality(self):
        bpy.ops.transform.translate(self.override(), value=self.inputs["Value"].execute(), constraint_axis=self.prop_constraint_axis, constraint_orientation=self.override()["space"].transform_orientation)
class RotateNode(Node, ScTransformNode):
    bl_idname = "RotateNode"
    bl_label = "Rotate"

    prop_value = FloatProperty(name="Value", subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    prop_constraint_axis = EnumProperty(name="Constraint Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScAngleSocket", "Value").prop_prop = "prop_value"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_constraint_axis", expand=True)
    
    def functionality(self):
        bpy.ops.transform.rotate(self.override(), value=self.inputs["Value"].execute(), axis=(1.0, 1.0, 1.0), constraint_axis=(self.prop_constraint_axis=="X", self.prop_constraint_axis=="Y", self.prop_constraint_axis=="Z"))
class ResizeNode(Node, ScTransformNode):
    bl_idname = "ResizeNode"
    bl_label = "Resize"

    prop_value = FloatVectorProperty(name="Value", default=(1.0, 1.0, 1.0), update=ScNode.update_value)
    prop_constraint_axis = BoolVectorProperty(name="Constraint Axis", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatVectorSocket", "Value").prop_prop = "prop_value"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_constraint_axis")
    
    def functionality(self):
        bpy.ops.transform.resize(self.override(), value=self.inputs["Value"].execute(), constraint_axis=self.prop_constraint_axis, constraint_orientation=self.override()["space"].transform_orientation)
# Modifiers
class ArrayModNode(Node, ScModifierNode):
    bl_idname = "ArrayModNode"
    bl_label = "Array Modifier"

    fit_type = EnumProperty(name="Fit Type", items=[("FIXED_COUNT", "Fixed Count", ""), ("FIT_LENGTH", "Fit Length", ""), ("FIT_CURVE", "Fit Curve", "")], default="FIXED_COUNT", update=ScNode.update_value)
    count = IntProperty(name="Count", default=2, min=1, max=1000, update=ScNode.update_value)
    fit_length = FloatProperty(name="Length", default=0.0, min=0.0, update=ScNode.update_value)
    curve = PointerProperty(name="Curve", type=bpy.types.Object, update=ScNode.update_value)
    use_constant_offset = BoolProperty(name="Constant Offset", update=ScNode.update_value)
    constant_offset_displace = FloatVectorProperty(name="Offset", update=ScNode.update_value)
    use_merge_vertices = BoolProperty(name="Merge Vertices", update=ScNode.update_value)
    use_merge_vertices_cap = BoolProperty(name="Cap", update=ScNode.update_value)
    merge_threshold = FloatProperty(name="Threshold", default=0.01, min=0.0, max=1.0, update=ScNode.update_value)
    use_relative_offset = BoolProperty(name="Use Relative Offset", default=True, update=ScNode.update_value)
    relative_offset_displace = FloatVectorProperty(name="Relative Offset", default=(1.0, 0.0, 0.0), update=ScNode.update_value)
    use_object_offset = BoolProperty(name="Object Offset", update=ScNode.update_value)
    offset_object = PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    start_cap = PointerProperty(name="Start Cap", type=bpy.types.Object, update=ScNode.update_value)
    end_cap = PointerProperty(name="End Cap", type=bpy.types.Object, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Count").prop_prop = "count"
        self.inputs.new("ScFloatSocket", "Length").prop_prop = "fit_length"
        self.inputs.new("ScBoolSocket", "Use Constant Offset").prop_prop = "use_constant_offset"
        self.inputs.new("ScFloatVectorSocket", "Constant Offset").prop_prop = "constant_offset_displace"
        self.inputs.new("ScBoolSocket", "Use Relative Offset").prop_prop = "use_relative_offset"
        self.inputs.new("ScFloatVectorSocket", "Relative Offset").prop_prop = "relative_offset_displace"
        self.inputs.new("ScBoolSocket", "Use Object Offset").prop_prop = "use_object_offset"
        self.inputs.new("ScMeshRefSocket", "Object Offset").prop_prop = "offset_object"
        self.inputs.new("ScBoolSocket", "Merge").prop_prop = "use_merge_vertices"
        self.inputs.new("ScBoolSocket", "First Last").prop_prop = "use_merge_vertices_cap"
        self.inputs.new("ScFloatSocket", "Distance").prop_prop = "merge_threshold"
        self.inputs.new("ScMeshRefSocket", "End Cap").prop_prop = "start_cap"
        self.inputs.new("ScMeshRefSocket", "Start Cap").prop_prop = "end_cap"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "fit_type")
        if self.fit_type == 'FIT_CURVE':
            layout.prop(self, "curve")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="ARRAY")
        self.mesh.modifiers[0].fit_type = self.fit_type
        self.mesh.modifiers[0].count = self.inputs["Count"].execute()
        self.mesh.modifiers[0].fit_length = self.inputs["Length"].execute()
        self.mesh.modifiers[0].curve = self.curve
        self.mesh.modifiers[0].use_constant_offset = self.inputs["Use Constant Offset"].execute()
        self.mesh.modifiers[0].constant_offset_displace = self.inputs["Constant Offset"].execute()
        self.mesh.modifiers[0].use_merge_vertices = self.inputs["Merge"].execute()
        self.mesh.modifiers[0].use_merge_vertices_cap = self.inputs["First Last"].execute()
        self.mesh.modifiers[0].merge_threshold = self.inputs["Distance"].execute()
        self.mesh.modifiers[0].use_relative_offset = self.inputs["Use Relative Offset"].execute()
        self.mesh.modifiers[0].relative_offset_displace = self.inputs["Relative Offset"].execute()
        self.mesh.modifiers[0].use_object_offset = self.inputs["Use Object Offset"].execute()
        self.mesh.modifiers[0].offset_object = self.inputs["Object Offset"].execute()
        self.mesh.modifiers[0].start_cap = self.inputs["Start Cap"].execute()
        self.mesh.modifiers[0].end_cap = self.inputs["End Cap"].execute()
class BevelModNode(Node, ScModifierNode):
    bl_idname = "BevelModNode"
    bl_label = "Bevel Modifier"
    
    width = FloatProperty(name="Width", default=0.1, min=0.0, update=ScNode.update_value)
    segments = IntProperty(name="Segments", default=1, min=0, max=100, update=ScNode.update_value)
    profile = FloatProperty(name="Profile", default=0.5, min=0.0, max=1.0, update=ScNode.update_value)
    material = IntProperty(name="Material", default=-1, min=0, max=32767, update=ScNode.update_value)
    use_only_vertices = BoolProperty(name="Only Vertices", update=ScNode.update_value)
    use_clamp_overlap = BoolProperty(name="Clamp Overlap", default=True, update=ScNode.update_value)
    loop_slide = BoolProperty(name="Loop Slide", default=True, update=ScNode.update_value)
    limit_method = EnumProperty(name="Limit Method", items=[("NONE", "None", ""), ("ANGLE", "Angle", ""), ("WEIGHT", "Weight", "")], default="NONE", update=ScNode.update_value)
    angle_limit = FloatProperty(name="Angle", default=0.523599, min=0.0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    offset_type = EnumProperty(name="Limit Method", items=[("OFFSET", "Offset", ""), ("WIDTH", "Width", ""), ("DEPTH", "Depth", ""), ("PERCENT", "Percent", "")], default="OFFSET", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Width").prop_prop = "width"
        self.inputs.new("ScIntSocket", "Segments").prop_prop = "segments"
        self.inputs.new("ScFloatSocket", "Profile").prop_prop = "profile"
        self.inputs.new("ScBoolSocket", "Only Vertices").prop_prop = "use_only_vertices"
        super().init(context)

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, "material")
        col.prop(self, "use_clamp_overlap")
        col.prop(self, "loop_slide")
        layout.label(text="Limit Method:")
        layout.row().prop(self, "limit_method", expand=True)
        if self.limit_method == 'ANGLE':
            layout.prop(self, "angle_limit")
        layout.label(text="Width Method:")
        layout.row().prop(self, "offset_type", expand=True)
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="BEVEL")
        self.mesh.modifiers[0].width = self.inputs["Width"].execute()
        self.mesh.modifiers[0].segments = self.inputs["Segments"].execute()
        self.mesh.modifiers[0].profile = self.inputs["Profile"].execute()
        self.mesh.modifiers[0].material = self.material
        self.mesh.modifiers[0].use_only_vertices = self.inputs["Only Vertices"].execute()
        self.mesh.modifiers[0].use_clamp_overlap = self.use_clamp_overlap
        self.mesh.modifiers[0].loop_slide = self.loop_slide
        self.mesh.modifiers[0].limit_method = self.limit_method
        self.mesh.modifiers[0].angle_limit = self.angle_limit
        self.mesh.modifiers[0].offset_type = self.offset_type
class BooleanModNode(Node, ScModifierNode):
    bl_idname = "BooleanModNode"
    bl_label = "Boolean Modifier"
    
    prop_op = EnumProperty(name="Operation", items=[("DIFFERENCE", "Difference", ""), ("UNION", "Union", ""), ("INTERSECT", "Intersect", "")], default="INTERSECT", update=ScNode.update_value)
    prop_obj = PointerProperty(name="Object", type=bpy.types.Object)
    prop_overlap = FloatProperty(name="Overlap Threshold", default=0.000001, min=0.0, max=1.0, precision=6, update=ScNode.update_value)
    prop_draw_mode = EnumProperty(items=[("SOLID", "Solid", ""), ("WIRE", "Wire", ""), ("BOUNDS", "Bounds", "")], default="WIRE", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScMeshSocket", "Object").prop_prop = "prop_obj"
        self.inputs.new("ScFloatSocket", "Overlap").prop_prop = "prop_overlap"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_op")
        layout.label("Set Secondary Object Display Mode:")
        layout.prop(self, "prop_draw_mode", expand=True)
    
    def pre_execute(self):
        self.prop_obj = self.inputs["Object"].execute()
        if (self.prop_obj == None):
            print("DEBUG: " + self.name + ": Empty secondary object recieved")
            return False
        return super().pre_execute()
    
    def functionality(self):
        self.mesh.select = True
        self.prop_obj.select = False
        bpy.ops.object.modifier_add(type="BOOLEAN")
        self.mesh.modifiers[0].operation = self.prop_op
        self.mesh.modifiers[0].object = self.prop_obj
        self.mesh.modifiers[0].double_threshold = self.inputs["Overlap"].execute()
        self.prop_obj.draw_type = self.prop_draw_mode
class CastModNode(Node, ScModifierNode):
    bl_idname = "CastModNode"
    bl_label = "Cast Modifier"

    cast_type = EnumProperty(items=[("SPHERE", "Sphere", ""), ("CYLINDER", "Cylinder", ""), ("CUBOID", "Cuboid", "")], update=ScNode.update_value)
    use_x = BoolProperty(name="X", default=True, update=ScNode.update_value)
    use_y = BoolProperty(name="Y", default=True, update=ScNode.update_value)
    use_z = BoolProperty(name="Z", default=True, update=ScNode.update_value)
    factor = FloatProperty(name="Factor", default=0.5, update=ScNode.update_value)
    radius = FloatProperty(name="Radius", default=0.0, min=0.0, update=ScNode.update_value)
    size = FloatProperty(name="Size", default=0.0, min=0.0, update=ScNode.update_value)
    use_radius_as_size = BoolProperty(name="From Radius", default=True, update=ScNode.update_value)
    vertex_group = StringProperty(name="Vertex Group", update=ScNode.update_value)
    object = PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    use_transform = BoolProperty(name="Use transform", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "factor"
        self.inputs.new("ScFloatSocket", "Radius").prop_prop = "radius"
        self.inputs.new("ScFloatSocket", "Size").prop_prop = "size"
        self.inputs.new("ScBoolSocket", "From Radius").prop_prop = "use_radius_as_size"
        self.inputs.new("ScBoolSocket", "X").prop_prop = "use_x"
        self.inputs.new("ScBoolSocket", "Y").prop_prop = "use_y"
        self.inputs.new("ScBoolSocket", "Z").prop_prop = "use_z"
        self.inputs.new("ScMeshRefSocket", "Control Object").prop_prop = "object"
        self.inputs.new("ScBoolSocket", "Use Transform").prop_prop = "use_transform"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.label(text="Cast Type:")
        layout.prop(self, "cast_type", text="")
        if (not self.mesh == None):
            layout.label(text="Vertex Group:")
            layout.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="CAST")
        self.mesh.modifiers[0].cast_type = self.cast_type
        self.mesh.modifiers[0].use_x = self.inputs["X"].execute()
        self.mesh.modifiers[0].use_y = self.inputs["Y"].execute()
        self.mesh.modifiers[0].use_z = self.inputs["Z"].execute()
        self.mesh.modifiers[0].factor = self.inputs["Factor"].execute()
        self.mesh.modifiers[0].radius = self.inputs["Radius"].execute()
        self.mesh.modifiers[0].size = self.inputs["Size"].execute()
        self.mesh.modifiers[0].use_radius_as_size = self.inputs["From Radius"].execute()
        self.mesh.modifiers[0].vertex_group = self.vertex_group
        self.mesh.modifiers[0].object = self.inputs["Control Object"].execute()
        self.mesh.modifiers[0].use_transform = self.inputs["Use Transform"].execute()
class CorrectiveSmoothModNode(Node, ScModifierNode):
    bl_idname = "CorrectiveSmoothModNode"
    bl_label = "Corrective Smooth Modifier"
    
    factor = FloatProperty(default=0.5, soft_min=0.0, soft_max=1.0, update=ScNode.update_value)
    iterations = IntProperty(name="Repeat", default=5, min=-32768, max=32767, soft_min=0, soft_max=200, update=ScNode.update_value)
    smooth_type = EnumProperty(name="Smooth Type", items=[("SIMPLE", "Simple", ""), ("LENGTH_WEIGHTED", "Length Weight", "")], default="SIMPLE", update=ScNode.update_value)
    use_only_smooth = BoolProperty(name="Only Smooth", update=ScNode.update_value)
    use_pin_boundary = BoolProperty(name="Pin Boundaries", update=ScNode.update_value)
    vertex_group = StringProperty(name="Vertex Group", update=ScNode.update_value)
    invert_vertex_group = BoolProperty(update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "factor"
        self.inputs.new("ScIntSocket", "Repeat").prop_prop = "iterations"
        self.inputs.new("ScBoolSocket", "Only Smooth").prop_prop = "use_only_smooth"
        self.inputs.new("ScBoolSocket", "Pin Boundaries").prop_prop = "use_pin_boundary"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "smooth_type")
        if (not self.mesh == None):
            layout.label(text="Vertex Group:")
            split = layout.split()
            col = split.column()
            row = col.row(align=True)
            row.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
            row.prop(self, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="CORRECTIVE_SMOOTH")
        self.mesh.modifiers[0].factor = self.inputs["Factor"].execute()
        self.mesh.modifiers[0].iterations = self.inputs["Repeat"].execute()
        self.mesh.modifiers[0].smooth_type = self.smooth_type
        self.mesh.modifiers[0].use_only_smooth = self.inputs["Only Smooth"].execute()
        self.mesh.modifiers[0].use_pin_boundary = self.inputs["Pin Boundaries"].execute()
        self.mesh.modifiers[0].vertex_group = self.vertex_group
        self.mesh.modifiers[0].invert_vertex_group = self.invert_vertex_group
class CurveModNode(Node, ScModifierNode):
    bl_idname = "CurveModNode"
    bl_label = "Curve Modifier"
    
    vertex_group = StringProperty(name="Vertex Group", update=ScNode.update_value)
    object = PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    deform_axis = EnumProperty(items=[("POS_X", "X", ""), ("POS_Y", "Y", ""), ("POS_Z", "Z", ""), ("NEG_X", "-X", ""), ("NEG_Y", "-Y", ""), ("NEG_Z", "-Z", "")], default="POS_X", update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.label(text="Object:")
        layout.prop(self, "object", text="")
        if (not self.mesh == None):
            layout.label(text="Vertex Group:")
            layout.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
        layout.label(text="Deformation Axis:")
        layout.row().prop(self, "deform_axis", expand=True)
    
    def pre_execute(self):
        if (self.object == None):
            print("DEBUG: " + self.name + ": Empty curve object recieved")
            return False
        return super().pre_execute()
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="CURVE")
        self.mesh.modifiers[0].vertex_group = self.vertex_group
        self.mesh.modifiers[0].object = self.object
        self.mesh.modifiers[0].deform_axis = self.deform_axis
class DecimateModNode(Node, ScModifierNode):
    bl_idname = "DecimateModNode"
    bl_label = "Decimate Modifier"

    decimate_type = EnumProperty(items=[("COLLAPSE", "Collapse", ""), ("UNSUBDIV", "Un-Subdivide", ""), ("DISSOLVE", "Planar", "")], default="COLLAPSE", update=ScNode.update_value)
    vertex_group = StringProperty(update=ScNode.update_value)
    ratio = FloatProperty(name="Ratio", default=1.0, min=0.0, max=1.0, update=ScNode.update_value)
    invert_vertex_group = BoolProperty(update=ScNode.update_value)
    vertex_group_factor = FloatProperty(name="Factor", default=1.0, min=0, max=1000, soft_max=10, update=ScNode.update_value)
    use_collapse_triangulate = BoolProperty(name="Triangulate", update=ScNode.update_value)
    use_symmetry = BoolProperty(name="Symmetry", update=ScNode.update_value)
    symmetry_axis = EnumProperty(name="Symmetry", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X", update=ScNode.update_value)
    iterations = IntProperty(name="Iterations", default=0, min=0, max=32767, soft_max=100, update=ScNode.update_value)
    angle_limit = FloatProperty(name="Angle Limit", default=0.087266, min=0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    use_dissolve_boundaries = BoolProperty(name="All Boundaries", update=ScNode.update_value)
    delimit = EnumProperty(items=[("NORMAL", "Normal", "", 2), ("MATERIAL", "Material", "", 4), ("SEAM", "Seam", "", 8), ("SHARP", "Sharp", "", 16), ("UV", "UVs", "", 32)], default={"NORMAL"}, options={'ENUM_FLAG'}, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Ratio").prop_prop = "ratio"
        self.inputs.new("ScBoolSocket", "Triangulate").prop_prop = "use_collapse_triangulate"
        self.inputs.new("ScBoolSocket", "Symmetry").prop_prop = "use_symmetry"
        self.inputs.new("ScIntSocket", "Iterations").prop_prop = "iterations"
        self.inputs.new("ScAngleSocket", "Angle Limit").prop_prop = "angle_limit"
        self.inputs.new("ScBoolSocket", "All Boundaries").prop_prop = "use_dissolve_boundaries"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        decimate_type = self.decimate_type
        row = layout.row()
        row.prop(self, "decimate_type", expand=True)
        if decimate_type == 'COLLAPSE':
            has_vgroup = bool(self.vertex_group)
            col = layout.column()
            row = col.row(align=True)
            if (not self.mesh == None):
                row.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
                row.prop(self, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
            col = layout.column()
            row = col.row()
            row.active = has_vgroup
            row.prop(self, "vertex_group_factor")
            layout.prop(self, "symmetry_axis")
        elif decimate_type == 'DISSOLVE':
            layout.label("Delimit:")
            row = layout.row()
            row.prop(self, "delimit", expand=True)
        if (not self.mesh == None):
            layout.label(text="Faces: " + str(len(self.mesh.data.polygons)))
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="DECIMATE")
        self.mesh.modifiers[0].decimate_type = self.decimate_type
        self.mesh.modifiers[0].vertex_group = self.vertex_group
        self.mesh.modifiers[0].ratio = self.inputs["Ratio"].execute()
        self.mesh.modifiers[0].invert_vertex_group = self.invert_vertex_group
        self.mesh.modifiers[0].vertex_group_factor = self.vertex_group_factor
        self.mesh.modifiers[0].use_collapse_triangulate = self.inputs["Triangulate"].execute()
        self.mesh.modifiers[0].use_symmetry = self.inputs["Symmetry"].execute()
        self.mesh.modifiers[0].symmetry_axis = self.symmetry_axis
        self.mesh.modifiers[0].iterations = self.inputs["Iterations"].execute()
        self.mesh.modifiers[0].angle_limit = self.inputs["Angle Limit"].execute()
        self.mesh.modifiers[0].use_dissolve_boundaries = self.inputs["All Boundaries"].execute()
        self.mesh.modifiers[0].delimit = self.delimit
class DisplaceModNode(Node, ScModifierNode):
    bl_idname = "DisplaceModNode"
    bl_label = "Displace Modifier"

    texture = PointerProperty(type=bpy.types.Texture)
    direction = EnumProperty(items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""), ("NORMAL", "Normal", ""), ("CUSTOM_NORMAL", "Custom Normal", ""), ("RGB_TO_XYZ", "RGB to XYZ", "")], default="NORMAL", update=ScNode.update_value)
    space = EnumProperty(items=[("LOCAL", "Local", ""), ("GLOBAL", "Global", "")], default="LOCAL", update=ScNode.update_value)
    texture_coords = EnumProperty(items=[("LOCAL", "Local", ""), ("GLOBAL", "Global", ""), ("OBJECT", "Object", ""), ("UV", "UV", "")], default="LOCAL", update=ScNode.update_value)
    texture_coords_object = PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    vertex_group = StringProperty(update=ScNode.update_value)
    uv_layer = StringProperty(update=ScNode.update_value)
    mid_level = FloatProperty(name="Midlevel", default=0.5, soft_min=0.0, soft_max=1.0, update=ScNode.update_value)
    strength = FloatProperty(name="Strength", default=1.0, soft_min=-100.0, soft_max=100.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Midlevel").prop_prop = "mid_level"
        self.inputs.new("ScFloatSocket", "Strength").prop_prop = "strength"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        has_texture = (self.texture is not None)
        col = layout.column(align=True)
        col.label(text="Texture:")
        col.prop(self, "texture", text="")
        split = layout.split()
        col = split.column(align=True)
        col.label(text="Direction:")
        col.prop(self, "direction", text="")
        if self.direction in {'X', 'Y', 'Z', 'RGB_TO_XYZ'}:
            col.label(text="Space:")
            col.prop(self, "space", text="")
        col.label(text="Vertex Group:")
        if (not self.mesh == None):
            col.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
        col = split.column(align=True)
        col.active = has_texture
        col.label(text="Texture Coordinates:")
        col.prop(self, "texture_coords", text="")
        if self.texture_coords == 'OBJECT':
            col.label(text="Object:")
            col.prop(self, "texture_coords_object", text="")
        elif self.texture_coords == 'UV' and (not self.mesh == None):
            col.label(text="UV Map:")
            col.prop_search(self, "uv_layer", self.mesh.data, "uv_textures", text="")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="DISPLACE")
        self.mesh.modifiers[0].texture = self.texture
        self.mesh.modifiers[0].direction = self.direction
        self.mesh.modifiers[0].space = self.space
        self.mesh.modifiers[0].texture_coords = self.texture_coords
        self.mesh.modifiers[0].texture_coords_object = self.texture_coords_object
        self.mesh.modifiers[0].vertex_group = self.vertex_group
        self.mesh.modifiers[0].uv_layer = self.uv_layer
        self.mesh.modifiers[0].mid_level = self.inputs["Midlevel"].execute()
        self.mesh.modifiers[0].strength = self.inputs["Strength"].execute()
class EdgeSplitModNode(Node, ScModifierNode):
    bl_idname = "EdgeSplitModNode"
    bl_label = "Edge Split Modifier"
    
    split_angle = FloatProperty(name="Sharpness", default=0.523599, min=0.0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    use_edge_angle = BoolProperty(default=True, update=ScNode.update_value)
    use_edge_sharp = BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScAngleSocket", "Split Angle").prop_prop = "split_angle"
        self.inputs.new("ScBoolSocket", "Edge Angle").prop_prop = "use_edge_angle"
        self.inputs.new("ScBoolSocket", "Sharp Edges").prop_prop = "use_edge_sharp"
        super().init(context)
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="EDGE_SPLIT")
        self.mesh.modifiers[0].split_angle = self.inputs["Split Angle"].execute()
        self.mesh.modifiers[0].use_edge_angle = self.inputs["Edge Angle"].execute()
        self.mesh.modifiers[0].use_edge_sharp = self.inputs["Sharp Edges"].execute()
class LaplacianSmoothModNode(Node, ScModifierNode):
    bl_idname = "LaplacianSmoothModNode"
    bl_label = "Laplacian Smooth Modifier"

    iterations = IntProperty(name="Repeat", default=1, min=-32768, max=32767, soft_min=0, soft_max=200, update=ScNode.update_value)
    use_x = BoolProperty(name="X", default=True, update=ScNode.update_value)
    use_y = BoolProperty(name="Y", default=True, update=ScNode.update_value)
    use_z = BoolProperty(name="Z", default=True, update=ScNode.update_value)
    lambda_factor = FloatProperty(default=0.01, soft_min=-1000.0, soft_max=1000.0, update=ScNode.update_value)
    lambda_border = FloatProperty(default=0.01, soft_min=-1000.0, soft_max=1000.0, update=ScNode.update_value)
    use_volume_preserve = BoolProperty(name="Preserve Volume", default=True, update=ScNode.update_value)
    use_normalized = BoolProperty(name="Normalized", default=True, update=ScNode.update_value)
    vertex_group = StringProperty(name="Vertex Group", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Repeat").prop_prop = "iterations"
        self.inputs.new("ScBoolSocket", "X").prop_prop = "use_x"
        self.inputs.new("ScBoolSocket", "Y").prop_prop = "use_y"
        self.inputs.new("ScBoolSocket", "Z").prop_prop = "use_z"
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "lambda_factor"
        self.inputs.new("ScFloatSocket", "Border").prop_prop = "lambda_border"
        self.inputs.new("ScBoolSocket", "Preserve Volume").prop_prop = "use_volume_preserve"
        self.inputs.new("ScBoolSocket", "Normalized").prop_prop = "use_normalized"
        super().init(context)

    def draw_buttons(self, context, layout):
        if (not self.mesh == None):
            layout.label(text="Vertex Group:")
            layout.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="LAPLACIANSMOOTH")
        self.mesh.modifiers[0].iterations = self.inputs["Repeat"].execute()
        self.mesh.modifiers[0].use_x = self.inputs["X"].execute()
        self.mesh.modifiers[0].use_y = self.inputs["Y"].execute()
        self.mesh.modifiers[0].use_z = self.inputs["Z"].execute()
        self.mesh.modifiers[0].lambda_factor = self.inputs["Factor"].execute()
        self.mesh.modifiers[0].lambda_border = self.inputs["Border"].execute()
        self.mesh.modifiers[0].use_volume_preserve = self.inputs["Preserve Volume"].execute()
        self.mesh.modifiers[0].use_normalized = self.inputs["Normalized"].execute()
        self.mesh.modifiers[0].vertex_group = self.vertex_group
class MirrorModNode(Node, ScModifierNode):
    bl_idname = "MirrorModNode"
    bl_label = "Mirror Modifier"
    
    use_x = BoolProperty(name="X", default=True, update=ScNode.update_value)
    use_y = BoolProperty(name="Y", update=ScNode.update_value)
    use_z = BoolProperty(name="Z", update=ScNode.update_value)
    use_mirror_merge = BoolProperty(default=True, update=ScNode.update_value)
    use_clip = BoolProperty(update=ScNode.update_value)
    use_mirror_vertex_groups = BoolProperty(default=True, update=ScNode.update_value)
    use_mirror_u = BoolProperty(update=ScNode.update_value)
    use_mirror_v = BoolProperty(update=ScNode.update_value)
    mirror_offset_u = FloatProperty(name="U Offset", default=0.0, min=-1.0, max=1.0, update=ScNode.update_value)
    mirror_offset_v = FloatProperty(name="V Offset", default=0.0, min=-1.0, max=1.0, update=ScNode.update_value)
    merge_threshold = FloatProperty(name="Merge Limit", default=0.001, min=0, soft_max=1, update=ScNode.update_value)
    mirror_object = PointerProperty(type=bpy.types.Object, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "X").prop_prop = "use_x"
        self.inputs.new("ScBoolSocket", "Y").prop_prop = "use_y"
        self.inputs.new("ScBoolSocket", "Z").prop_prop = "use_z"
        self.inputs.new("ScBoolSocket", "Merge").prop_prop = "use_mirror_merge"
        self.inputs.new("ScBoolSocket", "Clipping").prop_prop = "use_clip"
        self.inputs.new("ScBoolSocket", "Vertex Groups").prop_prop = "use_mirror_vertex_groups"
        self.inputs.new("ScBoolSocket", "U").prop_prop = "use_mirror_u"
        self.inputs.new("ScBoolSocket", "V").prop_prop = "use_mirror_v"
        self.inputs.new("ScFloatSocket", "U Offset").prop_prop = "mirror_offset_u"
        self.inputs.new("ScFloatSocket", "V Offset").prop_prop = "mirror_offset_v"
        self.inputs.new("ScFloatSocket", "Merge Limit").prop_prop = "merge_threshold"
        super().init(context)

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.label(text="Mirror Object:")
        col.prop(self, "mirror_object", text="")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="MIRROR")
        self.mesh.modifiers[0].use_x = self.inputs["X"].execute()
        self.mesh.modifiers[0].use_y = self.inputs["Y"].execute()
        self.mesh.modifiers[0].use_z = self.inputs["Z"].execute()
        self.mesh.modifiers[0].use_mirror_merge = self.inputs["Merge"].execute()
        self.mesh.modifiers[0].use_clip = self.inputs["Clipping"].execute()
        self.mesh.modifiers[0].use_mirror_vertex_groups = self.inputs["Vertex Groups"].execute()
        self.mesh.modifiers[0].use_mirror_u = self.inputs["U"].execute()
        self.mesh.modifiers[0].use_mirror_v = self.inputs["V"].execute()
        self.mesh.modifiers[0].mirror_offset_u = self.inputs["U Offset"].execute()
        self.mesh.modifiers[0].mirror_offset_v = self.inputs["V Offset"].execute()
        self.mesh.modifiers[0].merge_threshold = self.inputs["Merge Limit"].execute()
        self.mesh.modifiers[0].mirror_object = self.mirror_object
class RemeshModNode(Node, ScModifierNode):
    bl_idname = "RemeshModNode"
    bl_label = "Remesh Modifier"
    
    mode = EnumProperty(name="Mode", items=[("BLOCKS", "Blocks", ""), ("SMOOTH", "Smooth", ""), ("SHARP", "Sharp", "")], default="SHARP", update=ScNode.update_value)
    octree_depth = IntProperty(name="Octree Depth", default=4, min=1, max=12, update=ScNode.update_value)
    scale = FloatProperty(name="Scale", default=0.9, min=0.0, max=0.99, update=ScNode.update_value)
    sharpness = FloatProperty(name="Sharpness", default=1.0, update=ScNode.update_value)
    use_smooth_shade = BoolProperty(name="Smooth Shading", update=ScNode.update_value)
    use_remove_disconnected = BoolProperty(name="Remove Disconnected Pieces", default=True, update=ScNode.update_value)
    threshold = FloatProperty(name="Threshold", default=1.0, min=0.0, max=1.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Octree Depth").prop_prop = "octree_depth"
        self.inputs.new("ScFloatSocket", "Scale").prop_prop = "scale"
        self.inputs.new("ScFloatSocket", "Sharpness").prop_prop = "sharpness"
        self.inputs.new("ScBoolSocket", "Smooth Shading").prop_prop = "use_smooth_shade"
        self.inputs.new("ScBoolSocket", "Remove Disconnected Pieces").prop_prop = "use_remove_disconnected"
        self.inputs.new("ScFloatSocket", "Threshold").prop_prop = "threshold"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "mode")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="REMESH")
        self.mesh.modifiers[0].mode = self.mode
        self.mesh.modifiers[0].octree_depth = self.inputs["Octree Depth"].execute()
        self.mesh.modifiers[0].scale = self.inputs["Scale"].execute()
        self.mesh.modifiers[0].sharpness = self.inputs["Sharpness"].execute()
        self.mesh.modifiers[0].use_smooth_shade = self.inputs["Smooth Shading"].execute()
        self.mesh.modifiers[0].use_remove_disconnected = self.inputs["Remove Disconnected Pieces"].execute()
        self.mesh.modifiers[0].threshold = self.inputs["Threshold"].execute()
class ScrewModNode(Node, ScModifierNode):
    bl_idname = "ScrewModNode"
    bl_label = "Screw Modifier"

    axis = EnumProperty(name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="Z", update=ScNode.update_value)
    object = PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    angle = FloatProperty(name="Angle", default=6.283185, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    steps = IntProperty(name="Steps", default=16, min=2, max=10000, soft_max=512, update=ScNode.update_value)
    render_steps = IntProperty(name="Render Steps", default=16, min=2, max=10000, soft_max=512, update=ScNode.update_value)
    use_smooth_shade = BoolProperty(name="Smooth Shading", default=True, update=ScNode.update_value)
    use_merge_vertices = BoolProperty(name="Merge Vertices", update=ScNode.update_value)
    merge_threshold = FloatProperty(name="Merge Distance", default=0.01, min=0, update=ScNode.update_value)
    screw_offset = FloatProperty(name="Screw", update=ScNode.update_value)
    use_object_screw_offset = BoolProperty(name="Object Screw", update=ScNode.update_value)
    use_normal_calculate = BoolProperty(name="Calc Order", update=ScNode.update_value)
    use_normal_flip = BoolProperty(name="Flip", update=ScNode.update_value)
    iterations = IntProperty(default=1, min=1, max=10000, name="Iterations", update=ScNode.update_value)
    use_stretch_u = BoolProperty(name="Stretch U", update=ScNode.update_value)
    use_stretch_v = BoolProperty(name="Stretch V", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScMeshRefSocket", "AxisOb").prop_prop = "object"
        self.inputs.new("ScAngleSocket", "Angle").prop_prop = "angle"
        self.inputs.new("ScIntSocket", "Steps").prop_prop = "steps"
        self.inputs.new("ScIntSocket", "Render Steps").prop_prop = "render_steps"
        self.inputs.new("ScBoolSocket", "Smooth Shading").prop_prop = "use_smooth_shade"
        self.inputs.new("ScBoolSocket", "Merge Vertices").prop_prop = "use_merge_vertices"
        self.inputs.new("ScFloatSocket", "Merge Distance").prop_prop = "merge_threshold"
        self.inputs.new("ScFloatSocket", "Screw").prop_prop = "screw_offset"
        self.inputs.new("ScBoolSocket", "Object Screw").prop_prop = "use_object_screw_offset"
        self.inputs.new("ScBoolSocket", "Calc Order").prop_prop = "use_normal_calculate"
        self.inputs.new("ScBoolSocket", "Flip").prop_prop = "use_normal_flip"
        self.inputs.new("ScIntSocket", "Iterations").prop_prop = "iterations"
        self.inputs.new("ScBoolSocket", "Stretch U").prop_prop = "use_stretch_u"
        self.inputs.new("ScBoolSocket", "Stretch V").prop_prop = "use_stretch_v"
        super().init(context)
        
    def draw_buttons(self, context, layout):
        layout.prop(self, "axis")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="SCREW")
        self.mesh.modifiers[0].axis = self.axis
        self.mesh.modifiers[0].object = self.inputs["AxisOb"].execute()
        self.mesh.modifiers[0].angle = self.inputs["Angle"].execute()
        self.mesh.modifiers[0].steps = self.inputs["Steps"].execute()
        self.mesh.modifiers[0].render_steps = self.inputs["Render Steps"].execute()
        self.mesh.modifiers[0].use_smooth_shade = self.inputs["Smooth Shading"].execute()
        self.mesh.modifiers[0].use_merge_vertices = self.inputs["Merge Vertices"].execute()
        self.mesh.modifiers[0].merge_threshold = self.inputs["Merge Distance"].execute()
        self.mesh.modifiers[0].screw_offset = self.inputs["Screw"].execute()
        self.mesh.modifiers[0].use_object_screw_offset = self.inputs["Object Screw"].execute()
        self.mesh.modifiers[0].use_normal_calculate = self.inputs["Calc Order"].execute()
        self.mesh.modifiers[0].use_normal_flip = self.inputs["Flip"].execute()
        self.mesh.modifiers[0].iterations = self.inputs["Iterations"].execute()
        self.mesh.modifiers[0].use_stretch_u = self.inputs["Stretch U"].execute()
        self.mesh.modifiers[0].use_stretch_v = self.inputs["Stretch V"].execute()
class SimpleDeformModNode(Node, ScModifierNode):
    bl_idname = "SimpleDeformModNode"
    bl_label = "Simple Deform Modifier"

    vertex_group = StringProperty(name="Vertex Group", update=ScNode.update_value)
    deform_method = EnumProperty(items=[("TWIST", "Twist", ""), ("BEND", "Bend", ""), ("TAPER", "Taper", ""), ("STRETCH", "Stretch", "")], default="TWIST", update=ScNode.update_value)
    invert_vertex_group = BoolProperty(update=ScNode.update_value)
    origin = PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    lock_x = BoolProperty(name="Lock X Axis", update=ScNode.update_value)
    lock_y = BoolProperty(name="Lock Y Axis", update=ScNode.update_value)
    factor = FloatProperty(name="Factor", default=0.785398, update=ScNode.update_value)
    angle = FloatProperty(name="Angle", default=0.785398, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    limits = FloatVectorProperty(size=2, default=(0.0, 1.0), min=0.0, max=1.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScMeshRefSocket", "Origin").prop_prop = "origin"
        self.inputs.new("ScBoolSocket", "Lock X Axis").prop_prop = "lock_x"
        self.inputs.new("ScBoolSocket", "Lock Y Axis").prop_prop = "lock_y"
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "factor"
        self.inputs.new("ScAngleSocket", "Angle").prop_prop = "angle"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.row().prop(self, "deform_method", expand=True)
        if (not self.mesh == None):
            split = layout.split()
            col = split.column()
            col.label(text="Vertex Group:")
            row = col.row(align=True)
            row.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
            row.prop(self, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
        split = layout.split()
        col = split.column()
        col.prop(self, "limits", slider=True)
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="SIMPLE_DEFORM")
        self.mesh.modifiers[0].deform_method = self.deform_method
        self.mesh.modifiers[0].vertex_group = self.vertex_group
        self.mesh.modifiers[0].invert_vertex_group = self.invert_vertex_group
        self.mesh.modifiers[0].origin = self.inputs["Origin"].execute()
        self.mesh.modifiers[0].lock_x = self.inputs["Lock X Axis"].execute()
        self.mesh.modifiers[0].lock_y = self.inputs["Lock Y Axis"].execute()
        if self.deform_method in {'TAPER', 'STRETCH'}:
            self.mesh.modifiers[0].factor = self.inputs["Factor"].execute()
        else:
            self.mesh.modifiers[0].angle = self.inputs["Angle"].execute()
        self.mesh.modifiers[0].limits = self.limits
class SkinModNode(Node, ScModifierNode):
    bl_idname = "SkinModNode"
    bl_label = "Skin Modifier"

    branch_smoothing = FloatProperty(name="Branch Smoothing", default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    use_smooth_shade = BoolProperty(name="Smooth Shading", update=ScNode.update_value)
    use_x_symmetry = BoolProperty(name="X", default=True, update=ScNode.update_value)
    use_y_symmetry = BoolProperty(name="Y", update=ScNode.update_value)
    use_z_symmetry = BoolProperty(name="Z", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Branch Smoothing").prop_prop = "branch_smoothing"
        self.inputs.new("ScBoolSocket", "Smooth Shading").prop_prop = "use_smooth_shade"
        self.inputs.new("ScBoolSocket", "X").prop_prop = "use_x_symmetry"
        self.inputs.new("ScBoolSocket", "Y").prop_prop = "use_y_symmetry"
        self.inputs.new("ScBoolSocket", "Z").prop_prop = "use_z_symmetry"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        row = layout.row()
        row.operator("object.skin_armature_create", text="Create Armature")
        row.operator("mesh.customdata_skin_add")
        layout.label(text="Selected Vertices:")
        sub = layout.split()
        # None of the operators below will work as the mesh will be in object mode
        # Even if it is in the edit mode, the modifier will have already been applied
        sub.operator("object.skin_loose_mark_clear", text="Mark Loose").action = 'MARK'
        sub.operator("object.skin_loose_mark_clear", text="Clear Loose").action = 'CLEAR'
        sub = layout.split()
        sub.operator("object.skin_root_mark", text="Mark Root")
        sub.operator("object.skin_radii_equalize", text="Equalize Radii")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="SKIN")
        self.mesh.modifiers[0].branch_smoothing = self.inputs["Branch Smoothing"].execute()
        self.mesh.modifiers[0].use_smooth_shade = self.inputs["Smooth Shading"].execute()
        self.mesh.modifiers[0].use_x_symmetry = self.inputs["X"].execute()
        self.mesh.modifiers[0].use_y_symmetry = self.inputs["Y"].execute()
        self.mesh.modifiers[0].use_z_symmetry = self.inputs["Z"].execute()
class SmoothModNode(Node, ScModifierNode):
    bl_idname = "SmoothModNode"
    bl_label = "Smooth Modifier"

    use_x = BoolProperty(name="X", default=True, update=ScNode.update_value)
    use_y = BoolProperty(name="Y", default=True, update=ScNode.update_value)
    use_z = BoolProperty(name="Z", default=True, update=ScNode.update_value)
    factor = FloatProperty(name="Factor", default=0.5, update=ScNode.update_value)
    iterations = IntProperty(name="Repeat", default=1, min=0, max=32767, soft_max=30, update=ScNode.update_value)
    vertex_group = StringProperty(name="Vertex Group", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "factor"
        self.inputs.new("ScIntSocket", "Repeat").prop_prop = "iterations"
        self.inputs.new("ScBoolSocket", "X").prop_prop = "use_x"
        self.inputs.new("ScBoolSocket", "Y").prop_prop = "use_y"
        self.inputs.new("ScBoolSocket", "Z").prop_prop = "use_z"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        if (not self.mesh == None):
            layout.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="SMOOTH")
        self.mesh.modifiers[0].use_x = self.inputs["X"].execute()
        self.mesh.modifiers[0].use_y = self.inputs["Y"].execute()
        self.mesh.modifiers[0].use_z = self.inputs["Z"].execute()
        self.mesh.modifiers[0].factor = self.inputs["Factor"].execute()
        self.mesh.modifiers[0].iterations = self.inputs["Repeat"].execute()
        self.mesh.modifiers[0].vertex_group = self.vertex_group
class SolidifyModNode(Node, ScModifierNode):
    bl_idname = "SolidifyModNode"
    bl_label = "Solidify Modifier"
    
    thickness = FloatProperty(name="Thickness", default=0.01, update=ScNode.update_value)
    thickness_clamp = FloatProperty(name="Clamp", default=0.0, min=0.0, max=100.0, update=ScNode.update_value)
    vertex_group = StringProperty(name="Vertex Group", update=ScNode.update_value)
    invert_vertex_group = BoolProperty(name="Invert", update=ScNode.update_value)
    thickness_vertex_group = FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    edge_crease_inner = FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    edge_crease_outer = FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    edge_crease_rim = FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    offset = FloatProperty(name="Offset", default=-1.0, update=ScNode.update_value)
    use_flip_normals = BoolProperty(name="Flip Normals", update=ScNode.update_value)
    use_even_offset = BoolProperty(name="Even Thickness", update=ScNode.update_value)
    use_quality_normals = BoolProperty(name="High Quality Normals", update=ScNode.update_value)
    use_rim = BoolProperty(name="Fill Rim", default=True, update=ScNode.update_value)
    use_rim_only = BoolProperty(name="Only Rim", update=ScNode.update_value)
    material_offset = IntProperty(default=0, min=-32768, max=32767, update=ScNode.update_value)
    material_offset_rim = IntProperty(default=0, min=-32768, max=32767, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Thickness").prop_prop = "thickness"
        self.inputs.new("ScFloatSocket", "Clamp").prop_prop = "thickness_clamp"
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "thickness_vertex_group"
        self.inputs.new("ScFloatSocket", "Inner").prop_prop = "edge_crease_inner"
        self.inputs.new("ScFloatSocket", "Outer").prop_prop = "edge_crease_outer"
        self.inputs.new("ScFloatSocket", "Rim").prop_prop = "edge_crease_rim"
        self.inputs.new("ScFloatSocket", "Offset").prop_prop = "offset"
        self.inputs.new("ScBoolSocket", "Flip Normals").prop_prop = "use_flip_normals"
        self.inputs.new("ScBoolSocket", "Even Thickness").prop_prop = "use_even_offset"
        self.inputs.new("ScBoolSocket", "High Quality Normals").prop_prop = "use_quality_normals"
        self.inputs.new("ScBoolSocket", "Fill Rim").prop_prop = "use_rim"
        self.inputs.new("ScBoolSocket", "Only Rim").prop_prop = "use_rim_only"
        self.inputs.new("ScIntSocket", "Material Offset").prop_prop = "material_offset"
        self.inputs.new("ScIntSocket", "Material Offset Rim").prop_prop = "material_offset_rim"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        split = layout.split()
        col = split.column()
        row = col.row(align=True)
        if (not self.mesh == None):
            row.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
            sub = row.row(align=True)
            sub.active = bool(self.vertex_group)
            sub.prop(self, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="SOLIDIFY")
        self.mesh.modifiers[0].thickness = self.inputs["Thickness"].execute()
        self.mesh.modifiers[0].thickness_clamp = self.inputs["Clamp"].execute()
        self.mesh.modifiers[0].vertex_group = self.vertex_group
        self.mesh.modifiers[0].invert_vertex_group = self.invert_vertex_group
        self.mesh.modifiers[0].thickness_vertex_group = self.inputs["Factor"].execute()
        self.mesh.modifiers[0].edge_crease_inner = self.inputs["Inner"].execute()
        self.mesh.modifiers[0].edge_crease_outer = self.inputs["Outer"].execute()
        self.mesh.modifiers[0].edge_crease_rim = self.inputs["Rim"].execute()
        self.mesh.modifiers[0].offset = self.inputs["Offset"].execute()
        self.mesh.modifiers[0].use_flip_normals = self.inputs["Flip Normals"].execute()
        self.mesh.modifiers[0].use_even_offset = self.inputs["Even Thickness"].execute()
        self.mesh.modifiers[0].use_quality_normals = self.inputs["High Quality Normals"].execute()
        self.mesh.modifiers[0].use_rim = self.inputs["Fill Rim"].execute()
        self.mesh.modifiers[0].use_rim_only = self.inputs["Only Rim"].execute()
        self.mesh.modifiers[0].material_offset = self.inputs["Material Offset"].execute()
        self.mesh.modifiers[0].material_offset_rim = self.inputs["Material Offset Rim"].execute()
class SubdivideModNode(Node, ScModifierNode):
    bl_idname = "SubdivideModNode"
    bl_label = "Subdivision Surface Modifier"
    
    subdivision_type = EnumProperty(items=[("CATMULL_CLARK", "Catmull-Clark", ""), ("SIMPLE", "Simple", "")], default="CATMULL_CLARK", update=ScNode.update_value)
    levels = IntProperty(default=1, min=0, max=11, soft_max=6, update=ScNode.update_value)
    render_levels = IntProperty(default=2, min=0, max=11, soft_max=6, update=ScNode.update_value)
    use_subsurf_uv = BoolProperty(name="Subdivide UVs", default=True, update=ScNode.update_value)
    show_only_control_edges = BoolProperty(name="Optimal Display", update=ScNode.update_value)
    prop_levels = IntProperty()

    def init(self, context):
        self.inputs.new("ScIntSocket", "View").prop_prop = "levels"
        self.inputs.new("ScIntSocket", "Render").prop_prop = "render_levels"
        self.inputs.new("ScBoolSocket", "Subdivide UVs").prop_prop = "use_subsurf_uv"
        self.inputs.new("ScBoolSocket", "Optimal Display").prop_prop = "show_only_control_edges"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.row().prop(self, "subdivision_type", expand=True)
    
    def pre_execute(self):
        self.prop_levels = self.inputs["View"].execute()
        if (self.prop_levels == 0):
            return False
        return super().pre_execute()
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="SUBSURF")
        self.mesh.modifiers[0].subdivision_type = self.subdivision_type
        self.mesh.modifiers[0].levels = self.prop_levels
        self.mesh.modifiers[0].render_levels = self.inputs["Render"].execute()
        self.mesh.modifiers[0].use_subsurf_uv = self.inputs["Subdivide UVs"].execute()
        self.mesh.modifiers[0].show_only_control_edges = self.inputs["Optimal Display"].execute()
class TriangulateModNode(Node, ScModifierNode):
    bl_idname = "TriangulateModNode"
    bl_label = "Triangulate Modifier"
    
    quad_method = EnumProperty(items=[("BEAUTY", "Beauty", ""), ("FIXED", "Fixed", ""), ("FIXED_ALTERNATE", "Fixed Alternate", ""), ("SHORTEST_DIAGONAL", "Shortest Diagonal", "")], default="SHORTEST_DIAGONAL", update=ScNode.update_value)
    ngon_method = EnumProperty(items=[("BEAUTY", "Beauty", ""), ("CLIP", "Clip", "")], default="BEAUTY", update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.label(text="Quad Method:")
        layout.prop(self, "quad_method", text="")
        layout.label(text="Ngon Method:")
        layout.prop(self, "ngon_method", text="")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="TRIANGULATE")
        self.mesh.modifiers[0].quad_method = self.quad_method
        self.mesh.modifiers[0].ngon_method = self.ngon_method
class WireframeModNode(Node, ScModifierNode):
    bl_idname = "WireframeModNode"
    bl_label = "Wireframe Modifier"

    thickness = FloatProperty(update=ScNode.update_value)
    vertex_group = StringProperty(update=ScNode.update_value)
    invert_vertex_group = BoolProperty(update=ScNode.update_value)
    thickness_vertex_group = FloatProperty(default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    use_crease = BoolProperty(update=ScNode.update_value)
    crease_weight = FloatProperty(update=ScNode.update_value)
    offset = FloatProperty(name="Offset", update=ScNode.update_value)
    use_even_offset = BoolProperty(update=ScNode.update_value)
    use_relative_offset = BoolProperty(update=ScNode.update_value)
    use_boundary = BoolProperty(update=ScNode.update_value)
    use_replace = BoolProperty(update=ScNode.update_value)
    material_offset = IntProperty(default=0, min=-32768, max=32767, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Thickness").prop_prop = "thickness"
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "thickness_vertex_group"
        self.inputs.new("ScFloatSocket", "Crease Weight").prop_prop = "crease_weight"
        self.inputs.new("ScFloatSocket", "Offset").prop_prop = "offset"
        self.inputs.new("ScBoolSocket", "Crease Edges").prop_prop = "use_crease"
        self.inputs.new("ScBoolSocket", "Even Thickness").prop_prop = "use_even_offset"
        self.inputs.new("ScBoolSocket", "Relative Thickness").prop_prop = "use_relative_offset"
        self.inputs.new("ScBoolSocket", "Boundary").prop_prop = "use_boundary"
        self.inputs.new("ScBoolSocket", "Replace Original").prop_prop = "use_replace"
        self.inputs.new("ScIntSocket", "Material Offset").prop_prop = "material_offset"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        if (not self.mesh == None):
            row = layout.row(align=True)
            row.prop_search(self, "vertex_group", self.mesh, "vertex_groups", text="")
            row.prop(self, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="WIREFRAME")
        self.mesh.modifiers[0].thickness = self.inputs["Thickness"].execute()
        self.mesh.modifiers[0].vertex_group = self.vertex_group
        self.mesh.modifiers[0].invert_vertex_group = self.invert_vertex_group
        self.mesh.modifiers[0].thickness_vertex_group = self.inputs["Factor"].execute()
        self.mesh.modifiers[0].use_crease = self.inputs["Crease Edges"].execute()
        self.mesh.modifiers[0].crease_weight = self.inputs["Crease Weight"].execute()
        self.mesh.modifiers[0].offset = self.inputs["Offset"].execute()
        self.mesh.modifiers[0].use_even_offset = self.inputs["Even Thickness"].execute()
        self.mesh.modifiers[0].use_relative_offset = self.inputs["Relative Thickness"].execute()
        self.mesh.modifiers[0].use_boundary = self.inputs["Boundary"].execute()
        self.mesh.modifiers[0].use_replace = self.inputs["Replace Original"].execute()
        self.mesh.modifiers[0].material_offset = self.inputs["Material Offset"].execute()
# Conversion
class ToComponentNode(Node, ScConversionNode):
    bl_idname = "ToComponentNode"
    bl_label = "To Component"
    
    prop_selection_type = EnumProperty(name="Component", items=[("FACE", "Faces", ""), ("VERT", "Vertices", ""), ("EDGE", "Edges", "")], default="FACE", update=ScNode.update_value)
    prop_deselect = BoolProperty(name="Deselect All", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScMeshSocket", "Mesh").prop_prop = "mesh"
        self.inputs.new("ScBoolSocket", "Deselect").prop_prop = "prop_deselect"
        self.outputs.new("ScComponentSocket", "Component")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_selection_type", expand=True)
    
    def functionality(self):
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type=self.prop_selection_type)
        if (self.inputs["Deselect"].execute()):
            bpy.ops.mesh.select_all(action="DESELECT")
class ToMeshNode(Node, ScConversionNode):
    bl_idname = "ToMeshNode"
    bl_label = "To Mesh"

    def init(self, context):
        self.inputs.new("ScComponentSocket", "Component").prop_prop = "mesh"
        self.outputs.new("ScMeshSocket", "Mesh")
        super().init(context)
    
    def functionality(self):
        bpy.ops.object.mode_set(mode="OBJECT")
class ChangeModeNode(Node, ScConversionNode):
    bl_idname = "ChangeModeNode"
    bl_label = "Change Component Mode"
    
    prop_selection_type = EnumProperty(name="Component", items=[("FACE", "Faces", ""), ("VERT", "Vertices", ""), ("EDGE", "Edges", "")], default="FACE", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScComponentSocket", "Component").prop_prop = "mesh"
        self.outputs.new("ScComponentSocket", "Component")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_selection_type", expand=True)
    
    def functionality(self):
        bpy.ops.mesh.select_mode(type=self.prop_selection_type)
# Selection
class SelectManuallyNode(Node, ScSelectionNode):
    bl_idname = "SelectManuallyNode"
    bl_label = "Select Manually"
    
    selection_face = StringProperty()
    selection_vert = StringProperty()
    selection_edge = StringProperty()

    def save_selection(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        self.selection_face = str([i.index for i in self.mesh.data.polygons if i.select])
        self.selection_vert = str([i.index for i in self.mesh.data.vertices if i.select])
        self.selection_edge = str([i.index for i in self.mesh.data.edges if i.select])
        bpy.ops.object.mode_set(mode="EDIT")
        print("DEBUG: " + self.name + ": Saved components selection")

    def draw_buttons(self, context, layout):
        if (self.mesh):
            if (self == self.id_data.nodes.active):
                layout.operator("sc.save_selection_op", "Save Selection")
            layout.label(text="Faces: " + str(len([i for i in self.mesh.data.polygons if i.select])) + "/" + str(len(self.mesh.data.polygons)))
            layout.label(text="Vertices: " + str(len([i for i in self.mesh.data.vertices if i.select])) + "/" + str(len(self.mesh.data.vertices)))
            layout.label(text="Edges: " + str(len([i for i in self.mesh.data.edges if i.select])) + "/" + str(len(self.mesh.data.edges)))
    
    def functionality(self):
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        list_face = toList(self.selection_face)
        list_vert = toList(self.selection_vert)
        list_edge = toList(self.selection_edge)
        for i in list_face:
            if i >= len(self.mesh.data.polygons):
                break
            self.mesh.data.polygons[i].select = True
        for i in list_vert:
            if i >= len(self.mesh.data.vertices):
                break
            self.mesh.data.vertices[i].select = True
        for i in list_edge:
            if i >= len(self.mesh.data.edges):
                break
            self.mesh.data.edges[i].select = True
        bpy.ops.object.mode_set(mode="EDIT")
class SelectComponentByIndexNode(Node, ScSelectionNode):
    bl_idname = "SelectComponentByIndexNode"
    bl_label = "Select Component By Index"

    prop_index = IntProperty(name="Index", min=0, update=ScNode.update_value)
    prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)
    prop_deselect = BoolProperty(name="Deselect", update=ScNode.update_value)
    prop_selection_type = EnumProperty(name="Component", items=[("FACE", "Faces", ""), ("VERT", "Vertices", ""), ("EDGE", "Edges", "")], default="FACE", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Index").prop_prop = "prop_index"
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        self.inputs.new("ScBoolSocket", "Deselect").prop_prop = "prop_deselect"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_selection_type")
    
    def functionality(self):
        if (not self.inputs["Extend"].execute()):
            bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        if (self.prop_selection_type == "FACE"):
            self.mesh.data.polygons[min(max(self.inputs["Index"].execute(), 0), len(self.mesh.data.polygons)-1)].select = not self.inputs["Deselect"].execute()
        elif (self.prop_selection_type == "VERT"):
            self.mesh.data.vertices[min(max(self.inputs["Index"].execute(), 0), len(self.mesh.data.vertices)-1)].select = not self.inputs["Deselect"].execute()
        else:
            self.mesh.data.edges[min(max(self.inputs["Index"].execute(), 0), len(self.mesh.data.edges)-1)].select = not self.inputs["Deselect"].execute()
        bpy.ops.object.mode_set(mode="EDIT")
class SelectFacesByMaterialNode(Node, ScSelectionNode):
    bl_idname = "SelectFacesByMaterialNode"
    bl_label = "Select Faces By Material"

    prop_mat = PointerProperty(name="Material", type=bpy.types.Material, update=ScNode.update_value)
    prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)
    prop_deselect = BoolProperty(name="Deselect", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        self.inputs.new("ScBoolSocket", "Deselect").prop_prop = "prop_deselect"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_mat")
    
    def pre_execute(self):
        if (self.prop_mat == None):
            print("DEBUG: " + self.name + ": No material selected")
            return False
        return super().pre_execute()

    def functionality(self):
        if (not self.inputs["Extend"].execute()):
            bpy.ops.mesh.select_all(action="DESELECT")
        slot = self.mesh.material_slots.find(self.prop_mat.name)
        if (slot == -1):
            print("DEBUG: " + self.name + ": No material slot found")
        else:
            self.mesh.active_material_index = slot
            if (self.inputs["Deselect"].execute()):
                bpy.ops.object.material_slot_deselect()
            else:
                bpy.ops.object.material_slot_select()
class SelectFacesByNormalNode(Node, ScSelectionNode):
    bl_idname = "SelectFacesByNormalNode"
    bl_label = "Select Faces By Normal"
    
    prop_min = FloatVectorProperty(name="Minimum", default=(-1.0, -1.0, -1.0), min=-1.0, max=1.0, update=ScNode.update_value)
    prop_max = FloatVectorProperty(name="Maximum", default=(1.0, 1.0, 1.0), min=-1.0, max=1.0, update=ScNode.update_value)
    prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatVectorSocket", "Min").prop_prop = "prop_min"
        self.inputs.new("ScFloatVectorSocket", "Max").prop_prop = "prop_max"
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        super().init(context)
    
    def functionality(self):
        if (not self.inputs["Extend"].execute()):
            bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        prop_min = self.inputs["Min"].execute()
        prop_max = self.inputs["Max"].execute()
        for face in self.mesh.data.polygons:
            if ((face.normal[0] >= prop_min[0] and face.normal[1] >= prop_min[1] and face.normal[2] >= prop_min[2]) and (face.normal[0] <= prop_max[0] and face.normal[1] <= prop_max[1] and face.normal[2] <= prop_max[2])):
                face.select = True
        bpy.ops.object.mode_set(mode="EDIT")
class SelectVerticesByVertexGroupNode(Node, ScSelectionNode):
    bl_idname = "SelectVerticesByVertexGroupNode"
    bl_label = "Select Vertices By Vertex Group"

    prop_vg = StringProperty(name="Vertex Group", update=ScNode.update_value)
    prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)
    prop_deselect = BoolProperty(name="Deselect", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        self.inputs.new("ScBoolSocket", "Deselect").prop_prop = "prop_deselect"
        super().init(context)

    def draw_buttons(self, context, layout):
        if (not self.mesh == None):
            layout.prop_search(self, "prop_vg", self.mesh, "vertex_groups")
    
    def pre_execute(self):
        self.mesh = self.inputs["Component"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        if (self.prop_vg == ""):
            print("DEBUG: " + self.name + ": No vertex group selected")
            return False
        return True

    def functionality(self):
        if (not self.inputs["Extend"].execute()):
            bpy.ops.mesh.select_all(action="DESELECT")
        self.mesh.vertex_groups.active = self.mesh.vertex_groups[self.prop_vg]
        if (self.inputs["Deselect"].execute()):
            bpy.ops.object.vertex_group_deselect()
        else:
            bpy.ops.object.vertex_group_select()
class SelectAllNode(Node, ScSelectionNode):
    bl_idname = "SelectAllNode"
    bl_label = "Select All"

    prop_action = EnumProperty(name="Action", items=[("TOGGLE", "Toggle", ""), ("SELECT", "Select", ""), ("DESELECT", "Deselect", ""), ("INVERT", "Invert", "")], default="TOGGLE", update=ScNode.update_value)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_action")
    
    def functionality(self):
        bpy.ops.mesh.select_all(action=self.prop_action)
class SelectAxisNode(Node, ScSelectionNode):
    bl_idname = "SelectAxisNode"
    bl_label = "Select Axis"

    prop_mode = EnumProperty(name="Mode", items=[("POSITIVE", "Positive", ""), ("NEGATIVE", "Negative", ""), ("ALIGNED", "Aligned", "")], default="POSITIVE", update=ScNode.update_value)
    prop_axis = EnumProperty(name="Axis", items=[("X_AXIS", "X", ""), ("Y_AXIS", "Y", ""), ("Z_AXIS", "Z", "")], default="X_AXIS", update=ScNode.update_value)
    prop_threshold = FloatProperty(name="Threshold", default=0.0001, min=0.000001, max=50, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Threshold").prop_prop = "prop_threshold"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_mode", expand=True)
        layout.prop(self, "prop_axis")
    
    def functionality(self):
        bpy.ops.mesh.select_axis(mode=self.prop_mode, axis=self.prop_axis, threshold=self.inputs["Threshold"].execute())
class SelectFaceBySidesNode(Node, ScSelectionNode):
    bl_idname = "SelectFaceBySidesNode"
    bl_label = "Select Face By Sides"

    prop_number = IntProperty(name="Number", default=3, min=3, update=ScNode.update_value)
    prop_type = EnumProperty(name="Type", items=[("LESS", "Less", ""), ("EQUAL", "Equal", ""), ("GREATER", "Greater", ""), ("NOTEQUAL", "Not Equal", "")], default="EQUAL", update=ScNode.update_value)
    prop_extend = BoolProperty(name="Extend", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Number").prop_prop = "prop_number"
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
    
    def functionality(self):
        bpy.ops.mesh.select_face_by_sides(number=self.inputs["Number"].execute(), type=self.prop_type, extend=self.inputs["Extend"].execute())
class SelectInteriorFaces(Node, ScSelectionNode):
    bl_idname = "SelectInteriorFaces"
    bl_label = "Select Interior Faces"

    def functionality(self):
        bpy.ops.mesh.select_interior_faces()
class SelectLessNode(Node, ScSelectionNode):
    bl_idname = "SelectLessNode"
    bl_label = "Select Less"

    prop_face_step = BoolProperty(name="Face Step", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Face Step").prop_prop = "prop_face_step"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.select_less(use_face_step=self.inputs["Face Step"].execute())
class SelectMoreNode(Node, ScSelectionNode):
    bl_idname = "SelectMoreNode"
    bl_label = "Select More"

    prop_face_step = BoolProperty(name="Face Step", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Face Step").prop_prop = "prop_face_step"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.select_more(use_face_step=self.inputs["Face Step"].execute())
class SelectLinkedNode(Node, ScSelectionNode):
    bl_idname = "SelectLinkedNode"
    bl_label = "Select Linked"

    prop_delimit = EnumProperty(name="Delimit", items=[("NORMAL", "Normal", ""), ("MATERIAL", "Material", ""), ("SEAM", "Seam", ""), ("SHARP", "Sharp", ""), ("UV", "UV", "")], default="SEAM", update=ScNode.update_value)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_delimit")
    
    def functionality(self):
        bpy.ops.mesh.select_linked(delimit={self.prop_delimit})
class SelectLoopNode(Node, ScSelectionNode):
    bl_idname = "SelectLoopNode"
    bl_label = "Select Loop"

    prop_ring = BoolProperty(name="Ring", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Ring").prop_prop = "prop_ring"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.loop_multi_select(ring=self.inputs["Ring"].execute())
class SelectLoopRegionNode(Node, ScSelectionNode):
    bl_idname = "SelectLoopRegionNode"
    bl_label = "Select Loop Region"

    prop_bigger = BoolProperty(name="Select Bigger", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Select Bigger").prop_prop = "prop_bigger"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.loop_to_region(select_bigger=self.inputs["Select Bigger"].execute())
class SelectLooseNode(Node, ScSelectionNode):
    bl_idname = "SelectLooseNode"
    bl_label = "Select Loose"

    prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.select_loose(extend=self.inputs["Extend"].execute())
class SelectMirrorNode(Node, ScSelectionNode):
    bl_idname = "SelectMirrorNode"
    bl_label = "Select Mirror"

    prop_axis = EnumProperty(name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X", update=ScNode.update_value)
    prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_axis", expand=True)
    
    def functionality(self):
        bpy.ops.mesh.select_mirror(axis={self.prop_axis}, extend=self.inputs["Extend"].execute())
class SelectNextItemNode(Node, ScSelectionNode):
    bl_idname = "SelectNextItemNode"
    bl_label = "Select Next Item"

    def functionality(self):
        bpy.ops.mesh.select_next_item()
class SelectPrevItemNode(Node, ScSelectionNode):
    bl_idname = "SelectPrevItemNode"
    bl_label = "Select Previous Item"

    def functionality(self):
        bpy.ops.mesh.select_prev_item()
class SelectNonManifoldNode(Node, ScSelectionNode):
    bl_idname = "SelectNonManifoldNode"
    bl_label = "Select Non-Manifold"

    prop_extend = BoolProperty(name="Extend", default=True, update=ScNode.update_value)
    prop_wire = BoolProperty(name="Wire", default=True, update=ScNode.update_value)
    prop_boundary = BoolProperty(name="Boundary", default=True, update=ScNode.update_value)
    prop_multi_face = BoolProperty(name="Multiple Faces", default=True, update=ScNode.update_value)
    prop_non_contiguous = BoolProperty(name="Non Contiguous", default=True, update=ScNode.update_value)
    prop_verts = BoolProperty(name="Vertices", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        self.inputs.new("ScBoolSocket", "Wire").prop_prop = "prop_wire"
        self.inputs.new("ScBoolSocket", "Boundary").prop_prop = "prop_boundary"
        self.inputs.new("ScBoolSocket", "Multiple Faces").prop_prop = "prop_multi_face"
        self.inputs.new("ScBoolSocket", "Non Contiguous").prop_prop = "prop_non_contiguous"
        self.inputs.new("ScBoolSocket", "Vertices").prop_prop = "prop_verts"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.select_non_manifold(extend=self.inputs["Extend"].execute(), use_wire=self.inputs["Wire"].execute(), use_boundary=self.inputs["Boundary"].execute(), use_multi_face=self.inputs["Multiple Faces"].execute(), use_non_contiguous=self.inputs["Non Contiguous"].execute(), use_verts=self.inputs["Vertices"].execute())
class SelectNthNode(Node, ScSelectionNode):
    bl_idname = "SelectNthNode"
    bl_label = "Select Nth (Checker Deselect)"

    prop_nth = IntProperty(name="Nth", default=2, min=2, update=ScNode.update_value)
    prop_skip = IntProperty(name="Skip", default=1, min=1, update=ScNode.update_value)
    prop_offset = IntProperty(name="Offset", default=0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Nth").prop_prop = "prop_nth"
        self.inputs.new("ScIntSocket", "Skip").prop_prop = "prop_skip"
        self.inputs.new("ScIntSocket", "Offset").prop_prop = "prop_offset"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.select_nth(nth=self.inputs["Nth"].execute(), skip=self.inputs["Skip"].execute(), offset=self.inputs["Offset"].execute())
class SelectAlternateFacesNode(Node, ScSelectionNode):
    bl_idname = "SelectAlternateFacesNode"
    bl_label = "Select Alternate Faces"

    prop_nth = IntProperty(name="Every Nth", default=1, min=1, update=ScNode.update_value)
    prop_offset = IntProperty(name="Offset", default=0, min=0, update=ScNode.update_value)
    prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Every Nth").prop_prop = "prop_nth"
        self.inputs.new("ScIntSocket", "Offset").prop_prop = "prop_offset"
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        super().init(context)
    
    def functionality(self):
        if (not self.inputs["Extend"].execute()):
            bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        i = self.inputs["Offset"].execute()
        prop_nth = self.inputs["Every Nth"].execute()
        while (i < len(self.mesh.data.polygons)):
            self.mesh.data.polygons[i].select = True
            i += prop_nth
        bpy.ops.object.mode_set(mode="EDIT")
class SelectRandomNode(Node, ScSelectionNode):
    bl_idname = "SelectRandomNode"
    bl_label = "Select Random"

    prop_percent = FloatProperty(name="Percent", default=50.0, min=0.0, max=100.0, update=ScNode.update_value)
    prop_seed = IntProperty(name="Seed", default=0, min=0, update=ScNode.update_value)
    prop_action = EnumProperty(name="Action", items=[("SELECT", "Select", ""), ("DESELECT", "Deselect", "")], default="SELECT", update=ScNode.update_value)
    
    def init(self, context):
        self.inputs.new("ScFloatSocket", "Percent").prop_prop = "prop_percent"
        self.inputs.new("ScIntSocket", "Seed").prop_prop = "prop_seed"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_action")

    def functionality(self):
        bpy.ops.mesh.select_random(percent=self.inputs["Percent"].execute(), seed=self.inputs["Seed"].execute(), action=self.prop_action)
class SelectRegionBoundaryNode(Node, ScSelectionNode):
    bl_idname = "SelectRegionBoundaryNode"
    bl_label = "Select Region Boundary"

    def functionality(self):
        bpy.ops.mesh.region_to_loop()
class SelectSharpEdgesNode(Node, ScSelectionNode):
    bl_idname = "SelectSharpEdgesNode"
    bl_label = "Select Sharp Edges"

    prop_sharpness = FloatProperty(name="Sharpness", default=0.523599, min=0.000174533, max=3.14159, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Sharpness").prop_prop = "prop_sharpness"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.edges_select_sharp(sharpness=self.inputs["Sharpness"].execute())
# class SelectEdgeRingNode(Node, ScSelectionNode):
#     bl_idname = "SelectEdgeRingNode"
#     bl_label = "Select Edge Ring"

#     prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)
#     prop_deselect = BoolProperty(name="Deselect", update=ScNode.update_value)
#     prop_toggle = BoolProperty(name="Toggle", update=ScNode.update_value)
#     prop_ring = BoolProperty(name="Ring", default=True, update=ScNode.update_value)

#     def init(self, context):
#         self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
#         self.inputs.new("ScBoolSocket", "Deselect").prop_prop = "prop_deselect"
#         self.inputs.new("ScBoolSocket", "Toggle").prop_prop = "prop_toggle"
#         self.inputs.new("ScBoolSocket", "Ring").prop_prop = "prop_ring"

#     def functionality(self):
#         bpy.ops.mesh.edgering_select(extend=self.inputs["Extend"].execute(), deselect=self.inputs["Deselect"].execute(), toggle=self.inputs["Toggle"].execute(), ring=self.inputs["Ring"].execute())
class SelectSimilarNode(Node, ScSelectionNode):
    bl_idname = "SelectSimilarNode"
    bl_label = "Select Similar"

    prop_type = EnumProperty(name="Type", items=[("MATERIAL", "Material", ""), ("IMAGE", "Image", ""), ("AREA", "Area", ""), ("SIDES", "Sides", ""), ("PERIMETER", "Perimeter", ""), ("NORMAL", "Normal", ""), ("COPLANAR", "Co-Planar", ""), ("SMOOTH", "Smooth", ""), ("FREESTYLE_FACE", "Freestyle Face", "")], default="NORMAL", update=ScNode.update_value)
    prop_compare = EnumProperty(name="Compare", items=[("EQUAL", "Equal", ""), ("GREATER", "Greater", ""), ("LESS", "Less", "")], default="EQUAL", update=ScNode.update_value)
    prop_threshold = FloatProperty(name="Threshold", default=0.0, min=0.0, max=1.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Threshold").prop_prop = "prop_threshold"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
        layout.prop(self, "prop_compare")

    def functionality(self):
        bpy.ops.mesh.select_similar(type=self.prop_type, compare=self.prop_compare, threshold=self.inputs["Threshold"].execute())
class SelectSimilarRegionNode(Node, ScSelectionNode):
    bl_idname = "SelectSimilarRegionNode"
    bl_label = "Select Similar Region"

    def functionality(self):
        bpy.ops.mesh.select_similar_region()
class SelectShortestPathNode(Node, ScSelectionNode):
    bl_idname = "SelectShortestPathNode"
    bl_label = "Select Shortest Path"

    prop_step = BoolProperty(name="Face Stepping", update=ScNode.update_value)
    prop_distance = BoolProperty(name="Topology Distance", update=ScNode.update_value)
    prop_fill = BoolProperty(name="Fill Region", update=ScNode.update_value)
    prop_nth = IntProperty(name="Nth Selection", default=1, min=1, update=ScNode.update_value)
    prop_skip = IntProperty(name="Skip", default=1, min=1, update=ScNode.update_value)
    prop_offset = IntProperty(name="Offset", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Face Stepping").prop_prop = "prop_step"
        self.inputs.new("ScBoolSocket", "Topology Distance").prop_prop = "prop_distance"
        self.inputs.new("ScBoolSocket", "Fill Region").prop_prop = "prop_fill"
        self.inputs.new("ScFloatSocket", "Nth Selection").prop_prop = "prop_nth"
        self.inputs.new("ScFloatSocket", "Skip").prop_prop = "prop_skip"
        self.inputs.new("ScFloatSocket", "Offset").prop_prop = "prop_offset"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.shortest_path_select(use_face_step=self.inputs["Face Stepping"].execute(), use_topology_distance=self.inputs["Topology Distance"].execute(), use_fill=self.inputs["Fill Region"].execute(), nth=self.inputs["Nth Selection"].execute(), skip=self.inputs["Skip"].execute(), offset=self.inputs["Offset"].execute())
class SelectUngroupedNode(Node, ScSelectionNode):
    bl_idname = "SelectUngroupedNode"
    bl_label = "Select Ungrouped"

    prop_extend = BoolProperty(name="Extend", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Extend").prop_prop = "prop_extend"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.select_ungrouped(extend=self.inputs["Extend"].execute())
class SelectFacesLinkedFlatNode(Node, ScSelectionNode):
    bl_idname = "SelectFacesLinkedFlatSharpNode"
    bl_label = "Select Linked Faces By Angle"

    prop_sharpness = FloatProperty(name="Sharpness", default=0.523599, min=0.000174533, max=3.14159, precision=6, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Sharpness").prop_prop = "prop_sharpness"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.faces_select_linked_flat(sharpness=self.inputs["Sharpness"].execute())
# Deletion
class DeleteNode(Node, ScDeletionNode):
    bl_idname = "DeleteNode"
    bl_label = "Delete"

    prop_type = EnumProperty(name="Type", items=[("VERT", "Vertices", ""), ("EDGE", "Edges", ""), ("FACE", "Faces", ""), ("EDGE_FACE", "Edges And Faces", ""), ("ONLY_FACE", "Only Faces", "")], default="VERT", update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
    
    def functionality(self):
        bpy.ops.mesh.delete(type=self.prop_type)
class DeleteEdgeLoopNode(Node, ScEditOperatorNode):
    bl_idname = "DeleteEdgeLoopNode"
    bl_label = "Delete Edge Loop"

    prop_split = BoolProperty(name="Face Split", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Face Split").prop_prop = "prop_split"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.delete_edgeloop(use_face_split=self.inputs["Face Split"].execute())
class DissolveFacesNode(Node, ScEditOperatorNode):
    bl_idname = "DissolveFacesNode"
    bl_label = "Dissolve Faces"

    prop_verts = BoolProperty(name="Dissolve Vertices", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Dissolve Vertices").prop_prop = "prop_verts"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.dissolve_faces(use_verts=self.inputs["Dissolve Vertices"].execute())
class DissolveEdgesNode(Node, ScEditOperatorNode):
    bl_idname = "DissolveEdgesNode"
    bl_label = "Dissolve Edges"

    prop_verts = BoolProperty(name="Dissolve Vertices", default=True, update=ScNode.update_value)
    prop_face_split = BoolProperty(name="Face Split", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Dissolve Vertices").prop_prop = "prop_verts"
        self.inputs.new("ScBoolSocket", "Face Split").prop_prop = "prop_face_split"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.dissolve_edges(use_verts=self.inputs["Dissolve Vertices"].execute(), use_face_split=self.inputs["Face Split"].execute())
class DissolveVerticesNode(Node, ScEditOperatorNode):
    bl_idname = "DissolveVerticesNode"
    bl_label = "Dissolve Vertices"

    prop_face_split = BoolProperty(name="Face Split", update=ScNode.update_value)
    prop_boundary_tear = BoolProperty(name="Tear Boundary", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Face Split").prop_prop = "prop_face_split"
        self.inputs.new("ScBoolSocket", "Tear Boundary").prop_prop = "prop_boundary_tear"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.dissolve_verts(use_face_split=self.inputs["Face Split"].execute(), use_boundary_tear=self.inputs["Tear Boundary"].execute())
class DissolveDegenerateNode(Node, ScDeletionNode):
    bl_idname = "DissolveDegenerateNode"
    bl_label = "Dissolve Degenerate"

    prop_threshold = FloatProperty(name="Threshold", default=0.0001, min=0.000001, max=50.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Threshold").prop_prop = "prop_threshold"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.dissolve_degenerate(threshold=self.inputs["Threshold"].execute())
class EdgeCollapseNode(Node, ScEditOperatorNode):
    bl_idname = "EdgeCollapseNode"
    bl_label = "Edge Collapse"
    
    def functionality(self):
        bpy.ops.mesh.edge_collapse()
# Component Operators
class AddEdgeFaceNode(Node, ScEditOperatorNode):
    bl_idname = "AddEdgeFaceNode"
    bl_label = "Add Edge/Face"

    def functionality(self):
        bpy.ops.mesh.edge_face_add()
class BeautifyFillNode(Node, ScEditOperatorNode):
    bl_idname = "BeautifyFillNode"
    bl_label = "Beautify Fill"

    prop_angle_limit = FloatProperty(name="Angle Limit", default=3.14159, min=0.0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScAngleSocket", "Angle Limit").prop_prop = "prop_angle_limit"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.beautify_fill(angle_limit=self.inputs["Angle Limit"].execute())
class BevelNode(Node, ScEditOperatorNode):
    bl_idname = "BevelNode"
    bl_label = "Bevel"

    prop_offset_type = EnumProperty(name="Offset Type", items=[("OFFSET", "Offset", ""), ("WIDTH", "Width", ""), ("PERCENT", "Percent", ""), ("DEPTH", "Depth", "")], default="OFFSET", update=ScNode.update_value)
    prop_offset = FloatProperty(name="Offset", default=0.0, min=-1000000.0, max=1000000.0, update=ScNode.update_value)
    prop_segments = IntProperty(name="Segments", default=1, min=1, max=1000, update=ScNode.update_value)
    prop_profile = FloatProperty(name="Profile", default=0.5, min=0.15, max=1.0, update=ScNode.update_value)
    prop_vertex_only = BoolProperty(name="Vertex Only", update=ScNode.update_value)
    prop_clamp_overlap = BoolProperty(name="Clamp Overlap", update=ScNode.update_value)
    prop_loop_slide = BoolProperty(name="Loop Slide", default=True, update=ScNode.update_value)
    prop_material = IntProperty(name="Material", default=-1, min=-1, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Offset").prop_prop = "prop_offset"
        self.inputs.new("ScIntSocket", "Segments").prop_prop = "prop_segments"
        self.inputs.new("ScFloatSocket", "Profile").prop_prop = "prop_profile"
        self.inputs.new("ScBoolSocket", "Vertex Only").prop_prop = "prop_vertex_only"
        self.inputs.new("ScBoolSocket", "Clamp Overlap").prop_prop = "prop_clamp_overlap"
        self.inputs.new("ScBoolSocket", "Loop Slide").prop_prop = "prop_loop_slide"
        self.inputs.new("ScIntSocket", "Material").prop_prop = "prop_material"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_offset_type")
    
    def functionality(self):
        bpy.ops.mesh.bevel(offset_type=self.prop_offset_type, offset=self.inputs["Offset"].execute(), segments=self.inputs["Segments"].execute(), profile=self.inputs["Profile"].execute(), vertex_only=self.inputs["Vertex Only"].execute(), clamp_overlap=self.inputs["Clamp Overlap"].execute(), loop_slide=self.inputs["Loop Slide"].execute(), material=self.inputs["Material"].execute())
class BridgeEdgeLoopsNode(Node, ScEditOperatorNode):
    bl_idname = "BridgeEdgeLoopsNode"
    bl_label = "Bridge Edge Loops"

    prop_type = EnumProperty(name="Connect Loops", items=[("SINGLE", "Single", ""), ("CLOSED", "Closed", ""), ("PAIRS", "Pairs", "")], default="SINGLE", update=ScNode.update_value)
    prop_use_merge = BoolProperty(name="Merge", update=ScNode.update_value)
    prop_merge_factor = FloatProperty(name="Merge Factor", default=0.5, min=0.0, max=0.1, update=ScNode.update_value)
    prop_twist_offset = IntProperty(name="Twist", default=0, min=-1000, max=1000, update=ScNode.update_value)
    prop_number_cuts = IntProperty(name="Number of Cuts", default=0, min=0, max=1000, update=ScNode.update_value)
    prop_interpolation = EnumProperty(name="Interpolation", items=[("LINEAR", "Linear", ""), ("PATH", "Path", ""), ("SURFACE", "Surface", "")], default="PATH", update=ScNode.update_value)
    prop_smoothness = FloatProperty(name="Smoothness", default=1.0, min=0.0, max=1000.0, update=ScNode.update_value)
    prop_profile_shape_factor = FloatProperty(name="Profile Factor", default=0.0, min=-1000.0, max=1000.0, update=ScNode.update_value)
    prop_profile_shape = EnumProperty(name="Profile Shape", items=[("SMOOTH", "Smooth", ""), ("SPHERE", "Sphere", ""), ("ROOT", "Root", ""), ("INVERSE_SQUARE", "Inverse Square", ""), ("SHARP", "Sharp", ""), ("LINEAR", "Linear", "")], default="SMOOTH", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Merge").prop_prop = "prop_use_merge"
        self.inputs.new("ScFloatSocket", "Merge Factor").prop_prop = "prop_merge_factor"
        self.inputs.new("ScIntSocket", "Twist").prop_prop = "prop_twist_offset"
        self.inputs.new("ScIntSocket", "Number of Cuts").prop_prop = "prop_number_cuts"
        self.inputs.new("ScFloatSocket", "Smoothness").prop_prop = "prop_smoothness"
        self.inputs.new("ScFloatSocket", "Profile Factor").prop_prop = "prop_profile_shape_factor"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
        layout.prop(self, "prop_interpolation")
        layout.prop(self, "prop_profile_shape")
    
    def functionality(self):
        bpy.ops.mesh.bridge_edge_loops(type=self.prop_type, use_merge=self.inputs["Merge"].execute(), merge_factor=self.inputs["Merge Factor"].execute(), twist_offset=self.inputs["Twist"].execute(), number_cuts=self.inputs["Number of Cuts"].execute(), interpolation=self.prop_interpolation, smoothness=self.inputs["Smoothness"].execute(), profile_shape_factor=self.inputs["Profile Factor"].execute(), profile_shape=self.prop_profile_shape)
class ConvexHullNode(Node, ScEditOperatorNode):
    bl_idname = "ConvexHullNode"
    bl_label = "Convex Hull"

    prop_delete_unused = BoolProperty(name="Delete Unused", default=True, update=ScNode.update_value)
    prop_use_existing_faces = BoolProperty(name="Use Existing Faces", default=True, update=ScNode.update_value)
    prop_make_holes = BoolProperty(name="Make Holes", update=ScNode.update_value)
    prop_join_triangles = BoolProperty(name="Join Triangles", default=True, update=ScNode.update_value)
    prop_face_threshold = FloatProperty(name="Max Face Angle", default=0.698132, min=0.0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    prop_shape_threshold = FloatProperty(name="Max Shape Angle", default=0.698132, min=0.0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    prop_uvs = BoolProperty(name="Compare UVs", update=ScNode.update_value)
    prop_vcols = BoolProperty(name="Compare VCols", update=ScNode.update_value)
    prop_seam = BoolProperty(name="Compare Seam", update=ScNode.update_value)
    prop_sharp = BoolProperty(name="Compare Sharp", update=ScNode.update_value)
    prop_materials = BoolProperty(name="Compare Materials", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Delete Unused").prop_prop = "prop_delete_unused"
        self.inputs.new("ScBoolSocket", "Use Existing Faces").prop_prop = "prop_use_existing_faces"
        self.inputs.new("ScBoolSocket", "Make Holes").prop_prop = "prop_make_holes"
        self.inputs.new("ScBoolSocket", "Join Triangles").prop_prop = "prop_join_triangles"
        self.inputs.new("ScFloatSocket", "Max Face Angle").prop_prop = "prop_face_threshold"
        self.inputs.new("ScFloatSocket", "Max Shape Angle").prop_prop = "prop_shape_threshold"
        self.inputs.new("ScBoolSocket", "Compare UVs").prop_prop = "prop_uvs"
        self.inputs.new("ScBoolSocket", "Compare VCols").prop_prop = "prop_vcols"
        self.inputs.new("ScBoolSocket", "Compare Seam").prop_prop = "prop_seam"
        self.inputs.new("ScBoolSocket", "Compare Sharp").prop_prop = "prop_sharp"
        self.inputs.new("ScBoolSocket", "Compare Materials").prop_prop = "prop_materials"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.convex_hull(delete_unused=self.inputs["Delete Unused"].execute(), use_existing_faces=self.inputs["Use Existing Faces"].execute(), make_holes=self.inputs["Make Holes"].execute(), join_triangles=self.inputs["Join Triangles"].execute(), face_threshold=self.inputs["Max Face Angle"].execute(), shape_threshold=self.inputs["Max Shape Angle"].execute(), uvs=self.inputs["Compare UVs"].execute(), vcols=self.inputs["Compare VCols"].execute(), seam=self.inputs["Compare Seam"].execute(), sharp=self.inputs["Compare Sharp"].execute(), materials=self.inputs["Compare Materials"].execute())
class DecimateNode(Node, ScEditOperatorNode):
    bl_idname = "DecimateNode"
    bl_label = "Decimate"

    prop_ratio = FloatProperty(name="Ratio", default=1.0, min=0.0, max=1.0, update=ScNode.update_value)
    prop_use_vertex_group = BoolProperty(name="Vertex Group", update=ScNode.update_value)
    prop_vertex_group_factor = FloatProperty(name="Weight", default=1.0, min=0.0, max=1000.0, update=ScNode.update_value)
    prop_invert_vertex_group = BoolProperty(name="Invert", update=ScNode.update_value)
    prop_use_symmetry = BoolProperty(name="Symmetry", update=ScNode.update_value)
    prop_symmetry_axis = EnumProperty(name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="Y", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Ratio").prop_prop = "prop_ratio"
        self.inputs.new("ScBoolSocket", "Vertex Group").prop_prop = "prop_use_vertex_group"
        self.inputs.new("ScFloatSocket", "Weight").prop_prop = "prop_vertex_group_factor"
        self.inputs.new("ScBoolSocket", "Invert").prop_prop = "prop_invert_vertex_group"
        self.inputs.new("ScBoolSocket", "Symmetry").prop_prop = "prop_use_symmetry"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_symmetry_axis")
    
    def functionality(self):
        bpy.ops.mesh.decimate(ratio=self.inputs["Ratio"].execute(), use_vertex_group=self.inputs["Vertex Group"].execute(), vertex_group_factor=self.inputs["Weight"].execute(), invert_vertex_group=self.inputs["Invert"].execute(), use_symmetry=self.inputs["Symmetry"].execute(), symmetry_axis=self.prop_symmetry_axis)
class ExtrudeFacesNode(Node, ScEditOperatorNode):
    bl_idname = "ExtrudeFacesNode"
    bl_label = "Extrude Faces (Individual)"

    prop_value = FloatProperty(name="Value", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Value").prop_prop = "prop_value"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.extrude_faces_move(self.override(), TRANSFORM_OT_shrink_fatten={"value":self.inputs["Value"].execute()})
class ExtrudeEdgesNode(Node, ScEditOperatorNode):
    bl_idname = "ExtrudeEdgesNode"
    bl_label = "Extrude Edges (Individual)"

    prop_value = FloatVectorProperty(name="Value", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatVectorSocket", "Value").prop_prop = "prop_value"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.extrude_edges_move(self.override(), TRANSFORM_OT_translate={"value":self.inputs["Value"].execute()})
class ExtrudeVerticesNode(Node, ScEditOperatorNode):
    bl_idname = "ExtrudeVerticesNode"
    bl_label = "Extrude Vertices (Individual)"

    prop_value = FloatVectorProperty(name="Value", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatVectorSocket", "Value").prop_prop = "prop_value"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.extrude_vertices_move(self.override(), TRANSFORM_OT_translate={"value":self.inputs["Value"].execute()})
class ExtrudeRegionNode(Node, ScEditOperatorNode):
    bl_idname = "ExtrudeRegionNode"
    bl_label = "Extrude Region"

    prop_amount = FloatProperty(name="Amount", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Amount").prop_prop = "prop_amount"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.extrude_region_shrink_fatten(self.override(), TRANSFORM_OT_shrink_fatten={"value":self.inputs["Amount"].execute()})
# class ExtrudeRepeatNode(Node, ScEditOperatorNode):
#     bl_idname = "ExtrudeRepeatNode"
#     bl_label = "Extrude Repeat"

#     prop_offset = FloatProperty(name="Offset", default=2.0, min=0.0, update=ScNode.update_value)
#     prop_steps = IntProperty(name="Steps", default=10, min=0, max=1000000, update=ScNode.update_value)
    
#     def init(self, context):
#         self.inputs.new("ScFloatSocket", "Offset").prop_prop = "prop_offset"
#         self.inputs.new("ScIntSocket", "Steps").prop_prop = "prop_steps"
#         super().init(context)
    
#     def functionality(self):
#         bpy.ops.mesh.extrude_repeat(self.override(), offset=self.inputs["Offset"].execute(), steps=self.inputs["Steps"].execute())
class FlipNormalsNode(Node, ScEditOperatorNode):
    bl_idname = "FlipNormalsNode"
    bl_label = "Flip Normals"
    
    def functionality(self):
        bpy.ops.mesh.flip_normals()
class MakeNormalsConsistentNode(Node, ScEditOperatorNode):
    bl_idname = "MakeNormalsConsistentNode"
    bl_label = "Make Normals Consistent"
    
    prop_inside = BoolProperty(name="Inside", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Inside").prop_prop = "prop_inside"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.normals_make_consistent(inside=self.inputs["Inside"].execute())
class FlattenNode(Node, ScEditOperatorNode):
    bl_idname = "FlattenNode"
    bl_label = "Flatten"
    
    prop_mode = EnumProperty(name="Mode", items=[("FACES", "Faces", ""), ("VERTICES", "Vertices", "")], default="FACES", update=ScNode.update_value)
    prop_factor = FloatProperty(name="Factor", default=0.5, min=-10.0, max=10.0, update=ScNode.update_value)
    prop_repeat = IntProperty(name="Repeat", default=1, min=0, max=1000, update=ScNode.update_value)
    prop_x = BoolProperty(name="X", default=True, update=ScNode.update_value)
    prop_y = BoolProperty(name="Y", default=True, update=ScNode.update_value)
    prop_z = BoolProperty(name="Z", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "prop_factor"
        self.inputs.new("ScIntSocket", "Repeat").prop_prop = "prop_repeat"
        self.inputs.new("ScBoolSocket", "X").prop_prop = "prop_x"
        self.inputs.new("ScBoolSocket", "Y").prop_prop = "prop_y"
        self.inputs.new("ScBoolSocket", "Z").prop_prop = "prop_z"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_mode", expand=True)

    def functionality(self):
        if (self.prop_mode == "VERTICES"):
            bpy.ops.mesh.vertices_smooth(factor=self.inputs["Factor"].execute(), repeat=self.inputs["Repeat"].execute(), xaxis = self.inputs["X"].execute(), yaxis = self.inputs["Y"].execute(), zaxis = self.inputs["Z"].execute())
        else:
            bpy.ops.mesh.face_make_planar(factor=self.inputs["Factor"].execute(), repeat=self.inputs["Repeat"].execute())
class FillEdgeLoopNode(Node, ScEditOperatorNode):
    bl_idname = "FillEdgeLoopNode"
    bl_label = "Fill Edge Loop"
    
    prop_beauty = BoolProperty(name="Beauty", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Beauty").prop_prop = "prop_beauty"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.fill(use_beauty=self.inputs["Beauty"].execute())
class FillGridNode(Node, ScEditOperatorNode):
    bl_idname = "FillGridNode"
    bl_label = "Fill Grid"
    
    prop_span = IntProperty(name="Span", default=1, min=1, max=1000, update=ScNode.update_value)
    prop_offset = IntProperty(name="Offset", default=0, min=-1000, max=1000, update=ScNode.update_value)
    prop_interp = BoolProperty(name="Simple Blending", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Span").prop_prop = "prop_span"
        self.inputs.new("ScIntSocket", "Offset").prop_prop = "prop_offset"
        self.inputs.new("ScBoolSocket", "Simple Blending").prop_prop = "prop_interp"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.fill_grid(span=self.inputs["Span"].execute(), offset=self.inputs["Offset"].execute(), use_interp_simple=self.inputs["Simple Blending"].execute())
class FillHolesBySidesNode(Node, ScEditOperatorNode):
    bl_idname = "FillHolesBySidesNode"
    bl_label = "Fill Holes By Sides"
    
    prop_sides = IntProperty(name="Sides", default=4, min=0, max=1000, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Sides").prop_prop = "prop_sides"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.fill_holes(sides=self.inputs["Sides"].execute())
class InsetNode(Node, ScEditOperatorNode):
    bl_idname = "InsetNode"
    bl_label = "Inset"
    
    prop_thickness = FloatProperty(name="Thickness", default=0.01, min=0.0, update=ScNode.update_value)
    prop_depth = FloatProperty(name="Depth", update=ScNode.update_value)
    prop_boundary = BoolProperty(name="Boundary", default=True, update=ScNode.update_value)
    prop_even_offset = BoolProperty(name="Even Offset", default=True, update=ScNode.update_value)
    prop_relative_offset = BoolProperty(name="Relative Offset", update=ScNode.update_value)
    prop_edge_rail = BoolProperty(name="Edge Rail", update=ScNode.update_value)
    prop_outset = BoolProperty(name="Outset", update=ScNode.update_value)
    prop_select_inset = BoolProperty(name="Select Inset", update=ScNode.update_value)
    prop_individual = BoolProperty(name="Individual", update=ScNode.update_value)
    prop_interpolate = BoolProperty(name="Interpolate", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Thickness").prop_prop = "prop_thickness"
        self.inputs.new("ScFloatSocket", "Depth").prop_prop = "prop_depth"
        self.inputs.new("ScBoolSocket", "Individual").prop_prop = "prop_individual"
        self.inputs.new("ScBoolSocket", "Select Inset").prop_prop = "prop_select_inset"
        self.inputs.new("ScBoolSocket", "Boundary").prop_prop = "prop_boundary"
        self.inputs.new("ScBoolSocket", "Even Offset").prop_prop = "prop_even_offset"
        self.inputs.new("ScBoolSocket", "Edge Rail").prop_prop = "prop_edge_rail"
        self.inputs.new("ScBoolSocket", "Outset").prop_prop = "prop_outset"
        self.inputs.new("ScBoolSocket", "Relative Offset").prop_prop = "prop_relative_offset"
        self.inputs.new("ScBoolSocket", "Interpolate").prop_prop = "prop_interpolate"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.inset(use_boundary=self.inputs["Boundary"].execute(), use_even_offset=self.inputs["Even Offset"].execute(), use_relative_offset=self.inputs["Relative Offset"].execute(), use_edge_rail=self.inputs["Edge Rail"].execute(), thickness=self.inputs["Thickness"].execute(), depth=self.inputs["Depth"].execute(), use_outset=self.inputs["Outset"].execute(), use_select_inset=self.inputs["Select Inset"].execute(), use_individual=self.inputs["Individual"].execute(), use_interpolate=self.inputs["Interpolate"].execute())
class LoopCutNode(Node, ScEditOperatorNode):
    bl_idname = "LoopCutNode"
    bl_label = "Loop Cut"

    prop_number = IntProperty(name="Number of Cuts", default=1, min=1, soft_max=100, update=ScNode.update_value)
    prop_smoothness = FloatProperty(name="Smoothness", soft_min=-4.0, soft_max=4.0, update=ScNode.update_value)
    prop_use_selected_edge = BoolProperty(name="Use selected edge", default=True, update=ScNode.update_value)
    prop_index = IntProperty(name="Edge Index", default=0, min=0, update=ScNode.update_value)
    prop_factor = FloatProperty(name="Factor", default=0.0, min=-1.0, max=1.0, update=ScNode.update_value)
    prop_single = BoolProperty(name="Single Side", update=ScNode.update_value)
    prop_even = BoolProperty(name="Even", update=ScNode.update_value)
    prop_flipped = BoolProperty(name="Flipped", update=ScNode.update_value)
    prop_clamp = BoolProperty(name="Clamp", default=True, update=ScNode.update_value)
    index = IntProperty()

    def init(self, context):
        self.inputs.new("ScIntSocket", "Number of Cuts").prop_prop = "prop_number"
        self.inputs.new("ScFloatSocket", "Smoothness").prop_prop = "prop_smoothness"
        self.inputs.new("ScBoolSocket", "Use Selected Edge").prop_prop = "prop_use_selected_edge"
        self.inputs.new("ScIntSocket", "Edge Index").prop_prop = "prop_index"
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "prop_factor"
        self.inputs.new("ScBoolSocket", "Single Side").prop_prop = "prop_single"
        self.inputs.new("ScBoolSocket", "Even").prop_prop = "prop_even"
        self.inputs.new("ScBoolSocket", "Flipped").prop_prop = "prop_flipped"
        self.inputs.new("ScBoolSocket", "Clamp").prop_prop = "prop_clamp"
        super().init(context)
    
    def pre_execute(self):
        self.mesh = self.inputs["Component"].execute()
        if (self.mesh == None):
            print("DEBUG: " + self.name + ": Empty object recieved")
            return False
        bpy.ops.object.mode_set(mode="OBJECT")
        if (self.inputs["Use Selected Edge"].execute()):
            try:
                self.index = [i.index for i in self.mesh.data.edges if i.select][0]
            except:
                print("DEBUG: " + self.name + ": No edge selected")
                bpy.ops.object.mode_set(mode="EDIT")
                return False
        else:
            self.index = max(min(self.inputs["Edge Index"].execute(), len(self.mesh.data.edges)-1), 0)
        bpy.ops.object.mode_set(mode="EDIT")
        return True
    
    def functionality(self):
        bpy.ops.mesh.loopcut_slide(self.override(), MESH_OT_loopcut={"number_cuts":self.inputs["Number of Cuts"].execute(), "smoothness":self.inputs["Smoothness"].execute(), "falloff":'INVERSE_SQUARE', "edge_index":self.index}, TRANSFORM_OT_edge_slide={"value":self.inputs["Factor"].execute(), "single_side":self.inputs["Single Side"].execute(), "use_even":self.inputs["Even"].execute(), "flipped":self.inputs["Flipped"].execute(), "use_clamp":self.inputs["Clamp"].execute()})
class MaterialNode(Node, ScEditOperatorNode):
    bl_idname = "MaterialNode"
    bl_label = "Material"

    prop_mat = PointerProperty(name="Material", type=bpy.types.Material, update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_mat")
    
    def pre_execute(self):
        if (self.prop_mat == None):
            print("DEBUG: " + self.name + ": No material selected")
            return False
        return super().pre_execute()

    def functionality(self):
        slot = self.mesh.material_slots.find(self.prop_mat.name)
        if (slot == -1):
            bpy.ops.object.material_slot_add()
            self.mesh.active_material = self.prop_mat
        else:
            self.mesh.active_material_index = slot
        bpy.ops.object.material_slot_assign()
class MergeComponentsNode(Node, ScEditOperatorNode):
    bl_idname = "MergeComponentsNode"
    bl_label = "Merge Components"
    
    prop_type = EnumProperty(name="Type", items=[("CENTER", "Center", ""), ("CURSOR", "Cursor", ""), ("COLLAPSE", "Collapse", "")], default="CENTER", update=ScNode.update_value)
    prop_uv = BoolProperty(name="UVs", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "UVs").prop_prop = "prop_uv"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")

    def functionality(self):
        bpy.ops.mesh.merge(type=self.prop_type, uvs=self.inputs["UVs"].execute())
class OffsetEdgeLoopNode(Node, ScEditOperatorNode):
    bl_idname = "OffsetEdgeLoopNode"
    bl_label = "Offset Edge Loop"
    
    prop_cap = BoolProperty(name="Cap Endpoint", update=ScNode.update_value)
    prop_factor = FloatProperty(name="Factor", default=0.523187, min=-1.0, max=1.0, update=ScNode.update_value)
    prop_single = BoolProperty(name="Single Side", update=ScNode.update_value)
    prop_even = BoolProperty(name="Even", update=ScNode.update_value)
    prop_flipped = BoolProperty(name="Flipped", update=ScNode.update_value)
    prop_clamp = BoolProperty(name="Clamp", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Cap Endpoint").prop_prop = "prop_cap"
        self.inputs.new("ScFloatSocket", "Factor").prop_prop = "prop_factor"
        self.inputs.new("ScBoolSocket", "Single Side").prop_prop = "prop_single"
        self.inputs.new("ScBoolSocket", "Even").prop_prop = "prop_even"
        self.inputs.new("ScBoolSocket", "Flipped").prop_prop = "prop_flipped"
        self.inputs.new("ScBoolSocket", "Clamp").prop_prop = "prop_clamp"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.offset_edge_loops_slide(self.override(), MESH_OT_offset_edge_loops={"use_cap_endpoint":self.inputs["Cap Endpoint"].execute()}, TRANSFORM_OT_edge_slide={"value":self.inputs["Factor"].execute(), "single_side":self.inputs["Single Side"].execute(), "use_even":self.inputs["Even"].execute(), "flipped":self.inputs["Flipped"].execute(), "use_clamp":self.inputs["Clamp"].execute()})
class PokeNode(Node, ScEditOperatorNode):
    bl_idname = "PokeNode"
    bl_label = "Poke"

    prop_offset = FloatProperty(name="Poke Offset", default=0.0, min=-1000.0, max=1000.0, update=ScNode.update_value)
    prop_use_relative_offset = BoolProperty(name="Relative Offset", update=ScNode.update_value)
    prop_center_mode = EnumProperty(name="Poke Center", items=[("MEAN_WEIGHTED", "Mean Weighted", ""), ("MEAN", "Mean", ""), ("BOUNDS", "Bounds", "")], default="MEAN_WEIGHTED", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Poke Offset").prop_prop = "prop_offset"
        self.inputs.new("ScBoolSocket", "Relative Offset").prop_prop = "prop_use_relative_offset"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_center_mode")
    
    def functionality(self):
        bpy.ops.mesh.poke(offset=self.inputs["Poke Offset"].execute(), use_relative_offset=self.inputs["Relative Offset"].execute(), center_mode=self.prop_center_mode)
class RemoveDoublesNode(Node, ScEditOperatorNode): # Contributed by @lucaspedrajas
    bl_idname = "RemoveDoublesNode"
    bl_label = "Remove Doubles"

    prop_threshold = FloatProperty(name="Threshold", default=0.0001, min=0.000001, max=50.0, update=ScNode.update_value)
    prop_unselected = BoolProperty(name="Unselected", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Threshold").prop_prop = "prop_threshold"
        self.inputs.new("ScBoolSocket", "Unselected").prop_prop = "prop_unselected"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.remove_doubles(threshold=self.inputs["Threshold"].execute(), use_unselected=self.inputs["Unselected"].execute())
class RotateEdgeNode(Node, ScEditOperatorNode):
    bl_idname = "RotateEdgeNode"
    bl_label = "Rotate Edge"
    
    prop_ccw = BoolProperty(name="Counter Clockwise", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Counter Clockwise").prop_prop = "prop_ccw"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.edge_rotate(use_ccw=self.inputs["Counter Clockwise"].execute())
class ScrewNode(Node, ScEditOperatorNode):
    bl_idname = "ScrewNode"
    bl_label = "Screw"

    prop_steps = IntProperty(name="Steps",default=9, min=1, max=100000, update=ScNode.update_value)
    prop_turns = IntProperty(name="Turns",default=1, min=1, max=100000, update=ScNode.update_value)
    prop_center = FloatVectorProperty(name="Center", update=ScNode.update_value)
    prop_axis = FloatVectorProperty(name="Axis", default=(1.0, 0.0, 0.0), min=-1.0, max=1.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Steps").prop_prop = "prop_steps"
        self.inputs.new("ScIntSocket", "Turns").prop_prop = "prop_turns"
        self.inputs.new("ScFloatVectorSocket", "Center").prop_prop = "prop_center"
        self.inputs.new("ScFloatVectorSocket", "Axis").prop_prop = "prop_axis"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.screw(steps=self.inputs["Steps"].execute(), turns=self.inputs["Turns"].execute(), center=self.inputs["Center"].execute(), axis=self.inputs["Axis"].execute())
class SolidifyNode(Node, ScEditOperatorNode):
    bl_idname = "SolidifyNode"
    bl_label = "Solidify"
    
    prop_thickness = FloatProperty(name="Thickness", default=0.01, min=-10000.0, max=10000.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Thickness").prop_prop = "prop_thickness"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.solidify(thickness=self.inputs["Thickness"].execute())
class SpinNode(Node, ScEditOperatorNode):
    bl_idname = "SpinNode"
    bl_label = "Spin"
    
    prop_steps = IntProperty(name="Steps", default=9, min=0, max=1000000, update=ScNode.update_value)
    prop_dupli = BoolProperty(name="Duplicate", update=ScNode.update_value)
    prop_angle = FloatProperty(name="Angle", default=1.5708, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    prop_center = FloatVectorProperty(name="Center", update=ScNode.update_value)
    prop_axis = FloatVectorProperty(name="Axis", min=-1.0, max=1.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Steps").prop_prop = "prop_steps"
        self.inputs.new("ScBoolSocket", "Dupli").prop_prop = "prop_dupli"
        self.inputs.new("ScAngleSocket", "Angle").prop_prop = "prop_angle"
        self.inputs.new("ScFloatVectorSocket", "Center").prop_prop = "prop_center"
        self.inputs.new("ScFloatVectorSocket", "Axis").prop_prop = "prop_axis"
        super().init(context)
    
    def functionality(self):
        bpy.ops.mesh.spin(steps=self.inputs["Steps"].execute(), dupli=self.inputs["Dupli"].execute(), angle=self.inputs["Angle"].execute(), center=self.inputs["Center"].execute(), axis=self.inputs["Axis"].execute())
class SplitNode(Node, ScEditOperatorNode):
    bl_idname = "SplitNode"
    bl_label = "Split"

    prop_individual = BoolProperty(name="Individual", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Individual").prop_prop = "prop_individual"
        super().init(context)

    def functionality(self):
        if (self.inputs["Individual"].execute()):
            bpy.ops.mesh.edge_split()
        else:
            bpy.ops.mesh.split()
class SubdivideNode(Node, ScEditOperatorNode):
    bl_idname = "SubdivideNode"
    bl_label = "Subdivide"

    prop_number_cuts = IntProperty(name="Number of Cuts", default=1, min=1, max=100, update=ScNode.update_value)
    prop_smoothness = FloatProperty(name="Smoothness", default=0.0, min=0.0, max=1000.0, update=ScNode.update_value)
    prop_quadtri = BoolProperty(name="Quad/Tri Mode", update=ScNode.update_value)
    prop_quadcorner = EnumProperty(name="Quad Corner Type", items=[("INNERVERT", "Inner Vertices", ""), ("PATH", "Path", ""), ("STRAIGHT_CUT", "Straight Cut", ""), ("FAN", "Fan", "")], default="STRAIGHT_CUT", update=ScNode.update_value)
    prop_fractal = FloatProperty(name="Fractal", default=0.0, min=0.0, max=1000000, update=ScNode.update_value)
    prop_fractal_along_normal = FloatProperty(name="Along Normal", default=0.0, min=0.0, max=1.0, update=ScNode.update_value)
    prop_seed = IntProperty(name="Random Seed", default=0, min=0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Number of Cuts").prop_prop = "prop_number_cuts"
        self.inputs.new("ScFloatSocket", "Smoothness").prop_prop = "prop_smoothness"
        self.inputs.new("ScBoolSocket", "Quad/Tri Mode").prop_prop = "prop_quadtri"
        self.inputs.new("ScFloatSocket", "Fractal").prop_prop = "prop_fractal"
        self.inputs.new("ScFloatSocket", "Along Normal").prop_prop = "prop_fractal_along_normal"
        self.inputs.new("ScIntSocket", "Random Seed").prop_prop = "prop_seed"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_quadcorner")
    
    def functionality(self):
        bpy.ops.mesh.subdivide(number_cuts=self.inputs["Number of Cuts"].execute(), smoothness=self.inputs["Smoothness"].execute(), quadtri=self.inputs["Quad/Tri Mode"].execute(), quadcorner=self.prop_quadcorner, fractal=self.inputs["Fractal"].execute(), fractal_along_normal=self.inputs["Along Normal"].execute(), seed=self.inputs["Random Seed"].execute())
class SymmetrizeNode(Node, ScEditOperatorNode):
    bl_idname = "SymmetrizeNode"
    bl_label = "Symmetrize"
    
    prop_direction = EnumProperty(name="Direction", items=[("NEGATIVE_X", "-X", ""), ("POSITIVE_X", "X", ""), ("NEGATIVE_Y", "-Y", ""), ("POSITIVE_Y", "Y", ""), ("NEGATIVE_Z", "-Z", ""), ("POSITIVE_Z", "Z", "")], default="NEGATIVE_X", update=ScNode.update_value)
    prop_threshold = FloatProperty(name="Threshold", default=0.0001, min=0.0, max=10.0, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Threshold").prop_prop = "prop_threshold"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_direction")

    def functionality(self):
        bpy.ops.mesh.symmetrize(direction=self.prop_direction, threshold=self.inputs["Threshold"].execute())
class TriangulateFacesNode(Node, ScEditOperatorNode):
    bl_idname = "TriangulateFacesNode"
    bl_label = "Triangulate Faces"
    
    prop_quad = EnumProperty(name="Quad Method", items=[("BEAUTY", "Beauty", ""), ("FIXED", "Fixed", ""), ("FIXED_ALTERNATE", "Fixed Alternate", ""), ("SHORTEST_DIAGONAL", "Shortest Diagonal", "")], default="BEAUTY", update=ScNode.update_value)
    prop_ngon = EnumProperty(name="Polygon Method", items=[("BEAUTY", "Beauty", ""), ("CLIP", "Clip", "")], default="BEAUTY", update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_quad")
        layout.prop(self, "prop_ngon")

    def functionality(self):
        bpy.ops.mesh.quads_convert_to_tris(quad_method=self.prop_quad, ngon_method=self.prop_ngon)
class UnSubdivideNode(Node, ScEditOperatorNode):
    bl_idname = "UnSubdivideNode"
    bl_label = "Un-Subdivide"
    
    prop_iterations = IntProperty(name="Iterations", default=2, min=1, max=1000, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Iterations").prop_prop = "prop_iterations"
        super().init(context)

    def functionality(self):
        bpy.ops.mesh.unsubdivide(iterations=self.inputs["Iterations"].execute())
class VertexGroupNode(Node, ScEditOperatorNode):
    bl_idname = "VertexGroupNode"
    bl_label = "Vertex Group"

    prop_vg = StringProperty(default="Group", update=ScNode.update_value)
    prop_assign = BoolProperty(default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScStringSocket", "Vertex Group").prop_prop = "prop_vg"
        self.inputs.new("ScBoolSocket", "Assign").prop_prop = "prop_assign"
        super().init(context)
    
    def functionality(self):
        name = self.inputs["Vertex Group"].execute()
        slot = self.mesh.vertex_groups.find(name)
        if (slot == -1):
            bpy.ops.object.vertex_group_add()
            self.mesh.vertex_groups.active.name = name
        else:
            self.mesh.vertex_groups.active_index = slot
        if (self.inputs["Assign"].execute()):
            bpy.ops.object.vertex_group_assign()
        else:
            bpy.ops.object.vertex_group_remove_from()
# Mesh Operators
class ApplyTransformNode(Node, ScObjectOperatorNode):
    bl_idname = "ApplyTransformNode"
    bl_label = "Apply Transform"

    prop_transform = EnumProperty(items=[("LOCATION", "Location", "", 2), ("ROTATION", "Rotation", "", 4), ("SCALE", "Scale", "", 8)], default={"LOCATION"}, options={"ENUM_FLAG"}, update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_transform", expand=True)
    
    def functionality(self):
        bpy.ops.object.transform_apply(location="LOCATION" in self.prop_transform, rotation="ROTATION" in self.prop_transform, scale="SCALE" in self.prop_transform)
class CopyTransformNode(Node, ScObjectOperatorNode):
    bl_idname = "CopyTransformNode"
    bl_label = "Copy Transform"

    prop_object = PointerProperty(type=bpy.types.Object, update=ScNode.update_value)
    prop_transform = EnumProperty(items=[("LOCATION", "Location", "", 2), ("ROTATION", "Rotation", "", 4), ("SCALE", "Scale", "", 8)], default={"LOCATION"}, options={"ENUM_FLAG"}, update=ScNode.update_value)
    obj = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScMeshRefSocket", "Object").prop_prop = "prop_object"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_transform", expand=True)
    
    def pre_execute(self):
        self.obj = self.inputs["Object"].execute()
        if (self.obj == None):
            print("DEBUG: " + self.name + ": Empty secondary object recieved")
            return False
        return super().pre_execute()
    
    def functionality(self):
        if ("LOCATION" in self.prop_transform):
            self.mesh.location = self.obj.location
        if ("ROTATION" in self.prop_transform):
            self.mesh.rotation_euler = self.obj.rotation_euler
        if ("SCALE" in self.prop_transform):
            self.mesh.scale = self.obj.scale
class DrawModeNode(Node, ScObjectOperatorNode):
    bl_idname = "DrawModeNode"
    bl_label = "Draw Mode"

    prop_name = BoolProperty(name="Name", update=ScNode.update_value)
    prop_wire = BoolProperty(name="Wire", update=ScNode.update_value)
    prop_xray = BoolProperty(name="X-Ray", update=ScNode.update_value)
    prop_transparency = BoolProperty(name="Transparency", update=ScNode.update_value)
    prop_max_draw_type = EnumProperty(name="Maximum Draw Type", items=[("SOLID", "Solid", ""), ("WIRE", "Wire", ""), ("BOUNDS", "Bounds", "")], default="SOLID", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Name").prop_prop = "prop_name"
        self.inputs.new("ScBoolSocket", "Wire").prop_prop = "prop_wire"
        self.inputs.new("ScBoolSocket", "X-Ray").prop_prop = "prop_xray"
        self.inputs.new("ScBoolSocket", "Transparency").prop_prop = "prop_transparency"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.label("Maximum Draw Type:")
        layout.prop(self, "prop_max_draw_type", expand=True)
    
    def functionality(self):
        self.mesh.show_name = self.inputs["Name"].execute()
        self.mesh.show_wire = self.inputs["Wire"].execute()
        self.mesh.show_x_ray = self.inputs["X-Ray"].execute()
        self.mesh.show_transparent = self.inputs["Transparency"].execute()
        self.mesh.draw_type = self.prop_max_draw_type
class MakeLinksNode(Node, ScObjectOperatorNode):
    bl_idname = "MakeLinksNode"
    bl_label = "Make Links"

    prop_type = EnumProperty(items=[("OBDATA", "Object Data", ""), ("MATERIAL", "Material", ""), ("ANIMATION", "Animation", ""), ("GROUPS", "Groups", ""), ("DUPLIGROUP", "Dupligroup", ""), ("MODIFIERS", "Modifiers", ""), ("FONTS", "Fonts", "")], default="OBDATA", update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_type", expand=True)
    
    def functionality(self):
        bpy.ops.object.make_links_data(type=self.prop_type)
# class MergeMeshesNode(Node, ScNode):
#     bl_idname = "MergeMeshesNode"
#     bl_label = "Merge Meshes"

#     def select_meshes(self, meshes, value=True):
#         for mesh in meshes:
#             bpy.data.objects[mesh].select = value
#         self.mesh.select = True
#         bpy.context.scene.objects.active = self.mesh

#     def init(self, context):
#         self.inputs.new("MeshSocket", "Mesh")
#         self.inputs.new("MeshArraySocket", "Mesh").link_limit = 1000
#         self.outputs.new("MeshSocket", "Mesh")
    
#     def execute(self):
#         if (not self.inputs[0].is_linked):
#             print("DEBUG: " + self.name + ": Not linked")
#             return ""
#         self.mesh = self.inputs[0].links[0].from_node.execute()
#         if (self.mesh == ""):
#             print("DEBUG: " + self.name + ": Empty object recieved")
#             return self.mesh
#         if (not self.inputs[1].is_linked):
#             print("DEBUG: " + self.name + ":Mesh array not linked")
#             return self.mesh
#         meshes = []
#         for link in self.inputs[1].links:
#             if (link.from_node.mesh == self.mesh):
#                 print("DEBUG: " + self.name + ": Cannot merge to self")
#                 self.select_meshes(meshes, False)
#                 return self.mesh
#             mesh = link.from_node.execute()
#             if (mesh == ""):
#                 print("DEBUG: " + self.name + ": Empty object recieved")
#                 self.select_meshes(meshes, False)
#                 return self.mesh
#             meshes.append(mesh)
#         self.select_meshes(meshes)
#         self.functionality()
#         return self.mesh
    
#     def functionality(self):
#         bpy.ops.object.join()
class OriginNode(Node, ScObjectOperatorNode):
    bl_idname = "OriginNode"
    bl_label = "Origin"

    prop_type = EnumProperty(name="Type", items=[("GEOMETRY_ORIGIN", "Geometry to Origin", ""), ("ORIGIN_GEOMETRY", "Origin to Geometry", ""), ("ORIGIN_CURSOR", "Origin to 3D Cursor", ""), ("ORIGIN_CENTER_OF_MASS", "Origin to Center of Mass (Surface)", ""), ("ORIGIN_CENTER_OF_VOLUME", "Origin to Center of Mass (Volume)", "")], default="GEOMETRY_ORIGIN", update=ScNode.update_value)
    prop_center = EnumProperty(name="Center", items=[("MEDIAN", "Median", ""), ("BOUNDS", "Bounds", "")], default="MEDIAN", update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
        layout.prop(self, "prop_center", expand=True)
    
    def functionality(self):
        bpy.ops.object.origin_set(type=self.prop_type, center=self.prop_center)
class ShadingNode(Node, ScObjectOperatorNode):
    bl_idname = "ShadingNode"
    bl_label = "Shading"

    prop_shading = EnumProperty(name="Shading", items=[("SMOOTH", "Smooth", ""), ("FLAT", "Flat", "")], default="FLAT", update=ScNode.update_value)
    prop_auto = BoolProperty(name="Auto Smooth", update=ScNode.update_value)
    prop_angle = FloatProperty(name="Angle", default=0.523599, min=0.0, max=3.14159, subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScBoolSocket", "Auto Smooth").prop_prop = "prop_auto"
        self.inputs.new("ScFloatSocket", "Angle").prop_prop = "prop_angle"
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_shading", expand=True)
    
    def functionality(self):
        if (self.prop_shading == "FLAT"):
            bpy.ops.object.shade_flat()
        else:
            bpy.ops.object.shade_smooth()
        self.mesh.data.use_auto_smooth = self.inputs["Auto Smooth"].execute()
        self.mesh.data.auto_smooth_angle = self.inputs["Angle"].execute()
# Constants
class FloatNode(Node, ScConstantNode):
    bl_idname = "FloatNode"
    bl_label = "Float"

    prop_float = FloatProperty(name="Float", update=ScNode.update_value)

    def init(self, context):
        self.outputs.new("ScFloatSocket", "Float")
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_float")
    
    def post_execute(self):
        return self.prop_float
class IntNode(Node, ScConstantNode):
    bl_idname = "IntNode"
    bl_label = "Integer"

    prop_int = IntProperty(name="Integer", update=ScNode.update_value)

    def init(self, context):
        self.outputs.new("ScIntSocket", "Integer")
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_int")
    
    def post_execute(self):
        return self.prop_int
class BoolNode(Node, ScConstantNode):
    bl_idname = "BoolNode"
    bl_label = "Boolean"

    prop_bool = BoolProperty(name="Boolean", update=ScNode.update_value)

    def init(self, context):
        self.outputs.new("ScBoolSocket", "Boolean")
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_bool")
    
    def post_execute(self):
        return self.prop_bool
class AngleNode(Node, ScConstantNode):
    bl_idname = "AngleNode"
    bl_label = "Angle"

    prop_angle = FloatProperty(name="Angle", subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)

    def init(self, context):
        self.outputs.new("ScAngleSocket", "Angle")
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_angle")
    
    def post_execute(self):
        return self.prop_angle
class FloatVectorNode(Node, ScConstantNode):
    bl_idname = "FloatVectorNode"
    bl_label = "Float Vector"

    prop_x = FloatProperty(name="X", update=ScNode.update_value)
    prop_y = FloatProperty(name="Y", update=ScNode.update_value)
    prop_z = FloatProperty(name="Z", update=ScNode.update_value)
    prop_uniform = EnumProperty(name="Uniform", items=[("NONE", "None", ""), ("XY", "XY", ""), ("YZ", "YZ", ""), ("XZ", "XZ", ""), ("XYZ", "XYZ", "")], default="NONE", update=ScNode.update_value)
    prop_vector = FloatVectorProperty()

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_uniform")

    def init(self, context):
        self.inputs.new("ScFloatSocket", "X").prop_prop = "prop_x"
        self.inputs.new("ScFloatSocket", "Y").prop_prop = "prop_y"
        self.inputs.new("ScFloatSocket", "Z").prop_prop = "prop_z"
        self.outputs.new("ScFloatVectorSocket", "Float Vector")
        super().init(context)
    
    def functionality(self):
        if (self.prop_uniform == "NONE"):
            self.prop_vector = (self.inputs["X"].execute(), self.inputs["Y"].execute(), self.inputs["Z"].execute())
        elif (self.prop_uniform == "XY"):
            self.prop_vector[0] = self.inputs["X"].execute()
            self.prop_vector[1] = self.prop_vector[0]
            self.prop_vector[2] = self.inputs["Z"].execute()
        elif (self.prop_uniform == "YZ"):
            self.prop_vector[0] = self.inputs["X"].execute()
            self.prop_vector[1] = self.inputs["Y"].execute()
            self.prop_vector[2] = self.prop_vector[1]
        elif (self.prop_uniform == "XZ"):
            self.prop_vector[0] = self.inputs["X"].execute()
            self.prop_vector[1] = self.inputs["Y"].execute()
            self.prop_vector[2] = self.prop_vector[0]
        else:
            self.prop_vector[0] = self.inputs["X"].execute()
            self.prop_vector[1] = self.prop_vector[0]
            self.prop_vector[2] = self.prop_vector[0]
    
    def post_execute(self):
        return self.prop_vector
class AngleVectorNode(Node, ScConstantNode):
    bl_idname = "AngleVectorNode"
    bl_label = "Angle Vector"

    prop_x = FloatProperty(name="X", subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    prop_y = FloatProperty(name="Y", subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    prop_z = FloatProperty(name="Z", subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    prop_uniform = EnumProperty(name="Uniform", items=[("NONE", "None", ""), ("XY", "XY", ""), ("YZ", "YZ", ""), ("XZ", "XZ", ""), ("XYZ", "XYZ", "")], default="NONE", update=ScNode.update_value)
    prop_vector = FloatVectorProperty(unit="ROTATION")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_uniform")

    def init(self, context):
        self.inputs.new("ScAngleSocket", "X").prop_prop = "prop_x"
        self.inputs.new("ScAngleSocket", "Y").prop_prop = "prop_y"
        self.inputs.new("ScAngleSocket", "Z").prop_prop = "prop_z"
        self.outputs.new("ScAngleVectorSocket", "Angle Vector")
        super().init(context)
    
    def functionality(self):
        if (self.prop_uniform == "NONE"):
            self.prop_vector = (self.inputs["X"].execute(), self.inputs["Y"].execute(), self.inputs["Z"].execute())
        elif (self.prop_uniform == "XY"):
            self.prop_vector[0] = self.inputs["X"].execute()
            self.prop_vector[1] = self.prop_vector[0]
            self.prop_vector[2] = self.inputs["Z"].execute()
        elif (self.prop_uniform == "YZ"):
            self.prop_vector[0] = self.inputs["X"].execute()
            self.prop_vector[1] = self.inputs["Y"].execute()
            self.prop_vector[2] = self.prop_vector[1]
        elif (self.prop_uniform == "XZ"):
            self.prop_vector[0] = self.inputs["X"].execute()
            self.prop_vector[1] = self.inputs["Y"].execute()
            self.prop_vector[2] = self.prop_vector[0]
        else:
            self.prop_vector[0] = self.inputs["X"].execute()
            self.prop_vector[1] = self.prop_vector[0]
            self.prop_vector[2] = self.prop_vector[0]
    
    def post_execute(self):
        return self.prop_vector
class RandomFloatNode(Node, ScConstantNode):
    bl_idname = "RandomFloatNode"
    bl_label = "Random Float"

    prop_min = FloatProperty(name="Min", update=ScNode.update_value)
    prop_max = FloatProperty(name="Max", default=1.0, update=ScNode.update_value)
    prop_seed = IntProperty(name="Seed", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "Min").prop_prop = "prop_min"
        self.inputs.new("ScFloatSocket", "Max").prop_prop = "prop_max"
        self.inputs.new("ScIntSocket", "Seed").prop_prop = "prop_seed"
        self.outputs.new("ScFloatSocket", "Value")
        super().init(context)
    
    def functionality(self):
        if (self.first_time):
            random.seed(self.inputs["Seed"].execute())
    
    def post_execute(self):
        return random.uniform(self.inputs["Min"].execute(), self.inputs["Max"].execute())
class RandomIntNode(Node, ScConstantNode):
    bl_idname = "RandomIntNode"
    bl_label = "Random Integer"

    prop_min = IntProperty(name="Min", default=1, update=ScNode.update_value)
    prop_max = IntProperty(name="Max", default=5, update=ScNode.update_value)
    prop_seed = IntProperty(name="Seed", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Min").prop_prop = "prop_min"
        self.inputs.new("ScIntSocket", "Max").prop_prop = "prop_max"
        self.inputs.new("ScIntSocket", "Seed").prop_prop = "prop_seed"
        self.outputs.new("ScIntSocket", "Value")
        super().init(context)
    
    def functionality(self):
        if (self.first_time):
            random.seed(self.inputs["Seed"].execute())
    
    def post_execute(self):
        return random.randint(self.inputs["Min"].execute(), self.inputs["Max"].execute())
class RandomBoolNode(Node, ScConstantNode):
    bl_idname = "RandomBoolNode"
    bl_label = "Random Boolean"

    prop_seed = IntProperty(name="Seed", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScIntSocket", "Seed").prop_prop = "prop_seed"
        self.outputs.new("ScBoolSocket", "Value")
        super().init(context)
    
    def functionality(self):
        if (self.first_time):
            random.seed(self.inputs["Seed"].execute())
    
    def post_execute(self):
        return bool(random.getrandbits(1))
class RandomAngleNode(Node, ScConstantNode):
    bl_idname = "RandomAngleNode"
    bl_label = "Random Angle"

    prop_min = FloatProperty(name="Min", subtype="ANGLE", unit="ROTATION", update=ScNode.update_value)
    prop_max = FloatProperty(name="Max", subtype="ANGLE", unit="ROTATION", default=3.14159, update=ScNode.update_value)
    prop_seed = IntProperty(name="Seed", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScAngleSocket", "Min").prop_prop = "prop_min"
        self.inputs.new("ScAngleSocket", "Max").prop_prop = "prop_max"
        self.inputs.new("ScIntSocket", "Seed").prop_prop = "prop_seed"
        self.outputs.new("ScAngleSocket", "Value")
        super().init(context)
    
    def functionality(self):
        if (self.first_time):
            random.seed(self.inputs["Seed"].execute())
    
    def post_execute(self):
        return random.uniform(self.inputs["Min"].execute(), self.inputs["Max"].execute())
class StringNode(Node, ScConstantNode):
    bl_idname = "StringNode"
    bl_label = "String"

    prop_string = StringProperty(name="String", update=ScNode.update_value)

    def init(self, context):
        self.outputs.new("ScStringSocket", "String")
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_string")
    
    def post_execute(self):
        return self.prop_string
# Utilities
class PrintDataNode(Node, ScUtilityNode):
    bl_idname = "PrintDataNode"
    bl_label = "Print Data (Debug)"

    prop_value = FloatProperty(name="Value", update=ScNode.update_value)
    prop_list = BoolProperty(name="List")

    def init(self, context):
        self.inputs.new("ScUniversalSocket", "Value").prop_prop = "prop_value"
        self.inputs.new("ScBoolSocket", "List").prop_prop = "prop_list"
        self.outputs.new("ScUniversalSocket", "Value")
        super().init(context)
    
    def draw_buttons(self, context, layout):
        if (self == self.id_data.nodes.active):
            layout.operator("sc.execute_node_op", "Print")

    def execute(self):
        temp = self.inputs["Value"].execute()
        if (self.inputs["List"].execute()):
            print(list(temp))
        else:
            print(temp)
        return temp
class MathsOpNode(Node, ScUtilityNode):
    bl_idname = "MathsOpNode"
    bl_label = "Maths Operation"

    prop_op = EnumProperty(name="Opertion", items=[("ADD", "+", ""), ("SUB", "-", ""), ("MULT", "*", "")], default="ADD", update=ScNode.update_value)
    prop_x = FloatProperty(name="X", update=ScNode.update_value)
    prop_y = FloatProperty(name="Y", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatSocket", "X").prop_prop = "prop_x"
        self.inputs.new("ScFloatSocket", "Y").prop_prop = "prop_y"
        self.outputs.new("ScFloatSocket", "Sum")
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_op")
    
    def execute(self):
        if (self.prop_op == "ADD"):
            return self.inputs["X"].execute() + self.inputs["Y"].execute()
        elif(self.prop_op == "SUB"):
            return self.inputs["X"].execute() - self.inputs["Y"].execute()
        elif(self.prop_op == "MULT"):
            return self.inputs["X"].execute() * self.inputs["Y"].execute()
# Flow Control
class BeginForLoopNode(Node, ScControlNode):
    bl_idname = "BeginForLoopNode"
    bl_label = "Begin For Loop"

    mesh = PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.inputs.new("ScComponentSocket", "Component")
        self.outputs.new("ScInfoSocket", "End For Loop")
        self.outputs.new("ScComponentSocket", "Component")
        super().init(context)

    def pre_execute(self):
        if (not self.outputs[0].is_linked):
            print("DEBUG: " + self.name + ": End For Loop not found")
            return False
        if (self.first_time):
            self.mesh = self.inputs["Component"].execute()
            if (self.mesh == None):
                print("DEBUG: " + self.name + ": Empty object recieved")
                return False
        return True
    
    def post_execute(self):
        return self.mesh
class EndForLoopNode(Node, ScControlNode):
    bl_idname = "EndForLoopNode"
    bl_label = "End For Loop"

    mesh = PointerProperty(type=bpy.types.Object)

    prop_start = IntProperty(name="Start", default=1, update=ScNode.update_value)
    prop_end = IntProperty(name="End", default=3, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScInfoSocket", "Begin For Loop")
        self.inputs.new("ScComponentSocket", "Component")
        self.inputs.new("ScIntSocket", "Start").prop_prop = "prop_start"
        self.inputs.new("ScIntSocket", "End").prop_prop = "prop_end"
        self.outputs.new("ScComponentSocket", "Component")
        super().init(context)
    
    def pre_execute(self):
        if (not self.inputs[0].is_linked):
            print("DEBUG: " + self.name + ": Begin For Loop not found")
            return False
        self.mesh = self.inputs[0].links[0].from_node.outputs["Component"].execute()
        return True
    
    def functionality(self):
        for i in range(self.inputs["Start"].execute(), self.inputs["End"].execute()+1):
            self.mesh = self.inputs["Component"].execute()
            if (self.mesh == None):
                print("DEBUG: " + self.name + ": Empty object recieved")
                return
    
    def post_execute(self):
        return self.mesh
class BeginForEachLoopNode(Node, ScControlNode):
    bl_idname = "BeginForEachLoopNode"
    bl_label = "Begin For-Each Loop"
    
    mesh = PointerProperty(type=bpy.types.Object)
    prop_selection = StringProperty(default="[]")

    def init(self, context):
        self.inputs.new("ScComponentSocket", "Component")
        self.outputs.new("ScInfoSocket", "End For-Each Loop")
        self.outputs.new("ScComponentSocket", "Component")
        super().init(context)

    def pre_execute(self):
        if (not self.outputs[0].is_linked):
            print("DEBUG: " + self.name + ": End For-Each Loop not found")
            return False
        if (self.first_time):
            self.mesh = self.inputs["Component"].execute()
            if (self.mesh == None):
                print("DEBUG: " + self.name + ": Empty object recieved")
                return False
            bpy.ops.object.mode_set(mode="OBJECT")
            self.prop_selection = str([i.index for i in self.mesh.data.polygons if i.select])
            bpy.ops.object.mode_set(mode="EDIT")
            if (self.prop_selection == "[]"):
                print("DEBUG: " + self.name + ": No face selected")
                return False
        return True

    def functionality(self):
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        temp_list = toList(self.prop_selection)
        self.mesh.data.polygons[temp_list.pop()].select = True
        self.prop_selection = str(temp_list)
    
    def post_execute(self):
        if (self.prop_selection == "[]"):
            self.outputs[0].links[0].to_node.last_time = True
        bpy.ops.object.mode_set(mode="EDIT")
        return self.mesh
class EndForEachLoopNode(Node, ScControlNode):
    bl_idname = "EndForEachLoopNode"
    bl_label = "End For-Each Loop"

    mesh = PointerProperty(type=bpy.types.Object)
    last_time = BoolProperty()
    prop_selection = StringProperty(default="[]")

    def init(self, context):
        self.inputs.new("ScInfoSocket", "Begin For-Each Loop")
        self.inputs.new("ScComponentSocket", "Component")
        self.outputs.new("ScComponentSocket", "Component")
        super().init(context)
    
    def pre_execute(self):
        if (not self.inputs[0].is_linked):
            print("DEBUG: " + self.name + ": Begin For-Each Loop not found")
            return False
        self.prop_selection = "[]"
        return True
    
    def functionality(self):
        while(not self.last_time):
            self.mesh = self.inputs["Component"].execute()
            if (self.mesh == None):
                print("DEBUG: " + self.name + ": Empty object recieved")
                return
            bpy.ops.object.mode_set(mode="OBJECT")
            try:
                temp_index = [i.index for i in self.mesh.data.polygons if i.select][0]
                temp_list = toList(self.prop_selection)
                temp_list.append(temp_index)
                self.prop_selection = str(temp_list)
            except:
                print("DEBUG: " + self.name + ": No face selected")
            bpy.ops.object.mode_set(mode="EDIT")
    
    def post_execute(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        for i in toList(self.prop_selection):
            self.mesh.data.polygons[i].select = True
        bpy.ops.object.mode_set(mode="EDIT")
        return self.mesh
class IfElseNode(Node, ScControlNode):
    bl_idname = "IfElseNode"
    bl_label = "If-Else"

    prop_bool = BoolProperty(name="Condition", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScUniversalSocket", "True")
        self.inputs.new("ScUniversalSocket", "False")
        self.inputs.new("ScBoolSocket", "Condition").prop_prop = "prop_bool"
        self.outputs.new("ScUniversalSocket", "")
        super().init(context)
    
    def post_execute(self):
        if (self.inputs["Condition"].execute()):
            return self.inputs["True"].execute()
        else:
            return self.inputs["False"].execute()
# Settings
class CursorLocationNode(Node, ScSettingNode):
    bl_idname = "CursorLocationNode"
    bl_label = "Cursor Location"

    prop_location = FloatVectorProperty(name="Location", update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScFloatVectorSocket", "Location").prop_prop = "prop_location"
        super().init(context)
    
    def functionality(self):
        self.override()["space"].cursor_location = self.inputs["Location"].execute()
class OrientationNode(Node, ScSettingNode):
    bl_idname = "OrientationNode"
    bl_label = "Transform Orientation"

    prop_orientation = EnumProperty(name="Pivot Point", items=[("GLOBAL", "Global", ""), ("LOCAL", "Local", ""), ("NORMAL", "Normal", ""), ("GIMBAL", "Gimbal", ""), ("VIEW", "View", "")], default="GLOBAL", update=ScNode.update_value)
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_orientation", expand=True)
    
    def functionality(self):
        self.override()["space"].transform_orientation = self.prop_orientation
class PivotNode(Node, ScSettingNode):
    bl_idname = "PivotNode"
    bl_label = "Pivot Center"

    prop_pivot = EnumProperty(name="Pivot Point", items=[("BOUNDING_BOX_CENTER", "Bound Box Center", ""), ("CURSOR", "Cursor", ""), ("INDIVIDUAL_ORIGINS", "Individual Origins", ""), ("MEDIAN_POINT", "Median Point", ""), ("ACTIVE_ELEMENT", "Active Element", "")], default="MEDIAN_POINT", update=ScNode.update_value)

    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_pivot", expand=True)
    
    def functionality(self):
        self.override()['space'].pivot_point = self.prop_pivot
class CustomPythonNode(Node, ScSettingNode):
    bl_idname = "CustomPythonNode"
    bl_label = "Custom Python Script"

    prop_script = StringProperty(name="Script", description="Variables to use: _OBJ (active object), _OVERRIDE, _M (bpy.ops.mesh), _O (bpy.ops.object), [;] - separator", update=ScNode.update_value)
    prop_iterations = IntProperty(name="Iterations", default=1, min=1, max=1000, update=ScNode.update_value)
    prop_print = BoolProperty(name="Print Script", default=True, update=ScNode.update_value)

    def init(self, context):
        self.inputs.new("ScStringSocket", "Script").prop_prop = "prop_script"
        self.inputs.new("ScIntSocket", "Iterations").prop_prop = "prop_iterations"
        super().init(context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_print")
    
    def functionality(self):
        _OBJ = bpy.context.active_object
        _OVERRIDE = self.override()
        _M = bpy.ops.mesh
        _O = bpy.ops.object
        script = self.inputs["Script"].execute()
        if (self.prop_print):
            print("SCRIPT: " + script)
        for i in range (0, self.inputs["Iterations"].execute()):
            try:
                exec(script)
            except:
                print("DEBUG: " + self.name + ": Invalid script")
                break
# Output
class RefreshMeshNode(Node, ScOutputNode):
    bl_idname = "RefreshMeshNode"
    bl_label = "Refresh Mesh Output"
    
    print_output = BoolProperty(name="Print Output (Debug)", default=False)
    
    def draw_buttons(self, context, layout):
        if (self == self.id_data.nodes.active):
            layout.operator("sc.execute_node_op", "Refresh Mesh")
        layout.column().prop(self, "print_output")
    
    def functionality(self):
        if (self.print_output):
            print(self.name + ": " + self.mesh.name)
class ExportMeshFBXNode(Node, ScOutputNode):
    bl_idname = "ExportMeshFBXNode"
    bl_label = "Export Mesh (FBX)"

    prop_filepath = StringProperty(name="File Path", default="/path/to/dir/")
    prop_filename = StringProperty(name=" File Name", default="untitled")

    def init(self, context):
        self.inputs.new("ScStringSocket", "File Path").prop_prop = "prop_filepath"
        self.inputs.new("ScStringSocket", "File Name").prop_prop = "prop_filename"
        self.outputs.new("ScMeshSocket", "Mesh")
        super().init(context)
    
    def draw_buttons(self, context, layout):
        if (self == self.id_data.nodes.active):
            layout.operator("sc.execute_node_op", "Export Mesh")

    def functionality(self):
        bpy.ops.export_scene.fbx(filepath=self.inputs["File Path"].execute()+self.inputs["File Name"].execute()+".fbx", use_selection=True, use_tspace=True)
##############################################################


inputs = [PlaneNode, CubeNode, CircleNode, UVSphereNode, IcoSphereNode, CylinderNode, ConeNode, GridNode, SuzanneNode, CustomMeshNode] # TorusNode
transform = [LocationNode, RotationNode, ScaleNode, TranslateNode, RotateNode, ResizeNode]
modifiers = [ArrayModNode, BevelModNode, BooleanModNode, CastModNode, CorrectiveSmoothModNode, CurveModNode, DecimateModNode, DisplaceModNode, EdgeSplitModNode, LaplacianSmoothModNode, MirrorModNode, RemeshModNode, ScrewModNode, SimpleDeformModNode, SkinModNode, SmoothModNode, SolidifyModNode, SubdivideModNode, TriangulateModNode, WireframeModNode]
conversion = [ToComponentNode, ToMeshNode, ChangeModeNode]
selection = [SelectManuallyNode, SelectComponentByIndexNode, SelectFacesByMaterialNode, SelectFacesByNormalNode, SelectVerticesByVertexGroupNode, SelectAllNode, SelectAxisNode, SelectFaceBySidesNode, SelectInteriorFaces, SelectLessNode, SelectMoreNode, SelectLinkedNode, SelectLoopNode, SelectLoopRegionNode, SelectLooseNode, SelectMirrorNode, SelectNextItemNode, SelectPrevItemNode, SelectNonManifoldNode, SelectNthNode, SelectAlternateFacesNode, SelectRandomNode, SelectRegionBoundaryNode, SelectSharpEdgesNode, SelectSimilarNode, SelectSimilarRegionNode, SelectShortestPathNode, SelectUngroupedNode, SelectFacesLinkedFlatNode] # SelectEdgeRingNode
deletion = [DeleteNode, DeleteEdgeLoopNode, DissolveFacesNode, DissolveEdgesNode, DissolveVerticesNode, DissolveDegenerateNode, EdgeCollapseNode]
edit_operators = [AddEdgeFaceNode, BeautifyFillNode, BevelNode, BridgeEdgeLoopsNode, ConvexHullNode, DecimateNode, ExtrudeFacesNode, ExtrudeEdgesNode, ExtrudeVerticesNode, ExtrudeRegionNode, FlipNormalsNode, MakeNormalsConsistentNode, FlattenNode, FillEdgeLoopNode, FillGridNode, FillHolesBySidesNode, InsetNode, LoopCutNode, MaterialNode, MergeComponentsNode, OffsetEdgeLoopNode, PokeNode, RemoveDoublesNode, RotateEdgeNode, ScrewNode, SolidifyNode, SpinNode, SplitNode, SubdivideNode, SymmetrizeNode, TriangulateFacesNode, UnSubdivideNode, VertexGroupNode] # ExtrudeRepeatNode
object_operators = [ApplyTransformNode, CopyTransformNode, DrawModeNode, MakeLinksNode, OriginNode, ShadingNode] # MergeMeshesNode
constants = [FloatNode, IntNode, BoolNode, AngleNode, FloatVectorNode, AngleVectorNode, RandomFloatNode, RandomIntNode, RandomBoolNode, RandomAngleNode, StringNode]
utilities = [PrintDataNode, MathsOpNode]
control = [BeginForLoopNode, EndForLoopNode, BeginForEachLoopNode, EndForEachLoopNode, IfElseNode]
settings = [CursorLocationNode, OrientationNode, PivotNode, CustomPythonNode]
outputs = [RefreshMeshNode, ExportMeshFBXNode]

node_categories = [ScNodeCategory("sc.inputs", "Inputs", items=[NodeItem(i.bl_idname) for i in inputs]),
                   ScNodeCategory("sc.transform", "Transform", items=[NodeItem(i.bl_idname) for i in transform]),
                   ScNodeCategory("sc.modifiers", "Modifiers", items=[NodeItem(i.bl_idname) for i in modifiers]),
                   ScNodeCategory("sc.conversion", "Conversion", items=[NodeItem(i.bl_idname) for i in conversion]),
                   ScNodeCategory("sc.selection", "Selection", items=[NodeItem(i.bl_idname) for i in selection]),
                   ScNodeCategory("sc.deletion", "Deletion", items=[NodeItem(i.bl_idname) for i in deletion]),
                   ScNodeCategory("sc.edit_operators", "Component Operators", items=[NodeItem(i.bl_idname) for i in edit_operators]),
                   ScNodeCategory("sc.object_operators", "Mesh Operators", items=[NodeItem(i.bl_idname) for i in object_operators]),
                   ScNodeCategory("sc.constants", "Constants", items=[NodeItem(i.bl_idname) for i in constants]),
                   ScNodeCategory("sc.utilities", "Utilities", items=[NodeItem(i.bl_idname) for i in utilities]),
                   ScNodeCategory("sc.control", "Flow Control", items=[NodeItem(i.bl_idname) for i in control]),
                   ScNodeCategory("sc.settings", "Settings", items=[NodeItem(i.bl_idname) for i in settings]),
                   ScNodeCategory("sc.outputs", "Outputs", items=[NodeItem(i.bl_idname) for i in outputs])]

def register():
    nodeitems_utils.register_node_categories("ScNodeCategories", node_categories)
    bpy.utils.register_module(__name__)
def unregister():
    nodeitems_utils.unregister_node_categories("ScNodeCategories")
    bpy.utils.unregister_module(__name__)
