import nodeitems_utils

from nodeitems_utils import NodeCategory

class ScNodeCategory(NodeCategory):
    @classmethod
    def poll(self, context):
        return context.space_data.tree_type == "ScNodeTree"