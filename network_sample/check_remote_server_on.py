import socket
import datetime
def check_remote_server_on(server_ip):
    print(server_ip)
    start = datetime.datetime.now()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((server_ip, 22))
        print("Port 22 reachable")
        now = datetime.datetime.now()
        print("time to check: {}".format((now - start).seconds))
    except socket.error as e:
        print("Error on connect: %s" % e)
        now = datetime.datetime.now()
        print("time to check: {}".format((now - start).seconds))
    s.close()
    
# check_remote_server_on("10.0.1.7")
check_remote_server_on("10.64.0.180")