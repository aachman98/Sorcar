print("______________________________________________________")
bl_info = {
    "name": "ProcGenMod",
    "author": "Punya Aachman",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "Node Editor",
    "description": "Create procedural meshes using Node Editor",
    "category": "PCG"}

import bpy
import bmesh
import nodeitems_utils

from bpy.types import NodeTree, Node, NodeSocket, Operator
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty, StringProperty, FloatVectorProperty, PointerProperty, BoolVectorProperty
from nodeitems_utils import NodeCategory, NodeItem

class PcgNodeTree(NodeTree):
    bl_idname = 'PcgNodeTree'
    bl_label = 'PCG node tree'
    bl_icon = 'NODETREE'
class PcgNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'PcgNodeTree'
class PcgNode:
    mesh = StringProperty()
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'PcgNodeTree'
    def update_value(self, context):
        bpy.ops.pcg.refresh_mesh_op()
        return None

class PcgInputNode(PcgNode):
    def init(self, context):
        self.outputs.new("MeshSocket", "Mesh")
        self.hide = True
        self.use_custom_color = True
        self.color = (0.5, 0.0, 0.0)
    def execute(self):
        if (not self.mesh == ""):
            try:
                bpy.data.objects.remove(bpy.data.objects[self.mesh])
            except:
                print("Debug: " + self.name + ": Mesh object non-existant")
        self.functionality()
        self.mesh = bpy.context.active_object.name
        return self.mesh
    def functionality(self):
        print("Debug: PcgInputNode: Main functionality of the node")
class PcgTransformNode(PcgNode):
    def init(self, context):
        self.inputs.new("MeshSocket", "Mesh")
        self.outputs.new("MeshSocket", "Mesh")
        self.hide = True
        self.use_custom_color = True
        self.color = (0.0, 0.5, 0.0)
    def execute(self):
        if (not self.inputs[0].is_linked):
            print("Debug: " + self.name + ": Not linked")
            return ""
        self.mesh = self.inputs[0].links[0].from_node.execute()
        if (self.mesh == ""):
            print("Debug: " + self.name + ": Empty object recieved")
            return ""
        self.functionality()
        return self.mesh
    def functionality(self):
        print("Debug: PcgTransformNode: Main functionality of the node")
class PcgModifierNode(PcgNode):
    def init(self, context):
        self.inputs.new("MeshSocket", "Mesh")
        self.outputs.new("MeshSocket", "Mesh")
        self.hide = True
        self.use_custom_color = True
        self.color = (0.0, 0.0, 0.5)
    def execute(self):
        if (not self.inputs[0].is_linked):
            print("Debug: " + self.name + ": Not linked")
            return ""
        self.mesh = self.inputs[0].links[0].from_node.execute()
        if (self.mesh == ""):
            print("Debug: " + self.name + ": Empty object recieved")
            return ""
        bpy.context.scene.objects.active = bpy.data.objects[self.mesh]
        if (not self.functionality()):
            print("Debug: " + self.name + ": Error: Modifier failed to execute")
            return ""
        self.name = bpy.data.objects[self.mesh].modifiers[0].name
        bpy.ops.object.modifier_apply(modifier=self.name)
        return self.mesh
    def functionality(self):
        print("Debug: PcgModifierNode: Main functionality of the node")
        return True
class PcgSelectionNode(PcgNode):
    def init(self, context):
        self.inputs.new("ComponentSocket", "Component")
        self.outputs.new("ComponentSocket", "Component")
        self.hide = True
        self.use_custom_color = True
        self.color = (0.0, 0.5, 0.5)
    def execute(self):
        if (not self.inputs[0].is_linked):
            print("Debug: " + self.name + ": Not linked")
            return ""
        self.mesh = self.inputs[0].links[0].from_node.execute()
        if (self.mesh == ""):
            print("Debug: " + self.name + ": Empty object recieved")
            return ""
        self.functionality()
        return self.mesh
    def functionality(self):
        print("Debug: PcgSelectionNode: Main functionality of the node")
class PcgOperatorNode(PcgNode):
    def init(self, context):
        self.inputs.new("ComponentSocket", "Component")
        self.outputs.new("ComponentSocket", "Component")
        self.hide = True
        self.use_custom_color = True
        self.color = (0.5, 0.0, 0.5)
    def execute(self):
        if (not self.inputs[0].is_linked):
            print("Debug: " + self.name + ": Not linked")
            return ""
        self.mesh = self.inputs[0].links[0].from_node.execute()
        if (self.mesh == ""):
            print("Debug: " + self.name + ": Empty object recieved")
            return ""
        self.functionality()
        return self.mesh
    def functionality(self):
        print("Debug: PcgOperationNode: Main functionality of the node")


########################### SOCKETS ##########################
class MeshSocket(NodeSocket):
    bl_idname = "MeshSocket"
    bl_label = "Mesh"

    def draw(self, context, layout, node, text):
        if (node.mesh == ""):
            layout.label(self.name)
        else:
            layout.label(node.mesh)

    def draw_color(self, context, node):
        return 1, 1, 1, 1
class ComponentSocket(NodeSocket):
    bl_idname = "ComponentSocket"
    bl_label = "Component"

    def draw(self, context, layout, node, text):
        layout.label(self.name)

    def draw_color(self, context, node):
        return 0, 0, 0, 1
##############################################################


######################### HELPER OPS #########################
class GenerateMeshOp(Operator):
    bl_idname = "pcg.generate_mesh_op"
    bl_label = "Execute MeshNode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR"
    
    def execute(self, context):
        node = context.active_node
        if (node == None):
            print("Debug: GenerateMeshOp: No Active Node")
            return {'CANCELLED'}
        node.execute()
        return {'FINISHED'}
class RealtimeMeshOp(Operator):
    bl_idname = "pcg.realtime_mesh_op"
    bl_label = "Realtime Mesh Update"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR"

    def execute(self, context):
        node = context.active_node
        if (not node == None):
            node.execute()
            return {'FINISHED'}
        print("Debug: RealtimeMeshOp: No active node")
        return {'CANCELLED'}

    def modal(self, context, event):
        if (event.type == "ESC"):
            print("Debug: RealtimeMeshOp: STOP")
            return {'FINISHED'}
        self.execute(context)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        print("Debug: RealtimeMeshOp: START")        
        return {'RUNNING_MODAL'}
class SaveSelectionOp(Operator):
    bl_idname = "pcg.save_selection_op"
    bl_label = "Execute MeshNode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR"
    
    def execute(self, context):
        node = context.active_node
        if (node == None):
            print("Debug: SaveSelectionOp: No Active Node")
            return {'CANCELLED'}
        node.save_selection()
        return {'FINISHED'}
##############################################################


########################### NODES ############################
class PlaneNode(Node, PcgInputNode):
    bl_idname = "PlaneNode"
    bl_label = "Plane"
    
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0)
    prop_location = FloatVectorProperty(name="Location")
    prop_rotation = FloatVectorProperty(name="Rotation")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_radius")
        layout.column().separator()
        layout.row().prop(self, "prop_location")
        layout.row().prop(self, "prop_rotation")
    
    def functionality(self):
        bpy.ops.mesh.primitive_plane_add(radius=self.prop_radius, location=self.prop_location, rotation=self.prop_rotation)
class CubeNode(Node, PcgInputNode):
    bl_idname = "CubeNode"
    bl_label = "Cube"
    
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0.0)
    prop_location = FloatVectorProperty(name="Location")
    prop_rotation = FloatVectorProperty(name="Rotation")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_radius")
        layout.column().separator()
        layout.row().prop(self, "prop_location")
        layout.row().prop(self, "prop_rotation")
    
    def functionality(self):
        bpy.ops.mesh.primitive_cube_add(radius=self.prop_radius, location=self.prop_location, rotation=self.prop_rotation)
