import subprocess
import datetime
import time
import logging
import sys
from logging.handlers import RotatingFileHandler
    
def lock_screen():  
    command = "gnome-screensaver-command -la"
    subprocess.Popen(command, shell=True, 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.STDOUT)
def unlock_screen():
    '''
     sudo apt install xdotool -y
    '''
    password = "nghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailao"
    command = '''gnome-screensaver-command -d ;\ 
                xdotool type {}; xdotool key Return'''.format(password)
    subprocess.Popen(command, shell=True, 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.STDOUT)
    
def deactivate_screensaver():
    command = "gnome-screensaver-command -d"
    subprocess.Popen(command, shell=True, 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.STDOUT)
    
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

def working_time(times):
    '''
    @times: time to work, in second
                ex: 1200 = 20m
    '''
    start = datetime.datetime.now()
    now = datetime.datetime.now()

    while (now - start).seconds < times:
        logging.info("working time: {}".format((now - start).seconds))
        
        if is_screen_locked():
            start = now
            deactivate_screensaver()
            
        time.sleep(1)
        now = datetime.datetime.now()
        
def break_time(times):
    '''
    @times: time to work, in second
                ex: 1200 = 20m
    '''
    start = datetime.datetime.now()
    now = datetime.datetime.now()

    while (now - start).seconds < times:
        
        time.sleep(1)
        now = datetime.datetime.now()
        
        if not is_screen_locked():
            lock_screen()
            
#     unlock_screen()
    deactivate_screensaver()

def main(time_to_work, time_to_break):
    while True:
        working_time(times=time_to_work)
        break_time(times=time_to_break)
            
if __name__ == '__main__':
    '''
     sudo apt install xdotool -y
    '''
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(asctime)s] : %(message)s",
                        datefmt="%Y-%m-%d__%H:%M:%S", 
                        stream=sys.stdout,
                        )
    my_handler = RotatingFileHandler('/tmp/time_break.log', 
                                     mode='a', 
                                     maxBytes=50, 
                                     backupCount=1, 
                                     encoding=None, 
                                     delay=0)
    log_formatter = logging.Formatter("[%(asctime)s] : %(message)s", "%Y-%m-%d__%H:%M:%S")
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)
    logging.getLogger('').addHandler(my_handler)

    main(time_to_work=1200, time_to_break=120)
    
    