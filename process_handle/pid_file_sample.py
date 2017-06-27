'''
Created on Jun 27, 2017

@author: xuananh
'''
import os, sys
import logging

pidfile = '/tmp/pid_file_sample.pid'

if os.path.isfile(pidfile):
    old_pid = file(pidfile, 'r').read().strip()
    old_pid_path = '/proc/' + old_pid 
     
    if os.path.exists(old_pid_path) and old_pid != '' and old_pid != None:
        print("Python script is still running, pid: {}".format(old_pid))
        sys.exit(1)
    else:
        os.unlink(pidfile)
 
# create pid lock file        
with open(pidfile, 'w+') as f:
    print("pid = {}".format(os.getpid()))
    f.write('{}'.format(os.getpid()))



while True:
    pass