class SphereNode(Node, PcgInputNode):
    bl_idname = "SphereNode"
    bl_label = "Sphere"
    
    prop_segments = IntProperty(name="Segments", default=32, min=3, max=10000)
    prop_rings = IntProperty(name="Ring Count", default=16, min=3, max=10000)
    prop_size = FloatProperty(name="Size", default=1.0, min=0.0)
    prop_location = FloatVectorProperty(name="Location")
    prop_rotation = FloatVectorProperty(name="Rotation")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_segments")
        layout.column().prop(self, "prop_rings")
        layout.column().prop(self, "prop_size")
        layout.column().separator()
        layout.row().prop(self, "prop_location")
        layout.row().prop(self, "prop_rotation")
    
    def functionality(self):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=self.prop_segments, ring_count=self.prop_rings, size=self.prop_size, location=self.prop_location, rotation=self.prop_rotation)
class CylinderNode(Node, PcgInputNode):
    bl_idname = "CylinderNode"
    bl_label = "Cylinder"
    
    prop_vertices = IntProperty(name="Vertices", default=32, min=3, max=1000000)
    prop_radius = FloatProperty(name="Radius", default=1.0, min=0)
    prop_depth = FloatProperty(name="Depth", default=2.0, min=0)
    prop_end = EnumProperty(name="End Fill Type", items=[("NOTHING", "Nothing", "Don’t fill at all."), ("NGON", "Ngon", "Use ngons"), ("TRIFAN", "Triangle Fan", "Use triangle fans.")], default="NGON")
    prop_location = FloatVectorProperty(name="Location")
    prop_rotation = FloatVectorProperty(name="Rotation")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_vertices")
        layout.column().prop(self, "prop_radius")
        layout.column().prop(self, "prop_depth")
        layout.column().prop(self, "prop_end")
        layout.column().separator()
        layout.row().prop(self, "prop_location")
        layout.row().prop(self, "prop_rotation")
    
    def functionality(self):
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.prop_vertices, radius=self.prop_radius, depth=self.prop_depth, end_fill_type=self.prop_end, location=self.prop_location, rotation=self.prop_rotation)
class ConeNode(Node, PcgInputNode):
    bl_idname = "ConeNode"
    bl_label = "Cone"
    
    prop_vertices = IntProperty(name="Vertices", default=32, min=3, max=1000000)
    prop_radius1 = FloatProperty(name="Radius 1", default=1.0, min=0.0)
    prop_radius2 = FloatProperty(name="Radius 2", default=0.0, min=0.0)
    prop_depth = FloatProperty(name="Depth", default=2.0, min=0)
    prop_end = EnumProperty(name="End Fill Type", items=[("NOTHING", "Nothing", "Don’t fill at all."), ("NGON", "Ngon", "Use ngons"), ("TRIFAN", "Triangle Fan", "Use triangle fans.")], default="NGON")
    prop_location = FloatVectorProperty(name="Location")
    prop_rotation = FloatVectorProperty(name="Rotation")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_vertices")
        layout.column().prop(self, "prop_radius1")
        layout.column().prop(self, "prop_radius2")
        layout.column().prop(self, "prop_depth")
        layout.column().prop(self, "prop_end")
        layout.column().separator()
        layout.row().prop(self, "prop_location")
        layout.row().prop(self, "prop_rotation")
    
    def functionality(self):
        bpy.ops.mesh.primitive_cone_add(vertices=self.prop_vertices, radius1=self.prop_radius1, radius2=self.prop_radius2, depth=self.prop_depth, end_fill_type=self.prop_end, location=self.prop_location, rotation=self.prop_rotation)
class TorusNode(Node, PcgInputNode):
    bl_idname = "TorusNode"
    bl_label = "Torus"
    
    prop_major_segments = IntProperty(name="Major Segment", default=48, min=3, max=256)
    prop_minor_segments = IntProperty(name="Minor Segment", default=12, min=3, max=256)
    prop_mode = EnumProperty(name="Mode", items=[("MAJOR_MINOR", "Major/Minor", "Use the major/minor radii for torus dimensions."), ("EXT_INT", "Exterior/Interior", "Use the exterior/interior radii for torus dimensions.")], default="MAJOR_MINOR")
    prop_major_radius = FloatProperty(name="Major Radius", default=1.0, min=0.01, max=100)
    prop_minor_radius = FloatProperty(name="Minor Radius", default=0.25, min=0.01, max=100)
    prop_ext_radius = FloatProperty(name="Exterior Radius", default=1.25, min=0.01, max=100)
    prop_int_radius = FloatProperty(name="Interior Radius", default=0.75, min=0.01, max=100)
    prop_location = FloatVectorProperty(name="Location")
    prop_rotation = FloatVectorProperty(name="Rotation")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_major_segments")
        layout.column().prop(self, "prop_minor_segments")
        layout.column().prop(self, "prop_mode")
        if (self.prop_mode == "MAJOR_MINOR"):
            layout.column().prop(self, "prop_major_radius")
            layout.column().prop(self, "prop_minor_radius")
        else:
            layout.column().prop(self, "prop_ext_radius")
            layout.column().prop(self, "prop_int_radius")
        layout.column().separator()
        layout.row().prop(self, "prop_location")
        layout.row().prop(self, "prop_rotation")
    
    def functionality(self):
        bpy.ops.mesh.primitive_torus_add(major_segments=self.prop_major_segments, minor_segments=self.prop_minor_segments, mode=self.prop_mode, major_radius = self.prop_major_radius, minor_radius = self.prop_minor_radius, abso_major_rad = self.prop_ext_radius, abso_minor_rad = self.prop_int_radius, location=self.prop_location, rotation=self.prop_rotation)

class LocationNode(Node, PcgTransformNode):
    bl_idname = "LocationNode"
    bl_label = "Location"
    
    prop_location = FloatVectorProperty(name="Location")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_location")
    
    def functionality(self):
        bpy.data.objects[self.mesh].location = self.prop_location
class RotationNode(Node, PcgTransformNode):
    bl_idname = "RotationNode"
    bl_label = "Rotation"
    
    prop_rotation = FloatVectorProperty(name="Rotation")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_rotation")
    
    def functionality(self):
        bpy.data.objects[self.mesh].rotation_euler = self.prop_rotation
class ScaleNode(Node, PcgTransformNode):
    bl_idname = "ScaleNode"
    bl_label = "Scale"
    
    prop_scale = FloatVectorProperty(name="Scale", default=(1.0, 1.0, 1.0))
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_scale")
    
    def functionality(self):
        bpy.data.objects[self.mesh].scale = self.prop_scale
class ResizeNode(Node, PcgOperatorNode):
    bl_idname = "ResizeNode"
    bl_label = "Component Scale"

    prop_value = FloatVectorProperty(name="Value", default=(1.0, 1.0, 1.0))
    prop_axis = BoolVectorProperty(name="Constraint Axis")
    prop_orientation = EnumProperty(name="Constraint Orientation", items=[("GLOBAL", "Global", "")], default="GLOBAL")
    prop_mirror = BoolProperty(name="Mirror")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_value")
        layout.prop(self, "prop_axis")
        layout.prop(self, "prop_orientation")
        layout.prop(self, "prop_mirror")
    
    def functionality(self):
        window = bpy.data.window_managers['WinMan'].windows[0]
        screen=window.screen
        area=screen.areas[4]
        space=area.spaces[0]
        scene=bpy.data.scenes[0]
        region=area.regions[4]
        override = {'window':window, 'screen':screen, 'area': area, 'space':space, 'scene':scene, 'active_object':bpy.data.objects[self.mesh], 'region':region, 'edit_object':bpy.data.objects[self.mesh], 'gpencil_data':bpy.context.gpencil_data}
        bpy.ops.transform.resize(override, value=self.prop_value, constraint_axis=self.prop_axis, constraint_orientation=self.prop_orientation, mirror=self.prop_mirror, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1.0, snap=False, snap_target='CLOSEST', snap_point=(0.0, 0.0, 0.0), snap_align=False, snap_normal=(0.0, 0.0, 0.0), gpencil_strokes=False, texture_space=False, remove_on_cancel=False, release_confirm=False, use_accurate=False)

