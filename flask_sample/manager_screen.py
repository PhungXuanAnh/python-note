#!/usr/bin/python
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


def make_publish_server(server):
    new_server = {}
    for field in server:
        if field == 'id':
            new_server['uri'] = url_for(
                'get_server', server_id=server['id'], _external=True)
        else:
            new_server[field] = server[field]
    return new_server


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/screen/unlock', methods=['GET'])
def unlock_screen():
    # threading.Thread(target=kill_time_rest, args=[]).start()

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
    time_rest_t = threading.Thread(target=time_rest.run_time_break, args=[
                                   t_working, t_long_break, t_short_break])
    time_rest_t.start()


if __name__ == '__main__':
    # allow_run('yes')
    # t_working = 1200
    # t_short_break = 20
    # t_long_break = 300
    # time_rest.logging_config()

    # time_rest_t = threading.Thread(target=time_rest.run_time_break, args=[
    #                                t_working, t_long_break, t_short_break])
    # time_rest_t.start()

    app.run(host='0.0.0.0', port=6688, debug=True)
