import socket
import fcntl
import struct

def get_ip_address_interface(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

print get_ip_address_interface('enp2s0')


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
    s.connect(("google.com", 80))
    return s.getsockname()[0]

print get_ip_address()