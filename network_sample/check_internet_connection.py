import socket
import traceback


def internet_is_connected(domain, port=80):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(domain)
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection((host, port), 2)
        return True
    except:
        traceback.print_exc()
        return False


print(internet_is_connected("www.google.com"))


def check_connection(host, port):
    try:
        socket.create_connection((host, port), 10)
        return True
    except:
        traceback.print_exc()
        return False

print(check_connection('localhost', 2181))
