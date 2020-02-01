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


def internet_is_connected(domain, port=80):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(domain)
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection((host, port), 2)
        return True
    except Exception:
        traceback.print_exc()
        return False


def check_connection(host, port):
    try:
        socket.create_connection((host, port), 10)
        return True
    except Exception:
        traceback.print_exc()
        return False


def check_ping_server(server_ip):
    import shlex
    import subprocess

    # Tokenize the shell command
    # cmd will contain  ["ping","-c1","google.com"]

    # cmd=shlex.split("ping -c1 google.com")
    cmd = shlex.split("ping -c1 {}".format(server_ip))
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        # Will print the command failed with its exit status
        print("The IP {0} is Not Reachable".format(cmd[-1]))
    else:
        print("The IP {0} is Reachable".format(cmd[-1]))


if __name__ == "__main__":
    print(check_connection('localhost', 22))
    print(internet_is_connected("www.google.com"))
    print(is_remote_server_on("localhost"))
    check_ping_server('localhost')
