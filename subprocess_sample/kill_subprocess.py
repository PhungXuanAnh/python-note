'''
Use a process group so as to enable sending a signal to all the process in the groups. 
For that, you should attach a session id to the parent process of the spawned/child processes, 
which is a shell in your case. This will make it the group leader of the processes. 
So now, when a signal is sent to the process group leader, 
it's transmitted to all of the child processes of this group.

Here's the code:
'''
import os
import signal
import subprocess
import time
import sys

cmd = 'ping localhost'
cmd = ['gateone']
# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.
pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
print pro.pid
time.sleep(10)
os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups


