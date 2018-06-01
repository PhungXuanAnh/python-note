import subprocess
import datetime
import time
import logging
import sys
import os
# import dbus
from os import environ
import multiprocessing
from logging.handlers import RotatingFileHandler

pid_file = '/tmp/time_break.pid'
time_short_break = 1

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
    
def lock_screen():
    command = "gnome-screensaver-command -la"
    run_cmd(command)
    
def unlock_screen():
    '''
     sudo apt install xdotool -y
     or using command: sudo killall gnome-screensaver
    '''
    password = "nghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailaonghigiailao"
    command = '''gnome-screensaver-command -d ;\ 
                xdotool type {}; xdotool key Return'''.format(password)
    run_cmd(command)
    
def deactivate_screensaver():
    command = "gnome-screensaver-command -d"
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

def turnon_screensaver():
    command = "gnome-screensaver-command -a"
    run_cmd(command)
    
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

def play_mp3(): 
    song_file = "/media/xuananh/data/Downloads/.music/Magic-chimes.mp3"
    import pyglet    
    song = pyglet.media.load(song_file)
    song.play()
        
    def exiter(dt):
        pyglet.app.exit()
    print ("Song length is: %f" % song.duration)
    # song.duration is the song length
    pyglet.clock.schedule_once(exiter, song.duration)
        
    pyglet.app.run()    

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
#             stop_youtube()
#             pause_vlc()
#         else:
#             play_vlc()
        time.sleep(1) 
        now = datetime.datetime.now()
#     
#     stop_youtube()
#     pause_vlc()
#     lock_screen()
    
def open_image():
    import signal
    images_dir = '/media/xuananh/data/github/python-note/time_sample/images'
    command = 'eog -n {images_dir}/boss-baby-{num}.jpg'
    for i in range(1,8):
        p = subprocess.Popen(command.format(images_dir=images_dir, num=i), 
                         shell=True, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         preexec_fn=os.setsid)
        time.sleep(10)
        os.killpg(os.getpgid(p.pid), signal.SIGTERM) 
           
def break_time(times):
    global time_short_break
    if time_short_break == 3:
        lock_screen()

    start = datetime.datetime.now()
    now = datetime.datetime.now()
    
    while (now - start).seconds < times:
        logging.info("break time: {}".format((now - start).seconds))
#         play_mp3()

        open_image()
                
        # if is_screen_locked():
            # now = datetime.datetime.now()

#             lock_screen()
#             play_mp3()
        # now = datetime.datetime.now()
#         if not is_screensaver_active():
#             turnon_screensaver()
            
        # time.sleep(1)


             
#     unlock_screen()
    if is_screensaver_active():
        deactivate_screensaver()

    if time_short_break == 3:
        time_short_break = 1
    else:
        time_short_break = time_short_break + 1
    
    logging.info(time_short_break)


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

def play_vlc():
    if not is_vlc_playing():
        run_cmd("dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play")
    
def pause_vlc():
    if is_vlc_playing():
        run_cmd("dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause")
        
def is_vlc_playing():
    if 'DISPLAY' not in environ:
        exit(0)
    
    # name = "rhythmbox"
    name = 'vlc'
    if len(sys.argv) > 1:
        name = sys.argv[1]
    
    bus = dbus.SessionBus()
    
    try:
        proxy = bus.get_object("org.mpris.MediaPlayer2.%s" % name, "/org/mpris/MediaPlayer2")
        device_prop = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
    
        prop = device_prop.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    
        status = device_prop.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
    except dbus.exceptions.DBusException:
        # Probably not running.
        exit(0)
    
    if status == "Playing":
        logging.info((prop.get("xesam:artist")[0] + " - " + prop.get("xesam:title")).encode('utf-8'))
        return True
    else:
        logging.info("Not playing.")
        return False

    
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
    
def run_time_break(time_to_work=1200, time_to_break=120):
    while True:
        working_time(times=time_to_work)
        break_time(times=time_to_break)    
    
def stop_youtube():
    run_cmd("xdotool windowfocus 75497476; xdotool key Control_R+Shift_R+Down")
    
if __name__ == '__main__':
    '''
     sudo apt install xdotool -y
    '''
    t_working = 3#1200
    t_break = 2
    logging_config()
    # run_time_break(t_working, t_break)
    turnon_screensaver()
    lock_screen()
    
