# Copyright (C) 2019 Punya Aachman
# aachman98@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
	"name": "Sorcar",
    "author": "Punya Aachman",
    "version": (3, 2, 2),
    "blender": (2, 81, 0),
    "location": "Node Editor",
    "category": "Node",
    "description": "Create procedural meshes using Node Editor",
	"wiki_url": "https://github.com/aachman98/Sorcar/wiki",
    "tracker_url": "https://github.com/aachman98/Sorcar/issues"
}

import bpy
import nodeitems_utils
import addon_utils
import importlib
import os

from bpy.types import NodeTree, Operator, PropertyGroup, AddonPreferences
from bpy.props import BoolProperty, StringProperty, IntProperty, EnumProperty

from .tree.ScNodeCategory import ScNodeCategory
from .tree.ScNodeTree import ScNodeTree
from .tree.ScNodeItem import ScNodeItem

from .helper import update_each_frame
from .debug import log

from . import addon_updater_ops

class SorcarPreferences(AddonPreferences):
    bl_idname = __package__
    bl_label = "Sorcar Preferences"

    log_level: EnumProperty(
    name = "Log Level",
    description = "Maximum level of logs to print to console",
    items = [
        ('NONE', '0: None', 'No logs'),
        ('INFO', '1: Info', 'Register/unregister, addon-updater, versions, etc.'),
        ('DEBUG', '2: Dataflow', 'Node-trees, node-groups, nodes, sockets, etc.'),
        ('TRACE', '3: All', 'Node functions, socket functions, error conditions, etc.')
    ],
    default = 'INFO',
    )
    # Addon updater properties
    auto_check_update: BoolProperty(
    name = "Auto-check for Update",
    description = "If enabled, auto-check for updates using an interval",
    default = False,
    )
    updater_intrval_months: IntProperty(
        name='Months',
        description = "Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days: IntProperty(
        name='Days',
        description = "Number of days between checking for updates",
        default=7,
        min=0,
    )
    updater_intrval_hours: IntProperty(
        name='Hours',
        description = "Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes: IntProperty(
        name='Minutes',
        description = "Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        self.layout.prop(self, "log_level")
        addon_updater_ops.update_settings_ui(self, context)

def import_ops(path="./"):
    out = []
    for i in bpy.path.module_names(path + "operators"):
        out.append(getattr(importlib.import_module(".operators." + i[0], __name__), i[0]))
        log("IMPORT", "Operator", msg=i[0], level=2)
    return out

def import_sockets(path="./"):
    out = []
    for i in bpy.path.module_names(path + "sockets"):
        out.append(getattr(importlib.import_module(".sockets." + i[0], __name__), i[0]))
        log("IMPORT", "Socket", msg=i[0], level=2)
    return out

def import_ui(path="./"):
    out = []
    for i in bpy.path.module_names(path + "ui"):
        out.append(getattr(importlib.import_module(".ui." + i[0], __name__), i[0]))
        log("IMPORT", "UI Panel", msg=i[0], level=2)
    return out

def import_nodes(path="./"):
    out = {}
    for cat in [i for i in os.listdir(path + "nodes") if not i.startswith("_")]:
        out[cat] = []
        for i in bpy.path.module_names(path + "nodes/" + cat):
            out[cat].append(getattr(importlib.import_module(".nodes." + cat + "." + i[0], __name__), i[0]))
            log("IMPORT", "Node ("+bpy.path.display_name(cat)+")", msg=i[0], level=2)
    return out

def init_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="Node Generic", space_type='NODE_EDITOR')
    kmi = [
        km.keymap_items.new("sorcar.execute_node", 'E', 'PRESS'),
        km.keymap_items.new("sorcar.clear_preview", 'E', 'PRESS', alt=True),
        km.keymap_items.new("sorcar.group_nodes", 'G', 'PRESS', ctrl=True),
        km.keymap_items.new("sorcar.edit_group", 'TAB', 'PRESS')
    ]
    return km, kmi

