import subprocess
import time
import os
import signal
import sys

import psutil

NOW_PID_FILE = 'now.pid'
RESTARTER_PID_FILE = 'restarter.pid'


# Logging function
def AddLog(status):
    # Add line to status log
    logFile = open('restartlog.txt', 'a')
    timeString = time.asctime(time.localtime(time.time()))
    logFile.write('%s %s\n' % (timeString, status))
    # Force the log to be written out
    logFile.flush()
    logFile.close()






while True:
    # Check the state of the process
    if not os.path.isfile(NOW_PID_FILE):
        try:
            # Process is not running, restart it
            AddLog('Process not running, restarting')
            process = subprocess.Popen(['python3.8', 'NOW.py'])
            with open(NOW_PID_FILE, 'w') as f:
                f.write(str(process.pid))
            print(f'Started process with PID {process.pid}')
            time.sleep(5)
            AddLog('Restarted')
        except OSError:
            time.sleep(5)

    else:
        with open(NOW_PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        if psutil.pid_exists(pid):
            AddLog('Process running')
        else:
            AddLog('Process not running, restarting')
            process = subprocess.Popen(['python3.8', 'NOW.py'])
            with open(NOW_PID_FILE, 'w') as f:
                f.write(str(process.pid))
            print(f'Restarted process with PID {process.pid}')
            time.sleep(5)
            AddLog('Restarted')
    time.sleep(5)


