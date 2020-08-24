import bpy
import time

from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty
from ..helper import sc_poll_op
from ..debug import flush_logs

class ScFlushStacktrace(Operator):
    """Output the full stacktrace for the last execution of node-tree"""
    bl_idname = "sorcar.flush_stacktrace"
    bl_label = "Flush Stacktrace"

    prop_level: IntProperty(name="Log Level", default=2, min=1, max=3)
    prop_save: BoolProperty(name="Save as Text Block", default=False)

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        curr_tree = context.space_data.edit_tree
        logs = flush_logs(self.prop_level)
        if (len(logs) > 0):
            if (self.prop_save):
                t = bpy.data.texts.new("sc_" + time.strftime('%Y-%m-%d_%H-%M-%S') + ".log")
            for log in logs:
                print(log)
                if (self.prop_save):
                    t.write(log[0] + '\n')
            return {"FINISHED"}
        return {"CANCELLED"}