def sc_register_node_categories(identifier, cat_list):
    if identifier in nodeitems_utils._node_categories:
        raise KeyError("Node categories list '%s' already registered" % identifier)
        return
    
    menu_types = []

    # works as draw function for menus
    def draw_node_item(self, context):
        layout = self.layout
        col = layout.column()
        for item in self.category.items(context):
            item.draw(item, col, context)

    for cat in cat_list:
        if (cat):
            menu_type = type("NODE_MT_category_" + cat.identifier, (bpy.types.Menu,), {
                "bl_space_type": 'NODE_EDITOR',
                "bl_label": cat.name,
                "category": cat,
                "poll": cat.poll,
                "draw": draw_node_item,
            })
            menu_types.append(menu_type)
            bpy.utils.register_class(menu_type)

    def draw_add_menu(self, context):
        layout = self.layout
        col = layout.column()
        for cat in cat_list:
            if (cat):
                if cat.poll(context):
                    cat.draw(context, col)
            else:
                col.separator()

    # stores: (categories list, menu draw function, submenu types)
    nodeitems_utils._node_categories[identifier] = (cat_list, draw_add_menu, menu_types)

all_classes = []
addon_keymaps = []

def register():
    log(msg="REGISTERING...")
    path = repr([i for i in addon_utils.modules() if i.bl_info['name'] == "Sorcar"][0]).split("from '")[1].split("__init__.py'>")[0]
    classes_ops = import_ops(path)
    classes_sockets = import_sockets(path)
    classes_ui = import_ui(path)
    classes_nodes = import_nodes(path)

    global all_classes, addon_keymaps
    all_classes = [ScNodeTree]
    all_classes.extend(classes_ops)
    all_classes.extend(classes_sockets)
    all_classes.extend(classes_ui)
    all_classes.append(SorcarPreferences)

    total_nodes = 0
    cat_ordered = ScNodeCategory.add_node_menu()
    cat_unordered = [i for i in classes_nodes if (not i in cat_ordered)]
    if (len(cat_unordered) > 0):
        cat_ordered.append(None)
        cat_ordered.extend(cat_unordered)
    node_categories = []
    for cat in cat_ordered:
        if (cat):
            total_nodes += len(classes_nodes[cat])
            node_categories.append(ScNodeCategory(identifier="sc_"+cat, name=bpy.path.display_name(cat), items=[ScNodeItem(i.bl_idname) for i in classes_nodes[cat]]))
            all_classes.extend(classes_nodes[cat])
        else:
            node_categories.append(None)
    
    for i in all_classes:
        bpy.utils.register_class(i)
    sc_register_node_categories("sc_node_categories", node_categories)
    if not (update_each_frame in bpy.app.handlers.frame_change_post):
        bpy.app.handlers.frame_change_post.append(update_each_frame)
    
    if (not bpy.app.background):
        km, kmi = init_keymaps()
        for k in kmi:
            k.active = True
            addon_keymaps.append((km, k))
    
    addon_updater_ops.register(bl_info)
    
    log("REGISTERED", msg="{} operators, {} sockets, {} UI panels, {} keymaps & {} nodes ({} categories)".format(len(classes_ops), len(classes_sockets), len(classes_ui), len(addon_keymaps), total_nodes, len(classes_nodes)))

def unregister():
    log(msg="UNREGISTERING...")
    global all_classes, addon_keymaps
    all_classes.reverse()

    for i in all_classes:
        bpy.utils.unregister_class(i)
        log("UNREGISTER", i.bl_idname, msg=i.bl_label, level=2)
    nodeitems_utils.unregister_node_categories("sc_node_categories")
    if (update_each_frame in bpy.app.handlers.frame_change_post):
        bpy.app.handlers.frame_change_post.remove(update_each_frame)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    addon_updater_ops.unregister()

    log("UNREGISTERED", msg=str(len(all_classes)) + " classes")