import bpy
import traceback

from datetime import datetime

sc_logs = [] # Sample log: ("SORCAR [2020-08-24 18:51:23,143602] (INFO): ...log message...", 1)
mem_time = []

def str_to_level(str='INFO'):
    if str == 'NONE':
        return 0
    elif str == 'INFO':
        return 1
    elif str == 'DEBUG':
        return 2
    elif str == 'TRACE':
        return 3

def level_to_str(level=1):
    if level == 0:
        return 'NONE'
    elif level == 1:
        return 'INFO'
    elif level == 2:
        return 'DEBUG'
    elif level == 3:
        return 'TRACE'

def log(parent=None, child=None, func=None, msg="", level=1, mem='NONE'):
    # Set current time & delta time (in seconds)
    time_now = datetime.now()
    time_msg = None
    if (mem == 'SET'):
        mem_time.append(time_now)
        time_msg = "Recording time..."
    elif (mem == 'GET'):
        if (len(mem_time) > 0):
            time_msg = "Time taken = "+str((time_now - mem_time.pop()).total_seconds())+" seconds"
        else:
            time_msg = "'mem_time' empty"
    # Create log (string) and append to list along with its level
    log = "SORCAR " + time_now.strftime('[%d-%h-%Y %T,%f]') + " (" + level_to_str(level) + "): "
    if (parent):
        log += parent + ": "
    if (child):
        log += child + ": "
    if (func):
        log += func + "(): "
    log += msg
    if (time_msg):
        log += " (" + time_msg + ")"
    sc_logs.append((log, level))
    # Try to get minimum log level from user prefs (default to 1)
    try:
        min_level = str_to_level(bpy.context.preferences.addons.get(__package__).preferences.log_level)
    except:
        min_level = 1
    if (min_level >= level):
        print(log)

def flush_logs(level=1):
    logs = []
    for log in sc_logs:
        if (log[1] <= level):
            logs.append(log[0])
    return logs

def clear_logs():
    sc_logs.clear()

def print_traceback():
    log(msg="ERROR\n"+traceback.format_exc())