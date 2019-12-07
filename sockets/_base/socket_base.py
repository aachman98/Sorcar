import bpy

from bpy.props import StringProperty
from mathutils import Vector
from ...helper import print_log, convert_data

class ScNodeSocket:
    default_prop: StringProperty()

    def get_label(self):
        return str(self.default_value)
    
    def get_data(self, data_type=None):
        return convert_data(self.default_value, self.default_type, data_type)
    
    def set(self, val, data_type=None):
        ret = True
        if (data_type):
            ret, data = convert_data(val, data_type, self.default_type)
        else:
            data = val
        if (ret):
            self.default_value = data
            return True
        print_log(self.node.name, self.name, "set", "Value not set")
        return False
    
    def init(self, default_prop="", visible=False):
        # Initialise node socket values
        self.default_prop = default_prop
        if not (self.is_output or default_prop == ""):
            self.hide = not visible

    def draw_color(self, context, node):
        return self.color
    
    def draw(self, context, layout, node, text):
        if (self.is_output):
            layout.label(text=text + " (" + self.get_label() + ")")
        else:
            if (self.is_linked):
                layout.label(text=text + " (" + self.get_label() + ")")
            else:
                if (self.default_prop == ""):
                    layout.label(text=text)
                else:
                    layout.prop(self, "hide", icon='RADIOBUT_OFF', icon_only=True, invert_checkbox=True)
                    if self.default_prop == "in_selection_type":
                        row = layout.row(align = True)
                        row.label(text=text)
                        row.prop(node, self.default_prop, index = 0, toggle = True, icon_only = True, icon = "VERTEXSEL")
                        row.prop(node, self.default_prop, index = 1, toggle = True, icon_only = True, icon = "EDGESEL")
                        row.prop(node, self.default_prop, index = 2, toggle = True, icon_only = True, icon = "FACESEL")
                    else:
                        layout.column().prop(node, self.default_prop, text=text)
    
    def execute(self, forced):
        # Execute node socket to get/set default_value
        if (self.is_output):
            return self.node.execute(forced)
        else:
            if (self.is_linked):
                if (self.links[0].from_socket.execute(forced)):
                    ret, data = self.links[0].from_socket.get_data(self.default_type)
                    if(ret):
                        return self.set(data)
                    else:
                        print_log(self.name, msg="No ret")
            else:
                if (self.default_prop == ""):
                    return False
                return self.set(eval("bpy.data.node_groups['" + self.id_data.name + "'].nodes['" + self.node.name + "']." + self.default_prop))
            return False