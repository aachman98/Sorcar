import nodeitems_utils

from nodeitems_utils import NodeCategory
from ..helper import sc_poll_op

class ScNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return sc_poll_op(context)
    
    def __init__(self, identifier, name, description="", items=None, icon_value=0):
        self.icon_value = icon_value
        self.identifier = identifier
        self.name = name
        self.description = description

        if items is None:
            self.items = lambda context: []
        elif callable(items):
            self.items = items
        else:
            def items_gen(context):
                for item in items:
                    if (item):
                        if item.poll is None or context is None or item.poll(context):
                            yield item
                    else:
                        yield None
            self.items = items_gen
    
    def draw(self, context, layout):
        layout.menu("NODE_MT_category_%s" % self.identifier, icon_value=self.icon_value)
    
    def add_node_menu(): # Separate class to handle menu
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