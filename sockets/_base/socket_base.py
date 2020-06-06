import bpy

from bpy.props import StringProperty, BoolProperty
from mathutils import Vector
from ...helper import print_log, convert_data

class ScNodeSocket:
    default_prop: StringProperty()
    socket_error: BoolProperty()

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
    
    def draw_layout(self, context, layout, node, prop, text):
        # Draw overridable custom layout of socket
        layout.prop(node, prop, text=text)
    
    def draw(self, context, layout, node, text):
        if (self.is_output):
            layout.label(text=text + ": " + self.get_label())
        else:
            if (self.socket_error):
                layout.label(icon='ERROR')
            if (self.is_linked):
                layout.label(text=text + ": " + self.get_label())
            else:
                if (self.default_prop == ""):
                    if (self.node.bl_idname == "ScNodeGroup" and [i for i in node.node_tree.inputs if i.identifier==self.identifier][0].show_prop):
                        self.draw_layout(context, layout, self, "default_value_update", text)
                    else:
                        layout.label(text=text)
                else:
                    layout.prop(self, "hide", icon='RADIOBUT_OFF', icon_only=True, invert_checkbox=True)
                    self.draw_layout(context, layout, node, self.default_prop, text)
    
    def execute(self, forced):
        # Execute node socket to get/set default_value
        if (self.is_output):
            if (self.node.type == "GROUP_INPUT"):
                return True
            return self.node.execute(forced)
        else:
            self.socket_error = True
            # if (len(self.links) > 0):
            if (self.is_linked): # self.is_linked doesn't get updated quickly (when using realtime update & modify links)
                from_node = self.links[0].from_node
                from_socket = self.links[0].from_socket
                while (from_node.bl_idname == "NodeReroute"):
                    if (not from_node.inputs[0].is_linked):
                        from_socket = None
                        break
                    from_socket = from_node.inputs[0].links[0].from_socket
                    from_node = from_node.inputs[0].links[0].from_node
                if (from_socket and from_socket.execute(forced)):
                    ret, data = from_socket.get_data(self.default_type)
                    if(ret):
                        self.socket_error = False
                        return self.set(data)
                    else:
                        print_log(self.node.name, self.name, "execute", msg="No ret")
            else:
                if (self.default_prop == ""):
                    if (self.node.bl_idname == "ScNodeGroup" and [i for i in self.node.node_tree.inputs if i.identifier==self.identifier][0].show_prop):
                        self.socket_error = False
                        self.default_value = self.default_value_update
                        return True
                    return False
                self.socket_error = False
                return self.set(eval("bpy.data.node_groups['" + self.id_data.name + "'].nodes['" + self.node.name + "']." + self.default_prop))
            return False