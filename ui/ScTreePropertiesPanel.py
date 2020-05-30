import bpy

from bpy.types import Panel
from ._base.panel_base import ScPanel

class ScTreePropertiesPanel(Panel, ScPanel):
    bl_label = "Properties"
    bl_idname = "NODE_PT_sc_tree_properties"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.space_data.node_tree, "prop_realtime")