import bpy

from bpy.props import BoolProperty, StringProperty
from bpy.types import NodeTree
from ..helper import print_log, update_each_frame, remove_object

class ScNodeTree(NodeTree):
    bl_idname = 'ScNodeTree'
    bl_label = 'Sorcar'
    bl_icon = 'MESH_CUBE'

    node = None
    links_hash = 0
    objects = []
    variables: {}

    def update_realtime(self, context):
        if not (update_each_frame in bpy.app.handlers.frame_change_post):
            bpy.app.handlers.frame_change_post.append(update_each_frame)
        return None
    prop_realtime: BoolProperty(name="Realtime", update=update_realtime)
    prop_clear_vars: BoolProperty(name="Clear variables", default=True)

    def register_object(self, object):
        if (object not in self.objects):
            self.objects.append(object)
    
    def unregister_object(self, object):
        if object in self.objects:
            remove_object(object)
            self.objects.remove(object)
    
    def unregister_all_objects(self):
        for object in self.objects:
            remove_object(object)
        self.objects = []

    def get_links_hash(self):
        links = self.links
        links_data = []
        for link in links:
            links_data.append((link.from_node.name+":"+link.from_socket.identifier, link.to_node.name+":"+link.to_socket.identifier))
        return hash(str(links_data))
    
    def reset_nodes(self, execute):
        if (not self.nodes.get(str(self.node))):
            self.node = None
        for i in self.nodes:
            if (hasattr(i, "reset")):
                i.reset(execute)
    
    def update_links(self):
        for i in self.links:
            if not (i.to_socket.bl_rna.name == i.from_socket.bl_rna.name):
                if (i.to_socket.bl_rna.name == "ScNodeSocketArrayPlaceholder"):
                    new_socket = i.to_node.inputs.new(i.from_socket.bl_rna.name, i.from_socket.bl_label)
                    self.links.new(i.from_socket, new_socket)
                    self.links.remove(i)

    def update(self):
        self.update_links()
        links_hash = self.get_links_hash()
        if (not self.links_hash == links_hash):
            self.execute_node()
            self.links_hash = links_hash
        self.reset_nodes(False)
    
    def execute_node(self):
        self.reset_nodes(True)
        n = self.nodes.get(str(self.node))
        if (n):
            if (self.prop_clear_vars):
                self.variables = {}
            self.unregister_all_objects()
            if (hasattr(n, "execute")):
                print_log(msg="---EXECUTE NODE---")
                if (not n.execute()):
                    print_log(self.name, msg="Failed to execute...")
                else:
                    print_log(self.name, msg="Executed successfully!")
    
    def set_value(self, node_name="Cube", attr_name="in_size", value=1, refresh=True):
        n = self.nodes.get(node_name)
        if (n):
            setattr(n, attr_name, value)
            if (refresh):
                self.execute_node();
    
    def set_preview(self, node_name="Cube"):
        n = self.nodes.get(node_name)
        if (n):
            self.node = n.name
            self.execute_node();