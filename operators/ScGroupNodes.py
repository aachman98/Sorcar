import bpy
from mathutils import Vector

from bpy.types import Operator
from ..helper import sc_poll_op, get_override

class ScGroupNodes(Operator):
    bl_idname = "sc.group_nodes"
    bl_label = "Group Nodes"

    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)

    def execute(self, context):
        space = context.space_data
        node_tree = space.node_tree
        node_group = bpy.data.node_groups.new("ScNodeGroup", "ScNodeTree")
        
        group_input = node_group.nodes.new("NodeGroupInput")
        group_output = node_group.nodes.new("NodeGroupOutput")
        selected_nodes = [i for i in node_tree.nodes if i.select]
        l = len(selected_nodes)

        loc_x_in = 0
        loc_x_out = 0
        loc_avg = Vector((0, 0))
        for n in selected_nodes:
            loc_avg += n.location/l
            if (n.location[0] < loc_x_in):
                loc_x_in = n.location[0]
            if (n.location[0] > loc_x_out):
                loc_x_out = n.location[0]
        
        if (l > 0):
            bpy.ops.node.clipboard_copy(get_override(type='NODE_EDITOR'))
        space.path.append(node_group)
        if (l > 0):
            bpy.ops.node.clipboard_paste(get_override(type='NODE_EDITOR'))

        group_input.location = Vector((loc_x_in-200, loc_avg[1]))
        group_output.location = Vector((loc_x_out+200, loc_avg[1]))

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
                    l = o.links[0]
                    if (not l.to_node in selected_nodes):
                        if (not l in links_external_out):
                            links_external_out.append(l)

        # for link in links_external_in:
        #     node_group.links.new(group_input.outputs[''], group_nodes[link.to_node].inputs[link.to_socket.name])
        # for link in links_external_out:
        #     node_group.links.new(group_nodes[link.from_node].outputs[link.from_socket.name], group_output.inputs[''])

        for link in links_external_in:
            node_group.links.new(group_input.outputs[''], node_group.nodes[link.to_node.name].inputs[link.to_socket.name])
        for link in links_external_out:
            node_group.links.new(node_group.nodes[link.from_node.name].outputs[link.from_socket.name], group_output.inputs[''])

        group_node = node_tree.nodes.new("ScNodeGroup")
        group_node.location = loc_avg
        group_node.node_tree = node_group
        
        for i in range(0, len(links_external_in)):
            link = links_external_in[i]
            node_tree.links.new(link.from_node.outputs[link.from_socket.name], group_node.inputs[i])
        for i in range(0, len(links_external_out)):
            link = links_external_out[i]
            node_tree.links.new(group_node.outputs[i], link.to_node.inputs[link.to_socket.name])

        for n in selected_nodes:
            node_tree.nodes.remove(n)

        return {"FINISHED"}