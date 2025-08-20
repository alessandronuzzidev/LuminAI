import os
import signal

def control_monitor(action):
    if not os.path.exists("data/monitor.pid"):
        return

    with open("data/monitor.pid") as f:
        pid = int(f.read().strip())

    if action == "pause":
        os.kill(pid, signal.SIGUSR1)
    elif action == "resume":
        os.kill(pid, signal.SIGUSR2)
    else:
        return