class ToComponentNode(Node, PcgNode):
    bl_idname = "ToComponentNode"
    bl_label = "To Component Mode"
    
    prop_selection_type = EnumProperty(name="Component", items=[("FACE", "Faces", ""), ("VERT", "Vertices", ""), ("EDGE", "Edges", "")], default="FACE")
    prop_deselect = BoolProperty(name="Deselect All", default=True)

    def init(self, context):
        self.inputs.new("MeshSocket", "Mesh")
        self.outputs.new("ComponentSocket", "Component")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_selection_type", expand=True)
        layout.prop(self, "prop_deselect")
    
    def execute(self):
        if (not self.inputs[0].is_linked):
            print("Debug: " + self.name + ": Not linked")
            return ""
        self.mesh = self.inputs[0].links[0].from_node.execute()
        if (self.mesh == ""):
            print("Debug: " + self.name + ": Empty object recieved")
            return ""
        bpy.context.scene.objects.active = bpy.data.objects[self.mesh]
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type=self.prop_selection_type)
        if (self.prop_deselect):
            bpy.ops.mesh.select_all(action="DESELECT")
        return self.mesh
class ToMeshNode(Node, PcgSelectionNode):
    bl_idname = "ToMeshNode"
    bl_label = "To Mesh Mode"

    def init(self, context):
        self.inputs.new("ComponentSocket", "Component")
        self.outputs.new("MeshSocket", "Mesh")
    
    def execute(self):
        if (not self.inputs[0].is_linked):
            print("Debug: " + self.name + ": Not linked")
            return ""
        self.mesh = self.inputs[0].links[0].from_node.execute()
        if (self.mesh == ""):
            print("Debug: " + self.name + ": Empty object recieved")
            return ""
        bpy.context.scene.objects.active = bpy.data.objects[self.mesh]
        bpy.ops.object.mode_set(mode="OBJECT")
        return self.mesh
class ChangeModeNode(Node, PcgNode):
    bl_idname = "ChangeModeNode"
    bl_label = "Change Mode Mode"
    
    prop_selection_type = EnumProperty(name="Component", items=[("FACE", "Faces", ""), ("VERT", "Vertices", ""), ("EDGE", "Edges", "")], default="FACE")

    def init(self, context):
        self.inputs.new("ComponentSocket", "Component")
        self.outputs.new("ComponentSocket", "Component")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_selection_type", expand=True)
    
    def execute(self):
        if (not self.inputs[0].is_linked):
            print("Debug: " + self.name + ": Not linked")
            return ""
        self.mesh = self.inputs[0].links[0].from_node.execute()
        if (self.mesh == ""):
            print("Debug: " + self.name + ": Empty object recieved")
            return ""
        bpy.ops.mesh.select_mode(type=self.prop_selection_type)
        return self.mesh
class PivotNode(Node, PcgTransformNode):
    bl_idname = "PivotNode"
    bl_label = "Change Pivot-Point"

    prop_pivot = EnumProperty(name="Pivot Point", items=[("BOUNDING_BOX_CENTER", "Bound Box Center", ""), ("CURSOR", "Cursor", ""), ("INDIVIDUAL_ORIGINS", "Individual Origins", ""), ("MEDIAN_POINT", "Median Point", ""), ("ACTIVE_ELEMENT", "Active Element", "")], default="MEDIAN_POINT")

    def init(self, context):
        self.inputs.new("MeshSocket", "")
        self.outputs.new("MeshSocket", "")
    
    def draw_buttons(self, context, layout):
        layout.column().prop(self, "prop_pivot", expand=True)
    
    def functionality(self):
        bpy.data.screens['Default'].areas[4].spaces[0].pivot_point=self.prop_pivot

