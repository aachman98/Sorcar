import bpy

from bpy.props import BoolProperty
from bpy.types import NodeTree
from ..helper import print_log

class ScNodeTree(NodeTree):
    bl_idname = 'ScNodeTree'
    bl_label = 'Sorcar'
    bl_icon = 'MESH_CUBE'

    node = None
    links_hash = 0
    prop_realtime: BoolProperty(name="Realtime")

    def get_links_hash(self):
        links = self.links
        links_data = []
        for link in links:
            links_data.append((link.from_node.name+":"+link.from_socket.name, link.to_node.name+":"+link.to_socket.name))
        return hash(str(links_data))
    
    def reset_nodes(self):
        for i in self.nodes:
            i.reset()
    
    def update_links(self):
        for i in self.links:
            if not (i.to_socket.bl_rna.name == i.from_socket.bl_rna.name):
                if not (i.to_socket.bl_rna.name == "ScNodeSocketArrayPlaceholder"):
                    self.links.remove(i)

    def update(self):
        # self.update_links()
        links_hash = self.get_links_hash()
        if (not self.links_hash == links_hash):
            self.execute_node()
            self.links_hash = links_hash
        if (not self.nodes.get(str(self.node))):
            self.node = None
        self.reset_nodes()
    
    def execute_node(self):
        if (not self.nodes.get(str(self.node))):
            self.node = None
        self.reset_nodes()
        if (self.nodes.get(str(self.node))):
            print_log(msg="---EXECUTE NODE---")
            if (not self.nodes[self.node].execute()):
                print_log(self.name, msg="Failed to execute...")
            else:
                print_log(self.name, msg="Executed successfully!")