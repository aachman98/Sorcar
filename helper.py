import bpy
from mathutils import Vector

def focus_on_object(obj, edit=False):
    if (bpy.ops.object.mode_set.poll()):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
    if (obj):
        if (obj.name in bpy.context.view_layer.objects):
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            if (edit):
                bpy.ops.object.mode_set(mode="EDIT")

def remove_object(obj):
    if (obj):
        data = obj.data
        bpy.data.objects.remove(object=obj)
        if (data):
            bpy.data.meshes.remove(mesh=data)

def get_override(active=None, edit=False, selected=[]):
    override = bpy.context.copy()
    override["active_object"] = active
    if (edit):
        override["edit_object"] = active
    if (active not in selected):
        selected.append(active)
    override["selected_object"] = selected
    override["area"] = [i for i in bpy.context.screen.areas if i.type == 'VIEW_3D'][0]
    override["region"] = [i for i in override["area"].regions if i.type == 'WINDOW'][0]
    return override

def print_log(parent=None, child=None, func=None, msg=""):
    log = "SORCAR: "
    if (parent):
        log += parent + ": "
    if (child):
        log += child + ": "
    if (func):
        log += func + "(): "
    log += msg
    print(log)

def update_each_frame(scene):
    for i in bpy.data.node_groups:
        if (i.bl_idname == "ScNodeTree"):
            if (i.prop_realtime):
                i.execute_node()

def convert_data(data, from_type=None, to_type=None):
    if (data == None or from_type == None or to_type == None):
        return False, None
    try:
        if (to_type == "NUMBER"):
            if (from_type == "NUMBER"):
                val = data
            elif (from_type == "BOOL"):
                val = float(data)
            elif (from_type == "STRING"):
                val = float(eval(data))
            elif (from_type == "VECTOR"):
                val = Vector(data).magnitude
            elif (from_type == "OBJECT"):
                val = bpy.data.objects.find(data.name)
            elif (from_type == "ARRAY"):
                val = len(eval(data))
            elif (from_type == "SELECTION_TYPE"):
                return False, None
        elif (to_type == "BOOL"):
            if (from_type == "NUMBER"):
                val = bool(data)
            elif (from_type == "BOOL"):
                val = data
            elif (from_type == "STRING"):
                val = bool(data)
            elif (from_type == "VECTOR"):
                val = bool(data)
            elif (from_type == "OBJECT"):
                val = bool(data)
            elif (from_type == "ARRAY"):
                val = bool(eval(data))
            elif (from_type == "SELECTION_TYPE"):
                val = data[0] or data[1] or data[2]
        elif (to_type == "STRING"):
            if (from_type == "NUMBER"):
                val = str(data)
            elif (from_type == "BOOL"):
                val = str(data)
            elif (from_type == "STRING"):
                val = data
            elif (from_type == "VECTOR"):
                val = str(Vector(data).to_tuple())
            elif (from_type == "OBJECT"):
                val = str(repr(data))
            elif (from_type == "ARRAY"):
                val = data
            elif (from_type == "SELECTION_TYPE"):
                val = selection_type_to_string(data)
        elif (to_type == "VECTOR"):
            if (from_type == "NUMBER"):
                val = (data, data, data)
            elif (from_type == "BOOL"):
                val = (float(data), float(data), float(data))
            elif (from_type == "STRING"):
                val = Vector(eval(data)).to_tuple()
            elif (from_type == "VECTOR"):
                val = data
            elif (from_type == "OBJECT"):
                return False, None
            elif (from_type == "ARRAY"):
                val = Vector((eval(data)[0], eval(data)[1], eval(data)[2])).to_tuple()
            elif (from_type == "SELECTION_TYPE"):
                val = Vector((float(eval(data)[0]), float(eval(data)[1]), float(eval(data)[2]))).to_tuple()
        elif (to_type == "OBJECT"):
            if (from_type == "NUMBER"):
                val = bpy.data.objects[data]
            elif (from_type == "BOOL"):
                return False, None
            elif (from_type == "STRING"):
                val = bpy.data.objects[eval(data).name]
            elif (from_type == "VECTOR"):
                return False, None
            elif (from_type == "OBJECT"):
                val = data
            elif (from_type == "ARRAY"):
                return False, None
        elif (to_type == "ARRAY"):
            if (from_type == "NUMBER"):
                val = "[" + str(data) + "]"
            elif (from_type == "BOOL"):
                val = "[" + str(data) + "]"
            elif (from_type == "STRING"):
                val = str(list(eval(data)))
            elif (from_type == "VECTOR"):
                val = str(list(data))
            elif (from_type == "OBJECT"):
                val = "[" + repr(data) + "]"
            elif (from_type == "ARRAY"):
                val = data
            elif (from_type == "SELECTION_TYPE"):
                val = data
        elif (to_type == "SELECTION_TYPE"): # TODO: Add more automatic conversions
            if (from_type == "NUMBER"):
                return False, None
            elif (from_type == "BOOL"):
                return False, None
            elif (from_type == "STRING"):
                return False, None
            elif (from_type == "VECTOR"):
                val = [bool(data[0]), bool(data[1]), bool(data[2])]
            elif (from_type == "OBJECT"):
                return False, None
            elif (from_type == "ARRAY"):
                val = [bool(eval(data)[0]), bool(eval(data)[1]), bool(eval(data)[2])]
            elif (from_type == "SELECTION_TYPE"):
                val = data
        return True, val
    except:
        return False, None

def selection_type_to_string(sel_type):
    out = []
    if sel_type[0]:
        out.append("Vertex")

    if sel_type[1]:
        out.append("Edge")

    if sel_type[2]:
        out.append("Face")

    return " + ".join(out)