class SelectComponentsManuallyNode(Node, PcgSelectionNode):
    bl_idname = "SelectComponentsManuallyNode"
    bl_label = "Select Mesh Manually Components"
    
    selection_face = StringProperty()
    selection_vert = StringProperty()
    selection_edge = StringProperty()

    def toList(self, string):
        string = string.replace("[", "")
        string = string.replace("]", "")
        list_string = string.rsplit(", ")
        list = []
        for i in list_string:
            if i == "False":
                list.append(False)
            else:
                list.append(True)
        return list

    def save_selection(self):
        if (not self.mesh == ""):
            bpy.ops.object.mode_set(mode="OBJECT")
            self.selection_face = str([i.select for i in bpy.data.objects[self.mesh].data.polygons])
            self.selection_vert = str([i.select for i in bpy.data.objects[self.mesh].data.vertices])
            self.selection_edge = str([i.select for i in bpy.data.objects[self.mesh].data.edges])
            bpy.ops.object.mode_set(mode="EDIT")
            print("Debug: " + self.name + ": Saved components selection")

    def draw_buttons(self, context, layout):
        if (self == self.id_data.nodes.active):
            layout.operator("pcg.save_selection_op", "Save Selection")
        if (not self.mesh == ""):
            layout.label(text="Faces: " + str(len([i for i in bpy.data.objects[self.mesh].data.polygons if i.select == True])) + "/" + str(len(bpy.data.objects[self.mesh].data.polygons)))
            layout.label(text="Vertices: " + str(len([i for i in bpy.data.objects[self.mesh].data.vertices if i.select == True])) + "/" + str(len(bpy.data.objects[self.mesh].data.vertices)))
            layout.label(text="Edges: " + str(len([i for i in bpy.data.objects[self.mesh].data.edges if i.select == True])) + "/" + str(len(bpy.data.objects[self.mesh].data.edges)))
    
    def functionality(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        list_face = self.toList(self.selection_face)
        list_vert = self.toList(self.selection_vert)
        list_edge = self.toList(self.selection_edge)
        if len(list_face) == len(bpy.data.objects[self.mesh].data.polygons):
            for i in range(0, len(bpy.data.objects[self.mesh].data.polygons)):
                bpy.data.objects[self.mesh].data.polygons[i].select = list_face[i]
        if len(list_vert) == len(bpy.data.objects[self.mesh].data.vertices):
            for i in range(0, len(bpy.data.objects[self.mesh].data.vertices)):
                bpy.data.objects[self.mesh].data.vertices[i].select = list_vert[i]
        if len(list_edge) == len(bpy.data.objects[self.mesh].data.edges):
            for i in range(0, len(bpy.data.objects[self.mesh].data.edges)):
                bpy.data.objects[self.mesh].data.edges[i].select = list_edge[i]
        bpy.ops.object.mode_set(mode="EDIT")
class SelectAllNode(Node, PcgSelectionNode):
    bl_idname = "SelectAllNode"
    bl_label = "Select All"

    prop_action = EnumProperty(name="Action", items=[("TOGGLE", "Toggle", ""), ("SELECT", "Select", ""), ("DESELECT", "Deselect", ""), ("INVERT", "Invert", "")], default="TOGGLE")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_action")
    
    def functionality(self):
        bpy.ops.mesh.select_all(action=self.prop_action)
class SelectAxisNode(Node, PcgSelectionNode):
    bl_idname = "SelectAxisNode"
    bl_label = "Select Axis"

    prop_mode = EnumProperty(name="Mode", items=[("POSITIVE", "Positive", ""), ("NEGATIVE", "Negative", ""), ("ALIGNED", "Aligned", "")], default="POSITIVE")
    prop_axis = EnumProperty(name="Axis", items=[("X_AXIS", "X", ""), ("Y_AXIS", "Y", ""), ("Z_AXIS", "Z", "")], default="X_AXIS")
    prop_threshold = FloatProperty(name="Threshold", default=0.0001, min=0.000001, max=50)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_mode", expand=True)
        layout.prop(self, "prop_axis")
        layout.prop(self, "prop_threshold")
    
    def functionality(self):
        bpy.ops.mesh.select_axis(mode=self.prop_mode, axis=self.prop_axis, threshold=self.prop_threshold)
class SelectFaceBySidesNode(Node, PcgSelectionNode):
    bl_idname = "SelectFaceBySidesNode"
    bl_label = "Select Face By Sides"

    prop_number = IntProperty(name="Number", default=3, min=3)
    prop_type = EnumProperty(name="Type", items=[("LESS", "Less", ""), ("EQUAL", "Equal", ""), ("GREATER", "Greater", ""), ("NOTEQUAL", "Not Equal", "")], default="EQUAL")
    prop_extend = BoolProperty(name="Extend", default=True)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_number")
        layout.prop(self, "prop_type")
        layout.prop(self, "prop_extend")
    
    def functionality(self):
        bpy.ops.mesh.select_face_by_sides(number=self.prop_number, type=self.prop_type, extend=self.prop_extend)
class SelectInteriorFaces(Node, PcgSelectionNode):
    bl_idname = "SelectInteriorFaces"
    bl_label = "Select Interior Faces"

    def functionality(self):
        bpy.ops.mesh.select_interior_faces()
class SelectLessNode(Node, PcgSelectionNode):
    bl_idname = "SelectLessNode"
    bl_label = "Select Less"

    prop_face_step = BoolProperty(name="Face Step", default=True)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_face_step")
    
    def functionality(self):
        bpy.ops.mesh.select_less(use_face_step=self.prop_face_step)
class SelectMoreNode(Node, PcgSelectionNode):
    bl_idname = "SelectMoreNode"
    bl_label = "Select More"

    prop_face_step = BoolProperty(name="Face Step", default=True)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_face_step")
    
    def functionality(self):
        bpy.ops.mesh.select_more(use_face_step=self.prop_face_step)
class SelectLinkedNode(Node, PcgSelectionNode):
    bl_idname = "SelectLinkedNode"
    bl_label = "Select Linked"

    prop_delimit = EnumProperty(name="Delimit", items=[("NORMAL", "Normal", ""), ("MATERIAL", "Material", ""), ("SEAM", "Seam", ""), ("SHARP", "Sharp", ""), ("UV", "UV", "")], default="SEAM")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_delimit")
    
    def functionality(self):
        bpy.ops.mesh.select_linked(delimit={self.prop_delimit})
class SelectLooseNode(Node, PcgSelectionNode):
    bl_idname = "SelectLooseNode"
    bl_label = "Select Loose"

    prop_extend = BoolProperty(name="Extend")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_extend")
    
    def functionality(self):
        bpy.ops.mesh.select_loose(extend=self.prop_extend)
class SelectMirrorNode(Node, PcgSelectionNode):
    bl_idname = "SelectMirrorNode"
    bl_label = "Select Mirror"

    prop_axis = EnumProperty(name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X")
    prop_extend = BoolProperty(name="Extend")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_axis", expand=True)
        layout.prop(self, "prop_extend")
    
    def functionality(self):
        bpy.ops.mesh.select_mirror(axis={self.prop_axis}, extend=self.prop_extend)
class SelectNextItemNode(Node, PcgSelectionNode):
    bl_idname = "SelectNextItemNode"
    bl_label = "Select Next Item"

    def functionality(self):
        bpy.ops.mesh.select_next_item()
class SelectPrevItemNode(Node, PcgSelectionNode):
    bl_idname = "SelectPrevItemNode"
    bl_label = "Select Previous Item"

    def functionality(self):
        bpy.ops.mesh.select_prev_item()
class SelectNonManifoldNode(Node, PcgSelectionNode):
    bl_idname = "SelectNonManifoldNode"
    bl_label = "Select Non-Manifold"

    prop_extend = BoolProperty(name="Extend", default=True)
    prop_wire = BoolProperty(name="Wire", default=True)
    prop_boundary = BoolProperty(name="Boundary", default=True)
    prop_multi_face = BoolProperty(name="Multiple Faces", default=True)
    prop_non_contiguous = BoolProperty(name="Non Contiguous", default=True)
    prop_verts = BoolProperty(name="Vertices", default=True)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_extend")
        layout.prop(self, "prop_wire")
        layout.prop(self, "prop_boundary")
        layout.prop(self, "prop_multi_face")
        layout.prop(self, "prop_non_contiguous")
        layout.prop(self, "prop_verts")

    def functionality(self):
        bpy.ops.mesh.select_non_manifold(extend=self.prop_extend, use_wire=self.prop_wire, use_boundary=self.prop_boundary, use_multi_face=self.prop_multi_face, use_non_contiguous=self.prop_non_contiguous, use_verts=self.prop_verts)
class SelectNthNode(Node, PcgSelectionNode):
    bl_idname = "SelectNthNode"
    bl_label = "Select Nth"

    prop_nth = IntProperty(name="Nth", default=2, min=2)
    prop_skip = IntProperty(name="Skip", default=1, min=1)
    prop_offset = IntProperty(name="Offset", default=0)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_nth")
        layout.prop(self, "prop_skip")
        layout.prop(self, "prop_offset")

    def functionality(self):
        bpy.ops.mesh.select_nth(nth=self.prop_nth, skip=self.prop_skip, offset=self.prop_offset)
class SelectRandomNode(Node, PcgSelectionNode):
    bl_idname = "SelectRandomNode"
    bl_label = "Select Random"

    prop_percent = FloatProperty(name="Percent", default=50.0, min=0.0, max=100.0)
    prop_seed = IntProperty(name="Seed", default=0, min=0)
    prop_action = EnumProperty(name="Action", items=[("SELECT", "Select", ""), ("DESELECT", "Deselect", "")], default="SELECT")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_percent")
        layout.prop(self, "prop_seed")
        layout.prop(self, "prop_action")

    def functionality(self):
        bpy.ops.mesh.select_random(percent=self.prop_percent, seed=self.prop_seed, action=self.prop_action)
class SelectSimilarNode(Node, PcgSelectionNode):
    bl_idname = "SelectSimilarNode"
    bl_label = "Select Similar"

    prop_type = EnumProperty(name="Type", items=[("MATERIAL", "Material", ""), ("IMAGE", "Image", ""), ("AREA", "Area", ""), ("SIDES", "Sides", ""), ("PERIMETER", "Perimeter", ""), ("NORMAL", "Normal", ""), ("COPLANAR", "Co-Planar", ""), ("SMOOTH", "Smooth", ""), ("FREESTYLE_FACE", "Freestyle Face", "")], default="NORMAL")
    prop_compare = EnumProperty(name="Compare", items=[("EQUAL", "Equal", ""), ("GREATER", "Greater", ""), ("LESS", "Less", "")], default="EQUAL")
    prop_threshold = FloatProperty(name="Threshold", default=0.0, min=0.0, max=1.0)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
        layout.prop(self, "prop_compare")
        layout.prop(self, "prop_threshold")

    def functionality(self):
        bpy.ops.mesh.select_similar(type=self.prop_type, compare=self.prop_compare, threshold=self.prop_threshold)
class SelectSimilarRegionNode(Node, PcgSelectionNode):
    bl_idname = "SelectSimilarRegionNode"
    bl_label = "Select Similar Region"

    def functionality(self):
        bpy.ops.mesh.select_similar_region()
class SelectUngroupedNode(Node, PcgSelectionNode):
    bl_idname = "SelectUngroupedNode"
    bl_label = "Select Ungrouped"

    prop_extend = BoolProperty(name="Extend")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_extend")
    
    def functionality(self):
        bpy.ops.mesh.select_ungrouped(extend=self.prop_extend)
class SelectEdgesSharpNode(Node, PcgSelectionNode):
    bl_idname = "SelectEdgesSharpNode"
    bl_label = "Select Sharp-Enough Edges"

    prop_sharpness = FloatProperty(name="Sharpness", default=0.523599, min=0.000174533, max=3.14159, precision=6)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_sharpness")
    
    def functionality(self):
        bpy.ops.mesh.edges_select_sharp(sharpness=self.prop_sharpness)
class SelectFacesLinkedFlatNode(Node, PcgSelectionNode):
    bl_idname = "SelectFacesLinkedFlatSharpNode"
    bl_label = "Select Linked Faces By Angle"

    prop_sharpness = FloatProperty(name="Sharpness", default=0.523599, min=0.000174533, max=3.14159, precision=6)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_sharpness")
    
    def functionality(self):
        bpy.ops.mesh.faces_select_linked_flat(sharpness=self.prop_sharpness)

class DeleteNode(Node, PcgOperatorNode):
    bl_idname = "DeleteNode"
    bl_label = "Delete"

    prop_type = EnumProperty(name="Type", items=[("VERT", "Vertices", ""), ("EDGE", "Edges", ""), ("FACE", "Faces", ""), ("EDGE_FACE", "Edges And Faces", ""), ("ONLY_FACE", "Only Faces", "")], default="VERT")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
    
    def functionality(self):
        bpy.ops.mesh.delete(type=self.prop_type)
class DissolveFacesNode(Node, PcgOperatorNode):
    bl_idname = "DissolveFacesNode"
    bl_label = "Dissolve Faces"

    prop_verts = BoolProperty(name="Use Vertices")

    def draw_buttons(self, context, layout):
        layout(self, "prop_verts")
    
    def functionality(self):
        bpy.ops.mesh.dissolve_faces(use_verts=self.prop_verts)

class BeautifyFillNode(Node, PcgOperatorNode):
    bl_idname = "BeautifyFillNode"
    bl_label = "Beautify Fill"

    prop_angle_limit = FloatProperty(name="Angle Limit", default=3.14159, min=0.0, max=3.14159, subtype="ANGLE", unit="ROTATION")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_angle_limit")
    
    def functionality(self):
        bpy.ops.mesh.beautify_fill(angle_limit=self.prop_angle_limit)
class BevelNode(Node, PcgOperatorNode):
    bl_idname = "BevelNode"
    bl_label = "Bevel"

    prop_offset_type = EnumProperty(name="Offset Type", items=[("OFFSET", "Offset", ""), ("WIDTH", "Width", ""), ("PERCENT", "Percent", ""), ("DEPTH", "Depth", "")], default="OFFSET")
    prop_offset = FloatProperty(name="Offset", default=0.0, min=-1000000, max=1000000)
    prop_segments = IntProperty(name="Segments", default=1, min=1, max=1000)
    prop_profile = FloatProperty(name="Profile", default=0.5, min=0.15, max=1.0)
    prop_vertex_only = BoolProperty(name="Vertex Only")
    prop_clamp_overlap = BoolProperty(name="Clamp Overlap")
    prop_loop_slide = BoolProperty(name="Loop Slide", default=True)
    prop_material = IntProperty(name="Material", default=-1, min=-1)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_offset_type")
        layout.prop(self, "prop_offset")
        layout.prop(self, "prop_segments")
        layout.prop(self, "prop_profile")
        layout.prop(self, "prop_vertex_only")
        layout.prop(self, "prop_clamp_overlap")
        layout.prop(self, "prop_loop_slide")
        layout.prop(self, "prop_material")
    
    def functionality(self):
        bpy.ops.mesh.bevel(offset_type=self.prop_offset_type, offset=self.prop_offset, segments=self.prop_segments, profile=self.prop_segments, vertex_only=self.prop_vertex_only, clamp_overlap=self.prop_clamp_overlap, loop_slide=self.prop_loop_slide, material=self.prop_material)
class BridgeEdgeLoopsNode(Node, PcgOperatorNode):
    bl_idname = "BridgeEdgeLoopsNode"
    bl_label = "Bridge Edge Loops"

    prop_type = EnumProperty(name="Connect Loops", items=[("SINGLE", "Single", ""), ("CLOSED", "Closed", ""), ("PAIRS", "Pairs", "")], default="SINGLE")
    prop_use_merge = BoolProperty(name="Merge")
    prop_merge_factor = FloatProperty(name="Merge Factor", default=0.5, min=0.0, max=0.1)
    prop_twist_offset = IntProperty(name="Twist", default=0, min=-1000, max=1000)
    prop_number_cuts = IntProperty(name="Number of Cuts", default=0, min=0, max=1000)
    prop_interpolation = EnumProperty(name="Interpolation", items=[("LINEAR", "Linear", ""), ("PATH", "Path", ""), ("SURFACE", "Surface", "")], default="PATH")
    prop_smoothness = FloatProperty(name="Smoothness", default=1.0, min=0.0, max=1000.0)
    prop_profile_shape_factor = FloatProperty(name="Profile Factor", default=0.0, min=-1000.0, max=1000.0)
    prop_profile_shape = EnumProperty(name="Profile Shape", items=[("SMOOTH", "Smooth", ""), ("SPHERE", "Sphere", ""), ("ROOT", "Root", ""), ("INVERSE_SQUARE", "Inverse Square", ""), ("SHARP", "Sharp", ""), ("LINEAR", "Linear", "")], default="SMOOTH")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
        layout.prop(self, "prop_use_merge")
        layout.prop(self, "prop_merge_factor")
        layout.prop(self, "prop_twist_offset")
        layout.prop(self, "prop_number_cuts")
        layout.prop(self, "prop_interpolation")
        layout.prop(self, "prop_smoothness")
        layout.prop(self, "prop_profile_shape_factor")
        layout.prop(self, "prop_profile_shape")
    
    def functionality(self):
        bpy.ops.mesh.bridge_edge_loops(type=self.prop_type, use_merge=self.prop_use_merge, merge_factor=self.prop_merge_factor, twist_offset=self.prop_twist_offset, number_cuts=self.prop_number_cuts, interpolation=self.prop_interpolation, smoothness=self.prop_smoothness, profile_shape_factor=self.prop_profile_shape_factor, profile_shape=self.prop_profile_shape)
class DecimateNode(Node, PcgOperatorNode):
    bl_idname = "DecimateNode"
    bl_label = "Decimate"

    prop_ratio = FloatProperty(name="Ratio", default=1.0, min=0.0, max=1.0)
    prop_use_vertex_group = BoolProperty(name="Vertex Group")
    prop_vertex_group_factor = FloatProperty(name="Weight", default=1.0, min=0.0, max=1000.0)
    prop_invert_vertex_group = BoolProperty(name="Invert")
    prop_use_symmetry = BoolProperty(name="Symmetry")
    prop_symmetry_axis = EnumProperty(name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="Y")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_ratio")
        layout.prop(self, "prop_use_vertex_group")
        layout.prop(self, "prop_vertex_group_factor")
        layout.prop(self, "prop_invert_vertex_group")
        layout.prop(self, "prop_use_symmetry")
        layout.prop(self, "prop_symmetry_axis")
    
    def functionality(self):
        bpy.ops.mesh.decimate(ratio=self.prop_ratio, use_vertex_group=self.prop_use_vertex_group, vertex_group_factor=self.prop_vertex_group_factor, invert_vertex_group=self.prop_invert_vertex_group, use_symmetry=self.prop_use_symmetry, symmetry_axis=self.prop_symmetry_axis)
class ExtrudeFacesNode(Node, PcgOperatorNode):
    bl_idname = "ExtrudeFacesNode"
    bl_label = "Extrude Faces"

    prop_amount = FloatProperty(name="Amount")
    prop_mirror = BoolProperty(name="Mirror")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_amount")
        layout.prop(self, "prop_mirror")
    
    def functionality(self):
        window = bpy.data.window_managers['WinMan'].windows[0]
        screen=window.screen
        area=screen.areas[4]
        space=area.spaces[0]
        scene=bpy.data.scenes[0]
        region=area.regions[4]
        override = {'window':window, 'screen':screen, 'area': area, 'space':space, 'scene':scene, 'active_object':bpy.data.objects[self.mesh], 'region':region, 'edit_object':bpy.data.objects[self.mesh], 'gpencil_data':bpy.context.gpencil_data}
        bpy.ops.mesh.extrude_faces_move(override ,MESH_OT_extrude_faces_indiv={"mirror":self.prop_mirror}, TRANSFORM_OT_shrink_fatten={"value":self.prop_amount, "use_even_offset":False, "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":True, "use_accurate":False})
class ExtrudeRegionNode(Node, PcgOperatorNode):
    bl_idname = "ExtrudeRegionNode"
    bl_label = "Extrude Region"

    prop_amount = FloatProperty(name="Amount")
    prop_mirror = BoolProperty(name="Mirror")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_amount")
        layout.prop(self, "prop_mirror")
    
    def functionality(self):
        window = bpy.data.window_managers['WinMan'].windows[0]
        screen=window.screen
        area=screen.areas[4]
        space=area.spaces[0]
        scene=bpy.data.scenes[0]
        region=area.regions[4]
        override = {'window':window, 'screen':screen, 'area': area, 'space':space, 'scene':scene, 'active_object':bpy.data.objects[self.mesh], 'region':region, 'edit_object':bpy.data.objects[self.mesh], 'gpencil_data':bpy.context.gpencil_data}
        bpy.ops.mesh.extrude_region_shrink_fatten(override ,MESH_OT_extrude_region={"mirror":self.prop_mirror}, TRANSFORM_OT_shrink_fatten={"value":self.prop_amount, "use_even_offset":False, "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":True, "use_accurate":False})
class InsetNode(Node, PcgOperatorNode):
    bl_idname = "InsetNode"
    bl_label = "Inset"
    
    prop_thickness = FloatProperty(name="Thickness", default=0.01, min=0.0)
    prop_depth = FloatProperty(name="Depth")
    prop_boundary = BoolProperty(name="Boundary", default=True)
    prop_even_offset = BoolProperty(name="Even Offset", default=True)
    prop_relative_offset = BoolProperty(name="Relative Offset")
    prop_edge_rail = BoolProperty(name="Edge Rail")
    prop_outset = BoolProperty(name="Outset")
    prop_select_inset = BoolProperty(name="Select Inset")
    prop_individual = BoolProperty(name="Individual")
    prop_interpolate = BoolProperty(name="Interpolate", default=True)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_thickness")
        layout.prop(self, "prop_depth")
        split = layout.split()
        col=split.column()
        col.prop(self, "prop_boundary")
        col.prop(self, "prop_even_offset")
        col.prop(self, "prop_relative_offset")
        col.prop(self, "prop_edge_rail")
        col=split.column()
        col.prop(self, "prop_outset")
        col.prop(self, "prop_select_inset")
        col.prop(self, "prop_individual")
        col.prop(self, "prop_interpolate")

    def functionality(self):
        bpy.ops.mesh.inset(use_boundary=self.prop_boundary, use_even_offset=self.prop_even_offset, use_relative_offset=self.prop_relative_offset, use_edge_rail=self.prop_edge_rail, thickness=self.prop_thickness, depth=self.prop_depth, use_outset=self.prop_outset, use_select_inset=self.prop_select_inset, use_individual=self.prop_individual, use_interpolate=self.prop_interpolate)
class MergeNode(Node, PcgOperatorNode):
    bl_idname = "MergeNode"
    bl_label = "Merge"
    
    prop_type = EnumProperty(name="Type", items=[("CENTER", "Center", ""), ("CURSOR", "Cursor", ""), ("COLLAPSE", "Collapse", "")], default="CENTER")
    prop_uv = BoolProperty(name="UVs")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")
        layout.prop(self, "prop_uv")

    def functionality(self):
        bpy.ops.mesh.merge(type=self.prop_type, uvs=self.prop_uv)
class SolidifyNode(Node, PcgOperatorNode):
    bl_idname = "SolidifyNode"
    bl_label = "Solidify"
    
    prop_thickness = FloatProperty(name="Thickness", default=0.01, min=-10000.0, max=10000.0)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_thickness")

    def functionality(self):
        bpy.ops.mesh.solidify(thickness=self.prop_thickness)
class SpinNode(Node, PcgOperatorNode):
    bl_idname = "SpinNode"
    bl_label = "Spin"
    
    prop_steps = IntProperty(name="Steps", default=9, min=0, max=1000000)
    prop_dupli = BoolProperty(name="Duplicate")
    prop_angle = FloatProperty(name="Angle", default=1.5708, subtype="ANGLE", unit="ROTATION")
    prop_center = FloatVectorProperty(name="Center")
    prop_axis = FloatVectorProperty(name="Axis", min=-1.0, max=1.0)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_steps")
        layout.prop(self, "prop_dupli")
        layout.prop(self, "prop_angle")
        layout.prop(self, "prop_center")
        layout.prop(self, "prop_axis")

    def functionality(self):
        bpy.ops.mesh.spin(steps=self.prop_steps, dupli=self.prop_dupli, angle=self.prop_angle, center=self.prop_center, axis=self.prop_axis)
class SubdivideNode(Node, PcgOperatorNode):
    bl_idname = "SubdivideNode"
    bl_label = "Subdivide"

    prop_number_cuts = IntProperty(name="Number of Cuts", default=1, min=1, max=100)
    prop_smoothness = FloatProperty(name="Smoothness", default=0.0, min=0.0, max=1000.0)
    prop_quadtri = BoolProperty(name="Quad/Tri Mode")
    prop_quadcorner = EnumProperty(name="Quad Corner Type", items=[("INNERVERT", "Inner Vertices", ""), ("PATH", "Path", ""), ("STRAIGHT_CUT", "Straight Cut", ""), ("FAN", "Fan", "")], default="STRAIGHT_CUT")
    prop_fractal = FloatProperty(name="Fractal", default=0.0, min=0.0, max=1000000)
    prop_fractal_along_normal = FloatProperty(name="Along Normal", default=0.0, min=0.0, max=1.0)
    prop_seed = IntProperty(name="Random Seed", default=0, min=0)

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_number_cuts")
        layout.prop(self, "prop_smoothness")
        layout.prop(self, "prop_quadtri")
        layout.prop(self, "prop_quadcorner")
        layout.prop(self, "prop_fractal")
        layout.prop(self, "prop_fractal_along_normal")
        layout.prop(self, "prop_seed")
    
    def functionality(self):
        bpy.ops.mesh.subdivide(number_cuts=self.prop_number_cuts, smoothness=self.prop_smoothness, quadtri=self.prop_quadtri, quadcorner=self.prop_quadcorner, fractal=self.prop_fractal, fractal_along_normal=self.prop_fractal_along_normal, seed=self.prop_seed)

class ArrayNode(Node, PcgModifierNode):
    bl_idname = "ArrayNode"
    bl_label = "Array"

    fit_type = EnumProperty(name="Fit Type", items=[("FIXED_COUNT", "Fixed Count", ""), ("FIT_LENGTH", "Fit Length", ""), ("FIT_CURVE", "Fit Curve", "")], default="FIXED_COUNT")
    count = IntProperty(name="Count", default=2, min=1, max=1000)
    fit_length = FloatProperty(name="Length", default=0.0, min=0.0)
    curve = PointerProperty(name="Curve", type=bpy.types.Curve)
    use_constant_offset = BoolProperty(name="Constant Offset")
    constant_offset_displace = FloatVectorProperty()
    use_merge_vertices = BoolProperty()
    use_merge_vertices_cap = BoolProperty()
    merge_threshold = FloatProperty(default=0.01, min=0.0, max=1.0)
    use_relative_offset = BoolProperty(name="Use Relative Offset", default=True)
    relative_offset_displace = FloatVectorProperty(default=(1.0, 0.0, 0.0))
    use_object_offset = BoolProperty(name="Object Offset")
    offset_object = PointerProperty(type=bpy.types.Object)
    start_cap = PointerProperty(name="Start Cap", type=bpy.types.Object)
    end_cap = PointerProperty(name="End Cap", type=bpy.types.Object)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "fit_type")
        if self.fit_type == 'FIXED_COUNT':
            layout.prop(self, "count")
        elif self.fit_type == 'FIT_LENGTH':
            layout.prop(self, "fit_length")
        elif self.fit_type == 'FIT_CURVE':
            layout.prop(self, "curve")
        layout.separator()
        split = layout.split()
        col = split.column()
        col.prop(self, "use_constant_offset")
        sub = col.column()
        sub.active = self.use_constant_offset
        sub.prop(self, "constant_offset_displace", text="")
        col.separator()
        col.prop(self, "use_merge_vertices", text="Merge")
        sub = col.column()
        sub.active = self.use_merge_vertices
        sub.prop(self, "use_merge_vertices_cap", text="First Last")
        sub.prop(self, "merge_threshold", text="Distance")
        col = split.column()
        col.prop(self, "use_relative_offset")
        sub = col.column()
        sub.active = self.use_relative_offset
        sub.prop(self, "relative_offset_displace", text="")
        col.separator()
        col.prop(self, "use_object_offset")
        sub = col.column()
        sub.active = self.use_object_offset
        sub.prop(self, "offset_object", text="")
        layout.separator()
        layout.prop(self, "start_cap")
        layout.prop(self, "end_cap")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="ARRAY")
        bpy.data.objects[self.mesh].modifiers[0].fit_type = self.fit_type
        bpy.data.objects[self.mesh].modifiers[0].count = self.count
        bpy.data.objects[self.mesh].modifiers[0].fit_length = self.fit_length
        bpy.data.objects[self.mesh].modifiers[0].curve = self.curve
        bpy.data.objects[self.mesh].modifiers[0].use_constant_offset = self.use_constant_offset
        bpy.data.objects[self.mesh].modifiers[0].constant_offset_displace = self.constant_offset_displace
        bpy.data.objects[self.mesh].modifiers[0].use_merge_vertices = self.use_merge_vertices
        bpy.data.objects[self.mesh].modifiers[0].use_merge_vertices_cap = self.use_merge_vertices_cap
        bpy.data.objects[self.mesh].modifiers[0].merge_threshold = self.merge_threshold
        bpy.data.objects[self.mesh].modifiers[0].use_relative_offset = self.use_relative_offset
        bpy.data.objects[self.mesh].modifiers[0].relative_offset_displace = self.relative_offset_displace
        bpy.data.objects[self.mesh].modifiers[0].use_object_offset = self.use_object_offset
        bpy.data.objects[self.mesh].modifiers[0].offset_object = self.offset_object
        bpy.data.objects[self.mesh].modifiers[0].start_cap = self.start_cap
        bpy.data.objects[self.mesh].modifiers[0].end_cap = self.end_cap
        return True
