import sys
import time
from os.path import abspath, join, dirname

sys.path.append(abspath(join(dirname(__file__), '..')))

from time_sample import time_rest
import subprocess
import threading
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

time_rest_t = None


def allow_run(data):
    with open('/tmp/time_rest.is_run', 'w+') as f:
        f.write(data)


@app.route('/screen/unlock', methods=['GET'])
def unlock_screen():
    threading.Thread(target=kill_time_rest, args=[]).start()

    command = 'gnome-screensaver-command -d ; xdotool mousemove 100 100 ; xdotool mousemove 200 200'
    subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return jsonify({'servers': 'da nhan'})


def kill_time_rest():
    global time_rest_t

    allow_run('no')

    while time_rest_t.is_alive():
        time.sleep(1)
        pass

    command = 'gnome-screensaver-command -d ; xdotool mousemove 100 100 ; xdotool mousemove 200 200'
    subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    allow_run('yes')
    time_rest_t = threading.Thread(target=time_rest.run_time_break, args=[t_working, t_break])
    time_rest_t.start()


if __name__ == '__main__':
    allow_run('yes')
    t_working = 1800
    t_break = 300
    time_rest.logging_config()

    time_rest_t = threading.Thread(target=time_rest.run_time_break, args=[t_working, t_break])
    time_rest_t.start()

    app.run(host='0.0.0.0', port=6688, debug=False)
