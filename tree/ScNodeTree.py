import bpy

from bpy.props import BoolProperty
from bpy.types import NodeTree
from ..helper import print_log, update_each_frame

class ScNodeTree(NodeTree):
    bl_idname = 'ScNodeTree'
    bl_label = 'Sorcar'
    bl_icon = 'MESH_CUBE'

    node = None
    links_hash = 0

    def update_realtime(self, context):
        if not (update_each_frame in bpy.app.handlers.frame_change_post):
            bpy.app.handlers.frame_change_post.append(update_each_frame)
        return None
    prop_realtime: BoolProperty(name="Realtime", update=update_realtime)

    def get_links_hash(self):
        links = self.links
        links_data = []
        for link in links:
            links_data.append((link.from_node.name+":"+link.from_socket.name, link.to_node.name+":"+link.to_socket.name))
        return hash(str(links_data))
    
    def reset_nodes(self, execute):
        if (not self.nodes.get(str(self.node))):
            self.node = None
        for i in self.nodes:
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
        if (self.nodes.get(str(self.node))):
            print_log(msg="---EXECUTE NODE---")
            if (not self.nodes[self.node].execute()):
                print_log(self.name, msg="Failed to execute...")
            else:
                print_log(self.name, msg="Executed successfully!")