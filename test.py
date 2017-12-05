'''
check if screen is locked on ubuntu 16.04
'''

import subprocess, time

def is_screen_locked():
    command = "gdbus call -e -d com.canonical.Unity -o /com/canonical/Unity/Session -m com.canonical.Unity.Session.IsLocked"
    process = subprocess.Popen(command, shell=True, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    result = process.communicate()
    
    if result[0] == '(true,)\n':
        return True
    elif result[0] == '(false,)\n':
        return False
           
while True:
    print(is_screen_locked())
    time.sleep(1)
    
