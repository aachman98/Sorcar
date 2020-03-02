import bpy

from bpy.props import FloatProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_setting import ScSettingNode

class ScSnap(Node, ScSettingNode):
    bl_idname = "ScSnap"
    bl_label = "Snap"

    prop_elements: EnumProperty(name="Snap To", items=[('INCREMENT', 'Increment', '', 1), ('VERTEX', 'Vertex', '', 2), ('EDGE', 'Edge', '', 4), ('FACE', 'Face', '', 8), ('VOLUME', 'Volume', '', 16), ('EDGE_MIDPOINT', 'Edge Center', '', 32), ('EDGE_PERPENDICULAR', 'Edge Perpendicular', '', 64)], default={'INCREMENT'}, options={'ENUM_FLAG'}, update=ScNode.update_value)
    prop_affect: EnumProperty(name="Affect", items=[('MOVE', 'Move', '', 1), ('ROTATE', 'Rotate', '', 2), ('SCALE', 'Scale', '', 4)], default={'MOVE'}, options={'ENUM_FLAG'}, update=ScNode.update_value)
    in_snap: BoolProperty(update=ScNode.update_value)
    in_target: EnumProperty(name="Snap With", items=[('CLOSEST', 'Closest', ''), ('CENTER', 'Center', ''), ('MEDIAN', 'Median', ''), ('ACTIVE', 'Active', '')], update=ScNode.update_value)
    in_grid: BoolProperty(update=ScNode.update_value)
    in_cull: BoolProperty(update=ScNode.update_value)
    in_peel: BoolProperty(update=ScNode.update_value)
    in_project: BoolProperty(update=ScNode.update_value)
    in_snap_self: BoolProperty(default=True, update=ScNode.update_value)
    in_align: BoolProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Snap").init("in_snap", True)
        self.inputs.new("ScNodeSocketString", "Snap With").init("in_target", True)
        self.inputs.new("ScNodeSocketBool", "Absolute Grid Snap").init("in_grid")
        self.inputs.new("ScNodeSocketBool", "Backface Culling").init("in_cull")
        self.inputs.new("ScNodeSocketBool", "Snap Peel Object").init("in_peel")
        self.inputs.new("ScNodeSocketBool", "Project Individual Elements").init("in_project")
        self.inputs.new("ScNodeSocketBool", "Project onto Self").init("in_snap_self")
        self.inputs.new("ScNodeSocketBool", "Align Rotation to Target").init("in_align")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.column().prop(self, "prop_elements", expand=True)
        layout.prop(self, "prop_affect", expand=True)
    
    def error_condition(self):
        return (
            super().error_condition()
            or len(self.prop_elements) == 0
            or (not self.inputs["Snap With"].default_value in ['CLOSEST', 'CENTER', 'MEDIAN', 'ACTIVE'])
        )
    
    def functionality(self):
        bpy.context.scene.tool_settings.use_snap = self.inputs["Snap"].default_value
        bpy.context.scene.tool_settings.snap_elements = self.prop_elements
        bpy.context.scene.tool_settings.snap_target = self.inputs["Snap With"].default_value
        bpy.context.scene.tool_settings.use_snap_grid_absolute = self.inputs["Absolute Grid Snap"].default_value
        bpy.context.scene.tool_settings.use_snap_backface_culling = self.inputs["Backface Culling"].default_value
        bpy.context.scene.tool_settings.use_snap_peel_object = self.inputs["Snap Peel Object"].default_value
        bpy.context.scene.tool_settings.use_snap_project = self.inputs["Project Individual Elements"].default_value
        bpy.context.scene.tool_settings.use_snap_translate = 'MOVE' in self.prop_affect
        bpy.context.scene.tool_settings.use_snap_rotate = 'ROTATE' in self.prop_affect
        bpy.context.scene.tool_settings.use_snap_scale = 'SCALE' in self.prop_affect
        bpy.context.scene.tool_settings.use_snap_self = self.inputs["Project onto Self"].default_value
        bpy.context.scene.tool_settings.use_snap_align_rotation = self.inputs["Align Rotation to Target"].default_value