class BevelModNode(Node, PcgModifierNode):
    bl_idname = "BevelModNode"
    bl_label = "Bevel"
    
    width = FloatProperty(name="Width", default=0.1, min=0.0)
    segments = IntProperty(name="Segments", default=1, min=0, max=100)
    profile = FloatProperty(name="Profile", default=0.5, min=0.0, max=1.0)
    material = IntProperty(name="Material", default=-1, min=0, max=32767)
    use_only_vertices = BoolProperty(name="Only Vertices")
    use_clamp_overlap = BoolProperty(name="Clamp Overlap", default=True)
    loop_slide = BoolProperty(name="Loop Slide", default=True)
    limit_method = EnumProperty(name="Limit Method", items=[("NONE", "None", ""), ("ANGLE", "Angle", ""), ("WEIGHT", "Weight", "")], default="NONE")
    angle_limit = IntProperty(name="Angle", default=30, min=0, max=180, subtype="ANGLE")
    offset_type = EnumProperty(name="Limit Method", items=[("OFFSET", "Offset", ""), ("WIDTH", "Width", ""), ("DEPTH", "Depth", ""), ("PERCENT", "Percent", "")], default="OFFSET")
    
    def draw_buttons(self, context, layout):
        split = layout.split()
        col = split.column()
        col.prop(self, "width")
        col.prop(self, "segments")
        col.prop(self, "profile")
        col.prop(self, "material")
        col = split.column()
        col.prop(self, "use_only_vertices")
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
        bpy.data.objects[self.mesh].modifiers[0].width = self.width
        bpy.data.objects[self.mesh].modifiers[0].segments = self.segments
        bpy.data.objects[self.mesh].modifiers[0].profile = self.profile
        bpy.data.objects[self.mesh].modifiers[0].material = self.material
        bpy.data.objects[self.mesh].modifiers[0].use_only_vertices = self.use_only_vertices
        bpy.data.objects[self.mesh].modifiers[0].use_clamp_overlap = self.use_clamp_overlap
        bpy.data.objects[self.mesh].modifiers[0].loop_slide = self.loop_slide
        bpy.data.objects[self.mesh].modifiers[0].limit_method = self.limit_method
        bpy.data.objects[self.mesh].modifiers[0].angle_limit = self.angle_limit
        bpy.data.objects[self.mesh].modifiers[0].offset_type = self.offset_type
        return True
