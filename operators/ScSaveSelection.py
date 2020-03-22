import bpy

from bpy.types import Operator
from ..helper import sc_poll

class ScSaveSelection(Operator):
    bl_idname = "sc.save_selection"
    bl_label = "Save Selection"

    @classmethod
    def poll(cls, context):
        return sc_poll(context)

    def execute(self, context):
        context.space_data.edit_tree.nodes.active.save_selection()
        return {"FINISHED"}