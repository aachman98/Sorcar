import bpy
import nodeitems_utils

from nodeitems_utils import NodeItem

class ScNodeItem(NodeItem):
    def __init__(self, nodetype, label=None, icon=None, settings=None, poll=None):

        if settings is None:
            settings = {}

        self.nodetype = nodetype
        self._label = label
        self._icon = icon
        self.settings = settings
        self.poll = poll
    
    @property
    def icon(self):
        if self._icon:
            return self._icon
        else:
            # if no custom icon is defined, fall back to the node type UI icon
            bl_rna = bpy.types.Node.bl_rna_get_subclass(self.nodetype)
            if bl_rna is not None:
                return getattr(bl_rna, "bl_icon", 'NONE')
    
    @staticmethod
    def draw(self, layout, _context):
        props = layout.operator("node.add_node", text=self.label, text_ctxt=self.translation_context, icon=self.icon)
        props.type = self.nodetype
        props.use_transform = True

        for setting in self.settings.items():
            ops = props.settings.add()
            ops.name = setting[0]
            ops.value = setting[1]