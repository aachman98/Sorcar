import bpy
import time

from bpy.types import Operator
from bpy.props import EnumProperty
from ..helper import sc_poll_op
from ..debug import flush_logs, str_to_level

class ScFlushStacktrace(Operator):
    """Output the full stacktrace for the last execution of node-tree"""
    bl_idname = "sorcar.flush_stacktrace"
    bl_label = "Flush Stacktrace"

    prop_level: EnumProperty(
    name = "Log Level",
    description = "Maximum level of logs to output",
    items = [
        ('INFO', '1: Info', 'Register/unregister, addon-updater, versions, etc.'),
        ('DEBUG', '2: Dataflow', 'Node-trees, node-groups, nodes, sockets, etc.'),
        ('TRACE', '3: All', 'Node functions, socket functions, error conditions, etc.')
    ],
    default = 'DEBUG',
    )

    prop_save: EnumProperty(
    name = "Output",
    items = [
        ('CONSOLE', 'Console', 'Print logs to external console/terminal only'),
        ('TEXT', 'Text-Block', 'Save as internal text block only'),
        ('BOTH', 'Both', 'Print to console and save as text')
    ],
    default = 'CONSOLE',
    )

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        curr_tree = context.space_data.edit_tree
        logs = flush_logs(str_to_level(self.prop_level))
        if (len(logs) > 0):
            str = "sc_" + time.strftime('%Y-%m-%d_%H-%M-%S') + ".log"
            if (self.prop_save in ['TEXT', 'BOTH']):
                text = bpy.data.texts.new(str)
            if (self.prop_save in ['CONSOLE', 'BOTH']):
                print("#"*48)
                print("#"*10+" "+str+" "+"#"*10)
                print("#"*48)
            for log in logs:
                if (self.prop_save in ['CONSOLE', 'BOTH']):
                    print(log)
                if (self.prop_save in ['TEXT', 'BOTH']):
                    text.write(log + '\n')
            if (self.prop_save in ['CONSOLE', 'BOTH']):
                print("#"*48)
            return {'FINISHED'}
        return {'CANCELLED'}