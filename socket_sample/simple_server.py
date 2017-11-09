#!/usr/bin/python

import socket
from paramiko_211.paramiko_origin_source import client

s = socket.socket()             # create socket
host = socket.gethostname()     # get local machine name
port = 12345                    # port for your service
s.bind((host, port))            # bind socket to host and port
s.listen(5)                     # wait for client connection

while True:
    c, addr = s.accept()        # establish connection with client
    print("Got connection from", addr)
    c.send("Thanh for connecting")
    c.close()                   # close the connection