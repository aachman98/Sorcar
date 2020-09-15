import nodeitems_utils

from nodeitems_utils import NodeCategory

class ScNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "ScNodeTree"
    
    def __init__(self, identifier, name, description="", items=None, icon_value=0):
        self.icon_value = icon_value
        super().__init__(identifier, name, description, items)
    
    def draw(self, context, layout):
        layout.menu("NODE_MT_category_%s" % self.identifier, icon_value=self.icon_value)
    
    def add_node_menu():
        return [
            "inputs",
            "curves",
            None,
            "transform",
            "selection",
            "deletion",
            None,
            "component_operators",
            "object_operators",
            "modifiers",
            None,
            "constants",
            "arrays",
            "noise",
            None,
            "utilities",
            "settings",
            None,
            "flow_control"
        ]