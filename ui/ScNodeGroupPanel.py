import bpy

from bpy.types import Panel
from ._base.panel_base import ScPanel

class ScNodeGroupPanel(Panel, ScPanel):
    bl_label = "Node Groups"
    bl_idname = "NODE_PT_sc_node_group"

    def draw(self, context):
        layout = self.layout
        layout.operator("sorcar.group_nodes", text="Create Group", icon='GROUP')
        layout.operator("sorcar.edit_group", text="Edit Group", icon='MENU_PANEL')