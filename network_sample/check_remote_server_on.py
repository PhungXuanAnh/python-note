import socket
import datetime
def is_remote_server_on(server_ip, port=22):
    print(server_ip, port)
    start = datetime.datetime.now()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((server_ip, port))
        print("Port {} reachable".format(port))
        now = datetime.datetime.now()
        print("time to check: {}".format((now - start).seconds))
        s.close()
        return True
    except socket.error as e:
        print("Error on connect: %s" % e)
        now = datetime.datetime.now()
        print("time to check: {}".format((now - start).seconds))
        s.close()
        return False
    
print is_remote_server_on("10.80.200.23")