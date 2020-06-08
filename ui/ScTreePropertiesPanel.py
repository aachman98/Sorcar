import bpy

from bpy.types import Panel
from ._base.panel_base import ScPanel

class ScTreePropertiesPanel(Panel, ScPanel):
    bl_label = "Properties"
    bl_idname = "NODE_PT_sc_tree_properties"
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        nt = context.space_data.node_tree
        layout.label(text="Preview node: " + str(nt.node), icon='NODE')
        layout.prop(nt, "prop_realtime")
        layout.prop(nt, "prop_clear_vars")