class BooleanNode(Node, PcgModifierNode):
    bl_idname = "BooleanNode"
    bl_label = "Boolean"
    
    prop_op = EnumProperty(name="Operation", items=[("DIFFERENCE", "Difference", ""), ("UNION", "Union", ""), ("INTERSECT", "Intersect", "")], default="INTERSECT")
    prop_obj = PointerProperty(name="Object", type=bpy.types.Object)
    prop_overlap = FloatProperty(name="Overlap Threshold", default=0.000001, min=0.0, max=1.0, precision=6)
    prop_draw_mode = EnumProperty(items=[("SOLID", "Solid", ""), ("WIRE", "Wire", ""), ("BOUNDS", "Bounds", "")], default="WIRE")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_op")
        layout.prop(self, "prop_obj")
        layout.prop(self, "prop_overlap")
        layout.label("Set Secondary Object Display Mode:")
        layout.prop(self, "prop_draw_mode", expand=True)
    
    def functionality(self):
        if (self.prop_obj == None):
            return False
        bpy.ops.object.modifier_add(type="BOOLEAN")
        bpy.data.objects[self.mesh].modifiers[0].operation = self.prop_op
        bpy.data.objects[self.mesh].modifiers[0].object = self.prop_obj
        bpy.data.objects[self.mesh].modifiers[0].double_threshold = self.prop_overlap
        self.prop_obj.draw_type = self.prop_draw_mode
        return True
