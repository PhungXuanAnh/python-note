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


def run_command_print_output(command, print_output=True):
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
            if print_output:
                print(out.strip().decode())
            # NOTE: trong một số trường hợp không in được màu của text trên terminal
            # lúc này phải enable color output của command, nếu có
            # tham khảo:
            # https://stackoverflow.com/questions/42589584/ansi-color-lost-when-using-python-subprocess
            # https://stackoverflow.com/questions/32486974/how-to-print-original-color-output-using-subprocess-check-output
    return_code = p.poll()
    print(f"===> return-code = {return_code} after run command'")
    return return_code

def run_command_return_results(command):
    logging.info("Running command '{}' ...".format(command))
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    result = process.communicate() # NOTE: this line cause this func wait until command exit

    results = {
        'return-code': process.poll(),
        'stdout': result[0],
        'stderr': result[1]
    }
    # print(results)
    return results

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
            sys.stdout.write(out.strip().decode())
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
    # cmd = 'ping 8.8.8.8 -c 10'  # NOTE: using this cmd for test timeout
    # NOTE: to run chainging command must set shell=True
    cmd = 'cd ~/ && ls -lha | grep zsh'

    run_command_print_output(cmd)
    # run_command_return_results(cmd)
    # run_command_with_timeout1(cmd, 3)
    # run_command_with_timeout3(cmd, 3)