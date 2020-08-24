from datetime import datetime

# Log levels:
# 1. Info - Reg/unreg, updater, version, etc.
# 2. Dataflow - Node-trees, nodes, node-groups, etc.
# 3. All - Node functions, socket functions, error conditions, etc.
#
# Sample log: ("[2020-08-24 18:51:23,143602] SORCAR: ...log message...", 1)
sc_logs = []

def log(parent=None, child=None, func=None, msg="", level=1):
    log = datetime.now().strftime('[%d-%h-%Y %T,%f] ') + "SORCAR: "
    if (parent):
        log += parent + ": "
    if (child):
        log += child + ": "
    if (func):
        log += func + "(): "
    log += msg
    sc_logs.append((log, level))

def flush_logs(level=1):
    logs = []
    for log in sc_logs:
        if (log[1] <= level):
            logs.append(log[0])
    return logs

def clear_logs():
    sc_logs.clear()