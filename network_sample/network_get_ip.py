import socket
import fcntl
import struct
import traceback
import requests
import json


def get_ip_address_interface1(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
        print("IP of '{}' is {}".format(ifname, ip))
        return ip
    except OSError:
        print("No such device: {} to get IP".format(ifname))
        return None
    except Exception:
        traceback.print_exc()
        return None


def get_ip_which_can_connect_to_internet1():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    s.connect(("google.com", 80))
    ip = s.getsockname()[0]
    print("IP addresses which can connect to internet: {}".format(ip))
    return ip


def get_ip_which_can_connect_to_internet2():
    from pyroute2 import IPRoute
    ip_addresses = []
    with IPRoute() as ipr:
        routes = ipr.route('get', dst='8.8.8.8')
        for value in list(routes):
            for v in value['attrs']:
                if v[0] == 'RTA_PREFSRC':
                    ip = v[1]
                    print("IP addresses which can connect to internet: {}".format(ip))
                    return ip


def get_all_interface_and_their_ip():
    from netifaces import interfaces, ifaddresses, AF_INET
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        print('%s: %s' % (ifaceName, ', '.join(addresses)))

def get_external_ip():
    resp = requests.get("https://ipinfo.io/json")
    print(json.dumps(resp.json(), indent=4, sort_keys=True))


if __name__ == "__main__":
    get_ip_which_can_connect_to_internet1()
    print('----------------------------------')
    get_ip_which_can_connect_to_internet2()
    print('----------------------------------')
    get_ip_address_interface1('wlo1')
    print('----------------------------------')
    get_all_interface_and_their_ip()
    print('----------------------------------')
    get_external_ip()
