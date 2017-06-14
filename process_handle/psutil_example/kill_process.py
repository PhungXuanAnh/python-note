'''
Created on Apr 5, 2017

@author: xuananh
'''

import subprocess

import psutil


def kill(parent_pid):
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):  # or parent.children() for recursive=False
        child.kill()
    parent.kill()


proc = subprocess.Popen(["infinite_app", "param"], shell=True)
try:
    proc.wait(timeout=3)
except subprocess.TimeoutExpired:
    kill(proc.pid)