#!/usr/bin/python
import subprocess
import datetime
import time
import logging
import sys
import os
from os import environ
import multiprocessing
from logging.handlers import RotatingFileHandler

pid_file = '/tmp/time_break.pid'
count_short_break = 1

def run_cmd(command):  
    process = subprocess.Popen(command, shell=True, 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.STDOUT)
    result = process.communicate()
    
    logging.debug({
        'return-code': process.poll(),
        'stdout': result[0],
        'stderr': result[1]
        })

def open_file():
    command = 'eog -f /media/xuananh/data/github/python-note/time_sample/break.jpg'
    subprocess.Popen(command, shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
    
def lock_screen():
    command = "gnome-screensaver-command -la"
    run_cmd(command)
    
def unlock_screen():
    '''
     sudo apt install xdotool -y
     or using command: sudo killall gnome-screensaver
    '''
    password = "nghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailao"
    command = '''gnome-screensaver-command -d ; xdotool type {}; xdotool key Return'''.format(password)
    run_cmd(command)
    
def deactivate_screensaver():
    command = "gnome-screensaver-command -d"
    run_cmd(command)

def turnon_screensaver():
    command = "gnome-screensaver-command -a"
    run_cmd(command)    
    
def is_screensaver_active():
    command = "gnome-screensaver-command -q"
    process = subprocess.Popen(command, shell=True, 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.STDOUT)
    result = process.communicate()
    if result[0] == 'The screensaver is active\n':
        return True
    elif result[0] == 'The screensaver is inactive\n':
        return False

def is_screen_locked():
    command = "gdbus call -e -d com.canonical.Unity -o /com/canonical/Unity/Session -m com.canonical.Unity.Session.IsLocked"
    process = subprocess.Popen(command, shell=True, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    result = process.communicate()
    
    logging.debug({
        'return-code': process.poll(),
        'stdout': result[0],
        'stderr': result[1]
        })
    
    if result[0] == '(true,)\n':
        return True
    elif result[0] == '(false,)\n':
        return False

def working_time(times):
    start = datetime.datetime.now()
    now = datetime.datetime.now()
    
    while (now - start).seconds < times:
        logging.info("working time: {}".format((now - start).seconds))
        
        if is_screen_locked() or is_screensaver_active():
            start = now
            deactivate_screensaver()
            
        time.sleep(1) 
        now = datetime.datetime.now()
    
def break_time(time_long_break, time_short_break):
    global count_short_break
    
    if count_short_break == 3:
        count_short_break = 1
        times = time_long_break
    else:
        count_short_break = count_short_break + 1
        times = time_short_break

    start = datetime.datetime.now()
    now = datetime.datetime.now()
    
    while (now - start).seconds < times:
        open_file()
        logging.info("break time: {}".format((now - start).seconds))
        
        if not is_screen_locked():
            lock_screen()
        time.sleep(1)
        now = datetime.datetime.now()
        
    if is_screensaver_active():
        deactivate_screensaver()

    logging.info(count_short_break)


def check_script_running():
    pid_file = '/tmp/time_break.pid'
    if os.path.exists(pid_file):
        old_pid = file(pid_file, 'r').read().strip()
        if os.path.exists('/proc/' + str(old_pid)) and old_pid != '' and old_pid != None:
            logging.error('time_break is running with pid {}'.format(old_pid))
            sys.exit(1)
        else:
            file(pid_file, 'w+').write(str(os.getpid()))
    else:
        file(pid_file, 'w+').write(str(os.getpid()))

def logging_config():
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s] : %(message)s",
                        datefmt="%Y-%m-%d__%H:%M:%S", 
                        stream=sys.stdout,
                        )
    my_handler = RotatingFileHandler('/tmp/time_break.log', 
                                     mode='a', 
                                     maxBytes=1024*1024, 
                                     backupCount=1, 
                                     encoding=None, 
                                     delay=0)
    log_formatter = logging.Formatter("[%(asctime)s] : %(funcName)s: %(message)s", "%Y-%m-%d__%H:%M:%S")
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)
    logging.getLogger('').addHandler(my_handler)
    
def run_time_break(time_to_work, time_long_break, time_short_break):
    while True:
        working_time(times=time_to_work)
        break_time(time_long_break, time_short_break)    
    
if __name__ == '__main__':
    '''
     install package for auto unlock screen:
     sudo apt install xdotool -y 
    '''
    t_working = 1200
    t_short_break = 20
    t_long_break = 120
    logging_config()

    process = multiprocessing.Process(name='rest_time', target=run_time_break, args=(t_working, t_long_break, t_short_break,))
    process.start()

    while True:
        if not process.is_alive():
            process = multiprocessing.Process(name='rest_time', target=run_time_break, args=(t_working, t_long_break, t_short_break,))
            process.start()

        time.sleep(5)
    
