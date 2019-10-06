import subprocess
import shlex
import sys
import select
import logging
import signal
import os
import time
import datetime
import threading
import psutil

"""
Popen starts a child processit does not wait for it to exit. 
You have to call .wait() method explicitly if you want to wait 
for the child process. In that sense, all subprocesses are 
background processes.
"""


def run_command_print_output1(command):
    """[Reference: https://stackoverflow.com/a/803396]

    Arguments:
        command {[string]} -- [command to run]
    """
    print("Running command '{}' ...".format(command))
    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT
                         )
    while True:
        out = p.stdout.readline()
        if out == b'' and p.poll() is not None:
            break
        if out != b'':
            print(out.strip().decode())
            # NOTE: trong một số trường hợp không in được màu của text trên terminal
            # lúc này phải enable color output của command, nếu có
            # tham khảo:
            # https://stackoverflow.com/questions/42589584/ansi-color-lost-when-using-python-subprocess
            # https://stackoverflow.com/questions/32486974/how-to-print-original-color-output-using-subprocess-check-output
    print("return-code = {} after run command '{}'".format(p.poll(), command))


def run_command_return_output(command):
    logging.info("Running command '{}' ...".format(command))
    logs_message = ""
    process = subprocess.Popen(shlex.split(command), shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logs_message = logs_message + output
    return {
        'return-code': process.poll(),
        'logs-message': logs_message
    }


def run_command_return_output3(command):
    logging.info("Running command '{}' ...".format(command))
    process = subprocess.Popen(shlex.split(command), shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    result = process.communicate()

    return {
        'return-code': process.poll(),
        'stdout': result[0],
        'stderr': result[1]
    }


def run_command_background(command):
    logging.info("Running command '{}' ...".format(command))
    process = subprocess.Popen(shlex.split(command), shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    print(process.pid)
    print(process.poll())
    print(process.returncode)


def run_command_with_timeout1(command, timeout):
    start = datetime.datetime.now()

    print(start)
    logging.info("Running command '{}' ...".format(command))
    p = subprocess.Popen(shlex.split(command), shell=True,
                         stdout=subprocess.PIPE,
                         preexec_fn=os.setsid)
    print("Start process with PID = {}".format(p.pid))
    while True:
        now = datetime.datetime.now()
        out = p.stdout.readline()
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

        if (now - start).seconds > timeout:
            print('Timeout happend')
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            return None, p.poll()


def run_command_with_timeout3(command, timeout):
    logging.info("Running command '{}' ...".format(command))

    def check_timeout():
        start = datetime.datetime.now()

        while True:
            now = datetime.datetime.now()
            if (now - start).seconds > timeout:
                print('Timeout happend')
#                 os.killpg(os.getpgid(process.pid), signal.SIGTERM)
#                 os.kill(process.pid, signal.SIGKILL)

                parent = psutil.Process(process.pid)
                # or parent.children() for recursive=False
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                break

    logs_message = ""
    process = subprocess.Popen(shlex.split(command), shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    print("Start process with PID = {}".format(process.pid))
    t1 = threading.Thread(target=check_timeout, args=[])
    t1.start()

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logs_message = logs_message + output
    return {
        'return-code': process.poll(),
        'logs-message': logs_message
    }


if __name__ == '__main__':
    mypass = '1'
    cmd1 = 'apt-get update'
#     cmd1 = 'mkdir /root/test1'
    cmd = "echo %s | sudo -S %s" % (mypass, cmd1)

    cmd = 'du -csh /home/xuananh/data/Downloads/PythonBook'
    cmd = 'ping 8.8.8.8 -c 10'
#     run_command_background(cmd)

    run_command_print_output1(cmd)

#     run_command_with_timeout(cmd, 10)

    # result = run_command_return_output(cmd)
    # result = run_command_with_timeout3(cmd, 5)
    # print("return-code = {}".format(result['return-code']))
    # print("logs-message = {}".format(result['logs-message']))

    # result = run_command_return_output3(cmd)
    # print("return-code = {}".format(result['return-code']))
    # print("stdout = {}".format(result['stdout'].decode('utf-8')))
    # print("stderr = {}".format(result['stderr']))