class SolidifyModNode(Node, PcgModifierNode):
    bl_idname = "SolidifyModNode"
    bl_label = "Solidify"
    
    thickness = FloatProperty(name="Thickness", default=0.01)
    thickness_clamp = FloatProperty(name="Clamp", default=0.0, min=0.0, max=100.0)
    vertex_group = StringProperty()
    invert_vertex_group = BoolProperty()
    thickness_vertex_group = FloatProperty(default=0.0, min=0.0, max=1.0)
    edge_crease_inner = FloatProperty(default=0.0, min=0.0, max=1.0)
    edge_crease_outer = FloatProperty(default=0.0, min=0.0, max=1.0)
    edge_crease_rim = FloatProperty(default=0.0, min=0.0, max=1.0)
    offset = FloatProperty(name="Offset", default=-1.0)
    use_flip_normals = BoolProperty(name="Flip Normals")
    use_even_offset = BoolProperty(name="Even Thickness")
    use_quality_normals = BoolProperty(name="High Quality Normals")
    use_rim = BoolProperty(name="Fill Rim", default=True)
    use_rim_only = BoolProperty(name="Only Rim")
    material_offset = IntProperty(default=0, min=-32768, max=32767)
    material_offset_rim = IntProperty(default=0, min=-32768, max=32767)
    
    def draw_buttons(self, context, layout):
        split = layout.split()
        col = split.column()
        col.prop(self, "thickness")
        col.prop(self, "thickness_clamp")
        col.separator()
        row = col.row(align=True)
        if (not self.mesh == ""):
            row.prop_search(self, "vertex_group", bpy.data.objects[self.mesh], "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(self.vertex_group)
        sub.prop(self, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
        sub = col.row()
        sub.active = bool(self.vertex_group)
        sub.prop(self, "thickness_vertex_group", text="Factor")
        col.label(text="Crease:")
        col.prop(self, "edge_crease_inner", text="Inner")
        col.prop(self, "edge_crease_outer", text="Outer")
        col.prop(self, "edge_crease_rim", text="Rim")
        col = split.column()
        col.prop(self, "offset")
        col.prop(self, "use_flip_normals")
        col.prop(self, "use_even_offset")
        col.prop(self, "use_quality_normals")
        col.prop(self, "use_rim")
        col_rim = col.column()
        col_rim.active = self.use_rim
        col_rim.prop(self, "use_rim_only")
        col.separator()
        col.label(text="Material Index Offset:")
        sub = col.column()
        row = sub.split(align=True, percentage=0.4)
        row.prop(self, "material_offset", text="")
        row = row.row(align=True)
        row.active = self.use_rim
        row.prop(self, "material_offset_rim", text="Rim")
    
    def functionality(self):
        bpy.ops.object.modifier_add(type="SOLIDIFY")
        bpy.data.objects[self.mesh].modifiers[0].thickness = self.thickness
        bpy.data.objects[self.mesh].modifiers[0].thickness_clamp = self.thickness_clamp
        bpy.data.objects[self.mesh].modifiers[0].vertex_group = self.vertex_group
        bpy.data.objects[self.mesh].modifiers[0].invert_vertex_group = self.invert_vertex_group
        bpy.data.objects[self.mesh].modifiers[0].thickness_vertex_group = self.thickness_vertex_group
        bpy.data.objects[self.mesh].modifiers[0].edge_crease_inner = self.edge_crease_inner
        bpy.data.objects[self.mesh].modifiers[0].edge_crease_outer = self.edge_crease_outer
        bpy.data.objects[self.mesh].modifiers[0].edge_crease_rim = self.edge_crease_rim
        bpy.data.objects[self.mesh].modifiers[0].offset = self.offset
        bpy.data.objects[self.mesh].modifiers[0].use_flip_normals = self.use_flip_normals
        bpy.data.objects[self.mesh].modifiers[0].use_even_offset = self.use_even_offset
        bpy.data.objects[self.mesh].modifiers[0].use_quality_normals = self.use_quality_normals
        bpy.data.objects[self.mesh].modifiers[0].use_rim = self.use_rim
        bpy.data.objects[self.mesh].modifiers[0].use_rim_only = self.use_rim_only
        bpy.data.objects[self.mesh].modifiers[0].material_offset = self.material_offset
        bpy.data.objects[self.mesh].modifiers[0].material_offset_rim = self.material_offset_rim
        return True

class MeshNode(Node, PcgTransformNode):
    bl_idname = "MeshNode"
    bl_label = "Mesh Output"
    
    print_output = BoolProperty(name="Print Output (Debug)", default=False)
    
    def init(self, context):
        self.inputs.new("MeshSocket", "Mesh")
    
    def draw_buttons(self, context, layout):
        if (self == self.id_data.nodes.active):
            layout.operator("pcg.generate_mesh_op", "Generate Mesh")
        layout.column().prop(self, "print_output")
    
    def functionality(self):
        if (self.print_output):
            print(self.name + ": " + self.mesh)
class DrawModeNode(Node, PcgTransformNode):
    bl_idname = "DrawModeNode"
    bl_label = "Mesh Draw Mode (Viewport)"

    prop_name = BoolProperty(name="Name")
    prop_wire = BoolProperty(name="Wire")
    prop_xray = BoolProperty(name="X-Ray")
    prop_transparency = BoolProperty(name="Transparency")
    prop_max_draw_type = EnumProperty(name="Maximum Draw Type", items=[("SOLID", "Solid", ""), ("WIRE", "Wire", ""), ("BOUNDS", "Bounds", "")], default="SOLID")
    
    def draw_buttons(self, context, layout):
        split = layout.split()
        col = split.column()
        col.prop(self, "prop_name")
        col.prop(self, "prop_wire")
        col = split.column()
        col.prop(self, "prop_xray")
        col.prop(self, "prop_transparency")
        layout.label("Maximum Draw Type:")
        layout.prop(self, "prop_max_draw_type", expand=True)
    
    def functionality(self):
        bpy.data.objects[self.mesh].show_name = self.prop_name
        bpy.data.objects[self.mesh].show_wire = self.prop_wire
        bpy.data.objects[self.mesh].show_x_ray = self.prop_xray
        bpy.data.objects[self.mesh].show_transparent = self.prop_transparency
        bpy.data.objects[self.mesh].draw_type = self.prop_max_draw_type
##############################################################


inputs = [PlaneNode, CubeNode, SphereNode, CylinderNode, ConeNode] #TorusNode
transform = [LocationNode, RotationNode, ScaleNode, ResizeNode] #ComponentTransform
modifiers = [ArrayNode, BevelModNode, BooleanNode, SolidifyModNode]
conversion = [ToComponentNode, ToMeshNode, ChangeModeNode, PivotNode]
selection = [SelectComponentsManuallyNode, SelectAllNode, SelectAxisNode, SelectFaceBySidesNode, SelectInteriorFaces, SelectLessNode, SelectMoreNode, SelectLinkedNode, SelectLooseNode, SelectMirrorNode, SelectNextItemNode, SelectPrevItemNode, SelectNonManifoldNode, SelectNthNode, SelectRandomNode, SelectSimilarNode, SelectSimilarRegionNode, SelectUngroupedNode, SelectEdgesSharpNode, SelectFacesLinkedFlatNode]
deletion = [DeleteNode, DissolveFacesNode]
operators = [BeautifyFillNode, BevelNode, BridgeEdgeLoopsNode, DecimateNode, ExtrudeFacesNode, ExtrudeRegionNode, InsetNode, MergeNode, SolidifyNode, SpinNode, SubdivideNode] #Overrides
outputs = [MeshNode, DrawModeNode]

node_categories = [PcgNodeCategory("inputs", "Inputs", items=[NodeItem(i.bl_idname) for i in inputs]),
                   PcgNodeCategory("transform", "Transform", items=[NodeItem(i.bl_idname) for i in transform]),
                   PcgNodeCategory("modifiers", "Modifiers", items=[NodeItem(i.bl_idname) for i in modifiers]),
                   PcgNodeCategory("conversion", "Conversion", items=[NodeItem(i.bl_idname) for i in conversion]),
                   PcgNodeCategory("selection", "Selection", items=[NodeItem(i.bl_idname) for i in selection]),
                   PcgNodeCategory("deletion", "Deletion", items=[NodeItem(i.bl_idname) for i in deletion]),
                   PcgNodeCategory("operators", "Operators", items=[NodeItem(i.bl_idname) for i in operators]),
                   PcgNodeCategory("outputs", "Outputs", items=[NodeItem(i.bl_idname) for i in outputs])]

def register():
    nodeitems_utils.register_node_categories("PcgNodeCategories", node_categories)
    bpy.utils.register_module(__name__)
def unregister():
    nodeitems_utils.unregister_node_categories("PcgNodeCategories")
    bpy.utils.unregister_module(__name__)
