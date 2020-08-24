import bpy

from bpy.types import Panel
from bpy.props import PointerProperty
from ._base.panel_base import ScPanel

class ScDebugPanel(Panel, ScPanel):
    bl_label = "Debug"
    bl_idname = "NODE_PT_sc_debug"
    bl_order = 3

    def draw(self, context):
        layout = self.layout
        nt = context.space_data.node_tree
        n = nt.nodes.active
        layout.operator("sorcar.flush_stacktrace")
        if (n):
            arr_in = []
            arr_prop = []
            arr_out = []
            arr_internal = []
            for i in range(0, len(n.keys())):
                k = n.keys()[i]
                if (k.startswith('in_')):
                    arr_in.append((bpy.path.display_name(k.replace('in_', '')), eval('n.' + k)))
                elif (k.startswith('prop_')):
                    arr_prop.append((bpy.path.display_name(k.replace('prop_', '')), eval('n.' + k)))
                elif (k.startswith('out_')):
                    arr_out.append((bpy.path.display_name(k.replace('out_', '')), eval('n.' + k)))
                else:
                    arr_internal.append((bpy.path.display_name(k.replace('node', '')), eval('n.' + k)))
            if (len(arr_in) > 0):
                layout.label(text="Inputs")
                b = layout.box()
                for p in arr_in:
                    r = b.row()
                    r.label(text=p[0])
                    r.label(text=repr(p[1]))
            if (len(arr_prop) > 0):
                layout.label(text="Internal")
                b = layout.box()
                for p in arr_prop:
                    r = b.row()
                    r.label(text=p[0])
                    r.label(text=repr(p[1]))
            if (len(arr_out) > 0):
                layout.label(text="Outputs")
                b = layout.box()
                for p in arr_out:
                    r = b.row()
                    r.label(text=p[0])
                    r.label(text=repr(p[1]))
            if (len(arr_internal) > 0):
                layout.label(text="Inherited")
                b = layout.box()
                for p in arr_internal:
                    r = b.row()
                    r.label(text=p[0])
                    r.label(text=repr(p[1]))