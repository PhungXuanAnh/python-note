import sys
import time
from os.path import abspath, join, dirname
from flask import Flask, jsonify, abort, make_response, request, url_for
import subprocess
import threading
import socket
import requests

sys.path.append(abspath(join(dirname(__file__), '..')))
from network_sample.get_ip import get_ip_which_can_connect_to_internet1
from time_sample import time_rest


def allow_run(data):
    with open('/tmp/time_rest.is_run', 'w+') as f:
        f.write(data)


def send_computer_info(ip):
    data = {
        'name': socket.gethostname(),
        'ip': ip
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    url = 'https://ubuntu-screen-manager-1.herokuapp.com/api/v1/computer/'
    # url = 'http://localhost:5000/api/v1/computer/'
    resp = requests.post(url, json=data, headers=headers)
    print(resp.status_code)
    print(resp.text)


def check_and_update_ip():
    global current_ip
    while True:
        print('------------------------------- current ip: ' + current_ip)

        time.sleep(3)
        try:
            ip = get_ip_which_can_connect_to_internet1()
            if ip != current_ip:
                send_computer_info(ip)
                current_ip = ip
        except Exception:
            pass


current_ip = get_ip_which_can_connect_to_internet1()
app = Flask(__name__)

allow_run('yes')
t_working = 1800
t_break = 300
time_rest.logging_config()

time_rest_t = threading.Thread(target=time_rest.run_time_break, args=[t_working, t_break])
time_rest_t.start()


@app.route('/screen/unlock', methods=['GET'])
def unlock_screen():
    print(request.headers)
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
    send_computer_info(current_ip)
    threading.Thread(target=check_and_update_ip, args=[]).start()
    app.run(host='0.0.0.0', port=6688, debug=False)
