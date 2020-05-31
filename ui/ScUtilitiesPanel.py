import bpy

from bpy.types import Panel
from ._base.panel_base import ScPanel

class ScUtilitiesPanel(Panel, ScPanel):
    bl_label = "Utilities"
    bl_idname = "NODE_PT_sc_utilities"
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        layout.operator("node.join", text="Frame (Comment)", icon='SEQ_STRIP_META')