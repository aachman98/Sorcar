import bpy
from mathutils import Vector

from bpy.types import Operator
from ..helper import sc_poll_op, get_override
from ..debug import log

class ScGroupNodes(Operator):
    """Create node-group from selected nodes"""
    bl_idname = "sorcar.group_nodes"
    bl_label = "Group Nodes"

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)

    def execute(self, context):
        # Get space, path, current nodetree, selected nodes (except group input/output) and a newly created group
        space = context.space_data
        path = space.path
        node_tree = space.path[-1].node_tree
        node_group = bpy.data.node_groups.new("ScNodeGroup", "ScNodeTree")
        selected_nodes = []
        for n in node_tree.nodes:
            if n.select:
                if n.bl_idname in ['NodeGroupInput', 'NodeGroupOutput']:
                    n.select = False
                else:
                    selected_nodes.append(n)
        nodes_len = len(selected_nodes)

        # Store all links (internal/external) for the selected nodes to be created as group inputs/outputs
        links_external_in = []
        links_external_out = []
        for n in selected_nodes:
            for i in n.inputs:
                if (i.is_linked):
                    l = i.links[0]
                    if (not l.from_node in selected_nodes):
                        if (not l in links_external_in):
                            links_external_in.append(l)
            for o in n.outputs:
                if (o.is_linked):
                    for l in o.links:
                        if (not l.to_node in selected_nodes):
                            if (not l in links_external_out):
                                links_external_out.append(l)
        
        # Log the current node-tree, newly created group, and the number of nodes & sockets (input/output)
        log("OPERATOR", node_tree.name, self.bl_idname, "NodeGroup="+"\""+node_group.name+"\", Nodes="+str(nodes_len)+", Inputs="+str(len(links_external_in))+", Outputs="+str(len(links_external_out)), 1)

        # Calculate the required locations for placement of grouped node and input/output nodes
        loc_x_in = 0
        loc_x_out = 0
        loc_avg = Vector((0, 0))
        for n in selected_nodes:
            loc_avg += n.location/nodes_len
            if (n.location[0] < loc_x_in):
                loc_x_in = n.location[0]
            if (n.location[0] > loc_x_out):
                loc_x_out = n.location[0]
        
        # Create and relocate group input & output nodes in the newly created group
        group_input = node_group.nodes.new("NodeGroupInput")
        group_output = node_group.nodes.new("NodeGroupOutput")
        group_input.location = Vector((loc_x_in-200, loc_avg[1]))
        group_output.location = Vector((loc_x_out+200, loc_avg[1]))
        
        # Copy the selected nodes from current nodetree
        if (nodes_len > 0):
            bpy.ops.node.clipboard_copy(get_override(type='NODE_EDITOR'))
        
        # Create a grouped node with correct location and assign newly created group
        group_node = node_tree.nodes.new("ScNodeGroup")
        group_node.location = loc_avg
        group_node.node_tree = node_group
        
        # Add overlay to node editor for the newly created group
        path.append(node_group, node=group_node)
        
        # Paste the copied nodes to newly created group
        if (nodes_len > 0):
            bpy.ops.node.clipboard_paste(get_override(type='NODE_EDITOR'))

        # Create group input/output links in the newly created group
        o = group_input.outputs
        for link in links_external_in:
            # node_group.links.new(o.get(link.from_socket.name, o[len(o)-1]), node_group.nodes[link.to_node.name].inputs[link.to_socket.name])
            node_group.links.new(group_input.outputs[''], node_group.nodes[link.to_node.name].inputs[link.to_socket.name])
        i = group_output.inputs
        for link in links_external_out:
            # node_group.links.new(node_group.nodes[link.from_node.name].outputs[link.from_socket.name], i.get(link.to_socket.name, i[len(i)-1]))
            node_group.links.new(node_group.nodes[link.from_node.name].outputs[link.from_socket.name], group_output.inputs[''])
        
        # Add new links to grouped node from original external links
        for i in range(0, len(links_external_in)):
            link = links_external_in[i]
            node_tree.links.new(link.from_node.outputs[link.from_socket.name], group_node.inputs[i])
        for i in range(0, len(links_external_out)):
            link = links_external_out[i]
            node_tree.links.new(group_node.outputs[i], link.to_node.inputs[link.to_socket.name])
        
        # Remove redundant selected nodes
        for n in selected_nodes:
            node_tree.nodes.remove(n)

        return {'FINISHED'}