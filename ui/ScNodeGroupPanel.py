import bpy

from bpy.types import Panel
from ._base.panel_base import ScPanel

class ScNodeGroupPanel(Panel, ScPanel):
    """Create/Edit Sorcar Node-Groups"""
    bl_label = "Node Groups"
    bl_idname = "NODE_PT_sc_node_group"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello world!", icon='WORLD_DATA')