import bpy

from ...helper import sc_poll_op

class ScPanel():
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Sorcar"
    
    @classmethod
    def poll(self, context):
        return sc_poll_op(context)